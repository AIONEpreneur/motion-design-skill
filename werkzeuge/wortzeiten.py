#!/usr/bin/env python3
"""Genaue Wortzeiten direkt aus der fertigen Sprachdatei (ersetzt die ungenauen Zeiten in vo.json).

Verfahren: Die finale out/vo.wav wird an echten Sprechpausen in kurze Stücke geschnitten (Stückanfang = exakter
Pegel-Einsatz). Jedes Stück wird einzeln mit whisper.cpp transkribiert (kurze Stücke -> genaue Zeiten), die Wortzeiten
werden um den Stückanfang verschoben und auf den nächsten Pegel-Einsatz im Fenster [-0,12 s, +0,08 s] eingerastet.
Ausrichtung aufs Skript per Wortabgleich; nicht erkannte Wörter werden zwischen Nachbarn interpoliert.

Nutzung:  python3 wortzeiten.py out/vo.wav out/vo.json        (überschreibt words/lines in vo.json, Sicherung vo_alt_zeiten.json)
          python3 wortzeiten.py out/vo.wav out/vo.json --nur-pruefen   (zeigt nur die Abweichungen)
"""
import json, os, re, shutil, subprocess, sys, tempfile, difflib
import numpy as np

wav, vojs = sys.argv[1], sys.argv[2]; nur = '--nur-pruefen' in sys.argv
M = os.path.expanduser('~/.cache/whisper/ggml-large-v3-turbo.bin')
ZW = {'null': '0', 'eins': '1', 'ein': '1', 'eine': '1', 'zwei': '2', 'drei': '3', 'vier': '4', 'fünf': '5', 'sechs': '6', 'sieben': '7', 'acht': '8',
      'neun': '9', 'zehn': '10', 'zwölf': '12', 'zwanzig': '20', 'dreißig': '30', 'vierzig': '40', 'fünfzig': '50', 'sechzig': '60', 'siebzig': '70', 'hundert': '100'}
def norm(t):
    t = re.sub(r'[^a-zäöüß0-9]', '', t.lower())
    return ZW.get(t, t)

with tempfile.TemporaryDirectory() as d:
    subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-i', wav, '-ar', '16000', '-ac', '1', f'{d}/a.wav'], check=True)
    raw = subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-i', f'{d}/a.wav', '-f', 'f32le', '-'], capture_output=True).stdout
    y = np.frombuffer(raw, np.float32); sr = 16000
    # Sprechstücke an echten Pausen (>= 0,12 s unter Schwelle); Stückanfänge sind am Pegel exakt
    hop = 160; e = np.array([np.sqrt((y[i:i + 320] ** 2).mean()) for i in range(0, len(y) - 320, hop)]); db = 20 * np.log10(e + 1e-6)
    fl = np.percentile(db, 15); p95 = np.percentile(db, 95); laut = db > max(fl + 12, p95 - 32)   # Einatmer (ca. p95-30 dB) zählen nicht als Sprache
    stuecke = []; i = 0; n = len(laut)
    while i < n:
        if laut[i]:
            j = i
            while j < n and (laut[j] or (j + 12 < n and laut[j:j + 12].any())): j += 1
            stuecke.append((max(0, i - 3) * .01, min(n, j + 3) * .01)); i = j
        else: i += 1
    W = []
    for k, (a0, a1) in enumerate(stuecke):
        if a1 - a0 < .15 or db[int(a0 * 100):int(a1 * 100)].max() < p95 - 22: continue   # zu kurz oder nur Atem/Geräusch
        seg = y[int(a0 * sr):int(a1 * sr)]
        import wave
        with wave.open(f'{d}/s.wav', 'wb') as wf:
            wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr); wf.writeframes((np.clip(np.concatenate([seg, np.zeros(int(.3 * sr), np.float32)]), -1, 1) * 32767).astype(np.int16).tobytes())
        subprocess.run(['whisper-cli', '-m', M, '-l', 'de', '-ml', '1', '-sow', '-oj', '-of', f'{d}/s', '-f', f'{d}/s.wav'], capture_output=True)
        try: js = json.load(open(f'{d}/s.json', encoding='utf-8'))
        except Exception: continue
        first = True
        for x in js['transcription']:
            rawtx = x['text']; tx = rawtx.strip()
            if not tx or tx.startswith('['): continue
            t = a0 + x['offsets']['from'] / 1000
            if not first and not rawtx.startswith(' ') and W:   # Wortteil ohne Leerzeichen gehört zum vorigen Wort (z. B. "Bauh"+"ütte")
                W[-1][0] += tx; continue
            if first:   # erstes Wort beginnt am ersten Stimm-Frame des Stücks (Einatmer liegen deutlich leiser und zählen nicht)
                i0 = int(a0 * 100); i1 = int(a1 * 100); pk = db[i0:i1].max() if i1 > i0 else fl
                stimm = [k for k in range(i0, i1) if db[k] > max(fl + 20, pk - 18)]
                t = (stimm[0] * .01) if stimm else a0 + .03; first = False
            if t > a1: continue
            W.append([tx, t])
W = [(norm(w), t) for w, t in W if norm(w)]
# Pegel-Einsätze (10 ms)
hop = 160; e = np.array([np.sqrt((y[i:i + 320] ** 2).mean()) for i in range(0, len(y) - 320, hop)]); db = 20 * np.log10(e + 1e-6); fl = np.percentile(db, 15)
ons = np.array([i * .01 for i in range(4, len(db)) if db[i] > fl + 15 and db[i] - db[i - 4] > 6])
def snap(t):
    if not len(ons): return t
    c = ons[(ons >= t - .05) & (ons <= t + .15)]   # whisper liegt eher zu früh
    return float(c[np.argmin(np.abs(c - t))]) if len(c) else t

vo = json.load(open(vojs, encoding='utf-8'))
S = [norm(w['w']) for w in vo['words']]
sm = difflib.SequenceMatcher(None, S, [w for w, _ in W], autojunk=False); zu = {}
for b in sm.get_matching_blocks():
    for k in range(b.size): zu[b.a + k] = b.b + k
neu = [snap(W[zu[i]][1]) if i in zu else None for i in range(len(S))]
known = [i for i in range(len(S)) if neu[i] is not None]
for i in range(len(S)):
    if neu[i] is None:
        lo = max([k for k in known if k < i], default=None); hi = min([k for k in known if k > i], default=None)
        if lo is not None and hi is not None: neu[i] = neu[lo] + (neu[hi] - neu[lo]) * (i - lo) / (hi - lo)
        else: neu[i] = vo['words'][i]['start']
abw = [(vo['words'][i]['w'], vo['words'][i]['start'], round(neu[i], 3)) for i in range(len(S))]
gross = [(w, a, b) for w, a, b in abw if abs(b - a) > .2]
print(f'{len(zu)}/{len(S)} Wörter erkannt · {len(gross)} weichen > 0,2 s ab')
for w, a, b in gross: print(f'  {w:16s} alt {a:6.2f}  neu {b:6.2f}  ({b - a:+.2f})')
if not nur:
    shutil.copy(vojs, vojs.replace('.json', '_alt_zeiten.json'))
    for i, w in enumerate(vo['words']):
        w['start'] = round(neu[i], 3)
        w['end'] = round(min(neu[i + 1] if i + 1 < len(S) else len(y) / sr, neu[i] + 1.2), 3)
    for l in vo['lines']:
        ws = [w for w in vo['words'] if w['line'] == l['i']]
        if ws: l['start'], l['end'] = ws[0]['start'], ws[-1]['end']
    json.dump(vo, open(vojs, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('geschrieben:', vojs)

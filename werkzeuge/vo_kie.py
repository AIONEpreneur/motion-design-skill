#!/usr/bin/env python3
"""Sprecherstimme über kie.ai (Gemini 2.5 Pro TTS): eine durchgehende Aufnahme des ganzen Skripts,
Prüfung per Transkription, danach Zeilen- und Wortzeiten für die Animation.

Eingabe:  skript.txt, eine Zeile pro Bild-Beat (Leerzeilen werden ignoriert).
Ausgabe:  out/vo.wav (48 kHz) und out/vo.json:
          {"duration", "stimme", "lines":[{i,text,start,end}], "words":[{w,line,start,end}]}
          Die Wortzeiten sind aufs Skript ausgerichtet: words[k] gehört zum k-ten Skriptwort.

Nutzung:
  python3 vo_kie.py skript.txt --stimme Charon --out out [--szene "Regieanweisung"] [--versuche 3]
Stimmen (Blindtest 27.09.2026, vom Nutzer gewählt): Charon (m, sachlich-lebendig), Sulafat (w, warm), Achird (m, freundlich).
Der API-Schlüssel kommt aus KIE_API_KEY bzw. ~/.claude/settings.json (env). Kosten: ~2,2 Credits je 30 s.
"""
import argparse, datetime, difflib, json, os, re, shutil, subprocess, sys, tempfile
import numpy as np

KIE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kie.py')
WHISPER = os.path.expanduser('~/.cache/whisper/ggml-large-v3-turbo.bin')
SZENE = ('Ein professioneller deutscher Werbesprecher liest einen kurzen Spot für ein regionales Unternehmen, '
         'direkt an den Kunden gerichtet. Natürliches, lebendiges Tempo, keine Monotonie, klare Betonung der Schlüsselwörter, '
         'mitfühlend beim Problem, zuversichtlich bei der Lösung. Hochdeutsch ohne Akzent.')
ap = argparse.ArgumentParser()
ap.add_argument('skript'); ap.add_argument('--stimme', default='Charon'); ap.add_argument('--out', default='out')
ap.add_argument('--szene', default=SZENE); ap.add_argument('--versuche', type=int, default=3); ap.add_argument('--vorlauf', type=float, default=0.3)
ap.add_argument('--temperatur', type=float, default=1.0)
ap.add_argument('--datei', help='vorhandene Aufnahme verwenden statt neu zu erzeugen (z. B. Blindtest-Gewinner)')
a = ap.parse_args()
if not os.environ.get('KIE_API_KEY'):
    try: os.environ['KIE_API_KEY'] = json.load(open(os.path.expanduser('~/.claude/settings.json')))['env']['KIE_API_KEY']
    except Exception: sys.exit('KIE_API_KEY fehlt: als Umgebungsvariable setzen oder in ~/.claude/settings.json unter "env" eintragen (Schlüssel: kie.ai → API Keys).')
os.makedirs(a.out, exist_ok=True)

zeilen = [l.strip() for l in open(a.skript, encoding='utf-8') if l.strip()]
text = ' '.join(zeilen)
ZAHLWORT = {'einundsiebzig': '71', 'fünfzig': '50', 'einundzwanzig': '21', 'zwanzig': '20', 'dreißig': '30', 'hundert': '100'}
def norm(t):
    w = re.sub(r'[^a-zäöüß0-9]+', ' ', t.lower()).split()
    return [ZAHLWORT.get(x, x) for x in w]
def tokens(t):  # Skriptwörter mit Zeilenzuordnung
    return [(w, li) for li, z in enumerate(zeilen) for w in norm(z)]

def whisper_json(wav16):
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(['whisper-cli', '-m', WHISPER, '-l', 'de', '-ml', '1', '-sow', '-ojf', '-dtw', 'large.v3.turbo', '-of', f'{d}/w', '-f', wav16], capture_output=True)
        return json.load(open(f'{d}/w.json', encoding='utf-8'))

# Eindeutiger Ablageordner je Projekt (mehrere Videos laufen parallel): nächster Ordnername der Form NN-name im Pfad
_teile = os.path.abspath(a.out).split(os.sep)
_slug = next((t for t in reversed(_teile) if re.match(r'^\d\d-', t)), '-'.join(_teile[-3:-1]))
ordner = os.path.join(os.path.abspath(a.out), 'stimmen')
os.makedirs(ordner, exist_ok=True)
best = None
for k in range(0 if a.datei else a.versuche):
    ziel = os.path.join(ordner, f'vo_{a.stimme}_{datetime.datetime.now():%H%M%S}_{os.getpid()}_{k + 1}.wav')
    eingabe = {'speakers': [{'speaker_id': 'Speaker 1', 'voice_name': a.stimme}], 'dialogue_turns': [{'speaker_id': 'Speaker 1', 'text': text}],
               'scene': a.szene, 'temperature': a.temperatur}
    r = subprocess.run([sys.executable, KIE, 'run', 'google/gemini-2-5-pro-tts', json.dumps(eingabe, ensure_ascii=False), ziel], capture_output=True, text=True)
    if r.returncode != 0 or not os.path.exists(ziel):
        print('  kie.ai-Fehler:', (r.stderr or r.stdout).strip().splitlines()[-1:]); continue
    print('  ' + r.stdout.strip().splitlines()[-1])
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-i', ziel, '-ar', '16000', '-ac', '1', f'{d}/a.wav'], check=True)
        j = whisper_json(f'{d}/a.wav')
    gehoert = ' '.join(s['text'] for s in j['transcription'])
    q = difflib.SequenceMatcher(None, norm(text), norm(gehoert), autojunk=False).ratio()
    print(f'  Versuch {k + 1}: Übereinstimmung {q:.3f}')
    if best is None or q > best[0]: best = (q, ziel, j)
    if q >= 0.97: break
if a.datei:
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-i', a.datei, '-ar', '16000', '-ac', '1', f'{d}/a.wav'], check=True)
        j = whisper_json(f'{d}/a.wav')
    best = (difflib.SequenceMatcher(None, norm(text), norm(' '.join(s['text'] for s in j['transcription'])), autojunk=False).ratio(), a.datei, j)
if best is None: raise SystemExit('Keine Aufnahme von kie.ai erhalten.')
q, quelle, j = best
if q < 0.97: print(f'  ! beste Aufnahme nur {q:.3f} – bitte anhören')

# Audio: auf 48 kHz, Stille am Anfang auf „vorlauf“ normieren
with tempfile.TemporaryDirectory() as d:
    subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-i', quelle, '-ar', '48000', '-ac', '1', '-c:a', 'pcm_f32le', f'{d}/a.wav'], check=True)
    import soundfile as sf
    y, sr = sf.read(f'{d}/a.wav', dtype='float32')
laut = np.where(np.abs(y) > 0.01)[0]; kopf = laut[0] / sr if len(laut) else 0.0
y = np.concatenate([np.zeros(int(a.vorlauf * sr), np.float32), y[max(0, laut[0] - int(.02 * sr)) if len(laut) else 0:]])
y = y / max(1e-6, np.abs(y).max()) * .89
versatz = a.vorlauf - kopf + .02

# Wortzeiten (Whisper, DTW) aufs Skript ausrichten
W = []
for s in j['transcription']:
    for w in norm(s['text']):
        W.append((w, s['offsets']['from'] / 1000 + versatz, s['offsets']['to'] / 1000 + versatz))
S = tokens(text)
sm = difflib.SequenceMatcher(None, [w for w, _ in S], [w for w, _, _ in W], autojunk=False)
zu = {}
for b in sm.get_matching_blocks():
    for i in range(b.size): zu[b.a + i] = b.b + i
starts = [W[zu[i]][1] if i in zu else None for i in range(len(S))]
ends = [W[zu[i]][2] if i in zu else None for i in range(len(S))]
bek = [i for i in range(len(S)) if starts[i] is not None]
for i in range(len(S)):  # Lücken linear füllen
    if starts[i] is None:
        lo = max([b for b in bek if b < i], default=None); hi = min([b for b in bek if b > i], default=None)
        t0 = ends[lo] if lo is not None else versatz; t1 = starts[hi] if hi is not None else len(y) / sr
        n = (hi if hi is not None else len(S)) - (lo if lo is not None else -1)
        k = i - (lo if lo is not None else -1); starts[i] = t0 + (t1 - t0) * (k - 1) / n; ends[i] = t0 + (t1 - t0) * k / n
# Phrasenweise an echten Sprechpausen einrasten: Whisper liegt je Phrase um bis zu ±0,4 s daneben.
hop = int(.01 * sr); en = np.array([np.sqrt((y[i:i + hop] ** 2).mean()) for i in range(0, len(y) - hop, hop)]); still = en < .012
pend = [i * .01 for i in range(1, len(still)) if still[i - 1] and not still[i] and still[max(0, i - 15):i].all()]  # Ende einer Pause >= 0,15 s
for k, pe in enumerate(pend):
    cand = [i for i in range(len(S)) if abs(starts[i] - pe) < .45]
    if not cand: continue
    i0 = min(cand, key=lambda i: abs(starts[i] - pe)); d = pe - starts[i0]
    nxt = pend[k + 1] if k + 1 < len(pend) else 1e9
    for i in range(i0, len(S)):
        if starts[i] + d >= nxt - .05 and i > i0: break
        starts[i] += d; ends[i] += d
surf = []  # Originalschreibweise je Skriptwort (für Untertitel)
for z in zeilen:
    for tok in z.split():
        n = len(norm(tok)); surf += [tok] + [''] * (n - 1) if n else []
surf += [''] * (len(S) - len(surf))
words = [{'w': w, 'text': surf[i], 'line': li, 'start': round(starts[i], 3), 'end': round(ends[i], 3)} for i, (w, li) in enumerate(S)]
lines = []
for li, z in enumerate(zeilen):
    ws = [x for x in words if x['line'] == li]
    lines.append({'i': li, 'text': z, 'start': ws[0]['start'] if ws else 0, 'end': ws[-1]['end'] if ws else 0})
sf.write(os.path.join(a.out, 'vo.wav'), y, sr)
json.dump({'duration': round(len(y) / sr, 3), 'stimme': 'kie/gemini-2.5-pro-tts:' + a.stimme, 'quelle': quelle, 'uebereinstimmung': round(q, 3), 'lines': lines, 'words': words},
          open(os.path.join(a.out, 'vo.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'{a.out}/vo.wav  {len(y) / sr:.2f} s  Stimme {a.stimme}  (Übereinstimmung {q:.3f})')
for l in lines: print(f"  {l['start']:6.2f}–{l['end']:6.2f}  {l['text']}")

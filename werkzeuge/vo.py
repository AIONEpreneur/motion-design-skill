#!/usr/bin/env python3
"""Sprecherstimme: eine durchgehende Aufnahme des ganzen Skripts, Prüfung per Transkription, danach Zeilen- und Wortzeiten
für die Animation.

Anbieter:
  elevenlabs (Standard)  Wortzeiten kommen aus den Zeitmarken je Zeichen, die ElevenLabs mitliefert.
  kie                    Gemini 2.5 Pro TTS über kie.ai, Wortzeiten per whisper.cpp.

Eingabe:  skript.txt, eine Zeile pro Bild-Beat (Leerzeilen werden ignoriert).
          Mit eleven_v3 sind Audio-Tags in eckigen Klammern erlaubt, z. B. „[concerned] Montagmorgen.“ Sie steuern nur den
          Tonfall, werden nicht gesprochen und tauchen in vo.json nicht als Wörter auf. Andere Modelle bekommen den Text ohne Tags.
Ausgabe:  out/vo.wav (48 kHz) und out/vo.json:
          {"duration", "stimme", "zeiten", "lines":[{i,text,start,end}], "words":[{w,text,line,start,end}]}
          Die Wortzeiten sind aufs Skript ausgerichtet: words[k] gehört zum k-ten Skriptwort.

Nutzung:
  python3 vo.py skript.txt --stimme <Name oder Voice-ID> --out out [--modell eleven_v3] [--stabilitaet 0.5] [--versuche 3]
  python3 vo.py skript.txt --anbieter kie --stimme Charon --out out [--szene "Regieanweisung"]
Ohne --stimme nimmt ElevenLabs die erste Stimme aus ELEVENLABS_STIMMEN, kie.ai nimmt Charon.
Schlüssel: ELEVENLABS_API_KEY bzw. KIE_API_KEY in schluessel.txt im Skill-Ordner (legt pruefen.py an).
Kosten: ElevenLabs rechnet nach Zeichen ab (30-s-Skript ≈ 500–600 Zeichen je Versuch), kie.ai ~2,2 Credits je 30 s.
"""
import argparse, datetime, difflib, json, os, re, shutil, subprocess, sys, tempfile
import numpy as np

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import elevenlabs as el

WHISPER = os.path.expanduser('~/.cache/whisper/ggml-large-v3-turbo.bin')
SZENE = ('Ein professioneller deutscher Werbesprecher liest einen kurzen Spot für ein regionales Unternehmen, '
         'direkt an den Kunden gerichtet. Natürliches, lebendiges Tempo, keine Monotonie, klare Betonung der Schlüsselwörter, '
         'mitfühlend beim Problem, zuversichtlich bei der Lösung. Hochdeutsch ohne Akzent.')
ERSATZMODELL = 'eleven_multilingual_v2'   # falls das gewählte Modell gar nichts liefert
ap = argparse.ArgumentParser()
ap.add_argument('skript'); ap.add_argument('--anbieter', choices=['elevenlabs', 'kie'], default='elevenlabs')
ap.add_argument('--stimme'); ap.add_argument('--out', default='out')
ap.add_argument('--modell', help='nur ElevenLabs, Standard eleven_v3 bzw. ELEVENLABS_MODELL')
ap.add_argument('--stabilitaet', type=float, default=0.5, help='nur ElevenLabs: 0.0 kreativ, 0.5 natürlich, 1.0 robust')
ap.add_argument('--szene', default=SZENE, help='nur kie: Regieanweisung als freier Text')
ap.add_argument('--temperatur', type=float, default=1.0, help='nur kie')
ap.add_argument('--versuche', type=int, default=3); ap.add_argument('--vorlauf', type=float, default=0.3)
ap.add_argument('--datei', help='vorhandene Aufnahme verwenden statt neu zu erzeugen (z. B. Blindtest-Gewinner), Wortzeiten per whisper')
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
whisper_da = bool(shutil.which('whisper-cli')) and os.path.exists(WHISPER)

TAG = re.compile(r'\[[^\]]*\]')
roh = [l.strip() for l in open(a.skript, encoding='utf-8') if l.strip()]
def ohne_tags(z): return re.sub(r'\s+', ' ', TAG.sub(' ', z)).strip()
zeilen = [ohne_tags(l) for l in roh if ohne_tags(l)]
text = ' '.join(zeilen)
ZAHLWORT = {'einundsiebzig': '71', 'fünfzig': '50', 'einundzwanzig': '21', 'zwanzig': '20', 'dreißig': '30', 'hundert': '100'}
def norm(t):
    w = re.sub(r'[^a-zäöüß0-9]+', ' ', t.lower()).split()
    return [ZAHLWORT.get(x, x) for x in w]
S = [(w, li) for li, z in enumerate(zeilen) for w in norm(z)]   # Skriptwörter mit Zeilenzuordnung

def whisper_json(datei):
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-i', datei, '-ar', '16000', '-ac', '1', f'{d}/a.wav'], check=True)
        subprocess.run(['whisper-cli', '-m', WHISPER, '-l', 'de', '-ml', '1', '-sow', '-ojf', '-dtw', 'large.v3.turbo', '-of', f'{d}/w', '-f', f'{d}/a.wav'],
                       capture_output=True)
        try: return json.load(open(f'{d}/w.json', encoding='utf-8'))
        except (OSError, ValueError): print('  ! whisper hat kein Ergebnis geliefert'); return None

def uebereinstimmung(j):
    gehoert = ' '.join(s['text'] for s in j['transcription'])
    return difflib.SequenceMatcher(None, norm(text), norm(gehoert), autojunk=False).ratio()

# ---------- Aufnahme ----------
ordner = os.path.join(os.path.abspath(a.out), 'stimmen')
os.makedirs(ordner, exist_ok=True)
def dateiname(etikett, k, endung):
    etikett = re.sub(r'[^A-Za-z0-9ÄÖÜäöüß_-]+', '-', etikett)[:30]
    return os.path.join(ordner, f'vo_{etikett}_{datetime.datetime.now():%H%M%S}_{os.getpid()}_{k + 1}{endung}')

if a.anbieter == 'elevenlabs':
    modell = a.modell or el.MODELL
    wunsch = a.stimme or (el.stammstimmen() or [None])[0]
    if a.datei:
        voice_id, stimmname = None, a.stimme or os.path.basename(a.datei)
    elif not wunsch:
        sys.exit('Keine Stimme: --stimme <Name oder Voice-ID> angeben oder ELEVENLABS_STIMMEN setzen.')
    else:
        voice_id, stimmname = el.stimme_aufloesen(wunsch)
    def tts_zeilen(m):   # Audio-Tags versteht nur eleven_v3
        return roh if m.startswith('eleven_v3') else zeilen
    if any(TAG.search(l) for l in roh) and not modell.startswith('eleven_v3'):
        print(f'  Hinweis: Audio-Tags entfernt, {modell} versteht sie nicht.')
    zeichen = 0
    def erzeugen(k, m):
        global zeichen
        t = ' '.join(tts_zeilen(m))
        r = el.sprich(t, voice_id, dateiname(stimmname, k, el.endung()), m, a.stabilitaet)
        zeichen += r['zeichen']
        return r['datei'], r['alignment'], t
    stimme_json = f'elevenlabs/{modell}:{stimmname}'
else:
    import kie
    if not os.environ.get('KIE_API_KEY'):
        os.environ['KIE_API_KEY'] = el.einstellung('KIE_API_KEY')
    if not os.environ['KIE_API_KEY'] and not a.datei:
        sys.exit(f'KIE_API_KEY fehlt: in {el.SCHLUESSELDATEI} eintragen (Schlüssel: kie.ai → API Keys).')
    if not whisper_da:
        sys.exit('whisper.cpp mit Modell fehlt, ohne Transkription gibt es mit kie.ai keine Wortzeiten (siehe werkzeuge/pruefen.py).')
    stimmname = a.stimme or 'Charon'; modell = 'google/gemini-2-5-pro-tts'; voice_id = None
    def erzeugen(k, m):
        ziel = dateiname(stimmname, k, '.wav')
        eingabe = {'speakers': [{'speaker_id': 'Speaker 1', 'voice_name': stimmname}],
                   'dialogue_turns': [{'speaker_id': 'Speaker 1', 'text': text}], 'scene': a.szene, 'temperature': a.temperatur}
        kie.run(modell, eingabe, ziel)
        if not os.path.exists(ziel): raise RuntimeError('keine Datei von kie.ai erhalten')
        return ziel, None, text
    stimme_json = 'kie/gemini-2.5-pro-tts:' + stimmname

best = None   # (übereinstimmung, quelle, whisper-json, alignment, gesendeter text)
if a.datei:
    if not whisper_da: sys.exit('Für --datei braucht es whisper.cpp mit Modell (Wortzeiten).')
    j = whisper_json(a.datei); best = (uebereinstimmung(j) if j else None, a.datei, j, None, text)
else:
    plan = [modell] * a.versuche
    for k in range(len(plan) + 1):
        if k == len(plan):   # alle Versuche ohne Ergebnis: einmal mit dem bewährten Modell
            if best is not None or a.anbieter != 'elevenlabs' or modell == ERSATZMODELL: break
            print(f'  {modell} lieferte nichts, letzter Versuch mit {ERSATZMODELL}'); m = ERSATZMODELL
        else:
            m = plan[k]
        try:
            quelle, al, gesendet = erzeugen(k, m)
        except Exception as e:
            print(f'  Versuch {k + 1}: {e}'); continue
        j = whisper_json(quelle) if whisper_da else None
        q = uebereinstimmung(j) if j else None
        if not al and not j:   # weder Zeitmarken noch Transkription: keine Wortzeiten möglich
            print(f'  Versuch {k + 1}: ohne Zeitmarken und ohne whisper, nicht verwendbar'); continue
        print(f'  Versuch {k + 1}: ' + (f'Übereinstimmung {q:.3f}' if q is not None else 'ohne Textprüfung')
              + ('' if al or a.anbieter != 'elevenlabs' else ', ohne Zeitmarken'))
        if m != modell: stimme_json = stimme_json.replace(modell, m, 1)
        if best is None or (q or 0) > (best[0] or 0): best = (q, quelle, j, al, gesendet)
        if q is None or q >= 0.97: break
if best is None: raise SystemExit(f'Keine Aufnahme von {a.anbieter} erhalten.')
q, quelle, j, al, gesendet = best
if q is not None and q < 0.97: print(f'  ! beste Aufnahme nur {q:.3f} – bitte anhören')
if not whisper_da: print('  ! whisper fehlt: Text nicht geprüft, Aufnahme bitte anhören')

# ---------- Audio: auf 48 kHz, Stille am Anfang auf „vorlauf“ normieren ----------
import soundfile as sf
with tempfile.TemporaryDirectory() as d:
    subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-i', quelle, '-ar', '48000', '-ac', '1', '-c:a', 'pcm_f32le', f'{d}/a.wav'], check=True)
    y, sr = sf.read(f'{d}/a.wav', dtype='float32')
laut = np.where(np.abs(y) > 0.01)[0]
schnitt = max(0, laut[0] - int(.02 * sr)) if len(laut) else 0
y = np.concatenate([np.zeros(int(a.vorlauf * sr), np.float32), y[schnitt:]])
y = y / max(1e-6, np.abs(y).max()) * .89
versatz = a.vorlauf - schnitt / sr   # Zeit in der Quelle + versatz = Zeit in vo.wav

# Sprechpausen >= 0,15 s: Ende jeder Pause
hop = int(.01 * sr); en = np.array([np.sqrt((y[i:i + hop] ** 2).mean()) for i in range(0, len(y) - hop, hop)]); still = en < .012
pend = [i * .01 for i in range(1, len(still)) if still[i - 1] and not still[i] and still[max(0, i - 15):i].all()]

def spannen(tz):
    """Zeichenbereiche der Skriptwörter im gesendeten Text, Audio-Tags ausgenommen."""
    out, pos = [], 0
    for z in tz:
        tags = [m.span() for m in TAG.finditer(z)]
        klein = ''.join(c.lower() if len(c.lower()) == 1 else c for c in z)
        out += [(pos + m.start(), pos + m.end()) for m in re.finditer(r'[a-zäöüß0-9]+', klein)
                if not any(t0 <= m.start() < t1 for t0, t1 in tags)]
        pos += len(z) + 1
    return out

def zeiten_elevenlabs():
    """Wortzeiten aus den Zeitmarken je Zeichen. None, wenn sie nicht zum Skript passen."""
    ch = al.get('characters') or []; st = al.get('character_start_times_seconds') or []; et = al.get('character_end_times_seconds') or []
    if not ch or len(ch) != len(st) or len(ch) != len(et): return None
    tz = roh if gesendet == ' '.join(roh) else zeilen
    sp = spannen(tz)
    if len(sp) != len(S): return None
    flach = [k for k, c in enumerate(ch) for _ in c]; gesamt = ''.join(ch)
    if gesamt == gesendet: zu = dict(enumerate(flach))
    else:   # ElevenLabs hat den Text leicht anders zurückgegeben: zeichenweise ausrichten
        zu = {}
        for b in difflib.SequenceMatcher(None, gesendet, gesamt, autojunk=False).get_matching_blocks():
            for i in range(b.size): zu[b.a + i] = flach[b.b + i]
    starts, ends = [], []
    for s0, s1 in sp:
        ks = [zu[i] for i in range(s0, s1) if i in zu]
        starts.append(st[ks[0]] + versatz if ks else None); ends.append(et[ks[-1]] + versatz if ks else None)
    if sum(s is None for s in starts) > len(S) // 5: return None
    # Gleichbleibenden Versatz (z. B. Decoder-Verzögerung) an den Pausenenden messen und herausrechnen
    d = []
    for pe in pend:
        nah = [s for s in starts if s is not None and abs(s - pe) < .3]
        if nah: d.append(pe - min(nah, key=lambda s: abs(s - pe)))
    if len(d) >= 3:
        med = float(np.median(d))
        if .02 < abs(med) <= .15:
            print(f'  Zeitmarken um {med:+.3f} s an die Sprechpausen angeglichen')
            starts = [s + med if s is not None else None for s in starts]; ends = [e + med if e is not None else None for e in ends]
        elif abs(med) > .15:
            print(f'  ! Zeitmarken liegen im Mittel {med:+.2f} s neben den Sprechpausen – mit wortzeiten.py --nur-pruefen nachsehen')
    return starts, ends

def zeiten_whisper():
    """Wortzeiten per whisper (DTW), aufs Skript ausgerichtet und phrasenweise an echten Sprechpausen eingerastet."""
    W = []
    for s in j['transcription']:
        for w in norm(s['text']):
            W.append((w, s['offsets']['from'] / 1000 + versatz, s['offsets']['to'] / 1000 + versatz))
    sm = difflib.SequenceMatcher(None, [w for w, _ in S], [w for w, _, _ in W], autojunk=False)
    zu = {}
    for b in sm.get_matching_blocks():
        for i in range(b.size): zu[b.a + i] = b.b + i
    starts = [W[zu[i]][1] if i in zu else None for i in range(len(S))]
    ends = [W[zu[i]][2] if i in zu else None for i in range(len(S))]
    return starts, ends

def luecken_fuellen(starts, ends):
    bek = [i for i in range(len(S)) if starts[i] is not None]
    for i in range(len(S)):   # Lücken linear füllen
        if starts[i] is None:
            lo = max([b for b in bek if b < i], default=None); hi = min([b for b in bek if b > i], default=None)
            t0 = ends[lo] if lo is not None else a.vorlauf; t1 = starts[hi] if hi is not None else len(y) / sr
            n = (hi if hi is not None else len(S)) - (lo if lo is not None else -1)
            k = i - (lo if lo is not None else -1); starts[i] = t0 + (t1 - t0) * (k - 1) / n; ends[i] = t0 + (t1 - t0) * k / n

zeiten = None
if al:
    zeiten = zeiten_elevenlabs()
    if zeiten is None: print('  ! Zeitmarken von ElevenLabs passen nicht zum Skript, nehme whisper')
quelle_zeiten = 'elevenlabs' if zeiten else 'whisper'
if zeiten is None:
    if j is None: sys.exit('Keine brauchbaren Zeitmarken und kein whisper: Wortzeiten nicht bestimmbar.')
    starts, ends = zeiten_whisper(); luecken_fuellen(starts, ends)
    # Phrasenweise an echten Sprechpausen einrasten: whisper liegt je Phrase um bis zu ±0,4 s daneben.
    for k, pe in enumerate(pend):
        cand = [i for i in range(len(S)) if abs(starts[i] - pe) < .45]
        if not cand: continue
        i0 = min(cand, key=lambda i: abs(starts[i] - pe)); dd = pe - starts[i0]
        nxt = pend[k + 1] if k + 1 < len(pend) else 1e9
        for i in range(i0, len(S)):
            if starts[i] + dd >= nxt - .05 and i > i0: break
            starts[i] += dd; ends[i] += dd
else:
    starts, ends = zeiten; luecken_fuellen(starts, ends)

surf = []   # Originalschreibweise je Skriptwort (für Untertitel)
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
json.dump({'duration': round(len(y) / sr, 3), 'stimme': stimme_json, 'stimme_id': voice_id, 'zeiten': quelle_zeiten, 'quelle': quelle,
           'uebereinstimmung': round(q, 3) if q is not None else None, 'lines': lines, 'words': words},
          open(os.path.join(a.out, 'vo.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'{a.out}/vo.wav  {len(y) / sr:.2f} s  Stimme {stimmname}  Wortzeiten: {quelle_zeiten}'
      + (f'  (Übereinstimmung {q:.3f})' if q is not None else ''))
for l in lines: print(f"  {l['start']:6.2f}–{l['end']:6.2f}  {l['text']}")
if a.anbieter == 'elevenlabs' and not a.datei:
    try:
        g = el.guthaben()
        print(f"  ElevenLabs: {zeichen} Zeichen für diese Aufnahme · {g['character_count']} von {g['character_limit']} im Tarif {g['tier']} verbraucht")
    except Exception:
        print(f'  ElevenLabs: {zeichen} Zeichen für diese Aufnahme')

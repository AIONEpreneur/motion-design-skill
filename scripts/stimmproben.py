#!/usr/bin/env python3
"""Drei Hörproben über kie.ai (Gemini 2.5 Pro TTS): derselbe Anfang des Sprechertexts mit mehreren Stimmen.

Jede Probe wird per whisper geprüft:
- Liest die Stimme mehr als den Text (etwa Wörter aus der Regieanweisung), wird hinter dem letzten Textwort abgeschnitten.
- Fehlen Wörter, wird die Probe einmal neu erzeugt.

Nutzung:
  python3 stimmproben.py --text "Montagmorgen. Ihr Server ist aus." --szene "Regieanweisung …" --out proben/ [--stimmen Charon,Sulafat,Achird]
Ausgabe:  proben/probe_<Stimme>.mp4 (AAC, im Browser abspielbar) und proben/proben.json
Kosten:   rund 0,3–0,9 Credits je Probe
"""
import argparse, concurrent.futures as cf, json, os, re, subprocess, sys, tempfile

KIE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'werkzeuge', 'kie.py')
WHISPER = os.path.expanduser('~/.cache/whisper/ggml-large-v3-turbo.bin')
ap = argparse.ArgumentParser()
ap.add_argument('--text', required=True); ap.add_argument('--szene', required=True); ap.add_argument('--out', required=True)
ap.add_argument('--stimmen', default='Charon,Sulafat,Achird'); ap.add_argument('--temperatur', type=float, default=1.0)
a = ap.parse_args()
if not os.environ.get('KIE_API_KEY'):
    try: os.environ['KIE_API_KEY'] = json.load(open(os.path.expanduser('~/.claude/settings.json')))['env']['KIE_API_KEY']
    except Exception: sys.exit('KIE_API_KEY fehlt: als Umgebungsvariable setzen oder in ~/.claude/settings.json unter "env" eintragen (Schlüssel: kie.ai → API Keys).')
os.makedirs(a.out, exist_ok=True)
ZW = {'null': '0', 'eins': '1', 'zwei': '2', 'drei': '3', 'vier': '4', 'fünf': '5', 'sechs': '6', 'sieben': '7', 'acht': '8', 'neun': '9', 'zehn': '10',
      'zwölf': '12', 'zwanzig': '20', 'dreißig': '30', 'fünfzig': '50', 'hundert': '100', 'einundsiebzig': '71'}
def norm(t): return [ZW.get(w, w) for w in re.sub(r'[^a-zäöüß0-9]+', ' ', t.lower()).split()]
SOLL = norm(a.text)

def woerter(wav):
    """whisper-Wortliste [(wort, start, ende)] einer Aufnahme."""
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', wav, '-ar', '16000', '-ac', '1', f'{d}/a.wav'], check=True)
        subprocess.run(['whisper-cli', '-m', WHISPER, '-l', 'de', '-ml', '1', '-sow', '-oj', '-of', f'{d}/w', '-f', f'{d}/a.wav'], capture_output=True)
        js = json.load(open(f'{d}/w.json', encoding='utf-8'))
    out = []
    for x in js['transcription']:
        for w in norm(x['text']):
            out.append((w, x['offsets']['from'] / 1000, x['offsets']['to'] / 1000))
    return out

def probe(stimme):
    wav = os.path.join(a.out, f'probe_{stimme}.wav')
    for versuch in (1, 2):
        eingabe = {'speakers': [{'speaker_id': 'Speaker 1', 'voice_name': stimme}], 'dialogue_turns': [{'speaker_id': 'Speaker 1', 'text': a.text}],
                   'scene': a.szene, 'temperature': a.temperatur}
        r = subprocess.run([sys.executable, KIE, 'run', 'google/gemini-2-5-pro-tts', json.dumps(eingabe, ensure_ascii=False), wav], capture_output=True, text=True)
        if not os.path.exists(wav):
            fehler = (r.stderr or r.stdout).strip().splitlines()[-1:]
            if versuch == 2: return {'stimme': stimme, 'ok': False, 'fehler': fehler}
            continue
        ist = woerter(wav); namen = [w for w, _, _ in ist]
        if namen[:len(SOLL)] == SOLL or all(w in namen for w in SOLL):
            ende = None
            if len(namen) > len(SOLL):   # zu viel gelesen: hinter dem letzten Sollwort schneiden
                idx = max(i for i, w in enumerate(namen) if w == SOLL[-1] and i < len(SOLL) + 3)
                ende = ist[idx][2] + 0.25
            mp4 = wav.replace('.wav', '.mp4')
            filt = ['-t', f'{ende:.2f}', '-af', f'afade=t=out:st={ende - 0.15:.2f}:d=0.15'] if ende else []
            subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', wav, *filt, '-c:a', 'aac', '-b:a', '128k', '-f', 'mp4', mp4], check=True)
            return {'stimme': stimme, 'ok': True, 'datei': mp4, 'wav': wav, 'gekuerzt_bei': ende, 'gehört': ' '.join(namen)}
        if versuch == 2: return {'stimme': stimme, 'ok': False, 'fehler': 'Text weicht ab: ' + ' '.join(namen)}
    return {'stimme': stimme, 'ok': False}

with cf.ThreadPoolExecutor(4) as ex:
    res = list(ex.map(probe, a.stimmen.split(',')))
json.dump({'text': a.text, 'szene': a.szene, 'proben': res}, open(os.path.join(a.out, 'proben.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for r in res: print(r['stimme'], 'ok' if r['ok'] else 'FEHLER', r.get('datei') or r.get('fehler'))

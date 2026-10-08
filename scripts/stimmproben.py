#!/usr/bin/env python3
"""Drei Hörproben: derselbe Anfang des Sprechertexts mit mehreren Stimmen.

Anbieter:
  elevenlabs (Standard)  Stimmen als Namen eigener Stimmen oder als Voice-IDs, ohne --stimmen aus ELEVENLABS_STIMMEN.
                         Regie über Audio-Tags im Text (nur eleven_v3), z. B. "[concerned] Montagmorgen. Ihr Server ist aus."
  kie                    Gemini 2.5 Pro TTS über kie.ai, Stimmen Charon, Sulafat, Achird, Regie über --szene.

Jede Probe wird per whisper geprüft (wenn installiert):
- Liest die Stimme mehr als den Text (etwa Wörter aus der Regieanweisung), wird hinter dem letzten Textwort abgeschnitten.
- Fehlen Wörter, wird die Probe einmal neu erzeugt.

Nutzung:
  python3 stimmproben.py --text "[concerned] Montagmorgen. Ihr Server ist aus." --stimmen "Meine Stimme,<voice-id>,<voice-id>" --out proben/
  python3 stimmproben.py --anbieter kie --text "Montagmorgen. Ihr Server ist aus." --szene "Regieanweisung …" --out proben/ [--stimmen Charon,Sulafat,Achird]
Ausgabe:  proben/probe_<Stimme>.mp4 (AAC, im Browser abspielbar) und proben/proben.json
Kosten:   ElevenLabs nach Zeichen (eine Probe ≈ 50–150 Zeichen), kie.ai rund 0,3–0,9 Credits je Probe
"""
import argparse, concurrent.futures as cf, json, os, re, shutil, subprocess, sys, tempfile

W = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'werkzeuge')
sys.path.insert(0, W)
import elevenlabs as el

WHISPER = os.path.expanduser('~/.cache/whisper/ggml-large-v3-turbo.bin')
ap = argparse.ArgumentParser()
ap.add_argument('--anbieter', choices=['elevenlabs', 'kie'], default='elevenlabs')
ap.add_argument('--text', required=True); ap.add_argument('--out', required=True)
ap.add_argument('--stimmen', help='Komma-Liste; ElevenLabs: Namen eigener Stimmen oder Voice-IDs')
ap.add_argument('--szene', help='nur kie: Regieanweisung als freier Text')
ap.add_argument('--modell', help='nur ElevenLabs, Standard eleven_v3 bzw. ELEVENLABS_MODELL')
ap.add_argument('--stabilitaet', type=float, default=0.5, help='nur ElevenLabs: 0.0 kreativ, 0.5 natürlich, 1.0 robust')
ap.add_argument('--temperatur', type=float, default=1.0, help='nur kie')
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
whisper_da = bool(shutil.which('whisper-cli')) and os.path.exists(WHISPER)
ZW = {'null': '0', 'eins': '1', 'zwei': '2', 'drei': '3', 'vier': '4', 'fünf': '5', 'sechs': '6', 'sieben': '7', 'acht': '8', 'neun': '9', 'zehn': '10',
      'zwölf': '12', 'zwanzig': '20', 'dreißig': '30', 'fünfzig': '50', 'hundert': '100', 'einundsiebzig': '71'}
def norm(t): return [ZW.get(w, w) for w in re.sub(r'[^a-zäöüß0-9]+', ' ', t.lower()).split()]
rein = re.sub(r'\s+', ' ', re.sub(r'\[[^\]]*\]', ' ', a.text)).strip()   # Text ohne Audio-Tags
SOLL = norm(rein)

if a.anbieter == 'elevenlabs':
    wunsch = [s.strip() for s in a.stimmen.split(',') if s.strip()] if a.stimmen else el.stammstimmen()
    if not wunsch:
        sys.exit('Keine Stimmen: --stimmen "Name,Voice-ID,…" angeben oder ELEVENLABS_STIMMEN setzen.\n'
                 f'Vorschläge: python3 "{W}/elevenlabs.py" bibliothek --sprache de   ·   eigene: python3 "{W}/elevenlabs.py" stimmen')
    try: liste = el.eigene_stimmen()
    except Exception: liste = None
    stimmen = [el.stimme_aufloesen(s, liste) for s in wunsch]   # [(voice_id, name)]
    modell = a.modell or el.MODELL
    sendetext = a.text if modell.startswith('eleven_v3') else rein
    def erzeugen(stimme, basis):
        return el.sprich(sendetext, stimme[0], basis + el.endung(), modell, a.stabilitaet)['datei']
else:
    KIE = os.path.join(W, 'kie.py')
    if not os.environ.get('KIE_API_KEY'):
        os.environ['KIE_API_KEY'] = el.einstellung('KIE_API_KEY')
    if not os.environ['KIE_API_KEY']:
        sys.exit(f'KIE_API_KEY fehlt: in {el.SCHLUESSELDATEI} eintragen (Schlüssel: kie.ai → API Keys).')
    if not a.szene:
        sys.exit('--szene fehlt: kie.ai braucht die Regieanweisung als freien Text.')
    stimmen = [(s.strip(), s.strip()) for s in (a.stimmen or 'Charon,Sulafat,Achird').split(',') if s.strip()]
    def erzeugen(stimme, basis):
        ziel = basis + '.wav'
        eingabe = {'speakers': [{'speaker_id': 'Speaker 1', 'voice_name': stimme[0]}], 'dialogue_turns': [{'speaker_id': 'Speaker 1', 'text': rein}],
                   'scene': a.szene, 'temperature': a.temperatur}
        r = subprocess.run([sys.executable, KIE, 'run', 'google/gemini-2-5-pro-tts', json.dumps(eingabe, ensure_ascii=False), ziel], capture_output=True, text=True)
        if not os.path.exists(ziel):
            raise RuntimeError(' '.join((r.stderr or r.stdout).strip().splitlines()[-1:]))
        return ziel

def woerter(datei):
    """whisper-Wortliste [(wort, start, ende)] einer Aufnahme."""
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', datei, '-ar', '16000', '-ac', '1', f'{d}/a.wav'], check=True)
        subprocess.run(['whisper-cli', '-m', WHISPER, '-l', 'de', '-ml', '1', '-sow', '-oj', '-of', f'{d}/w', '-f', f'{d}/a.wav'], capture_output=True)
        try: js = json.load(open(f'{d}/w.json', encoding='utf-8'))
        except (OSError, ValueError): return []
    out = []
    for x in js['transcription']:
        for w in norm(x['text']):
            out.append((w, x['offsets']['from'] / 1000, x['offsets']['to'] / 1000))
    return out

def als_mp4(quelle, mp4, ende=None):
    filt = ['-t', f'{ende:.2f}', '-af', f'afade=t=out:st={ende - 0.15:.2f}:d=0.15'] if ende else []
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', quelle, *filt, '-c:a', 'aac', '-b:a', '128k', '-f', 'mp4', mp4], check=True)

def probe(stimme):
    vid, name = stimme
    basis = os.path.join(a.out, 'probe_' + re.sub(r'[^A-Za-z0-9ÄÖÜäöüß_-]+', '-', name)[:30])
    erg = {'stimme': name, 'id': vid if a.anbieter == 'elevenlabs' else None}
    for versuch in (1, 2):
        try:
            quelle = erzeugen(stimme, basis)
        except Exception as e:
            if versuch == 2: return {**erg, 'ok': False, 'fehler': str(e)}
            continue
        if not whisper_da:   # ohne whisper keine Prüfung: Probe unverändert ausliefern
            als_mp4(quelle, basis + '.mp4')
            return {**erg, 'ok': True, 'datei': basis + '.mp4', 'quelle': quelle, 'geprueft': False}
        ist = woerter(quelle); namen = [w for w, _, _ in ist]
        if namen and (namen[:len(SOLL)] == SOLL or all(w in namen for w in SOLL)):
            ende = None
            if len(namen) > len(SOLL):   # zu viel gelesen: hinter dem letzten Sollwort schneiden
                idx = max((i for i, w in enumerate(namen) if w == SOLL[-1] and i < len(SOLL) + 3), default=None)
                ende = ist[idx][2] + 0.25 if idx is not None else None
            als_mp4(quelle, basis + '.mp4', ende)
            return {**erg, 'ok': True, 'datei': basis + '.mp4', 'quelle': quelle, 'gekuerzt_bei': ende, 'gehört': ' '.join(namen)}
        if versuch == 2: return {**erg, 'ok': False, 'fehler': 'Text weicht ab: ' + ' '.join(namen)}
    return {**erg, 'ok': False}

with cf.ThreadPoolExecutor(3) as ex:
    res = list(ex.map(probe, stimmen))
json.dump({'anbieter': a.anbieter, 'text': a.text, 'szene': a.szene, 'proben': res},
          open(os.path.join(a.out, 'proben.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for r in res: print(r['stimme'], r['id'] or '', 'ok' if r['ok'] else 'FEHLER', r.get('datei') or r.get('fehler'))
if not whisper_da: print('Hinweis: whisper fehlt, die Proben sind ungeprüft.')

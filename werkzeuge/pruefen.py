#!/usr/bin/env python3
"""Prüft, ob alles für den Erklärvideo-Skill installiert ist, und sagt, wie man Fehlendes nachholt.

Nutzung: python3 werkzeuge/pruefen.py               (öffnet schluessel.txt im Texteditor, wenn der Schlüssel fehlt)
         python3 werkzeuge/pruefen.py --schluessel  (öffnet schluessel.txt immer, z. B. um den Schlüssel zu ändern)
"""
import glob, importlib.util, os, platform, shutil, subprocess, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import elevenlabs as el
MAC = platform.system() == 'Darwin'
ok_alle = True

def zeile(ok, was, hilfe=''):
    global ok_alle
    ok_alle &= ok
    print(('✅ ' if ok else '❌ ') + was + ('' if ok or not hilfe else '\n     → ' + hilfe))

# Programme
zeile(shutil.which('node') is not None, 'Node.js', 'https://nodejs.org (Version 20 oder neuer)')
zeile(os.path.isdir(os.path.join(HIER, 'node_modules', 'puppeteer-core')), 'Node-Pakete der Werkzeuge', f'cd "{HIER}" && npm install')
zeile(shutil.which('ffmpeg') is not None, 'ffmpeg', 'brew install ffmpeg' if MAC else 'https://ffmpeg.org/download.html')
zeile(shutil.which('whisper-cli') is not None, 'whisper.cpp (whisper-cli) für die Wortzeiten', 'brew install whisper-cpp' if MAC else 'https://github.com/ggml-org/whisper.cpp')
modell = os.path.expanduser('~/.cache/whisper/ggml-large-v3-turbo.bin')
zeile(os.path.exists(modell), 'Whisper-Sprachmodell (1,6 GB)',
      'mkdir -p ~/.cache/whisper && curl -L -o ~/.cache/whisper/ggml-large-v3-turbo.bin '
      'https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin')

# Python-Pakete
fehlt = [m for m in ('numpy', 'soundfile', 'PIL') if importlib.util.find_spec(m) is None]
zeile(not fehlt, 'Python-Pakete (numpy, soundfile, Pillow)', 'python3 -m pip install numpy soundfile pillow')

# Chrome zum Rendern (gleiche Suche wie render.mjs)
chrome = os.environ.get('CHROME') if os.environ.get('CHROME') and os.path.exists(os.environ['CHROME']) else None
if not chrome:
    for p in sorted(glob.glob(os.path.expanduser('~/.cache/puppeteer/chrome-headless-shell/*/chrome-headless-shell-*/chrome-headless-shell*')), reverse=True):
        chrome = p; break
if not chrome:
    for p in ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/usr/bin/google-chrome', '/usr/bin/chromium',
              r'C:\Program Files\Google\Chrome\Application\chrome.exe']:
        if os.path.exists(p): chrome = p; break
zeile(chrome is not None, 'Chrome zum Rendern' + (f' ({chrome})' if chrome else ''),
      f'cd "{HIER}" && npx @puppeteer/browsers install chrome-headless-shell@stable --path ~/.cache/puppeteer')

# Schlüssel für die Stimmen: stehen in schluessel.txt. ElevenLabs ist Pflicht, kie.ai nur Ausweichweg.
def oeffnen(pfad):
    """Öffnet die Datei im Standard-Texteditor (TextEdit, Editor, …)."""
    try:
        if MAC: subprocess.run(['open', '-t', pfad], check=True)
        elif platform.system() == 'Windows': os.startfile(pfad)
        else: subprocess.run(['xdg-open', pfad], check=True)
        return True
    except Exception:
        return False
datei = el.schluesseldatei_anlegen()
key = el.einstellung('ELEVENLABS_API_KEY')
offen = oeffnen(datei) if (not key or '--schluessel' in sys.argv) else False
zeile(bool(key), 'ElevenLabs-Schlüssel für die Stimmen',
      ('Die Schlüsseldatei ist jetzt im Texteditor offen' if offen else f'Datei öffnen: {datei}') +
      '. Schlüssel (elevenlabs.io → Developers → API Keys) hinter ELEVENLABS_API_KEY= einfügen, speichern, erneut prüfen.')
if key and offen:
    print(f'ℹ️  Schlüsseldatei ist im Texteditor offen: {datei}')
if el.einstellung('ELEVENLABS_STIMMEN'):
    print('ℹ️  Feste Stimmen (ELEVENLABS_STIMMEN): ' + el.einstellung('ELEVENLABS_STIMMEN'))
print('ℹ️  kie.ai-Schlüssel (nur für --anbieter kie): ' + ('vorhanden' if el.einstellung('KIE_API_KEY') else 'nicht eingetragen'))

print('\nAlles bereit. Sag in Claude Code: „Ich brauche ein Erklärvideo für meine Firma.“' if ok_alle else '\nBitte die ❌-Punkte nachholen und dann erneut prüfen.')

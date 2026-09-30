#!/usr/bin/env python3
"""Prüft, ob alles für den Erklärvideo-Skill installiert ist, und sagt, wie man Fehlendes nachholt.

Nutzung: python3 werkzeuge/pruefen.py
"""
import glob, importlib.util, json, os, platform, shutil, subprocess

HIER = os.path.dirname(os.path.abspath(__file__))
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

# kie.ai-Schlüssel (Stimmen)
key = os.environ.get('KIE_API_KEY')
if not key:
    try: key = json.load(open(os.path.expanduser('~/.claude/settings.json')))['env']['KIE_API_KEY']
    except Exception: key = None
zeile(bool(key), 'kie.ai-Schlüssel für die Stimmen',
      'Schlüssel auf kie.ai → API Keys anlegen und in ~/.claude/settings.json eintragen: {"env": {"KIE_API_KEY": "…"}}')

print('\nAlles bereit. Sag in Claude Code: „Ich brauche ein Erklärvideo für meine Firma.“' if ok_alle else '\nBitte die ❌-Punkte nachholen und dann erneut prüfen.')

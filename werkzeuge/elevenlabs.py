#!/usr/bin/env python3
"""ElevenLabs-Client für die Sprecherstimme.

Nur Standardbibliothek, kein pip. Der Schlüssel kommt aus ELEVENLABS_API_KEY
bzw. ~/.claude/settings.json (env).

    # Eigene Stimmen im Konto (auch geklonte)
    python3 elevenlabs.py stimmen

    # Deutsche Stimmen aus der Bibliothek suchen (kostenlos)
    python3 elevenlabs.py bibliothek --sprache de --geschlecht female --einsatz advertisement --anzahl 20

    # Bibliotheksstimme ins eigene Konto holen (nötig, bevor die API sie spricht)
    python3 elevenlabs.py hinzufuegen <public_owner_id> <voice_id> [name]

    # Sprechen mit Zeitmarken je Zeichen (verbraucht Zeichen-Kontingent)
    python3 elevenlabs.py sprich <stimme> "<text>" <ziel.mp3> [--modell eleven_v3] [--stabilitaet 0.5]

    # Verbrauch und Kontingent
    python3 elevenlabs.py guthaben

<stimme> ist eine Voice-ID oder der Name einer eigenen Stimme.
Optionale Einstellungen (Umgebung oder ~/.claude/settings.json → env):
  ELEVENLABS_STIMMEN  feste Stimmen für die Hörproben, Komma-Liste aus Namen oder Voice-IDs
  ELEVENLABS_MODELL   Modell, Standard eleven_v3 (versteht Audio-Tags wie [warmly])
"""
import base64, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request, wave

def einstellung(name, standard=''):
    """Wert aus der Umgebung, sonst aus ~/.claude/settings.json (env)."""
    wert = os.environ.get(name, '').strip()
    if not wert:
        try: wert = str(json.load(open(os.path.expanduser('~/.claude/settings.json')))['env'][name]).strip()
        except Exception: wert = ''
    return wert or standard


BASE = einstellung('ELEVENLABS_BASE', 'https://api.elevenlabs.io').rstrip('/')
MODELL = einstellung('ELEVENLABS_MODELL', 'eleven_v3')
FORMAT = 'mp3_44100_128'   # auf allen Tarifen erlaubt; WAV/PCM mit 44,1 kHz erst ab Pro


def schluessel():
    key = einstellung('ELEVENLABS_API_KEY')
    if not key:
        raise SystemExit('ELEVENLABS_API_KEY fehlt: als Umgebungsvariable setzen oder in ~/.claude/settings.json unter "env" '
                         'eintragen (Schlüssel: elevenlabs.io → Developers → API Keys).')
    return key


def stammstimmen():
    """Feste Stimmen aus ELEVENLABS_STIMMEN (Komma-Liste aus Namen oder Voice-IDs), sonst leer."""
    return [s.strip() for s in einstellung('ELEVENLABS_STIMMEN').split(',') if s.strip()]


def _req(pfad, method='GET', body=None, params=None, timeout=180):
    url = f'{BASE}/{pfad.lstrip("/")}'
    if params:
        url += '?' + urllib.parse.urlencode({k: v for k, v in params.items() if v is not None}, doseq=True)
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header('xi-api-key', schluessel())
    req.add_header('Content-Type', 'application/json')
    req.add_header('Accept', 'application/json')
    for versuch in range(5):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode() or '{}')
        except urllib.error.HTTPError as e:
            txt = e.read().decode(errors='replace')
            # 429: zu viele gleichzeitige Anfragen für den Tarif, kurz warten
            if e.code in (429, 500, 502, 503, 504) and versuch < 4:
                time.sleep(3 * (versuch + 1)); continue
            hinweis = ''
            try:
                d = json.loads(txt).get('detail')
                if isinstance(d, dict):
                    if d.get('status') == 'voice_not_found':
                        hinweis = ' (Bibliotheksstimme? Erst mit „elevenlabs.py hinzufuegen <owner> <voice_id>“ ins Konto holen.)'
                    d = d.get('message', d)
                txt = d
            except Exception: pass
            raise RuntimeError(f'ElevenLabs HTTP {e.code}: {txt}{hinweis}')
        except urllib.error.URLError:
            if versuch < 4:
                time.sleep(3 * (versuch + 1)); continue
            raise
    raise RuntimeError('Anfrage nach fünf Versuchen fehlgeschlagen')


def eigene_stimmen():
    """Alle Stimmen im Konto: [{voice_id, name, category, labels, description, preview_url}]."""
    out, token = [], None
    while True:
        d = _req('v2/voices', params={'page_size': 100, 'next_page_token': token})
        out += d.get('voices', [])
        token = d.get('next_page_token')
        if not d.get('has_more') or not token: return out


def bibliothek(sprache='de', geschlecht=None, alter=None, akzent=None, einsatz=None, suche=None,
               anzahl=20, sortierung='cloned_by_count'):
    """Stimmen aus der öffentlichen Bibliothek. Stimmen mit Aufpreis bleiben draußen."""
    d = _req('v1/shared-voices', params={'language': sprache, 'gender': geschlecht, 'age': alter, 'accent': akzent,
                                         'use_cases': einsatz, 'search': suche, 'page_size': min(100, anzahl),
                                         'sort': sortierung, 'include_custom_rates': 'false'})
    return d.get('voices', [])


def hinzufuegen(owner, voice_id, name=None):
    """Holt eine Bibliotheksstimme ins Konto. Belegt einen Stimmplatz."""
    return _req(f'v1/voices/add/{owner}/{voice_id}', 'POST', {'new_name': name or voice_id})


def guthaben():
    d = _req('v1/user/subscription')
    return {k: d.get(k) for k in ('tier', 'character_count', 'character_limit', 'next_character_count_reset_unix',
                                  'voice_slots_used', 'voice_limit')}


def stimme_aufloesen(stimme, liste=None):
    """Voice-ID oder Name einer eigenen Stimme -> (voice_id, name)."""
    ist_id = re.fullmatch(r'[A-Za-z0-9]{20}', stimme)
    try:
        liste = eigene_stimmen() if liste is None else liste
    except Exception as e:   # Schlüssel ohne Leserecht für Stimmen: IDs gehen trotzdem
        if ist_id: return stimme, stimme
        raise SystemExit(f'Eigene Stimmen nicht lesbar ({e}). Voice-ID statt Namen angeben.')
    for v in liste:
        if stimme == v.get('voice_id') or stimme.strip().lower() == (v.get('name') or '').strip().lower():
            return v['voice_id'], v.get('name') or v['voice_id']
    if ist_id:
        return stimme, stimme   # nicht im Konto: Bibliotheksstimme vorher mit „hinzufuegen“ holen
    namen = ', '.join(v.get('name') or v['voice_id'] for v in liste) or 'keine'
    raise SystemExit(f'Stimme „{stimme}“ gibt es im Konto nicht. Eigene Stimmen: {namen}')


def sprich(text, voice_id, ziel, modell=None, stabilitaet=None, sprache='de', format=FORMAT, seed=None):
    """Erzeugt Sprache samt Zeitmarken je Zeichen und speichert die Audiodatei.

    Rückgabe: {'datei', 'alignment' (characters, character_start_times_seconds, character_end_times_seconds) oder None,
               'zeichen', 'modell'}. Zeiten beziehen sich auf den Originaltext inklusive Audio-Tags.
    """
    modell = modell or MODELL
    body = {'text': text, 'model_id': modell}
    if not modell.startswith('eleven_multilingual'):   # multilingual_v2 kennt language_code nicht
        body['language_code'] = sprache
    if stabilitaet is not None:
        body['voice_settings'] = {'stability': float(stabilitaet)}   # eleven_v3: nur 0.0 (kreativ), 0.5 (natürlich), 1.0 (robust)
    if seed is not None:
        body['seed'] = int(seed)
    d = _req(f'v1/text-to-speech/{voice_id}/with-timestamps', 'POST', body, params={'output_format': format})
    roh = d.get('audio_base64')
    if not roh:
        raise RuntimeError('ElevenLabs hat keine Audiodaten geliefert')
    audio = base64.b64decode(roh)
    os.makedirs(os.path.dirname(os.path.abspath(ziel)), exist_ok=True)
    if format.startswith('pcm_'):   # rohe 16-bit-Samples: in WAV verpacken
        with wave.open(ziel, 'wb') as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(int(format.split('_')[1])); w.writeframes(audio)
    else:
        open(ziel, 'wb').write(audio)
    return {'datei': ziel, 'alignment': d.get('alignment'), 'zeichen': len(text), 'modell': modell}


def endung(format=FORMAT):
    return '.mp3' if format.startswith('mp3') else '.opus' if format.startswith('opus') else '.wav'


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description='ElevenLabs-Client', usage=__doc__)
    sub = ap.add_subparsers(dest='befehl', required=True)
    sub.add_parser('stimmen')
    b = sub.add_parser('bibliothek')
    b.add_argument('--sprache', default='de'); b.add_argument('--geschlecht'); b.add_argument('--alter'); b.add_argument('--akzent')
    b.add_argument('--einsatz'); b.add_argument('--suche'); b.add_argument('--anzahl', type=int, default=20)
    b.add_argument('--sortierung', default='cloned_by_count'); b.add_argument('--json', action='store_true')
    h = sub.add_parser('hinzufuegen'); h.add_argument('owner'); h.add_argument('voice_id'); h.add_argument('name', nargs='?')
    sub.add_parser('guthaben')
    s = sub.add_parser('sprich'); s.add_argument('stimme'); s.add_argument('text'); s.add_argument('ziel')
    s.add_argument('--modell'); s.add_argument('--stabilitaet', type=float)
    a = ap.parse_args()

    if a.befehl == 'stimmen':
        for v in eigene_stimmen():
            lb = v.get('labels') or {}
            print(f"{v['voice_id']}  {v.get('name', ''):28s} {v.get('category', ''):12s} "
                  f"{' · '.join(x for x in (lb.get('gender'), lb.get('age'), lb.get('accent'), lb.get('language')) if x)}")

    elif a.befehl == 'bibliothek':
        vs = bibliothek(a.sprache, a.geschlecht, a.alter, a.akzent, a.einsatz, a.suche, a.anzahl, a.sortierung)
        if a.json:
            print(json.dumps(vs, ensure_ascii=False, indent=1))
        for v in ([] if a.json else vs):
            print(f"{v['voice_id']}  owner={v['public_owner_id']}  {v['name']}\n"
                  f"    {v.get('gender')} · {v.get('age')} · {v.get('accent')} · {v.get('use_case')} · {v.get('descriptive')}"
                  f" · {v.get('cloned_by_count')}× genutzt\n"
                  f"    {(v.get('description') or '').strip()[:160]}\n    Hörprobe: {v.get('preview_url')}")

    elif a.befehl == 'hinzufuegen':
        print(json.dumps(hinzufuegen(a.owner, a.voice_id, a.name), ensure_ascii=False))

    elif a.befehl == 'guthaben':
        g = guthaben()
        print(f"Tarif {g['tier']} · {g['character_count']} von {g['character_limit']} Zeichen verbraucht · "
              f"Stimmplätze {g['voice_slots_used']}/{g['voice_limit']}")

    elif a.befehl == 'sprich':
        vid, name = stimme_aufloesen(a.stimme)
        r = sprich(a.text, vid, a.ziel, a.modell, a.stabilitaet)
        print(json.dumps({'datei': r['datei'], 'stimme': name, 'zeichen': r['zeichen'], 'zeitmarken': bool(r['alignment'])},
                         ensure_ascii=False))

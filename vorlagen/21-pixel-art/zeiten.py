#!/usr/bin/env python3
"""V7: Leitet alle Bildzeitpunkte (K) aus den neu gemessenen Wortzeiten in out/vo.json ab
(out/vo.json mit werkzeuge/wortzeiten.py neu vermessen, Schlüsselwörter an der Pegelkurve geprüft: "geprueft": "pegel").
Schreibt film/zeiten.js (für den Film) und out/zeiten.json (für ton/partitur.py). Im Film stehen nur Abstände zu diesen K."""
import json
j = json.load(open('out/vo.json', encoding='utf-8'))
W = j['words']
def wort(w, n=1, dt=0.0):  # n-tes Vorkommen eines Skriptworts
    hits = [x for x in W if x['w'] == w]
    return round(hits[n - 1]['start'] + dt, 3)
def zeile(i, dt=0.0): return round(j['lines'][i]['start'] + dt, 3)
K = dict(durch=wort('durchgefallen'), schon=wort('schon'), zwei=zeile(1), fehler=wort('fehler'), links1=wort('linksabbiegen', 1),
         dabei=zeile(2), sechs=wort('sechs'), wochen=wort('wochen'), job=wort('job'), und1=zeile(3), ohne=wort('ohne'), auto=wort('auto'),
         kommen=wort('kommen'), nicht=wort('nicht'), hin=wort('hin'),
         bei=zeile(4), gruen=wort('grün', 1), pfeil=wort('pfeil', 1), ueben=wort('üben'), schwach=wort('schwachstelle'), zehn=zeile(5), links2=wort('linksabbiegen', 2),
         sitzt=wort('sitzt'), dann=zeile(6), probe=wort('probeprüfung'), echten=wort('echten'), strecke=wort('strecke'), und2=zeile(7), diesmal=wort('diesmal'),
         bestanden=wort('bestanden'), mont=zeile(8), selbst=wort('selbst'), arbeit=wort('arbeit'), fahr=zeile(9), gruen2=wort('grün', 2),
         erste=wort('erste'), kostenlos=wort('kostenlos'))
DUR = round(j['duration'] + 1.4, 2)
open('film/zeiten.js', 'w').write(f'// erzeugt von zeiten.py aus out/vo.json ({j["stimme"]}, Wortzeiten neu vermessen und an der Pegelkurve geprüft)\nconst K = {json.dumps(K)};\nconst DUR = {DUR};\n')
json.dump({'K': K, 'DUR': DUR}, open('out/zeiten.json', 'w'), indent=1)
print(DUR, K)

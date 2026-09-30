#!/usr/bin/env python3
"""V7: Leitet alle Bildzeitpunkte (K) und Szenenschnitte (CUT) aus den neu gemessenen Wortzeiten in out/vo.json ab
(out/vo.json mit werkzeuge/wortzeiten.py neu vermessen, Schlüsselwörter an der Pegelkurve geprüft: "geprueft": "pegel").
Schreibt film/zeiten.js (für den Film) und out/zeiten.json (für ton/partitur.py)."""
import json
j = json.load(open('out/vo.json', encoding='utf-8'))
W = j['words']
def wort(w, n=1, dt=0.0):  # n-tes Vorkommen eines Skriptworts
    hits = [x for x in W if x['w'] == w]
    return round(hits[n - 1]['start'] + dt, 3)
def zeile(i, dt=0.0): return round(j['lines'][i]['start'] + dt, 3)
K = dict(sonntag=wort('sonntagabend'), schreibt=wort('schreibt'), wasser=wort('wasser'), kueche=wort('küche'),
         rufen=zeile(1), handwerker=wort('handwerker'), an=wort('an'), niemand=wort('niemand'), ran=wort('ran'),
         dazu=zeile(2), n20=wort('20'), nachrichten=wort('nachrichten'), belege=wort('belege'),
         wochenende=wort('wochenende'), weg=wort('weg'),
         mit=zeile(4), domus=wort('domus', 1), anders=wort('anders'),
         meldet=zeile(5), meldet_w=wort('meldet'), schaden=wort('schaden'), portal=wort('portal'), foto=wort('foto'),
         dreissig=zeile(6), n30=wort('30'), minuten=wort('minuten'), notdienst=wort('notdienst'), beauftragt=wort('beauftragt', 1),
         live0=zeile(7), live=wort('live'), gemeldet=wort('gemeldet'), beauftragt2=wort('beauftragt', 2), erledigt=wort('erledigt'),
         bleiben=zeile(8), esstisch=wort('esstisch'), sitzen=wort('sitzen'),
         schluss=zeile(9), monat=wort('monat'), kostenlos=wort('kostenlos'))
# Schnitte aus K: jeweils vor dem ersten Wort der neuen Zeile
CUT = dict(cd=round(K['dazu'] - .25, 2), ef0=round(K['mit'] - .6, 2), ef1=round(K['mit'] - .33, 2), gh=round(K['dreissig'] - .55, 2),
           h=round(K['live0'] - .49, 2), ij0=round(K['bleiben'] - .42, 2), ij1=round(K['bleiben'] - .14, 2), end=round(K['schluss'] - .38, 2))
DUR = round(j['duration'] + 1.4, 2)
open('film/zeiten.js', 'w').write(f'// erzeugt von zeiten.py aus out/vo.json ({j["stimme"]}, Wortzeiten neu vermessen)\nconst K = {json.dumps(K)};\nconst CUT = {json.dumps(CUT)};\nconst DUR = {DUR};\n')
json.dump({'K': K, 'CUT': CUT, 'DUR': DUR}, open('out/zeiten.json', 'w'), indent=1)
print(DUR, CUT); print(K)

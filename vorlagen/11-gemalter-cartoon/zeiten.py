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
K = dict(klammert=wort('klammert'), tuer=wort('tür'), bloss=wort('bloß'), zahnarzt=wort('zahnarzt'),
         dabei=zeile(1), backenzahn=wort('backenzahn'), seit=wort('seit'), tagen=wort('tagen'), weh=wort('weh'),
         jedes=zeile(2), warten=wort('warten'), macht=wort('macht'), loch=wort('loch'), groesser=wort('größer'),
         angst0=zeile(3), angst=wort('angst'), bleibt=wort('bleibt'), ein=wort('ein'), leben=wort('leben'), lang=wort('lang'),
         bei=zeile(4), zahnfee=wort('zahnfee', 1), anders=wort('anders'),
         besuch0=zeile(5), besuch=wort('besuch', 1), gespielt=wort('gespielt'),
         loecher0=zeile(6), loecher=wort('löcher'), behandeln=wort('behandeln'), ohne=wort('ohne'), bohren=wort('bohren'),
         nach=zeile(7), n20=wort('20'), minuten=wort('minuten'), vorbei=wort('vorbei'),
         und=zeile(8), kind2=wort('kind', 2), wieder=wort('wiederkommen'),
         schluss=zeile(9), kza=wort('kinderzahnarzt'), kennen=wort('besuch', 2), kostenlos=wort('kostenlos'))
# Szenenanfänge aus K (Iris/Wischblende davor)
CUT = dict(bc=round(K['dabei'] - .17, 2), d=round(K['angst0'] - .46, 2), ef=round(K['bei'] - .34, 2), g=round(K['loecher0'] - .12, 2),
           h=round(K['nach'] - .1, 2), i=round(K['und'] - .3, 2), j=round(K['schluss'] - .49, 2))
DUR = round(j['duration'] + 1.4, 2)
open('film/zeiten.js', 'w').write(f'// erzeugt von zeiten.py aus out/vo.json ({j["stimme"]}, Wortzeiten neu vermessen)\nconst K = {json.dumps(K)};\nconst CUT = {json.dumps(CUT)};\nconst DUR = {DUR};\n')
json.dump({'K': K, 'CUT': CUT, 'DUR': DUR}, open('out/zeiten.json', 'w'), indent=1)
print(DUR, CUT); print(K)

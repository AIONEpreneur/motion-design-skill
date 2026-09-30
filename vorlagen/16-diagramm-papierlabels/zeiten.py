#!/usr/bin/env python3
"""Leitet die Bildzeitpunkte (K) aus den Wortzeiten in out/vo.json ab.
Schreibt film/zeiten.js (für den Film) und out/zeiten.json (für ton/partitur.py)."""
import json
j = json.load(open('out/vo.json', encoding='utf-8'))
W = j['words']
def wort(w, n=1, dt=0.0):  # n-tes Vorkommen eines Skriptworts
    hits = [x for x in W if x['w'] == w]
    return round(hits[n - 1]['start'] + dt, 3)
def zeile(i, dt=0.0): return round(j['lines'][i]['start'] + dt, 3)
K = dict(gas=wort('gasrechnung'), betrag=wort('dreitausendzweihundert'), euro=wort('euro'), jahr=wort('jahr', 1),
         kessel=wort('kessel'), keller=wort('keller'), alt25=wort('fünfundzwanzig'), alt=wort('alt'),
         faellt=zeile(2), januar=wort('januar'), aus=wort('aus'), kalt=wort('kalt'),
         dabei=zeile(3), draussen=wort('draußen'), waerme=wort('wärme'), sogar=wort('sogar'), minus=wort('minus'), grad=wort('grad'),
         werk=zeile(4), pumpe=wort('wärmepumpe'), drei=wort('drei'), tagen=wort('tagen'),
         antrag=wort('förderantrag'), bis=wort('bis'), siebzig=wort('siebzig'), zuschuss=wort('zuschuss'),
         danach=zeile(6), warm=wort('warm'), heizkosten=wort('heizkosten'), sinken=wort('sinken'), drittel=wort('drittel'),
         marke=zeile(7), haustechnik=wort('haustechnik'), beratung=wort('beratung'), kostenlos=wort('kostenlos'))
DUR = round(j['duration'] + 1.4, 2)
open('film/zeiten.js', 'w').write(f'// erzeugt von zeiten.py aus out/vo.json ({j["stimme"]})\nconst K = {json.dumps(K)};\nconst DUR = {DUR};\n')
json.dump({'K': K, 'DUR': DUR}, open('out/zeiten.json', 'w'), indent=1)
print(DUR, K)

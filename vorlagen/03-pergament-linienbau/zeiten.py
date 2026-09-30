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
K = dict(fleck=wort('fleck'), wand=wort('wand'), altbau=wort('altbaus'), waechst=wort('wächst'), dahinter=wort('dahinter'), balken=wort('balken', 1), schimmel=wort('schimmel'),
         wer=zeile(2), drueber=wort('drüberstreicht'), riskiert=wort('riskiert'), haus=wort('haus', 1), bh=zeile(3), sehen=wort('sehen'), genau=wort('genau'),
         jeder=zeile(4), riss=wort('riss'), zgenau=wort('zentimetergenau'), vermessen=wort('vermessen'), plan=wort('plan'), bleibt=wort('bleibt', 1), ersetzt=wort('ersetzt'),
         gebaut=zeile(6), kalk=wort('kalk'), holz=wort('holz'), damals=wort('damals'), ihr=zeile(7), trocken=wort('trocken'), n100=wort('100'), jahre=wort('jahre'),
         ende=zeile(8), erst=wort('erstgespräch'), kostenlos=wort('kostenlos'))
# V7: Wortzeiten aus werkzeuge/wortzeiten.py (echte Einsätze), drei Einatmer-Fehlgriffe in vo.json korrigiert (siehe korrektur_v7).
K.update(und=wort('und', 1), nasse=wort('nasse'), das=wort('das', 1), ganze=wort('ganze'), erst2=wort('erst'), hin=wort('hin'), jeder2=wort('jeder', 2),
         im=wort('im'), wird2=wort('wird', 2), gebaut=wort('gebaut'), mit=wort('mit'), wie=wort('wie'), haus2=wort('haus', 2), bleibt2=wort('bleibt', 2),
         naechsten=wort('nächsten'), das2=wort('das', 2), ist=wort('ist'), bh=wort('bauhütte', 1), ende=wort('bauhütte', 2))
K['lampe'] = round(K['bh'] - .2, 3)
# Szenenwechsel (in den Sprechpausen, vor dem ersten Bildwort der neuen Szene)
CUT = dict(b=3.45, c=6.45, d=7.4, e=round(K['bh'] - .22, 2), f=11.95, g=15.4, h=18.35, i=21.3, j=24.6)
K['cut'] = CUT
DUR = round(j['duration'] + 1.4, 2)
open('film/zeiten.js', 'w').write(f'// erzeugt von zeiten.py aus out/vo.json ({j["stimme"]})\nconst K = {json.dumps(K)};\nconst DUR = {DUR};\n')
json.dump({'K': K, 'DUR': DUR}, open('out/zeiten.json', 'w'), indent=1)
print(DUR, K)

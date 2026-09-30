#!/usr/bin/env python3
"""V7: Leitet alle Bildzeitpunkte (K) und Szenenschnitte (CUT) aus den neu gemessenen Wortzeiten in out/vo.json ab
(out/vo.json mit werkzeuge/wortzeiten.py neu vermessen, Schlüsselwörter an der Pegelkurve geprüft: "geprueft": "pegel").
Schreibt film/zeiten.js (für den Film) und out/zeiten.json (für ton/partitur.py). Im Film stehen nur Abstände zu diesen K."""
import json
j = json.load(open('out/vo.json', encoding='utf-8'))
W = j['words']
def wort(w, n=1, dt=0.0):  # n-tes Vorkommen eines Skriptworts
    hits = [x for x in W if x['w'] == w]
    return round(hits[n - 1]['start'] + dt, 3)
def zeile(i, dt=0.0): return round(j['lines'][i]['start'] + dt, 3)
K = dict(sams=wort('samstag'), nacht=wort('nachtdienst'), zwei1=wort('zwei', 1), pflege=wort('pflegekräfte'), fallen=wort('fallen'), krank=zeile(1), hier=wort('hier'),
         anrufe=wort('anrufe'), da=wort('da'), luecken=wort('lücken'), ueberall=wort('überall'), und1=zeile(2), selbst=wort('selbst'),
         zum=zeile(3), dritten=wort('dritten'), monat=wort('monat'), mit=zeile(4), pb1=wort('pflegebrücke', 1), melden=wort('melden', 1), luecke=wort('lücke'),
         in1=wort('in'), zwei2=wort('zwei', 2), minuten=wort('minuten'), wir=zeile(5), gepr=wort('geprüfte'), fach=wort('fachkräfte'), aus2=wort('aus', 2), region=wort('region'),
         nach=zeile(6), spaet=wort('spätestens'), n48=wort('achtundvierzig'), stunden=wort('stunden'), ist=wort('ist'), schicht=wort('schicht', 1), besetzt=wort('besetzt'),
         und2=zeile(7), ihr=wort('ihr'), sams2=wort('samstag', 2), gehoert=wort('gehört'), ihnen=wort('ihnen'), pb=zeile(8), personal=wort('personal'),
         melden2=wort('melden', 2), heute=wort('heute'), offene=wort('offene'), schicht2=wort('schicht', 2))
# Schnitte: kurz vor dem ersten Wort der neuen Zeile, nach dem Ende der vorigen Sprechphase
CUT = dict(B=round(K['krank'] - .3, 2), C=round(K['und1'] - .25, 2), D=round(K['mit'] - .35, 2), E=round(K['wir'] - .23, 2),
           F=round(K['nach'] - .3, 2), G=round(K['und2'] - .3, 2), H=round(K['pb'] - .3, 2))
DUR = round(j['duration'] + 1.4, 2)
open('film/zeiten.js', 'w').write(f'// erzeugt von zeiten.py aus out/vo.json ({j["stimme"]}, Wortzeiten neu vermessen und an der Pegelkurve geprüft)\nconst K = {json.dumps(K)};\nconst CUT = {json.dumps(CUT)};\nconst DUR = {DUR};\n')
json.dump({'K': K, 'CUT': CUT, 'DUR': DUR}, open('out/zeiten.json', 'w'), indent=1)
print(DUR, CUT); print(K)

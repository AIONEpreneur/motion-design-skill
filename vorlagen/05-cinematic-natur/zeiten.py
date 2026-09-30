#!/usr/bin/env python3
"""Leitet alle Bild-, Text-, Effektzeiten und Szenenwechsel (K) aus den Wortzeiten in out/vo.json ab.
V7: Wortzeiten aus werkzeuge/wortzeiten.py, Schlüsselwörter an der Pegelkurve geprüft (in vo.json "geprueft": "pegel");
die Aufzählung „Planung, Montage, Anmeldung“ liegt jetzt direkt in vo.json (keine festen Versätze mehr).
Schreibt film/zeiten.js (für den Film) und out/zeiten.json (für ton/partitur.py)."""
import json
j = json.load(open('out/vo.json', encoding='utf-8'))
W = j['words']
def wort(w, n=1, dt=0.0):
    hits = [x for x in W if x['w'] == w]
    return round(hits[n - 1]['start'] + dt, 3)
K = dict(schon=wort('schon'), strom=wort('stromrechnung'), steigt=wort('steigt'), jedes=wort('jedes'), jahr=wort('jahr'), hunderte=wort('hunderte'), mehr=wort('mehr'),
         dabei=wort('dabei'), sonne=wort('sonne'), jeden=wort('jeden'), tag=wort('tag'), dach=wort('dach'), sonnenhof=wort('sonnenhof'), kraftwerk=wort('kraftwerk'),
         planung=wort('planung'), montage=wort('montage'), anmeldung=wort('anmeldung'), alles=wort('alles'), hand=wort('hand'),
         tags=wort('tagsüber'), haus=wort('haus'), sonnenstrom=wort('sonnenstrom'), speicher=wort('speicher'), abend=wort('abend'),
         ihre2=wort('ihre', 2), rechnung=wort('rechnung'), sinkt=wort('sinkt'), siebzig=wort('siebzig'), prozent=wort('prozent'),
         sonnenhof2=wort('sonnenhof', 2), check=wort('check'), kostenlos=wort('kostenlos'))
# Szenen (alle aus Wortzeiten): Tropfen -> Wolkenmeer (Fahrt in den Tropfen endet 0,1 s vor „Dabei“),
# Sonne -> Blume (fertig 0,12 s vor „Tag“), Haus (fertig 0,4 s vor „Planung“), Tropfen am Morgen (fertig 0,06 s vor „Ihre“),
# Fahrt in den Tropfen -> Marke (fertig 0,11 s vor „Sonnenhof“)
K['cut'] = dict(sea=round(K['dabei'] - .1, 3), sun=round(K['tag'] - .47, 3), house=round(K['planung'] - .6, 3), drop2=round(K['ihre2'] - .36, 3), brand=round(K['sonnenhof2'] - .11, 3))
DUR = round(j['duration'] + 1.4, 2)
open('film/zeiten.js', 'w').write(f'// erzeugt von zeiten.py aus out/vo.json ({j["stimme"]})\nconst K = {json.dumps(K)};\nconst DUR = {DUR};\n')
json.dump({'K': K, 'DUR': DUR}, open('out/zeiten.json', 'w'), indent=1)
print(DUR, K)

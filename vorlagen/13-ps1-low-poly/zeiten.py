#!/usr/bin/env python3
"""V7: Leitet alle Bildzeitpunkte (K) und Szenenschnitte (CUT) aus den neu gemessenen Wortzeiten in out/vo.json ab.
out/vo.json wurde mit werkzeuge/wortzeiten.py aus out/vo.wav neu vermessen; Schlüsselwörter an der Pegelkurve geprüft
(Einträge mit "geprueft": "pegel"). Schreibt film/zeiten.js (Film) und out/zeiten.json (ton/partitur.py)."""
import json
j = json.load(open('out/vo.json', encoding='utf-8'))
W = j['words']
def wort(w, n=1, dt=0.0):  # n-tes Vorkommen eines Skriptworts
    hits = [x for x in W if x['w'] == w]
    return round(hits[n - 1]['start'] + dt, 3)
def zeile(i, dt=0.0): return round(j['lines'][i]['start'] + dt, 3)
K = dict(samstag=wort('samstag'), altbau=wort('altbau'), kein=wort('kein'), aufzug=wort('aufzug'), und=wort('und'), sofa=wort('sofa', 1), fest=wort('fest'),
         nichts=zeile(1), gepackt=wort('gepackt'), die=wort('die'), freunde=wort('freunde'), haben=wort('haben'), abgesagt=wort('abgesagt'),
         wagen=zeile(2), abend=wort('abend'), zurueck=wort('zurück'),
         montag0=zeile(3), montag=wort('montag'), job=wort('job'),
         mit=zeile(4), kistenheld=wort('kistenheld', 1), anders=wort('anders'),
         wir=zeile(5), n100=wort('100'), kartons=wort('kartons'), tag=wort('tag'), jeder=wort('jeder'), zimmer=wort('zimmer'), beschriftet=wort('beschriftet'),
         sofa2=zeile(6), lift=wort('möbellift'), fenster=wort('fenster'),
         abends=zeile(7), alles=wort('alles'), richtigen=wort('richtigen'), raum=wort('raum'),
         pizza0=zeile(8), pizza=wort('pizza'), wohnung=wort('wohnung'), angekommen=wort('angekommen'),
         schluss=zeile(9), umzuege=wort('umzüge'), fester=wort('fester'), kostenlose=wort('kostenlose'), besichtigung=wort('besichtigung'))
# Harte Schnitte wie im Original, jeweils 0,25–0,3 s vor dem ersten Wort der neuen Aussage
CUT = [0, round(K['und'] - .27, 2), round(K['nichts'] - .27, 2), round(K['die'] - .26, 2), round(K['wagen'] - .27, 2), round(K['montag0'] - .27, 2),
       round(K['mit'] - .27, 2), round(K['wir'] - .27, 2), round(K['jeder'] - .27, 2), round(K['sofa2'] - .27, 2), round(K['abends'] - .27, 2),
       round(K['pizza0'] - .27, 2), round(K['schluss'] - .3, 2)]
DUR = round(j['duration'] + 1.4, 2)
open('film/zeiten.js', 'w').write(f'// erzeugt von zeiten.py aus out/vo.json ({j["stimme"]}, Wortzeiten V7 neu vermessen)\nexport const K = {json.dumps(K)};\nexport const CUT = {json.dumps(CUT)};\nexport const DUR = {DUR};\n')
json.dump({'K': K, 'CUT': CUT, 'DUR': DUR}, open('out/zeiten.json', 'w'), indent=1)
print(DUR, CUT); print(K)

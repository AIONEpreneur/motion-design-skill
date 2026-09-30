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
K = dict(regen=wort('regen'), ihr=wort('ihr'), garten=wort('garten'), unter=wort('unter'), wasser=wort('wasser'), sommer=wort('sommer'), braun=wort('braun'),
         kinder=wort('kinder'), drinnen=wort('drinnen'), grund=wort('grund'), boden=wort('boden'), verdichtet=wort('verdichtet'),
         gw=wort('grünwerk'), lockert=wort('lockert'), n30=wort('30'), tief1=wort('tief', 1), darunter=wort('darunter'), kies=wort('kies'), ab=wort('ab'),
         oben=wort('obendrauf'), mutter=wort('mutterboden'), kompost=wort('kompost'), wurzeln=wort('wurzeln'), tief2=wort('tief', 2), versickert=wort('versickert'),
         rasen2=zeile(8), gruen=wort('grün'), regen3=wort('regen', 3), hitze=wort('hitze'), ende=zeile(9), probe=wort('bodenprobe'), kostenlos=wort('kostenlos'),
         rasen1=wort('rasen'), lieber=wort('lieber'), wasser2=wort('wasser', 2), regen2=wort('regen', 2), gartenbau=wort('gartenbau'))
DUR = 29.66  # Filmlänge bleibt (Musik/Mischung darauf gebaut)
open('film/zeiten.js', 'w').write(f'// erzeugt von zeiten.py aus out/vo.json ({j["stimme"]})\nconst K = {json.dumps(K)};\nconst DUR = {DUR};\n')
json.dump({'K': K, 'DUR': DUR}, open('out/zeiten.json', 'w'), indent=1)
print(DUR, K)

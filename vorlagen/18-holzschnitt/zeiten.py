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
K = dict(tuer=wort('tür'), zu=wort('zu'), schluessel=wort('schlüssel'), drinnen=wort('drinnen'), kurz=zeile(1), mitternacht=wort('mitternacht'),
         akku=wort('akku'), leer=wort('leer'), suchen=zeile(2), notdienst=wort('notdienst'), jeder=zeile(3), anderen=wort('anderen'), preis=wort('preis'),
         p50=wort('50'), p100=wort('100'), p300=wort('dreihundert'), riegel=zeile(5), festpreis=wort('festpreis'), sofort=wort('sofort'),
         zwanzig=zeile(6), minuten=wort('minuten'), da=wort('da'), oeffnet=zeile(7), folie=wort('folie'), ohne=wort('ohne'), bohren=wort('bohren'),
         klick=zeile(8), heil=wort('heil'), sind=wort('sind'), name=zeile(9), n24=wort('vierundzwanzig', 2), tag=wort('tag'), nacht=wort('nacht'),
         speichern=zeile(10), nummer=wort('nummer'), brauchen=wort('brauchen'))
DUR = round(j['duration'] + 1.4, 2)
open('film/zeiten.js', 'w').write(f'// erzeugt von zeiten.py aus out/vo.json ({j["stimme"]})\nconst K = {json.dumps(K)};\nconst DUR = {DUR};\n')
json.dump({'K': K, 'DUR': DUR}, open('out/zeiten.json', 'w'), indent=1)
print(DUR, K)

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
K = dict(vertrag=wort('vertrag'), heute=wort('heute'), kunden=wort('kunden'), sonst=zeile(1), auftrag=wort('auftrag'), weg=wort('weg'),
         post=wort('post'), frueh=wort('frühestens'), ueberm=wort('übermorgen'), ueber=zeile(3), vz=wort('verteilzentrum'), zweimal=wort('zweimal'),
         umgeladen=wort('umgeladen'), stadtbote=zeile(4), direkt=wort('direkt'), abgeholt=wort('abgeholt'), sechzig=wort('sechzig'),
         quer=zeile(6), stadt=wort('stadt'), ohne=wort('ohne'), umweg=wort('umweg'), halb=zeile(7), halbw=wort('halb'), vier=wort('vier'), da=wort('da'),
         mit=zeile(8), unterschrift=wort('unterschrift'), foto=wort('foto'), beleg=wort('beleg'), auftrag2=zeile(9), ihnen=wort('ihnen'),
         name=zeile(10), kurier=wort('kurier'), heute2=wort('heute', 2), bestellt=wort('bestellt'), heute3=wort('heute', 3), zugestellt=wort('zugestellt'),
         rufen=zeile(11), holen=wort('holen'), sofort=wort('sofort'))
DUR = round(j['duration'] + 1.4, 2)
open('film/zeiten.js', 'w').write(f'// erzeugt von zeiten.py aus out/vo.json ({j["stimme"]})\nconst K = {json.dumps(K)};\nconst DUR = {DUR};\n')
json.dump({'K': K, 'DUR': DUR}, open('out/zeiten.json', 'w'), indent=1)
print(DUR, K)

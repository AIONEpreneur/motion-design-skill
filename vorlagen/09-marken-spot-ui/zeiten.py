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
K = dict(montag=wort('montag'), acht=wort('8'), boden=wort('boden'), klebt=wort('klebt'), kueche=wort('küche'), die1=wort('die'), quillt=wort('quillt'), ueber=wort('über'),
         und=zeile(1), neun=wort('9'), wichtig=wort('wichtigster'), kunde=wort('kunde'),
         klarwerk=zeile(2), buchen=wort('buchen'), reinigung=wort('reinigung'), minute=wort('minute'), app=wort('app'),
         flaeche=zeile(3), rhythmus=wort('rhythmus'), waehlen=wort('wählen'), festpreis=wort('festpreis'), sofort=wort('sofort'),
         abends=zeile(4), dasselbe=wort('dasselbe'), team=wort('team'),
         jeder=zeile(5), raum=wort('raum'), haekchen=wort('häkchen'), foto=wort('foto'), handy=wort('handy'),
         morgen=zeile(6), glaenzt=max(wort('glänzt'), zeile(6, .3)), kunde2=wort('kunde', 2), kommen=wort('kommen'),
         ende=zeile(7), reinigung2=wort('reinigung', 2), erste=wort('erste'), schenken=wort('schenken'))
r = lambda x: round(x, 3)
# ---- V7: Schnitte, Mitteilungen und Mauszeiger aus den geprüften Wortzeiten ----
K['cut'] = dict(b1=r(K['boden'] - 0.35), b2=r(K['die1'] - 0.1), am=r(K['und'] - 0.45), choose=r(K['klarwerk'] - 0.17),
                office=r(K['flaeche'] - 0.03), f=r(K['abends'] - 0.1), pm=r(K['jeder'] - 0.38), h=r(K['morgen'] - 0.07), ende=r(K['kommen'] + 0.45))
K['pings'] = [r(K['jeder'] + 0.25), r(K['raum'] - 0.08), r(K['haekchen']), r(K['foto']), r(K['handy']), r(K['handy'] + 0.3)]   # Raum 3 = „Häkchen“, 4 = „Foto“
DUR = round(j['duration'] + 1.4, 2)
open('film/zeiten.js', 'w').write(f'// erzeugt von zeiten.py aus out/vo.json ({j["stimme"]})\nconst K = {json.dumps(K)};\nconst DUR = {DUR};\n')
json.dump({'K': K, 'DUR': DUR}, open('out/zeiten.json', 'w'), indent=1)
print(DUR, K)

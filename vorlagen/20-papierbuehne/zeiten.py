#!/usr/bin/env python3
"""V7: Leitet alle Bildzeitpunkte (K) aus den geprüften Wortzeiten in out/vo.json ab (Schlüsselwörter an der Pegelkurve
nachgeprüft, "geprueft": "pegel") -> film/zeiten.js + out/zeiten.json. Im Film gibt es keine festen Sekundenwerte, nur K."""
import json
j = json.load(open('out/vo.json', encoding='utf-8'))
W = j['words']
def wort(w, n=1, dt=0.0):
    hits = [x for x in W if x['w'] == w]
    return round(hits[n - 1]['start'] + dt, 3)
def zeile(i, dt=0.0): return round(j['lines'][i]['start'] + dt, 3)
K = dict(gitarre=wort('gitarre'), acht=wort('acht'), ecke=wort('ecke'), drei=zeile(1), drei2=wort('drei', 2), ein=wort('ein'), videos=wort('videos'), nach=zeile(2),
         wochen=wort('wochen', 1), auf=wort('aufgegeben'), dabei=zeile(3), tochter=wort('tochter'), eins=wort('eins'),
         lied=wort('lied', 1), ihnen=wort('ihnen'), abends=wort('abends'), bett=wort('bett'), tl=zeile(5), tonleiter=wort('tonleiter'), minuten=wort('minuten'), festem=wort('festem'), nicht=wort('nicht'),
         allein=wort('allein'), n30=wort('30'), woche=wort('woche'), lehrer=wort('lehrer'), ton1=zeile(7), ton2=wort('ton', 2),
         ihrem=wort('ihrem'), tempo=wort('tempo'), zwoelf=wort('zwölf'), sitzt=wort('sitzt'), erstes=wort('erstes'), lied2=wort('lied', 2),
         heute=zeile(9), spielen=wort('spielen'), vor=wort('vor'), tl2=zeile(10), musikschule=wort('musikschule'), erste=wort('erste'), probe=wort('probestunde'),
         kostenlos=wort('kostenlos'))
DUR = round(j['duration'] + 1.4, 2)
open('film/zeiten.js', 'w').write(f'// erzeugt von zeiten.py aus out/vo.json ({j["stimme"]})\nconst K = {json.dumps(K)};\nconst DUR = {DUR};\n')
json.dump({'K': K, 'DUR': DUR}, open('out/zeiten.json', 'w'), indent=1)
print(DUR, K)

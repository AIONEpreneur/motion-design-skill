#!/usr/bin/env python3
"""V7: Leitet alle Bildzeitpunkte (K) aus den neu gemessenen Wortzeiten in out/vo.json ab
(out/vo.json mit werkzeuge/wortzeiten.py neu vermessen, Schlüsselwörter an der Pegelkurve geprüft: "geprueft": "pegel").
Schreibt film/zeiten.js (für den Film) und out/zeiten.json (für ton/partitur.py)."""
import json
j = json.load(open('out/vo.json', encoding='utf-8'))
W = j['words']
def wort(w, n=1, dt=0.0):  # n-tes Vorkommen eines Skriptworts
    hits = [x for x in W if x['w'] == w]
    return round(hits[n - 1]['start'] + dt, 3)
def zeile(i, dt=0.0): return round(j['lines'][i]['start'] + dt, 3)
K = dict(brief=wort('brief'), geblitzt=wort('geblitzt'), n71=wort('71'), statt=wort('statt'), n50=wort('50'), monat=wort('monat'), fahrverbot=wort('fahrverbot'),
         nichtnur=wort('nicht'), keinauto=wort('kein', 1), dasheisst=zeile(4), arbeit=wort('arbeit'), kunden=zeile(5), kunden_w=wort('kunden'),
         kita=zeile(6), kita_w=wort('kindergarten'),
         aber=wort('aber'), fehler=wort('fehler'), recht=wort('recht'), prueft=wort('prüft'), mess=wort('messprotokoll'), eich=wort('eichung'), foto=wort('foto'),
         punkt=wort('punkt', 1), ein=zeile(10), verfahren=wort('verfahren'), eingestellt=wort('eingestellt'), fahren=zeile(11), einfach=wort('einfach'), weiter=wort('weiter'),
         schicken=wort('schicken'), bescheid2=wort('bescheid', 2), erst=wort('ersteinschätzung', 1), kostenlos=wort('kostenlos'))
DUR = round(j['duration'] + 1.4, 2)
open('film/zeiten.js', 'w').write(f'// erzeugt von zeiten.py aus out/vo.json ({j["stimme"]}, Wortzeiten neu vermessen)\nconst K = {json.dumps(K)};\nconst DUR = {DUR};\n')
json.dump({'K': K, 'DUR': DUR}, open('out/zeiten.json', 'w'), indent=1)
print(DUR, K)

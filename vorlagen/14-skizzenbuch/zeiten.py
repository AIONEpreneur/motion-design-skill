#!/usr/bin/env python3
"""V7: Leitet alle Bildzeitpunkte (K) aus den neu gemessenen Wortzeiten in out/vo.json ab (wortzeiten.py + Pegelprüfung,
Einträge mit "geprueft": "pegel"). Auch Szenenwechsel (TR im Film) und alle Bewegungen hängen an K.
Schreibt film/zeiten.js (für den Film) und out/zeiten.json (für ton/partitur.py)."""
import json
j = json.load(open('out/vo.json', encoding='utf-8'))
W = j['words']
def wort(w, n=1, dt=0.0):  # n-tes Vorkommen eines Skriptworts
    hits = [x for x in W if x['w'] == w]
    return round(hits[n - 1]['start'] + dt, 3)
def zeile(i, dt=0.0): return round(j['lines'][i]['start'] + dt, 3)
K = dict(kind=wort('kind', 1), fuenf=wort('fünf'), hause=wort('hause'), mathe=wort('mathe'), wieder=wort('wieder', 1),
         abend=zeile(2), streit=wort('streit'), haus=wort('hausaufgaben'), versetzung=wort('versetzung'), wackelt=wort('wackelt'),
         dabei=zeile(4), fehlt=wort('fehlt'), einziger=wort('einziger'), baustein=wort('baustein'),
         lernwerk=wort('lernwerk', 1), findet=wort('findet'), genau=wort('genau'), luecke=wort('lücke'), kostenlos1=wort('kostenlosen'), probe=wort('probestunde', 1),
         dann=zeile(7), zweimal=wort('zweimal'), woche=wort('woche', 1), hoechstens=wort('höchstens'), drei=wort('drei', 1), kinder=wort('kinder'), gruppe=wort('gruppe'),
         nach=zeile(8), acht=wort('acht'), eine3=wort('drei', 2), kind2=zeile(9), rechnet=wort('rechnet'), gern=wort('gern'),
         marke=zeile(10), nachhilfe=wort('nachhilfe'), buchen=wort('buchen'), kostenlos2=wort('kostenlose'), probe2=wort('probestunde', 2))
DUR = round(j['duration'] + 1.4, 2)
open('film/zeiten.js', 'w').write(f'// erzeugt von zeiten.py aus out/vo.json ({j["stimme"]})\nconst K = {json.dumps(K)};\nconst DUR = {DUR};\n')
json.dump({'K': K, 'DUR': DUR}, open('out/zeiten.json', 'w'), indent=1)
print(DUR, K)

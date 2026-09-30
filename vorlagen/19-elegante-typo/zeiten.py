#!/usr/bin/env python3
"""V7: Leitet alle Bildzeitpunkte (K) aus den geprüften Wortzeiten in out/vo.json ab (Wortanfänge an der Pegelkurve
nachgeprüft, siehe "geprueft": "pegel"). Schreibt film/zeiten.js (Film) und out/zeiten.json (ton/partitur.py).
Im Film gibt es keine festen Sekundenwerte, nur K."""
import json
j = json.load(open('out/vo.json', encoding='utf-8'))
W = j['words']
def wort(w, n=1, dt=0.0):  # n-tes Vorkommen eines Skriptworts
    hits = [x for x in W if x['w'] == w]
    return round(hits[n - 1]['start'] + dt, 3)
def zeile(i, dt=0.0): return round(j['lines'][i]['start'] + dt, 3)
K = dict(siebzig=wort('siebzig'), stunden=wort('stunden'), alles=wort('alles'), landet=wort('landet'), ihnen=wort('ihnen'),
         angebote=wort('angebote'), personal=wort('personal'), rechnungen=wort('rechnungen'), kunden=wort('kunden'),
         sie=zeile(2), arbeiten=wort('arbeiten'), mehr=wort('mehr'), aber=wort('aber'), firma=wort('firma'), tritt=wort('tritt'), stelle=wort('stelle'),
         klarsicht=zeile(3), beratung=wort('beratung'), sortiert=wort('sortiert'), wirklich=wort('wirklich'), zaehlt=wort('zählt'),
         drei=zeile(4), prio=wort('prioritäten'), statt=wort('statt'), n30=wort('30'), baustellen=wort('baustellen'),
         zwoelf=zeile(5), wochen=wort('wochen'), termin=wort('termin'), woche2=wort('woche', 2),
         team=wort('team'), ihr=zeile(6), uebernimmt=wort('übernimmt'), sie2=wort('sie', 2), fuehren=wort('führen'), wieder=wort('wieder'),
         ergebnis=zeile(7), n20=wort('20'), stunden2=wort('stunden', 2), weniger=wort('weniger'), endlich=wort('endlich'), urlaub=wort('urlaub'),
         name=zeile(8), beratung2=wort('beratung', 2), gespraech=wort('gespräch'), kostenlos=wort('kostenlos'), ende=round(j['lines'][8]['end'], 3))
DUR = round(j['duration'] + 1.4, 2)
open('film/zeiten.js', 'w').write(f'// erzeugt von zeiten.py aus out/vo.json ({j["stimme"]}), Wortanfänge an der Pegelkurve geprüft\nconst K = {json.dumps(K)};\nconst DUR = {DUR};\n')
json.dump({'K': K, 'DUR': DUR}, open('out/zeiten.json', 'w'), indent=1)
print(DUR, K)

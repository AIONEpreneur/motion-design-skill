#!/usr/bin/env python3
"""V7: Leitet ALLE Bildzeitpunkte (K) aus den neu gemessenen Wortzeiten in out/vo.json ab (wortzeiten.py + Pegelprüfung).
Die früher im Film fest eingetragenen Zusatzzeiten (Object.assign(K, {sucht: .56, …})) stehen jetzt hier.
Schreibt film/zeiten.js (für den Film) und out/zeiten.json (für ton/partitur.py)."""
import json
j = json.load(open('out/vo.json', encoding='utf-8'))
W = j['words']
def wort(w, n=1, dt=0.0):  # n-tes Vorkommen eines Skriptworts
    hits = [x for x in W if x['w'] == w]
    return round(hits[n - 1]['start'] + dt, 3)
def zeile(i, dt=0.0): return round(j['lines'][i]['start'] + dt, 3)
K = dict(kunde=wort('kunde'), sucht=wort('sucht'), tischler=wort('tischler'), er=wort('er'), findet=wort('findet'), ihre=wort('ihre'), website=wort('website', 1),
         winzige=wort('winzige'), schrift=wort('schrift'), foto=wort('foto'), nummer=wort('telefonnummer'),
         nach=zeile(2), zwei=wort('zwei'), sekunden=wort('sekunden'), weg=wort('weg'),
         und=zeile(3), auftrag=wort('auftrag'), geht=wort('geht'), betrieb=wort('betrieb'), nebenan=wort('nebenan'),
         dabei=zeile(4), ihre2=wort('ihre', 2), arbeit=wort('arbeit'), besser=wort('besser'),
         werkseite=wort('werkseite', 1), baut=wort('baut'), ihre3=wort('ihre', 3), neue=wort('neue', 1), website2=wort('website', 2), vierzehn=wort('vierzehn'), tagen=wort('tagen'),
         logo=zeile(6), logoW=wort('logo'), projekte=wort('projekte'), knopf=wort('knopf'), anrufen=wort('anrufen'),
         jetzt=zeile(7), klingelt=wort('klingelt', 1, .1), ihr4=wort('ihr', 2), telefon=wort('telefon'), jede=wort('jede'), woche=wort('woche'), neue2=wort('neue', 2), anfragen=wort('anfragen'),
         marke=zeile(8), websites=wort('websites'), fuer=wort('für'), handwerker=wort('handwerker'), festpreis=wort('festpreis'))
DUR = round(j['duration'] + 1.4, 2)
open('film/zeiten.js', 'w').write(f'// erzeugt von zeiten.py aus out/vo.json ({j["stimme"]})\nconst K = {json.dumps(K)};\nconst DUR = {DUR};\n')
json.dump({'K': K, 'DUR': DUR}, open('out/zeiten.json', 'w'), indent=1)
print(DUR, K)

#!/usr/bin/env python3
"""V7: Leitet alle Bildzeitpunkte (K) und Szenenschnitte (CUT) aus den neu gemessenen Wortzeiten in out/vo.json ab
(out/vo.json wurde mit werkzeuge/wortzeiten.py aus out/vo.wav neu vermessen).
Schreibt film/zeiten.js (für den Film) und out/zeiten.json (für ton/partitur.py)."""
import json
j = json.load(open('out/vo.json', encoding='utf-8'))
W = j['words']
def wort(w, n=1, dt=0.0):  # n-tes Vorkommen eines Skriptworts
    hits = [x for x in W if x['w'] == w]
    return round(hits[n - 1]['start'] + dt, 3)
def zeile(i, dt=0.0): return round(j['lines'][i]['start'] + dt, 3)
K = dict(montag1=wort('montagmorgen'), server=wort('server'), aus=wort('aus'), mails=wort('mails'), rechnungen=wort('rechnungen'), n20=wort('20'), warten=wort('warten'),
         ohne=zeile(3), sicherung=wort('sicherung', 1), kunden=wort('kundendaten'), weg=wort('weg'), oft=zeile(4), zeigt=wort('zeigt'), wochen=wort('wochen'), vorher=wort('vorher'),
         nnit=zeile(5), ueberwacht=wort('überwacht'), technik=wort('technik'), rund=wort('rund'), uhr=wort('uhr'),
         schwache=zeile(6), platten=wort('festplatten'), tauschen=wort('tauschen'), bevor=wort('bevor'), ausfallen=wort('ausfallen'),
         nacht=wort('nacht'), jede=zeile(7), verschl=wort('verschlüsselte'), sicherung2=wort('sicherung', 2), ausser=wort('außer'), haus=wort('haus'),
         notfall=wort('notfall'), alles=wort('alles'), unter=wort('unter'), stunde=wort('stunde'), wieder=wort('wieder'),
         montag2=zeile(9), team=wort('team'), arbeitet=wort('arbeitet'), ende=zeile(10), check=wort('check'), kostenlos=wort('kostenlos'))
# Schnitte: 0,26–0,3 s vor dem ersten Wort der neuen Zeile (immer nach dem Ende der vorigen Sprechphase)
CUT = dict(loss=round(K['ohne'] - .28, 2), watch=round(K['nnit'] - .28, 2), swap=round(K['schwache'] - .17, 2), night=round(K['jede'] - .27, 2),
           restore=round(zeile(8) - .26, 2), office2=round(K['montag2'] - .27, 2), end=round(K['ende'] - .28, 2))
DUR = round(j['duration'] + 1.4, 2)
open('film/zeiten.js', 'w').write(f'// erzeugt von zeiten.py aus out/vo.json ({j["stimme"]}, Wortzeiten neu vermessen)\nconst K = {json.dumps(K)};\nconst CUT = {json.dumps(CUT)};\nconst DUR = {DUR};\n')
json.dump({'K': K, 'CUT': CUT, 'DUR': DUR}, open('out/zeiten.json', 'w'), indent=1)
print(DUR, CUT); print(K)

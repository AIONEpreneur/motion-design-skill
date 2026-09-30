#!/usr/bin/env python3
"""Leitet alle Bild-, Text-, Effektzeiten und Szenenwechsel (K) aus den Wortzeiten in out/vo.json ab.
V7: Wortzeiten aus werkzeuge/wortzeiten.py, Schlüsselwörter an der Pegelkurve geprüft (in vo.json "geprueft": "pegel").
Schreibt film/zeiten.js (für den Film) und out/zeiten.json (für ton/partitur.py)."""
import json
j = json.load(open('out/vo.json', encoding='utf-8'))
W = j['words']
def wort(w, n=1, dt=0.0):
    hits = [x for x in W if x['w'] == w]
    return round(hits[n - 1]['start'] + dt, 3)
K = dict(urlaub=wort('urlaub'), gebucht=wort('gebucht'), wohin=wort('wohin'), katze=wort('katze'),
         nachbarin=wort('nachbarin'), keine=wort('keine'), zeit=wort('zeit'), fremde=wort('fremde'), wohnung=wort('wohnung'), lieber=wort('lieber'), nicht=wort('nicht'),
         pfoten=wort('pfotenhaus'), wohnt=wort('wohnt'), zimmer=wort('zimmer'), fenster=wort('fensterplatz'),
         morgens=wort('morgens'), abends=wort('abends'), futter=wort('futter'), dazwischen=wort('dazwischen'), spielen=wort('spielen'), kuscheln=wort('kuscheln'),
         jeden=wort('jeden'), abend=wort('abend'), foto=wort('foto'), handy=wort('handy'),
         so=wort('so'), urlaub2=wort('urlaub', 2), katze2=wort('katze', 2), auch=wort('auch'),
         pfoten2=wort('pfotenhaus', 2), kennen=wort('kennenlernen'), kostenlos=wort('kostenlos'))
K['stops'] = [round(K['pfoten'] - .15, 3), round(K['pfoten'] + .1, 3), round(K['pfoten'] + .35, 3)]   # Walzen rasten ein, die mittlere auf dem Namen
K['blitz'] = round(K['abend'] + .02, 3)                                                                # Kamerablitz auf „Abend“
# Szenenwechsel in den Sprechpausen: Flur (nach „Katze?“), Walzen (nach „nicht“), Zimmer (vor „wohnt“), Meer (Blitz), Split (vor „So“), Schluss (vor „Pfotenhaus“)
K['cut'] = dict(flur=round(K['nachbarin'] - .6, 3), walze=round(K['nicht'] + .35, 3), zimmer=round(K['wohnt'] - .5, 3), meer=round(K['blitz'] - .03, 3),
                split=round(K['so'] - .45, 3), schluss=round(K['pfoten2'] - .4, 3))
DUR = round(j['duration'] + 1.4, 2)
open('film/zeiten.js', 'w').write(f'// erzeugt von zeiten.py aus out/vo.json ({j["stimme"]})\nconst K = {json.dumps(K)};\nconst DUR = {DUR};\n')
json.dump({'K': K, 'DUR': DUR}, open('out/zeiten.json', 'w'), indent=1)
print(DUR, K)

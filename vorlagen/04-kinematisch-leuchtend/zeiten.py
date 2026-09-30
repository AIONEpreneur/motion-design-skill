#!/usr/bin/env python3
"""Leitet alle Bild-, Text-, Effektzeiten und Szenenwechsel (K) aus den Wortzeiten in out/vo.json ab.
V7: Wortzeiten aus werkzeuge/wortzeiten.py, Schlüsselwörter an der Pegelkurve geprüft (in vo.json mit "geprueft": "pegel").
Schreibt film/zeiten.js (für den Film) und out/zeiten.json (für ton/partitur.py)."""
import json
j = json.load(open('out/vo.json', encoding='utf-8'))
W = j['words']
def wort(w, n=1, dt=0.0):
    hits = [x for x in W if x['w'] == w]
    return round(hits[n - 1]['start'] + dt, 3)
K = dict(sturz=wort('sturz'), fahrrad=wort('fahrrad'), monate=wort('monatelang'), nicht=wort('nicht'), arbeiten=wort('arbeiten'),
         ihr=wort('ihr', 1), gehalt=wort('gehalt'), bleibt=wort('bleibt'), aus=wort('aus'), rate=wort('rate'), haus=wort('haus'), weiter=wort('weiter'),
         und2=wort('und', 2), kinder=wort('kinder'), brauchen=wort('brauchen'), dafuer=wort('dafür'), es=wort('es', 1), bu=wort('berufsunfähigkeitsversicherung'),
         nur=wort('nur'), welcher=wort('welcher'), tarif=wort('tarif'), zahlt=wort('zahlt'), wirklich=wort('wirklich'),
         halt=wort('halt'), hundert=wort('100'), tarife=wort('tarife'), und3=wort('und', 3), prueft=wort('prüft'), klein=wort('kleingedruckte'),
         kl1=wort('klausel', 1), kl2=wort('klausel', 2), passiert=wort('passiert'), kommt=wort('kommt'), gehalt2=wort('gehalt', 2),
         trotzdem=wort('trotzdem'), und4=wort('und', 4), familie=wort('familie'), behaelt=wort('behält'), zuhause=wort('zuhause'),
         halt2=wort('halt', 2), makler=wort('versicherungsmakler'), erst=wort('erstgespräch'), kostenlos=wort('kostenlos'))
# Häkchen auf der Treppe: fertig auf „Klausel“, „Klausel“, dann eins im Nachklang
K['ck'] = [K['kl1'], K['kl2'], round(K['kl2'] + .45, 3)]
# Szenenwechsel: jeweils in der Sprechpause vor dem ersten Wort der neuen Zeile (Überblendung 0,3 s, fertig vor dem Wort)
K['cut'] = dict(b=round(K['ihr'] - .12, 3), c=round(K['und2'] - .25, 3), d=round(K['dafuer'] - .1, 3), e=round(K['nur'] - .15, 3),
                f=round(K['und3'] - .17, 3), g=round(K['passiert'] - .05, 3), h=round(K['und4'] - .05, 3), i=round(K['halt2'] - .04, 3))
DUR = round(j['duration'] + 1.4, 2)
open('film/zeiten.js', 'w').write(f'// erzeugt von zeiten.py aus out/vo.json ({j["stimme"]})\nconst K = {json.dumps(K)};\nconst DUR = {DUR};\n')
json.dump({'K': K, 'DUR': DUR}, open('out/zeiten.json', 'w'), indent=1)
print(DUR, K)

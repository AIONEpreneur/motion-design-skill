#!/usr/bin/env python3
"""V7: Leitet ALLE Bild-, Text-, Effekt- und Schnittzeiten (K) aus den an der Pegelkurve geprüften Wortzeiten in out/vo.json ab.
Die Blender-Bildfolgen werden nicht neu gerendert: jede Einstellung bekommt Ankerpunkte (Film-Zeit -> Bildfolgen-Zeit),
so dass die eingebauten Ereignisse (Tropfen, Kasten landet, Flasche kippt, Kisten, Wasser, Mahlen, Karton, Anstoßen) auf den Wörtern liegen.
Schreibt film/zeiten.js (für den Film) und out/zeiten.json (für ton/partitur.py)."""
import json
j = json.load(open('out/vo.json', encoding='utf-8'))
W = j['words']
def wort(w, n=1, dt=0.0):  # n-tes Vorkommen eines Skriptworts
    hits = [x for x in W if x['w'] == w]
    return round(hits[n - 1]['start'] + dt, 3)
def zeile(i, dt=0.0): return round(j['lines'][i]['start'] + dt, 3)
K = dict(und=zeile(2), qw=wort('quellwerk'), drei=wort('3'), kanne=wort('kanne'), leer=wort('leer'), kasten=zeile(1), wasserkasten=wort('wasserkasten'), auch=wort('auch'),
         schleppt=wort('schleppt'), sechs=wort('6'), kisten=wort('kisten'), dritten=wort('3', 2), stock=wort('stock'),
         quellwerk=zeile(3), wasser=wort('wasser'), direkt=wort('direkt'), leitung=wort('leitung'),
         gefiltert=zeile(4), gekuehlt=max(wort('gekühlt'), zeile(4, .5)), sprudelnd=wort('sprudelnd'), knopf=wort('auf'), knopfdruck=wort('knopfdruck'),
         kaffee=zeile(5), mahlt=wort('mahlt'), tasse=wort('jede'), frisch=wort('frisch'),
         bohnen=zeile(6), filter=wort('filter'), alle=wort('alle'), vier=wort('4'), ohne=wort('ohne'), bestellung=wort('bestellung'),
         team=zeile(7), frisch2=wort('frisch', 2), feierabend=wort('feierabend'),
         ende=zeile(8), office=wort('office'), zwei=wort('2'), kostenlos=wort('kostenlos'), testen=wort('testen'))
r = lambda x: round(x, 3)
# ---- Schnitte und Zeit-Anker der Bildfolgen: [Filmzeit, Bildfolgenzeit in s] ----
a2 = K['kasten'] - 0.2; a3 = K['und'] + 0.12; a4 = K['leitung'] - 2.65; a5 = K['gefiltert'] - 0.35; a5c = a5 + 73 / 30
a6 = K['kaffee'] - 0.1; a7 = K['bohnen'] - 0.08; a8 = K['frisch2'] - 1.31; a9 = K['ende'] - 0.28
K['cut'] = [0, r(a2), r(a3), r(a4), r(a5), r(a5c), r(a6), r(a7), r(a8), r(a9)]
K['map'] = [
  [[0, 0], [K['leer'] - 0.3, 1.95]],                               # S1: letzter Tropfen schlägt kurz vor „leer“ auf
  [[K['wasserkasten'] - 0.08, 0.40], [K['auch'], 1.18]],           # S2: Kasten landet auf „Wasserkasten“, Flasche kippt auf „auch“
  [[K['sechs'] - 0.56, 0.91], [K['dritten'], 2.44]],               # S3: Stapel steht vor „sechs“, Schild „3. OG“ im Bild auf „dritten“
  [[a4, 0], [K['leitung'], 2.65]],                                  # S4: Wasser fließt auf „Leitung“
  [[a5, 0], [a5 + 1, 1]],                                           # S5: Kartusche fliegt auf „gefiltert“ in den Kranz, Perlen steigen auf „sprudelnd“
  [[a5c, 0], [a6, 39 / 30]],                                        # S5c: Zeitlupe bis zum Schnitt
  [[a6, 0], [K['mahlt'], 1.19], [a7, 3.27]],                        # S6: Mahlen auf „mahlt“
  [[a7, 0], [K['ohne'] + 0.05, 2.72]],                              # S7: Karton springt auf „ohne“ auf
  [[a8, 0], [a8 + 1, 1]],                                           # S8: Anstoßen auf „frisch“
  [[a9, 0], [a9 + 1, 1]]]                                           # S9: Packshot
def film_t(i, u):  # Bildfolgenzeit -> Filmzeit (für Partitur)
    m = K['map'][i]
    if len(m) < 2: return m[0][0]
    for (t0, u0), (t1, u1) in zip(m, m[1:]):
        if u <= u1 or (t1, u1) == tuple(m[-1]): return r(t0 + (u - u0) * (t1 - t0) / (u1 - u0))
K['map'] = [[[r(a), r(b)] for a, b in m] for m in K['map']]
K['tropfen'] = film_t(0, 1.95); K['kasten_land'] = film_t(1, 0.40); K['kippt'] = film_t(1, 1.18)
K['kisten_land'] = [film_t(2, 0.56 + j * 0.07) for j in range(6)]
K['wasser_an'] = r(K['leitung'] - 0.02); K['karton_auf'] = r(K['ohne'] + 0.05); K['klirr'] = r(K['frisch2'] - 0.05)
K['whip'] = [r(K['ende'] - 0.51), r(a9), r(K['ende'] - 0.03)]
DUR = round(j['duration'] + 1.4, 2)
open('film/zeiten.js', 'w').write(f'// erzeugt von zeiten.py aus out/vo.json ({j["stimme"]})\nconst K = {json.dumps(K)};\nconst DUR = {DUR};\n')
json.dump({'K': K, 'DUR': DUR}, open('out/zeiten.json', 'w'), indent=1)
print(DUR, K)

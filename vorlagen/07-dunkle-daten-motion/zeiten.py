#!/usr/bin/env python3
"""V7: Leitet ALLE Bild-, Text-, Effekt- und Szenenzeiten (K) aus den an der Pegelkurve geprüften Wortzeiten in out/vo.json ab.
Schreibt film/zeiten.js (für den Film) und out/zeiten.json (für ton/partitur.py). Im Film stehen keine festen Sekundenwerte mehr."""
import json
j = json.load(open('out/vo.json', encoding='utf-8'))
W = j['words']
def wort(w, n=1, dt=0.0):  # n-tes Vorkommen eines Skriptworts
    hits = [x for x in W if x['w'] == w]
    return round(hits[n - 1]['start'] + dt, 3)
def zeile(i, dt=0.0): return round(j['lines'][i]['start'] + dt, 3)
K = dict(bescheid=wort('steuerbescheid'), n14=wort('14000'), nachz=wort('nachzahlung'), faellig=wort('fällig'), wochen=wort('4'), wochenW=wort('wochen'),
         dazu=wort('dazu'), steigen=wort('steigen'), voraus=wort('vorauszahlungen'), polster=wort('polster'), weg=wort('weg'),
         maschine=wort('maschine'), gestrichen=wort('gestrichen'), dasmuss=zeile(4), nicht=wort('nicht'),
         kanzlei=zeile(5), belege=wort('belege'), monat=wort('monat'), digital=wort('digital'), jedes=wort('jedes'), quartal=wort('quartal'),
         hoch=wort('steuer'), hochW=wort('hoch'), sagt=zeile(7), zurueck=wort('zurücklegen'), kommt=zeile(8), bescheid2=wort('bescheid'), n14b=wort('14000', 2),
         bereit=wort('längst'), bereitW=wort('bereit'), maschine2=wort('maschine', 2), kaufen=wort('kaufen'), trotzdem=wort('trotzdem'),
         ende=zeile(10), steuerb=wort('steuerberatung'), erst=wort('erstgespräch'), kostenlos=wort('kostenlos'))
r = lambda x: round(x, 3)
lerp = lambda a, b, k: a + (b - a) * k
# ---- abgeleitete Ereignisse (Film und Partitur benutzen dieselben Werte) ----
K['gate'] = r(K['n14'] - 0.24)                                                   # Röhre trifft das Bescheid-Tor, kurz vor „vierzehntausend“
K['weeks'] = [r(lerp(K['faellig'] - 0.06, K['wochenW'] + 0.06, i / 3)) for i in range(4)]   # 4 Wochen-Tore von „Fällig“ bis „Wochen“
K['stairs'] = [r(K['dazu'] + .05), r(K['steigen'] + .35), r(K['voraus'] + .05), r(K['voraus'] + .6)]   # Treppe abwärts = Vorauszahlungen
K['tb0'] = r(K['kanzlei'] - 0.25)                                                # Lauf B beginnt
q = [K['quartal'], K['hoch'], K['sagt'] + 0.13, K['zurueck'] + 0.45]              # Quartals-Tore: Q1 genau auf „Quartal“
m = [K['kanzlei'] + 0.45, K['monat'], K['digital'] + 0.5]                         # Februar-Tor genau auf „Monat“
for a, b in [(q[0], q[1]), (q[1], q[2]), (q[2], q[3])]:
    m += [lerp(a, b, k) for k in (0.25, 0.5, 0.75)]
K['q'] = [r(x) for x in q]; K['mon'] = [r(x) for x in m]
K['impact'] = K['bescheid2']                                                     # Glaswand zerspringt auf „Bescheid“
K['mach'] = K['maschine2']                                                       # Maschinen-Tor leuchtet auf „Maschine“
K['resA'] = r(K['sagt'] + 0.3); K['resZ'] = r(K['zurueck'] + 0.2)                # Rücklage zählt hoch
DUR = round(j['duration'] + 1.4, 2)
open('film/zeiten.js', 'w').write(f'// erzeugt von zeiten.py aus out/vo.json ({j["stimme"]}), Wortzeiten an der Pegelkurve geprüft\nconst K = {json.dumps(K)};\nconst DUR = {DUR};\n')
json.dump({'K': K, 'DUR': DUR}, open('out/zeiten.json', 'w'), indent=1)
print(DUR, json.dumps(K))

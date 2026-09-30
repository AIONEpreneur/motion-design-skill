#!/usr/bin/env python3
"""Grünpfeil V4 – eigene Chiptune-Musik + 8-Bit-Effekte (48 kHz Stereo), liest out/zeiten.json.
Instrumente wie auf einer Spielkonsole: Pulswelle (Melodie), Dreieck (Bass), Rauschen (Trommeln).
Dramaturgie: „Game-over“-Jingle beim Durchfallen -> Moll, Herzschlag-Bass (Job in Gefahr) -> Ampel-Blips, Wendung nach Dur
-> Üben: jede Runde ein steigender Ton, „Level up“ bei „sitzt“ -> Probefahrt-Groove mit Münzen -> Boss-Spannung, Stille im
Hit-Stop, Siegesfanfare -> Montagmorgen fröhlich -> Schlussjingle."""
import numpy as np, soundfile as sf, os, json
SR = 48000; Z = json.load(open('out/zeiten.json')); K = Z['K']; DUR = Z['DUR']
HIT = K['bestanden'] - .04; LAND = K['probe']  # V7: alle Einsätze aus den geprüften Wortzeiten
N = int(DUR * SR); R = np.random.default_rng(21)
M = np.zeros((N, 2)); S = np.zeros((N, 2))
def tt(d): return np.arange(int(d * SR)) / SR
def put(buf, a, x, pan=0.):
    i = int(a * SR); n = min(len(x), N - i)
    if i < 0 or n <= 0: return
    buf[i:i + n, 0] += x[:n] * np.cos((pan + 1) * np.pi / 4) * 1.41; buf[i:i + n, 1] += x[:n] * np.sin((pan + 1) * np.pi / 4) * 1.41
def hz(n): return 440 * 2 ** ((n - 69) / 12)
def env(t, d, a=.005, r=.04): return np.clip(t / a, 0, 1) * np.clip((d - t) / r, 0, 1)
def pulse(n, a, d, amp=.06, duty=.25, pan=0, buf=None, slide=0):
    t = tt(d); f = hz(n) * (1 + slide * t / d); ph = np.cumsum(f) / SR % 1; x = np.where(ph < duty, 1., -1.)
    put(M if buf is None else buf, a, x * env(t, d) * amp, pan)
def tri(n, a, d, amp=.12):
    t = tt(d); ph = np.cumsum(np.full(len(t), hz(n))) / SR % 1; x = 4 * np.abs(ph - .5) - 1; put(M, a, x * env(t, d, .003, .02) * amp)
def noiseq(a, d, amp=.05, pan=0, dec=40, buf=None):  # 8-Bit-Rauschen (gehaltene Werte)
    t = tt(d); x = np.repeat(R.uniform(-1, 1, len(t) // 8 + 1), 8)[:len(t)]; put(M if buf is None else buf, a, x * np.exp(-t * dec) * amp, pan)
def kick(a, amp=.18): t = tt(.15); put(M, a, np.sign(np.sin(2 * np.pi * np.cumsum(60 + 200 * np.exp(-t * 40)) / SR)) * np.exp(-t * 25) * amp)
def arp(ns, a, d, step=.05, amp=.035, duty=.125, pan=0):
    k = 0; x = a
    while x < a + d: pulse(ns[k % len(ns)], x, step * .9, amp, duty, pan); k += 1; x += step
B = .3  # Achtel bei 100 BPM
# 1) Game over: absteigender Jingle, dann Moll mit Herzschlag
for i, n in enumerate([72, 71, 70, 69]): pulse(n, K['durch'] + i * .14, .13, .07, .5)
pulse(57, K['durch'] + .56, .5, .06, .5, slide=-.06)
for a in np.arange(K['schon'], K['bei'] - .1, .8): tri(33, a, .12, .14); tri(33, a + .2, .1, .09)   # Herzschlag
for a, ns in [(K['zwei'], [57, 60, 64]), (K['dabei'], [53, 57, 60]), (K['und1'], [50, 53, 57]), (K['ohne'], [52, 56, 59])]:
    arp(ns, a, 1.6, .1, .025, .25, -.3)
for k, n in [('fehler', 58), ('links1', 58)]: pulse(n, K[k], .25, .06, .5); pulse(n - 6, K[k] + .02, .25, .04, .5)
pulse(64, K['sechs'], .4, .04, .25, .3); pulse(67, K['job'], .5, .045, .25, .3)
# 2) Wendung: Ampel-Blips, dann C-Dur-Groove
pulse(60, K['bei'], .12, .05, .5); pulse(67, K['bei'] + .15, .12, .05, .5); pulse(72, K['bei'] + .32, .3, .06, .5)
PROG = [[48, 60, 64, 67], [45, 60, 64, 69], [41, 60, 65, 69], [43, 59, 62, 67]]
MEL = [72, 74, 76, 79, 76, 74, 72, 67]
a = K['gruen'] + .3; i = 0
while a < K['und2'] - .3:
    c = PROG[(i // 8) % 4]
    tri(c[0] - 12 + (12 if i % 2 else 0), a, B * .9, .1)
    if i % 4 == 0: kick(a)
    if i % 4 == 2: noiseq(a, .12, .05, .1, 30)
    noiseq(a + B / 2, .04, .015, .3, 80)
    if a > K['dann'] - .1 and i % 2 == 0: pulse(MEL[(i // 2) % 8], a, B * 1.8, .04, .25, .2)
    i += 1; a += B
# Üben: jede Runde ein steigender Ton, Level-up bei „sitzt“
L0 = K['zehn'] - .05; per = (K['sitzt'] - L0) / 10
for n in range(10): pulse(72 + [0, 2, 4, 5, 7, 9, 11, 12, 14, 16][n], L0 + (n + 1) * per - .02, .12, .045, .125, -.2 + n * .04)
arp([72, 76, 79, 84], K['sitzt'], .5, .05, .05, .25)
# 3) Boss: Spannung, Stille im Hit-Stop, Fanfare
for a in np.arange(K['und2'] - .1, K['bestanden'] - .3, .1): noiseq(a, .06, .03 + .03 * (a - K['und2']), 0, 60)
for a in np.arange(K['und2'], K['bestanden'] - .3, B): tri(28, a, B * .8, .12)
HW = .6  # Wortlänge „bestanden“: davor Stille, Fanfare erst danach
hs = K['bestanden']
for i, n in enumerate([67, 72, 76, 79]): pulse(n, hs + HW + i * .08, .08, .06, .5)
pulse(84, hs + HW + .32, .7, .07, .5); pulse(76, hs + HW + .32, .7, .045, .25); tri(36, hs + HW + .32, .7, .14)
# 4) Montagmorgen: fröhliche Melodie in F-Dur, Schluss-Jingle
a = K['mont'] - .1; i = 0; MEL2 = [69, 72, 77, 76, 74, 72, 74, 77]
while a < DUR - 1.2:
    c = [[41, 57, 60, 65], [43, 58, 62, 67], [45, 60, 64, 69], [36, 55, 60, 64]][(i // 8) % 4]
    tri(c[0] - 12 + (12 if i % 2 else 0), a, B * .9, .09)
    if i % 4 == 0: kick(a, .14)
    if i % 2 == 0 and a < K['fahr']: pulse(MEL2[(i // 2) % 8], a, B * 1.7, .04, .25, .2)
    if a > K['fahr'] and i % 2 == 0: arp(c[1:], a, B * 1.8, .075, .02, .125, .3)
    i += 1; a += B
for i, n in enumerate([72, 76, 79, 84]): pulse(n, K['kostenlos'] + i * .09, .12, .06, .5)
pulse(88, K['kostenlos'] + .36, .6, .05, .5); tri(36, K['kostenlos'] + .36, .8, .13)

# --- 8-Bit-Effekte, nur wo im Bild etwas passiert ---
def blip(a, n, d=.06, amp=.08, pan=0, duty=.5, slide=0): pulse(n, a, d, amp, duty, pan, S, slide)
# Motor im Leerlauf (Auto steht), Warnblinker
for a in np.arange(.2, K['zwei'] - .2, .12): noiseq(a, .05, .025, -.1, 60, S)
for a in np.arange(K['durch'], K['zwei'] - .2, 1 / 3):
    if int(a * 3) % 2: blip(a, 84, .02, .04, -.1)
# Herz zerbricht
blip(K['durch'] + .15, 64, .2, .07, 0, .5, -.5); blip(K['schon'], 60, .3, .08, .1, .5, -.6); noiseq(K['schon'], .15, .06, .1, 30, S)
# Fehler-Kreuze
for k, d in [('fehler', 0), ('links1', 0)]: blip(K[k] + d, 40, .18, .08, 0, .5); blip(K[k] + d + .02, 41, .18, .05, 0, .25)
# Kalender fällt, Straße bricht, Haltestelle ohne Bus
blip(K['sechs'] - .2, 76, .15, .05, .5, .25, -.4); noiseq(K['sechs'] + .05, .08, .06, .5, 40, S)
blip(K['ohne'] - .02, 45, .3, .07, 0, .5, -.3); blip(K['auto'], 40, .15, .06, 0, .5, -.2)   # Auto verpufft, Strich
blip(K['nicht'] - .03, 40, .18, .07, 0, .5); blip(K['nicht'] - .01, 41, .18, .05, 0, .25)     # Weg bricht ab
# Ampel schaltet, Schild fällt und schlägt auf, Lehrerin tippelt
for i, n in enumerate([60, 64, 72]): blip(K['bei'] + i * .15, n, .05, .06, -.3)
blip(K['gruen'] - .1, 84, .3, .05, .3, .25, -.6); noiseq(K['pfeil'] + .1, .12, .09, .3, 25, S)
for a in np.arange(K['ueben'] - .3, K['ueben'] + .4, 1 / 6): noiseq(a, .02, .03, -.5, 120, S)
# Fadenkreuz rastet ein
for i in range(3): blip(K['schwach'] - .3 + i * .1, 88, .03, .04, 0, .125)
blip(K['schwach'], 91, .1, .05)
# Probefahrt: Münzen (Checkpunkte) – gleiche Formel wie im Film
for a in [K['echten'], K['strecke'] + .45]:   # Münze beim Ausweichen, wie im Film (DODGE)
    blip(a, 83, .05, .05, .2); blip(a + .05, 88, .15, .05, .2)
for a in [K['sitzt']]: blip(a, 91, .08, .05)   # Häkchen am Fähigkeitsfenster
# Boss fällt von oben und landet
blip(LAND - .35, 70, .3, .05, .3, .5, -.7); noiseq(LAND, .25, .14, .3, 14, S)
# Hit-Stop: harter Treffer, dann Stempel, Münzen sprühen
noiseq(HIT, .06, .12, 0, 20, S); blip(HIT, 36, .15, .08, 0, .5, -.5)
for i in range(10): blip(hs + HW + .15 + i * .07, 83 + (i % 3) * 2, .05, .035, -.4 + i * .08)
# Morgen: Auto startet, parkt, Tür
blip(K['mont'], 36, .5, .04, -.2, .5, .5); noiseq(K['selbst'] + .1, .1, .05, .3, 40, S); blip(K['selbst'] + .25, 60, .05, .04, .3)
# Schild fällt ins Schlussbild, Münzen
noiseq(K['gruen2'], .15, .1, -.4, 20, S)
for i in range(8): blip(K['kostenlos'] - .1 + i * .06, 86, .04, .03, -.3 + i * .08)
# Wort „bestanden“ freistellen: Musik und Effekte darum herum stark absenken
tn = np.arange(N) / SR; duck = 1 - .9 * np.clip(np.minimum((tn - (HIT + .04)) / .1, ((hs + HW) - tn) / .1), 0, 1)
M *= duck[:, None]; S *= duck[:, None]
os.makedirs('out', exist_ok=True)
def room(x, d=.09, g=.25):  # kleiner Raumhall (Echo), passend zur Konsole
    y = x.copy(); n = int(d * SR); y[n:] += x[:-n] * g; y[2 * n:] += x[:-2 * n] * g * .5; return y
for name, buf, pk in [('musik', room(M), .6), ('sfx', room(S, .06, .15), .8)]:
    sf.write(f'out/{name}.wav', (buf / (np.abs(buf).max() + 1e-9) * pk).astype(np.float32), SR)
print('ok')

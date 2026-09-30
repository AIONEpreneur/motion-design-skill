#!/usr/bin/env python3
"""Klarwerk Reinigung V4 – eigene Musik + Effekte (reduziert, modern wie ein App-Spot: E-Piano-Plucks, weiche Bässe, leichte Claps).
Dramaturgie: Montagmorgen-Chaos (e-Moll, stolpernder Puls, Fliege) -> Termin-Druck (Handy vibriert, Puls schneller)
-> Wendung „Klarwerk“: Kreis wird türkis = heller Glockenakkord, G-Dur-Groove 118 BPM -> App: jeder Tipp ein Ton, Preis zählt
-> abends ruhiger (nur Pad + Plucks) -> Benachrichtigungen: aufsteigende Ping-Tonleiter -> Küche glänzt (Glitzer) -> Logo (3 Holz-Klicks) + Schlussakkord.
Effekte aus dem Material: klebender Schuh, Geschirr, Fliege, Vibration, Taps, Tippen, Wischmopp auf Fliesen, Häkchen-Pings, Türklinke."""
import numpy as np, soundfile as sf, os, json
SR = 48000; Z = json.load(open('out/zeiten.json')); K = Z['K']; DUR = Z['DUR']; N = int(DUR * SR); R = np.random.default_rng(3)
M = np.zeros((N, 2)); S = np.zeros((N, 2))
def tt(d): return np.arange(int(d * SR)) / SR
def put(buf, a, x, pan=0.):
    i = int(a * SR)
    if i < 0: x = x[-i:]; i = 0
    n = min(len(x), N - i)
    if n > 0: buf[i:i + n, 0] += x[:n] * np.cos((pan + 1) * np.pi / 4) * 1.41; buf[i:i + n, 1] += x[:n] * np.sin((pan + 1) * np.pi / 4) * 1.41
def bp(x, fc, q=2.):
    w = 2 * np.pi * fc / SR; al = np.sin(w) / (2 * q); b0, b2, a0, a1, a2 = al, -al, 1 + al, -2 * np.cos(w), 1 - al
    y = np.zeros_like(x); x1 = x2 = y1 = y2 = 0.
    for i in range(len(x)): y0 = (b0 * x[i] + b2 * x2 - a1 * y1 - a2 * y2) / a0; x2, x1 = x1, x[i]; y2, y1 = y1, y0; y[i] = y0
    return y / (np.abs(y).max() + 1e-9)
def nz(d): return R.standard_normal(int(d * SR))
def reverb(x, sec, mix):
    n = int(sec * SR); ir = R.standard_normal((n, 2)) * np.exp(-np.arange(n) / SR * 6 / sec)[:, None]; F = 1 << int(np.ceil(np.log2(len(x) + n))); out = np.zeros_like(x)
    for c in range(2): out[:, c] = np.fft.irfft(np.fft.rfft(x[:, c], F) * np.fft.rfft(ir[:, c], F), F)[:len(x)]
    out *= np.abs(x).max() / (np.abs(out).max() + 1e-9); return x * (1 - mix) + out * mix
def hz(n): return 440 * 2 ** ((n - 69) / 12)
def epiano(n, a, amp=.08, pan=0, d=1.2):
    t = tt(d); f = hz(n); x = (np.sin(2 * np.pi * f * t + .8 * np.sin(2 * np.pi * f * t) * np.exp(-t * 6)) + .2 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 9)) * np.exp(-t * 3.5)
    put(M, a, x * np.clip(t / .003, 0, 1) * amp, pan)
def pad(ns, a, b, amp=.025, att=.6):
    t = tt(b - a); e = np.clip(t / att, 0, 1) * np.clip((b - a - t) / .7, 0, 1)
    for i, n in enumerate(ns): f = hz(n); put(M, a, (np.sin(2 * np.pi * f * t) + .25 * np.sin(2 * np.pi * 2.003 * f * t)) * e * amp, -.5 + i / max(1, len(ns) - 1))
def bass(n, a, d, amp=.17):
    t = tt(d); f = hz(n); put(M, a, np.sin(2 * np.pi * f * t) * np.clip(t / .01, 0, 1) * np.clip((d - t) / .05, 0, 1) * np.exp(-t * 1.5) * amp)
def kick(a, amp=.28):
    t = tt(.3); put(M, a, np.sin(2 * np.pi * np.cumsum(48 + 100 * np.exp(-t * 34)) / SR) * np.exp(-t * 11) * amp)
def clap(a, amp=.045):
    t = tt(.18); put(M, a, bp(nz(.18), 1500, 1) * np.exp(-t * 26) * amp, .1)
def tick(a, amp=.02, pan=.3):
    t = tt(.04); put(M, a, bp(nz(.04), 8000, 2) * np.exp(-t * 120) * amp, pan)
def ping(n, a, amp=.07, pan=0):
    t = tt(.7); f = hz(n); put(S, a, (np.sin(2 * np.pi * f * t) + .3 * np.sin(2 * np.pi * 3 * f * t) * np.exp(-t * 20)) * np.exp(-t * 7) * amp, pan)

# 1) Chaos: e-Moll, stolpernder Puls (5/8-Gefühl)
pad([52, 55, 59], 0, K['klarwerk'], .02)
a = .15; i = 0
while a < K['und']:
    kick(a, .16 if i % 5 else .22); a += [.34, .34, .26, .34, .3][i % 5]; i += 1
for k, n in [('acht', 64), ('klebt', 62), ('quillt', 60), ('ueber', 59)]: epiano(n, K[k], .07, -.2); epiano(n - 12, K[k], .05, .2)
# 2) Termin-Druck: schneller Puls, tiefer Ton
for a in np.arange(K['und'], K['klarwerk'] - .2, .25): tick(a, .025)
for a in np.arange(K['und'], K['klarwerk'] - .2, .5): kick(a, .2); bass(40, a, .3, .12)
epiano(52, K['neun'], .1, 0, 2.0); epiano(58, K['neun'], .06, 0, 2.0)
# 3) Wendung: heller Akkord, G-Dur-Groove 118 BPM
for j, n in enumerate([67, 71, 74, 79, 83]): epiano(n, K['klarwerk'] - .08 + j * .03, .06, -.4 + .2 * j, 2.0)
b = 60 / 118; prog = [[43, 67, 71, 74], [40, 67, 71, 76], [36, 67, 72, 76], [38, 66, 69, 74]]
a = K['klarwerk'] + .1; i = 0
while a < K['ende'] - .2:
    c = prog[(i // 4) % 4]; evening = K['abends'] - .1 < a < K['jeder'] - .1
    if not evening: kick(a, .24 if i % 2 == 0 else .12)
    if i % 2 == 1 and not evening: clap(a, .04)
    tick(a + b / 2, .018, -.3)
    if i % 4 == 0: pad(c[1:], a, a + 4 * b + .3, .02); bass(c[0], a, 2 * b * .9, .16); bass(c[0] + 7, a + 2 * b, 2 * b * .85, .1)
    epiano(c[1 + i % 3] + 12, a + (b / 2 if i % 2 else 0), .035, -.3 + .3 * (i % 3), .8)
    i += 1; a += b
pad([55, 59, 62, 67, 71], K['ende'] - .3, DUR, .03, .4); bass(43, K['ende'] - .3, DUR - K['ende'], .15)
for n in [67, 71, 74, 79]: epiano(n, K['erste'] - .05, .06, (n - 72) / 10, 2.5)
M = reverb(M, 1.4, .2)

# ===== Effekte =====
# Fliege summt (nur vorher)
t = tt(K['und']); f = 210 + 30 * np.sin(2 * np.pi * 3.1 * t); fly = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * .5 + np.sin(2 * np.pi * np.cumsum(f) / SR) * .5
put(S, 0, fly * (.35 + .25 * np.sin(2 * np.pi * .6 * t)) * np.clip((K['und'] - t) / .2, 0, 1) * .02, .4)
# klebender Schuh: Schmatzen
t = tt(.6); sq = bp(nz(.6), 500, 4) * np.exp(-((t - .25) / .12) ** 2) + np.sin(2 * np.pi * np.cumsum(180 + 400 * t) / SR) * np.exp(-((t - .35) / .06) ** 2) * .5
put(S, K['klebt'] - .1, sq * .2, -.3)
# Geschirr quillt: Porzellan-Klirren
for j in range(7):
    t = tt(.4); f0 = 1800 + R.random() * 1600; put(S, K['quillt'] - .05 + j * .09 + R.random() * .03, (np.sin(2 * np.pi * f0 * t) + .5 * np.sin(2 * np.pi * f0 * 2.7 * t)) * np.exp(-t * 18) * .06, .2 + R.random() * .4)
t = tt(1.0); put(S, K['ueber'], bp(nz(1.0), 3000, 1.5) * np.exp(-t * 3) * .04, .3)    # Schaum
# Handy vibriert + Kalender-Ton
t = tt(.5); put(S, K['neun'] - .02, np.sin(2 * np.pi * 150 * t) * (np.sin(2 * np.pi * 12 * t) > 0) * np.exp(-t * 2) * .12)
ping(76, K['neun'], .06); ping(72, K['neun'] + .12, .06)
# Wendung: Kreis wird türkis – weiche Glocke
t = tt(1.5); put(S, K['klarwerk'] - .05, sum(np.sin(2 * np.pi * hz(n) * t) for n in [79, 86, 91]) * np.exp(-t * 3) * .03)
# Taps, Tippen, Auswahl, Preiszählen, Gebucht
def tap(a, amp=.12): t = tt(.05); put(S, a, (bp(nz(.05), 2400, 3) * .6 + np.sin(2 * np.pi * 900 * t)) * np.exp(-t * 110) * amp, -.1)
for a in [K['reinigung'], K['app'] - .28, K['flaeche'] - .2, K['waehlen'], K['sofort'] - .05]: tap(a)   # V7: genau die Klicks im Bild
for j in range(3): t = tt(.04); put(S, K['flaeche'] + .05 + j * .13, bp(nz(.04), 3500, 4) * np.exp(-t * 140) * .08, -.2)
ping(84, K['festpreis'], .05, .3); ping(91, K['festpreis'] + .06, .03, .3)   # V7: Preis steht sofort da (kein Hochzähl-Ticken)
ping(79, K['sofort'] + .02, .07); ping(86, K['sofort'] + .14, .06)
# Stoppuhr-Ticks während der Minute
for a in np.arange(K['buchen'], K['minute'] + .1, .25): t = tt(.02); put(S, a, np.sin(2 * np.pi * 3200 * t) * np.exp(-t * 250) * .025, .5)
# abends: Wischmopp auf Fliesen (quietschen + nasses Wischen)
d = K['jeder'] - K['abends']; t = tt(d); mop = bp(nz(d), 1100, 1.5) * (.5 + .5 * np.sin(2 * np.pi * 2.5 * t)) ** 2
put(S, K['abends'], mop * np.clip(t / .2, 0, 1) * np.clip((d - t) / .2, 0, 1) * .05, -.3)
t = tt(.25); put(S, K['abends'] + .6, np.sin(2 * np.pi * np.cumsum(1500 + 700 * np.sin(2 * np.pi * 6 * t)) / SR) * np.sin(np.pi * t / .25) * .02, -.3)
# Benachrichtigungen: aufsteigende Pings (6 Räume) – Zeiten wie im Film
ts = K['pings']   # V7: dieselben Zeiten wie die Mitteilungen im Bild
for i, a in enumerate(ts): ping([74, 76, 78, 79, 81, 83][i], a, .07, -.3 + .12 * i); ping([74, 76, 78, 79, 81, 83][i] + 7, a + .08, .04, -.3 + .12 * i)
# Küche glänzt: Glitzer; Türklinke; Begrüßung (Handschlag)
for j in range(14): t = tt(.5); put(S, K['glaenzt'] - .1 + j * .08 + R.random() * .04, np.sin(2 * np.pi * (3000 + R.random() * 3000) * t) * np.exp(-t * 14) * .03, R.random() * 2 - 1)
t = tt(.15); put(S, K['kunde2'] - .35, bp(nz(.15), 1800, 6) * np.exp(-t * 40) * .1 + np.sin(2 * np.pi * 700 * t) * np.exp(-t * 60) * .05, .7)
t = tt(.12); put(S, K['kommen'] + .3, bp(nz(.12), 900, 2) * np.exp(-t * 50) * .08, .3)
# Logo: drei Holz-Klicks, Wortmarke
for j in range(3): t = tt(.12); put(S, K['ende'] - .7 + j * .14, np.sin(2 * np.pi * (700 + j * 120) * t) * np.exp(-t * 55) * .12, -.3 + .3 * j)
t = tt(.2); put(S, K['erste'], np.sin(2 * np.pi * np.cumsum(500 + 800 * t / .2) / SR) * np.exp(-t * 18) * .07)
S = reverb(S, .8, .12)
os.makedirs('out', exist_ok=True)
for name, buf, pk in [('musik', M, .6), ('sfx', S, .8)]:
    sf.write(f'out/{name}.wav', (buf / (np.abs(buf).max() + 1e-9) * pk).astype(np.float32), SR)
print('ok')

#!/usr/bin/env python3
"""Riegel 24 V4 – eigene Musik + Effekte. Dramaturgie folgt dem Kunden:
Nacht/ausgesperrt (e-Moll, Spieluhr + tiefer Puls, Uhr tickt) -> Suche/Preise (Puls wird dichter)
-> Fall durch den Flur (steigender Ton-Sog, Trommel beschleunigt) -> Sternburst (ein Schlag, Stille)
-> Festpreis/Techniker (G-Dur, gezupfte Gitarre, ruhiger Groove) -> Klick/Tür auf (Aufhellung) -> Marke (warmer Schluss).
Effekte nur aus dem Bild: Tür knallt, Schlüssel klirren, Akku piept, Licht aus/an, Tippen, Glas bricht, Scherben,
Preisschilder schlagen auf, Anrufton, Stempel, Schritte, Folie gleitet, Bohrer stirbt ab, Klick, Tür knarrt, Taste."""
import numpy as np, soundfile as sf, os, json
SR = 48000; Z = json.load(open('out/zeiten.json')); K = Z['K']; DUR = Z['DUR']; N = int(DUR * SR); R = np.random.default_rng(18)
M = np.zeros((N, 2)); S = np.zeros((N, 2))
def tt(d): return np.arange(int(round(d * SR))) / SR
def put(buf, a, x, pan=0.):
    i = int(a * SR); n = min(len(x), N - i)
    if n > 0 and i >= 0: buf[i:i + n, 0] += x[:n] * np.cos((pan + 1) * np.pi / 4) * 1.41; buf[i:i + n, 1] += x[:n] * np.sin((pan + 1) * np.pi / 4) * 1.41
def reso(x, fc, q):
    w = 2 * np.pi * fc / SR; r = np.exp(-w / (2 * q)); c1, c2 = 2 * r * np.cos(w), -r * r; y = np.zeros(len(x)); y1 = y2 = 0.
    for i in range(len(x)): y0 = x[i] + c1 * y1 + c2 * y2; y[i] = y0; y2, y1 = y1, y0
    return y / (np.abs(y).max() + 1e-9)
def nz(d, fc, q=2): return reso(R.standard_normal(int(round(d * SR))), fc, q)
def reverb(x, sec, mix):
    n = int(sec * SR); ir = R.standard_normal((n, 2)) * np.exp(-np.arange(n) / SR * 6 / sec)[:, None]; F = 1 << int(np.ceil(np.log2(len(x) + n))); out = np.zeros_like(x)
    for c in range(2): out[:, c] = np.fft.irfft(np.fft.rfft(x[:, c], F) * np.fft.rfft(ir[:, c], F), F)[:len(x)]
    out *= np.abs(x).max() / (np.abs(out).max() + 1e-9); return x * (1 - mix) + out * mix
def hz(n): return 440 * 2 ** ((n - 69) / 12)
def musicbox(n, a, amp=.05, pan=0):
    t = tt(1.6); f = hz(n); x = (np.sin(2 * np.pi * f * t) + .4 * np.sin(2 * np.pi * f * 3.01 * t) * np.exp(-t * 6) + .2 * np.sin(2 * np.pi * f * 5.2 * t) * np.exp(-t * 12)) * np.exp(-t * 3)
    put(M, a, x * np.clip(t / .001, 0, 1) * amp, pan)
def guitar(n, a, amp=.08, pan=0, d=1.6):  # Karplus-Strong
    f = hz(n); p = int(SR / f); L = int(d * SR); buf = R.uniform(-1, 1, p); y = np.zeros(L)
    for i in range(L): y[i] = buf[i % p]; buf[i % p] = .5 * (buf[i % p] + buf[(i + 1) % p]) * .996
    put(M, a, y * amp, pan)
def pad(ns, a, b, amp=.025):
    t = tt(b - a); e = np.clip(t / .7, 0, 1) * np.clip((b - a - t) / .6, 0, 1)
    for i, n in enumerate(ns): f = hz(n); put(M, a, (np.sin(2 * np.pi * f * t) + .5 * np.sin(2 * np.pi * f * 1.005 * t + 1)) * .5 * e * amp, -.5 + i / max(1, len(ns) - 1))
def kick(a, amp=.3):
    t = tt(.4); ph = 2 * np.pi * np.cumsum(44 + 90 * np.exp(-t * 28)) / SR; put(M, a, np.sin(ph) * np.exp(-t * 8) * amp)
def tom(a, amp=.2, f0=110):
    t = tt(.35); put(M, a, np.sin(2 * np.pi * np.cumsum(f0 * (1 + .6 * np.exp(-t * 20))) / SR) * np.exp(-t * 10) * amp, .2)
def rim(a, amp=.05): t = tt(.08); put(M, a, nz(.08, 2200, 6) * np.exp(-t * 60) * amp, -.2)
def bass(n, a, d, amp=.15):
    t = tt(d); f = hz(n); put(M, a, np.sin(2 * np.pi * f * t) * np.clip(t / .01, 0, 1) * np.clip((d - t) / .05, 0, 1) * np.exp(-t * 1.2) * amp)
# 1) Nacht 0–5.4: e-Moll, Spieluhr, Herzschlag-Puls
pad([52, 55, 59], .1, K['suchen'] + .3, .02)
mel = [76, 79, 71, 74, 72, 71, 67, 71]
for i, a in enumerate(np.arange(.9, K['suchen'], .55)): musicbox(mel[i % 8], a, .045, -.3 + .1 * (i % 6))
for a in np.arange(K['kurz'], K['suchen'], .9): kick(a, .14); kick(a + .2, .08)
# 2) Suche 5.4–8.1: Puls wird dichter, Moll-Bass
for i, a in enumerate(np.arange(K['suchen'], K['preis'] + .1, .3)):
    kick(a, .12 + .01 * i if i % 2 == 0 else .06); bass([40, 40, 36, 38][(i // 4) % 4], a, .28, .1)
    musicbox([76, 74, 72, 71][i % 4], a + .15, .03, .3)
# 3) Fall 8.3–11.4: steigender Ton-Sog (Shepard-artig), Trommel beschleunigt
d = K['riegel'] - .2 - (K['preis'] + .25); t = tt(d); x = np.zeros(len(t))
for k in range(5):
    f = 55 * 2 ** ((k + (t / d) * 1.5) % 5); w = np.sin(np.pi * ((k + (t / d) * 1.5) % 5) / 5) ** 2; x += np.sin(2 * np.pi * np.cumsum(f) / SR) * w
put(M, K['preis'] + .25, x * np.clip(t / .3, 0, 1) * .05)
a = K['preis'] + .3; step = .32
while a < K['riegel'] - .25: tom(a, .18, 90 + 40 * (a - K['preis']) / 3); a += step; step = max(.08, step * .9)
for k, n in [('p50', 52), ('p100', 55), ('p300', 58)]: bass(n - 12, K[k], .5, .2)
# 4) Wendung: ein Schlag, dann G-Dur
kick(K['riegel'] - .18, .5)
prog = [[43, 59, 62, 67], [38, 57, 62, 66], [40, 59, 64, 67], [36, 55, 60, 64]]
B = .52; a = K['riegel'] + .5; i = 0
while a < K['name'] - .1:
    c = prog[(i // 4) % 4]
    if i % 4 == 0: pad(c[1:], a, a + B * 4 + .1, .018); bass(c[0], a, B * 1.8, .14)
    if i % 2 == 0: kick(a, .18)
    else: rim(a, .05)
    guitar(c[1 + i % 3], a, .07, -.4 + .2 * (i % 3), 1.0); guitar(c[1 + (i + 2) % 3] + 12, a + B / 2, .045, .35, .8)
    i += 1; a += B
for n in [55, 59, 62, 67, 71]: musicbox(n + 12, K['klick'] + .3 + (n - 55) * .006, .04)
# 5) Marke: warmer Schlussakkord + Spieluhr in Dur
for n in [43, 55, 62, 67, 71]: guitar(n, K['name'] + .3, .06, 0, 2.5)
for i, n in enumerate([79, 83, 86, 91]): musicbox(n, K['name'] + .6 + i * .18, .04, -.3 + .2 * i)
a = K['name'] + .3; i = 0
while a < DUR - 1.6:
    if i % 2 == 0: kick(a, .14)
    guitar([55, 59, 62, 59][i % 4] + 12, a + B / 2, .035, .3, .7); i += 1; a += B
for n in [43, 50, 55, 59, 62, 67]: guitar(n, DUR - 1.6, .06, 0, 1.6)
M = reverb(M, 2.0, .25)

# --- Effekte ---
def thud(a, amp=.3, f0=60, q=2):
    t = tt(.5); put(S, a, (np.sin(2 * np.pi * (f0 + 50 * np.exp(-t * 25)) * t) * np.exp(-t * 9) + nz(.5, 900, q) * np.exp(-t * 40) * .3) * amp)
thud(K['zu'] + .15, .5, 55); t = tt(.3); put(S, K['zu'] + .2, nz(.3, 3200, 8) * np.exp(-t * 18) * .08, .3)       # Tür knallt + Klinke
for i in range(5): t = tt(.25); put(S, K['schluessel'] + .6 + i * .11, nz(.25, 4000 + 900 * (i % 3), 20) * np.exp(-t * 20) * .05, .4)  # Schlüssel klirren
for a in np.arange(.1, K['suchen'], .5): t = tt(.03); put(S, a, nz(.03, 2800, 8) * np.exp(-t * 200) * .05, -.4)     # Uhr tickt
for d0 in [0, .18]: t = tt(.1); put(S, K['akku'] + d0, np.sin(2 * np.pi * 1760 * t) * np.clip((.1 - t) / .01, 0, 1) * .05, .2)  # Akku piept
t = tt(.06); put(S, K['leer'] + .05, nz(.06, 3000, 3) * np.exp(-t * 90) * .15)                                     # Licht aus (Klick)
t = tt(.05); put(S, K['notdienst'] - .25, nz(.05, 3500, 4) * np.exp(-t * 120) * .08, .3)  # V7: ein Antippen, Suchbegriff steht als Ganzes (kein Tipp-Geräusch)
t = tt(.15); put(S, K['folie'] - .25, nz(.15, 1500, 1) * np.exp(-t * 40) * .1, .3)  # V7: Zettel „Folie“ klatscht an
t = tt(.6); put(S, K['preis'] - .02, (nz(.6, 5200, 6) * np.exp(-t * 9) + nz(.6, 1800, 3) * np.exp(-t * 20) * .5) * .18, .1)  # Glas bricht
for i in range(14): t = tt(.2); put(S, K['preis'] + .35 + R.random() * .6, nz(.2, 3000 + R.random() * 4000, 25) * np.exp(-t * 25) * .04, R.uniform(-.8, .8))  # Scherben
for k in ['p50', 'p100', 'p300']: thud(K[k] + .05, .3, 80)                                                          # Preisschilder
t = tt(.6); put(S, K['riegel'] - .18, (nz(.6, 400, 1) * np.exp(-t * 6) + nz(.6, 2500, 1) * np.exp(-t * 14) * .4) * .4)  # Sternburst
for d0 in [0, .5]: t = tt(.35); put(S, K['riegel'] + .45 + d0, (np.sin(2 * np.pi * 425 * t)) * np.clip(t / .01, 0, 1) * np.clip((.35 - t) / .02, 0, 1) * .025, .3)  # Freizeichen
thud(K['festpreis'] + .1, .35, 70)                                                                                     # Preis-Stempel
for i, a in enumerate(np.arange(K['zwanzig'] + .1, K['da'] + .1, .31)): thud(a, .07, 110 + 10 * (i % 2), 4)           # Schritte
t = tt(.06); put(S, K['zwanzig'] + .1, nz(.06, 3000, 3) * np.exp(-t * 90) * .12)                                        # Licht an
t = tt(.8); put(S, K['folie'] - .2, nz(.8, 6000, 2) * np.sin(np.pi * t / .8) * .05, .3)                                # Folie gleitet
t = tt(.5); f = 180 * (1 - .7 * t / .5); put(S, K['ohne'] + .1, np.tanh(3 * np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-t * 3) * (t < .4) * .04, -.3)  # Bohrer stirbt ab
t = tt(.12); put(S, K['klick'], (nz(.12, 4200, 10) * np.exp(-t * 80) + nz(.12, 1200, 6) * np.exp(-np.abs(t - .03) * 150) * .7) * .3)  # Klick
t = tt(.9); f = 300 + 180 * np.sin(np.pi * t / .9) + 30 * np.sin(2 * np.pi * 23 * t); put(S, K['klick'] + .45, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / .9) * nz(.9, 800, 1) * .06)  # Tür knarrt
for i in range(4): t = tt(.25); put(S, K['name'] + .5 + i * .09, nz(.25, 4500 + 700 * (i % 2), 20) * np.exp(-t * 18) * .04, -.3)  # Schlüssel (Logo)
t = tt(.08); put(S, K['nummer'] + .4, nz(.08, 1500, 3) * np.exp(-t * 80) * .1)                                          # Taste
for i, n in enumerate([88, 93]): t = tt(.4); put(S, K['brauchen'] + i * .1, np.sin(2 * np.pi * hz(n) * t) * np.exp(-t * 9) * .05, .2)  # gespeichert
S = reverb(S, .9, .15)
os.makedirs('out', exist_ok=True)
for name, buf, pk in [('musik', M, .6), ('sfx', S, .8)]:
    sf.write(f'out/{name}.wav', (buf / (np.abs(buf).max() + 1e-9) * pk).astype(np.float32), SR)
print('ok')

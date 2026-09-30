#!/usr/bin/env python3
"""Domus V4 – eigene Musik + Effekte (numpy, 48 kHz Stereo, liest out/zeiten.json).
Dramaturgie: Sonntagabend-Problem (d-Moll, Uhr-Puls, Tropfen) -> Wochenende weg (Stille + tiefer Ton)
-> Wendung Pixel-Auflösung (Glitzer-Arpeggio) -> Domus-Lösung (F-Dur, leichter Produktvideo-Groove, Zupf-Synth)
-> Esstisch (warm, Groove bleibt, leiser) -> Schluss (Akkord). Effekte aus dem Material des Themas:
Wassertropfen, Handy-Vibration, Freizeichen, Nachrichten-Pops, Papier, Kreide-Strich, Tastatur, Klicks, Kamera, Besteck."""
import numpy as np, soundfile as sf, os, json
SR = 48000; Z = json.load(open('out/zeiten.json')); K = Z['K']; DUR = Z['DUR']; N = int(DUR * SR); R = np.random.default_rng(10)
M = np.zeros((N, 2)); S = np.zeros((N, 2))
def tt(d): return np.arange(int(d * SR)) / SR
def put(buf, a, x, pan=0.):
    i = int(a * SR); n = min(len(x), N - i)
    if n > 0 and i >= 0: buf[i:i + n, 0] += x[:n] * np.cos((pan + 1) * np.pi / 4) * 1.41; buf[i:i + n, 1] += x[:n] * np.sin((pan + 1) * np.pi / 4) * 1.41
def reso(x, fc, q):
    w = 2 * np.pi * fc / SR; r = np.exp(-w / (2 * q)); c1, c2 = 2 * r * np.cos(w), -r * r; y = np.zeros(len(x)); y1 = y2 = 0.
    for i in range(len(x)): y0 = x[i] + c1 * y1 + c2 * y2; y[i] = y0; y2, y1 = y1, y0
    return y / (np.abs(y).max() + 1e-9)
def nz(d, fc, q=2): return reso(R.standard_normal(int(d * SR)), fc, q)
def reverb(x, sec, mix):
    n = int(sec * SR); ir = R.standard_normal((n, 2)) * np.exp(-np.arange(n) / SR * 6 / sec)[:, None]; F = 1 << int(np.ceil(np.log2(len(x) + n))); out = np.zeros_like(x)
    for c in range(2): out[:, c] = np.fft.irfft(np.fft.rfft(x[:, c], F) * np.fft.rfft(ir[:, c], F), F)[:len(x)]
    out *= np.abs(x).max() / (np.abs(out).max() + 1e-9); return x * (1 - mix) + out * mix
def hz(n): return 440 * 2 ** ((n - 69) / 12)
def pluck(n, a, amp=.07, pan=0, dec=6.5):  # Zupf-Synth (Produktvideo)
    t = tt(1.2); f = hz(n); x = (np.sin(2 * np.pi * f * t) + .45 * np.sin(4 * np.pi * f * t + np.sin(2 * np.pi * f * t) * 1.5) * np.exp(-t * 12)) * np.exp(-t * dec)
    put(M, a, x * np.clip(t / .002, 0, 1) * amp, pan)
def pad(ns, a, b, amp=.03, bright=0.):
    t = tt(b - a); e = np.clip(t / .9, 0, 1) * np.clip((b - a - t) / .8, 0, 1)
    for i, n in enumerate(ns): f = hz(n); x = np.sin(2 * np.pi * f * t) + np.sin(2 * np.pi * f * 1.004 * t + 1) + bright * .3 * np.sin(6 * np.pi * f * t); put(M, a, x * .5 * e * amp, -.6 + 1.2 * i / max(1, len(ns) - 1))
def kick(a, amp=.3): t = tt(.35); ph = 2 * np.pi * np.cumsum(48 + 110 * np.exp(-t * 32)) / SR; put(M, a, np.sin(ph) * np.exp(-t * 10) * amp)
def clap(a, amp=.05): t = tt(.2); put(M, a, nz(.2, 1700, 1) * np.exp(-t * 26) * amp, .1)
def hat(a, amp=.02): t = tt(.06); put(M, a, nz(.06, 8000, 1.5) * np.exp(-t * 70) * amp, .3)
def bass(n, a, d, amp=.15): t = tt(d); f = hz(n); x = np.tanh(1.6 * (np.sin(2 * np.pi * f * t) + .3 * np.sin(4 * np.pi * f * t))); put(M, a, x * np.clip(t / .01, 0, 1) * np.clip((d - t) / .04, 0, 1) * amp)
BEAT = 60 / 112
# 1) Problem: d-Moll-Fläche, Uhr-Ticken als Puls, tiefe Pluck-Töne auf den Schlüsselwörtern
turn = K['mit']
pad([50, 53, 57], .1, K['wochenende'] + .3, .024)
a = .2
while a < K['wochenende'] - .1:
    t = tt(.04); put(M, a, nz(.04, 3200, 6) * np.exp(-t * 120) * .05, .4)  # Uhr tick
    a += BEAT
for k, ns in [('wasser', [50, 57]), ('niemand', [46, 53]), ('n20', [48, 55]), ('belege', [45, 52])]:
    for n in ns: pluck(n + 12, K[k], .07, 0, 3.5)
for i in range(8):  # nervöser Puls ab „Dazu“
    kick(K['dazu'] + i * BEAT / 2, .12 + i * .01)
# 2) Wochenende weg: tiefer Ton, dann Luft
for n in [38, 45]: pluck(n, K['weg'], .16, 0, 1.2)
pad([38, 45, 50], K['weg'], turn + .2, .02)
# 3) Wendung: Glitzer-Arpeggio (Pixel)
for i, n in enumerate([65, 69, 72, 77, 81, 84]): pluck(n, turn - .15 + i * .07, .05, -.5 + i * .2, 7)
# 4) Lösung: F – C – d – B, leichter Groove bis zum Esstisch, dann weicher bis Schluss
prog = [[41, 65, 69, 72], [36, 64, 67, 72], [38, 62, 65, 69], [34, 62, 65, 70]]
a = K['domus'] - .05; i = 0
while a < DUR - 1.2:
    c = prog[(i // 4) % 4]; soft = a > K['bleiben'] - .2; end = a > K['schluss'] - .1
    if i % 4 == 0: pad(c[1:], a, a + BEAT * 4 + .3, .02 if not soft else .026, .5); bass(c[0], a, BEAT * 1.8, .12 if not soft else .08)
    if i % 2 == 0: kick(a, .24 if not soft else .15)
    elif not soft: clap(a, .05)
    hat(a + BEAT / 2, .018)
    if not end: pluck(c[1 + i % 3] + 12, a, .04, -.3 + .3 * (i % 3)); pluck(c[1 + (i + 1) % 3] + 12, a + BEAT / 2, .03, .3)
    i += 1; a += BEAT
for n in [41, 53, 60, 65, 69, 72, 77]: pluck(n, K['kostenlos'] + .15, .07, 0, 1.4)
pad([53, 60, 65, 69], K['kostenlos'] + .1, DUR, .025, .5)
M = reverb(M, 1.8, .22)

# --- Effekte ---
def dropfx(a, amp=.06, pan=0):  # Wassertropfen: Plink mit fallender Tonhöhe
    t = tt(.18); f = 1400 + 900 * np.exp(-t * 60); put(S, a, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 30) * amp, pan)
rd = np.random.default_rng(3)
for a in np.arange(.25, turn - .2, .33): dropfx(a + rd.random() * .2, .025 + rd.random() * .03, rd.random() * 1.6 - .8)
def buzz(a, d=.5, amp=.12):  # Handy vibriert
    t = tt(d); put(S, a, np.sin(2 * np.pi * 150 * t) * (np.sin(2 * np.pi * 22 * t) > 0) * np.clip(t / .01, 0, 1) * np.clip((d - t) / .02, 0, 1) * amp)
buzz(.3); buzz(K['kueche'] - .1, .35, .08); buzz(K['bleiben'] + .02, .4, .08)
t = tt(.25); put(S, .08, (np.sin(2 * np.pi * 80 * t) * .6 + nz(.25, 600, 1) * .4) * np.exp(-t * 20) * .2)       # Handy landet
def keys(a, n, cps, amp=.035):  # Tastatur: Tippen der Schlagwörter
    for k in range(n):
        t = tt(.03); put(S, a + k / cps + rd.random() * .01, nz(.03, 3500 + rd.random() * 1500, 3) * np.exp(-t * 160) * amp, rd.random() * .6 - .3)
# V7: keine Tipp-Geräusche mehr (es wird nichts getippt). Stattdessen weiche „Pop“-Töne, wo ein Wort am Objekt erscheint.
def pop(a, f=1200, amp=.035, pan=0.):
    t = tt(.12); put(S, a, np.sin(2 * np.pi * f * t * (1 + .3 * np.exp(-t * 40))) * np.exp(-t * 32) * amp, pan)
for k, f in [('wasser', 900), ('schaden', 1000), ('n30', 1100), ('live', 1300), ('monat', 900)]: pop(K[k] - .06, f)
def ring(a, d=.5):  # Freizeichen
    t = tt(d); put(S, a, (np.sin(2 * np.pi * 425 * t)) * np.clip(t / .02, 0, 1) * np.clip((d - t) / .02, 0, 1) * .05, .2)
def nope(a):  # Keine Antwort: zwei tiefe Töne
    for k, f in enumerate([370, 290]): t = tt(.12); put(S, a + k * .13, np.sin(2 * np.pi * f * t) * np.exp(-t * 8) * .06, .2)
for tp in [K['handwerker'] - .05, K['handwerker'] + .45, K['an'] + .05]:  # V7: Klicks des Zeigers = Anrufzeiten im Film (TC)
    t = tt(.04); put(S, tp, nz(.04, 2500, 2) * np.exp(-t * 90) * .08, .3); ring(tp + .05, .4); nope(tp + .47)
for k in range(20):  # Nachrichten-Pops, immer schneller
    a = K['dazu'] + .05 + (K['n20'] + .45 - K['dazu'] - .05) * (1 - (1 - k / 20) ** 1.6); t = tt(.08); put(S, a, np.sin(2 * np.pi * (900 + k * 40) * t) * np.exp(-t * 45) * .04, rd.random() - .5)
for k in range(7):  # Belege: Papier
    t = tt(.18); put(S, K['belege'] - .45 + k * .06, nz(.18, 3000, 1) * np.exp(-t * 18) * .05, rd.random() - .5)
for k in range(3):  # Kalenderkacheln landen
    t = tt(.3); put(S, K['wochenende'] + .3 + k * .1, (np.sin(2 * np.pi * (90 - k * 8) * t) * np.exp(-t * 16) + nz(.3, 800, 2) * np.exp(-t * 40) * .3) * .14, -.5 + k * .5)
for k in range(2):  # Strich durchs Wochenende (Filzstift), wie im Film K.weg-.45 / K.weg-.27
    t = tt(.3); put(S, K['weg'] - .45 + k * .18, nz(.3, 1800, 4) * np.sin(np.pi * t / .3) * .09, -.2 + k * .4)
t = tt(.6); put(S, turn - .2, nz(.6, 6000, 3) * (np.sin(2 * np.pi * 30 * t) > 0) * np.sin(np.pi * t / .6) * .05)   # Pixel-Auflösung: Bitkörnung
def click(a, amp=.08): t = tt(.05); put(S, a, (nz(.05, 4200, 3) * .6 + np.sin(2 * np.pi * 1800 * t) * .4) * np.exp(-t * 110) * amp, .2)
for k in range(4): t = tt(.12); put(S, K['domus'] + .25 + k * .1, np.sin(2 * np.pi * hz(76 + [0, 4, 7, 12][k]) * t) * np.exp(-t * 30) * .035, -.4 + k * .25)  # Icons poppen
for a in [K['meldet_w'] - .2, K['portal'] - .3, K['foto'] - .3, K['beauftragt'] - .2, K['kostenlos'] - .1]: click(a)  # V7: an Zeiger-Klicks
t = tt(.25); put(S, K["foto"] - .3, nz(.25, 5000, 2) * np.exp(-t * 25) * .07)  # Kamera-Verschluss
for k, f in enumerate([880, 1320]): t = tt(.25); put(S, K['foto'] + .62 + k * .09, np.sin(2 * np.pi * f * t) * np.exp(-t * 14) * .04)  # gesendet
t = tt(.35); put(S, Z['CUT']['gh'] + .02, (np.sin(2 * np.pi * (140 + 80 * np.exp(-t * 20)) * t) * np.exp(-t * 14)) * .12)  # Meldung landet
for k in range(12): t = tt(.03); put(S, K['n30'] - .1 + k * .06, nz(.03, 5000, 5) * np.exp(-t * 150) * .03, .4)  # Uhr zählt
for k, f in enumerate([660, 880, 1100]): t = tt(.35); put(S, K['beauftragt'] + .1 + k * .07, np.sin(2 * np.pi * f * t) * np.exp(-t * 10) * .04)
for k, key in enumerate(['gemeldet', 'beauftragt2', 'erledigt']):  # Zeitleiste: steigende Glocken
    t = tt(.9); f = hz(79 + [0, 4, 7][k]); put(S, K[key], (np.sin(2 * np.pi * f * t) + .3 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 6)) * np.exp(-t * 4) * .06, -.5 + k * .5)
t = tt(.5); put(S, K['live'], np.sin(2 * np.pi * 1000 * t) * (np.sin(2 * np.pi * 8 * t) > 0) * np.exp(-t * 4) * .02, .5)   # Live-Punkt
for k in range(3): t = tt(.25); put(S, K['esstisch'] + .2 + k * .55, np.sin(2 * np.pi * (2900 + k * 300) * t) * np.exp(-t * 18) * .03, -.3 + k * .3)  # Besteck
t = tt(.3); put(S, K['schluss'] + .05, (np.sin(2 * np.pi * (110 + 60 * np.exp(-t * 25)) * t) * np.exp(-t * 12)) * .12)  # Logo landet
S = reverb(S, 1.0, .12)
os.makedirs('out', exist_ok=True)
for name, buf, pk in [('musik', M, .6), ('sfx', S, .8)]: sf.write(f'out/{name}.wav', (buf / (np.abs(buf).max() + 1e-9) * pk).astype(np.float32), SR)
print('ok')

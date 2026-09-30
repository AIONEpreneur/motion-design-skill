#!/usr/bin/env python3
"""Zahnfee V4 – eigene Musik + Effekte (numpy, 48 kHz Stereo, liest out/zeiten.json).
Dramaturgie: Hook (a-Moll, stolpernde Pizzicati) -> Zahnschmerz (tiefe Pochschläge) -> Angst ein Leben lang
(Brummen, Spieluhr verstimmt) -> Wendung Zahnfee (Harfen-Glissando, Glocken) -> Spielen/ohne Bohren/20 Minuten
(C-Dur, Marimba + Holzblock, hüpfend) -> Schluss (Glockenakkord). Instrumente passend zum gemalten Kinder-Cartoon.
Effekte nur, wo im Bild etwas passiert: Tür, Comic-Schlag, Bohrer-Surren, Pochen, Kalenderblatt, Thermometer,
Zauberstab, Stuhl-Hydraulik, Lampe, Filzstift-X, Pinsel, Uhr, Konfetti, Herzen, Schild."""
import numpy as np, soundfile as sf, os, json
SR = 48000; Z = json.load(open('out/zeiten.json')); K = Z['K']; DUR = Z['DUR']; N = int(DUR * SR); R = np.random.default_rng(21)
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
def pizz(n, a, amp=.08, pan=0):  # Pizzicato-Streicher
    t = tt(.5); f = hz(n); x = sum(np.sin(2 * np.pi * f * k * t) * np.exp(-t * (9 + k * 5)) / k for k in range(1, 6)); put(M, a, x * np.clip(t / .004, 0, 1) * amp, pan)
def marimba(n, a, amp=.09, pan=0):
    t = tt(.8); f = hz(n); x = (np.sin(2 * np.pi * f * t) + .35 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t * 30)) * np.exp(-t * 7); put(M, a, x * np.clip(t / .002, 0, 1) * amp, pan)
def glock(n, a, amp=.05, pan=0, buf=None):
    t = tt(1.6); f = hz(n); x = (np.sin(2 * np.pi * f * t) + .4 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 6) + .2 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 12)) * np.exp(-t * 2.8)
    put(M if buf is None else buf, a, x * np.clip(t / .001, 0, 1) * amp, pan)
def bassoon(n, a, d, amp=.1):
    t = tt(d); f = hz(n); ph = 2 * np.pi * f * t; x = np.tanh(2.2 * (np.sin(ph) + .5 * np.sin(2 * ph) + .3 * np.sin(3 * ph))) * np.clip(t / .05, 0, 1) * np.clip((d - t) / .08, 0, 1); put(M, a, x * amp, -.2)
def pad(ns, a, b, amp=.02):
    t = tt(b - a); e = np.clip(t / .8, 0, 1) * np.clip((b - a - t) / .8, 0, 1)
    for i, n in enumerate(ns): f = hz(n); put(M, a, (np.sin(2 * np.pi * f * t) + .5 * np.sin(2 * np.pi * f * 1.005 * t)) * e * amp, -.5 + i / max(1, len(ns) - 1))
def wood(a, amp=.05, f=1200, pan=.3): t = tt(.08); put(M, a, np.sin(2 * np.pi * f * t) * np.exp(-t * 60) * amp, pan)
def shaker(a, amp=.02): t = tt(.1); put(M, a, nz(.1, 7000, 1.5) * np.sin(np.pi * t / .1) * amp, -.3)
BEAT = 60 / 120
# 1) Hook: a-Moll, stolpernde Pizzicati
for i, n in enumerate([57, 60, 64, 60, 57, 59, 56, 59]): pizz(n, .15 + i * BEAT / 2, .07, -.3 + (i % 2) * .6)
pizz(45, K['bloss'], .12); pizz(52, K['bloss'], .1); pizz(44, K['zahnarzt'], .12)
# 2) Zahnschmerz: Fagott-Töne + Pochen im Herzschlag
bassoon(45, K['dabei'], 1.6, .08); bassoon(44, K['weh'] - .1, 1.2, .09); bassoon(41, K['jedes'], 2.4, .08)
for a in np.arange(K['weh'], K['angst0'], BEAT * 1.2):
    t = tt(.3); put(M, a, np.sin(2 * np.pi * 55 * t) * np.exp(-t * 14) * .18); put(M, a + .22, np.sin(2 * np.pi * 55 * t) * np.exp(-t * 18) * .1)
# 3) Angst: Brummen + verstimmte Spieluhr
pad([33, 40, 45], K['angst0'] - .2, K['bei'] + .1, .03)
for i, n in enumerate([81, 77, 76, 72, 71, 69]):
    t = tt(1.2); f = hz(n) * (1 - .012 * i); put(M, K['angst0'] + .1 + i * .42, np.sin(2 * np.pi * f * t) * np.exp(-t * 3.5) * .05, .4 - i * .15)
# 4) Wendung: Harfen-Glissando + Glocken
for i, n in enumerate(range(60, 88, 2)): pizz(n, K['bei'] - .25 + i * .03, .04, -.6 + i * .09)
for n in [72, 76, 79, 84]: glock(n, K['bei'] + .2, .05)
# 5) Spielen … bis Schluss: C-Dur, Marimba-Hüpfer, Holzblock, Shaker
prog = [[48, 64, 67, 72], [53, 65, 69, 72], [55, 67, 71, 74], [48, 64, 67, 72]]
a = K['anders'] - .1; i = 0
while a < DUR - 1.4:
    c = prog[(i // 4) % 4]; end = a > K['schluss'] - .1
    if i % 4 == 0: pad(c[1:], a, a + BEAT * 4 + .2, .016); pizz(c[0], a, .12, 0); pizz(c[0] + 7, a + BEAT * 2, .09, 0)
    marimba(c[1 + (i % 3)] + (12 if i % 2 else 0), a, .07, -.4 + .4 * (i % 3)); marimba(c[1 + ((i + 1) % 3)], a + BEAT / 2, .05, .4)
    if not end: wood(a + BEAT / 2, .04, 1400 if i % 2 else 1000); shaker(a + BEAT / 4); shaker(a + BEAT * .75)
    i += 1; a += BEAT
for n in [60, 64, 67, 72, 76, 79]: glock(n, K['kostenlos'] + .2, .05)
M = reverb(M, 2.0, .25)

# --- Effekte ---
t = tt(.6); put(S, .1, nz(.6, 900, 8) * np.sin(np.pi * t / .6) * (1 + .5 * np.sin(2 * np.pi * 18 * t)) * .05, -.4)                    # Tür knarrt
for a in [.5, K['bloss']]:  # Comic-Schlag
    t = tt(.5); put(S, a, (np.sin(2 * np.pi * (180 + 200 * np.exp(-t * 20)) * t) * np.exp(-t * 10) + nz(.5, 3000, .7) * np.exp(-t * 16) * .6) * .2)
def buzz(a, d, amp=.035, f=880):  # Bohrer-Surren
    t = tt(d); x = np.sin(2 * np.pi * np.cumsum(f + 40 * np.sin(2 * np.pi * 30 * t)) / SR) + .4 * np.sin(4 * np.pi * np.cumsum(f + 40 * np.sin(2 * np.pi * 30 * t)) / SR)
    put(S, a, x * np.clip(t / .05, 0, 1) * np.clip((d - t) / .1, 0, 1) * amp, .4)
buzz(.35, K['bloss'] - .5, .018)
buzz(K['behandeln'] - .1, K['ohne'] + .1 - K['behandeln'], .04, 1100)  # V7: Bohrer im Bild von „behandeln“ bis zum X auf „ohne“
for a in np.arange(K['weh'], K['jedes'] - .2, .5): t = tt(.2); put(S, a, np.sin(2 * np.pi * 70 * t) * np.exp(-t * 18) * .18)  # Pochen
for f in [K['tagen'] - .15, K['tagen'] + .12, K['warten'], K['macht'], K['loch']]:  # Kalenderblatt reißt (V7: wie im Film)
    t = tt(.35); put(S, f, nz(.35, 2600, 1.2) * (np.abs(np.sin(2 * np.pi * 40 * t)) ** 3) * np.exp(-t * 6) * .1, .1)
t = tt(K['lang'] + .3 - K['angst'] + .1); put(S, K['angst'] - .1, np.sin(2 * np.pi * np.cumsum(300 + 500 * (t / t[-1])) / SR) * .015 * np.clip(t / .3, 0, 1), .5)  # Thermometer steigt
t = tt(2.8); put(S, K['angst'], (np.sin(2 * np.pi * 41 * t) + .5 * np.sin(2 * np.pi * 61.5 * t)) * np.clip(t / 1.5, 0, 1) * np.clip((2.8 - t) / .4, 0, 1) * .09)  # Schatten wächst
for i in range(10):  # Zauberstab-Funkeln
    glock(96 - (i % 5) * 2, K['bei'] + .05 + i * .05, .02, -.6 + i * .12, S)
t = tt(1.0); put(S, K['besuch0'] + .5, (nz(1.0, 1800, 2) * .3 + np.sin(2 * np.pi * np.cumsum(200 + 300 * t) / SR) * .4) * np.sin(np.pi * t / 1.0) * .06)  # Stuhl-Hydraulik
t = tt(.8); put(S, K['gespielt'] - .3, (nz(.8, 1500, 2) * .3 + np.sin(2 * np.pi * np.cumsum(250 + 500 * t) / SR) * .4) * np.sin(np.pi * t / .8) * .07)
t = tt(.05); put(S, K['gespielt'], nz(.05, 3000, 3) * np.exp(-t * 100) * .12, .4)  # Lampe klickt
for k in range(2): t = tt(.2); put(S, K['ohne'] - .32 + k * .16, nz(.2, 2200, 5) * np.sin(np.pi * t / .2) * .1, .4)  # Filzstift-X
t = tt(.45); put(S, K['bohren'] + .05, nz(.45, 1200, 1.2) * np.sin(np.pi * t / .45) ** 2 * .07, -.2)  # Pinsel tupft
for i in range(6): glock(88 + [0, 4, 7, 12, 7, 16][i], K['bohren'] + .3 + i * .06, .02, -.4 + i * .15, S)
for k in range(10): t = tt(.04); put(S, K['n20'] - .1 + k * .12, nz(.04, 4000, 6) * np.exp(-t * 120) * .05, .3)  # Uhr tickt
glock(84, K['vorbei'] - .05, .06, 0, S); glock(88, K['vorbei'] + .08, .05, 0, S)
for k in range(12): t = tt(.06); put(S, K['vorbei'] + .05 + k * .03, nz(.06, 5000 + k * 200, 2) * np.exp(-t * 60) * .04, R.random() * 1.6 - .8)  # Konfetti
for k in range(6):  # Herzen poppen
    t = tt(.12); put(S, K['und'] + .1 + k * .4, np.sin(2 * np.pi * np.cumsum(500 + 900 * t / .12) / SR) * np.exp(-t * 20) * .05, -.3 + k * .1)
t = tt(.8); put(S, K['kza'] - .02, (np.sin(2 * np.pi * (90 + 40 * np.exp(-t * 10)) * t) * np.exp(-t * 7)) * .15)  # Schild landet
t = tt(.1); put(S, K['kennen'] - .1, np.sin(2 * np.pi * np.cumsum(400 + 1200 * t / .1) / SR) * np.exp(-t * 20) * .07)  # Knopf poppt
S = reverb(S, 1.0, .15)
os.makedirs('out', exist_ok=True)
for name, buf, pk in [('musik', M, .6), ('sfx', S, .8)]: sf.write(f'out/{name}.wav', (buf / (np.abs(buf).max() + 1e-9) * pk).astype(np.float32), SR)
print('ok')

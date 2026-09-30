#!/usr/bin/env python3
"""Netzwerk Nord IT V4/V6/V7 (V7: alle Zeiten aus neu vermessenem vo.json über zeiten.py) – eigene Musik + Effekte (numpy, 48 kHz Stereo, liest out/zeiten.json).
Dramaturgie: Problem im Büro (d-Moll, Uhr-Ticken, gedämpfter Puls) -> Wendung in die Blaupause (Stille, ein Sinuston)
-> Lösung (F-Dur, digitale Zupf-Arpeggios in Sechzehnteln, wie Datenpakete) -> Notfall (kurzer Bruch) -> „läuft alles“ (Aufhellung)
-> Büro läuft (leichter Groove) -> Schlussakkord. Effekte nur, wo im Bild etwas passiert: Tastatur, Lüfter fährt herunter,
Fehlerton, Ordner rutschen und zerfallen, Warn-Pings, Datenpulse, Laufwerk raus/rein, Schloss-Klicks, Stoppuhr, Mails."""
import numpy as np, soundfile as sf, os, json
SR = 48000; Z = json.load(open('out/zeiten.json')); DUR = Z['DUR']; K = Z['K']; N = int(DUR * SR); R = np.random.default_rng(11)
M = np.zeros((N, 2)); S = np.zeros((N, 2))
def tt(d): return np.arange(int(d * SR)) / SR
def put(buf, a, x, pan=0.):
    i = int(a * SR); n = min(len(x), N - i)
    if n > 0 and i >= 0: buf[i:i + n, 0] += x[:n] * np.cos((pan + 1) * np.pi / 4) * 1.41; buf[i:i + n, 1] += x[:n] * np.sin((pan + 1) * np.pi / 4) * 1.41
def lp(x, fc):  # einfacher Tiefpass 1. Ordnung
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); s = 0.
    for i in range(len(x)): s = (1 - a) * x[i] + a * s; y[i] = s
    return y
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
# --- Instrumente: Rhodes-artiges E-Piano, digitaler Zupf (Dreieck), weiches Pad, Sub-Bass, Kick, Hi-Hat
def epiano(n, a, d=2.2, amp=.16, pan=0):
    t = tt(d); f = hz(n); x = np.sin(2 * np.pi * f * t + 1.2 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t * 3)) * np.exp(-t * 1.6)
    put(M, a, x * np.clip(t / .004, 0, 1) * amp, pan)
def pluck(n, a, amp=.06, pan=0, dec=9):
    t = tt(.6); f = hz(n); ph = (f * t) % 1; tri = 2 * np.abs(2 * ph - 1) - 1; x = tri * np.exp(-t * dec)
    put(M, a, x * np.clip(t / .002, 0, 1) * amp, pan)
def pad(ns, a, b, amp=.025, bright=0):
    t = tt(b - a); e = np.clip(t / 1.0, 0, 1) * np.clip((b - a - t) / .8, 0, 1)
    for i, n in enumerate(ns): f = hz(n); put(M, a, (np.sin(2 * np.pi * f * t) + np.sin(2 * np.pi * f * 1.004 * t + 1) + bright * .3 * np.sin(4 * np.pi * f * t)) * .5 * e * amp, -.6 + 1.2 * i / max(1, len(ns) - 1))
def sub(n, a, d, amp=.16):
    t = tt(d); f = hz(n); put(M, a, np.sin(2 * np.pi * f * t) * np.clip(t / .01, 0, 1) * np.clip((d - t) / .05, 0, 1) * amp)
def kick(a, amp=.3):
    t = tt(.35); ph = 2 * np.pi * np.cumsum(48 + 110 * np.exp(-t * 35)) / SR; put(M, a, np.sin(ph) * np.exp(-t * 10) * amp)
def hat(a, amp=.025, pan=.3):
    t = tt(.08); put(M, a, nz(.08, 8000, 1) * np.exp(-t * 60) * amp, pan)
B = .5  # 120 BPM
# 1) Problem 0 – oft: d-Moll, gedämpfter Puls + Uhr
pad([50, 57, 62, 65], .1, K['oft'] + .2, .02)
for a in np.arange(.3, K['oft'] - .1, B * 2): kick(a, .14)
for a, ns in [(K['server'], [38, 45]), (K['aus'], [37, 44]), (K['mails'], [50]), (K['rechnungen'], [48]), (K['n20'], [46, 53]), (K['kunden'], [45, 52]), (K['weg'], [38, 44, 50])]:
    for n in ns: epiano(n, a, 2.4, .14)
for a in np.arange(K['n20'], K['oft'], B): epiano(74 if int(a / B) % 2 else 69, a, .5, .03, .4)
# 2) Wendung: Stille, ein Sinuston
t = tt(2.2); put(M, K['oft'], np.sin(2 * np.pi * hz(81) * t) * np.exp(-t * 1.5) * .05)
epiano(62, K['wochen'], 2.5, .09); epiano(69, K['wochen'] + .25, 2.2, .07)
# 3) Lösung ab nnit: F – C – d – B, Zupf-Sechzehntel (Datenpakete)
prog = [[41, 65, 69, 72], [36, 64, 67, 72], [38, 62, 65, 69], [34, 62, 65, 70]]
a = K['nnit'] - .05; i = 0
while a < K['notfall'] - .1:
    c = prog[(i // 4) % 4]
    if i % 4 == 0: pad(c[1:], a, a + B * 4 + .3, .018, 1); sub(c[0], a, B * 3.8, .13)
    if i % 2 == 0: kick(a, .2)
    hat(a + B / 2, .02)
    for j, n in enumerate([c[1] + 12, c[2] + 12, c[3] + 12, c[2] + 12]): pluck(n, a + j * B / 4, .04, -.4 + .25 * j)
    i += 1; a += B
# 4) Notfall: Bruch, dann Aufbau zur Stunde
for n in [38, 44]: epiano(n, K['notfall'], 1.6, .12)
a = K['notfall'] + .4; i = 0
while a < K['wieder'] - .05:
    pluck(62 + (i % 4) * 2, a, .035 + i * .002, .2 * ((i % 2) * 2 - 1)); i += 1; a += B / 2
for n in [41, 53, 60, 65, 69, 72, 77]: epiano(n, K['wieder'], 2.6, .1)
# 5) Büro läuft: leichter Groove bis Schluss
prog2 = [[41, 65, 69, 72], [43, 67, 70, 74], [36, 64, 67, 72], [41, 65, 69, 72]]
a = K['montag2'] - .1; i = 0
while a < K['kostenlos'] + .4:
    c = prog2[(i // 4) % 4]
    if i % 2 == 0: kick(a, .24)
    hat(a + B / 2, .025)
    if i % 4 == 0: pad(c[1:], a, a + B * 4 + .3, .02, 1); sub(c[0], a, B * 3.8, .14)
    pluck(c[1 + i % 3] + 12, a, .045, -.3 + .3 * (i % 3)); pluck(c[1 + (i + 1) % 3] + 12, a + B / 2, .035, .3)
    i += 1; a += B
for n in [41, 53, 57, 60, 65, 69, 72]: epiano(n, K['kostenlos'] + .5, 3.0, .1)
M = reverb(M, 1.8, .22)

# --- Effekte ---
def click(a, amp=.05, pan=0, fc=3500):
    t = tt(.03); put(S, a, nz(.03, fc, 3) * np.exp(-t * 200) * amp, pan)
# V6: kein Tippen mehr am Anfang (es wird nichts getippt). Stattdessen: Uhr springt auf 8:00 und klingelt kurz
for i, n in enumerate([88, 84]): t = tt(.7); put(S, .25 + i * .12, np.sin(2 * np.pi * hz(n) * t) * np.exp(-t * 7) * .05, -.4)
# Tastatur nur im arbeitenden Büro am Ende
for a in np.arange(K['montag2'] + .1, K['team'], .1): click(a + R.random() * .04, .04, .2, 3000 + R.random() * 1500)
# Uhr tickt (Problem)
for a in np.arange(.2, K['oft'] - .1, 1.0): click(a, .05, .4, 2200); click(a + .5, .035, .4, 1800)
# Lüfter fährt herunter + Fehlerton
t = tt(1.1); f = 900 * np.exp(-t * 2.4) + 60; put(S, K['server'] - .05, (np.sin(2 * np.pi * np.cumsum(f) / SR) * .4 + nz(1.1, 700, 1) * .6) * np.exp(-t * 2.2) * .12, .3)
t = tt(.5); put(S, K['aus'] + .38, .6 * np.sign(np.sin(2 * np.pi * 330 * t)) * .25 * np.exp(-t * 6) * (t < .22) + np.sign(np.sin(2 * np.pi * 247 * t)) * .25 * np.exp(-(t - .25) * 6) * (t > .25), .1)
# Mail/Rechnung scheitern: kurzes tiefes Doppel-Brummen
for k in ['mails', 'rechnungen']:  # V6: Aufprall am Server (K-0,38), dann Landen am Boden
    t = tt(.3); put(S, K[k] - .38, (np.sin(2 * np.pi * 150 * t) + np.sin(2 * np.pi * 159 * t)) * np.exp(-t * 12) * .1, .3)
    t = tt(.08); put(S, K[k] - .1, nz(.08, 900, 2) * np.exp(-t * 50) * .06, .1)
# 20 Warte-Kringel ploppen auf
for i in range(20): t = tt(.06); put(S, K['n20'] - .1 + i * .035, np.sin(2 * np.pi * (700 + i * 30) * t) * np.exp(-t * 60) * .04, -.7 + i * .07)
# Server-Klappe, Ordner rutschen, zerfallen
t = tt(.35); put(S, K['sicherung'] - .05, (nz(.35, 500, 2) * .6 + np.sin(2 * np.pi * 90 * t) * .4) * np.exp(-t * 10) * .12, .4)
for i in range(4): t = tt(.25); put(S, K['kunden'] - .1 + i * .12, nz(.25, 2500, 1.2) * np.sin(np.pi * t / .25) * .05, .3)
for i in range(18): t = tt(.05); put(S, K['weg'] + .1 + i * .04 + R.random() * .02, nz(.05, 1200 + R.random() * 2000, 4) * np.exp(-t * 70) * .07, .2 + R.random() * .4)
# Blaupause: Warn-Pings, Linie zeichnet
# V7: Warnzeichen erscheinen um „zeigt“, Ausfall-Kreuz, Lupe kommt an W2 an (Aufleuchten)
for dt in [-.05, .2, .32]:
    t = tt(.5); put(S, K['zeigt'] + dt, np.sign(np.sin(2 * np.pi * 1320 * t)) * np.exp(-t * 14) * .04, .3)
t = tt(.4); put(S, K['zeigt'] + .15, (np.sin(2 * np.pi * 220 * t) + np.sin(2 * np.pi * 233 * t)) * np.exp(-t * 8) * .09)
t = tt(.6); put(S, K['wochen'] - .08, np.sin(2 * np.pi * hz(93) * t) * np.exp(-t * 6) * .05, -.2)
# Datenpulse im Netz
for i in range(26): t = tt(.07); put(S, K['nnit'] + .5 + i * .09, np.sin(2 * np.pi * hz(88 + (i % 5) * 2) * t) * np.exp(-t * 50) * .025, -.8 + (i % 9) * .2)
for i in range(20): t = tt(.1); put(S, K['technik'] - .1 + i * .025, np.sin(2 * np.pi * hz(91 + (i % 3) * 4) * t) * np.exp(-t * 35) * .02, -.6 + i * .06)
t = tt(.9); put(S, K['uhr'] - .2, np.sin(2 * np.pi * np.cumsum(500 + 500 * t / .9) / SR) * np.sin(np.pi * t / .9) * .03)
# Laufwerk: raus (Schlitten), rein (Klack), Anlauf
t = tt(.5); put(S, K['tauschen'] - .05, (nz(.5, 1800, 6) * (0.5 + .5 * np.sign(np.sin(2 * np.pi * 28 * t)))) * np.sin(np.pi * t / .5) * .07, .4)
t = tt(.12); put(S, K['bevor'] + .1, (np.sin(2 * np.pi * 180 * t) * .5 + nz(.12, 3000, 2) * .5) * np.exp(-t * 45) * .2, .3)
t = tt(1.0); put(S, K['bevor'] + .2, np.sin(2 * np.pi * np.cumsum(80 + 300 * (1 - np.exp(-t * 3))) / SR) * np.clip(t / .2, 0, 1) * np.exp(-t * 1.5) * .04, .3)
# V6: alte Festplatte am Boden fällt aus (kleines Knistern + Puff)
t = tt(.35); put(S, K['ausfallen'] - .15, nz(.35, 700, 1.5) * np.exp(-t * 9) * .05, -.4)
# Nacht: Schloss-Klicks je Paket
for i in range(7):
    s0 = K['nacht'] + .2 + i * .38; a = max(s0 + .25, K['verschl']) + .3
    t = tt(.05); put(S, a, nz(.05, 4200, 5) * np.exp(-t * 90) * .06, -.2 + i * .08); put(S, a + .05, nz(.05, 2600, 5) * np.exp(-t * 90) * .05, -.2 + i * .08)
# Notfall: Alarm, Stoppuhr, Erfolg
for d in [0, .22]: t = tt(.18); put(S, K['notfall'] + d, np.sign(np.sin(2 * np.pi * 880 * t)) * np.exp(-t * 10) * .05)
for a in np.arange(K['notfall'] + .4, K['wieder'], .25): click(a, .035, -.3, 5000)
for i, n in enumerate([84, 88, 91, 96]): t = tt(.5); put(S, K['wieder'] + i * .07, np.sin(2 * np.pi * hz(n) * t) * np.exp(-t * 8) * .05, -.3 + i * .2)
# Büro gut: Mails fliegen (Papier-Flappen)
for i in range(10): t = tt(.12); put(S, K['montag2'] + .2 + i * .22, nz(.12, 2200, 1.5) * np.sin(np.pi * t / .12) * .035, -.6 + (i % 5) * .3)
# Schluss: Karte steigt, Stempel-Häkchen
t = tt(.3); put(S, K['ende'], (np.sin(2 * np.pi * 70 * t) * np.exp(-t * 12)) * .15)
t = tt(.4); put(S, K['check'], np.sin(2 * np.pi * 1318 * t) * np.exp(-t * 9) * .05); put(S, K['kostenlos'] + .05, np.sin(2 * np.pi * 1760 * t) * np.exp(-t * 9) * .05)
S = reverb(S, .9, .12)
for name, buf, pk in [('musik', M, .6), ('sfx', S, .8)]:
    sf.write(f'out/{name}.wav', (buf / (np.abs(buf).max() + 1e-9) * pk).astype(np.float32), SR)
print('ok')

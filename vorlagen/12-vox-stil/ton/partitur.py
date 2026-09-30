#!/usr/bin/env python3
"""Recht am Steuer V4 – eigene Musik + Effekte. Dramaturgie folgt dem Kunden:
Problem (a-Moll, sparsam, Puls) -> Wendung bei „Aber“ (Stille, ein Ton) -> Prüfung (C-Dur, Zupf-Ostinato)
-> „eingestellt“ (Aufhellung) -> „Sie fahren weiter“ (voller, leichter Groove) -> Schlussakkord.
Effekte nur, wo im Bild etwas passiert: Umschlag, Kamerablitz, Stempel, Straßenbruch, Lupe, Prüfbalken, Häkchen, Auto."""
import numpy as np, soundfile as sf, os
SR = 48000; import json as _j; _Z = _j.load(open('out/zeiten.json')); DUR = _Z['DUR']; N = int(DUR * SR); R = np.random.default_rng(4)
K = _Z['K']
M = np.zeros((N, 2)); S = np.zeros((N, 2))
def tt(d): return np.arange(int(d * SR)) / SR
def put(buf, a, x, pan=0.):
    i = int(a * SR); n = min(len(x), N - i)
    if n > 0: buf[i:i + n, 0] += x[:n] * np.cos((pan + 1) * np.pi / 4) * 1.41; buf[i:i + n, 1] += x[:n] * np.sin((pan + 1) * np.pi / 4) * 1.41
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
# --- Instrumente ---
def piano(n, a, d=2.5, amp=.2, pan=0):
    t = tt(d); f = hz(n); x = sum(np.sin(2 * np.pi * f * k * t * (1 + .0004 * k * k)) * np.exp(-t * (1.1 + k * .8)) / k ** 1.4 for k in range(1, 8))
    put(M, a, x * np.clip(t / .003, 0, 1) * amp, pan)
def pluck(n, a, amp=.07, pan=0):
    t = tt(.9); f = hz(n); x = (np.sin(2 * np.pi * f * t) + .5 * np.sin(4 * np.pi * f * t) * np.exp(-t * 14)) * np.exp(-t * 6.5)
    put(M, a, x * np.clip(t / .002, 0, 1) * amp, pan)
def pad(ns, a, b, amp=.03):
    t = tt(b - a); e = np.clip(t / 1.2, 0, 1) * np.clip((b - a - t) / 1.0, 0, 1)
    for i, n in enumerate(ns): f = hz(n); put(M, a, (np.sin(2 * np.pi * f * t) + np.sin(2 * np.pi * f * 1.003 * t + 1)) * .5 * e * amp, -.5 + i / max(1, len(ns) - 1))
def kick(a, amp=.35):
    t = tt(.4); ph = 2 * np.pi * np.cumsum(45 + 90 * np.exp(-t * 30)) / SR; put(M, a, np.sin(ph) * np.exp(-t * 9) * amp)
def clap(a, amp=.05):
    t = tt(.25); put(M, a, nz(.25, 1500, 1) * np.exp(-t * 22) * amp, .1)
def bass(n, a, d, amp=.16):
    t = tt(d); f = hz(n); x = np.sin(2 * np.pi * f * t) + .25 * np.sin(4 * np.pi * f * t); put(M, a, x * np.clip(t / .01, 0, 1) * np.clip((d - t) / .05, 0, 1) * np.exp(-t * .8) * amp)
BEAT = .6
# 1) Problem 0–8.3: a-Moll, Herzschlag-Puls, tiefe Pianotöne
pad([57, 60, 64], .2, 8.6, .022)
for a in np.arange(.4, 8.2, BEAT * 2): kick(a, .16); kick(a + .22, .09)
for a, ns in [(K['geblitzt'], [45, 52]), (K['n71'], [57]), (K['n50'], [55]), (K['fahrverbot'], [41, 48, 53]), (K['keinauto'], [40, 47])]:
    for n in ns: piano(n, a, 2.6, .18)
# 2) Karte 8.3–13.3: a – F – d – E, Puls 100 BPM
chords = [[45, 57, 60, 64], [41, 57, 60, 65], [38, 57, 62, 65], [40, 56, 59, 64]]
t0 = K['dasheisst']
for i in range(8):
    a = t0 + i * BEAT * 1.0
    if a > K['aber'] - .3: break
    kick(a, .28); c = chords[(i // 2) % 4]; bass(c[0], a, BEAT * .95)
    if i % 2 == 0: pad(c[1:], a, a + BEAT * 2 + .2, .018)
for k in ['arbeit', 'kunden', 'kita']:
    for n, d in [(69, 0), (64, .12), (57, .24)]: piano(n, K[k] + d, 1.8, .09, .2)
# 3) Wendung „Aber“: Stille, ein heller Ton
piano(76, K['aber'], 3.2, .12); piano(64, K['aber'], 3.2, .09)
# 4) Prüfung 15.76–22.3: C – G – a – F, Zupf-Ostinato in Achteln
prog = [[48, 60, 64, 67], [43, 59, 62, 67], [45, 60, 64, 69], [41, 60, 65, 69]]
a = K['recht'] - .05; i = 0
while a < K['eingestellt'] - .05:
    c = prog[(i // 4) % 4]
    if i % 4 == 0: pad(c[1:], a, a + BEAT * 4 + .3, .016); bass(c[0], a, BEAT * 1.9, .12)
    for j, n in enumerate([c[1] + 12, c[2] + 12, c[3] + 12, c[2] + 12]): pluck(n, a + j * BEAT / 4, .045, -.3 + .2 * j)  # Sechzehntel
    i += 1; a += BEAT
# 5) eingestellt + Sie fahren weiter: Aufhellung, leichter Groove bis 29.6
for n in [48, 60, 64, 67, 72, 74]: piano(n, K['eingestellt'], 3.0, .1)
a = K['fahren'] - .3; i = 0; prog2 = [[48, 64, 67, 72], [43, 62, 67, 71], [41, 65, 69, 72], [48, 64, 67, 72]]
while a < K['kostenlos'] + .7:
    c = prog2[(i // 4) % 4]
    if i % 2 == 0: kick(a, .26)
    if i % 2 == 1: clap(a, .06)
    if i % 4 == 0: pad(c[1:], a, a + BEAT * 4 + .3, .02); bass(c[0], a, BEAT * 1.9, .14)
    pluck(c[1 + i % 3] + 12, a, .05, -.3 + .3 * (i % 3)); pluck(c[1 + (i + 1) % 3] + 12, a + BEAT / 2, .04, .3)
    i += 1; a += BEAT
for n in [48, 55, 60, 64, 67, 72]: piano(n, K['kostenlos'] + .9, 3.0, .12)
M = reverb(M, 2.2, .28)

# --- Effekte ---
t = tt(.5); put(S, .15, nz(.5, 2800, 1) * np.exp(-t * 7) * np.sin(np.pi * np.clip(t / .5, 0, 1)) * .06, -.2)          # Umschlag gleitet
t = tt(.3); put(S, .66, (np.sin(2 * np.pi * 90 * t) * .6 + nz(.3, 700, 1) * .4) * np.exp(-t * 18) * .25)                 # Aufsetzen
t = tt(.35); put(S, K['geblitzt'] - .35, np.sin(2 * np.pi * np.cumsum(1800 + 4200 * (t / .35) ** 2) / SR) * (t / .35) ** 2 * .05)  # Blitz lädt
t = tt(.5); put(S, K['geblitzt'], (nz(.5, 5000, .8) * np.exp(-t * 16) + np.sin(2 * np.pi * 180 * t) * np.exp(-t * 30)) * .3)       # Auslöser
t = tt(.45); put(S, K['geblitzt'] + .08, nz(.45, 3500, 1.5) * np.exp(-t * 6) * np.sin(np.pi * t / .45) * .08, .3)            # Brief raus
def thud(a, amp=.3):
    t = tt(.5); put(S, a, (np.sin(2 * np.pi * (60 + 50 * np.exp(-t * 25)) * t) * np.exp(-t * 8) + nz(.5, 1200, 2) * np.exp(-t * 50) * .2) * amp)
for k in ['n71', 'n50', 'keinauto']: thud(K[k], .22)
t = tt(.25); put(S, K['fahrverbot'] - .6, nz(.25, 1800, 1) * np.sin(np.pi * t / .25) * .05, .5)                              # Karte gleitet
def stampfx(a, amp):
    t = tt(.7); put(S, a, (np.sin(2 * np.pi * (70 + 60 * np.exp(-t * 30)) * t) * np.exp(-t * 7) + nz(.7, 900, 3) * np.exp(-t * 35) * .5) * amp)
stampfx(K['fahrverbot'] - .02, .45); stampfx(K['eingestellt'] - .02, .5)  # V7: Stempel sitzt auf dem Wort
# Straßenbruch: kurzes Knacken
for k in ['arbeit', 'kunden_w', 'kita_w']:  # V7: Bruch fertig auf dem Nomen
    t = tt(.3); put(S, K[k] - .06, nz(.3, 2400, 5) * np.exp(-t * 25) * .12 + np.sin(2 * np.pi * 110 * t) * np.exp(-t * 20) * .15, .1)
# Kamera fährt raus / rein: tonales Anschwellen (kein Whoosh)
for a, up in [(K['dasheisst'] - .3, 1), (K['aber'] - .45, 0), (K['fahren'] - .5, 1)]:
    t = tt(.6); f = 110 * (1 + (t / .6) * (1 if up else -.3)); put(S, a, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / .6) * .06)
# Lupe: zwei Sonar-Pings, Markerstrich
for d in [0, .35]:
    t = tt(1.2); put(S, K['fehler'] - .2 + d, np.sin(2 * np.pi * 1760 * t) * np.exp(-t * 5) * .05, .3)
t = tt(.45); put(S, K['fehler'] + .02, nz(.45, 3300, 5) * (0.5 + .5 * np.sin(2 * np.pi * 10 * t)) * np.sin(np.pi * t / .45) * .07)
# Prüfbalken: weiches Summen, Häkchen-Töne
t = tt(1.6); put(S, K['prueft'] - .2, np.sin(2 * np.pi * 220 * t) * np.sin(np.pi * t / 1.6) * .03 + nz(1.6, 900, 4) * np.sin(np.pi * t / 1.6) * .02)
for i in range(6):
    a = K['prueft'] - .05 + i * .2; t = tt(.2)  # V7: wie die Häkchen im Film
    if i == 4: put(S, a, (np.sin(2 * np.pi * 220 * t) + np.sin(2 * np.pi * 233 * t)) * np.exp(-t * 14) * .08)             # Fehler-Brummen
    else: put(S, a, np.sin(2 * np.pi * hz(84 + [0, 2, 4, 7, 0, 9][i]) * t) * np.exp(-t * 22) * .05, -.2 + i * .08)
# Belege fächern auf + Auswahl
for i, k in enumerate(['mess', 'eich', 'foto']):
    t = tt(.2); put(S, K['mess'] - .3 + i * .12, nz(.2, 3000, 1.2) * np.exp(-t * 20) * .06, -.5 + i * .5)
    t = tt(.3); put(S, K[k], (np.sin(2 * np.pi * (330 if k == 'eich' else 880) * t) * np.exp(-t * 14)) * .07, -.5 + i * .5)
# Straßen wieder heil: Arpeggio; Auto fährt
for i, n in enumerate([72, 76, 79]): pluck(n, K['fahren'] - .05 + i * .12, .08, -.4 + i * .4)
t = tt(2.2); f = 70 + 25 * np.sin(np.pi * t / 2.2); put(S, K['fahren'] + .5, (np.sin(2 * np.pi * np.cumsum(f) / SR) * .5 + nz(2.2, 300, 1) * .5) * np.sin(np.pi * t / 2.2) * .07)
# Schild steigt, Zusatzschild, Schluss
thud(K['schicken'] + .1, .2)
t = tt(.3); put(S, K['erst'], np.sin(2 * np.pi * 1318 * t) * np.exp(-t * 12) * .05)
S = reverb(S, 1.2, .15)
os.makedirs('out', exist_ok=True)
for name, buf, pk in [('musik', M, .6), ('sfx', S, .8)]:
    sf.write(f'out/{name}.wav', (buf / (np.abs(buf).max() + 1e-9) * pk).astype(np.float32), SR)
print('ok')

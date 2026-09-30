#!/usr/bin/env python3
"""Wärmewerk V4 – eigene Musik + Effekte. Kalt gegen warm:
Problem (e-Moll, gläserne kalte Flächen, Kessel brummt) -> Kessel aus (Stille, Frost-Klirren) -> Wendung „Dabei“ (erster warmer Akkord)
-> Lösung (G-Dur, warmes E-Piano, weicher Puls, Wärmepumpe summt) -> „warm“ (voller Akkord) -> Marke (ruhiger Schluss).
Effekte aus dem Material des Themas: Schreibmaschine (Etiketten tippen), Papierbogen, Gasflamme, Verpuffen, Frost, Lüfter, Wasser in der Leitung, Stempel."""
import numpy as np, soundfile as sf, os, json
SR = 48000; Z = json.load(open('out/zeiten.json')); K = Z['K']; DUR = Z['DUR']; N = int(DUR * SR); R = np.random.default_rng(16)
M = np.zeros((N, 2)); S = np.zeros((N, 2))
def tt(d): return np.arange(int(round(d * SR))) / SR
def put(buf, a, x, pan=0.):
    i = int(a * SR)
    if i < 0: x = x[-i:]; i = 0
    n = min(len(x), N - i)
    if n > 0: buf[i:i + n, 0] += x[:n] * np.cos((pan + 1) * np.pi / 4) * 1.41; buf[i:i + n, 1] += x[:n] * np.sin((pan + 1) * np.pi / 4) * 1.41
def bp(x, fc, q):
    F = np.fft.rfftfreq(len(x), 1 / SR); Hh = 1 / (1 + 1j * q * (F / fc - fc / np.maximum(F, 1)))
    y = np.fft.irfft(np.fft.rfft(x) * Hh, len(x)); return y / (np.abs(y).max() + 1e-9)
def nz(d, fc, q=2): return bp(R.standard_normal(max(16, int(round(d * SR)))), fc, q)
def reverb(x, sec, mix):
    n = int(sec * SR); ir = R.standard_normal((n, 2)) * np.exp(-np.arange(n) / SR * 6 / sec)[:, None]; F = 1 << int(np.ceil(np.log2(len(x) + n))); out = np.zeros_like(x)
    for c in range(2): out[:, c] = np.fft.irfft(np.fft.rfft(x[:, c], F) * np.fft.rfft(ir[:, c], F), F)[:len(x)]
    out *= np.abs(x).max() / (np.abs(out).max() + 1e-9); return x * (1 - mix) + out * mix
def hz(n): return 440 * 2 ** ((n - 69) / 12)
def glass(ns, a, b, amp=.02):  # kalte gläserne Fläche
    t = tt(b - a); e = np.clip(t / 1.2, 0, 1) * np.clip((b - a - t) / .8, 0, 1)
    for i, n in enumerate(ns): f = hz(n); put(M, a, (np.sin(2 * np.pi * f * t) + .3 * np.sin(2 * np.pi * f * 3 * t) * (.5 + .5 * np.sin(2 * np.pi * .3 * t))) * e * amp, -.6 + 1.2 * i / max(1, len(ns) - 1))
def epiano(n, a, d=2.2, amp=.08, pan=0):  # warmes E-Piano
    t = tt(d); f = hz(n); x = (np.sin(2 * np.pi * f * t + 1.2 * np.sin(2 * np.pi * f * t) * np.exp(-t * 3)) * np.exp(-t * 1.4) + .2 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t * 4)) * (1 + .1 * np.sin(2 * np.pi * 4.5 * t))
    put(M, a, x * np.clip(t / .004, 0, 1) * amp, pan)
def celesta(n, a, amp=.04, pan=0): t = tt(1.5); f = hz(n); put(M, a, (np.sin(2 * np.pi * f * t) * np.exp(-t * 3) + .3 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t * 9)) * amp, pan)
def warmpad(ns, a, b, amp=.02):
    t = tt(b - a); e = np.clip(t / .9, 0, 1) * np.clip((b - a - t) / .7, 0, 1)
    for i, n in enumerate(ns): f = hz(n); x = sum(np.sin(2 * np.pi * f * k * t * (1 + .002 * (j - 1))) / k ** 1.5 for k in range(1, 5) for j in range(3)) / 3; put(M, a, x * e * amp, -.5 + i / max(1, len(ns) - 1))
def bass(n, a, d, amp=.13): t = tt(d); f = hz(n); put(M, a, np.sin(2 * np.pi * f * t) * np.clip(t / .01, 0, 1) * np.clip((d - t) / .05, 0, 1) * np.exp(-t * 1.5) * amp)
def kick(a, amp=.2): t = tt(.3); ph = 2 * np.pi * np.cumsum(50 + 70 * np.exp(-t * 30)) / SR; put(M, a, np.sin(ph) * np.exp(-t * 11) * amp)
def shaker(a, amp=.015): t = tt(.07); put(M, a, nz(.07, 6500, 1.5) * np.exp(-t * 60) * amp, .3)
B = 60 / 96
# 1) Problem: kalt, e-Moll
glass([64, 67, 71], .1, K['dabei'] + .2, .016)
for a, ns in [(K['betrag'], [40, 52, 55]), (K['alt25'], [43, 55]), (K['januar'], [45, 52]), (K['kalt'], [40, 47, 59])]:
    for n in ns: epiano(n, a, 2.4, .07)
a = K['kessel'] - .2
while a < K['aus']: bass(28, a, B * 1.8, .08); a += B * 2
for i, n in enumerate([83, 88, 86, 91]): celesta(n, K['kalt'] + .1 + i * .18, .035, -.5 + .3 * i)  # Frost
# 2) Wendung: erster warmer Akkord
warmpad([55, 59, 62, 67], K['dabei'] - .05, K['werk'] + .3, .02)
for i, n in enumerate([67, 71, 74]): epiano(n, K['waerme'] + i * .12, 2.5, .07, -.3 + .3 * i)
# 3) Lösung: G – D – e – C, weicher Puls
prog = [[43, 59, 62, 67], [38, 57, 62, 66], [40, 59, 64, 67], [36, 60, 64, 67]]
a = K['werk'] - .05; i = 0
while a < K['kostenlos'] + 1.2 and a < DUR - 1:
    c = prog[(i // 4) % 4]
    if i % 2 == 0: kick(a, .17)
    shaker(a + B / 2, .016)
    if i % 4 == 0: warmpad(c[1:], a, a + B * 4 + .2, .016); bass(c[0], a, B * 1.9, .12)
    epiano(c[1 + i % 3] + 12, a, 1.2, .045, -.3 + .3 * (i % 3))
    i += 1; a += B
for n in [43, 55, 62, 67, 71, 74]: epiano(n, K['warm'], 3.0, .07)
for n in [43, 55, 59, 62, 67, 71]: epiano(n, K['kostenlos'] + .9, 3.0, .08)
M = reverb(M, 2.0, .25)
# --- Effekte ---
def key(a, amp=.06, pan=-.2):  # Schreibmaschinen-Anschlag
    t = tt(.05); put(S, a, (nz(.05, 2800, 3) * np.exp(-t * 120) + np.sin(2 * np.pi * 900 * t) * np.exp(-t * 160) * .4) * amp, pan)
def slap(a, amp=.1): t = tt(.12); put(S, a, nz(.12, 1500, 1) * np.exp(-t * 45) * amp, .1)
def typed(a, n, cps=30, amp=.045, pan=-.2):
    slap(a, .09)
    for i in range(n): key(a + .12 + i / cps + R.random() * .008, amp * (.7 + .6 * R.random()), pan)
# V7: nichts wird getippt – jedes Etikett klatscht als Ganzes auf (ein Papier-Klatsch), rote Hand-Ellipsen/Schnitte = Stiftstrich
def pen(a, d=.3, amp=.03):
    t = tt(d); put(S, a, nz(d, 4200, 3) * (.5 + .5 * np.sin(2 * np.pi * 14 * t)) ** 2 * np.sin(np.pi * t / d) * amp, .15)
for a in [K['betrag'] - .25, K['jahr'] - .25, K['kessel'] - .25, K['alt25'] - .25, K['minus'] - .25, K['werk'] - .25, K['drei'] - .25,
          K['heizkosten'] - .3, K['drittel'] - .25, K['marke'] - .25, K['haustechnik'] + .45, K['beratung'] - .25, K['kostenlos'] - .25]:
    slap(a, .1)
for a in [K['euro'] - .3, K['aus'] - .3, K['waerme'] - .3, K['kostenlos'] - .28, K['sinken'] - .25]: pen(a)
t = tt(.5); put(S, K['gas'] - .35, nz(.5, 2200, .8) * np.sin(np.pi * t / .5) ** 2 * .06, 0)  # Rechnung schiebt sich hoch
t = tt(.6); put(S, K['sinken'] + .1, nz(.6, 500, 2) * np.sin(np.pi * t / .6) * .05, .4)  # Drittel kippt weg

# Zahl rollt: schnelles Rattern
# V5: kein Zahlenrattern mehr (Betrag wird getippt)
# Gasflamme: Zischen im Himmel und im Keller
t = tt(K['aus'] + .3); put(S, 0, nz(len(t) / SR, 3500, .7) * (.5 + .3 * np.sin(2 * np.pi * 7 * t)) * np.clip(t / .5, 0, 1) * np.clip((K['aus'] + .3 - t) / .3, 0, 1) * .025, -.3)
t = tt(K['aus'] - K['kessel'] + .2); put(S, K['kessel'], np.sin(2 * np.pi * 55 * t) * (.6 + .4 * np.sin(2 * np.pi * 1.3 * t)) * np.clip(t / .4, 0, 1) * np.clip((len(t) / SR - t) / .2, 0, 1) * .06)  # Kessel brummt
# Papierbogen schiebt sich über den Himmel / zurück
for a in [K['kessel'] - .55, K['marke'] - .72]: t = tt(.65); put(S, a, nz(.65, 2400, .8) * np.sin(np.pi * t / .65) ** 2 * .07, 0)
# Kessel aus: Verpuffen + metallisches Klacken, dann Frost
t = tt(.6); put(S, K['aus'] - .2, (nz(.6, 400, 1.5) * np.exp(-t * 7) + np.sin(2 * np.pi * 80 * t) * np.exp(-t * 12) * .5) * .2)
t = tt(.3); put(S, K['aus'] + .45, (np.sin(2 * np.pi * 1300 * t) + .6 * np.sin(2 * np.pi * 2140 * t)) * np.exp(-t * 18) * .05, .3)
t = tt(1.4); put(S, K['kalt'], nz(1.4, 7000, 6) * np.clip(t / .8, 0, 1) * np.exp(-np.maximum(t - .8, 0) * 5) * .04, .5)  # Frost knistert
# Luft aus Wörtern: leises Rauschen, dunkel → hell
t = tt(1.5); put(S, K['waerme'] - .3, nz(1.5, 900, .8) * np.sin(np.pi * t / 1.5) * .03, -.5)
# Wärmepumpe senkt sich, setzt auf, Lüfter summt
t = tt(1.4); put(S, K['werk'] - .7, np.sin(2 * np.pi * np.cumsum(180 - 60 * t / 1.4) / SR) * np.sin(np.pi * t / 1.4) * .03, -.4)
t = tt(.35); put(S, K['pumpe'] - .1, (np.sin(2 * np.pi * (70 + 40 * np.exp(-t * 30)) * t) * np.exp(-t * 12) + nz(.35, 800, 2) * np.exp(-t * 40) * .3) * .22, -.4)
a0 = K['danach'] - .3; t = tt(DUR - a0 - .8); put(S, a0, (np.sin(2 * np.pi * 110 * t) * .5 + nz(len(t) / SR, 600, 3) * .5) * np.clip(t / .6, 0, 1) * np.clip((len(t) / SR - t) / .5, 0, 1) * .025, -.4)
# alter Kessel hebt sich heraus, Speicher kommt
t = tt(.8); put(S, K['drei'] - .2, nz(.8, 300, 4) * (.5 + .5 * np.sin(2 * np.pi * 9 * t)) * np.sin(np.pi * t / .8) * .06, .2)
for i in range(3): t = tt(.2); put(S, K['drei'] - .04 + i * .25, np.sin(2 * np.pi * hz(79 + [0, 4, 7][i]) * t) * np.exp(-t * 16) * .05, .3)
t = tt(.3); put(S, K['tagen'] + .3, (np.sin(2 * np.pi * 95 * t) * np.exp(-t * 14)) * .12, .3)
# Leitung zeichnet sich (Stift), Förderantrag klatscht, Stempel
t = tt(max(.3, K['antrag'] - K['tagen'])); put(S, K['tagen'], nz(len(t) / SR, 4200, 3) * (.5 + .5 * np.sin(2 * np.pi * 10 * t)) ** 2 * .03, .2)
slap(K['antrag'] - .08, .18)
t = tt(.5); put(S, K['siebzig'] - .02, (np.sin(2 * np.pi * (65 + 60 * np.exp(-t * 30)) * t) * np.exp(-t * 8) + nz(.5, 900, 3) * np.exp(-t * 35) * .5) * .3)
# Wärme fließt: Wasser in der Leitung
t = tt(DUR - K['danach'] - 1.5); gur = nz(len(t) / SR, 700, 5) * (.5 + .5 * np.sin(2 * np.pi * (3 + np.sin(2 * np.pi * .4 * t)) * t)); put(S, K['danach'], gur * np.clip(t / .6, 0, 1) * np.clip((len(t) / SR - t) / .5, 0, 1) * .025, .2)
t = tt(.3); put(S, K['drittel'] - .05, np.sin(2 * np.pi * hz(84) * t) * np.exp(-t * 10) * .05)
S = reverb(S, .7, .1)
os.makedirs('out', exist_ok=True)
for name, buf, pk in [('musik', M, .6), ('sfx', S, .8)]:
    sf.write(f'out/{name}.wav', (buf / (np.abs(buf).max() + 1e-9) * pk).astype(np.float32), SR)
print('ok')

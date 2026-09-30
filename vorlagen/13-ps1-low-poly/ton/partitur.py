#!/usr/bin/env python3
"""Kistenheld V4 – eigene Musik + Effekte (numpy, 48 kHz Stereo, liest out/zeiten.json).
Instrumentierung wie ein PS1-Spiel: Rechteck/Dreieck-Synth, FM-Bass, Lo-Fi-Trommeln (8-Bit-Körnung).
Dramaturgie: Treppenhaus (e-Moll, schleppend) -> Absagen/Uhr (nervöses Arpeggio, schneller Puls) -> Montag (Leere, sinkende Töne)
-> Wendung: Licht an + „Power-up“-Arpeggio -> Kistenheld packt (G-Dur, treibender Chip-Groove) -> Pizza (warm, halbes Tempo) -> Jingle.
Effekte nur, wo im Bild etwas passiert: Sofa schrammt, Glühbirne flackert, Nachrichten, Stempel, Uhr, Kraftbalken, Lichtschalter,
Lkw, Ladetür, 100 Kartons ploppen (Tonhöhe steigt mit dem Zähler), Etiketten, Möbellift, Raumlichter, Herzen, Schilder."""
import numpy as np, soundfile as sf, os, json
SR = 48000; Z = json.load(open('out/zeiten.json')); K = Z['K']; DUR = Z['DUR']; N = int(DUR * SR); R = np.random.default_rng(13)
M = np.zeros((N, 2)); S = np.zeros((N, 2))
def tt(d): return np.arange(int(d * SR)) / SR
def put(buf, a, x, pan=0.):
    i = int(a * SR); n = min(len(x), N - i)
    if n > 0 and i >= 0: buf[i:i + n, 0] += x[:n] * np.cos((pan + 1) * np.pi / 4) * 1.41; buf[i:i + n, 1] += x[:n] * np.sin((pan + 1) * np.pi / 4) * 1.41
def reverb(x, sec, mix):
    n = int(sec * SR); ir = R.standard_normal((n, 2)) * np.exp(-np.arange(n) / SR * 6 / sec)[:, None]; F = 1 << int(np.ceil(np.log2(len(x) + n))); out = np.zeros_like(x)
    for c in range(2): out[:, c] = np.fft.irfft(np.fft.rfft(x[:, c], F) * np.fft.rfft(ir[:, c], F), F)[:len(x)]
    out *= np.abs(x).max() / (np.abs(out).max() + 1e-9); return x * (1 - mix) + out * mix
def hz(n): return 440 * 2 ** ((n - 69) / 12)
def crush(x, bits=6): q = 2 ** bits; return np.round(x * q) / q
def sq(n, a, d, amp=.05, pan=0, duty=.5, dec=3.):  # Rechteck
    t = tt(d); ph = (hz(n) * t) % 1; x = np.where(ph < duty, 1., -1.) * np.exp(-t * dec) * np.clip(t / .003, 0, 1) * np.clip((d - t) / .01, 0, 1); put(M, a, crush(x) * amp, pan)
def tri(n, a, d, amp=.08, pan=0):
    t = tt(d); ph = (hz(n) * t) % 1; x = (4 * np.abs(ph - .5) - 1) * np.clip(t / .003, 0, 1) * np.clip((d - t) / .02, 0, 1); put(M, a, crush(x, 5) * amp, pan)
def fmbass(n, a, d, amp=.12):
    t = tt(d); f = hz(n); x = np.sin(2 * np.pi * f * t + 2.2 * np.exp(-t * 6) * np.sin(2 * np.pi * f * 2 * t)) * np.exp(-t * 2.5) * np.clip((d - t) / .02, 0, 1); put(M, a, x * amp)
def kick(a, amp=.3): t = tt(.25); put(M, a, crush(np.sin(2 * np.pi * np.cumsum(50 + 140 * np.exp(-t * 35)) / SR) * np.exp(-t * 12), 5) * amp)
def snare(a, amp=.08): t = tt(.18); put(M, a, crush(R.standard_normal(len(t)) * np.exp(-t * 22), 4) * amp, .1)
def hat(a, amp=.025): t = tt(.04); put(M, a, crush(R.standard_normal(len(t)) * np.exp(-t * 90), 4) * amp, .3)
B = 60 / 100
# 1) Treppenhaus + Probleme: e-Moll, schleppend
for i, a in enumerate(np.arange(.1, K['mit'] - .2, B)):
    c = [40, 40, 36, 38][(i // 2) % 4]; fmbass(c, a, B * .9, .1)
    if i % 2 == 0: kick(a, .18)
    if a > K['nichts'] - .2: hat(a + B / 2, .02)
for k, ns in [('aufzug', [64, 67]), ('fest', [63, 66]), ('gepackt', [64, 71]), ('abgesagt', [62, 65]), ('zurueck', [63, 67])]:
    for j, n in enumerate(ns): sq(n, K[k] + j * .09, .35, .035, -.2 + j * .4, .25)
for i in range(10): sq(76 + (i % 2) * 3, K['wagen'] + .2 + i * .14, .1, .02, .4, .125)  # nervöses Arpeggio zur Uhr
for i, n in enumerate([71, 69, 67, 64, 62]): tri(n, K['montag'] + i * .35, .4, .06)   # Montag: sinkt
# 2) Wendung: Power-up
for i, n in enumerate([55, 59, 62, 67, 71, 74, 79, 83]): sq(n, K['mit'] + .05 + i * .045, .12, .045, -.5 + i * .14, .25, 8)
# 3) Kistenheld: G-Dur Chip-Groove bis zur Pizza
prog = [[43, 67, 71, 74], [40, 64, 67, 71], [36, 64, 67, 72], [38, 66, 69, 74]]
a = K['anders'] - .15; i = 0; B2 = 60 / 124
while a < K['pizza0'] - .1:
    c = prog[(i // 8) % 4]; fmbass(c[0] + (12 if i % 2 else 0), a, B2 * .45, .11)
    if i % 2 == 0: kick(a, .26)
    if i % 4 == 2: snare(a)
    hat(a + B2 / 4)
    sq(c[1 + (i % 3)] + 12, a, .12, .025, -.3 + .3 * (i % 3), .25, 10)
    if i % 4 == 0: tri(c[1] , a, B2 * 3.8, .045)
    i += 1; a += B2 / 2
# 4) Pizza: warm, halbes Tempo, Dreieck-Melodie
for j, (n, d) in enumerate([(71, .5), (74, .5), (79, 1.0), (78, .5), (74, .5), (76, 1.2)]):
    tri(n, K['pizza0'] + sum(x[1] for x in [(71, .5), (74, .5), (79, 1.0), (78, .5), (74, .5), (76, 1.2)][:j]) * .95, d * .95, .06)
for a in np.arange(K['pizza0'], K['schluss'], B): fmbass(43 if int((a - K['pizza0']) / B) % 2 == 0 else 38, a, B * .9, .07)
# 5) Jingle
for j, n in enumerate([67, 71, 74, 79]): sq(n, K['schluss'] + .05 + j * .12, .25, .04, 0, .5, 4)
a = K['schluss'] + .6; i = 0
while a < DUR - 1.2:
    c = prog[(i // 8) % 4]; fmbass(c[0], a, B2 * .45, .08)
    if i % 2 == 0: kick(a, .18)
    if i % 4 == 2: snare(a, .05)
    hat(a + B2 / 4, .015); i += 1; a += B2 / 2
for n in [55, 67, 71, 74, 79]: sq(n, K['besichtigung'] + .5, 1.2, .03, 0, .5, 1.5)
M = reverb(M, 1.2, .18)

# --- Effekte ---
def thud(a, amp=.2, f=70): t = tt(.3); put(S, a, crush(np.sin(2 * np.pi * (f + 60 * np.exp(-t * 30)) * t) * np.exp(-t * 14), 6) * amp)
def blip(a, f, d=.06, amp=.05, pan=0): t = tt(d); ph = (f * t) % 1; put(S, a, np.where(ph < .5, 1., -1.) * np.exp(-t * 30) * amp, pan)
for a in np.arange(.15, K['nichts'] - .3, .75):  # Sofa schrammt am Geländer
    t = tt(.35); put(S, a, crush(R.standard_normal(len(t)), 5) * np.sin(np.pi * t / .35) * .05, -.2); thud(a + .3, .12, 60)
for a in np.arange(.2, K['nichts'], .9): t = tt(.08); put(S, a + (a * 7 % .3), np.sin(2 * np.pi * 100 * t) * (np.sin(2 * np.pi * 50 * t) > 0) * .015, .5)  # Glühbirne
blip(K['aufzug'] - .1, 880, .08, .05); blip(K['aufzug'], 660, .08, .05)  # V7: Ring um das Aufzug-Schild
blip(K['nichts'] - .1, 880, .08, .04); blip(K['nichts'], 660, .08, .04)  # V7: Ring um die flachen Kartons
for k, tk in enumerate([K['freunde'] - .12, K['haben'] - .12, K['abgesagt'] - .12]): blip(tk, 1320, .05, .04, .5); blip(tk + .06, 880, .07, .04, .5)  # V7: je ein rotes ✕
thud(K['abgesagt'], .22, 55)  # Handy ruckt beim letzten ✕
for k in range(16): t = tt(.03); put(S, K['wagen'] + .2 + k * .08, crush(R.standard_normal(len(t)) * np.exp(-t * 120), 4) * .05, -.4)  # Uhr rast
for k in range(4): blip(K['montag'] + .3 + k * (K['job'] - K['montag'] - .3) / 3, 880 - k * 140, .09, .035, .4)  # V7: Batterie verliert Segmente
t = tt(.05); put(S, K['kistenheld'] - .25, crush(R.standard_normal(len(t)) * np.exp(-t * 80), 4) * .12)  # Lichtschalter
t = tt(1.4); put(S, K['mit'] - .27, crush(np.sin(2 * np.pi * np.cumsum(38 + 6 * np.sin(2 * np.pi * 9 * t)) / SR), 5) * np.clip(t / .2, 0, 1) * np.clip((1.4 - t) / .4, 0, 1) * .14)  # Lkw rollt an
t = tt(.5); put(S, K['kistenheld'] + .05, crush(R.standard_normal(len(t)), 4) * np.exp(-t * 6) * .05, .3)  # Druckluftbremse
thud(K['anders'] - .2, .15, 90)  # Ladetür
for k in range(100):  # 100 Kartons: Plopp, Tonhöhe steigt mit dem Zähler
    a = K['n100'] - .3 + (K['tag'] - K['n100'] + .3) * k / 100
    if k % 2 == 0: blip(a, 300 + k * 9, .04, .025, -.5 + (k % 10) / 10)
blip(K['tag'] - .05, 1175, .12, .045)  # V7: „1 TAG“
for k in range(4): blip(K['jeder'] - .2 + k * (K['beschriftet'] - .05 - K['jeder']) / 3 + .18, 1500 + k * 200, .05, .035, -.5 + k * .3)  # Etiketten
t = tt(2.0); put(S, K['lift'] - .5, crush(np.sin(2 * np.pi * 110 * t) + .3 * np.sin(2 * np.pi * 220 * t), 5) * np.clip(t / .2, 0, 1) * np.clip((2.0 - t) / .2, 0, 1) * .04)  # Liftmotor
thud(K['fenster'] + .35, .18, 80)
for k in range(4): t = tt(.04); tw = K['raum'] - .75 + k * .25; put(S, tw - .2, crush(R.standard_normal(len(t)) * np.exp(-t * 90), 4) * .08, -.5 + k * .33); blip(tw - .05, 990 + k * 110, .08, .035)  # Licht + Häkchen
for k in range(12): t = tt(.1); put(S, K['abends'] + .1 + k * .12, crush(R.standard_normal(len(t)), 4) * np.sin(np.pi * t / .1) * .02, .2)  # Kartons gleiten
for k in range(6): blip(K['wohnung'] - .3 + k * .45, 1200 + k * 100, .1, .025, -.3 + k * .12)  # Herzen
blip(K['angekommen'], 1568, .2, .05); blip(K['angekommen'] + .1, 2093, .3, .04)
for tk in [K['kostenlose'] - .1]: blip(tk, 1046, .08, .05); blip(tk + .07, 1568, .1, .05)  # V7: nur noch die Angebotstafel
S = reverb(S, .8, .12)
os.makedirs('out', exist_ok=True)
for name, buf, pk in [('musik', M, .6), ('sfx', S, .8)]: sf.write(f'out/{name}.wav', (buf / (np.abs(buf).max() + 1e-9) * pk).astype(np.float32), SR)
print('ok')

#!/usr/bin/env python3
"""Werkseite V4 – eigene Musik + Effekte. Brand-Motion-Prinzip „Logo + Jingle“: jedes Zeichen landet auf einem Jingle-Schlag.
Dramaturgie: Problem (a-Moll, trocken, Tipp-Geräusche, alter Modem-Ton) -> verlorener Auftrag (tiefer Absturz) ->
Wendung „Dabei“ (warme Marimba, Holz) -> Werkseite baut (C-Dur, Groove, Marimba-Ostinato) -> Holm-Jingle -> Telefon klingelt ->
Werkseite-Jingle + Schlussakkord. Effekte nur, wo im Bild etwas passiert."""
import numpy as np, soundfile as sf, os, json
SR = 48000; Z = json.load(open('out/zeiten.json')); K = Z['K']; DUR = Z['DUR']; N = int(DUR * SR); R = np.random.default_rng(15)
M = np.zeros((N, 2)); S = np.zeros((N, 2))
def tt(d): return np.arange(int(d * SR)) / SR
def put(buf, a, x, pan=0.):
    i = int(a * SR)
    if i < 0: x = x[-i:]; i = 0
    n = min(len(x), N - i)
    if n > 0: buf[i:i + n, 0] += x[:n] * np.cos((pan + 1) * np.pi / 4) * 1.41; buf[i:i + n, 1] += x[:n] * np.sin((pan + 1) * np.pi / 4) * 1.41
def bp(x, fc, q):  # einfacher Resonanzfilter (vektorisiert über FFT)
    F = np.fft.rfftfreq(len(x), 1 / SR); H = 1 / (1 + 1j * q * (F / fc - fc / np.maximum(F, 1)))
    y = np.fft.irfft(np.fft.rfft(x) * H, len(x)); return y / (np.abs(y).max() + 1e-9)
def nz(d, fc, q=2): return bp(R.standard_normal(max(16, int(d * SR))), fc, q)
def reverb(x, sec, mix):
    n = int(sec * SR); ir = R.standard_normal((n, 2)) * np.exp(-np.arange(n) / SR * 6 / sec)[:, None]; F = 1 << int(np.ceil(np.log2(len(x) + n))); out = np.zeros_like(x)
    for c in range(2): out[:, c] = np.fft.irfft(np.fft.rfft(x[:, c], F) * np.fft.rfft(ir[:, c], F), F)[:len(x)]
    out *= np.abs(x).max() / (np.abs(out).max() + 1e-9); return x * (1 - mix) + out * mix
def hz(n): return 440 * 2 ** ((n - 69) / 12)
# --- Instrumente ---
def marimba(n, a, amp=.12, pan=0, buf=None):
    t = tt(1.2); f = hz(n); x = np.sin(2 * np.pi * f * t) * np.exp(-t * 5) + .35 * np.sin(2 * np.pi * f * 3.98 * t) * np.exp(-t * 16) + .12 * np.sin(2 * np.pi * f * 9.2 * t) * np.exp(-t * 40)
    put(M if buf is None else buf, a, x * np.clip(t / .002, 0, 1) * amp, pan)
def bell(n, a, amp=.06, pan=0):
    t = tt(2.5); f = hz(n); x = np.sin(2 * np.pi * f * t) * np.exp(-t * 1.6) + .5 * np.sin(2 * np.pi * f * 2.0 * t) * np.exp(-t * 3) + .25 * np.sin(2 * np.pi * f * 3.01 * t) * np.exp(-t * 5)
    put(M, a, x * np.clip(t / .001, 0, 1) * amp, pan)
def pluck(n, a, amp=.05, pan=0):
    t = tt(.5); f = hz(n); x = (np.sin(2 * np.pi * f * t) + .4 * np.sign(np.sin(2 * np.pi * f * t)) * np.exp(-t * 30)) * np.exp(-t * 10)
    put(M, a, x * np.clip(t / .003, 0, 1) * amp, pan)
def pad(ns, a, b, amp=.02):
    t = tt(b - a); e = np.clip(t / .8, 0, 1) * np.clip((b - a - t) / .6, 0, 1)
    for i, n in enumerate(ns): f = hz(n); put(M, a, (np.sin(2 * np.pi * f * t) + .5 * np.sin(2 * np.pi * f * 2.003 * t)) * .5 * e * amp, -.5 + i / max(1, len(ns) - 1))
def bass(n, a, d, amp=.15):
    t = tt(d); f = hz(n); x = np.tanh(2 * np.sin(2 * np.pi * f * t)) * .7; put(M, a, x * np.clip(t / .008, 0, 1) * np.clip((d - t) / .04, 0, 1) * np.exp(-t * 2) * amp)
def kick(a, amp=.3):
    t = tt(.35); ph = 2 * np.pi * np.cumsum(48 + 110 * np.exp(-t * 32)) / SR; put(M, a, np.sin(ph) * np.exp(-t * 10) * amp)
def clap(a, amp=.06):
    t = tt(.22); x = sum(nz(.22, 1400, 1.2) * np.exp(-np.maximum(t - d, 0) * 30) * (t >= d) for d in (0, .01, .022)); put(M, a, x * amp / 3, .15)
def hat(a, amp=.02): t = tt(.06); put(M, a, nz(.06, 8000, 2) * np.exp(-t * 70) * amp, .35)
B = 60 / 110
# 1) Problem: a-Moll, trocken, sparsam
pad([57, 60, 64], .1, K['auftrag'], .016)
for a, n in [(K['tischler'], 69), (K['website'], 64), (K['winzige'], 60), (K['foto'], 59), (K['nummer'], 57)]: pluck(n, a, .06); pluck(n - 12, a, .05)
a = K['findet']
while a < K['auftrag'] - .4: kick(a, .12); a += B * 2
# 2) Auftrag weg: tiefer Absturz
for n in [45, 52, 57]: marimba(n, K['nebenan'], .1)
t = tt(1.4); put(M, K['nebenan'], np.sin(2 * np.pi * np.cumsum(55 * (1 - .4 * t / 1.4)) / SR) * np.exp(-t * 2) * .3)
bass(33, K['auftrag'], B * 2, .1); bass(31, K['auftrag'] + B * 2, B * 2, .1)
# 3) Wendung: warm, Holz
pad([53, 57, 60, 64], K['dabei'] - .1, K['werkseite'], .022)
for i, n in enumerate([65, 69, 72, 76]): marimba(n, K['dabei'] + i * B / 2, .08, -.3 + .2 * i)
marimba(72, K['besser'], .12); marimba(79, K['besser'] + .12, .08)
# 4) Werkseite baut: C-Dur-Groove
prog = [[48, 64, 67, 72], [43, 62, 67, 71], [45, 64, 69, 72], [41, 65, 69, 72]]
a = K['werkseite'] - .02; i = 0
while a < K['marke'] + 3.5:
    c = prog[(i // 4) % 4]; late = a > K['logo'] - .1
    if i % 2 == 0: kick(a, .26 if late else .2)
    if i % 2 == 1 and late: clap(a, .07)
    hat(a + B / 2, .025 if late else .015)
    if i % 4 == 0: pad(c[1:], a, a + B * 4 + .2, .014); bass(c[0], a, B * 1.8, .12); bass(c[0], a + B * 2.5, B * .9, .09)
    marimba(c[1 + i % 3] + 12, a, .05, -.3 + .3 * (i % 3)); marimba(c[1 + (i + 2) % 3] + 12, a + B / 2, .035, .3)
    i += 1; a += B
    if a > DUR - 1.2: break
# Jingles: Holm-Logo und Werkseite-Zeichen landen auf dem Schlag
for j, n in enumerate([67, 72, 76]): marimba(n, K['logo'] - .1 + j * .12, .14); bell(n + 12, K['logo'] - .1 + j * .12, .04)
for n in [60, 64, 67, 72]: bell(n, K['logo'] + .26, .03)
for j, n in enumerate([72, 67, 72, 79]): marimba(n, K['marke'] + .0 + j * .1, .15); bell(n + 12, K['marke'] + j * .1, .035)
for n in [48, 60, 64, 67, 72, 76]: bell(n, K['festpreis'] + .9, .04); marimba(n, K['festpreis'] + .9, .07)
M = reverb(M, 1.6, .22)

# --- Effekte ---
def click(a, amp=.05, f=3500, pan=.3): t = tt(.03); put(S, a, nz(.03, f, 2) * np.exp(-t * 200) * amp, pan)
def pop(a, amp=.08, f=600, pan=0): t = tt(.14); put(S, a, np.sin(2 * np.pi * np.cumsum(f + 1200 * t / .14) / SR) * np.exp(-t * 32) * amp, pan)
def thud(a, amp=.2): t = tt(.3); put(S, a, (np.sin(2 * np.pi * (60 + 60 * np.exp(-t * 30)) * t) * np.exp(-t * 14) + nz(.3, 900, 2) * np.exp(-t * 60) * .3) * amp)
def scribble(a, d, amp=.05, pan=.3):
    t = tt(d); env = (.5 + .5 * np.sin(2 * np.pi * 8 * t)) ** 2 * np.clip((d - t) / .05, 0, 1); put(S, a, nz(d, 3600, 3) * env * amp, pan)
def swell(a, d=.5, up=True, amp=.06):  # tonales Anschwellen beim Farbfluten (kein Whoosh)
    t = tt(d); f = 220 * (1 + (t / d) * (.5 if up else -.3)); put(S, a, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / d) * amp)
# V7: Suchwort erscheint als Ganzes – ein Tipp statt Tipp-Geräusch je Buchstabe
click(K['tischler'] - .2, .06, 3200, .3)
for i in range(3): pop(K['tischler'] + .45 + i * .1, .04, 700 + i * 100, .3)
click(K['findet'] - .25, .08, 2000);
t = tt(1.2); put(S, K['findet'] + .05, (np.sign(np.sin(2 * np.pi * np.where((t * 8).astype(int) % 2, 1200, 2100) * t)) * .3 + nz(1.2, 2500, 1) * .2) * np.exp(-t * 2.5) * .05, .3)  # alte Seite lädt: Modem-Zirpen
for k, d in [('winzige', .5), ('foto', .3), ('nummer', .4)]: scribble(K[k] - .32, d, .06); pop(K[k] - .1, .07, 400, -.4)  # V5: Kreise zeichnen sich vor dem Wort
# 2 Sekunden: Uhr tickt, dann weg
for i in range(9): click(K['zwei'] + i * (K['weg'] - K['zwei'] + .1) / 8, .07 if i < 8 else 0, 2600, 0)
thud(K['weg'], .18); pop(K['weg'] + .35, .05, 900, .3)
# Auftrag: Karte ploppt, gleitet, landet im anderen Telefon
pop(K['auftrag'], .09, 500, -.4); swell(K['auftrag'] - .3, .5, False, .05)
t = tt(.8); put(S, K['betrieb'] - .1, nz(.8, 2000, 1.5) * np.sin(np.pi * t / .8) ** 2 * .04, np.linspace(-.5, .5, len(t)).mean())
thud(K['nebenan'] + .05, .25)
# Holz: Schrank zeichnet sich, zweimal Klopfen auf Qualität
swell(K['dabei'] - .3, .5, True, .04)
for i in range(4): click(K['dabei'] - .1 + i * .25, .05, 1800, -.2)
for i in range(2): t = tt(.2); put(S, K['besser'] + .08 + i * .16, (np.sin(2 * np.pi * 260 * t) * np.exp(-t * 40) + nz(.2, 700, 4) * np.exp(-t * 50) * .5) * .22, .3)
# Werkseite: Punkt, Flut, Drahtrahmen, 14 Tage
pop(K['werkseite'] - .3, .08, 800); swell(K['werkseite'] - .3, .5, True, .05)
for i in range(4): click(K['baut'] - .1 + i * .15, .05, 4200, .3)
for i in range(6): click(K['website2'] - .2 + i * .1, .04, 3800, .3)
for i in range(14): click(K['vierzehn'] + i * .06, .05, 2200 + i * 80, -.3)
# Holm: Logo-Punkt, Karten, Knopf, Tipp
pop(K['logoW'] - .3, .09, 700, -.3)
for i in range(3): pop(K['projekte'] - .15 + i * .1, .07, 900 + i * 120, .3)  # V5: Papiere landen im Raster
pop(K['knopf'] - .05, .08, 500, .3); click(K['knopf'] + .05, .1, 1500, .3)
# Telefon klingelt: Vibration + Klingelmotiv, Anfragen-Pings
for rep in range(2):
    t = tt(.4); put(S, K['klingelt'] + rep * .45, np.sin(2 * np.pi * 150 * t) * (np.sin(2 * np.pi * 25 * t) > 0) * np.sin(np.pi * t / .4) * .1, .2)
    for j, n in enumerate([76, 79, 84]): marimba(n, K['klingelt'] + rep * .45 + j * .08, .06, .2, S)
for i in range(3): t = tt(.5); put(S, [K['jede'], K['neue2'], K['anfragen']][i] - .05, (np.sin(2 * np.pi * hz(88) * t) + .5 * np.sin(2 * np.pi * hz(95) * t)) * np.exp(-t * 9) * .05, .5)
# Marke
pop(K['marke'] - .2, .08, 800); swell(K['marke'] - .3, .5, True, .05)
for i in range(5): click(K['marke'] + .05 + i * .07, .04, 3500, 0)
pop(K['festpreis'] - .05, .08, 600)
S = reverb(S, .7, .1)
os.makedirs('out', exist_ok=True)
for name, buf, pk in [('musik', M, .6), ('sfx', S, .8)]:
    sf.write(f'out/{name}.wav', (buf / (np.abs(buf).max() + 1e-9) * pk).astype(np.float32), SR)
print('ok')

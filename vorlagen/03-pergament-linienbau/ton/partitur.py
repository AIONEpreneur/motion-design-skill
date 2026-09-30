#!/usr/bin/env python3
"""Bauhütte Architekten V4 – eigene Musik + Effekte (numpy, 48 kHz Stereo, liest out/zeiten.json).
Instrumente wie die feierliche Referenz, aber warm-handwerklich: Kammerstreicher (additiv), Klavier, tiefe Pauke, Holzblock.
Dramaturgie: Fleck wächst (d-Moll, Klavier + tiefe Streicher, tropfendes Wasser) -> Licht geht aus (Pauke, Cluster, Stille)
-> Lampe der Architekten (ein heller Ton, Aufhellung nach F-Dur) -> Vermessen/Planen (Pizzicato-Achtel, präzise)
-> Bauen (Holz, Kelle) -> 100 Jahre (voller Streichersatz, B-Dur -> F-Dur) -> Schlussakkord.
Effekte nur, wo im Bild etwas passiert: Tropfen, Putz reißt auf, Farbrolle, Risse knacken, Lampe klickt, Maßband, Stempel „bleibt/ersetzt“,
Balken rutscht raus, Eichenbalken schiebt sich ein, Kelle streicht, Fenster gehen an."""
import numpy as np, json, wave
class sf:  # V6: soundfile fehlt in dieser Umgebung -> 24-bit-WAV über das wave-Modul
    @staticmethod
    def write(path, x, sr):
        y = (np.clip(x, -1, 1) * 8388607).astype('<i4'); b = y.reshape(-1).view(np.uint8).reshape(-1, 4)[:, :3].tobytes()
        w = wave.open(path, 'wb'); w.setnchannels(x.shape[1]); w.setsampwidth(3); w.setframerate(sr); w.writeframes(b); w.close()
SR = 48000; Z = json.load(open('out/zeiten.json')); DUR = Z['DUR']; K = Z['K']; N = int(DUR * SR); R = np.random.default_rng(31)
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
def strings(ns, a, b, amp=.03, att=.5):
    d = b - a; t = tt(d); e = np.clip(t / att, 0, 1) * np.clip((d - t) / .6, 0, 1)
    for i, n in enumerate(ns):
        f = hz(n); vib = 1 + .005 * np.sin(2 * np.pi * (5 + i * .3) * t + i); ph = 2 * np.pi * np.cumsum(f * vib) / SR
        x = sum(np.sin(k * ph + i) / k ** 1.1 for k in range(1, 8)); put(M, a, x * e * amp, -.6 + 1.2 * i / max(1, len(ns) - 1))
def piano(n, a, d=2.5, amp=.16, pan=0):
    t = tt(d); f = hz(n); x = sum(np.sin(2 * np.pi * f * k * t * (1 + .0004 * k * k)) * np.exp(-t * (1.1 + k * .8)) / k ** 1.4 for k in range(1, 8)); put(M, a, x * np.clip(t / .003, 0, 1) * amp, pan)
def pizz(n, a, amp=.07, pan=0):
    t = tt(.5); f = hz(n); x = (np.sin(2 * np.pi * f * t) + .4 * np.sin(4 * np.pi * f * t) * np.exp(-t * 20)) * np.exp(-t * 9); put(M, a, x * np.clip(t / .002, 0, 1) * amp, pan)
def timp(a, n=38, amp=.35):
    t = tt(1.6); f = hz(n); x = (np.sin(2 * np.pi * f * t * (1 + .02 * np.exp(-t * 8))) + .4 * nz(1.6, 120, 2) * np.exp(-t * 12)) * np.exp(-t * 2.2); put(M, a, x * amp)
B = .6
# 1) Fleck: d-Moll, Klavier + tiefe Streicher
strings([38, 45, 50], .1, K['riskiert'] + .2, .02, 1.2)
for a, n in [(K['fleck'], 62), (K['wand'], 65), (K['altbau'], 69), (K['waechst'], 70), (K['dahinter'], 69), (K['balken'], 65), (K['schimmel'], 64), (K['drueber'], 62)]: piano(n, a, 2.4, .12, .1)
for a in [K['fleck'], K['waechst'], K['dahinter'], K['schimmel']]: piano(38, a, 3.0, .12)
# 2) Licht geht aus: Pauke + Cluster
timp(K['riskiert'], 38, .3); timp(K['haus'], 33, .4)
strings([37, 44, 50, 51], K['riskiert'], K['lampe'] + .4, .022, .3)
# 3) Lampe: ein heller Ton, Aufhellung F-Dur
piano(81, K['lampe'] + .05, 3.0, .08); strings([53, 57, 60, 65], K['lampe'], K['jeder'] + .4, .018, 1.0)
piano(77, K['sehen'], 2.5, .08); piano(72, K['genau'], 2.5, .08)
# 4) Vermessen/Planen: Pizzicato-Achtel F – C – d – B
prog = [[41, 65, 69, 72], [36, 64, 67, 72], [38, 62, 65, 69], [34, 62, 65, 70]]
a = K['jeder'] - .05; i = 0
while a < K['gebaut'] - .05:
    c = prog[(i // 4) % 4]
    if i % 4 == 0: strings(c[1:], a, a + B * 4 + .2, .012, .4); pizz(c[0], a, .1)
    pizz(c[1 + i % 3] + 12, a, .06, -.4); pizz(c[1 + (i + 1) % 3] + 12, a + B / 2, .05, .4)
    i += 1; a += B
# 5) Bauen: wärmer, Holzblock im Takt
prog2 = [[46, 62, 65, 70], [41, 60, 65, 69]]
a = K['gebaut'] - .05; i = 0
while a < K['ihr'] - .1:
    c = prog2[(i // 2) % 2]
    if i % 2 == 0: strings(c[1:], a, a + B * 2 + .3, .016, .3); pizz(c[0], a, .1)
    pizz(c[1 + i % 3] + 12, a, .06, -.3); pizz(c[1 + (i + 1) % 3] + 12, a + B / 2, .05, .3)
    i += 1; a += B
# 6) 100 Jahre + Schluss: voller Satz
strings([46, 58, 62, 65, 70], K['ihr'] - .1, K['n100'] + .2, .02, .8)
strings([41, 57, 60, 65, 69, 72], K['n100'] - .1, DUR, .024, .6)
timp(K['n100'], 41, .25)
for n in [53, 60, 65, 69, 72, 77]: piano(n, K['n100'], 3.5, .07)
for n in [41, 53, 57, 60, 65]: piano(n, K['kostenlos'] + .4, 3.0, .08)
M = reverb(M, 2.4, .3)

# --- Effekte ---
def drip(a, amp=.05, pan=0):
    t = tt(.15); f = 900 + 1400 * np.exp(-t * 30); put(S, a, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 30) * amp, pan)
for i in range(int(K['riskiert'] / .9)): drip(.5 + i * .9 + R.random() * .1, .04, .3)
# Putz reißt auf (Wand teilt sich)
t = tt(.5); put(S, K['cut']['b'], nz(.5, 1800, 1.5) * np.exp(-t * 7) * .12 + nz(.5, 300, 2) * np.exp(-t * 10) * .1)
for i in range(10): t = tt(.05); put(S, K['cut']['b'] + .1 + i * .05, nz(.05, 2500, 4) * np.exp(-t * 80) * .05, R.uniform(-.5, .5))
# Farbrolle
t = tt(1.2); put(S, K['cut']['c'], nz(1.2, 900, .8) * (0.6 + .4 * np.sin(2 * np.pi * 9 * t)) * np.sin(np.pi * t / 1.2) * .06, .2)
# Risse knacken
for i, d in enumerate([.3, .7, 1.1]): t = tt(.2); put(S, K['riskiert'] + d, (nz(.2, 3000, 6) * np.exp(-t * 60) + nz(.2, 200, 3) * np.exp(-t * 25) * .6) * .12, -.3 + i * .3)
# Lampe klickt an
t = tt(.06); put(S, K['lampe'], nz(.06, 4000, 5) * np.exp(-t * 120) * .08, -.5)
t = tt(1.2); put(S, K['lampe'] + .05, np.sin(2 * np.pi * 110 * t) * np.sin(np.pi * t / 1.2) * .02, -.4)
# Maßband / Maßketten
for k in ['jeder', 'riss', 'zgenau']:
    t = tt(.5); put(S, K[k], nz(.5, 5000, 8) * (0.5 + .5 * np.sign(np.sin(2 * np.pi * 40 * t))) * np.sin(np.pi * t / .5) * .03, .3)
    t = tt(.08); put(S, K[k] + .5, nz(.08, 1500, 4) * np.exp(-t * 60) * .08, .3)
# Stempel bleibt / ersetzt
for k in ['bleibt', 'ersetzt']: t = tt(.3); put(S, K[k] + .05, (np.sin(2 * np.pi * (80 + 60 * np.exp(-t * 30)) * t) * np.exp(-t * 12) + nz(.3, 900, 3) * np.exp(-t * 40) * .4) * .25)
# Balken raus (Holz schabt), Eiche rein (Klack)
t = tt(.8); put(S, K['gebaut'] - .1, nz(.8, 600, 3) * (0.6 + .4 * np.sin(2 * np.pi * 17 * t)) * np.sin(np.pi * t / .8) * .1, -.3)
t = tt(.25); put(S, K['holz'], (np.sin(2 * np.pi * 240 * t) + .6 * np.sin(2 * np.pi * 520 * t)) * np.exp(-t * 25) * .18, -.3)
# Kelle streicht Kalk
t = tt(1.1); put(S, K['kalk'], nz(1.1, 2600, 1) * np.sin(np.pi * t / 1.1) * (0.7 + .3 * np.sin(2 * np.pi * 3 * t)) * .05, -.2)
# Fenster gehen an (warme Glöckchen)
for i in range(8): t = tt(.8); put(S, K['ihr'] - .2 + i * .08, np.sin(2 * np.pi * hz(84 + [0, 4, 7, 12, 7, 4, 9, 12][i]) * t) * np.exp(-t * 5) * .025, -.6 + i * .15)
t = tt(.3); put(S, K['erst'], np.sin(2 * np.pi * 1047 * t) * np.exp(-t * 10) * .04)
t = tt(.6); put(S, K['schimmel'] - .05, np.sin(2 * np.pi * 1568 * t) * np.exp(-t * 7) * .03, .3)
S = reverb(S, 1.0, .15)
for name, buf, pk in [('musik', M, .6), ('sfx', S, .8)]:
    sf.write(f'out/{name}.wav', (buf / (np.abs(buf).max() + 1e-9) * pk).astype(np.float32), SR)
print('ok')

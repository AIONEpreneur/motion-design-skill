#!/usr/bin/env python3
"""Quellwerk Office V4 – eigene Musik + Effekte (Marimba/Kalimba, weicher Bass, Shaker – warm, „wässrig“).
Dramaturgie: Nachmittagstief (d-Moll, langsam, müde Uhr) -> Kisten schleppen (schwerer, stockender Puls) -> Wendung „Quellwerk“:
Wasser strömt, Tonart hellt nach F-Dur auf, Groove 112 BPM -> Kaffee (wärmer, Bass) -> 4-Wochen-Kreis (Marimba-Figur je Woche)
-> Anstoßen (Akkord) -> Packshot (Schlussakkord).
Effekte nur aus dem Material: Tropfen, Plastikkiste, Flaschen, Schritte, Wasser in der Leitung, Filter-Klick, Eis, Kohlensäure,
Taste, Einschenken (Tonhöhe steigt mit dem Füllstand), Mahlwerk, Karton, Glas/Tasse klirren, Uhr. Kein Whoosh."""
import numpy as np, soundfile as sf, os, json
SR = 48000; Z = json.load(open('out/zeiten.json')); K = Z['K']; DUR = Z['DUR']; N = int(DUR * SR); R = np.random.default_rng(11)
M = np.zeros((N, 2)); S = np.zeros((N, 2))
def tt(d): return np.arange(int(d * SR)) / SR
def put(buf, a, x, pan=0.):
    i = int(a * SR)
    if i < 0: x = x[-i:]; i = 0
    n = min(len(x), N - i)
    if n > 0: buf[i:i + n, 0] += x[:n] * np.cos((pan + 1) * np.pi / 4) * 1.41; buf[i:i + n, 1] += x[:n] * np.sin((pan + 1) * np.pi / 4) * 1.41
def bp(x, fc, q=2.):  # Resonanzfilter (Biquad-Bandpass), vektorisiert per scipy-freiem Rekursionsweg
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
def env(t, a, d): return np.clip(t / a, 0, 1) * np.exp(-t * d)
# --- Instrumente ---
def marimba(n, a, amp=.1, pan=0, d=1.0):
    t = tt(d); f = hz(n); x = np.sin(2 * np.pi * f * t) * np.exp(-t * 5) + .35 * np.sin(2 * np.pi * f * 3.93 * t) * np.exp(-t * 22) + .12 * np.sin(2 * np.pi * f * 9.2 * t) * np.exp(-t * 40)
    put(M, a, x * np.clip(t / .002, 0, 1) * amp, pan)
def kalimba(n, a, amp=.08, pan=0):
    t = tt(1.4); f = hz(n); x = (np.sin(2 * np.pi * f * t) + .25 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 12)) * np.exp(-t * 3.2)
    put(M, a, x * np.clip(t / .003, 0, 1) * amp, pan)
def pad(ns, a, b, amp=.025, att=.8):
    t = tt(b - a); e = np.clip(t / att, 0, 1) * np.clip((b - a - t) / .8, 0, 1)
    for i, n in enumerate(ns): f = hz(n); put(M, a, (np.sin(2 * np.pi * f * t) + .3 * np.sin(4 * np.pi * f * 1.002 * t)) * e * amp, -.5 + i / max(1, len(ns) - 1))
def bass(n, a, d, amp=.18):
    t = tt(d); f = hz(n); put(M, a, np.sin(2 * np.pi * f * t) * (1 + .3 * np.sin(4 * np.pi * f * t)) * np.clip(t / .01, 0, 1) * np.clip((d - t) / .05, 0, 1) * np.exp(-t * 1.2) * amp)
def kick(a, amp=.3):
    t = tt(.35); put(M, a, np.sin(2 * np.pi * np.cumsum(50 + 90 * np.exp(-t * 30)) / SR) * np.exp(-t * 10) * amp)
def clap(a, amp=.05):
    t = tt(.2); put(M, a, bp(nz(.2), 1400, 1) * np.exp(-t * 25) * amp, .15)
def shaker(a, amp=.02, pan=-.3):
    t = tt(.09); put(M, a, bp(nz(.09), 6500, 1.5) * np.sin(np.pi * t / .09) * amp, pan)

# 1) Nachmittagstief: d-Moll, müde, 80 BPM
b1 = .75
pad([50, 53, 57], 0, K['quellwerk'], .02, 1.0)
for i, a in enumerate(np.arange(.1, K['quellwerk'] - .3, b1)):
    if i % 2 == 0: bass([38, 38, 34, 36][(i // 2) % 4], a, b1 * 1.8, .14)
    marimba([62, 65, 69, 65][i % 4] - (0 if i % 8 < 4 else 2), a + b1 / 2, .05, .3 - .2 * (i % 2), .8)
for k in ['leer', 'auch']: marimba(50, K[k], .12, 0, 1.6); marimba(57, K[k], .06, 0, 1.6)
# schwerer Puls beim Schleppen
for a in np.arange(K['schleppt'] - .2, K['quellwerk'] - .3, b1): kick(a, .18)
# 2) Wendung: kurze Stille, dann F-Dur, 112 BPM
b2 = 60 / 112
for n in [65, 69, 72, 77]: kalimba(n + 12, K['quellwerk'] - .05 + (n - 65) * .012, .07, (n - 70) / 10)
prog = [[41, 65, 69, 72], [38, 62, 65, 69], [34, 62, 65, 70], [36, 64, 67, 72]]
a = K['quellwerk'] + .05; i = 0
while a < K['ende'] - .3:
    c = prog[(i // 4) % 4]
    if a > K['wasser'] - .2:
        kick(a, .26 if i % 2 == 0 else .14); shaker(a + b2 / 2, .022); shaker(a + b2 / 4, .012, .3)
        if i % 2 == 1: clap(a, .05)
    if i % 4 == 0: pad(c[1:], a, a + 4 * b2 + .3, .018); bass(c[0], a, 2 * b2 * .95, .17); bass(c[0] + 7, a + 2 * b2, 2 * b2 * .9, .12)
    marimba(c[1 + i % 3] + 12, a, .05, -.3 + .3 * (i % 3), .6); marimba(c[1 + (i + 2) % 3] + 12, a + b2 / 2, .035, .3, .5)
    i += 1; a += b2
# Kaffee: wärmer (tiefe Kalimba), 4-Wochen-Kreis: Figur je Woche
for j, n in enumerate([65, 67, 69, 72]): kalimba(n, K['bohnen'] + .6 + (K['ohne'] - .6 - K['bohnen']) * (j + .5) / 4, .08, -.4 + .27 * j)
# Anstoßen: heller Akkord; Schluss
for n in [65, 69, 72, 77, 81]: kalimba(n + 12, K['frisch2'] - .05, .05, (n - 72) / 12)
pad([53, 60, 65, 69, 72], K['ende'] - .35, DUR, .03, .5); bass(41, K['ende'] - .35, DUR - K['ende'], .15)
for n in [65, 72, 77, 81, 84]: marimba(n, K['zwei'] - .05, .05, (n - 77) / 10, 2.0)
for n in [53, 65, 69, 72]: kalimba(n + 12, K['testen'] + .3, .06, 0)
M = reverb(M, 1.6, .22)

# ===== Effekte =====
# Tropfen fällt und trifft das leere Glas
t = tt(.5); put(S, K['tropfen'], np.sin(2 * np.pi * np.cumsum(1300 - 700 * np.exp(-t * 30)) / SR) * np.exp(-t * 14) * .18 + np.sin(2 * np.pi * 3400 * t) * np.exp(-t * 30) * .05, .2)
# Uhr tickt im Nachmittag (leise)
for a in np.arange(.2, K['kasten'], .5): t = tt(.03); put(S, a, np.sin(2 * np.pi * 2600 * t) * np.exp(-t * 200) * .05, -.6)
# Kiste landet: Plastik-Thud + Flaschen klappern
t = tt(.5); put(S, K['kasten_land'], (np.sin(2 * np.pi * (95 + 60 * np.exp(-t * 30)) * t) * np.exp(-t * 12) + bp(nz(.5), 700, 2) * np.exp(-t * 25) * .5) * .5)
for j in range(6):
    t = tt(.25); put(S, K['kasten_land'] + .03 + j * .03 + R.random() * .02, bp(nz(.25), 1800 + R.random() * 900, 12) * np.exp(-t * 28) * .1, R.random() - .5)
# Flasche kippt und rollt (hohles Klopfen)
for j, d in enumerate([.05, .45, .62, .75]):
    t = tt(.3); put(S, K['kippt'] + d, bp(nz(.3), 900 + 150 * j, 10) * np.exp(-t * 30) * (.16 - .03 * j), .3 + .1 * j)
# Kisten stapeln sich (6 Plastik-Stöße)
for j in range(6):
    t = tt(.3); put(S, K['kisten_land'][j], (np.sin(2 * np.pi * (120 - j * 6) * t) * np.exp(-t * 20) + bp(nz(.3), 800, 3) * np.exp(-t * 40) * .3) * .18, -.5 + j * .2)
# schwere Schritte auf der Treppe
for a in np.arange(K['schleppt'] - .4, K['quellwerk'] - .4, .42):
    t = tt(.2); put(S, a, (np.sin(2 * np.pi * 70 * t) * np.exp(-t * 30) + bp(nz(.2), 400, 2) * np.exp(-t * 40) * .3) * .12, .4)
# Wasser in der Leitung (Rauschen + Blubbern), steigt nach oben
d = K['gefiltert'] - K['quellwerk']; t = tt(d); flow = bp(nz(d), 700, .7) * np.clip(t / .4, 0, 1) * np.clip((d - t) / .5, 0, 1)
put(S, K['quellwerk'] - .2, flow * .1)
for j in range(40):
    a = K['quellwerk'] + R.random() * (d - .4); t = tt(.12); f0 = 300 + R.random() * 500
    put(S, a, np.sin(2 * np.pi * np.cumsum(f0 * (1 + 2.5 * t / .12)) / SR) * np.exp(-t * 30) * .06, R.random() - .5)
# Ankunft im Spender: Gluckern
for j in range(4): t = tt(.18); put(S, K['leitung'] + .05 + j * .09, np.sin(2 * np.pi * np.cumsum(220 * (1 + 3 * t / .18)) / SR) * np.exp(-t * 18) * .12)
# Filter rastet ein, Eis klingt, Kohlensäure zischt
t = tt(.12); put(S, K['gefiltert'], bp(nz(.12), 3000, 4) * np.exp(-t * 60) * .15 + np.sin(2 * np.pi * 900 * t) * np.exp(-t * 80) * .08, -.4)
t = tt(1.2); put(S, K['gekuehlt'], sum(np.sin(2 * np.pi * f * t) * np.exp(-t * dd) for f, dd in [(2793, 4), (4186, 6), (5588, 9)]) * .05, .3)
t = tt(1.0); put(S, K['sprudelnd'], bp(nz(1.0), 7000, 1.2) * np.exp(-t * 3) * .07, .4)
for j in range(24): t = tt(.03); put(S, K['sprudelnd'] + R.random() * .9, np.sin(2 * np.pi * (1500 + R.random() * 2500) * t) * np.exp(-t * 120) * .05, R.random() * 2 - 1)
# Taste, Einschenken (Resonanz steigt mit Füllstand), Spritzer
t = tt(.08); put(S, K['knopfdruck'] + .02, bp(nz(.08), 2500, 3) * np.exp(-t * 80) * .2 + np.sin(2 * np.pi * 1200 * t) * np.exp(-t * 90) * .1)
d = 1.0; t = tt(d); pour = bp(nz(d), 1500, .8) * .5
res = np.sin(2 * np.pi * np.cumsum(350 + 900 * (t / d) ** 1.3) / SR) * .35
put(S, K['knopfdruck'] + .08, (pour + res * (R.standard_normal(len(t)) * .3 + .7)) * np.clip(t / .05, 0, 1) * np.clip((d - t) / .1, 0, 1) * .14)
for j in range(10): t = tt(.1); put(S, K['knopfdruck'] + .2 + R.random() * .8, np.sin(2 * np.pi * (900 + R.random() * 1400) * t) * np.exp(-t * 50) * .05, R.random() - .5)
# Bohnen rascheln im Kreis, Mahlwerk
for j in range(26): t = tt(.05); put(S, K['kaffee'] + R.random() * (K['mahlt'] - K['kaffee']), bp(nz(.05), 2500 + R.random() * 2000, 6) * np.exp(-t * 90) * .06, R.random() * 2 - 1)
d = 1.1; t = tt(d); grind = bp(nz(d), 1800, 1.2) * (1 + .6 * np.sin(2 * np.pi * 55 * t)) * np.clip(t / .08, 0, 1) * np.clip((d - t) / .2, 0, 1)
put(S, K['mahlt'] - .05, grind * .12)
d = 1.2; t = tt(d); put(S, K['mahlt'] + .5, bp(nz(d), 500, 1) * np.sin(np.pi * t / d) * .07)            # Kaffee läuft
# Box: Karton-Plopp, Artikel springen heraus
t = tt(.3); put(S, K['karton_auf'], (np.sin(2 * np.pi * (150 + 80 * np.exp(-t * 30)) * t) * np.exp(-t * 18) + bp(nz(.3), 900, 2) * np.exp(-t * 35) * .4) * .22)
for j in range(5): t = tt(.1); put(S, K['ohne'] + .15 + j * .05, np.sin(2 * np.pi * (600 + j * 180) * t) * np.exp(-t * 40) * .06, -.5 + j * .25)
# Anstoßen: Glas + Porzellan
t = tt(1.6); put(S, K['klirr'], sum(np.sin(2 * np.pi * f * t) * np.exp(-t * dd) * w for f, dd, w in [(1760, 3, 1), (2637, 4, .7), (4400, 6, .4), (3136, 5, .5), (5274, 8, .25)]) * .07)
t = tt(.6); put(S, K['frisch2'] - .02, bp(nz(.6), 3500, 3) * np.exp(-t * 12) * .05, .2)
# Uhr dreht bis Feierabend: Ratsche
for j in range(18): t = tt(.03); put(S, K['feierabend'] - .1 + j * .055, bp(nz(.03), 3800, 5) * np.exp(-t * 150) * .09, .5)
t = tt(.8); put(S, K['feierabend'] + .95, np.sin(2 * np.pi * 1318 * t) * np.exp(-t * 5) * .06, .5)                        # Glöckchen 18:00
# Angebot: Pille ploppt
t = tt(.2); put(S, K['zwei'], np.sin(2 * np.pi * np.cumsum(500 + 900 * t / .2) / SR) * np.exp(-t * 20) * .08)
S = reverb(S, .9, .14)
# Atempause vor „Bohnen“: Kranz verwandelt sich in den Lieferkreis – Musik und Effekte setzen kurz aus, das „B“ bleibt verständlich
tg = np.arange(N) / SR; dip = 1 - .85 * np.clip(np.minimum((tg - (K['bohnen'] - .35)) / .1, ((K['bohnen'] + .35) - tg) / .15), 0, 1)
M *= dip[:, None]; S *= dip[:, None]
os.makedirs('out', exist_ok=True)
for name, buf, pk in [('musik', M, .6), ('sfx', S, .8)]:
    sf.write(f'out/{name}.wav', (buf / (np.abs(buf).max() + 1e-9) * pk).astype(np.float32), SR)
print('ok')

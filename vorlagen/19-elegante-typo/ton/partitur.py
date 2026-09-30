#!/usr/bin/env python3
"""Klarsicht Beratung V4 – eigene Musik + Effekte. Dramaturgie folgt dem Kunden:
Chaos (gehetzter Puls, dissonante Pizzicato-Cluster, alles gleichzeitig) -> Stillstand (ein Ton, der nicht weitergeht)
-> Wendung „Klarsicht sortiert“ (Glasklang, Luft) -> Ordnung (A-Dur, ruhiges Klavier-Ostinato, Streicher)
-> Fortschritt Woche für Woche (Puls kommt dazu) -> Urlaub (offener Akkord, Glanz) -> Marke (Auflösung).
Effekte nur aus dem Bild: Wörter schlagen auf, Stift zeichnet Linien, Stempel ±0 %, Lichtbalken (tonal), Karten werden sortiert,
Wörter fallen weg, Wochenpunkte, Haken, Übergabe, Pfeil, Linse stellt scharf, Knopf erscheint. Kein Whoosh."""
import numpy as np, soundfile as sf, os, json
SR = 48000; Z = json.load(open('out/zeiten.json')); K = Z['K']; DUR = Z['DUR']; N = int(DUR * SR); R = np.random.default_rng(19)
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
def piano(n, a, d=2.4, amp=.12, pan=0):
    t = tt(d); f = hz(n); x = sum(np.sin(2 * np.pi * f * k * t * (1 + .0003 * k * k)) * np.exp(-t * (1.0 + k * .9)) / k ** 1.5 for k in range(1, 7)); put(M, a, x * np.clip(t / .003, 0, 1) * amp, pan)
def pizz(n, a, amp=.06, pan=0):
    t = tt(.35); f = hz(n); put(M, a, (np.sin(2 * np.pi * f * t) + .3 * np.sin(4 * np.pi * f * t)) * np.exp(-t * 16) * np.clip(t / .002, 0, 1) * amp, pan)
def strings(ns, a, b, amp=.02):
    t = tt(b - a); e = np.clip(t / .9, 0, 1) * np.clip((b - a - t) / .8, 0, 1); vib = 1 + .003 * np.sin(2 * np.pi * 5 * t)
    for i, n in enumerate(ns):
        f = hz(n); x = sum(np.sin(2 * np.pi * f * k * np.cumsum(vib) / SR) / k for k in range(1, 5)); put(M, a, x * e * amp, -.6 + 1.2 * i / max(1, len(ns) - 1))
def glass(ns, a, amp=.035):
    for i, n in enumerate(ns): t = tt(2.5); f = hz(n); put(M, a + i * .05, (np.sin(2 * np.pi * f * t) + .3 * np.sin(2 * np.pi * f * 2.01 * t)) * np.clip(t / .25, 0, 1) * np.exp(-t * 1.4) * amp, -.4 + .3 * i)
def kick(a, amp=.25):
    t = tt(.35); ph = 2 * np.pi * np.cumsum(46 + 90 * np.exp(-t * 30)) / SR; put(M, a, np.sin(ph) * np.exp(-t * 10) * amp)
def tick(a, amp=.03, f=5000, pan=0): t = tt(.04); put(M, a, nz(.04, f, 5) * np.exp(-t * 160) * amp, pan)
# 1) Chaos 0–6.6: gehetzter Puls 150 BPM, dissonante Cluster
for i, a in enumerate(np.arange(.1, K['sie'], .2)):
    kick(a, .16 if i % 2 == 0 else .07); tick(a + .1, .03, 6000, .3)
    pizz([57, 58, 63, 64, 70][i % 5], a, .045, -.5 + .25 * (i % 5)); pizz([69, 70, 75][i % 3], a + .1, .03, .5)
for k in ['angebote', 'personal', 'rechnungen', 'kunden']: piano(45, K[k], 1.2, .12); piano(46, K[k], 1.2, .08)
# 2) Stillstand 6.6–9.2: der Puls verliert Kraft, ein liegender Ton
strings([57, 58], K['sie'], K['klarsicht'] + .2, .016)
for a in np.arange(K['sie'], K['klarsicht'] - .2, .6): kick(a, .1)
piano(57, K['stelle'], 2.0, .1); piano(58, K['stelle'] + .01, 2.0, .06)
# 3) Wendung: Glasklang + A-Dur
glass([69, 73, 76, 81], K['klarsicht'] - .1, .03)
B = .56
prog = [[45, 64, 69, 73], [42, 64, 69, 73], [38, 62, 66, 69], [40, 64, 68, 71]]
a = K['klarsicht'] + .5; i = 0
while a < K['ergebnis'] - .2:
    c = prog[(i // 4) % 4]
    if i % 4 == 0: strings(c[1:], a, a + B * 4 + .2, .012); piano(c[0], a, 2.2, .1)
    piano(c[1 + i % 3] + 12, a, 1.4, .045, -.3 + .3 * (i % 3)); piano(c[1 + (i + 1) % 3] + 12, a + B / 2, 1.2, .03, .3)
    if a > K['zwoelf'] - .1: kick(a, .16 if i % 2 == 0 else .08); tick(a + B / 2, .02, 7000, -.2)
    i += 1; a += B
# 4) Ergebnis + Urlaub: offener Akkord, Glanz
strings([57, 64, 69, 73, 76], K['ergebnis'], K['name'] + .3, .014)
piano(45, K['n20'], 2.4, .1); piano(69, K['weniger'], 2.4, .07); piano(76, K['weniger'] + .08, 2.4, .05)
glass([76, 81, 85, 88], K['urlaub'] - .05, .035); piano(45, K['urlaub'], 3, .12); piano(57, K['urlaub'], 3, .08)
# 5) Marke: Auflösung
a = K['name']; i = 0
while a < DUR - 1.8:
    c = [[45, 64, 69, 73], [38, 62, 66, 69]][(i // 4) % 2]
    if i % 4 == 0: strings(c[1:], a, a + B * 4 + .2, .012); piano(c[0], a, 2.2, .09)
    piano(c[1 + i % 3] + 12, a, 1.2, .035); i += 1; a += B
for n in [45, 52, 57, 64, 69, 73]: piano(n, DUR - 1.7, 2.2, .08)
glass([81, 88], DUR - 1.7, .02)
M = reverb(M, 2.4, .3)
# --- Effekte ---
def thud(a, amp=.2, f0=90, pan=0):
    t = tt(.35); put(S, a, (np.sin(2 * np.pi * (f0 + 40 * np.exp(-t * 30)) * t) * np.exp(-t * 14) + nz(.35, 1400, 2) * np.exp(-t * 50) * .35) * amp, pan)
for j, a in enumerate(np.arange(K['landet'] - .25, K['landet'] + .45, .035)): thud(a, .07, 120 + 30 * (j % 4), R.uniform(-.6, .6))  # V7: Berg fällt auf den Punkt
for k in ['angebote', 'personal', 'rechnungen', 'kunden']: thud(K[k], .3, 70)                                     # große Wörter knallen
def pen(a, d, amp=.04):
    t = tt(d); put(S, a, nz(d, 3200, 4) * (.6 + .4 * np.abs(np.sin(2 * np.pi * 9 * t))) * np.sin(np.pi * t / d) * amp, .2)
pen(K['mehr'] - .1, 1.2)
for ev in (K['tritt'], K['stelle']): pen(ev - .26, .24, .03); thud(ev + .12, .22, 75)                             # V7: Pfeil schießt vor und schnappt zurück
for a in [w for w in [K['klarsicht'] - .15, K['zwoelf'] - .3, K['ergebnis'] - .25, K['name'] - .25]]:              # Lichtbalken: tonaler Glanz
    t = tt(.7); f = 880 * (1 + .5 * t / .7); put(S, a, (np.sin(2 * np.pi * np.cumsum(f) / SR) + .5 * np.sin(2 * np.pi * np.cumsum(f * 1.5) / SR)) * np.sin(np.pi * t / .7) * .012, .3)
for j in range(30): t = tt(.05); put(S, K['sortiert'] - .3 + j * .009, nz(.05, 4500, 3) * np.exp(-t * 90) * .03, -.4 + .8 * (j % 3) / 2)  # Karten sortieren
for j in range(10): t = tt(.3); f = 700 - 40 * j; put(S, K['n30'] - .3 + j * .028, np.sin(2 * np.pi * f * t) * np.exp(-t * 12) * .012, -.5 + j * .1)  # Wörter fallen weg
for n in range(12):                                                                                                 # Wochenpunkte
    a = K['termin'] - .22 + (K['team'] - .25 - K['termin'] + .22) * n / 12; t = tt(.08); put(S, a, np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 60) * .03, -.6 + n * .1)
    if n in (3, 7, 11): t = tt(.4); put(S, a, (np.sin(2 * np.pi * hz(88) * t) + np.sin(2 * np.pi * hz(93) * t)) * np.exp(-t * 9) * .025)
for j in range(3): t = tt(.25); put(S, K['team'] - .05 + j * .1, np.sin(2 * np.pi * hz(76 + 3 * j) * t) * np.exp(-t * 14) * .04, -.5 + .5 * j)  # Übergabe
pen(K['fuehren'] - .4, .45, .03); pen(K['weniger'] - .28, .28, .035); pen(K['baustellen'] - .28, .28, .035)  # V7: Punkt nach vorn, Minus-Strich, Durchstreichen
t = tt(.12); put(S, K['name'] + .6, nz(.12, 3000, 8) * np.exp(-t * 70) * .08)                                      # Linse rastet ein
t = tt(.2); put(S, K['kostenlos'] - .05, np.sin(2 * np.pi * 1100 * t) * np.exp(-t * 25) * .04)                      # Knopf erscheint
for i, a in enumerate(np.arange(K['team'] - .1, K['team'] + .55, .16)): thud(a, .05, 130 + 20 * (i % 2), .4)            # Team kommt (Schritte)
t = tt(.25); put(S, K['n20'], (nz(.25, 2500, 6) * np.exp(-t * 40) + np.sin(2 * np.pi * 180 * t) * np.exp(-t * 30) * .5) * .12)  # 20 h lösen sich
thud(K['urlaub'] - .02, .2, 90)                                                                                     # V7: Urlaub steht
d = K['name'] - K['endlich'] + .6; t = tt(d); put(S, K['endlich'] - .2, nz(d, 700, .7) * (.5 + .5 * np.sin(2 * np.pi * .7 * t) ** 2) * np.sin(np.pi * t / d) * .05)  # Wellen
for i in range(3): t = tt(.18); put(S, K['endlich'] + .3 + i * .45, np.sin(2 * np.pi * np.cumsum(2400 - 900 * t / .18) / SR) * np.sin(np.pi * t / .18) * .012, .6)  # Möwen
S = reverb(S, .8, .15)
os.makedirs('out', exist_ok=True)
for name, buf, pk in [('musik', M, .6), ('sfx', S, .8)]:
    sf.write(f'out/{name}.wav', (buf / (np.abs(buf).max() + 1e-9) * pk).astype(np.float32), SR)
print('ok')

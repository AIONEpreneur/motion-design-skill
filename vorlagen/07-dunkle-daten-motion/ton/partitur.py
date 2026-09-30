#!/usr/bin/env python3
"""Kanzlei Weber V4/V7 (V7: alle Zeiten aus K) – eigene Musik + Effekte (Synthesizer, passend zur Leuchtlinien-Welt).
Dramaturgie: goldener Aufstieg (D-Dur-Arpeggio) -> Absturz (Tonhöhe stürzt, Einschlag) -> d-Moll-Drone, Uhr tickt je Wochen-Tor
-> Treppe abwärts (4 fallende Basstöne) -> Polster läuft leer, Maschine: metallischer Schlag -> Rückspulen (rückwärts gespielte Töne)
-> Stille + Glocke -> Lösung: Puls 120 BPM, jedes Monats-Tor ein Ton der Tonleiter aufwärts, jedes Quartal ein Akkord,
Rücklage: Zähl-Ticks -> Glaswand zerspringt (Glas-Partials) -> Maschine läuft an -> Schlussakkord.
Alle Zeitpunkte aus out/zeiten.json; Tor-Zeiten mit derselben Interpolation wie im Film."""
import numpy as np, soundfile as sf, os, json
SR = 48000; Z = json.load(open('out/zeiten.json')); K = Z['K']; DUR = Z['DUR']; N = int(DUR * SR); R = np.random.default_rng(7)
M = np.zeros((N, 2)); S = np.zeros((N, 2))
def tt(d): return np.arange(int(d * SR)) / SR
def put(buf, a, x, pan=0.):
    i = int(a * SR); n = min(len(x), N - i)
    if i < 0: x = x[-i:]; n = min(len(x), N); i = 0
    if n > 0: buf[i:i + n, 0] += x[:n] * np.cos((pan + 1) * np.pi / 4) * 1.41; buf[i:i + n, 1] += x[:n] * np.sin((pan + 1) * np.pi / 4) * 1.41
def lp(x, fc):  # einfacher Tiefpass 1. Ordnung (zweimal)
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); s = 0.
    for _ in range(2):
        for i in range(len(x)): s = (1 - a) * x[i] + a * s; y[i] = s
        x = y.copy()
    return y
def reverb(x, sec, mix):
    n = int(sec * SR); ir = R.standard_normal((n, 2)) * np.exp(-np.arange(n) / SR * 6 / sec)[:, None]; F = 1 << int(np.ceil(np.log2(len(x) + n))); out = np.zeros_like(x)
    for c in range(2): out[:, c] = np.fft.irfft(np.fft.rfft(x[:, c], F) * np.fft.rfft(ir[:, c], F), F)[:len(x)]
    out *= np.abs(x).max() / (np.abs(out).max() + 1e-9); return x * (1 - mix) + out * mix
def hz(n): return 440 * 2 ** ((n - 69) / 12)
def saw(f, t, det=0.): return sum(np.sin(2 * np.pi * f * (1 + det) * k * t) / k for k in range(1, 9))
# --- Instrumente ---
def pluck(n, a, amp=.08, pan=0, d=.5, bright=1.):
    t = tt(d); f = hz(n); x = (np.sin(2 * np.pi * f * t) + .45 * bright * np.sin(4 * np.pi * f * t) * np.exp(-t * 18) + .2 * bright * np.sin(6 * np.pi * f * t) * np.exp(-t * 26)) * np.exp(-t * 7)
    put(M, a, x * np.clip(t / .002, 0, 1) * amp, pan)
def pad(ns, a, b, amp=.03, att=.8):
    t = tt(b - a); e = np.clip(t / att, 0, 1) * np.clip((b - a - t) / .8, 0, 1)
    for i, n in enumerate(ns): f = hz(n); put(M, a, (saw(f, t, .003) * .35 + np.sin(2 * np.pi * f * t)) * .5 * e * amp, -.6 + 1.2 * i / max(1, len(ns) - 1))
def bass(n, a, d, amp=.2):
    t = tt(d); f = hz(n); x = np.tanh(2.2 * (np.sin(2 * np.pi * f * t) + .3 * np.sin(4 * np.pi * f * t))) * .6
    put(M, a, x * np.clip(t / .006, 0, 1) * np.clip((d - t) / .04, 0, 1) * amp)
def kick(a, amp=.35):
    t = tt(.38); ph = 2 * np.pi * np.cumsum(46 + 110 * np.exp(-t * 32)) / SR; put(M, a, np.sin(ph) * np.exp(-t * 9) * amp)
def hat(a, amp=.03, pan=.2):
    t = tt(.06); put(M, a, R.standard_normal(len(t)) * np.exp(-t * 90) * amp, pan)
def bell(n, a, amp=.1, d=2.5, pan=0):
    t = tt(d); f = hz(n); x = sum(np.sin(2 * np.pi * f * r * t) * np.exp(-t * (1.2 + r)) * w for r, w in [(1, 1), (2.76, .4), (5.4, .2), (8.9, .08)])
    put(M, a, x * np.clip(t / .002, 0, 1) * amp, pan)

# Tor-Zeiten wie im Film (monotone kubische Interpolation)
def pchip(keys):
    xs = np.array([k[0] for k in keys]); ys = np.array([k[1] for k in keys]); d = np.diff(ys) / np.diff(xs); n = len(xs); m = np.zeros(n)
    m[0] = d[0]; m[-1] = d[-1]
    for i in range(1, n - 1): m[i] = 0 if d[i - 1] * d[i] <= 0 else 2 / (1 / d[i - 1] + 1 / d[i])
    def f(t):
        if t <= xs[0]: return ys[0] + m[0] * (t - xs[0])
        if t >= xs[-1]: return ys[-1] + m[-1] * (t - xs[-1])
        i = np.searchsorted(xs, t) - 1; h = xs[i + 1] - xs[i]; s = (t - xs[i]) / h
        return (2 * s**3 - 3 * s**2 + 1) * ys[i] + (s**3 - 2 * s**2 + s) * h * m[i] + (-2 * s**3 + 3 * s**2) * ys[i + 1] + (s**3 - s**2) * h * m[i + 1]
    return f
# V7: Ereigniszeiten kommen direkt aus K (zeiten.py) – dieselben Werte wie im Film
TB0 = K['tb0']; t_gate = K['gate']; t_weeks = K['weeks']; t_stairs = K['stairs']
t_month = K['mon']; t_q = K['q']; t_wall = K['impact']; t_mach = K['mach']

# ===== Musik =====
# 1) Aufstieg (0 – Tor): D-Dur-Arpeggio in Sechzehnteln, steigend
for i, a in enumerate(np.arange(0.05, t_gate, .125)): pluck([62, 66, 69, 74, 78, 81][i % 6] + (12 if i > 5 else 0), a, .055, -.4 + .8 * (i % 2), .35)
pad([50, 57, 62, 66], 0, t_gate + .3, .02, .1)
# 2) Absturz -> d-Moll-Drone mit Puls, bis zum Rückspulen
pad([38, 45, 50, 53], t_gate + .4, K['dasmuss'] + .2, .028, 1.2)
for a in np.arange(t_gate + .6, K['polster'] - .2, .5): kick(a, .22); bass(38, a, .22, .12)
for i, a in enumerate(t_stairs): bass(50 - i * 3, a, .45, .2); pluck(62 - i * 3, a, .06, .3, .8, .6)
for a in np.arange(K['polster'], K['dasmuss'] - .2, 1.0): kick(a, .16)
for n in [41, 48, 51, 56]: bell(n + 12, K['gestrichen'] + .02, .05, 2.2)   # Dissonanz bei „gestrichen“
# 3) Wendung: rückwärts gespielte Töne (Rückspulen), dann Glocke
for i, a in enumerate(np.arange(K['nicht'] - .2, K['tb0'] - .1, .06)):   # Rückspulen ab „nicht“ wie im Bild
    t = tt(.28); f = hz(86 - i % 7 * 3); x = np.sin(2 * np.pi * f * t) * np.exp(-(.28 - t) * 14) * np.clip((.28 - t) / .01, 0, 1)
    put(M, a, x * .045, -.5 + (i % 5) * .25)
bell(74, K['nicht'], .12, 3.2); bell(81, K['nicht'], .07, 3.2, .3)
# 4) Lösung: Puls 120 BPM, D-Dur – h-Moll – G – A
prog = [[50, 62, 66, 69], [47, 62, 66, 71], [43, 62, 67, 71], [45, 61, 64, 69]]
beat = .5; a = TB0 + .05; i = 0
while a < K['ende'] - .2:
    c = prog[(i // 4) % 4]
    kick(a, .28 if i % 2 == 0 else .18); hat(a + .25, .025)
    if i % 4 == 0: pad(c[1:], a, a + 2.1, .02); bass(c[0], a, 1.9, .16)
    else: bass(c[0], a, .4, .1)
    i += 1; a += beat
scale = [62, 64, 66, 67, 69, 71, 73, 74, 76, 78, 79, 81]
for i, a in enumerate(t_month): pluck(scale[i] + 12, a, .06, -.5 + i / 11, .45)          # Monats-Tore: Tonleiter aufwärts
for i, a in enumerate(t_q):
    for n in [62, 66, 69, 74 + i * 2]: pluck(n + 12, a, .045, 0, 1.0, .5)                   # Quartal: Akkord
# Glaswand -> heller Akkord, Maschine -> Groove bleibt, Schluss
for n in [50, 62, 66, 69, 74, 78]: pluck(n + 12, t_wall + .02, .05, 0, 1.6, .4)
pad([62, 66, 69, 74], K['ende'] - .3, DUR, .03, .6); bass(38, K['ende'] - .3, DUR - K['ende'], .14)
for n in [62, 66, 69, 74, 78]: bell(n + 12, K['erst'] - .05, .05, 3.0, -.3 + .15 * (n % 5))
for n in [50, 57, 62, 66, 69]: pluck(n + 12, K['kostenlos'] + .4, .05, 0, 2.5, .3)
M = reverb(M, 1.8, .25)

# ===== Effekte =====
# Linie summt (steigend) bis zum Tor
t = tt(t_gate); f = 90 + 60 * t / t_gate; put(S, 0, np.sin(2 * np.pi * np.cumsum(f) / SR) * .06 * np.clip(t / .1, 0, 1))
# Aufprall aufs Bescheid-Tor + Tonhöhensturz der Linie
t = tt(.6); put(S, t_gate, (np.sin(2 * np.pi * (60 + 80 * np.exp(-t * 20)) * t) * np.exp(-t * 6) + R.standard_normal(len(t)) * np.exp(-t * 40) * .3) * .5)
t = tt(.8); f = 420 * np.exp(-t * 3.2) + 40; put(S, t_gate + .05, np.tanh(2 * np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-t * 2.2) * .18)
# Rot flutet: dumpfer Schlag
t = tt(1.2); put(S, K['n14'] + .38, (np.sin(2 * np.pi * (42 + 30 * np.exp(-t * 12)) * t) * np.exp(-t * 3.5)) * .55)
# Uhr-Ticks je Wochen-Tor (Holzblock), letzter tiefer
for i, a in enumerate(t_weeks):
    t = tt(.12); f = [1900, 1700, 1500, 1100][i]; put(S, a, np.sin(2 * np.pi * f * t) * np.exp(-t * 60) * .16, .4 - i * .25)
# Treppe: vier Stufen-Schläge
for i, a in enumerate(t_stairs):
    t = tt(.3); put(S, a, np.sin(2 * np.pi * (110 - i * 12) * t) * np.exp(-t * 16) * .22 + R.standard_normal(len(t)) * np.exp(-t * 60) * .04)
# Polster läuft leer: fallender, gefilterter Ton
t = tt(.9); f = 330 * np.exp(-t * 1.6); put(S, K['weg'] - .05, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / .9) * .08)
# Maschine gestrichen: Metall-Klang + Strich
t = tt(1.0); put(S, K['gestrichen'] + .05, sum(np.sin(2 * np.pi * f * t) * np.exp(-t * d) for f, d in [(412, 5), (1033, 8), (1790, 11), (2477, 14)]) * .06, .3)
t = tt(.3); put(S, K['gestrichen'] + .15, lp(R.standard_normal(len(t)), 2500) * np.sin(np.pi * t / .3) * .12)
# Monats-Tore: Beleg landet (Papier-Klick)
for a in t_month:
    t = tt(.05); put(S, a - .02, lp(R.standard_normal(len(t)), 5000) * np.exp(-t * 120) * .08, .2)
# Hochrechnung je Quartal: kurzer aufsteigender Ton
for a in t_q:
    t = tt(.5); f = 600 + 900 * t / .5; put(S, a + .05, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / .5) * .04)
# Rücklage zählt hoch: 14 Münz-Ticks
t0, t1 = K['resA'], K['resZ']
for k in range(14):
    u = k / 13; a = t0 + (t1 - t0) * u
    t = tt(.15); put(S, a, (np.sin(2 * np.pi * 2637 * t) + .6 * np.sin(2 * np.pi * 3951 * t)) * np.exp(-t * 45) * .05, -.3 + .6 * (k % 2))
# Glaswand zerspringt: Glas-Partials + Splitter
t = tt(.5); put(S, t_wall, R.standard_normal(len(t)) * np.exp(-t * 14) * .25 + np.sin(2 * np.pi * 70 * t) * np.exp(-t * 10) * .3)
for k in range(40):
    a = t_wall + .02 + R.random() ** 2 * 1.4; f = 2500 + R.random() * 5000; t = tt(.35)
    put(S, a, np.sin(2 * np.pi * f * t) * np.exp(-t * (18 + R.random() * 20)) * (.05 + .05 * R.random()), R.random() * 2 - 1)
# Maschine läuft an: Motor fährt hoch
t = tt(1.6); f = 45 + 80 * (1 - np.exp(-t * 2.5)); m = np.tanh(3 * np.sin(2 * np.pi * np.cumsum(f) / SR)) + .3 * np.sin(2 * np.pi * np.cumsum(f * 4.02) / SR)
put(S, t_mach + .05, m * np.clip(t / .2, 0, 1) * np.clip((1.6 - t) / .5, 0, 1) * .08)
t = tt(.2); put(S, t_mach, sum(np.sin(2 * np.pi * f * t) for f in [880, 1320]) * np.exp(-t * 20) * .05)
S = reverb(S, 1.0, .15)
os.makedirs('out', exist_ok=True)
for name, buf, pk in [('musik', M, .6), ('sfx', S, .8)]:
    sf.write(f'out/{name}.wav', (buf / (np.abs(buf).max() + 1e-9) * pk).astype(np.float32), SR)
print('ok', round(t_gate, 2), [round(x, 2) for x in t_q], round(t_wall, 2), round(t_mach, 2))

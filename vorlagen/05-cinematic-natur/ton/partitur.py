#!/usr/bin/env python3
"""Sonnenhof Solar V4 – eigene Musik + Effekte (numpy, 48 kHz Stereo, liest out/zeiten.json).
Instrumente wie ein Naturfilm: gedämpftes Klavier, Streicherfläche, Zupfgitarre, Glas-Glocken.
Dramaturgie: Problem (e-Moll, Uhrticken des Zählers) -> Zeitraffer (je Tag ein Akkord-Atemzug) -> „Dabei scheint die Sonne“
(Aufhellung nach G-Dur, Vögel) -> Verwandlung (Glas-Glitzern) -> Takt der Montage (Zupf-Ostinato) -> Mittag (voll)
-> Abend (ruhig, Grillen) -> Rechnung sinkt (Auflösung) -> Schlussakkord.
Effekte nur, wo im Bild etwas passiert: Papier, Zählwerk, Blume dreht sich, Kerne -> Zellen, Stift, Module rasten ein,
Stempel, Transporter, Stromfluss, Speicher, Grillen, Glühwürmchen, Betrag rollt, Stempel, Angebot."""
import numpy as np, os, json, wave
class sf:  # schlanker Ersatz für soundfile (16-bit PCM)
    @staticmethod
    def write(fn, x, sr):
        x = np.clip(np.asarray(x), -1, 1); w = wave.open(fn, 'wb'); w.setnchannels(x.shape[1] if x.ndim > 1 else 1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((x * 32767).astype('<i2').tobytes()); w.close()
SR = 48000; Z = json.load(open('out/zeiten.json')); K = Z['K']; DUR = Z['DUR']; N = int(DUR * SR); R = np.random.default_rng(11)
M = np.zeros((N, 2)); S = np.zeros((N, 2))
def tt(d): return np.arange(int(round(d * SR))) / SR
def put(buf, a, x, pan=0.):
    i = int(a * SR)
    if i < 0: x = x[-i:]; i = 0
    x = x[:max(0, N - i)]; n = len(x)
    if n > 0: buf[i:i + n, 0] += x * np.cos((pan + 1) * np.pi / 4) * 1.41; buf[i:i + n, 1] += x * np.sin((pan + 1) * np.pi / 4) * 1.41
def reso(x, fc, q):
    w = 2 * np.pi * fc / SR; r = np.exp(-w / (2 * q)); c1, c2 = 2 * r * np.cos(w), -r * r; y = np.zeros(len(x)); y1 = y2 = 0.
    for i in range(len(x)): y0 = x[i] + c1 * y1 + c2 * y2; y[i] = y0; y2, y1 = y1, y0
    return y / (np.abs(y).max() + 1e-9)
def nz(d, fc, q=2): return reso(R.standard_normal(int(round(d * SR))), fc, q)
def reverb(x, sec, mix):
    n = int(sec * SR); ir = R.standard_normal((n, 2)) * np.exp(-np.arange(n) / SR * 6 / sec)[:, None]; F = 1 << int(np.ceil(np.log2(len(x) + n))); out = np.zeros_like(x)
    for c in range(2): out[:, c] = np.fft.irfft(np.fft.rfft(x[:, c], F) * np.fft.rfft(ir[:, c], F), F)[:len(x)]
    out *= np.abs(x).max() / (np.abs(out).max() + 1e-9); return x * (1 - mix) + out * mix
def hz(n): return 440 * 2 ** ((n - 69) / 12)
def piano(n, a, d=2.8, amp=.18, pan=0, soft=1.):
    t = tt(d); f = hz(n); x = sum(np.sin(2 * np.pi * f * k * t * (1 + .0003 * k * k)) * np.exp(-t * (1.2 + k * (1.1 + soft))) / k ** 1.6 for k in range(1, 7))
    put(M, a, x * np.clip(t / .006, 0, 1) * amp, pan)
def guitar(n, a, amp=.07, pan=0):  # Karplus-Strong
    f = hz(n); p = int(SR / f); d = 1.6; buf = R.uniform(-1, 1, p); out = np.zeros(int(d * SR))
    for i in range(len(out)): out[i] = buf[i % p]; buf[i % p] = .5 * (buf[i % p] + buf[(i + 1) % p]) * .996
    put(M, a, out * amp, pan)
def strings(ns, a, b, amp=.025, att=1.0, rel=1.0):
    t = tt(b - a); e = np.clip(t / att, 0, 1) * np.clip((b - a - t) / rel, 0, 1); vib = 1 + .003 * np.sin(2 * np.pi * 5 * t)
    for i, n in enumerate(ns):
        f = hz(n); ph = 2 * np.pi * np.cumsum(f * vib) / SR; x = np.sin(ph) + .3 * np.sin(2 * ph) + .15 * np.sin(3 * ph)
        put(M, a, x * e * amp, -.6 + 1.2 * i / max(1, len(ns) - 1))
def glass(n, a, amp=.05, pan=0, d=2.5):
    t = tt(d); f = hz(n); put(M, a, (np.sin(2 * np.pi * f * t) + .3 * np.sin(2 * np.pi * f * 3.01 * t) * np.exp(-t * 4)) * np.exp(-t * 2.2) * np.clip(t / .003, 0, 1) * amp, pan)
def bass(n, a, d, amp=.12):
    t = tt(d); f = hz(n); put(M, a, (np.sin(2 * np.pi * f * t) + .15 * np.sin(4 * np.pi * f * t)) * np.clip(t / .02, 0, 1) * np.clip((d - t) / .1, 0, 1) * amp)

# 1) Problem: e-Moll, tiefe Klaviertöne, Zählerticken
strings([52, 55, 59], 0, K['jedes'] + .4, .018, att=.4)
for a, n in [(K['schon'], 40), (K['strom'], 52), (K['steigt'], 47)]: piano(n, a, 3, .18)
# 2) Zeitraffer: je Tag ein Akkord-Atemzug, steigend
days = [K['jahr'], K['hunderte'], K['mehr'], K['dabei'] - .3]   # V7: Akkord auf jedem Betragssprung
for i, a in enumerate(days[:-1]):
    ch = [[40, 52, 55, 59], [41, 53, 57, 60], [43, 55, 58, 62]][i]; strings(ch[1:], a, days[i + 1] + .3, .02, att=.35, rel=.35); bass(ch[0], a, days[i + 1] - a, .1); piano(ch[3] + 12, a, 1.5, .07)
# 3) Wendung: G-Dur, Klaviermotiv
strings([55, 59, 62, 67], K['dabei'] - .1, K['sonnenhof'] + .3, .022)
for d, n in [(0, 67), (.3, 71), (.6, 74), (1.2, 72), (1.5, 71), (1.8, 74)]: piano(n, K['dabei'] + d, 2.2, .08, .2)
# 4) Verwandlung: Glas-Arpeggio
for i, n in enumerate([79, 83, 86, 91, 95, 98]): glass(n, K['sonnenhof'] + .6 + i * .12, .035, -.5 + .2 * i)
strings([55, 62, 67, 71], K['sonnenhof'] - .1, K['planung'] + .2, .02)
# 5) Montage-Takt: Zupf-Ostinato G – D – Em – C, 112 BPM
B = 60 / 112; a = K['planung'] - .05; i = 0; prog = [[43, 55, 59, 62], [38, 57, 62, 66], [40, 55, 59, 64], [36, 55, 60, 64]]
while a < DUR - 1.3:
    c = prog[(i // 4) % 4]; dusk = K['speicher'] < a < K['rechnung'] - .3
    if i % 4 == 0: bass(c[0], a, B * 3.9, .1 if not dusk else .07); strings([n + 12 for n in c[1:]], a, a + B * 4 + .3, .012 if not dusk else .016, att=.3)
    if not dusk or i % 2 == 0: guitar(c[1 + i % 3] + 12, a, .06 if not dusk else .04, -.3 + .3 * (i % 3)); guitar(c[1 + (i + 1) % 3] + 12, a + B / 2, .04, .3)
    i += 1; a += B
for n in [55, 59, 62, 67]: piano(n + 12, K['sonnenstrom'], 2.5, .06)
for n in [52, 59, 64, 67]: piano(n + 12, K['abend'], 3, .06)
# 6) Rechnung sinkt: absteigende Linie, dann Auflösung
for d, n in [(0, 79), (.25, 76), (.5, 74), (.75, 71), (1.0, 67)]: piano(n, K['sinkt'] + d, 2, .07, -.2)
for n in [43, 55, 59, 62, 67, 71]: piano(n, K['siebzig'] + .05, 3, .08)
for n in [43, 50, 55, 59, 62, 67, 74]: piano(n, K['kostenlos'] + .4, 3.2, .085)
M = reverb(M, 2.4, .3)

# ---------- Effekte ----------
t = tt(.6); put(S, .05, np.sin(2 * np.pi * np.cumsum(1400 + 900 * np.exp(-t * 18)) / SR) * np.exp(-t * 9) * .04, .3)   # V5: Tautropfen statt Papier
tk = K['strom'] - .1
while tk < K['steigt'] + .3: t = tt(.03); put(S, tk, nz(.03, 5200, 4) * np.exp(-t * 150) * .05, .4); tk += .06   # Zählwerk
t = tt(.25); put(S, K['steigt'] - .05, np.sin(2 * np.pi * np.cumsum(500 + 700 * t / .25) / SR) * np.exp(-t * 6) * .05, .4)   # Pfeil
# Zeitraffer: je Tag ein Vogelruf am Morgen / eine Grille in der Nacht
for i, a in enumerate(days[:-1]):
    t = tt(.18); put(S, a + .25, np.sin(2 * np.pi * np.cumsum(3200 + 900 * np.sin(2 * np.pi * 14 * t)) / SR) * np.sin(np.pi * t / .18) * .02, .6 - .4 * i)
# Morgen: Vögel, Blume dreht sich (Blätterrascheln)
def bird(a, f0=3400, amp=.025, pan=0):
    for k in range(3):
        t = tt(.09); f = f0 * (1 + .25 * np.sin(np.pi * t / .09)); put(S, a + k * .11, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / .09) * amp, pan)
for a, f, p in [(K['dabei'], 3600, .6), (K['sonne'] + .4, 4100, -.5), (K['jeden'] + .5, 3300, .7), (K['dach'] + .4, 3900, -.3)]: bird(a, f, .025, p)
t = tt(.8); put(S, K['sonne'] - .2, nz(.8, 2200, .7) * np.sin(np.pi * t / .8) * .05, -.4)
# Hitzeflimmern auf dem leeren Dach
t = tt(1.1); put(S, K['dach'], nz(1.1, 900, 6) * np.sin(np.pi * t / 1.1) * .02, .3)
# Kerne -> Zellen: gläsernes Flirren
t = tt(1.0); put(S, K['sonnenhof'] + .6, sum(np.sin(2 * np.pi * f * t) for f in [2637, 3136, 3951]) * np.sin(np.pi * t / 1) * .01)
# Planung: Stiftstriche
for k in range(2): t = tt(.45); put(S, K['planung'] + k * .2, nz(.45, 4200, 3) * (.5 + .5 * np.sin(2 * np.pi * 22 * t)) * np.sin(np.pi * t / .45) * .04, -.2 + .4 * k)
# Montage: Module rasten ein (V5: 24 Module, synchron zum Bild)
for n in range(24):
    a = K['montage'] - .12 + n * .033; t = tt(.08); put(S, a, (np.sin(2 * np.pi * 1900 * t) * np.exp(-t * 90) + nz(.08, 3000, 3) * np.exp(-t * 120) * .5) * .05, -.6 + .06 * (n % 7) * 2)
# Anmeldung: Stempel
t = tt(.4); put(S, K['anmeldung'] + .05, (np.sin(2 * np.pi * (80 + 50 * np.exp(-t * 30)) * t) * np.exp(-t * 10) + nz(.4, 900, 2) * np.exp(-t * 40) * .4) * .18, .5)
# Transporter fährt vorbei
d = K['tags'] - K['alles'] + .2; t = tt(d); e = np.sin(np.pi * t / d); f = 60 + 10 * np.sin(2 * np.pi * .7 * t)
put(S, K['alles'] + .1, (np.sin(2 * np.pi * np.cumsum(f) / SR) * .5 + nz(d, 250, 1) * .5) * e * .06, 0)
# Mittag: Stromfluss summt, Waschmaschine
t = tt(K['speicher'] - K['tags']); d = len(t) / SR; e = np.clip(t / .4, 0, 1) * np.clip((d - t) / .4, 0, 1)
put(S, K['tags'] + .2, (np.sin(2 * np.pi * 220 * t) * .5 + np.sin(2 * np.pi * 330 * t) * .3) * (.6 + .4 * np.sin(2 * np.pi * 3 * t)) * e * .02, .2)
put(S, K['tags'] + .3, nz(d, 300, 2) * (.5 + .5 * np.sin(2 * np.pi * 2.2 * t)) * e * .03, -.5)
# Speicher: steigender Ladeton, beim Entladen fallend
t = tt(1.0); put(S, K['speicher'] - .3, np.sin(2 * np.pi * np.cumsum(330 + 330 * t) / SR) * np.sin(np.pi * t) * .025, .5)
t = tt(1.2); put(S, K['abend'] - .1, np.sin(2 * np.pi * np.cumsum(660 - 260 * t / 1.2) / SR) * np.sin(np.pi * t / 1.2) * .02, .5)
# Lampe an
t = tt(.1); put(S, K['abend'] - .2, nz(.1, 2500, 5) * np.exp(-t * 60) * .08, .1)
# Grillen + Glühwürmchen
for k in range(12):
    a = K['abend'] - .2 + k * .17; t = tt(.08); put(S, a, np.sin(2 * np.pi * 4500 * t) * (np.sin(2 * np.pi * 50 * t) > 0) * np.exp(-t * 20) * .012, .7 if k % 2 else -.7)
for k in range(8): glass(96 + (k * 5) % 7, K['abend'] + .2 + k * .12, .012, R.uniform(-.8, .8), 1.0)
# Morgen: Betrag rollt nach unten, Stempel -70 %
tk = K['sinkt'] - .1
while tk < K['siebzig'] + .2: t = tt(.03); put(S, tk, nz(.03, 4200, 4) * np.exp(-t * 150) * .05, .4); tk += .055
t = tt(.5); put(S, K['siebzig'] + .08, (np.sin(2 * np.pi * (75 + 60 * np.exp(-t * 30)) * t) * np.exp(-t * 8) + nz(.5, 800, 2) * np.exp(-t * 40) * .5) * .22, .3)
bird(K['rechnung'] - .2, 3700, .02, .7)
# Angebot
t = tt(.15); put(S, K['check'] - .05, np.sin(2 * np.pi * 1568 * t) * np.exp(-t * 25) * .05)
S = reverb(S, 1.0, .12)
os.makedirs('out', exist_ok=True)
for name, buf, pk in [('musik', M, .6), ('sfx', S, .8)]:
    sf.write(f'out/{name}.wav', (buf / (np.abs(buf).max() + 1e-9) * pk).astype(np.float32), SR)
print('ok', DUR)

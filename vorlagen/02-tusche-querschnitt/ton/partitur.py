#!/usr/bin/env python3
"""Grünwerk Gartenbau V4 (V6: drei Effekte ergänzt) – eigene Musik + Effekte (numpy, 48 kHz Stereo, liest out/zeiten.json).
Instrumente wie die Tuschezeichnung: gezupfte Gitarre (Karplus-Strong), Holz-Marimba, Glockenspiel.
Dramaturgie: Regen/Hitze (a-Moll, spärlich, Regenrauschen) -> unter die Oberfläche (tiefe Töne, Stille)
-> Grünwerk baut Schicht für Schicht (C-Dur, Zupf-Ostinato, jede Schicht ein neuer Ton) -> Wurzeln wachsen (aufsteigende Marimba)
-> Rasen grün, Kind kickt (voller, leichter Groove) -> Schlussakkord.
Effekte nur, wo im Bild etwas passiert: Regen, Tropfen in der Pfütze, Zikaden-Hitze, Scheibe, Zinken im Boden,
Krümel, Kies prasselt, Erde rieselt, Wasser läuft ab, Tropfen versickern, Kick, Vögel, Schild aus Holz."""
import numpy as np, soundfile as sf, json
SR = 48000; Z = json.load(open('out/zeiten.json')); DUR = Z['DUR']; K = Z['K']; N = int(DUR * SR); R = np.random.default_rng(23)
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
def guitar(n, a, d=2.0, amp=.12, pan=0, bright=.5):  # Karplus-Strong
    f = hz(n); L = int(SR / f); buf = R.uniform(-1, 1, L); out = np.zeros(int(d * SR)); dec = .996 - (1 - bright) * .004
    for i in range(len(out)):
        out[i] = buf[i % L]; buf[i % L] = dec * .5 * (buf[i % L] + buf[(i + 1) % L])
    put(M, a, out * amp, pan)
def marimba(n, a, amp=.1, pan=0):
    t = tt(1.0); f = hz(n); x = (np.sin(2 * np.pi * f * t) + .35 * np.sin(2 * np.pi * f * 3.9 * t) * np.exp(-t * 18)) * np.exp(-t * 5)
    put(M, a, x * np.clip(t / .002, 0, 1) * amp, pan)
def glock(n, a, amp=.05, pan=0):
    t = tt(1.6); f = hz(n); x = (np.sin(2 * np.pi * f * t) + .4 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 6)) * np.exp(-t * 2.5); put(M, a, x * amp, pan)
def cello(n, a, d, amp=.05):
    t = tt(d); f = hz(n); vib = 1 + .004 * np.sin(2 * np.pi * 5 * t); ph = 2 * np.pi * np.cumsum(f * vib) / SR
    x = sum(np.sin(k * ph) / k ** 1.2 for k in range(1, 6)); e = np.clip(t / .4, 0, 1) * np.clip((d - t) / .5, 0, 1); put(M, a, x * e * amp)
def shaker(a, amp=.02, pan=.3):
    t = tt(.09); put(M, a, nz(.09, 6500, 1) * np.sin(np.pi * t / .09) * amp, pan)
B = 60 / 104
# 1) Regen + Sommer: a-Moll, spärliche Zupftöne, Cello-Liegeton
cello(45, .1, K['grund'] + .3, .045)
for a, n in [(.3, 57), (.9, 60), (1.5, 64), (K['unter'], 62), (K['wasser'], 60), (K['sommer'], 57), (K['braun'], 53), (K['kinder'], 52), (K['drinnen'] + .7, 57)]: guitar(n, a, 2.0, .11, -.2)
for a in [K['wasser'] + .4, K['braun'] + .3, K['drinnen'] + .8]: guitar(45, a, 2.2, .1, .1)
# 2) Unter die Oberfläche: tiefe Töne
for n, d in [(33, 0), (40, .3)]: cello(n, K['grund'] - .2 + d, 2.8, .06)
glock(76, K['verdichtet'], .03); guitar(40, K['verdichtet'], 2.5, .12)
# 3) Schicht für Schicht: C – G – a – F, Zupf-Ostinato
prog = [[48, 60, 64, 67], [43, 59, 62, 67], [45, 60, 64, 69], [41, 60, 65, 69]]
a = K['gw'] - .05; i = 0
while a < K['wurzeln'] - .1:
    c = prog[(i // 4) % 4]
    if i % 4 == 0: guitar(c[0], a, 2.4, .1, 0)
    for j, n in enumerate([c[1], c[2], c[3], c[2]]): guitar(n + 12, a + j * B / 4, .7, .05, -.4 + .27 * j, .3)
    if i % 2 == 1: shaker(a + B / 2)
    i += 1; a += B
for k, n in [('lockert', 72), ('n30', 76), ('kies', 74), ('ab', 72), ('mutter', 79), ('kompost', 77)]: glock(n, K[k], .04)
# 4) Wurzeln wachsen: aufsteigende Marimba
for i, n in enumerate([48, 52, 55, 60, 64, 67, 72, 76, 79, 84]): marimba(n, K['wurzeln'] + i * .22, .08, -.5 + i * .1)
guitar(36, K['wurzeln'], 3.0, .1); guitar(43, K['versickert'], 2.5, .08)
# 5) Rasen grün: F – C – G – C, leichter Groove mit Marimba + Gitarre
prog2 = [[41, 65, 69, 72], [36, 64, 67, 72], [43, 62, 67, 71], [36, 64, 67, 72]]
a = K['rasen2'] - .15; i = 0
while a < K['kostenlos'] + .3:
    c = prog2[(i // 2) % 4]
    if i % 2 == 0: guitar(c[0], a, 1.8, .11, 0)
    marimba(c[1 + i % 3], a, .07, -.3); marimba(c[1 + (i + 1) % 3] + 12, a + B / 2, .05, .3); shaker(a + B / 2, .025); shaker(a + B / 4, .012, -.3)
    i += 1; a += B
for n in [36, 48, 55, 60, 64, 67, 72]: guitar(n, K['kostenlos'] + .5, 3.0, .08, 0)
glock(84, K['kostenlos'] + .5, .04)
M = reverb(M, 1.6, .2)

# --- Effekte ---
rain = np.zeros(int((K['sommer'] + .4) * SR)); rain = nz(len(rain) / SR, 4000, .7) * .5 + nz(len(rain) / SR, 900, .7) * .5
env = np.clip(np.arange(len(rain)) / SR / .3, 0, 1) * np.clip((len(rain) / SR - np.arange(len(rain)) / SR) / .5, 0, 1); put(S, 0, rain * env * .05, -.1)
for i in range(22):
    a = .2 + R.random() * (K['sommer'] - .3); t = tt(.12); f = 900 + R.random() * 900; put(S, a, np.sin(2 * np.pi * np.cumsum(f * (1 + t * 6)) / SR) * np.exp(-t * 40) * .05, R.uniform(-.6, .6))  # Tropfen in die Pfütze
# Hitze: Zikaden
t = tt(K['kinder'] - K['sommer'] + .2); z = np.sin(2 * np.pi * 4800 * t) * (0.5 + .5 * np.sign(np.sin(2 * np.pi * 42 * t))) * (0.6 + .4 * np.sin(2 * np.pi * .8 * t)); e = np.clip(t / .6, 0, 1) * np.clip((t[-1] - t) / .4, 0, 1); put(S, K['sommer'], z * e * .012, .4)
# V6: Rasen vertrocknet auf „braun“ – trockenes Knistern
for i in range(26): t = tt(.03); put(S, K['braun'] - .38 + i * .018 + R.random() * .015, nz(.03, 3000 + R.random() * 3000, 5) * np.exp(-t * 120) * .05, -.6 + i * .045)
# V6: Grabegabel kommt von oben ins Bild (Luftzug)
t = tt(.45); put(S, K['gw'] - .5, nz(.45, 1200, .8) * np.sin(np.pi * t / .45) ** 2 * .05, .2)
# V6: Anhänger „kostenlos“ dreht sich ins Bild (Karton-Flip)
t = tt(.08); put(S, K['kostenlos'] - .12, nz(.08, 2400, 3) * np.exp(-t * 60) * .07, -.4)
# Kind an der Scheibe: zwei leise Klopfer auf Glas
for d in [0, .18]: t = tt(.15); put(S, K['kinder'] + .5 + d, (np.sin(2 * np.pi * 2300 * t) + np.sin(2 * np.pi * 3700 * t)) * np.exp(-t * 40) * .04, -.4)
# Hinab: tiefes Rumpeln der Erde
t = tt(1.0); put(S, K['grund'] - .2, nz(1.0, 120, 1.5) * np.sin(np.pi * t / 1.0) * .12)
# Verdichten: Pressen
t = tt(.6); put(S, K['verdichtet'], (nz(.6, 200, 2) * .7 + np.sin(2 * np.pi * 55 * t) * .3) * np.exp(-t * 5) * .2)
# Zinken stechen ein (Metall + Erde), Krümel
t = tt(.4); put(S, K['lockert'] + .05, (np.sin(2 * np.pi * 620 * t) * np.exp(-t * 18) * .3 + nz(.4, 700, 2) * np.exp(-t * 9)) * .2, .3)
for i in range(16): t = tt(.05); put(S, K['lockert'] + .3 + i * .06 + R.random() * .03, nz(.05, 900 + R.random() * 900, 4) * np.exp(-t * 80) * .06, R.uniform(-.5, .5))
# Kies prasselt
for i in range(60): t = tt(.04); put(S, K['kies'] - .25 + i * .018 + R.random() * .02, nz(.04, 2500 + R.random() * 3000, 6) * np.exp(-t * 110) * .07, R.uniform(-.7, .7))
# Wasser läuft ab (Gurgeln)
t = tt(1.4); g = sum(np.sin(2 * np.pi * (300 + 200 * np.sin(2 * np.pi * (3 + k) * t)) * t) for k in range(3)) / 3; put(S, K['ab'] - .5, g * np.sin(np.pi * t / 1.4) * .03, .3)
# Erde rieselt
t = tt(1.8); put(S, K['mutter'] - .6, nz(1.8, 3200, .8) * np.sin(np.pi * t / 1.8) * .05, -.2)
# Tropfen versickern
for i in range(14): t = tt(.1); put(S, K['versickert'] - .4 + i * .14, np.sin(2 * np.pi * (1400 - i * 30) * t) * np.exp(-t * 35) * .035, R.uniform(-.5, .5))
# Kick + Ball
t = tt(.25); put(S, K['gruen'] + .1, (np.sin(2 * np.pi * (140 * np.exp(-t * 12) + 60) * t) * np.exp(-t * 14) + nz(.25, 1500, 2) * np.exp(-t * 40) * .3) * .3, .1)
# Vögel in der guten Welt
for i in range(6):
    a = K['rasen2'] + .4 + i * .6 + R.random() * .2; t = tt(.18); f = 3200 + 900 * np.sin(2 * np.pi * 14 * t); put(S, a, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / .18) * .02, R.uniform(-.8, .8))
# Schild aus Holz steigt, setzt auf
t = tt(.3); put(S, K['ende'] + .55, (np.sin(2 * np.pi * 180 * t) + .5 * np.sin(2 * np.pi * 420 * t)) * np.exp(-t * 22) * .15)
t = tt(.3); put(S, K['probe'], np.sin(2 * np.pi * 1318 * t) * np.exp(-t * 10) * .04)
S = reverb(S, .8, .12)
for name, buf, pk in [('musik', M, .6), ('sfx', S, .8)]:
    sf.write(f'out/{name}.wav', (buf / (np.abs(buf).max() + 1e-9) * pk).astype(np.float32), SR)
print('ok')

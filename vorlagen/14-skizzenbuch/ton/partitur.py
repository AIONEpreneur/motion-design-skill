#!/usr/bin/env python3
"""Lernwerk Nachhilfe V4 – eigene Musik + Effekte. Instrumente passend zum Skizzenbuch: Klavier, Glockenspiel, Pizzicato, Holzblock.
Dramaturgie: Problem (d-Moll, Uhr tickt, sparsam) -> Wendung „Dabei“ (Stille, ein Glockenton) -> Lösung (F-Dur, Pizzicato-Ostinato,
Holzblöcke rasten ein) -> „eine Drei“ (Aufhellung) -> „wieder gern“ + Marke (voller, leichter Takt) -> Schlussakkord.
Effekte nur, wo im Bild etwas passiert: Blatt landet, Rotstift, Umblättern, Uhr, Sprechblasen, Stufe knarrt, Bausteine klacken, Lupe, Filzstift-Kreise."""
import numpy as np, soundfile as sf, os, json
SR = 48000; Z = json.load(open('out/zeiten.json')); K = Z['K']; DUR = Z['DUR']; N = int(DUR * SR); R = np.random.default_rng(14)
M = np.zeros((N, 2)); S = np.zeros((N, 2))
def tt(d): return np.arange(int(d * SR)) / SR
def put(buf, a, x, pan=0.):
    i = int(a * SR)
    if i < 0: x = x[-i:]; i = 0
    n = min(len(x), N - i)
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
def glock(n, a, amp=.06, pan=0):  # Glockenspiel: unharmonische Teiltöne, lang
    t = tt(2.2); f = hz(n); x = np.sin(2 * np.pi * f * t) * np.exp(-t * 2.2) + .4 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 6) + .2 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 11)
    put(M, a, x * np.clip(t / .001, 0, 1) * amp, pan)
def pizz(n, a, amp=.06, pan=0):
    t = tt(.6); f = hz(n); x = (np.sin(2 * np.pi * f * t) + .35 * np.sin(4 * np.pi * f * t) + .15 * np.sin(6 * np.pi * f * t)) * np.exp(-t * 9)
    put(M, a, x * np.clip(t / .004, 0, 1) * amp, pan)
def pad(ns, a, b, amp=.025):
    t = tt(b - a); e = np.clip(t / 1.0, 0, 1) * np.clip((b - a - t) / .8, 0, 1)
    for i, n in enumerate(ns): f = hz(n); put(M, a, (np.sin(2 * np.pi * f * t) + .6 * np.sin(2 * np.pi * f * 1.004 * t + 1)) * .5 * e * amp, -.5 + i / max(1, len(ns) - 1))
def bass(n, a, d, amp=.14):
    t = tt(d); f = hz(n); x = np.sin(2 * np.pi * f * t) + .2 * np.sin(4 * np.pi * f * t); put(M, a, x * np.clip(t / .01, 0, 1) * np.clip((d - t) / .05, 0, 1) * np.exp(-t * 1.2) * amp)
def shaker(a, amp=.02):
    t = tt(.08); put(M, a, nz(.08, 7000, 1.5) * np.exp(-t * 60) * amp, .3)
def softkick(a, amp=.18):
    t = tt(.3); ph = 2 * np.pi * np.cumsum(50 + 60 * np.exp(-t * 35)) / SR; put(M, a, np.sin(ph) * np.exp(-t * 12) * amp)
B = .625  # 96 BPM
# 1) Problem: d-Moll, sparsame tiefe Klavier-Töne auf den Schlüsselwörtern, Uhr-Puls
pad([50, 53, 57], .1, K['dabei'] - .2, .02)
for a, ns in [(K['fuenf'], [38, 50, 53]), (K['mathe'], [57]), (K['wieder'], [55, 46]), (K['streit'], [46, 53, 58]), (K['versetzung'], [43, 50, 55]), (K['wackelt'], [45, 52, 61])]:
    for n in ns: piano(n, a, 2.6, .15)
a = K['abend'] - .3
while a < K['dabei'] - .5: bass(38, a, B * .9, .09); a += B * 2
# 2) Wendung „Dabei“: kurzer Atem, ein heller Glockenton
glock(81, K['dabei'] + .05, .07); glock(76, K['dabei'] + .05, .05)
# 3) Lösung: F-Dur – C – d – B, Pizzicato-Achtel
prog = [[41, 65, 69, 72], [36, 64, 67, 72], [38, 65, 69, 74], [34, 65, 70, 74]]
a = K['lernwerk'] - .05; i = 0
while a < K['eine3'] - .1:
    c = prog[(i // 4) % 4]
    if i % 4 == 0: pad(c[1:], a, a + B * 4 + .3, .016); bass(c[0], a, B * 1.9, .11)
    pizz(c[1 + i % 3], a, .05, -.3); pizz(c[1 + (i + 1) % 3] + 12, a + B / 2, .035, .3)
    if a > K['dann'] - .2: shaker(a + B / 2, .018)
    i += 1; a += B
# 4) „eine Drei“: Aufhellung
for n in [53, 60, 65, 69, 72, 77]: piano(n, K['eine3'], 3.0, .09)
glock(84, K['eine3'] + .1, .06)
# 5) wieder gern + Marke: leichter Takt
a = K['kind2']; i = 0; prog2 = [[41, 65, 69, 72], [34, 62, 65, 70], [36, 64, 67, 72], [41, 65, 69, 72]]
while a < K['probe2'] + .6:
    c = prog2[(i // 4) % 4]
    if i % 2 == 0: softkick(a, .16)
    if i % 4 == 0: pad(c[1:], a, a + B * 4 + .3, .018); bass(c[0], a, B * 1.9, .12)
    pizz(c[1 + i % 3] + 12, a, .045, -.3 + .3 * (i % 3)); shaker(a + B / 2, .02)
    i += 1; a += B
for n in [41, 53, 60, 65, 69, 72]: piano(n, K['probe2'] + .8, 3.0, .11)
glock(89, K['probe2'] + .8, .05)
M = reverb(M, 2.0, .25)

# --- Effekte (Papier, Stift, Holz) ---
def paper(a, d=.35, amp=.08, pan=0):  # Blatt gleitet / landet
    t = tt(d); put(S, a, nz(d, 2600, .9) * np.sin(np.pi * t / d) ** 2 * amp, pan)
def slap(a, amp=.18):
    t = tt(.25); put(S, a, (nz(.25, 1100, 1.2) * np.exp(-t * 40) + np.sin(2 * np.pi * 120 * t) * np.exp(-t * 35) * .5) * amp)
def scribble(a, d, amp=.05, rate=9, fc=3800, pan=.2):  # Stift auf Papier
    t = tt(d); env = (.5 + .5 * np.sin(2 * np.pi * rate * t + R.random() * 6)) ** 2 * np.clip(t / .03, 0, 1) * np.clip((d - t) / .05, 0, 1)
    put(S, a, nz(d, fc, 3) * env * amp, pan)
def turnfx(a, amp=.11):  # Umblättern: Rascheln + Schnapp
    t = tt(.6); put(S, a, nz(.6, 3000, .7) * np.sin(np.pi * t / .6) ** 1.5 * (1 + .6 * np.sin(2 * np.pi * 14 * t)) * amp * .6, -.3)
    t2 = tt(.12); put(S, a + .5, nz(.12, 1800, 1.5) * np.exp(-t2 * 50) * amp, .3)
def clack(a, amp=.2, f=900, pan=0):  # Holzbaustein
    t = tt(.2); put(S, a, (np.sin(2 * np.pi * f * t) * np.exp(-t * 45) + .6 * np.sin(2 * np.pi * f * 2.3 * t) * np.exp(-t * 70) + nz(.2, 2500, 2) * np.exp(-t * 90) * .4) * amp, pan)
def tick(a, amp=.05): t = tt(.03); put(S, a, np.sin(2 * np.pi * 3200 * t) * np.exp(-t * 300) * amp, .5)
def pop(a, amp=.08, f=500, pan=0): t = tt(.15); put(S, a, np.sin(2 * np.pi * np.cumsum(f + 900 * t / .15) / SR) * np.exp(-t * 30) * amp, pan)
T = [K['abend'] - .6, K['dabei'] - .48, K['dann'] - .42, K['kind2'] - .36, K['marke'] - .66]  # V5: Überblendungen der Tafeln
# Szene 1
paper(K['kind'] - .53, .4, .08, -.2); slap(K['kind'] - .13, .2)
for i in range(3): scribble(.35 + i * .22, .22, .05, 14, 4200, .1)
scribble(K['fuenf'] - .36, .75, .09, 7, 3000, .1)                    # Rotstift zieht die Fünf
for i in range(2): paper(K['wieder'] - .52 + i * .16, .4, .07, .5); slap(K['wieder'] - .18 + i * .18, .1)  # V7: Blätter landen bis „wieder“
for k in ['mathe', 'wieder']: scribble(K[k] - .35, .4, .03, 11, 5000, .4)
for a in T: turnfx(a)
# Szene 2: Uhr tickt, wird schneller (Abend für Abend), Sprechblasen, Stufe knarrt + Riss
a = K['abend']; step = .5
while a < K['versetzung'] - .3: tick(a, .045); a += step; step = max(.12, step * .9)
pop(K['streit'], .09, 380, .3); pop(K['streit'] + .28, .08, 520, -.3)
for i in range(2): t = tt(.35); put(S, K['streit'] + .05 + i * .3, nz(.35, 700, 6) * (.5 + .5 * np.sign(np.sin(2 * np.pi * 22 * t))) * np.exp(-t * 6) * .05, .3 - .6 * i)
t = tt(.9); f = 90 * (1 - .35 * t / .9); put(S, K['versetzung'] - .35, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / .9) * .07)  # Rausfahren: tonales Absinken
for i in range(3): clack(K['versetzung'] - .12 + i * .09, .09, 300 + i * 60)
t = tt(.8); put(S, K['wackelt'], nz(.8, 420, 12) * (.5 + .5 * np.sin(2 * np.pi * 11 * t)) * np.sin(np.pi * t / .8) * .1, .4)  # Knarren
t = tt(.3); put(S, K['wackelt'] + .05, nz(.3, 2200, 2) * np.exp(-t * 25) * .12, .4)                                          # Riss
# Szene 3: Bausteine fallen und klacken, Lücke, Lupe, Baustein rastet ein
for i in range(5): clack(K['dabei'] - .2 + i * .07, .14, 700 + i * 70, -.4 + i * .2)  # V5: Pyramide steht beim Wort
t = tt(.6); put(S, K['fehlt'], (np.sin(2 * np.pi * 196 * t) + np.sin(2 * np.pi * 207 * t)) * np.exp(-t * 5) * .05)  # Lücke: schiefer Ton
paper(K['lernwerk'] - .15, .5, .04, .6)
t = tt(1.2); put(S, K['luecke'], np.sin(2 * np.pi * 2093 * t) * np.exp(-t * 4) * .05, -.2)                              # Lupe: Glas-Ping
clack(K['probe'] - .35, .3, 620); glock(88, K['probe'] - .33, .05)  # V5: Stein rastet in die Lücke
clack(K['probe'] + .55 + .17, .18, 820)
for k in ['fehlt', 'lernwerk', 'probe']: scribble(K[k] - .3, .35, .03, 11, 5000, .4)  # V7: Kringel um die Lücke, Name am Lupengriff, Banderole
# Szene 4: Filzstift-Kreise, Kinder setzen sich, Kurve steigt, grüne Drei
for i in range(5): tick(K['dann'] - .25 + i * .06, .03)
scribble(K['zweimal'] - .3, .3, .07, 6, 3400, .2); scribble(K['zweimal'] + .05, .4, .07, 6, 3400, .4)
for i in range(3): pop(K['drei'] - .36 + i * .15, .07, 600 + i * 150, -.4 + .4 * i)
t = tt(max(.3, K['eine3'] - K['acht'])); put(S, K['acht'], nz(len(t) / SR, 4500, 3) * .025 * (.6 + .4 * np.sin(2 * np.pi * 8 * t)))
for i in range(8): pizz(72 + [0, 2, 4, 5, 7, 9, 11, 12][i], K['acht'] + i * (K['eine3'] - K['acht']) / 8, .03, .3)
paper(K['eine3'] - .5, .3, .07, .6); slap(K['eine3'] - .22, .12); scribble(K['eine3'] - .3, .5, .08, 7, 3000, .3)
paper(K['nach'] - .5, .45, .03, -.4)  # V5: Kamerafahrt über das Blatt
# Szene 5 + 6
scribble(K['rechnet'] - .3, .6, .04, 12, 4500, -.2)
t = tt(.25); put(S, K['gern'], np.sin(2 * np.pi * 1568 * t) * np.exp(-t * 14) * .05)
for i in range(3): clack(K['marke'] - .2 + i * .1, .15, 760 + i * 90, -.3 + .3 * i)
scribble(K['marke'] - .36, .5, .04, 10, 4500, .2)
pop(K['kostenlos2'] - .3, .09, 450)  # V7: Banderole rollt aus
scribble(K['acht'] - .3, .3, .03, 10, 4500, .1); scribble(K['gruppe'] - .3, .3, .03, 10, 4500, .3)  # V7: „8 Wochen“, „max. 3“
S = reverb(S, .8, .12)
os.makedirs('out', exist_ok=True)
for name, buf, pk in [('musik', M, .6), ('sfx', S, .8)]:
    sf.write(f'out/{name}.wav', (buf / (np.abs(buf).max() + 1e-9) * pk).astype(np.float32), SR)
print('ok')

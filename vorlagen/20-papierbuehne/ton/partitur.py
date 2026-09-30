#!/usr/bin/env python3
"""Tonleiter V4 – eigene Musik + Effekte (48 kHz Stereo), liest out/zeiten.json.
Dramaturgie: Problem (a-Moll, eine einsame Gitarre, die abbricht) -> Wunsch (Spieluhr-Wiegenlied, zart)
-> Wendung „Bei Tonleiter“ (warmer Akkord, Gitarre + Lehrer-Gitarre im Zweiergespräch, C-Dur)
-> Tonleiter: Xylofon spielt c d e f g a h c genau auf den Stufen -> 12 Wochen / erstes Lied (voller Anschlag)
-> Heute Abend: dasselbe Wiegenlied, jetzt auf der Gitarre (Wunsch erfüllt) -> Schlussakkord.
Effekte nur, wo im Bild etwas passiert, aus dem Material: Papier, Faden, Holzboden, Buntstift, Kalenderblatt, Uhr, Stoffvorhang."""
import numpy as np, soundfile as sf, os, json
SR = 48000; Z = json.load(open('out/zeiten.json')); K = Z['K']; DUR = Z['DUR']; N = int(DUR * SR); R = np.random.default_rng(20)
M = np.zeros((N, 2)); S = np.zeros((N, 2))
def tt(d): return np.arange(int(d * SR)) / SR
def put(buf, a, x, pan=0.):
    i = int(a * SR); n = min(len(x), N - i)
    if i < 0 or n <= 0: return
    buf[i:i + n, 0] += x[:n] * np.cos((pan + 1) * np.pi / 4) * 1.41; buf[i:i + n, 1] += x[:n] * np.sin((pan + 1) * np.pi / 4) * 1.41
def hz(n): return 440 * 2 ** ((n - 69) / 12)
def lp(x, a):  # einfacher Tiefpass
    y = np.zeros_like(x); s = 0.
    for i in range(len(x)): s += a * (x[i] - s); y[i] = s
    return y
def reverb(x, sec, mix):
    n = int(sec * SR); ir = R.standard_normal((n, 2)) * np.exp(-np.arange(n) / SR * 6 / sec)[:, None]; F = 1 << int(np.ceil(np.log2(len(x) + n))); out = np.zeros_like(x)
    for c in range(2): out[:, c] = np.fft.irfft(np.fft.rfft(x[:, c], F) * np.fft.rfft(ir[:, c], F), F)[:len(x)]
    out *= np.abs(x).max() / (np.abs(out).max() + 1e-9); return x * (1 - mix) + out * mix
# --- Instrumente ---
def ks(f, d, bright=.5, decay=.996):  # Karplus-Strong-Saite, blockweise vektorisiert
    P = max(2, int(SR / f)); n = int(d * SR); y = np.zeros(n + P)
    y[:P] = R.uniform(-1, 1, P) * np.hanning(P) ** (1 - bright)
    for k in range(1, (n + P) // P):
        a, b = k * P, min((k + 1) * P, n + P); prev = y[a - P:b - P]; nxt = np.concatenate([y[a - P + 1:b - P + 1], [0]])[:b - a]
        y[a:b] = .5 * (prev + nxt) * decay
    y = y[P:P + n]; return y / (np.abs(y).max() + 1e-9)
def gtr(n, a, amp=.12, d=1.8, pan=0, bright=.5, M=M):
    put(M, a, ks(hz(n), d, bright) * np.exp(-tt(d) * .8) * amp, pan)
def strum(ns, a, amp=.09, down=True, gap=.018, d=1.6, pan=0):
    for i, n in enumerate(ns if down else ns[::-1]): gtr(n, a + i * gap, amp * (1 - i * .05), d, pan + (i - 2) * .06)
def box(n, a, amp=.07, pan=0):  # Spieluhr
    t = tt(1.6); x = (np.sin(2 * np.pi * hz(n) * t) + .35 * np.sin(2 * np.pi * hz(n) * 4.2 * t) * np.exp(-t * 9)) * np.exp(-t * 3.2)
    put(M, a, x * np.clip(t / .002, 0, 1) * amp, pan)
def xylo(n, a, amp=.12, pan=0):
    t = tt(.9); x = (np.sin(2 * np.pi * hz(n) * t) + .5 * np.sin(2 * np.pi * hz(n) * 3.93 * t) * np.exp(-t * 20)) * np.exp(-t * 7)
    put(M, a, x * np.clip(t / .001, 0, 1) * amp, pan)
def bass(n, a, d, amp=.13):
    t = tt(d); x = np.sin(2 * np.pi * hz(n) * t) + .3 * np.sin(4 * np.pi * hz(n) * t); put(M, a, x * np.clip(t / .01, 0, 1) * np.exp(-t * 2.2) * amp)
def pad(ns, a, b, amp=.02):
    t = tt(b - a); e = np.clip(t / .8, 0, 1) * np.clip((b - a - t) / .8, 0, 1)
    for i, n in enumerate(ns): put(M, a, (np.sin(2 * np.pi * hz(n) * t) + .5 * np.sin(2 * np.pi * hz(n) * 2.003 * t)) * e * amp, -.4 + .8 * i / max(1, len(ns) - 1))
def shaker(a, amp=.02):
    t = tt(.08); put(M, a, R.standard_normal(len(t)) * np.exp(-t * 60) * amp, .3)

# 1) Problem 0 – dabei: einsame Gitarre in a-Moll, Anläufe brechen ab
pad([45, 52, 57], .1, K['dabei'] + .3, .016)
for a, ns in [(.35, [45, 52, 57, 60, 64]), (K['acht'], [40, 47, 52, 55, 60])]: strum(ns, a, .07, d=2.4)
gtr(64, K['ecke'], .08, 2); gtr(60, K['ecke'] + .35, .06, 2)
# drei Anläufe: jeweils ein Anschlag, der stolpert (falscher Ton, abgedämpft)
for i in range(3):
    a = K['drei'] + i * .22 + .1
    strum([45, 52, 57, 60, 64], a, .05, d=.35); gtr(61 + i, a + .12, .04, .3)
for i, a in enumerate(np.arange(K['videos'], K['auf'] - .1, .3)): gtr([57, 60, 64, 62][i % 4], a, .045, .6, .2)
# aufgegeben: Saite rutscht ab, dann Stille
t = tt(.6); put(M, K['auf'], ks(hz(52), .6, .9) * np.exp(-t * 4) * .1)
# 2) Wunsch: Spieluhr-Wiegenlied (D-Dur), zart
LULL = [74, 78, 81, 78, 76, 74, 76, 78, 74]
a = K['dabei'] + .2
for i, n in enumerate(LULL + [74, 76, 78, 81, 83, 81, 78, 76]):
    if a > K['tl'] - .2: break
    box(n, a, .06 if i < 4 else .07, -.2 + .05 * (i % 5)); a += .34 if i % 3 else .5
pad([50, 57, 62, 66], K['dabei'], K['tl'] + .2, .018)
# 3) Wendung + Unterricht: zwei Gitarren im Wechsel, C-Dur-Groove
PROG = [[48, 55, 60, 64, 67], [43, 50, 55, 59, 62], [45, 52, 57, 60, 64], [41, 48, 53, 57, 60]]
strum(PROG[0], K['tl'] - .02, .1, d=2.6)
beat = .42; a = K['nicht']; i = 0
while a < K['ton1'] - .1:
    c = PROG[(i // 4) % 4]
    if i % 4 == 0: bass(c[0] - 12, a, beat * 3.5); pad(c[2:], a, a + beat * 4 + .2, .012)
    strum(c, a, .05 if i % 2 else .07, down=(i % 2 == 0), pan=-.35)          # Kunde
    if i % 2 == 1: gtr(c[-1] + 12, a + beat / 2, .05, 1, .45)                 # Lehrer antwortet
    shaker(a + beat / 2); i += 1; a += beat
# Tonleiter: Xylofon exakt auf den Stufen (gleiche Formel wie im Film)
STEP0 = K['ton1'] + .05; STEPD = (K['zwoelf'] - .2 - STEP0) / 7.6
for i, n in enumerate([72, 74, 76, 77, 79, 81, 83, 84]):
    st = STEP0 + i * STEPD; xylo(n, st, .13, -.5 + i * .14); gtr([48, 50, 52, 53, 55, 57, 59, 60][i], st + .15 * STEPD, .06, 1.2, .1)
# 12 Wochen + erstes Lied: fester Groove, voller Anschlag
a = K['zwoelf']; i = 0
while a < K['heute'] - .25:
    c = PROG[(i // 2) % 4]; strum(c, a, .06, down=(i % 2 == 0)); shaker(a + .21, .025)
    if i % 2 == 0: bass(c[0] - 12, a, .8, .12)
    i += 1; a += .42
strum([48, 55, 60, 64, 67, 72], K['erstes'], .11, d=2.2); strum([43, 55, 59, 62, 67, 71], K['lied2'], .1, d=2.2)
# 4) Heute Abend: das Wiegenlied jetzt auf der Gitarre, mit Begleitung
a = K['heute'] + .15
for i, n in enumerate(LULL):
    if a > K['tl2'] - .2: break
    gtr(n - 12, a, .11, 1.6, .15, .7)
    if i % 3 == 0: strum([50, 57, 62, 66], a, .045, d=1.8, pan=-.2)
    a += .34 if i % 3 else .5
pad([50, 57, 62, 66], K['heute'], K['tl2'] + .3, .02)
# 5) Schluss: heller C-Dur-Anschlag, Spieluhr-Echo, Schlussakkord
strum([48, 55, 60, 64, 67, 72], K['tl2'], .12, d=3)
for i, n in enumerate([72, 76, 79, 84]): box(n, K['tl2'] + .35 + i * .18, .06, -.3 + .2 * i)
a = K['tl2'] + .8; i = 0
while a < K['kostenlos'] + .1:
    c = PROG[[0, 3, 0, 1][(i // 2) % 4]]; strum(c, a, .045, down=(i % 2 == 0)); i += 1; a += .42
strum([36, 48, 55, 60, 64, 67, 72], K['kostenlos'] + .35, .13, d=3.2); box(84, K['kostenlos'] + .4, .07)
M = reverb(M, 1.8, .22)

# --- Effekte ---
def noise(d): return R.standard_normal(int(d * SR))
def crinkle(a, d, amp, pan=0):  # Papier: unregelmäßige Knister-Impulse, kein Rauschwisch
    t = tt(d); x = np.zeros(len(t)); idx = R.integers(0, len(t), int(d * 260))
    for k in idx: L = R.integers(30, 160); seg = R.standard_normal(L) * np.exp(-np.arange(L) / (L / 4)); x[k:k + L] += seg[:len(x[k:k + L])] * R.uniform(.2, 1)
    x = np.diff(np.concatenate([[0], x])); put(S, a, x * np.sin(np.pi * t / d) * amp, pan)
def thud(a, amp=.25, f=90, pan=0):  # Holzboden
    t = tt(.4); put(S, a, (np.sin(2 * np.pi * (f + 60 * np.exp(-t * 30)) * t) * np.exp(-t * 12) + lp(noise(.4), .2) * np.exp(-t * 40) * .6) * amp, pan)
def tick(a, amp=.05, f=3200, pan=0):
    t = tt(.05); put(S, a, np.sin(2 * np.pi * f * t) * np.exp(-t * 180) * amp, pan)
def pencil(a, d, amp=.05, pan=0):  # Buntstift: kratzig, mit Strich-Rhythmus
    t = tt(d); x = np.diff(np.concatenate([[0], noise(d)])) * (.5 + .5 * np.abs(np.sin(2 * np.pi * 7 * t))) * np.clip(t / .02, 0, 1) * np.clip((d - t) / .05, 0, 1); put(S, a, x * amp, pan)
def snap(a, amp=.12, pan=0):  # Faden reißt
    t = tt(.12); put(S, a, (np.sin(2 * np.pi * np.cumsum(2400 - 1600 * t / .12) / SR) * np.exp(-t * 50) + noise(.12) * np.exp(-t * 90) * .5) * amp, pan)
def step(a, amp=.08, pan=0):
    t = tt(.12); put(S, a, lp(noise(.12), .15) * np.exp(-t * 45) * amp * 3, pan)
# Spot an (Lampe klickt), Staub
tick(.15, .08, 1400); tick(.19, .04, 900)
# Tablets werden herabgelassen (Faden-Knarzen) und laufen an
for i in range(3):
    a = K['drei'] - .15 + i * .22; crinkle(a, .25, .05, .2 + i * .2); tick(K['videos'] + i * .12, .06, 2600, .2 + i * .2)
# Kalenderblätter reißen ab
crinkle(K['nach'] - .3, .3, .04, .6)
c0 = K['drei2'] - .1; cs = (K['wochen'] - .02 - c0) / 3
for d in range(3): pencil(c0 + d * cs, cs * .8, .06, .6)  # V7: drei Kreuze bis „Wochen“
# aufgegeben: Fäden reißen, Tablets schlagen auf, Gitarre wird abgestellt
for i in range(3): snap(K['auf'] + i * .07, .1, .1 + i * .25)
snap(K['auf'] + .1, .08, .7)
for i in range(3): thud(K['auf'] + .55 + i * .07, .18, 110, .1 + i * .25)
thud(K['auf'] + .4, .15, 70, .6)
# Tochter trippelt herein, Reißzwecke, Buntstift-Herz
for i, a in enumerate(np.arange(K['dabei'] - .1, K['tochter'] - .05, .17)): step(a, .05, -.6 + i * .08)
t = tt(.1); put(S, K['tochter'] + .12, np.sin(2 * np.pi * 900 * t) * np.exp(-t * 60) * .08)
pencil(K['tochter'] + .28, .24, .05)
# Hineinfahren in die Zeichnung: Papier wird glatt gestrichen
crinkle(K['lied'] - .75, .7, .05)
# Nacht rollt sich hoch (Papierrolle), später wieder herunter
crinkle(K['tl'] - .71, .5, .09); crinkle(K['heute'] - .3, .45, .08); crinkle(K['lehrer'] + .1, .45, .08); crinkle(K['zwoelf'] - .5, .3, .05, .6)
# Lehrer kommt (Schritte), setzt sich (Holz)
for i, a in enumerate(np.arange(K['tl'] + .1, K['allein'] - .35, .2)): step(a, .06, .6 - i * .08)  # V7: Mama kommt herein
thud(K['allein'] - .3, .1, 140, .3)
pencil(K['tonleiter'] - .34, .3, .04, -.5)  # Buntstift-Titel „Tonleiter“
pencil(K['festem'] - .2, K['lehrer'] - K['festem'] + .18, .05, .2)  # V7: Kreis um den Lehrer
crinkle(K['acht'] - .3, .2, .03, .5); crinkle(K['n30'] - .3, .2, .03, .5)  # V7: Etiketten schwingen ein
for i in range(5): t = tt(.25); put(S, K['lied'] - .25 + i * .4, np.sin(2 * np.pi * hz(83 + [0, 2, 4, 2, 0][i]) * t) * np.exp(-t * 14) * .02, .3)  # V7: gestrichelte Noten
# Uhr: herablassen, Ticken beim Füllen
crinkle(K['n30'] - .35, .25, .04, .5)
for a in np.arange(K['n30'], K['woche'] + .3, .12): tick(a, .03, 2900, .5)
# Stufen wachsen (Holzklötze) – Kunde hüpft
for i in range(8): thud(STEP0 + i * STEPD - .09, .12, 120 + i * 12, -.5 + i * .14)
# 12 Wochen: Häkchen mit Buntstift
pencil(K['zwoelf'] - .3, .28, .04, .5)  # V7: „12 Wochen“ auf den Kalenderkopf
for i in range(12): pencil(K['zwoelf'] + .1 + i * .085, .08, .05, -.5)
# Schluss: Vorhang (Stoff), Schild am Faden, Buntstift schreibt, Stempel-Plopp beim Angebot
crinkle(K['tl2'] - .76, .4, .07)
pencil(K['tl2'] - .36, .34, .045)
thud(K['probe'] - .04, .1, 160); thud(K['kostenlos'] - .03, .12, 200, .1)  # V7: Karte, Aufkleber
crinkle(K['kostenlos'] + .35, .3, .05)  # Adressschild
S = reverb(S, .8, .12)
os.makedirs('out', exist_ok=True)
for name, buf, pk in [('musik', M, .6), ('sfx', S, .8)]:
    sf.write(f'out/{name}.wav', (buf / (np.abs(buf).max() + 1e-9) * pk).astype(np.float32), SR)
print('ok')

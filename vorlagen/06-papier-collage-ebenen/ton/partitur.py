#!/usr/bin/env python3
"""Pfotenhaus V4 – eigene Musik + Effekte (numpy, 48 kHz Stereo, liest out/zeiten.json).
Instrumente passend zur Papier-Collage: Pizzicato, Marimba, Glockenspiel, Kontrabass, Besen-Shaker.
Dramaturgie: Frage (d-Moll, zögerndes Pizzicato) -> zwei Fehlversuche (je ein tiefer „Nein“-Ton) -> Walzen (Ratsche, dreimal Ding)
-> Pfotenhaus (F-Dur, Marimba-Groove) -> Abend/Foto (ruhiger) -> Strand + Mond wird voll (Glockenspiel) -> Schluss.
Effekte nur, wo im Bild etwas passiert: Papierbahnen, Koffer, Ticket, „?“, Stempel-X, Schlüssel fliegt, Buckel-Fauchen,
Walzen, Einrasten, Sprung, Futter, Spielmaus-Glöckchen, Schnurren, Kamera, Handy, Wellen, Mondstück, Zeichen."""
import numpy as np, os, json, wave
class sf:  # schlanker Ersatz für soundfile (16-bit PCM)
    @staticmethod
    def write(fn, x, sr):
        x = np.clip(np.asarray(x), -1, 1); w = wave.open(fn, 'wb'); w.setnchannels(x.shape[1] if x.ndim > 1 else 1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((x * 32767).astype('<i2').tobytes()); w.close()
SR = 48000; Z = json.load(open('out/zeiten.json')); K = Z['K']; DUR = Z['DUR']; N = int(DUR * SR); R = np.random.default_rng(23)
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
def pizz(n, a, amp=.08, pan=0):
    t = tt(.6); f = hz(n); x = (np.sin(2 * np.pi * f * t) + .4 * np.sin(4 * np.pi * f * t) * np.exp(-t * 20) + .2 * np.sin(6 * np.pi * f * t) * np.exp(-t * 30)) * np.exp(-t * 9)
    put(M, a, x * np.clip(t / .003, 0, 1) * amp, pan)
def marimba(n, a, amp=.08, pan=0):
    t = tt(.8); f = hz(n); x = (np.sin(2 * np.pi * f * t) + .3 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t * 30)) * np.exp(-t * 7)
    put(M, a, x * np.clip(t / .002, 0, 1) * amp, pan)
def glock(n, a, amp=.05, pan=0):
    t = tt(1.8); f = hz(n); x = (np.sin(2 * np.pi * f * t) + .4 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 5)) * np.exp(-t * 2.5)
    put(M, a, x * np.clip(t / .001, 0, 1) * amp, pan)
def bass(n, a, d=.4, amp=.13):
    t = tt(d); f = hz(n); put(M, a, (np.sin(2 * np.pi * f * t) + .3 * np.sin(4 * np.pi * f * t) * np.exp(-t * 8)) * np.exp(-t * 4) * np.clip(t / .004, 0, 1) * amp)
def shaker(a, amp=.02, pan=.3):
    t = tt(.08); put(M, a, nz(.08, 7000, 1) * np.exp(-t * 60) * amp, pan)
def pad(ns, a, b, amp=.015):
    t = tt(b - a); e = np.clip(t / .6, 0, 1) * np.clip((b - a - t) / .6, 0, 1)
    for i, n in enumerate(ns): put(M, a, (np.sin(2 * np.pi * hz(n) * t) + .5 * np.sin(2 * np.pi * hz(n) * 1.003 * t)) * e * amp, -.5 + i * .5)

B = 60 / 116
# 1) Frage: d-Moll, zögerndes Pizzicato (Viertel, mit Pausen)
pad([50, 53, 57], 0, K['pfoten'] - .2, .014)
seq = [62, None, 65, 64, None, 62, 60, None]
for i, a in enumerate(np.arange(.1, K['nicht'] + .3, B / 2)):
    n = seq[i % 8]
    if n: pizz(n, a, .07, -.2 + .1 * (i % 3))
    if i % 4 == 0: bass(38 if (i // 8) % 2 == 0 else 36, a, .5, .12)
pizz(69, K['wohin'], .08, .3); pizz(70, K['katze'] + .1, .07, .3)                     # Frage-Motiv
for k in ['zeit', 'nicht']: bass(33, K[k], .9, .2); pizz(49, K[k], .08)                  # „Nein“-Ton
# 2) Walzen: Tempo steigt, dreimal Ding
for i, n in enumerate([62, 65, 69, 72, 74, 77]): marimba(n, K['nicht'] + .45 + i * .12, .05, -.4 + .15 * i)
for i, a in enumerate(K['stops']): glock([77, 81, 84][i], a, .09, -.5 + .5 * i)
# 3) Pfotenhaus: F-Dur Marimba-Groove (F – C – Dm – Bb)
prog = [[53, 65, 69, 72], [48, 64, 67, 72], [50, 65, 69, 74], [46, 65, 70, 74]]
a = K['wohnt'] + .3; i = 0
while a < K['jeden'] - .2:
    c = prog[(i // 8) % 4]
    if i % 4 == 0: bass(c[0] - 12, a, .45, .13)
    if i % 4 == 2: bass(c[0] - 5, a, .3, .09)
    marimba(c[1 + (i * 2) % 3] + 12 * (i % 2), a, .045, -.3 + .2 * (i % 4)); shaker(a + B / 4, .018)
    i += 1; a += B / 2
# 4) Abend + Foto: ruhig, Glockenspiel
pad([53, 60, 65, 69], K['jeden'] - .2, K['so'] + .2, .016)
for d, n in [(0, 77), (.35, 81), (.7, 84), (1.4, 81)]: glock(n, K['jeden'] + d, .04, .2)
# 5) Strand + Split: warm, Mondstück rastet ein
pad([46, 53, 58, 62, 65], K['so'] - .2, K['pfoten2'] + .3, .018)
for i, a in enumerate(np.arange(K['so'], K['pfoten2'], B)): bass([46, 46, 48, 48, 53, 53][i % 6] - 12 + 12, a, .6, .1); marimba([70, 74, 77, 74][i % 4], a + B / 2, .035)
for i, n in enumerate([77, 81, 84, 89]): glock(n, K['katze2'] + i * .08, .06, -.3 + .2 * i)
# 6) Schluss: F-Dur, fröhlich
a = K['pfoten2']; i = 0
while a < DUR - 1.2:
    c = prog[(i // 8) % 4]
    if i % 4 == 0: bass(c[0] - 12, a, .45, .13)
    marimba(c[1 + (i * 2) % 3] + 12, a, .05, -.3 + .2 * (i % 4)); shaker(a + B / 4, .02); i += 1; a += B / 2
for n in [53, 60, 65, 69, 72, 77]: marimba(n, K['kostenlos'] + .3, .07)
glock(89, K['kostenlos'] + .3, .06)
M = reverb(M, 1.6, .25)

# ---------- Effekte ----------
def paper(a, d=.45, amp=.08, pan=0):  # Papierbahn gleitet
    t = tt(d); put(S, a, nz(d, 2600, .7) * (.6 + .4 * np.sin(2 * np.pi * 17 * t)) * np.sin(np.pi * t / d) * amp, pan)
def tap(a, amp=.07, pan=0):  # Papier wird aufgeklebt
    t = tt(.12); put(S, a, (nz(.12, 1800, 1.5) * np.exp(-t * 60) + np.sin(2 * np.pi * 180 * t) * np.exp(-t * 50) * .5) * amp, pan)
def stamp(a, amp=.25):
    t = tt(.5); put(S, a, (np.sin(2 * np.pi * (75 + 60 * np.exp(-t * 30)) * t) * np.exp(-t * 9) + nz(.5, 900, 2) * np.exp(-t * 40) * .5) * amp, .2)
paper(0, .5, .06)                                          # Koffer schiebt sich hoch
t = tt(.25); put(S, .35, (np.sin(2 * np.pi * 110 * t) * np.exp(-t * 20) + nz(.25, 600, 2) * np.exp(-t * 30) * .3) * .12)   # Koffer landet
paper(K['urlaub'] - .5, .4, .05, -.5); tap(K['urlaub'] - .05, .06, -.4)                            # Ticket
for k in ['wohin', 'katze']: t = tt(.2); put(S, K[k], np.sin(2 * np.pi * np.cumsum(500 + 900 * t / .2) / SR) * np.exp(-t * 10) * .05, .5)   # „?“ poppt
# Chips kleben
for k, dt in [('urlaub', -.05), ('wohin', -.05), ('nachbarin', -.05), ('zeit', -.05), ('fremde', 0), ('lieber', -.05), ('pfoten', .25), ('zimmer', -.05), ('fenster', -.05),
              ('morgens', -.05), ('futter', -.1), ('spielen', -.05), ('kuscheln', -.05), ('jeden', -.05), ('foto', -.1), ('urlaub2', -.05), ('katze2', -.1), ('pfoten2', .2), ('kennen', -.05)]:
    tap(K[k] + dt - .02, .04, R.uniform(-.6, .6))   # V5: Schild landet vor dem Wort
# Papierbahnen (Übergänge)
for a in [K['nachbarin'] - .45, K['nicht'] + .35, K['cut']['zimmer'] + .1, K['pfoten2'] - .3]: paper(a, .55, .1, R.uniform(-.3, .3))
t = tt(.6); put(S, K['so'] - .3, nz(.6, 2200, .8) * np.sin(np.pi * t / .6) * .07, .6)             # Riss in der Mitte
# Fehlversuche
stamp(K['zeit'] + .02); stamp(K['nicht'] + .02)
t = tt(.35); put(S, K['wohnung'], nz(.35, 3000, 1) * np.exp(-t * 6) * np.sin(np.pi * t / .35) * .07, .6)   # Fauchen
for k in range(4): t = tt(.05); put(S, K['nicht'] + .1 + k * .08, np.sin(2 * np.pi * 2600 * t) * np.exp(-t * 80) * .04, .5 + .1 * k)   # Schlüssel klimpert davon
# Walzen: Ratsche, Einrasten
a = K['nicht'] + .5
while a < K['stops'][2]:
    t = tt(.02); put(S, a, nz(.02, 3500, 4) * np.exp(-t * 200) * .05, R.uniform(-.4, .4)); a += .045 + .1 * max(0, a - K['pfoten'] + .3)
for i, a in enumerate(K['stops']): t = tt(.1); put(S, a, (np.sin(2 * np.pi * 900 * t) * np.exp(-t * 60)) * .08, -.5 + .5 * i)
# Sprung aufs Kissen
t = tt(.3); put(S, K['fenster'] - .05, (np.sin(2 * np.pi * 90 * t) * np.exp(-t * 18) + nz(.3, 700, 1) * np.exp(-t * 25) * .3) * .1, .1)
# Futter rieselt in den Napf
for i in range(16): a = K['futter'] - .4 + i * .03 + .25; t = tt(.04); put(S, a, np.sin(2 * np.pi * (1600 + (i * 263) % 900) * t) * np.exp(-t * 90) * .04, -.3)
# Spielmaus mit Glöckchen, Katze springt
for i in range(8): a = K['spielen'] - .1 + i * .09; t = tt(.3); put(S, a, (np.sin(2 * np.pi * 4200 * t) + np.sin(2 * np.pi * 5300 * t)) * np.exp(-t * 18) * .012, .5)
for i in range(3): a = K['spielen'] + i * .45; t = tt(.15); put(S, a + .2, np.sin(2 * np.pi * 120 * t) * np.exp(-t * 30) * .06)
# Schnurren
d = K['jeden'] - K['kuscheln']; t = tt(d); put(S, K['kuscheln'], nz(d, 180, 2) * (.5 + .5 * np.sin(2 * np.pi * 26 * t)) * np.clip(t / .3, 0, 1) * np.clip((d - t) / .3, 0, 1) * .09)
# Kamera + Handy
t = tt(.12); put(S, K['blitz'], (nz(.12, 4000, 2) * np.exp(-t * 40) + np.sin(2 * np.pi * 1100 * t) * np.exp(-t * 60) * .3) * .09, .4)
paper(K['blitz'] + .15, .9, .05, 0)                                                             # Foto fliegt
for i, n in enumerate([88, 93]): t = tt(.35); put(S, K['handy'] + i * .12, np.sin(2 * np.pi * hz(n) * t) * np.exp(-t * 10) * .05, -.3)
# Wellen am Strand
for i, a in enumerate(np.arange(K['foto'] - .3, K['pfoten2'], 1.3)):
    t = tt(1.5); put(S, a, nz(1.5, 900, .8) * np.sin(np.pi * t / 1.5) ** 2 * .05, -.6 + .3 * (i % 3))
# Zeichen erscheint
t = tt(.25); put(S, K['pfoten2'] + .15, (np.sin(2 * np.pi * 220 * t) * np.exp(-t * 14) + nz(.25, 1500, 1) * np.exp(-t * 30) * .3) * .1)
S = reverb(S, .9, .12)
os.makedirs('out', exist_ok=True)
for name, buf, pk in [('musik', M, .6), ('sfx', S, .8)]:
    sf.write(f'out/{name}.wav', (buf / (np.abs(buf).max() + 1e-9) * pk).astype(np.float32), SR)
print('ok', DUR)

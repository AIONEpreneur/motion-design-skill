#!/usr/bin/env python3
"""Halt Versicherungsmakler V5 (Effekte an das neue Bild angepasst: Monde statt Kalenderblätter) – eigene Musik + Effekte (numpy, 48 kHz Stereo, liest out/zeiten.json).
Dramaturgie: Problem (d-Moll, Herzschlag, tiefe Klavier-Einzeltöne, Regen) -> Wendung bei „Dafür“ (Stille, Glocke,
Licht schwillt an) -> Frage (schwebende sus-Akkorde, Tropfen) -> Vergleich (Zupf-Arpeggio, Zählwerk) -> Prüfung (Häkchen-Töne)
-> Lösung (D-Dur, warmes Pad, Klaviermelodie) -> Garten/Schluss (voller Akkord, Glockenspiel am Ring).
Effekte nur, wo im Bild etwas passiert: Rad, Sturz, Kalenderblätter, Gehaltsspur reißt, Raten-Pulse, Kinderschritte,
Fadenkreuz, Ring, Lichtscheibe, Schirm öffnet, Regen auf Schirmen, Suchlicht, Häkchen, Split-Linie, Ring, Angebot."""
import numpy as np, os, json, wave
class sf:  # schlanker Ersatz für soundfile (16-bit PCM)
    @staticmethod
    def write(fn, x, sr):
        x = np.clip(np.asarray(x), -1, 1); w = wave.open(fn, 'wb'); w.setnchannels(x.shape[1] if x.ndim > 1 else 1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((x * 32767).astype('<i2').tobytes()); w.close()
SR = 48000; Z = json.load(open('out/zeiten.json')); K = Z['K']; DUR = Z['DUR']; N = int(DUR * SR); R = np.random.default_rng(7)
M = np.zeros((N, 2)); S = np.zeros((N, 2))
def tt(d): return np.arange(int(d * SR)) / SR
def put(buf, a, x, pan=0.):
    i = int(a * SR); x = x[:max(0, N - i)] if i >= 0 else x[-i:]; i = max(i, 0); n = len(x)
    if n > 0: buf[i:i + n, 0] += x * np.cos((pan + 1) * np.pi / 4) * 1.41; buf[i:i + n, 1] += x * np.sin((pan + 1) * np.pi / 4) * 1.41
def lp(x, fc):  # einfacher Tiefpass 1. Ordnung
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); s = 0.
    for i in range(len(x)): s = (1 - a) * x[i] + a * s; y[i] = s
    return y
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
# ---------- Instrumente ----------
def piano(n, a, d=2.8, amp=.2, pan=0):
    t = tt(d); f = hz(n); x = sum(np.sin(2 * np.pi * f * k * t * (1 + .0004 * k * k)) * np.exp(-t * (1.0 + k * .8)) / k ** 1.4 for k in range(1, 8))
    put(M, a, x * np.clip(t / .003, 0, 1) * amp, pan)
def bell(n, a, d=3, amp=.08, pan=0):
    t = tt(d); f = hz(n); x = (np.sin(2 * np.pi * f * t) + .5 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 3) + .25 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 6)) * np.exp(-t * 1.6)
    put(M, a, x * np.clip(t / .002, 0, 1) * amp, pan)
def pluck(n, a, amp=.06, pan=0):
    t = tt(.9); f = hz(n); x = (np.sin(2 * np.pi * f * t) + .5 * np.sin(4 * np.pi * f * t) * np.exp(-t * 14)) * np.exp(-t * 6)
    put(M, a, x * np.clip(t / .002, 0, 1) * amp, pan)
def pad(ns, a, b, amp=.03, att=1.2, rel=1.0, bright=0.):
    t = tt(b - a); e = np.clip(t / att, 0, 1) * np.clip((b - a - t) / rel, 0, 1)
    for i, n in enumerate(ns):
        f = hz(n); x = np.sin(2 * np.pi * f * t) + np.sin(2 * np.pi * f * 1.004 * t + 1) + bright * .3 * np.sin(2 * np.pi * f * 2.002 * t)
        put(M, a, x * .5 * e * amp, -.6 + 1.2 * i / max(1, len(ns) - 1))
def sub(a, amp=.3, f0=46):
    t = tt(.6); ph = 2 * np.pi * np.cumsum(f0 + 60 * np.exp(-t * 28)) / SR; put(M, a, np.sin(ph) * np.exp(-t * 7) * amp)
def bass(n, a, d, amp=.14):
    t = tt(d); f = hz(n); x = np.sin(2 * np.pi * f * t) + .2 * np.sin(4 * np.pi * f * t); put(M, a, x * np.clip(t / .02, 0, 1) * np.clip((d - t) / .08, 0, 1) * amp)

# 1) Problem 0 – Dafür: d-Moll, Herzschlag, tiefe Einzeltöne
pad([50, 53, 57], 0.0, K['dafuer'] + .3, .02, att=.6)
for a in np.arange(K['monate'] - .2, K['dafuer'] - .2, .72): sub(a, .2); sub(a + .2, .11)
for a, ns in [(K['sturz'], [38, 50]), (K['monate'], [46]), (K['gehalt'], [45]), (K['aus'], [41, 44]), (K['rate'], [43]), (K['weiter'], [40])]:
    for n in ns: piano(n, a, 3.0, .18)
for i, n in enumerate([74, 72, 69]): piano(n, K['kinder'] + i * .28, 2.4, .08, .3)      # zarte Kinder-Figur
piano(62, K['brauchen'], 3, .08, -.2); piano(65, K['brauchen'] + .02, 3, .06, .2)
# 2) Wendung: kurzer Atem, dann Glocke am Ring, Licht schwillt an
bell(81, K['bu'] + .2, 3.5, .09); bell(88, K['bu'] + .2, 3.5, .04, .3)
pad([62, 69, 74, 78], K['dafuer'] + .3, K['nur'] + .4, .025, att=1.6, bright=1)
# 3) Frage: schwebend (Dsus2 / Bbmaj7#11), Tropfen
pad([50, 57, 64, 69], K['nur'] - .1, K['halt'] + .2, .022, att=.6)
pad([46, 57, 62, 64], K['tarif'], K['halt'] + .2, .016, att=.8)
# 4) Vergleich: Zupf-Arpeggio in Sechzehnteln (D – Bm – G – A), Tempo 110
B = 60 / 110; a = K['halt'] - .05; i = 0; prog = [[62, 66, 69, 74], [59, 62, 66, 71], [55, 59, 62, 67], [57, 61, 64, 69]]
while a < K['passiert'] - .3:
    c = prog[(i // 4) % 4]
    if i % 4 == 0: bass(c[0] - 12, a, B * 3.9, .12); pad(c[1:], a, a + B * 4 + .2, .012, att=.3)
    for j in range(4): pluck(c[j] + 12, a + j * B / 4, .035 + .01 * (j == 0), -.4 + .25 * j)
    i += 1; a += B
# 5) Lösung: D-Dur, warmes Pad, Klaviermelodie
L0 = K['passiert'] - .2
pad([50, 57, 62, 66, 69], L0, DUR, .028, att=1.0, rel=1.2, bright=.6)
mel = [(0, 74), (.45, 76), (.9, 78), (1.8, 81), (2.7, 78), (3.15, 76), (3.6, 74)]
for d, n in mel: piano(n, K['gehalt2'] - .1 + d * .7, 2.6, .07, .2)
for a2 in np.arange(L0, K['familie'] - .2, B * 2): bass(38, a2, B * 1.8, .1)
# Garten: voller Akkord, Achtel-Puls
for n in [38, 50, 57, 62, 66, 69, 74]: piano(n, K['familie'], 3.5, .075)
a = K['familie']; i = 0
while a < DUR - 1.4:
    c = [[62, 66, 69, 74], [59, 62, 66, 71], [55, 59, 62, 67], [57, 61, 64, 69]][(i // 8) % 4]
    if i % 8 == 0: bass(c[0] - 12, a, B * 3.8, .11)
    pluck(c[i % 4] + 12, a, .035, -.3 + .2 * (i % 4)); i += 1; a += B / 2
# Ring + Schluss
for i2, n in enumerate([74, 78, 81, 86]): bell(n, K['halt2'] + i2 * .14, 3, .06, -.3 + .2 * i2)
for n in [38, 50, 57, 62, 66, 69, 74, 78]: piano(n, K['kostenlos'] + .5, 3.2, .08)
M = reverb(M, 2.6, .32)

# ---------- Effekte ----------
tc = K['sturz'] - .14
t = tt(tc + .1); put(S, 0, (nz(tc + .1, 180, 1) * .6 + np.sin(2 * np.pi * 14 * 2 * t) * .1) * .08)             # Reifen auf Asphalt
for k in range(6): t = tt(.03); put(S, k * .06, nz(.03, 4000, 4) * np.exp(-t * 90) * .05, .2)                  # Kette tickt
def metal(a, amp):
    t = tt(.9); x = sum(np.sin(2 * np.pi * f * t) * np.exp(-t * d) for f, d in [(523, 6), (1187, 9), (1733, 11), (2641, 14), (3521, 18)]); put(S, a, (x / 5 + nz(.9, 2500, 1) * np.exp(-t * 25) * .8) * amp, .2)
metal(tc, .35); metal(tc + .18, .18)
t = tt(.5); put(S, tc + .55, (np.sin(2 * np.pi * (55 + 60 * np.exp(-t * 20)) * t) * np.exp(-t * 9) + nz(.5, 600, 1) * np.exp(-t * 30) * .4) * .45)   # Körper schlägt auf
for k in range(10): t = tt(.12); put(S, tc + .7 + k * .11, np.sin(2 * np.pi * 900 * t) * np.exp(-t * 60) * .03 * (1 - k / 10), .4)   # Rad dreht leer
# Regen: Teppich vom Sturz bis zum Garten
def rainbed(a, b, amp, fc=3200):
    d = b - a; t = tt(d); e = np.clip(t / .6, 0, 1) * np.clip((d - t) / .6, 0, 1); x = np.stack([nz(d, fc, .7), nz(d, fc * 1.1, .7)], 1) * e[:, None] * amp
    i = int(a * SR); n = min(len(x), N - i); S[i:i + n] += x[:n]
rainbed(tc, K['familie'] + .1, .05)
for k in range(40):  # einzelne Tropfen
    a = tc + .5 + R.random() * (K['familie'] - tc - 1); t = tt(.06); put(S, a, np.sin(2 * np.pi * (2200 + R.random() * 1800) * t) * np.exp(-t * 80) * .03, R.uniform(-.8, .8))
# V5: drei Monde ziehen über den Himmel (monatelang) – weiches Luftrauschen je Bogen
for k in range(3):
    a = K['monate'] - .3 + k * .52; t = tt(.72); env = np.sin(np.pi * t / .72) ** 2
    put(S, a, nz(.72, 900 + 500 * k, .8) * env * .09, -.8 + .8 * k); bell(79 + [0, 3, 7][k], a + .36, 2.2, .025, -.5 + .5 * k)
# Gehaltsspur: Fließen, dann Abriss (fallender Ton)
t = tt(K['aus'] - K['gehalt'] + .4); put(S, K['gehalt'] - .4, np.sin(2 * np.pi * 880 * t) * (.5 + .5 * np.sin(2 * np.pi * 6 * t)) * .02, -.4)
t = tt(.8); f = 700 * np.exp(-t * 2.6); put(S, K['aus'], np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3) * .12, -.3)
# Raten-Pulse: dumpfes Münz-Klacken bei Ankunft an der Bank
for i in range(12):
    a = K['rate'] + .15 + i * .34 + .5
    if a > K['kinder'] - .25: break
    t = tt(.25); put(S, a, (np.sin(2 * np.pi * 330 * t) * np.exp(-t * 25) + np.sin(2 * np.pi * 1320 * t) * np.exp(-t * 40) * .4) * .12, .6)
# Kinderschritte
for k in range(8): t = tt(.08); put(S, K['kinder'] - .75 + k * .11, nz(.08, 500, 2) * np.exp(-t * 60) * .12, -.5 + (k % 2))
# Fadenkreuz: dünner steigender Ton; Lichtscheibe: tonales Anschwellen
t = tt(.5); put(S, K['dafuer'] + .3, np.sin(2 * np.pi * np.cumsum(1200 + 800 * t / .5) / SR) * np.sin(np.pi * t / .5) * .03, .4)
t = tt(.9); f = 220 * (1 + t / .9); put(S, K['bu'] + .1, (np.sin(2 * np.pi * np.cumsum(f) / SR) + .5 * np.sin(2 * np.pi * np.cumsum(f * 1.5) / SR)) * np.sin(np.pi * t / .9) ** 2 * .05, .3)
def fwump(a, amp=.2, pan=0):  # Schirm spannt sich
    t = tt(.35); put(S, a, (nz(.35, 400, 1.5) * np.exp(-t * 14) + np.sin(2 * np.pi * 95 * t) * np.exp(-t * 18) * .6) * amp, pan)
fwump(K['bu'] + .55, .25, .3)   # V7: Schirm öffnet früher
# viele Schirme poppen auf
for i in range(22): fwump(K['nur'] + .1 + i * .045 + R.random() * .03, .05, R.uniform(-.9, .9))
# Tropfen durch Löcher
for k in range(14): a = K['zahlt'] - .3 + k * .12; t = tt(.1); put(S, a, np.sin(2 * np.pi * (1500 + (k * 7919 % 900)) * t) * np.exp(-t * 50) * .05, R.uniform(-.8, .8))
# Raster: Schirme gleiten an ihren Platz (leise Klicks)
for k in range(16): t = tt(.03); put(S, K['halt'] + k * .04, nz(.03, 3500, 3) * np.exp(-t * 100) * .04, -.2 + .03 * k)
# Suchlicht summt, Durchgefallene sacken ab (tiefe „Tocks“), Zählwerk tickt
t = tt(K['tarife'] - K['hundert'] + .9); put(S, K['hundert'] - .55, np.sin(2 * np.pi * 110 * t) * np.sin(np.pi * t / t[-1]) * .03 + nz(len(t) / SR + 1e-4, 800, 5)[:len(t)] * np.sin(np.pi * t / t[-1]) * .015)
for k in range(24): a = K['hundert'] - .5 + k * .065; t = tt(.1); put(S, a, np.sin(2 * np.pi * 180 * t) * np.exp(-t * 40) * .06, -.8 + k * .07)
tk = K['hundert'] - .55
while tk < K['tarife'] + .3: t = tt(.02); put(S, tk, nz(.02, 5000, 3) * np.exp(-t * 200) * .03, -.6); tk += .05 + .05 * (tk - K['hundert'] + .55)
# Tarifkarte: Papier gleitet heran, Häkchen
t = tt(.4); put(S, K['prueft'] - .1, nz(.4, 2600, 1) * np.sin(np.pi * t / .4) * .06, .4)
for i, a in enumerate([K['klein'] - .1] + K['ck']):   # V7: Lupe + Häkchen fertig auf den Wörtern
    t = tt(.35); put(S, a, (np.sin(2 * np.pi * hz(86 + [0, 2, 4, 7][i]) * t) * np.exp(-t * 12) + nz(.35, 4000, 4) * np.exp(-t * 60) * .3) * .06, .4)
fwump(K['passiert'] - .15, .15)
# Gehalt fließt wieder: Glitzern im Takt der Pulse; Regen prasselt auf den Schirm
for k in range(18): a = K['gehalt2'] - .3 + k * .1; bell(90 + (k % 4) * 2, a, 1.2, .012, -.4 + (k % 5) * .2)
t = tt(K['familie'] - K['passiert']); put(S, K['passiert'], nz(len(t) / SR + 1e-4, 1500, 1.2)[:len(t)] * np.clip(t / .5, 0, 1) * np.clip((t[-1] - t) / .3, 0, 1) * .04, -.1)
# Split-Linie: gläserner Ton, dann Glissando nach oben beim Wischen
t = tt(1.2); put(S, K['familie'] - .1, (np.sin(2 * np.pi * 1760 * t) + .4 * np.sin(2 * np.pi * 2637 * t)) * np.exp(-t * 3) * .05)
t = tt(.9); f = 440 * 2 ** (t / .9); put(S, K['behaelt'] - .05, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / .9) * .035, -.5)
# Grillen im Abendgarten
for k in range(30):
    a = K['behaelt'] + k * .17; t = tt(.09)
    if a > K['halt2'] + 1.4: break
    put(S, a, np.sin(2 * np.pi * 4400 * t) * (np.sin(2 * np.pi * 45 * t) > 0) * np.exp(-t * 20) * .012, .7 if k % 2 else -.7)
# Angebot
t = tt(.15); put(S, K['erst'] - .05, np.sin(2 * np.pi * 1318 * t) * np.exp(-t * 25) * .06)
S = reverb(S, 1.2, .12)
os.makedirs('out', exist_ok=True)
for name, buf, pk in [('musik', M, .6), ('sfx', S, .8)]:
    sf.write(f'out/{name}.wav', (buf / (np.abs(buf).max() + 1e-9) * pk).astype(np.float32), SR)
print('ok', DUR)

#!/usr/bin/env python3
"""Stadtbote Kurier V4 – eigene Musik + Effekte. Dramaturgie folgt dem Kunden:
Hook (Uhr tickt, d-Moll-Staccato, Druck) -> Auftrag weg / Post übermorgen (Moll-Akkorde, schwer)
-> Verteilzentrum (zäh, halbes Tempo, Förderband) -> Wendung „direkt“ (kurze Luft, dann D-Dur-Groove, 120 BPM)
-> Ankunft/Beleg (Glocken) -> Marke (heller Schluss, Hupe bei „sofort“).
Effekte nur aus dem Material des Bilds: Uhr, Umschlag, Stempel, Feder auf Papier (Karte/Route), Schild, Klecks,
Förderband, Paket, Stoppuhr, Motor, Unterschrift, Kameraauslöser, Haken, Hupe. Kein Whoosh."""
import numpy as np, soundfile as sf, os, json
SR = 48000; Z = json.load(open('out/zeiten.json')); K = Z['K']; DUR = Z['DUR']; N = int(DUR * SR); R = np.random.default_rng(17)
M = np.zeros((N, 2)); S = np.zeros((N, 2))
def tt(d): return np.arange(int(round(d * SR))) / SR
def put(buf, a, x, pan=0.):
    i = int(a * SR); n = min(len(x), N - i)
    if n > 0 and i >= 0: buf[i:i + n, 0] += x[:n] * np.cos((pan + 1) * np.pi / 4) * 1.41; buf[i:i + n, 1] += x[:n] * np.sin((pan + 1) * np.pi / 4) * 1.41
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
# --- Instrumente ---
def pluck(n, a, amp=.07, pan=0, dec=7):
    t = tt(.8); f = hz(n); x = (np.sin(2 * np.pi * f * t) + .45 * np.sign(np.sin(2 * np.pi * f * t)) * np.exp(-t * 30) * .5 + .3 * np.sin(4 * np.pi * f * t) * np.exp(-t * 12)) * np.exp(-t * dec)
    put(M, a, x * np.clip(t / .002, 0, 1) * amp, pan)
def keys(n, a, d=1.6, amp=.12, pan=0):
    t = tt(d); f = hz(n); x = sum(np.sin(2 * np.pi * f * k * t) * np.exp(-t * (1.5 + k)) / k ** 1.3 for k in range(1, 6)); put(M, a, x * np.clip(t / .004, 0, 1) * amp, pan)
def pad(ns, a, b, amp=.025):
    t = tt(b - a); e = np.clip(t / .6, 0, 1) * np.clip((b - a - t) / .5, 0, 1)
    for i, n in enumerate(ns): f = hz(n); put(M, a, (np.sin(2 * np.pi * f * t) + .6 * np.sin(2 * np.pi * f * 1.004 * t + 1) + .2 * np.sin(4 * np.pi * f * t)) * .5 * e * amp, -.5 + i / max(1, len(ns) - 1))
def kick(a, amp=.35):
    t = tt(.35); ph = 2 * np.pi * np.cumsum(48 + 110 * np.exp(-t * 32)) / SR; put(M, a, np.sin(ph) * np.exp(-t * 10) * amp)
def clap(a, amp=.06):
    t = tt(.2); put(M, a, nz(.2, 1400, 1) * (np.exp(-t * 30) + .5 * np.exp(-np.abs(t - .012) * 300)) * amp, .1)
def hat(a, amp=.02, pan=.3):
    t = tt(.06); put(M, a, nz(.06, 8000, 1.5) * np.exp(-t * 70) * amp, pan)
def bass(n, a, d, amp=.17):
    t = tt(d); f = hz(n); x = np.tanh(2 * (np.sin(2 * np.pi * f * t) + .3 * np.sin(4 * np.pi * f * t))) * .6; put(M, a, x * np.clip(t / .006, 0, 1) * np.clip((d - t) / .03, 0, 1) * amp)
def bell(n, a, amp=.06, pan=0):
    t = tt(2.2); f = hz(n); x = (np.sin(2 * np.pi * f * t) + .5 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 3) + .3 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 6)) * np.exp(-t * 2.2); put(M, a, x * amp, pan)
B = .5  # 120 BPM
# 1) Hook 0–2.7: d-Moll-Staccato in Achteln, tiefer Puls, steigt
for i, a in enumerate(np.arange(.25, K['sonst'] - .05, B / 2)):
    pluck([62, 65, 69, 65][i % 4] + (12 if i >= 8 else 0) * 0, a, .045 + .002 * i, -.3 + .2 * (i % 4))
    if i % 2 == 0: bass(38, a, B * .45, .12)
for a in [K['heute'], K['kunden']]: keys(50, a, 1.2, .1); keys(57, a, 1.2, .07)
# 2) Stake + Post 2.7–6.4: d – B – g – A, schwere Viertel
ch = [[38, 62, 65, 69], [34, 62, 65, 70], [31, 62, 67, 70], [33, 61, 64, 69]]
a = K['sonst']; i = 0
while a < K['ueber'] - .05:
    c = ch[(i // 2) % 4]; kick(a, .22); bass(c[0] + 12, a, B * .9, .15)
    if i % 2 == 0: pad(c[1:], a, a + B * 2 + .15, .02)
    pluck(c[1 + i % 3] + 12, a + B / 2, .035, .3); i += 1; a += B
keys(38, K['weg'], 2.0, .14); keys(50, K['weg'], 2.0, .1)
for n in [38, 50, 53, 58]: keys(n, K['ueberm'], 2.4, .1)
# 3) Verteilzentrum 6.4–9.9: zäh, halbes Tempo, liegender Ton, Uhr-Pendel
pad([50, 53, 57, 60], K['ueber'], K['stadtbote'] - .1, .022)
for a in np.arange(K['ueber'], K['stadtbote'] - .2, B * 2): kick(a, .16); bass(38, a, B * 1.8, .1)
for a in np.arange(K['ueber'] + B, K['stadtbote'] - .2, B * 2): pluck(69, a, .03, .4, 4); pluck(68, a + B * .5, .02, -.4, 4)
# 4) Wendung: „Der Stadtbote“ – Luft, Auftakt; ab „direkt“ D-Dur-Groove
for j, n in enumerate([62, 66, 69, 74]): pluck(n, K['stadtbote'] + j * .12, .06, -.3 + j * .2)
prog = [[38, 62, 66, 69], [45, 61, 64, 69], [47, 62, 66, 71], [43, 62, 67, 71]]
a = K['direkt'] - .02; i = 0
while a < K['name'] - .1:
    c = prog[(i // 4) % 4]
    kick(a, .3)
    if i % 2 == 1: clap(a, .07)
    hat(a + B / 2, .025); hat(a + B / 4, .012, -.3); hat(a + 3 * B / 4, .012, -.3)
    bass(c[0], a, B * .45, .17); bass(c[0] + 12 if i % 2 else c[0], a + B / 2, B * .4, .12)
    if i % 4 == 0: pad(c[1:], a, a + B * 4 + .1, .018)
    for j in range(4): pluck(c[1 + (i + j) % 3] + 12, a + j * B / 4, .03 + (.012 if j == 0 else 0), -.35 + .23 * j, 9)
    i += 1; a += B
# Ankunft + Beleg + „gehört Ihnen“
for j, n in enumerate([74, 78, 81]): bell(n, K['vier'] + j * .1, .05, -.3 + .3 * j)
for j, n in enumerate([81, 86]): bell(n, K['beleg'] + j * .12, .06)
for j, n in enumerate([74, 78, 81, 86]): bell(n, K['ihnen'] + j * .09, .045, -.3 + .2 * j)
# 5) Marke 22.3–Ende: heller, lockerer, Schlussakkord
a = K['name'] - .05; i = 0; prog2 = [[43, 62, 67, 71], [45, 64, 69, 73], [38, 62, 66, 69], [38, 62, 66, 69]]
while a < DUR - 1.6:
    c = prog2[(i // 4) % 4]
    if i % 2 == 0: kick(a, .22)
    if i % 2 == 1: clap(a, .05)
    hat(a + B / 2, .02)
    if i % 4 == 0: pad(c[1:], a, a + B * 4 + .1, .022); bass(c[0], a, B * 1.8, .14)
    pluck(c[1 + i % 3] + 12, a, .04, -.3 + .3 * (i % 3)); pluck(c[1 + (i + 1) % 3] + 12, a + B / 2, .03, .3)
    i += 1; a += B
for n in [38, 50, 57, 62, 66, 69, 74]: keys(n, DUR - 1.5, 2.0, .09)
bell(86, DUR - 1.5, .05)
M = reverb(M, 1.8, .22)

# --- Effekte ---
def tick(a, amp=.08, f=3200, pan=0): t = tt(.04); put(S, a, nz(.04, f, 6) * np.exp(-t * 180) * amp, pan)
for j, a in enumerate(np.arange(.2, K['sonst'] - .1, .25)): tick(a, .09, 3200 if j % 2 else 2600, .35)       # Uhr tickt (schnell = Zeitdruck)
def thud(a, amp=.3, f0=70):
    t = tt(.45); put(S, a, (np.sin(2 * np.pi * (f0 + 50 * np.exp(-t * 25)) * t) * np.exp(-t * 9) + nz(.45, 1100, 2) * np.exp(-t * 45) * .25) * amp)
t = tt(.35); put(S, .2, nz(.35, 3000, 1) * np.sin(np.pi * t / .35) * .05, -.3)                               # Umschlag gleitet auf den Tisch
thud(.55, .22, 90)                                                                                          # Umschlag liegt
thud(K['vertrag'] + .3, .38, 65)                                                                             # Stempel EILT
def pen(a, d, amp=.05, pan=0):  # Feder/Filzstift auf Papier: Kratzen mit Körnung
    t = tt(d); x = nz(d, 2600, 3) * (.6 + .4 * np.abs(np.sin(2 * np.pi * 13 * t + R.random()))) * np.sin(np.pi * np.clip(t / d, 0, 1)) ** .5; put(S, a, x * amp, pan)
pen(K['sonst'] - .1, 1.3, .035)                                                                             # Karte zeichnet sich
t = tt(.25); put(S, K['auftrag'], np.sin(2 * np.pi * 880 * t) * np.exp(-t * 18) * .06)                      # Schild ploppt
t = tt(.6); put(S, K['weg'], np.sin(2 * np.pi * np.cumsum(700 - 500 * t / .6) / SR) * np.exp(-t * 4) * .06)  # Schild fällt
pen(K['post'] - .1, 1.1, .06, -.3)                                                                          # roter Umweg
t = tt(.5); put(S, K['ueberm'], (nz(.5, 500, 1.2) * np.exp(-t * 14) + nz(.5, 2000, 2) * np.exp(-t * 30) * .5) * .3)  # Klecks
for a in np.arange(K['ueber'] + .2, K['stadtbote'] - .2, .16): tick(a, .03, 900, .2)                       # Förderband-Rollen
t = tt(3.0); put(S, K['ueber'] + .2, nz(3.0, 180, 1.5) * np.sin(np.pi * t / 3.0) * .06)                        # Hallenbrummen
thud(K['vz'] + .2, .18, 110); thud(K['zweimal'] + .3, .2, 100)                                                # Paket landet (2×)
pen(K['direkt'] - .4, .8, .07, .2)                                                                          # orange Linie direkt
for a in np.arange(K['abgeholt'], K['sechzig'] + .25, .08): tick(a, .05, 4200, .4)                         # Stoppuhr rattert
t = tt(.25); put(S, K['sechzig'] + .25, np.sin(2 * np.pi * 1760 * t) * np.exp(-t * 14) * .06, .4)             # 60 erreicht
t = tt(.35); put(S, K['abgeholt'] + .45, (nz(.35, 600, 1.5) * np.exp(-t * 12)) * .06)                         # Bremsen
d = K['da'] - K['quer']; t = tt(d); f = 55 + 18 * np.sin(np.pi * t / d); eng = np.tanh(3 * np.sin(2 * np.pi * np.cumsum(f) / SR)) + .4 * nz(d, 250, 1)
put(S, K['quer'], eng * np.sin(np.pi * np.clip(t / d, 0, 1)) ** .6 * .06)                                  # Motor quer durch die Stadt
t = tt(.3); put(S, K['da'] - .05, nz(.3, 700, 2) * np.exp(-t * 10) * .07)                                      # Halt am Kunden
thud(K['beleg'] - .05, .3, 75)                                                                               # V7: Stempel mit Häkchen
pen(K['sofort'] - .32, .3, .05)                                                                              # V7: Federstrich unter der Nummer
pen(K['zugestellt'] - .3, .25, .03)
t = tt(.8); put(S, K['unterschrift'] - .05, nz(.8, 3800, 4) * (.5 + .5 * np.abs(np.sin(2 * np.pi * 7 * t))) * np.sin(np.pi * t / .8) * .06, .3)  # Unterschrift
t = tt(.18); put(S, K['foto'], (nz(.18, 5000, 1) * np.exp(-t * 60) + nz(.18, 1800, 2) * np.exp(-np.abs(t - .07) * 200) * .6) * .2, .3)  # Auslöser
thud(K['ihnen'] + .05, .16, 120)
for d0 in [0, .22]:                                                                                          # Hupe: wir holen sofort ab
    t = tt(.16); put(S, K['sofort'] + .1 + d0, np.tanh(2 * (np.sin(2 * np.pi * 415 * t) + np.sin(2 * np.pi * 523 * t))) * np.clip(t / .01, 0, 1) * np.clip((.16 - t) / .02, 0, 1) * .07, .4)
S = reverb(S, .8, .12)
os.makedirs('out', exist_ok=True)
for name, buf, pk in [('musik', M, .6), ('sfx', S, .8)]:
    sf.write(f'out/{name}.wav', (buf / (np.abs(buf).max() + 1e-9) * pk).astype(np.float32), SR)
print('ok')

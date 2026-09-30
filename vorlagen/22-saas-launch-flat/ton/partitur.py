#!/usr/bin/env python3
"""Pflegebrücke V4 – eigene Musik + Effekte (48 kHz Stereo), liest out/zeiten.json.
Stil wie ein moderner Produkt-Launch, aber mit Dramaturgie der Kundin:
Nachtdienst-Problem (d-Moll, tiefer Puls, tickende Uhr) -> Chaos (Puls verdichtet sich) -> „selbst einspringen“ (Stille, nur Herzschlag)
-> Lichtpunkt: aufsteigender Ton, heller D-Dur-Akkord mit Logo -> Lösung (120 BPM, Plucks, sauberer Groove)
-> 48 Std. zählt hoch -> „besetzt“ Erfolgsklang -> Wochenende (Glocken, leicht) -> Schlussakkord.
Effekte nur, wo im Bild etwas passiert: Handy vibriert, Nachricht, Kalenderfelder, Tastatur, Klick, Karten, Pins."""
import numpy as np, soundfile as sf, os, json
SR = 48000; Z = json.load(open('out/zeiten.json')); K = Z['K']; DUR = Z['DUR']; N = int(DUR * SR); R = np.random.default_rng(22)
M = np.zeros((N, 2)); S = np.zeros((N, 2))
def tt(d): return np.arange(int(d * SR)) / SR
def put(buf, a, x, pan=0.):
    i = int(a * SR); n = min(len(x), N - i)
    if i < 0 or n <= 0: return
    buf[i:i + n, 0] += x[:n] * np.cos((pan + 1) * np.pi / 4) * 1.41; buf[i:i + n, 1] += x[:n] * np.sin((pan + 1) * np.pi / 4) * 1.41
def hz(n): return 440 * 2 ** ((n - 69) / 12)
def reverb(x, sec, mix):
    n = int(sec * SR); ir = R.standard_normal((n, 2)) * np.exp(-np.arange(n) / SR * 6 / sec)[:, None]; F = 1 << int(np.ceil(np.log2(len(x) + n))); out = np.zeros_like(x)
    for c in range(2): out[:, c] = np.fft.irfft(np.fft.rfft(x[:, c], F) * np.fft.rfft(ir[:, c], F), F)[:len(x)]
    out *= np.abs(x).max() / (np.abs(out).max() + 1e-9); return x * (1 - mix) + out * mix
def pad(ns, a, b, amp=.02, bright=0.):
    t = tt(b - a); e = np.clip(t / .6, 0, 1) * np.clip((b - a - t) / .6, 0, 1)
    for i, n in enumerate(ns):
        f = hz(n); x = np.sin(2 * np.pi * f * t) + .4 * np.sin(2 * np.pi * f * 1.004 * t + 1) + bright * .25 * np.sin(2 * np.pi * f * 2 * t)
        put(M, a, x * e * amp, -.5 + i / max(1, len(ns) - 1))
def pluck(n, a, amp=.06, pan=0, dec=7):
    t = tt(.8); f = hz(n); x = (np.sin(2 * np.pi * f * t) + .3 * np.sin(4 * np.pi * f * t) * np.exp(-t * 12) + .15 * np.sin(6 * np.pi * f * t) * np.exp(-t * 20)) * np.exp(-t * dec)
    put(M, a, x * np.clip(t / .002, 0, 1) * amp, pan)
def bell(n, a, amp=.05, pan=0):
    t = tt(2); f = hz(n); x = (np.sin(2 * np.pi * f * t) + .5 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 3) + .25 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 6)) * np.exp(-t * 2.2)
    put(M, a, x * np.clip(t / .002, 0, 1) * amp, pan)
def sub(n, a, d, amp=.14):
    t = tt(d); put(M, a, np.sin(2 * np.pi * hz(n) * t) * np.clip(t / .01, 0, 1) * np.clip((d - t) / .05, 0, 1) * amp)
def kick(a, amp=.3):
    t = tt(.35); put(M, a, np.sin(2 * np.pi * np.cumsum(48 + 110 * np.exp(-t * 28)) / SR) * np.exp(-t * 9) * amp)
def clap(a, amp=.05):
    t = tt(.2); x = R.standard_normal(len(t)); x = np.diff(np.concatenate([[0], x])); put(M, a, x * (np.exp(-t * 30) + .5 * np.exp(-np.abs(t - .012) * 400)) * amp, .1)
def hat(a, amp=.018, pan=.3):
    t = tt(.05); x = np.diff(np.concatenate([[0], R.standard_normal(len(t))])); put(M, a, x * np.exp(-t * 90) * amp, pan)
B = .5  # 120 BPM
# 1) Nachtdienst-Problem: d-Moll, tiefer Puls, Uhr tickt
pad([50, 53, 57], .1, K['und1'], .018)
for a in np.arange(.3, K['und1'] - .1, B): sub(38, a, .18, .13); hat(a + B / 2, .012, -.3)
for a in np.arange(K['krank'], K['und1'] - .1, B / 2): hat(a, .02, .3)   # Chaos verdichtet
for k, n in [('sams', 62), ('nacht', 65), ('zwei1', 64), ('fallen', 61)]: pluck(n, K[k], .05, -.2, 5)
for k, n in [('krank', 69), ('anrufe', 70), ('luecken', 72), ('ueberall', 73)]: pluck(n, K[k], .045, .2, 6)
# 2) selbst einspringen: nur Herzschlag, tiefer Akkord
for a in np.arange(K['und1'], K['mit'] - .5, .85): sub(36, a, .12, .16); sub(36, a + .22, .1, .1)
pad([38, 50, 53, 58], K['und1'], K['mit'] - .3, .02)
pluck(62, K['dritten'], .06, 0, 3); pluck(58, K['dritten'] + .02, .05, 0, 3)
# 3) Lichtpunkt: aufsteigender Ton (kein Rauschwisch), dann heller Akkord mit Logo
t = tt(.5); f = hz(62) * 2 ** (2 * t / .5); put(M, K['mit'] - .5, np.sin(2 * np.pi * np.cumsum(f) / SR) * (t / .5) ** 2 * .05)
for n in [50, 62, 66, 69, 74, 78]: bell(n, K['mit'], .03)
pad([62, 66, 69, 73], K['mit'], K['nach'], .016, .5)
# 4) Lösung: 120 BPM, D – A – h – G
PROG = [[38, 62, 66, 69], [45, 61, 64, 69], [47, 62, 66, 71], [43, 62, 67, 71]]
a = K['melden'] - .1; i = 0
while a < K['und2'] - .2:
    c = PROG[(i // 4) % 4]
    if a < K['nach'] - .05 or a > K['besetzt'] - .05:  # im 48-Std.-Moment nur Zählen
        if i % 2 == 0: kick(a, .24)
        if i % 4 == 2: clap(a, .045)
        hat(a + B / 2, .016)
        if i % 4 == 0: sub(c[0], a, B * 3.8, .12)
        pluck(c[1 + i % 3] + 12, a, .035, -.3 + .3 * (i % 3)); pluck(c[1 + (i + 1) % 3] + 12, a + B / 2, .028, .3)
    i += 1; a += B
# 48 Std.: Zählwerk steigt, dann Erfolgsakkord bei „besetzt“
for j in range(16):   # V7: Anlauf bis zur Zahl (die Zahl selbst zählt nicht mehr, sie steht auf „achtundvierzig“)
    a = K['spaet'] + j * (K['n48'] - K['spaet']) / 16; pluck(74 + j % 5, a, .02, -.4 + j * .05, 14)
for n in [50, 62, 66, 69, 74, 78, 81]: bell(n, K['besetzt'], .03, 0)
# 5) Wochenende: leichte Glocken in D-Dur, weniger Beat
for j, n in enumerate([78, 81, 83, 86, 83, 81, 78, 76]): bell(n, K['und2'] + j * .28, .035, -.3 + .08 * j)
pad([50, 62, 66, 69, 74], K['und2'], K['pb'] + .3, .02, .6)
for a in np.arange(K['und2'], K['pb'] - .1, B): hat(a + B / 2, .012)
# 6) Schluss: Groove leise weiter, Klick, Schlussakkord
a = K['pb']; i = 0
while a < DUR - 1.3:
    c = PROG[[0, 3, 0, 1][(i // 4) % 4]]
    if i % 2 == 0: kick(a, .2)
    hat(a + B / 2, .014); pluck(c[1 + i % 3] + 12, a, .03, -.2 + .2 * (i % 3))
    if i % 4 == 0: sub(c[0], a, B * 3.8, .1)
    i += 1; a += B
for n in [38, 50, 62, 66, 69, 74, 78]: bell(n, K['schicht2'] + .15, .035)
M = reverb(M, 1.6, .2)

# --- Effekte ---
def click(a, amp=.06, f=2500, pan=0):
    t = tt(.03); put(S, a, (np.sin(2 * np.pi * f * t) * .5 + np.diff(np.concatenate([[0], R.standard_normal(len(t))])) * .5) * np.exp(-t * 300) * amp, pan)
def buzz(a, d, amp=.08, pan=0):  # Handy vibriert
    t = tt(d); put(S, a, np.sign(np.sin(2 * np.pi * 170 * t)) * (np.sin(2 * np.pi * 9 * t) > 0) * np.clip((d - t) / .05, 0, 1) * amp * .5, pan)
def ping(a, n, amp=.05, pan=0):
    t = tt(.5); put(S, a, (np.sin(2 * np.pi * hz(n) * t) + .3 * np.sin(2 * np.pi * hz(n + 12) * t)) * np.exp(-t * 9) * amp, pan)
def tap(a, amp=.06, pan=0):  # Karte landet
    t = tt(.12); put(S, a, (np.sin(2 * np.pi * (140 + 80 * np.exp(-t * 60)) * t) * np.exp(-t * 40)) * amp, pan)
# Plan fährt ein, Lücken werden rot
tap(.5, .05, .3)
for a in [K['zwei1'], K['pflege']]: ping(a, 52, .05, .3); tap(a, .04, .3)
# Chaos: Krankmeldung, Anruf (vibriert), Nachricht, Kalenderfelder
tap(K['krank'] + .1, .06, .1); ping(K['krank'] + .05, 64, .03, .1)
buzz(K['anrufe'], .5, .1, .6); buzz(K['anrufe'] + .7, .4, .07, .6)
ping(K['da'], 76, .04, .6); ping(K['da'] + .08, 81, .03, .6)
for j in range(8): click(K['ueberall'] - .1 + j * .06, .05, 1800, .2)
# Sie springen ein: Avatar setzt sich in die Lücke; drei Markierungen im Monat
tap(K['selbst'] + .1, .07);
for a in [K['dritten'] - .4, K['dritten'] - .2, K['dritten']]: tap(a, .06, .2); ping(a, 50, .03, .2)
# Formular: Tastatur, Senden-Klick
for f0 in [K['melden'], K['luecke'], K['in1'] - .05]:   # V7: Felder springen gefüllt ein (nichts wird getippt)
    click(f0 - .12, .05, 3000, .3); click(f0 - .06, .04, 3400, .3)
click(K['minuten'], .1, 1500); ping(K['minuten'] + .2, 81, .04, .3)
# Karten landen, Häkchen, Karten-Pins
for j in range(3):
    t0 = K['gepr'] - .15 + j * .16; tap(t0 + .35, .06, -.4 + .4 * j)
    for k in range(3): ping(t0 + .45 + k * .18, 86 + k * 2, .02, -.4 + .4 * j)
for j in range(3): ping(K['region'] + .2 + j * .15, 79 + j * 3, .035, .5); tap(K['region'] + .2 + j * .15, .03, .5)
# 48 Std.: Zahl rastet ein, Lücken füllen sich
tap(K["n48"] + .1, .08)
for d in [0, .35]: ping(K['besetzt'] + d, 74 + d * 10, .04, .2)
# Wochenende: Benachrichtigung, zwei Vögel
ping(K['ihnen'] - .3, 88, .04, .4); ping(K['ihnen'] - .22, 93, .03, .4)
for a0, n, pan in [(K['sams2'], 84, -.5), (K['gehoert'], 86, -.4), (K['und2'] + .1, 79, .5)]: ping(a0, n, .035, pan); tap(a0, .03, pan)  # Plaketten und Bild erscheinen
# Schluss: Logo, Mauszeiger klickt
tap(K['pb'] - .05, .06); click(K['schicht2'], .12, 1400); ping(K['schicht2'] + .1, 86, .04)
S = reverb(S, .6, .1)
os.makedirs('out', exist_ok=True)
for name, buf, pk in [('musik', M, .6), ('sfx', S, .8)]:
    sf.write(f'out/{name}.wav', (buf / (np.abs(buf).max() + 1e-9) * pk).astype(np.float32), SR)
print('ok')

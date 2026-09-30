#!/usr/bin/env python3
"""Musikbett und Soundeffekte, komplett im Code synthetisiert (keine Samples, keine API).

Nutzung:
  python3 musik.py --dauer 30 --out out/musik.wav \
      [--stimmung warm|hell|dunkel|spannung|verspielt|elegant|retro] [--bpm 100] [--seed 1] \
      [--sfx out/sfx.json]

sfx.json (optional): [{"t": 1.20, "typ": "pop"}, {"t": 4.0, "typ": "whoosh"}, ...]
Typen: pop, klick, whoosh, swoosh_hoch, tick, ding, thump, glitzer, tipp (Tastatur), papier
Die Effekte landen auf out/sfx.wav (separat, damit mix.py sie getrennt pegeln kann).
"""
import argparse, json, os, wave
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument('--dauer', type=float, required=True); ap.add_argument('--out', default='out/musik.wav')
ap.add_argument('--stimmung', default='warm'); ap.add_argument('--bpm', type=float, default=0)
ap.add_argument('--seed', type=int, default=1); ap.add_argument('--sfx', default='')
a = ap.parse_args()
SR = 48000
rng = np.random.default_rng(a.seed)

def midi(n): return 440.0 * 2 ** ((n - 69) / 12)
# Akkorde als MIDI-Grundton + Intervalle; Progressionen je Stimmung
MOODS = {
    'warm':      dict(bpm=92,  prog=[(57, [0, 4, 7, 11]), (53, [0, 4, 7, 11]), (60, [0, 4, 7, 9]), (55, [0, 4, 7, 10])], pad=0.22, pluck=0.16, bass=0.20, drums=0.10, bright=0.5),
    'hell':      dict(bpm=112, prog=[(60, [0, 4, 7, 11]), (57, [0, 3, 7, 10]), (53, [0, 4, 7, 9]), (55, [0, 4, 7, 10])], pad=0.16, pluck=0.20, bass=0.22, drums=0.20, bright=0.8),
    'dunkel':    dict(bpm=84,  prog=[(50, [0, 3, 7, 10]), (46, [0, 4, 7, 11]), (48, [0, 4, 7]), (45, [0, 3, 7, 10])], pad=0.26, pluck=0.08, bass=0.24, drums=0.12, bright=0.25),
    'spannung':  dict(bpm=100, prog=[(52, [0, 3, 7]), (52, [0, 3, 8]), (50, [0, 3, 7]), (47, [0, 4, 7])], pad=0.2, pluck=0.14, bass=0.26, drums=0.22, bright=0.4),
    'verspielt': dict(bpm=118, prog=[(60, [0, 4, 7]), (65, [0, 4, 7]), (67, [0, 4, 7, 10]), (60, [0, 4, 7])], pad=0.1, pluck=0.24, bass=0.18, drums=0.16, bright=0.9),
    'elegant':   dict(bpm=76,  prog=[(55, [0, 4, 7, 11, 14]), (52, [0, 3, 7, 10]), (48, [0, 4, 7, 11]), (50, [0, 3, 7, 10])], pad=0.24, pluck=0.12, bass=0.16, drums=0.0, bright=0.45),
    'retro':     dict(bpm=120, prog=[(57, [0, 3, 7]), (53, [0, 4, 7]), (60, [0, 4, 7]), (55, [0, 4, 7])], pad=0.08, pluck=0.18, bass=0.2, drums=0.18, bright=0.7, square=True),
}
M = MOODS.get(a.stimmung, MOODS['warm'])
bpm = a.bpm or M['bpm']; beat = 60 / bpm; bar = 4 * beat
N = int(a.dauer * SR); t = np.arange(N) / SR
mix = np.zeros((N, 2), np.float32)

def env(n, att, rel, sustain=True):
    e = np.ones(n, np.float32); na = min(n, int(att * SR)); nr = min(n, int(rel * SR))
    if na: e[:na] = np.linspace(0, 1, na)
    if nr: e[-nr:] *= np.linspace(1, 0, nr)
    return e

def lowpass(x, cutoff):
    alpha = np.exp(-2 * np.pi * cutoff / SR); y = np.zeros_like(x); acc = 0.0
    # einfacher Einpol-Tiefpass, vektorisiert in Blöcken
    b = 1 - alpha
    from itertools import accumulate
    y = np.array(list(accumulate(x * b, lambda p, v: p * alpha + v)), dtype=np.float32)
    return y

def add(sig, start, pan=0.0, gain=1.0):
    i0 = int(start * SR); i1 = min(N, i0 + len(sig))
    if i1 <= i0 or i0 < 0: return
    s = sig[:i1 - i0] * gain
    mix[i0:i1, 0] += s * (1 - max(0, pan)); mix[i0:i1, 1] += s * (1 + min(0, pan))

def osc(freq, n, kind='saw', phase=0.0):
    tt = np.arange(n) / SR
    if kind == 'sine': return np.sin(2 * np.pi * freq * tt + phase).astype(np.float32)
    if kind == 'square': return np.sign(np.sin(2 * np.pi * freq * tt + phase)).astype(np.float32) * 0.6
    if kind == 'tri': return (2 * np.abs(2 * ((freq * tt + phase) % 1) - 1) - 1).astype(np.float32)
    return (2 * ((freq * tt + phase) % 1) - 1).astype(np.float32)

prog = M['prog']; nbars = int(np.ceil(a.dauer / bar)) + 1
for b in range(nbars):
    root, ints = prog[b % len(prog)]; start = b * bar; n = int(bar * SR * 1.15)
    # Pad: verstimmte Sägezähne, gefiltert
    if M['pad']:
        pad = np.zeros(n, np.float32)
        for k in ints:
            f = midi(root + k)
            for det in (-0.12, 0.12):
                pad += osc(f * 2 ** (det / 12), n, 'saw', rng.random())
        pad = lowpass(pad / (len(ints) * 2), 700 + 1600 * M['bright'])
        add(pad * env(n, bar * 0.35, bar * 0.4), start, 0, M['pad'])
    # Bass auf Zählzeit 1 und 3
    if M['bass']:
        for q in (0, 2):
            nb = int(beat * 1.6 * SR); f = midi(root - 12)
            s = osc(f, nb, 'sine') + 0.3 * osc(f * 2, nb, 'sine')
            add(s * env(nb, 0.01, beat * 1.2), start + q * beat, 0, M['bass'])
    # Pluck-Arpeggio in Achteln
    if M['pluck']:
        notes = [root + 12 + k for k in ints] + [root + 24 + ints[0]]
        for e in range(8):
            if rng.random() < 0.2: continue
            f = midi(notes[(e * 2 + b) % len(notes)]); nb = int(beat * 0.9 * SR)
            kind = 'square' if M.get('square') else 'tri'
            s = osc(f, nb, kind) + 0.35 * osc(f * 2, nb, 'sine')
            dec = np.exp(-np.arange(nb) / SR * (9 if not M.get('square') else 14)).astype(np.float32)
            add(s * dec, start + e * beat / 2, (-0.5 if e % 2 else 0.5), M['pluck'])
    # dezente Perkussion
    if M['drums']:
        for q in range(4):
            if q % 2 == 0:
                nb = int(0.35 * SR); tt = np.arange(nb) / SR
                kick = np.sin(2 * np.pi * (48 + 90 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 9)
                add(kick.astype(np.float32), start + q * beat, 0, M['drums'] * 1.4)
            nb = int(0.06 * SR); hat = rng.standard_normal(nb).astype(np.float32)
            hat = (hat - lowpass(hat, 6000)) * np.exp(-np.arange(nb) / SR * 60)
            add(hat, start + q * beat + beat / 2, 0.3, M['drums'] * 0.5)

# Ein- und Ausblenden
fade_in, fade_out = int(0.8 * SR), int(2.0 * SR)
mix[:fade_in] *= np.linspace(0, 1, fade_in)[:, None]; mix[-fade_out:] *= np.linspace(1, 0, fade_out)[:, None]
mix /= max(1e-6, np.abs(mix).max()); mix *= 0.8

def save(path, x):
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())
save(a.out, mix)
print(a.out, f'{a.dauer:.1f}s, {a.stimmung}, {bpm:.0f} bpm')

# ---------- Soundeffekte ----------
if a.sfx and os.path.exists(a.sfx):
    fx = np.zeros((N, 2), np.float32)
    def put(sig, st, pan=0, g=1.0):
        i0 = int(st * SR); i1 = min(N, i0 + len(sig))
        if i0 < 0 or i1 <= i0: return
        s = sig[:i1 - i0] * g; fx[i0:i1, 0] += s * (1 - max(0, pan)); fx[i0:i1, 1] += s * (1 + min(0, pan))
    def noise(n): return rng.standard_normal(n).astype(np.float32)
    for c in json.load(open(a.sfx)):
        typ, st = c['typ'], float(c['t']); g = float(c.get('gain', 1)); pan = float(c.get('pan', 0))
        if typ == 'pop':
            n = int(0.12 * SR); tt = np.arange(n) / SR
            s = np.sin(2 * np.pi * (380 + 900 * np.exp(-tt * 40)) * tt) * np.exp(-tt * 28)
        elif typ in ('klick', 'tick'):
            n = int(0.03 * SR); s = noise(n) * np.exp(-np.arange(n) / SR * (200 if typ == 'klick' else 320))
            s = s - lowpass(s, 2500)
        elif typ in ('whoosh', 'swoosh_hoch'):
            n = int(0.55 * SR); tt = np.arange(n) / SR; s = noise(n)
            cut = 400 + 3000 * (tt / tt[-1] if typ == 'swoosh_hoch' else np.sin(np.pi * tt / tt[-1]))
            y = np.zeros(n, np.float32); acc = 0.0
            for i in range(0, n, 256):
                al = np.exp(-2 * np.pi * cut[i] / SR)
                blk = s[i:i + 256]; o = np.empty_like(blk)
                for j, v in enumerate(blk): acc = acc * al + v * (1 - al); o[j] = acc
                y[i:i + 256] = o
            s = y * np.sin(np.pi * tt / tt[-1]) ** 2 * 3
        elif typ == 'ding':
            n = int(1.2 * SR); tt = np.arange(n) / SR; f = float(c.get('f', 1320))
            s = (np.sin(2 * np.pi * f * tt) + 0.4 * np.sin(2 * np.pi * f * 2.76 * tt)) * np.exp(-tt * 4)
        elif typ == 'thump':
            n = int(0.45 * SR); tt = np.arange(n) / SR
            s = np.sin(2 * np.pi * (45 + 70 * np.exp(-tt * 25)) * tt) * np.exp(-tt * 8) * 1.4
        elif typ == 'glitzer':
            n = int(0.9 * SR); s = np.zeros(n, np.float32)
            for k in range(7):
                o = int(rng.random() * 0.5 * SR); m = int(0.25 * SR); tt = np.arange(m) / SR
                f = 2000 + rng.random() * 3000
                s[o:o + m] += (np.sin(2 * np.pi * f * tt) * np.exp(-tt * 18))[:len(s[o:o + m])] * 0.4
        elif typ == 'tipp':
            n = int(0.6 * SR); s = np.zeros(n, np.float32)
            for k in range(6):
                o = int(k * 0.09 * SR + rng.random() * 0.02 * SR); m = int(0.025 * SR)
                blk = noise(m) * np.exp(-np.arange(m) / SR * 250); s[o:o + m] += (blk - lowpass(blk, 1800))[:len(s[o:o + m])]
        elif typ == 'papier':
            n = int(0.35 * SR); s = noise(n); s = (s - lowpass(s, 1500)) * np.exp(-np.arange(n) / SR * 9) * 0.6
        else:
            continue
        put(np.asarray(s, np.float32), st, pan, g)
    if np.abs(fx).max() > 0: fx /= np.abs(fx).max(); fx *= 0.8
    save(os.path.join(os.path.dirname(a.out) or '.', 'sfx.wav'), fx)
    print('sfx.wav geschrieben')

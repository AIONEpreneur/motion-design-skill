#!/usr/bin/env python3
"""Misst Schnitt-/Bewegungsdichte und Farbigkeit eines Videos (für Original-vs-Nachbau-Vergleich).
Nutzung: python3 dichte.py video.mp4 [--crop x:y:w:h]   -> JSON-Zeile
Werte: schnitte_pro_10s, bewegung (Anteil Pixel, die sich je 0,1 s ändern, Mittel in %),
standbild_anteil (% der Zeit ohne sichtbare Bewegung), farbigkeit (Hasler-Süsstrunk), sekunden."""
import sys, json, subprocess, numpy as np
W, H, FPS = 320, 180, 10
f = sys.argv[1]; crop = sys.argv[sys.argv.index('--crop') + 1] if '--crop' in sys.argv else None
vf = (f'crop={crop},' if crop else '') + f'fps={FPS},scale={W}:{H}'
raw = subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-i', f, '-vf', vf, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3).astype(np.float32)
g = fr.mean(3)
d = np.abs(np.diff(g, axis=0)) > 12
mot = d.mean((1, 2))
def hist(x):
    q = (x // 64).astype(int); h = np.bincount((q[..., 0] * 16 + q[..., 1] * 4 + q[..., 2]).ravel(), minlength=64)
    return h / h.sum()
hs = np.array([hist(x) for x in fr])
hd = np.abs(np.diff(hs, axis=0)).sum(1)
cut = (hd > .45) & (mot > .35)
# benachbarte Schnitte zusammenfassen
n = 0; last = -99
for i in np.where(cut)[0]:
    if i - last > 3: n += 1
    last = i
rg = fr[..., 0] - fr[..., 1]; yb = .5 * (fr[..., 0] + fr[..., 1]) - fr[..., 2]
col = (np.sqrt(rg.std((1, 2)) ** 2 + yb.std((1, 2)) ** 2) + .3 * np.sqrt(rg.mean((1, 2)) ** 2 + yb.mean((1, 2)) ** 2)).mean()
sek = len(fr) / FPS
print(json.dumps({'sekunden': round(sek, 1), 'schnitte_pro_10s': round(n / sek * 10, 1), 'bewegung': round(float(mot.mean()) * 100, 1),
                  'standbild_anteil': round(float((mot < .005).mean()) * 100), 'farbigkeit': round(float(col), 1)}))

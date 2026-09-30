#!/usr/bin/env python3
"""Text-Sync-Prüfung: alle 0,5 s ein Bild, darunter das in diesem Halbsekunden-Fenster gesprochene Wort.
Nutzung: python3 textbogen.py <video.mp4> <vo.json> <ausgabe_präfix>   -> <präfix>_teil1.jpg, _teil2.jpg, …
Damit prüft man: Steht der Text/das Bild da, wenn das Wort kommt? Wird irgendwo getippt oder umschrieben?"""
import glob, json, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont
video, vo, pre = sys.argv[1:4]
F = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 20)
d = tempfile.mkdtemp()
subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-i', video, '-vf', 'fps=2,scale=400:-2', f'{d}/%03d.png'], check=True)
words = json.load(open(vo, encoding='utf-8'))['words']
fs = sorted(glob.glob(d + '/*.png'))
for part in range(0, len(fs), 30):
    chunk = fs[part:part + 30]; W, H = 400, 225 + 44
    out = Image.new('RGB', (6 * W, 5 * H), 'white'); dr = ImageDraw.Draw(out)
    for i, f in enumerate(chunk):
        t = (part + i) * 0.5 + 0.25; x, y = (i % 6) * W, (i // 6) * H
        out.paste(Image.open(f), (x, y))
        said = ' '.join((w.get('text') or w['w']) for w in words if t - 0.5 <= w['start'] < t)
        dr.rectangle([x, y + 225, x + W, y + H], fill='black'); dr.text((x + 4, y + 227), f'{t:4.1f}s  {said}'[:40], fill='yellow', font=F)
    p = f'{pre}_teil{part // 30 + 1}.jpg'; out.save(p, quality=85); print(p)

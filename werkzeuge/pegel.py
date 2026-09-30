#!/usr/bin/env python3
"""Pegelkurve zum Nachprüfen einzelner Wortanfänge (so wurden bei 02/03 die korrekten Zeiten gefunden).

Nutzung:  python3 pegel.py out/vo.wav 9.0 9.8
Ausgabe:  Pro 25 ms eine Zeile: Zeit, Pegel in dB, Balken, Zischlaut-Anteil (hohe Frequenzen).
Lesen:    Stille ≈ Grundpegel. Einatmer: leicht über Grund (≈ 10–15 dB), rauschig, kurz. Wortanfang = Sprung auf
          Sprachpegel (≈ 25–40 dB über Grund). Zischlaute (s, sch, z, f) zeigen hohen Zischanteil bei mittlerem Pegel.
Stimmt ein Wort in vo.json nicht, den Wert in out/vo.json korrigieren und danach zeiten.py erneut ausführen.
"""
import subprocess, sys
import numpy as np
wav, a, b = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]); sr = 16000
raw = subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-i', wav, '-ac', '1', '-ar', str(sr), '-f', 'f32le', '-'], capture_output=True).stdout
y = np.frombuffer(raw, np.float32)
e_all = np.array([np.sqrt((y[i:i + 400] ** 2).mean()) for i in range(0, len(y) - 400, 400)])
grund = np.percentile(20 * np.log10(e_all + 1e-6), 15)
print(f'Grundpegel {grund:.0f} dB')
for t in np.arange(a, b, .025):
    s = y[int(t * sr):int((t + .025) * sr)]
    if len(s) < 50: break
    db = 20 * np.log10(np.sqrt((s ** 2).mean()) + 1e-6)
    sp = np.abs(np.fft.rfft(s * np.hanning(len(s)))); f = np.fft.rfftfreq(len(s), 1 / sr)
    zisch = sp[f > 3500].sum() / (sp.sum() + 1e-9)
    bar = '#' * max(0, int((db - grund) / 2))
    print(f'{t:6.3f}  {db:6.1f}  {bar:<30s}  zisch {zisch:.2f}')

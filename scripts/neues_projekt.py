#!/usr/bin/env python3
"""Legt ein neues Erklärvideo-Projekt an und kopiert die technische Vorlage des gewählten Stils hinein.

Nutzung:  python3 neues_projekt.py <stil-nr> <kunden-slug>
          z. B. python3 neues_projekt.py 12 kanzlei-mueller
Ergebnis: ./erklaervideos/<kunden-slug>/ (im aktuellen Arbeitsordner)
          film/     Film-Code der Vorlage (Startpunkt, die Geschichte wird komplett neu gebaut)
          ton/      Partitur der Vorlage (Musik und Geräusche, Zeiten kommen später aus K)
          zeiten.py Muster: leitet K (Bildzeitpunkte) aus out/vo.json ab
          STIL.md   die Stilbeschreibung aus der Wissensbasis
          out/      leer
Vorhandene Projekte werden nie überschrieben.
"""
import json, os, shutil, sys
SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASIS = os.path.join(os.getcwd(), 'erklaervideos')
nr, slug = sys.argv[1].zfill(2), sys.argv[2]
kat = {s['nr']: s for s in json.load(open(os.path.join(SKILL, 'references/stile/katalog.json'), encoding='utf-8'))['stile']}
if nr not in kat: sys.exit(f'Stil {nr} gibt es nicht (01–22).')
ziel = os.path.join(BASIS, slug)
if os.path.exists(ziel): sys.exit(f'{ziel} existiert schon. Anderen Namen wählen.')
v = os.path.join(SKILL, kat[nr]['vorlage'])
os.makedirs(os.path.join(ziel, 'out'))
for teil in ('film', 'ton'):
    if os.path.isdir(os.path.join(v, teil)):
        shutil.copytree(os.path.join(v, teil), os.path.join(ziel, teil), ignore=shutil.ignore_patterns('*.mp4', 'frames', 'render*', '__pycache__'))
shutil.copy(os.path.join(v, 'zeiten.py'), os.path.join(ziel, 'zeiten.py'))
shutil.copy(os.path.join(SKILL, f'references/stile/{nr}.md'), os.path.join(ziel, 'STIL.md'))
print(ziel)

# STILBIBEL V5 – SaaS-Launch im Notion-Look (Notion-Launch-Video, HyperFrames)

Referenz: `ref/player_240-292.mp4` (Player-Ausschnitt, 52 s). 18 Einzelbilder in `ref_frames/`, dazu Vollansichten von r_5, r_11, r_23, r_29,
r_32, r_36, r_44. Farben per PIL (5×5-Median).

## Die 5 Erkennungsmerkmale
1. **Warmes Fast-Weiß** (#f4f5eb) als Grund, dazwischen **neutrale Anthrazit-Szenen** (#1f1f1c Mitte → #141412 Rand) – harte Schnitte hell↔dunkel.
2. **Inter-Bold-Headlines**, eng gesetzt (−3,5 % Laufweite), schwarz bzw. weiß, mit **genau einem blauen Wort/Satzteil** (#0b74de, auf Dunkel #3d8ff0);
   Wörter erscheinen einzeln aus der Unschärfe (14 px → 0, 26 px Aufstieg, 0,42 s, power3.out).
3. **Echte, dichte Produkt-Oberflächen**: weiße Fenster mit 1,5-px-Rand #e6e6e1, drei graue Fensterpunkte, Brotkrumen, Tabellen mit Notion-Tag-Pillen,
   Pfirsich-Kopfband, sehr weiche große Schatten; UI fährt mit 3D-Neigung (rotateX) von unten ein.
4. **Notion-Figuren**: schwarze Tuschelinien, graue Gesichter mit Rasterpunkt-Schatten, schwarze Haarflächen, kleine Plaketten-Kreise mit
   dicker Kontur (blau/gold/weiß) um den Kopf, Porträt im roten Ring; blaue **Pille mit Punkt** im Headline-Satz („• Ship“ → „• Ihnen.“).
5. **Launch-Dramaturgie**: dunkles Chaos-Intro mit weißen App-Kacheln, das in einen Lichtpunkt zusammenfällt; Overlay-Moment mit riesiger blauer
   Zahl über unscharfer UI („24/7“ → „48 Std.“); Schluss mit Logo + Wortmarke, grauer Tagline, blauem CTA mit Glow-Halo, Mauszeiger klickt.

## Palette (gemessen)
| Rolle | Hex |
|---|---|
| Grund hell | #f4f5eb |
| Tinte | #161611 (gemessen #1b1b19) |
| Akzentblau / auf Dunkel | #0b74de (gemessen #0f70c5…#0071cc) / #3d8ff0 (gemessen #3696e7) |
| Dunkel Mitte / Rand | #1f1f1c / #141412 |
| Fensterfläche / Rand | #ffffff (gemessen #fafcfa) / #e6e6e1 |
| Sekundärtext | #9a9d9a (gemessen #9fa098) |
| Pille hellblau | #dde9f2 |
| Tags grün / rot / blau / gelb | #dcefe3 / #f9dcdc / #dbe9f7 / #f5e6c0 |
| Porträt-Ring rot | #de5951 |
| Gesichtsgrau | #d4d5d1 (gemessen #b4b6b4 inkl. Raster) |

## Typografie
- Inter 700, 96–124 px, Zeilenabstand ≈1,05; Unterzeile Inter 500 32–42 px grau; UI-Text Inter 500/600 17–25 px.
- Mono (JetBrains Mono) nur für Zähler „03 / 04“ und die URL unter dem CTA – wie „01 / 04“ und „NOTION.COM“ im Original. Keine Mono-Kicker.

## Bildaufbau / Bewegung
- Links Headline, rechts UI (wie „Bring everything…“); Karten oben, Headline unten links (wie „Get answers…“); zentrierte Headline mit Figuren
  links/rechts (wie „Where teams and agents…“); Schlussbild zentriert.
- Jede Einstellung schiebt langsam hinein (6 %, dunkles Zitat 10 %, Schluss 12 %); innerhalb Hell: Unschärfe-Überblendung 0,22 s.
- Tippen in Formularfeldern mit Cursor, Klick → Button „Gesendet ✓“ und Hinweis-Chip; Karten fliegen gestaffelt mit Unschärfe ein.

## Stilvergleich-Protokoll
**Runde 1** (`out/stilvergleich_1.jpg`): Headlines, Pillen, UI-Fenster, Schlussbild wirken wie aus demselben Launch-Video. Abweichungen:
dunkle Szenen blaustichig (Glow zu stark), Karten der Fachkräfte-Szene kleiner und luftiger als die Dashboard-Karten im Original,
Tagline im Schlussbild schwarz statt grau, Mono-Versalien „PERSONAL“ als Kicker (Original hat keinen).
→ Blauschimmer 0,35 → 0,16, Karten und Karte +10 % und enger gesetzt, Tagline #55564f in Inter 450, „Personal“ als graue Fortsetzung der Wortmarke.

**Runde 2** (`out/stilvergleich_2.jpg`): Überzeugt. Danach nur Bewegung ergänzt (Stillstand 29 % → 0 %: stärkere Push-ins, „48 Std.“ zählt hoch und wächst).

**Runde 3** (`out/stilvergleich_3.jpg`): Endstand.

## Messwerte
- `dichte.py` Film: Standbild-Anteil 0 %, Bewegung 4,2 %, Farbigkeit 16,5 (Original: 48 % / 2,7 % / 16,5 – Farbigkeit identisch).
- Timing-Streifen `out/strip_*.jpg` (zwei, Lücken, selbst, zwei Minuten, Fachkräfte, 48, besetzt, Samstag): Bild steht vor Wortbeginn.

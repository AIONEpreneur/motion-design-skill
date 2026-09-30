# STILBIBEL V5 – Pixel-Art (Ahmed T'aide, „It Wrote Every Frame“, Welt 1)

Referenz: `ref/vollbild_136-156.mp4` (1280×720, Vollbild ohne Webcam). 16 Einzelbilder in `ref_frames/`, Ausschnitte 2× (Sonne/Raster, Boden/Figur).
Maßstab gemessen: 1 Weltpixel = 4 px bei 1280 → **Welt 320×180**, bei 1920 Faktor 6, ohne Glättung.

## Die 5 Erkennungsmerkmale
1. **Echte 320×180-Pixel**, harte Treppenkanten, keine Verläufe – Übergänge nur als geordnetes Raster (Bayer 4×4, Punktgitter, Schachbrett).
2. **Synthwave-Kulisse in Parallax-Ebenen**: Nachtblau mit Einzelpixel-Sternen und flachen Wolkenbalken → Magenta-Punktband → rosa Horizontglühen
   mit Orangepunkten → Magenta-Hügel → Silhouette mit gelben Fensterpixeln → Magenta-Tannen → nachtblaue Tannen → neongrüne Grasnarbe, Ziegelboden mit Sprenkeln.
3. **Gestreifte Sonne**: Gelb oben, Orange-Band, Rot unten mit nach unten breiter werdenden Streifenlücken.
4. **Boss-Kampf-Grammatik**: Namen + Lebensbalken oben links/rechts (weiße Pixelschrift, grüner/roter Balken mit weißem Restbalken), Warnschrift,
   Sprung als Parabel, Sichelhieb, **Hit-Stop** (Standbild, Gegner weiß → rot, Punch-in 1,4×, Wackeln), Zerfall in Münzen auf gepunkteten Bahnen.
5. **Pixelschrift in Versalien mit harter Schlagschatten-/RGB-Versatzkante** („!! BOSS !!“, „HIT-STOP“, „VICTORY!“), plus eine glatte fette Grotesk nur
   für die Info-Plakette (gelbe Rubik ExtraBold in dunkler Box mit gelbem Rand und Punktleiste).

## Palette (PIL, Mediancut auf r_8.5 / r_13 / r_19.5 + Stichproben)
| Rolle | Hex |
|---|---|
| Himmel / oben | #1b2a50 / #172141 |
| Magenta (Band, Hügel, Silhouette, ferne Tannen) | #7c2550 |
| Rosa Raster / Glühen | #ff81c1 (Siegtext #fc7bad) |
| Sonne Gelb / Orange / Rot | #fcec25 / #fda300 / #e70047 |
| Gras / Gras dunkel | #00e432 / #00864e |
| Ziegel / Fuge / Sprenkel | #96443c / #7a382e / #f3d3b0 |
| Kontur / Schatten | #1b172c / #111022 |
| Held Orange / Bildschirm / Augen | #f88954 / #291f41 / #67ffdf |
| Wolke hell / dunkel | #eb649f / #922d69 |
| Creme (Treffer-Silhouette) | #fef2ea |

## Raster, Linien, Figuren
- Kontur 1 Weltpixel dunkel, keine Anti-Aliasing-Kanten. Dither-Zeilen: y 44–55 Nacht→Magenta, 66–81 Magenta→Rosa, ab 92 Orangepunkte im 3er-Gitter.
- Held im Original: Bildschirm-Roboter 25 px. Hier: **Fahrschulauto 30×20 px** mit Bildschirm-Kabine und zwei Cyan-Augen (gleiche Konstruktion), Dachschild.
- Boss im Original: grüner Schleimkönig mit Krone. Hier: **Prüfungs-Ampel** 48×88 px mit Krone, rote Lampe mit Wutgesicht; beim Sieg wird sie grün und lächelt.
- Stadtsilhouette statt Burg (gleiche Magenta-Technik, gelbe Fensterpixel, Fahne), Straßenlaternen statt Fackeln (gleiche Flacker-Flamme).

## Typografie
- Silkscreen Bold, 5-Pixel-Raster, hart geschwellt; Titel ×3 Weltpixel (18 px/Schriftpixel), Unterzeile ×2 gelb, HUD ×1 weiß.
- Warn-/Siegwörter mit RGB-Versatz (Rot/Rosa bzw. Rot/Cyan) wie „HIT-STOP“, Farbwechsel-Blinken wie „VICTORY!“.
- Etikett-Tags über Objekten („NEUER JOB“) wie „12 FPS“/„SMOOTH“ im Original. Plakette nur für das Angebot.

## Bewegung, Kamera, Übergänge
- Figuren auf 12 fps, Kamera/Parallax weich (Ebenenfaktoren 0 / .15 / .3 / .45 / .7 / 1), ständige langsame Seitenfahrt.
- Titel fallen mit Nachfedern, Unterzeilen tippen sich ein; Himmelwechsel (Morgen) als Bayer-Raster-Überblendung; Auto baut sich per Raster auf.

## Stilvergleich-Protokoll
**Runde 1** (`out/stilvergleich_1.jpg`): Welt, Sonne, Tannen, Boden, HUD sofort als Serie erkennbar. Abweichungen: zu viel Rosa (Band 62–120 statt
nur Horizont), Stadt als durchgehende Wand statt einzelner Silhouette, Held und Boss zu klein und zu leicht gegenüber Bit/Schleimkönig,
Hieb-Sichel zu klein, Umlaut-Punkte abgeschnitten.
→ Rosa auf Zeilen 66–92 begrenzt, Nacht-Anteil größer; Stadt in 6 Turmgruppen mit Luft; Auto 30×20, Ampel 48×88, Lampen r 12; Sichel r 40; Schrift tiefer gerendert.

**Runde 2** (`out/stilvergleich_2.jpg`): Dichte und Farbanteile jetzt wie im Original. Rest: Stadtturm verdeckt die Sonne.
→ Turmgruppen so gesetzt, dass die Sonne bei allen Kamerahalten frei bleibt. Stillstand 24 % → langsame Dauerfahrt der Kamera ergänzt.

**Runde 3** (`out/stilvergleich_3.jpg`): Endstand.

## Messwerte
- `dichte.py` Film: Standbild-Anteil 0 %, Bewegung 9,0 %, Farbigkeit 85,8 (Original: 2 % / 18,4 % / 86,1).
- Timing-Streifen `out/strip_*.jpg` (Durchgefallen, zwei, ohne, Grün, links, bestanden): Wort/Bild steht vor Wortbeginn.

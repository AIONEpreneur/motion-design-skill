# STILBIBEL V5 – 13 PS1-Low-Poly (g russ, PS1-Casino, „Final Version“, Three.js)

Referenz: `ref/vollbild.mp4` = rechte Hälfte („Final Version“) der Quelle 422–512 s, Crop 640×720 (Split-Screen, links
„Version 1“ in `ref/version1.mp4`). Angesehen: 18 Bilder (`ref/sheet.jpg`), 44er-Raster der Quelle (`ref/srcsheet.jpg`),
4 Vollbilder (`ref/detail.png`).

## Palette (PIL-Messung, Median-Cut, 640×500-Ausschnitt ohne Titelzeile)
| Rolle | Hex (gemessen) | im Code |
|---|---|---|
| Teppich orange | `#fe6927` `#d86a36` `#cb7b42` | `#E8571F`/`#FE6927` + Muster Gelb `#F4B830`, Rot `#8E1E14`, Petrol `#1D8A8A` |
| Bezugsrot (Stühle, Kleid) | `#681a12` `#84230c` | Samt `#9A1C16` / `#5A0E0A` |
| Holz / Vertäfelung | `#93643e` `#6b3f25` `#7d5e4a` `#3c1f16` | `#6B3F25` / `#93643E` / Kassetten `#4A2412` |
| Wände dunkel | `#343339` `#201715` `#110804` | Nebel/Hintergrund `#0E0604`, Tapete `#2E1A14` |
| Haut hell | `#f1cfae` `#b69376` | `#F1CFAE`, Nase `#D9A57C` |
| Schrift | Weiß `#f4f4ee`, Gelb `#f2dc3c`, Kontur `#0b0b0b` | identisch |

## Hintergrund und Textur
Warme, dunkle Innenräume: Teppich mit Pixelmuster (64×64, NearestFilter), Holzkassetten, dunkle Tapete, Messing-Wandlampen
mit Lichtkegel, Nebel ins Fast-Schwarz. Alle Flächen tragen niedrig aufgelöste, verrauschte Pixeltexturen (Stoff 16×16,
Karton 16×16, Ziegel 32×32). Außenszene: Pflaster und Ziegelfassade mit warmen Fenstern bei Nacht.

## Render
640×360 Rendertarget, hart hochskaliert (3×), Vertex-Snapping auf ein 290×164-Raster (Geometrie wackelt bei Kamerafahrt),
15-Bit-Farbe (32 Stufen) mit 4×4-Bayer-Dithering, leichte Wärmung, starke Vignette. Flat-Shading, sichtbare Facetten.

## Figuren
Blockkörper mit Stofftextur, Arme/Beine aus Kästen mit Gelenken, Klötzchenhände mit Fingern. Kopf = facettierte Kugel
(7×5 Segmente, flach schattiert) mit 16×16-Pixelgesicht (weiße Augen mit blauer Iris, Brauen, Mund, Rouge) und Keilnase;
Haar als Kugelkappe + Strähnenblöcke. Mimik-Tausch über Texturwechsel (gestresst, geschockt, müde, traurig, fröhlich).

## Typografie
Pixelschrift in Versalien (Pixelify Bold), Weiß mit gelbem Schlagwort, dicke schwarze Kontur + Schlagschatten, unten
mittig, springt hart ein (kein Einblenden) – wie die Casino-Zeilen. Nur Schlagworte, keine Sätze. Dazu Schrift im Raum:
LED-Tafeln (SAMSTAG 08:00, RÜCKGABE 20:00, KISTENHELD, FESTER PREIS, BESICHTIGUNG KOSTENLOS, Neon ANGEKOMMEN),
Kartonetiketten KÜCHE/BAD/KIND/WOHNEN, Pixel-Herzen und „!“-Sprite.

## Kamera und Schnitt
Harte Schnitte alle 0,6–3 s (3,9 Schnitte/10 s, Original 3,7), langsame Dolly-Fahrten, Draufsicht von oben (Kartonraster),
Nahaufnahmen von Gesicht und Hand (Handy), Puppenhaus-Aufsicht.

## Die 5 Merkmale, an denen man den Stil sofort erkennt
1. **Warmer, nebliger Innenraum** in Orange-Rotbraun mit Teppichmuster, Holz und Lampenlicht, Ecken im Schwarz.
2. **Pixeltexturen ohne Glättung** auf allem (Stoff, Teppich, Holz, Karton) + 15-Bit-Dithering.
3. **Facettierte Low-Poly-Köpfe mit Pixelgesicht und Keilnase**, Blockkörper, Blockhaare.
4. **Vertex-Wobble / niedrige Auflösung** (PS1-Treppenkanten).
5. **Pixelschrift Weiß/Gelb mit schwarzer Kontur**, harte Schnitte.

## Runden
**Runde 1** (`out/stilvergleich_1.jpg`): Licht und Palette zu einheitlich orange (Tapete rot, Lampen zu gesättigt), Gesichter
dunkel und halb im Schatten, Kopfhaar als große Platten („Hut“), Sofa-Einstellung zeigt kein Gesicht.
→ Führungslicht von der Kamera (warmweiß), Punktlichter entsättigt, Tapete dunkelbraun, Hemisphären-Boden heller,
Sofa-Szene umgestellt (Mann zieht von oben, Gesicht zur Kamera), engere Paar-Einstellung.
**Runde 2** (`out/stilvergleich_2.jpg`): Figuren lesen sich wie im Casino. Gesichtstextur auf 16×16 mit größeren Augen
(weiß + blaue Iris) wie im Original; Schlagworte nach unten (Position der Casino-Zeilen); LED-Schilder vergrößert;
Kistenheld-Wagen ist beim Wort „Kistenheld“ im Bild; Zähler zeigt bei „hundert“ bereits 100 (Balken füllt sich).
**Runde 3** (`out/stilvergleich_3.jpg`): Haarkappe korrigiert (kein Hut, keine Glatze), Beschnitt der LED-Texte behoben.

## Messwerte
dichte.py V5: Standbild 2 %, Bewegung 14,7 %, Farbigkeit 87,3, 3,9 Schnitte/10 s
(Original-Hälfte: Standbild 1 %, Bewegung 18,6 %, Farbigkeit 72,2, 3,7 Schnitte/10 s).

## Ehrliche Abweichungen
- Etwas gesättigter/oranger als das Original (Farbigkeit 87 statt 72).
- Die Casino-Figuren haben feiner modellierte Köpfe (mehr Polygone, größere Gesichter, Kleidung mit Kragen/Rüschen);
  unsere sind schlichter, Hände und Haare blockiger.
- Das Original hat volle Räume mit vielen Statisten (Tische, Spieler, Kronleuchter); unsere Kulissen sind leerer.
- Querformat 16:9 statt der 8:9-Hälfte des Originals.

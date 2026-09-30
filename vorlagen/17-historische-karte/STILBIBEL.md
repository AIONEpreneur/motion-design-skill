# Stilbibel V5 – 17 historische Karte (Stadtbote Kurier)

Vorbild: Andy Diep „Saratoga“ (KpepgP9xhrg), Vollbild-Ausschnitt `ref/ref_crop.mp4` (1010×566, Webcam unten rechts ignoriert).
Einzelbilder: `ref/frames/f_*.png` (18 Stück), Übersicht `ref/sheet_all.jpg`, Ausschnitte `ref/z1–z4.png`.

## Palette (mit PIL gemessen)
| Rolle | Original gemessen | im Film |
|---|---|---|
| Land/Papier | #E6D9BE (Median), Titelkarte #EEE2CF Mitte, #E9DEC5 Rand | Papier-Basis #E6D9BE, Mottling ±3, Korn ±7, Randabdunklung −9 |
| Wasser/See | #E8E0CB (heller als Land) | #EAE2CD + waagrechte Schraffur alle 7 Welteinheiten, Deckkraft .16–.24 |
| Tuschelinie | Kern #544834 | #4E4230 (Linien), #3A2E1B (Titel, Wall, Kartuschentext) |
| Beschriftung | Kern ~#5E513D (Kompression verfälscht auf #946752) | #5B4E3A |
| Pinselroute | Kern #9A4333 | #9C3A2B, Trockenpinsel-Schlieren #E8C9B8 @ .22 |
| Fläche „erobert“ | ~#C9B09A, flach, eine dunkle Kante | rgba(166,112,86,.28) + Kante #6A3E2C |
| Kartusche | Grund #EBDEC8, Text #473C26 | #EDE2CC / #3A2E1B |
| Titel „Saratoga“ | #3A2E1B | #3A2E1B |
| Gegenfarbe | Blau-Grau der Amerikaner #878580 | Post = #4A5670 (Pinsel), Einheit #9BA3B0 |

## Papier
Pergament/Creme, kaum Struktur: sehr weiche Wolken, feines Korn, in Version A kaum Vignette. Im Film: prozedurales Papier
(Wertrauschen + Korn + ganz feine waagrechte Leinenlinien alle 3 px + 900 Fasern @ 5 %), darüber Faser-Multiply, damit die
Tusche „im Papier sitzt“.

## Linien
- Küsten/Flüsse: 1,5–2 px bei 1010 → im Film 2,1 px (mit Zoom ^0,45 skaliert), leichtes Handzittern (Wertrauschen entlang der
  Normalen, Amplitude 4–6 Welteinheiten, Periode 45–90), zweite feine Uferlinie @ .35 wie im Original.
- Rote Route: 9–10 px bei 1010 ≈ 18–20 px bei 1080 → Film 25 px (Übersicht), rau gefüllter Pinselstrich mit schwankender
  Breite (±14 %), rauen Rändern (±0,9 px), stumpfem Anfang, **Widerhaken-Pfeilspitze** (eingekerbte Basis).
- Wallanlage: Zickzack mit Zähnchen außen (Übertragung der „Bemis Heights“-Signatur).
- Wald: Kreise r 8–16 mit zwei Punkten in der Mitte – exakt wie Freeman's Farm.

## Detailgrad
Die Karte ist luftig: viel leeres Papier, Geografie nur als Linie, Orte als kleine Symbole (⊙ Zielring doppelt rot, ⊠ Büro).
Truppen = gestapelte, schraffierte Rechtecke → Kurier = rot schraffierter Block, Post = blaugrauer Block.
Detailszene (Freeman's Farm) = Lichtung mit gestricheltem Rand im dichten Kreiswald → Verteilzentrum als Grundriss in einer
Lichtung, gestrichelter Rand, Kreiswald ringsum.

## Typografie
- Ortsnamen: Serif, **Versalien, gesperrt** (+16–20 %), 20–30 px, #5B4E3A. Film: Iowan Old Style.
- Titel: große Buchgrotesk-Serif, normal, 140–190 px, darüber gesperrte Versalienzeile mit Linien links/rechts.
- Kartusche: Serif 40 px im Doppelrahmen mit Eckquadraten und Schnörkeln, unten links.
- **Abweichung mit Absicht:** Das Original setzt Kartusche, Untertitel und Truppennamen kursiv. Auftraggeber hasst Kursiv →
  alles aufrecht. Kicker „— THE BRITISH PLAN · 1777“ entfällt (Eck-Deko). Kartusche trägt eine kurze Botschaft, nicht den
  gesprochenen Satz (keine Untertitel).

## Bildaufbau, Kamera, Übergänge
Detail zuerst, dann Überblick (Start nah auf Titel/Uhr, Rausfahren auf die Karte); Karte zeichnet sich radial vom Ziel aus;
Kamera driftet immer; Hineinzoomen statt Schnitt (Stadt → Region → Verteilzentrum → Stadt → Kunde → Zustellnachweis);
Titelkarte mit Kompassrose am Ende wie der „Saratoga“-Titel.

## Die 5 Merkmale, an denen man den Stil erkennt
1. Cremefarbenes Pergament mit feinen, leicht zittrigen Sepia-Tuschelinien und viel Leerraum.
2. Dicke, raue, dunkelrote Pinselrouten mit Widerhaken-Pfeil, die sich zeichnen.
3. Gesperrte Serifen-Versalien für Orte, doppelter roter Zielring.
4. Doppelrahmen-Kartusche unten links mit Eckquadraten.
5. Wald aus Kreisen mit zwei Punkten, Lichtung mit gestricheltem Rand; Kompassrose hinter dem Titel.

## Stilvergleich-Runden
- **Runde 1** (`out/stilvergleich_1.jpg`): Serie erkennbar, aber die Stadt war ein dichtes Rechteck-Raster (Waffel) – das
  Original ist luftig. Fläche „gehört Ihnen“ war ein Blob, Original ist polygonal. Verteilzentrum stand auf leerem Papier.
  → Raster entfernt; Stadt nur noch aus Straßen (Hauptstraßen doppelt, Nebenstraßen einfach), kleinen Häusern an den Straßen,
  schraffierten Blöcken nur in der Altstadt; Boulevard entlang der Route freigeschnitten; Route 21 → 25 px; Fläche folgt
  Flussufer/Stadtrand und wächst radial vom Kunden; Beschriftungen ohne Hinterlegung.
- **Runde 2** (`out/stilvergleich_2.jpg`): Karte, Route, Kartusche und Titel wirken wie aus derselben Serie.
  → Verteilzentrum in Lichtung mit gestricheltem Rand und dichtem Kreiswald (Freeman's-Farm-Zitat), Häuser heller/weniger,
  Flächenfarbe heller. Danach Bewegung: Titel- und Belegszene liegen über der weiterfahrenden Karte (Standbild 39 % → 17 %).

## Messwerte (dichte.py, out/film.mp4)
sekunden 30,0 · Schnitte/10 s 0,7 · Bewegung 8,4 · **Standbild 17 %** · Farbigkeit 19,2
Timing-Streifen: `out/strip_{vertrag,post,direkt,sechzig,vier,beleg}.jpg` – jedes Bild steht zur Wortzeit.

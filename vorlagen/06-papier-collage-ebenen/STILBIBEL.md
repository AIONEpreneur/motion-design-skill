# STILBIBEL 06 – Ring Hyacinth „Moon Festival“ (p5.js) → Pfotenhaus V5

Quelle: `ref/original.mp4` (1920×1080, 24 fps, 40 s, Vollbild). Gesichtet: 15 Einzelbilder `ref/f_*.png`, Übersicht
`ref/alle.jpg` (1 Bild / 0,8 s), `ref/sechs.jpg`, Ausschnitt Papierkante `ref/crop_paper.png`.

## Die 5 Erkennungsmerkmale
1. **Gerissene Papierbahnen in Nachtblau**, übereinander geklebt; an jeder Risskante blitzt der **weiße Faserkern**
   (3–10 px, unregelmäßig), darunter ein weicher Schlagschatten.
2. **Alles ist Papier**: sichtbares Faserkorn und Sprenkel auf jeder Fläche, Sterne/Wolken/Mond als Ausschnitte mit Schatten.
3. **Getigerte Sticker-Katze**: weißer Schnittrand (≈ 8–12 px), dunkelbraune Tintenkontur, Orange mit Papierkorn,
   Streifen, cremefarbenes Maul/Bauch, riesige braune Kulleraugen mit zwei Glanzlichtern, rosa Bäckchen,
   Schnurrhaare als weiße Papierstreifen über den Rand hinaus; kleine „?“/„!“ poppen über dem Kopf.
4. **Mond mit fehlendem Stück** als Problem-Bild; am Ende ist er voll, Katze von hinten davor, Laternen auf dem Wasser.
5. **Kino-Look**: warme Tönung, starke Vignette, Tiefenschärfe (Hintergrund weich), ruhige Dauerfahrt, Goldschrift.

## Palette (PIL Median-Cut, Anteil)
| Bild | Hex |
|---|---|
| Mond f_1 | #191734 (21 %), #2f2c4a, #242543, #544858, Mond #ccbba9 / #937c75 |
| Skyline f_3 | #171b38, #353958, #1f2142, #292646, #6e6571, #ac9d98 |
| Katze auf Mauer f_5 | #1e233d, #484454, #3b3444, Katze #c59b79 / #d5bda5; Katzenfläche Mittel #ce8f53 (σ 35 = Papierkorn) |
| Schluss f_36 | #3a475a, #18203f, #222f4c, #30354e, #666268, #ba9c80 |
Unsere Setzung: Nachtblau #171b38 / #1f2142 / #292646 / #353958 / #484454, Faserkern #f1ebe1, Mond #e6d6ad,
Katze #e3a263 / Streifen #cf6f36 / Creme #f3e2c4 / Tinte #4a2818, Akzente Rot #c8352c, Gold #d9a441, Petrol #2f6d6a.
Firmenbezug: Bremen (Vorwahl 0421) – Dom mit zwei Türmen und Rathausgiebel als Papier-Skyline statt Shanghai.

## Hintergrund und Papier
Prozedurale Papierkacheln (256 px): Grundfarbe + 26 weiche Flecken + 2600 Sprenkel + 180 Fasern, als Muster gefüllt;
darüber Faserkorn als Overlay (35 %), warme Soft-Light-Tönung, Vignette 60 %.
Risskanten: Wellenrauschen (±12–30 px) + Zacken (±1,7 px), Faserkern 2,5–9,5 px, Schatten 22 px weich, 7 px Versatz.

## Linien
Nur die Katze (und Symbole) hat Tintenkontur: 6,5 px #4a2818, runde Enden. Alles andere ist konturloses Papier mit Schatten.

## Typografie
Original: nur goldene Pinsel-Kalligrafie im Schlussbild. Übertragen: Marke „Pfotenhaus“ in Kaushan Script mit
Goldverlauf #fbe3a2 → #b77a2a und Glühen; Botschaften auf **gerissenen cremefarbenen Papierstreifen mit Klebeband**
(Kalam Bold, 46 px, Tinte #3a241a), die leicht gedreht aufgeklebt werden – fertig 0,05 s vor dem Wort.

## Kamera, Bewegung, Übergänge
Ruhige Dauerfahrt (Push-in 2–3 %/s, leichtes Schweben), Parallaxe Hintergrund/Vordergrund, Hintergrund 3–4 px weich.
Übergänge: Papierbahn mit Risskante gleitet herein (wie die Bahnen im Original), Kamerablitz, senkrechter Riss (Split).
Walzen-Szene wie im Original (rot-goldener Rahmen, drei Walzen rasten nacheinander ein).

## Umsetzung (Geschichte)
Koffer schiebt sich hoch, Katze sitzt drin, Ticket klebt an, „?“ poppt – Mond mit fehlendem Stück → Flur: Nachbarin
mit eigenem Koffer, Uhr, rotes X → Kamerafahrt zur eigenen Tür: Fremder mit Schlüssel, Katze faucht (Fell gesträubt),
X, Schlüssel fliegt weg → Walzen (Nachbarin/Fremder/?) rasten dreimal auf Pfotenhaus ein → eigenes Zimmer mit Blick
auf Bremen, Katze springt aufs Fensterkissen und rollt sich ein → Scheibe Sonne/Mond dreht sich, Napf füllt sich,
Spielmaus, Hand streichelt, Herzchen → Blitz, Polaroid fliegt ans Meer auf Ihr Handy → Riss: Sie am Meer | Katze am
Fenster, das fehlende Mondstück rastet ein → Katze von hinten vor dem vollen Mond, Weser mit Laternen, Goldschrift,
Angebot, Kontakt.

## Stilvergleich
### Runde 1 (`out/stilvergleich_1.jpg`)
Befund: gleiche Serie erkennbar (Papier, Risskanten, Sticker-Katze, Mond). Abweichungen: weißer Schnittrand der Katze zu
dick (≈ 17 px statt 8–12 px); Katze zu klein im Bild; zu wenig Tiefenschärfe; Himmel ohne die goldenen Papierstreifen
des Originals; Mond im Schlussbild neben statt hinter der Katze.
Geändert: Schnittrand 34 → 24 (Schwanz 66 → 56), Katze/Koffer ×1,22, fauchende Katze 0,78 → 1,05, Zimmer ×1,28;
Hintergrundunschärfe 2,5 → 4 px (Szene 1) und 1,5 → 3 px (Flur); goldene/cremefarbene Papierstreifen im Himmel; Mond
tiefer hinter den Katzenkopf; Walzen-Symbole mit Tintenkontur (Hauswand war unsichtbar).
### Runde 2 (`out/stilvergleich_2.jpg`)
Befund: Goldstreifen kreuzten im Schlussbild die Marke → dort abgeschaltet; Ticket-Schrift ragte über den Rand → kleiner.
### Runde 3 (`out/stilvergleich_3.jpg`) nach Dauerfahrt (Standbildanteil 27 % → 0 %) – Schlussbild mit gebremster Fahrt,
damit Marke und Kontakt im Bild bleiben.

## Messwerte (dichte.py)
Film: Bewegung 9,0 %, Standbild 0 %, Farbigkeit 36,9, 2,1 Schnitte/10 s.
Original: Bewegung 17,0 %, Standbild 6 %, Farbigkeit 40,6, 3,8 Schnitte/10 s.

## Ehrliche Abweichungen
- Menschen (Nachbarin, Fremder, Sie) sind einfache Papierfiguren; im Original gibt es keine Menschen, der Detailgrad
  liegt unter dem der Katze.
- Die Katze hat weniger Posen/Mimik-Feinheiten als im Original (keine Augenbrauen-Schweißperlen, keine Ganzkörper-Drehung).
- Flur und Zimmer sind flacher geschichtet als die Skyline-Collagen des Originals (weniger Ebenen, keine Musterpapiere
  mit Schrift/Notenlinien).
- Weniger Bewegung im Bild als im Original (9 % vs. 17 %), die Figuren bewegen sich sparsamer.

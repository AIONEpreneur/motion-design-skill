# Stilbibel V5 – 18 Holzschnitt (Riegel 24 Schlüsseldienst)

Vorbild: Andy Diep, Holzschnitt-Traum „almost asleep … falling … there is no bottom“ (KpepgP9xhrg), Vollbild-Ausschnitt
`ref/ref_crop.mp4`. Einzelbilder `ref/frames/f_*.png` (16), Übersicht `ref/sheet_all.jpg`, Ausschnitte `ref/z1–z5.png`.

## Palette (mit PIL gemessen)
| Rolle | Original | Film |
|---|---|---|
| Druckschwarz | #040404 (Median) | #050505 + Holzmaserung (helle Adern @ 2–5 %, „lighten“) |
| Schnitt-Weiß | #F0ECE4 (Median, leicht warm) | #F0ECE4 |
| Weißanteil | 13,8 % (Zimmer) | 11,9 % (Treppenhaus), 18,2 % (Flur), 20,3 % (offene Tür) |
| Akzent | keiner | nur Signalrot #D9432F für Problem-Dinge (Akku, 300 €, Bohrer-Kreuz, „24“, Auflegen) |

## Grund und Material
Tiefschwarz wie eingefärbter Druckstock. Im Film zusätzlich die **Holzmaserung** des Stocks: 260 lange, gewellte, kaum
sichtbare Adern + 7 Astringe, nur im Schwarz wirksam. Weiße Flächen = stehengebliebenes Holz: **Stanz-Kante** (unruhiger Rand
±2 px, ab und zu eine 5-px-Kerbe), schwarze Poren (1 Pore je 2600 px²) und schwarze Maserungsstriche quer durch die Fläche
(wie die Streifen im Fenster des Originals).

## Linien
Weiße Stichelschnitte 4–7 px (Original 3–4 px bei 1010 Breite), Breite schwankt ±16 %, **spitze Enden** (Verjüngung auf den
ersten/letzten 18 %), leicht ausfransende Ränder. Alle Schnitte **boilen 12×/s** (Rauschen neu je 1/12 s), die Kamera fährt immer.

## Detailgrad und Motive
- Zentralperspektive: Zimmer/Treppenhaus mit Dielen, Rückwand, Tür mit vier Füllungen, Fenster mit Mond (Kreis mit drei Punkten).
- **Tapetenmuster** Punkt + Kelch in versetzten Reihen auf allen Wänden, perspektivisch skaliert.
- **Mondlicht als massive weiße Fläche** mit Fensterkreuz auf dem Boden.
- Figur: schwarze Silhouette mit weißer Schnittkante, runder Kopf, dicke Glieder (Techniker mit Kappe und Koffer).
- **7-Segment-Uhr** im doppelten weißen Rahmen (23:52, läuft beim Warten auf 00:14; am Ende wird sie zur Telefonnummer).
- Endloser Flur mit Ringen, Fenstern, Uhren, Lichtpunkt mit Strahlen am Fluchtpunkt, Dinge fliegen vorbei, Bild rollt.
- **Sternburst**: gezackter weißer Stern → Weiß → Szene öffnet sich aus einem gezackten Loch.

## Typografie
Weißes Etikett oben links, schwarze runde Handschrift-Groteske (Comic Sans MS Bold wie im Original), wird **getippt** und steht
zur Wortzeit. Etiketten tragen 2–4 Wörter Botschaft, keine Satz-Untertitel. Preise auf weißen Anhängern in derselben Schrift.
Einzige Ausnahme: Markenname „RIEGEL 24“ in einer Holzletter-Serife (Superclarendon Black) mit Poren und Kerben, weil das
Original keinen Logo-Moment hat. Nichts kursiv.

## Die 5 Merkmale, an denen man den Stil erkennt
1. Reines Schwarz-Weiß wie ein Druck: tiefschwarzer Grund, warmweiße Schnitte.
2. Gestochene Linien mit schwankender Breite und spitzen Enden, die 12×/s zittern.
3. Tapete aus Punkt + Kelch und Sternenstaub überall.
4. Massive helle Lichtflächen mit Stanz-Kanten und Kerben (Mondlicht, offene Tür).
5. Zentralperspektive mit Sog in die Tiefe (Flur, Fall, Rollen) + getipptes weißes Etikett oben links + 7-Segment-Uhr.

## Stilvergleich-Runden
- **Runde 1** (`out/stilvergleich_1.jpg`): Welt stimmt, aber alle Linien halb so dick wie im Original, Tapete zu klein und zu
  dünn gestreut, Figur im Fall war ein liegender Klumpen, der Flur zu leer, das Fenster klebte riesig an der Seitenwand.
  → Perspektivlinien ×1,8 (min 1,6 px), Türlinien 6,5 px, Figur-Kante 10 px; Tapete 1,7× größer und dichter (0,3 statt 0,4);
  Fenster mit Mond in die Rückwand wie im Original; Fallpose mit gespreizten Gliedern; vorbeifliegende Fenster, Uhren, Türen;
  7-Segment-Ziffern als echte Balken (vorher unlesbare Striche).
- **Runde 2** (`out/stilvergleich_2.jpg`): Zimmer, Flur und Rollen wirken wie aus derselben Serie.
  → Sternburst deckend statt halbtransparent grau (Streifen `out/strip_riegel.jpg`), Tapete auf der Rückwand noch dichter,
  Bohrmaschine mit Akku klarer, „Tag & Nacht“ größer.

## Messwerte (dichte.py, out/film.mp4)
sekunden 30,7 · Schnitte/10 s 0,7 · Bewegung 13,0 · **Standbild 0 %** · Farbigkeit 7,0 (fast reines S/W)
Timing-Streifen: `out/strip_{schluessel,preis,p50,riegel,festpreis,klick}.jpg`; Wortzeit-Bogen `out/sheet3.jpg`.

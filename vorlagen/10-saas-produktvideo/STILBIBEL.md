# STILBIBEL V5 – 10 SaaS-Produktvideo (Shotbase-Launchvideo, Miguel Ángel / HyperFrames)

Referenz: `ref/vollbild.mp4` (Videofläche des Posts, 670×376, 45 s; 0–2,5 s mit Player-Leiste, danach sauber).
Angesehen: 18 Einzelbilder (`ref/sheet.jpg`), 82 Bilder im 0,5-s-Raster (`ref/dicht.jpg`), Ausschnitte (`ref/detail.png`, `ref/z_share.png`).

## Palette (PIL-Messung, Median-Cut)
| Rolle | Hex |
|---|---|
| Nacht-Wallpaper (Intro) | Grund `#010a2f`, Bänder `#0c2441` `#192a41` `#2a323b`, Oliv oben links `#44443d`, fast Schwarz `#171816` |
| Blau-Wallpaper | Grund `#022783`, Bänder `#064591` `#135a98` `#396596` `#42789b`, Petrolgrau `#608396` `#7c9697`, Lichtkante `#c5cddc` `#e6e7e6` |
| Helle Wolkenvariante (Blitz) | `#6599d9` `#7aa6dc` `#9cbee0` |
| Galerie-Weiß | `#fafafa` / `#f9f9f9` (60–92 % der Fläche in weißen Szenen) |
| Leiste | Fläche `#f7f7f7`, Kante `#dfdfdf`/`#e1e6e8`, Icons Grau `#8e8e93`, Labels `#a2a2a2` |
| Aktiv-Knopf | Cyan `#1fb9ee` |
| Text | `#0a0a0a`, Navy-Tauschwort `#0d3989`, Akzentblau `#2365dc`, frisches Wort `#97ceea` (auf Wallpaper) |
| Tasten | `#1c1c1e`, Druck-Glühen `#6a7dff` |
| Zeitleiste | Gelb `#f0c46b`, Magenta `#ba35ff`, Blau `#81a5fb`/`#2f66e8`, Rahmen `#35e3cc → #d94fc4` |
| Annotation | Rot `#ff1a1a`, Label schwarz fett auf Weiß |

## Hintergrund
Zwei Welten, hart gewechselt: (1) riesig geblurrtes macOS-Wallpaper aus diagonalen Farbbändern, die langsam fließen
(nachts fast schwarz-navy mit olivgrauer Ecke, tagsüber Navy/Petrol mit heller Lichtkante), (2) reines Galerie-Weiß ohne
jede Textur. Kein Korn, keine Muster, keine Vignette. Weichheit nur aus Blur.

## Linien / Formen
Keine Konturlinien. UI-Objekte: weiche Rundungen (Leiste Radius = halbe Höhe, Karten 18–24 px), 1-px-Kante `#e1e6e8`,
sehr großer weicher Schatten (Blur 60–90 px, 20–30 % Deckkraft). Icons: dünne graue Strichicons (≈ 3 px bei 1080p), kleine
graue Labels darunter. Echte Inhalte (Fotos, Screenshots, dichte UI) liegen in Karten – das Detail kommt aus echtem
Material, nicht aus Illustration.

## Detailgrad
Fotorealistische Inhalte in der UI (Wald-Wallpaper, Webcam-Person, Website-Screenshot mit vielen Kacheln). Mauszeiger ist
der große macOS-Pfeil (≈ 80 px hoch bei 1080p), schwarz, weiße Kontur, Schatten, kippt in Bewegungsrichtung.

## Typografie
SF Pro, Medium/Semibold (500–600), Satzschreibung, Laufweite ≈ −0,03 em. Klein im Bild: 44–64 px bei 1080p; nur der
Schluss-Satz groß (≈ 110 px). Wort für Wort: jedes Wort kommt aus Unschärfe, kurz hellblau, setzt sich zu Weiß/Schwarz.
Satzanfang wird ausgetauscht („When“ → „Share“ in Navy), letztes Wort blau. Keine Versalien, keine Balken hinter Text.

## Bildaufbau, Kamera, Bewegung
Zentriert, viel Luft. Kamera driftet immer (Punch-in 1,0 → 1,08, Rausfahren enthüllt Karte in Galerie). Grundgeste:
Blur-in (Blur 12–40 px + Scale 0,9 → 1), Easing expo-out. Objekt wechselt Zustand statt Schnitt (Pille → Leiste → Feld).
Übergänge: Wallpaper hell/dunkel blenden, Lichtblitz + Rausfahren, Blur-out nach unten, Pixel-Mosaik-Blende, harter
Schnitt Weiß ↔ Wallpaper mit Scale-Bewegung.

## Die 5 Merkmale, an denen man den Stil erkennt
1. **Riesig geblurrtes, fließendes macOS-Wallpaper** (nachts dunkel, tags Navy/Petrol) im Wechsel mit **reinem Galerie-Weiß**.
2. **Weiße schwebende Werkzeugleiste** mit grauen Strichicons, kleinen Labels und genau einem cyanfarbenen Aktiv-Knopf.
3. **Großer macOS-Mauszeiger**, der tanzt, kippt und klickt – jede Zustandsänderung wird durch einen Klick ausgelöst.
4. **Kleine SF-Headlines Wort für Wort** aus Unschärfe, frisches Wort hellblau; Schluss groß mit Navy-Tauschwort + blauem Endwort.
5. **Echtes Material in Karten** (Fotos, dichte UI, Zeitleistenbalken, rote Freihand-Annotation, Pixel-Mosaik).

## Umsetzung für Domus (Bildwelt aus der Geschichte)
- Sonntagabend: Nacht-Wallpaper, dunkle Tasten-Widgets (So 14 · 21:47 · Nachrichten-Taste glüht), Mitteilung mit Foto.
- Handwerker: weiße Anruf-Leiste mit drei Kontakten, Zeiger klickt, „Keine Antwort“.
- 20 Nachrichten/Belege: Stapel auf Galerie-Weiß (Ordner-Motiv), Belege fliegen dazu.
- Wochenende: macOS-Kalender, rote Freihand-Durchstreichung + Label „Weg.“ (Annotations-Motiv „blur this“).
- Wendung: Pixel-Mosaik → Blau-Wallpaper, Pille wächst zur Domus-Leiste, Foto-Meldung, Lichtblitz + Rausfahren zur Karte
  mit „✦ Zusammenfassung“, Handwerker-Karte, Zeitleistenbalken gemeldet/beauftragt/erledigt, Esstisch-Foto als Desktop,
  Schluss „Der erste Monat ist kostenlos“ neben kleiner Karte.

## Runden
**Runde 1** (`out/stilvergleich_1.jpg`): Leiste, Zeiger, Typo und Galerie-Weiß passen. Abweichungen: Blau-Wallpaper zu
gleichförmig königsblau, ohne die helle Lichtkante und die Petrol-/Oliv-Schwünge; Tasten-Widgets zu klein; Headline im
Stapel-Bild zu weit vom Objekt; Zeitleiste leer; Küchenfoto zeigt den Wasserschaden nicht.
→ Wallpaper neu: Navy-Schwung, Petrol-Band, helle Lichtkante `#b4c8d0`, Oliv-Ecke, weniger Blur (42 px statt 54 px).
Tasten 290 px, Stapel-Headline direkt unter dem Stapel, leere Spuren in der Zeitleiste, Foto neu (offener Spülenschrank,
Wasserstrahl, Pfütze mit Spiegelung), Tipp-Punkte in der Mitteilung.
**Runde 2** (`out/stilvergleich_2.jpg`): Wallpaper jetzt wie Original (Lichtkante, Schwung). dichte.py ergab 34 %
Standbild → permanente Kamerafahrt je Szene (Push 1,3 %/s + Schwenk) und schneller fließendes Wallpaper → 0–1 %.
Zoom-Rausfahrt und Schluss-Schrumpfen enden jetzt vor dem ersten Wort der Zeile.
**Runde 3** (`out/stilvergleich_3.jpg`): Randbeschnitt durch die Kamerafahrt behoben (Intro, Zeitleisten-Headline,
Schlusskarte). Serie wirkt wie derselbe Designer: gleiche Leiste, gleicher Zeiger, gleiche Typo, gleiche Weiß/Blau-Welt.

## Messwerte
dichte.py V5: Standbild 1 %, Bewegung 5,8 %, Farbigkeit 34,3, 2,0 Schnitte/10 s
(Original-Ausschnitt: Standbild 34 %, Bewegung 10,3 %, Farbigkeit 39,1, 2,0 Schnitte/10 s).

## Ehrliche Abweichungen
- Fotos (Küche, Esstisch) sind prozedural gemalt, nicht echte Fotografie wie Wald/Webcam im Original – im kleinen
  Kartenformat lesen sie als Foto, groß (Esstisch-Karte) wirken sie weicher/illustrativer.
- Das Original hat eine dichte echte Website (Toolfolio) als Material; unser dichtestes Material ist der Kalender.
- Die Headlines sind etwas länger (bis 6 Wörter) als im Original (2–4), weil der deutsche Sprechtext es verlangt.
- Keine 3D-Kippbewegung mit Bewegungsunschärfe (Original-Übergang 3); stattdessen Pixel-Mosaik und Blur-Übergänge.

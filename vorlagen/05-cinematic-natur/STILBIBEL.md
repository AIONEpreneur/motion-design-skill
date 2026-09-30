# STILBIBEL 05 – Leon Lin „Heliotrope“ (Coded Nature Film) → Sonnenhof Solar V5

Quelle: `ref/original.mp4` (1920×804 Cinemascope, 30 fps, 163 s, Vollbild). Gesichtet: 16 Einzelbilder `ref/f_*.png`,
Übersicht `ref/uebersicht.jpg`, 1 Bild alle 1,7 s `ref/alle.jpg`, Detailansichten `ref/vier.jpg`.
Unser Film ist 16:9 (1920×1080) ohne Balken, der Bildaufbau bleibt breit (Horizont im mittleren Drittel).

## Die 5 Erkennungsmerkmale
1. **Tautropfen am Grashalm, in dem eine ganze Welt liegt** (Himmel, Wolken, Horizontband), davor/dahinter Bokeh-Scheiben,
   Spinnfäden mit Tauperlen, unscharfe Halme – Makro-Tiefenschärfe in Blaustunde.
2. **Wolkenmeer im Gegenlicht**: weiche Wolkendünen, dunkle Täler, helle Kämme, Sonne knapp über dem Horizont,
   darüber waagerechte Zirrenstreifen auf blaugrünem Himmel, Vogelschwarm.
3. **Sonnenblumen als Hauptfigur**: detaillierte Blüte (Blütenblätter mit Adern, Fibonacci-Samenscheibe), unscharfe Köpfe im
   Vordergrund, Feld bis zum Horizont; Sonne verwandelt sich in Blüte (Formverwandlung statt Schnitt).
4. **Licht als Zeit**: Sonnenstand erzählt Tageszeit (Morgen → Mittag → Abend → Nacht), Glanzsterne (4-strahlig),
   Glühwürmchen als große grüne Bokeh-Punkte in der Nacht.
5. **Gesperrte Serifen-Versalien** (Garamond-Charakter), weiß, sehr weite Laufweite, klein, weich eingeblendet;
   dazu Korn, weiches Glühen, Vignette.

## Palette (PIL Median-Cut, Anteil)
| Einstellung | Hex |
|---|---|
| Tropfen/Blaustunde f_8 | #030e3d (24 %), #0d1126, #25234e, #573a5b (Band), Tropfen hell #937e9a |
| Wolkenmeer rot f_22 | #271d22, #562527, #956e54, #8d4e3b, #d2a779 |
| Wolkenmeer gold f_30 | #4f3531 (Täler 24 %), #a18a73, #ccb397, #ecdac2 (Kämme), Himmel #575a57 / #5a7080 |
| Sonnenblume f_50 | #223645, #3e647b (Himmel), #9dafb6 (Dunst), #d4b755 (Blüten), #74775d |
| See Abend f_100 | #501e24, #a14d44, #ca725a, #e7a37e |
| Berge Dämmerung f_110 | #4b2e5b, #673c69, #986487, #b78399 |
| Nacht f_146 | #030415, #01020e, #171b30, #333b49; Glühwürmchen ≈ #b4e678 |
Firmenfarbe (Sonnenhof-Gelb/Orange) kommt über Sonne, Blüten und Fensterlicht – keine Zusatzfarbe nötig.

## Hintergrund, Licht, Textur
Keine Flächen, nur Licht: Verläufe, Dunst zum Horizont, Gegenlicht. Korn fein (bei uns Overlay 10 %), Vignette ≈ −45 % in den
Ecken, weiches Glühen heller Stellen. Tiefenschärfe: Vordergrund 12–16 px weich.

## Linien, Detailgrad
Keine Konturen. Detail steckt in Materialien: Blütenblätter mit Mittelader und Seitenadern, 1100 Samen im Goldenen Winkel,
Blätter mit Adern, Tropfen mit Fresnel-Rand, Glanzlicht, hellerem unteren Rand.

## Typografie
Cormorant Garamond, Versalien, Laufweite 0,22–0,34 em, weiß #fbf6ee mit weichem Schatten; Zeilen 34–46 px links oben
(x = 150, wie der Titel im Original), Marke 96 px mittig. Einblendung: Deckkraft + 6 px Unschärfe → scharf, **fertig
0,04 s vor dem gesprochenen Wort**. Keine kursive Unterzeile (Auftrag).

## Kamera, Bewegung, Übergänge
Dauernde langsame Fahrt (Dolly seitlich, Push-in), Wolken strömen, Blumen wiegen sich, Bokeh driftet.
Übergänge wie im Original: **Fahrt in den Tropfen** (dessen Inhalt wird das nächste Bild), **Sonne → Blüte**,
**Zoom in die Samenscheibe** – Samen ordnen sich zu Solarzellen (Formverwandlung), Zeitraffer über den Sonnenstand.

## Umsetzung
- WebGL-Shader: Himmel (Verlauf, Sonne mit 3 Glühstufen, Zirren als gestreckte fbm-Schicht, Haufenwolken, Sterne),
  Wolkenmeer als Höhenfeld-Raymarch (90 Schritte + Verfeinerung, Normalen, Streulicht, Randlicht im Gegenlicht, Dunst),
  Tautropfen mit Linsenverzerrung, Fresnel und Glanz – die Welt im Tropfen ist derselbe Shader, deshalb ist die Fahrt
  in den Tropfen nahtlos.
- Canvas: Sonnenblumenkopf vorgerendert (3 Blattkränze, 1100 Samen), Feld in Zentralperspektive (≈1000 Pflanzen, Tiefe
  sortiert), Nahebene 14 px weichgezeichnet; Haus in Dreiviertelansicht mit Ziegellinien, Traufschatten, Fenstern, Speicher;
  Module auf der Dachfläche bilinear verzerrt mit wanderndem Himmelsreflex; Glanzsterne, Bokeh, Glühwürmchen, Korn.
- Geschichte: Tropfen schwillt Jahr für Jahr mit der Rechnung (1.620 → 2.140 €) → Fahrt in den Tropfen → Sonne über dem
  Wolkenmeer → Sonne wird Sonnenblume, daneben Ihr Haus mit leerem Dach → Samen werden Solarzellen (Kraftwerk) →
  Planung (Maßlinien), Montage (24 Module rasten ein, synchron zu den Klicks), Anmeldung (Lichtpuls zur Leitung),
  Transporter → Mittag: Licht fließt vom Dach ins Haus → Sonnenuntergang, Speicher lädt → Nacht, Fenster, Glühwürmchen →
  Tropfen im Morgenlicht, Rechnung sinkt auf 642 € (−70 %) → Fahrt in den Tropfen → Wolkenmeer, Marke, Angebot, Kontakt.

## Stilvergleich
### Runde 1 (`out/stilvergleich_1.jpg`)
Befund: Tropfen innen dunkel-braun statt hell-lila; Wolkenmeer flach, überbelichtet, ohne dunkle Täler; Himmel ohne
Zirren; Taghimmel blass und dunstig; Nacht zu lila, Glühwürmchen zu klein; alles etwas zu milchig (Glühen zu stark).
Geändert: Welt im Tropfen mit eigener Lila-Palette und Blick nach oben (pitch .3), Hintergrundband schwächer; Wolkenmeer:
Kamera tiefer, Höhe ×1,3, neue Beleuchtung (Streiflicht + Randlicht, Täler #4f3030), Dunst schwächer; Sonnenglanz ohne
breiten Schleier; Glühen 0,42 → 0,2; Tag- und Nachtpalette satter/dunkler; Glühwürmchen 60 Stück, bis 42 px.
### Runde 2 (`out/stilvergleich_2.jpg`)
Befund: Zirren liefen als Strahlen zur Sonne (falsche Streckrichtung), Himmel über dem Wolkenmeer braun statt blaugrün.
Geändert: Zirren quer gestreckt (waagerechte Bänder), Horizontverlauf enger (Zenitfarbe früher), Zirren hell cremeweiß.
### Runde 3/4 (`out/stilvergleich_3.jpg`, `out/stilvergleich_4.jpg`)
Wolkenmeer, Tropfen und Feld lesen sich als dieselbe Welt. Danach: Samen→Zellen-Hintergrund dunkel gehalten, Marken-Sonne
nach rechts (Titel frei), dauernde Kamerafahrt in allen Szenen (Standbildanteil 47 % → 7 %).

## Messwerte (dichte.py)
Film: Bewegung 16,0 %, Standbild 7 %, Farbigkeit 41,8, 2,7 Schnitte/10 s.
Original: Bewegung 7,1 %, Standbild 18 %, Farbigkeit 38,8, 0,2 Schnitte/10 s.

## Ehrliche Abweichungen
- Das Haus ist sauberer und „CG-flacher“ als die weich gerenderten 3D-Objekte des Originals (kein echtes Licht/Schatten).
- Haufenwolken am Taghimmel sind dünner/fedriger als die dicken, plastischen Wolken des Originals.
- Wolkenmeer: Dünen etwas regelmäßiger, keine fernen Wolkentürme am Horizont.
- Deutlich mehr Schnitte als im Original (163 s mit 13 Einstellungen vs. 26 s mit 9 Stationen der Geschichte).

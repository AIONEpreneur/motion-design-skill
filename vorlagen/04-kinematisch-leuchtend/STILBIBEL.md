# STILBIBEL 04 – „A Cosmic Journey“ (rege / CoAnimator) → Halt Versicherungsmakler V5

Quelle: `ref/original.mp4` (1920×1080, 60 fps, 95 s, Vollbild). Gesichtet: 16 Einzelbilder `ref/f_*.png`, 12 weitere `ref/g_*.png`,
1-Bild-pro-Sekunde-Übersicht `ref/alle.jpg`, 1:1-Ausschnitte `ref/crop_*.png`.

## Die 5 Erkennungsmerkmale
1. **Alles ist mit Ölpinsel gemalt**: jede Fläche besteht aus kurzen blattförmigen Strichen (≈ 30–45 px lang, 8–12 px breit,
   spitz auslaufend, leicht gebogen), die in Büscheln die Richtung wechseln. Kanten sind dadurch ausgefranst.
2. **Leuchtende goldene Menschen**: cremegelber Rumpf, nach unten orange bis rostrot, zwei weiße glühende Augenpunkte,
   braun-orange Pinselflocken an den Rändern, weicher Glühschein – sonst keinerlei Details.
3. **Eine satte, flächige Farbe pro Einstellung** (Rot, Gras-Grün, Violettgrau, Ocker, Nachtblau), darauf wenige, sehr einfache
   Kulissen (Tisch mit Beinen, Treppe aus Balken, Laterne mit Dreieck-Lichtkegel, Hausrechteck).
4. **Dünne Versalien mit Glühen**, oben mittig (oder unten mittig), bauen sich Buchstabe für Buchstabe mit Zufallsglyphen auf
   und zerfallen am Ende.
5. **Licht als Erzählmittel**: Lichtkegel, Fadenkreuz + sich schließender Kreis um einen Punkt, Lichtspur mit glühendem Kopf,
   leuchtende Trennlinie (JOY | SUFFERING).

## Palette (PIL Median-Cut auf `ref/f_*.png`, Anteil in Klammern)
| Einstellung im Original | Hex |
|---|---|
| All / Nacht | #0d0e1f (23 %), #111322, #080b1a, #1c1d29 |
| Lichtbänder | #4d2b24, #5e382c (Orange-Braun), #18162a, #291f32 (Violett), Blau ≈ #2a3a8a |
| Violettgrau (Treppe) | #4c495a (23 %), #454253, #2d2d3f, Stufen #8e8a94 / #aba5a1 |
| Ocker (Religions) | #996a2f, #c6a451, #e6d99e, dunkel #140e19 |
| Rot (King and Peasant) | #7d161a, #6e121d, #530f1c; Tisch/Menge #bcb498 / #776857 |
| Rot dunkel (Sinner) | #701d22, #31131d, #16111a |
| Wiese (Hopeful Child) | #83a637, #90b23e, #6a912c, Licht #bcc963 |
| Salbei (Vote) | #364236, #5a6c54, #455745 |
| Figuren | Mittelwert der hellen Pixel #e9e291; Verlauf #fff7cf → #ffeaa0 → #fbd06a → #f5a33c → #de6a22 |
| Akzent | Schirmrot #c8202a, Laternenlicht #f5eed6, Kegel #cdc6b1 |

Firmenfarben: keine eigene Palette – Halt bekommt Gold (Schirm, Suchlicht, Ring) als Akzent.

## Hintergrund, Textur, Licht
- Pinseltextur: Helligkeits-Streuung auf flacher Wiese gemessen σ = 23 bei Mittel 132 (≈ 17 %). Unser Film: Wiese σ ≈ 20–24.
- Große weiche Lichtinseln (Laternenhalo, Sonnenfleck), starke Vignette (Ecken ≈ −40 %), feines Korn.
- Regen: scharfe, helle, kurze Striche (18–44 px), leicht schräg, nicht gemalt.

## Linien und Figuren
- Keine Konturlinien. Nur feine Lichtlinien (Fadenkreuz 2–3 px, weiß mit Glühen; Kreis 4 px).
- Figuren: gestreckt, dicker Rumpf (Schulter ≈ 1,3× Hüfte), runder Kopf, Gliedmaßen dick mit runden Enden, keine Hände/Füße.
  Größe im Bild: 35–60 % der Bildhöhe.
- Pinselflocken: kleine Dreiecke 4–11 px, #8a3a14 / #c0561c, an Rändern, dichter an den Beinen.

## Typografie
Dünne geometrische Grotesk, nur Versalien, Laufweite ≈ 0,1 em, Versalhöhe ≈ 30 px (Schriftgröße ≈ 44–46 px), warmweiß
#f7f2e6 mit weißlich-goldenem Glühen, y ≈ 104 (oben) oder ≈ 986 (unten). Ersatz: Josefin Sans, Gewicht 350.
Aufbau Buchstabe für Buchstabe, jeder Buchstabe zeigt 2 Bilder lang eine Zufallsglyphe; Abgang ebenso.

## Kamera, Bewegung, Übergänge
Langsamer Push-in (3–8 %), ruhige Figurenbewegung, Regen/Staub/Monde halten das Bild immer in Bewegung.
Übergänge: Lichtblüte, Zoom durch ein Objekt, gemalte Überblendung. Punkt → Scheibe → neues Motiv.

## Umsetzung im Film
- **Pinsel**: WebGL-Shader malt die Canvas-Szene mit Blatt-Strichen: Zellraster 23 px, 2 Striche/Zelle, Länge 32–55 px,
  Breite 10–15 px, Richtung aus fbm-Flussfeld ± 0,55 rad Zufall, Farbe aus der Strichmitte (dadurch ausgefranste Kanten),
  Borstenrauschen längs, dunkler Strichrand. Wo die grobe Schicht zu stark abweicht (Kanten, feine Teile), zweite Schicht
  mit 9-px-Strichen. Glühen in Viertelauflösung (3 px + 11 px Weichzeichner = 12/44 px) ungemalt darüber.
- **Figuren**: `person()` mit Gelenkwinkeln, Verlauf wie gemessen, 150 Flocken je Figur, weiße Augen + Glühen, `on` dimmt
  die Figur (verletzt/ohne Einkommen) zu Braun.
- **Bildwelt aus der Geschichte**: Sturz in der Regennacht unter der Laterne (Motiv des Originals), drei Monde = Monate,
  Haus mit Gehaltsspur (Voyager-Lichtspur) und roter Ratenspur zur Säulenbank (wie der lange Tisch), Ocker-Kinderzimmer,
  Fadenkreuz + Kreis um den Punkt → goldener Schirm (BU), rotes Feld mit 100 Schirmen (wie die Menge), goldenes Suchlicht
  (wie der Sinner-Spot), Violettgrau-Treppe aus Kleingedrucktem (wie „Lived out their lives“), roter Schirm in der
  Regennacht, Split mit Lichtlinie (JOY | SUFFERING), Wiese mit Familie, Ring um das Zuhause mit Umlaufbahnen.
- **Schrift**: pro Zeile ein Satz, Wort für Wort *vor* dem gesprochenen Wort fertig (Buchstaben enden 0,1 s vor Wortbeginn).

## Stilvergleich
### Runde 1 (`out/stilvergleich_1.jpg`)
Befund: gleiche Familie, aber Pinselstriche als lange Fasern (LIC) statt Blätter → Shader auf einzelne Blatt-Striche umgebaut
(davor). Danach: Figuren zu klein und neonartig (Glühen zu stark), Treppe zu wenige und zu dicke Stufen, Glühen der
Stufen überstrahlt, Füße standen unter der Bodenlinie.
Geändert: Figuren 20–45 % größer und breiter (Rumpf 38→48 px, Beine 25/18 px), Figurenglühen 0,85→0,42, Augen größer;
Striche 21→23 px Zelle; feine Schicht erst ab Abweichung 0,34 (ausgefranstere Kanten); Treppe 9 Stufen à 44 px;
Stufenglühen halbiert; `gy` = Fußlinie; Kinderzimmer enger gefasst; Überblendung als weicher gemalter Wisch statt Flecken.
### Runde 2 (`out/stilvergleich_2.jpg`)
Befund: Textur, Figuren, Palette und Schrift lesen sich wie dieselbe Serie. Rest: Augen im Original größer/heller →
Augen 3,6→4,6 px, Glühen 9 px; Borstenkontrast etwas gesenkt (Original weicher); Häkchen-Glühen kleiner.
Timing danach: Buchstaben 0,1 s vor Wortbeginn fertig, Abgang nur noch in den letzten 0,16 s einer Zeile.

## Messwerte (dichte.py)
Film: Bewegung 10,4 %, Standbild 15 %, Farbigkeit 36,4, 3,5 Schnitte/10 s.
Original: Bewegung 10,7 %, Standbild 13 %, Farbigkeit 34,9, 2,3 Schnitte/10 s.

## Ehrliche Abweichungen
- Pinselstriche im Original etwas weicher und größer verrieben, bei uns minimal „fell-artiger“ und gleichmäßiger.
- Figurenflocken sind gezeichnete Dreiecke, im Original entstehen sie aus dem Malprozess – aus der Nähe regelmäßiger.
- Kinderzimmer (Bett, Vater mit Gips) ist die schwächste Einstellung: das Bett liest sich eher als Bank.
- 3,5 statt 2,3 Schnitte/10 s: die Geschichte hat in 28 s zehn Stationen, das Original lässt Einstellungen länger stehen.

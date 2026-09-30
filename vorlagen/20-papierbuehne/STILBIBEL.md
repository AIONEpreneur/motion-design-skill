# STILBIBEL V5 – Papierbühne (Andy Lo, „Hawking Radiation, a paper stage“)

Referenz: `ref/vollbild_270-344.mp4` (792×446, reine Bühne ohne Chat-UI). 20 Einzelbilder gezogen (`ref_frames/`),
Ausschnitte 3× vergrößert (Kopf, Vorhang, Titel, Teilchen, Rakete). Maße unten sind auf 1920×1080 umgerechnet (Faktor 2,42).

## Die 5 Erkennungsmerkmale
1. **Feste Puppenbühne**: Kraftpappe-Rahmen mit dünner weißer Innenlinie, korallene Zackenborte mit Senfpunkten,
   gedeckt-korallene Vorhänge mit dunkleren Faltenlinien, Holzdielenboden in leichter Perspektive. Nur das Bühnenbild dahinter wechselt.
2. **Weiße Kreide-Schnittkante um jede Form** (≈4 px, leicht unregelmäßig, runde Ecken) – alles wirkt aus Papier geschnitten.
3. **Zellophan-Schlieren**: breite, halbtransparente helle Bänder schräg „\“ (≈40° nach rechts unten) über jeder Fläche,
   dazu feines Papierkorn. Keine harten Glanzpunkte, keine Verläufe auf Figuren.
4. **Gedeckte Kinderbuch-Palette**: Senf-Streifentapete, Koralle, Petrol, Orange, Creme gegen Nachtblau mit violetten Wolken.
   Nichts ist grell gesättigt.
5. **Einfache, liebe Papierfiguren**: großer Kopf, Punktaugen, rosa Wangenkreise, winziger ovaler Mund, Bob-Haar mit
   weißer Glanzlinie, Trapez-Oberkörper, weißer Kragen, Arme als Streifen, Hände als Kreis. Dazu **blaue Buntstift-Titel**
   (runde Handschrift, gemischte Schreibweise, weiße Kontur) oben links.

## Palette (PIL-Messung auf den Referenzbildern)
| Rolle | Hex |
|---|---|
| Rahmen Kraftpappe | #c49f6f |
| Borte (Zacken) / Senfpunkt | #cb6b5f / #d9a24f |
| Vorhang / Faltenlinie | #e5877a / #cf6a60 |
| Tapete Streifen hell / dunkel | #ebc461 / #e8bb51 |
| Dielen / Fuge / Sockel | #a7703e / #8e5c30 / #c49f70 |
| Pult Platte / Korpus | #c49f70 / #ae8a5f |
| Haut | #f2caa1 |
| Wange | #e7a598 |
| Haar | #19141e |
| Petrol (Pulli, Pflanze) | #349c8d |
| Koralle (Topf) | #e38676 |
| Orange (Sonne, Bogen) | #e6823a |
| Senf-Gelb (Bogen innen) | #f3c057 |
| Creme (Papier) | #f9ecd8 |
| Nachtblau / Wolke | #1b2352 / #33306a |
| Loch fast schwarz | #1b1822 |
| Dämmerung oben → Horizont | #3d3651 → #5e4652 |
| Titel-Blau | #3c67cd |

## Hintergrund, Papier, Licht
- Tapete: senkrechte Streifen, 92 px breit, Kontrast nur ≈4 % (hell/dunkel oben). Keine Muster.
- Nacht: flaches Nachtblau, 3–4 verschwommene violette Wolkenbänder mit eigenen Schlieren, 150+ Sterne (1–3 px, creme/senf), blinkend.
- Dämmerung: senkrechter Verlauf dunkles Pflaume → Rosé, darüber Sterne.
- Leichte Vignette am Bühnenrand, sonst gleichmäßiges Licht. Weiche, kurze Schatten unter Objekten (Blur 10, Versatz 4, 20 %).
- Korn: feines Rauschen (±6 Grauwerte) auf allem.

## Linien
- Weiße Kante 4 px (#fbf4e6, 95 %), runde Ecken, Kanten mit statischem Zittern ±1,5 px (geschnittenes Papier) und Boil ±0,8 px bei 8 fps.
- Innenlinien (Falten, Fugen, Schublade) 3–4 px, dunkler Ton derselben Fläche. Keine schwarzen Konturen.
- Buntstiftzeichnungen (angepinntes Bild): 6–8 px, raue Ränder, orange/petrol/koralle auf Creme.

## Figuren (Detailgrad)
- Kopf ≈ 170 px breit; Gesicht U-Form, gerade Ponylinie; Augen 11 px schwarze Punkte; Wangen 30 px Kreise #e7a598 bei 80 %;
  Mund 8×12 px Oval #6b2a2a (offen beim Sprechen). Keine Nase, keine Ohren, keine Augenbrauen.
- Körper: Trapez mit leicht abfallenden Schultern, weißer Kragen als zwei Dreiecke, Arme als abgerundete Streifen, Hand = Hautkreis.
- Requisiten: gerahmtes Bild mit Holzleiste, Kaktus im Korallentopf, Pult mit Schublade und Senfknopf, Kalender mit Petrol-Pins
  und korallen Kästchen, Sanduhr mit Holzrahmen.

## Typografie
- Titel: runde Handschrift (Mali Bold), gemischte Schreibweise, Titelblau #3c67cd, weiße Kontur ≈ 16 % der Schriftgröße,
  Größe 84–100 px, oben links bei x≈360, y≈190 (unter der Borte). Laufweite normal. Entsteht als Buntstift-Strich von links nach rechts.
- Zweite Ebene: weiße Papierkarte (Radius 22, Schatten) mit dunkler Handschrift #2a2330 (wie „Play the show“).
- Keine Versalien-Schlagworte, keine Balken, keine Deko-Texte.

## Kamera, Bewegung, Übergänge
- Bühne steht, Kamera nur im Bühnenfenster: langsames Heranfahren (≤6 %), Fahrt in die angepinnte Zeichnung.
- Boil 8 fps, Figuren- und Requisitenbewegung in 12-fps-Stufen, weiches Easing.
- Requisiten kommen an Fäden von oben (Sanduhr, Kalender), Tapete rollt sich wie eine Schriftrolle auf/ab.
- Leben im Bild: Sterne blinken, Staub tanzt, Figuren atmen/blinzeln, Mund spricht.

## Umsetzung
Canvas 2D, reine Funktion von t. Formen als Punktlisten → statisches Zittern + Boil → Füllung, Schlieren-Muster (clip),
Korn, weiße Kante. Schlieren/Korn als vorab erzeugte Muster mit geseedetem Zufall.

## Stilvergleich-Protokoll
(wird nach jeder Runde ergänzt)
**Runde 1** (`out/stilvergleich_1.jpg`): Rahmen, Borte, Vorhänge, Tapete, Kreidekante und Schlieren sitzen – beide Seiten
wirken wie eine Serie. Abweichungen: Titel zu fett/groß mit zu dicker Kontur; Sitzfiguren lasen sich als stehend;
Wolken als flache Bänder statt weicher Wölbungen; Kopfteil des Betts wirkte wie ein Brett; Gedimmtes Licht in Szene 1 machte
die Senftapete bräunlich-matschig; herabgefallene Tablets lagen als Unordnung auf dem Boden.
→ Titel 80 px statt 92, Kontur 13 % statt 17 %; Sitzpose mit Schoß-Block und kurzen Unterschenkeln, niedrigere Sitze,
größerer Sessel; Wolken aus drei weichen Ellipsen mit Weichzeichner-Schatten; Kopfteil als abgerundete Holzplatte mit Leisten;
Dimmung 0,42 → 0,15; Tablets/Kalender fallen durch die Bühnenkante aus dem Bild.

**Runde 2** (`out/stilvergleich_2.jpg`): Figuren und Titel jetzt im Maß des Originals. Rest: Mond kollidierte mit dem Titel,
Füße des Lehrers unter dem Pult sichtbar, Vignette etwas zu schwer (Senf zu dunkel), Rahmenbild auf dem Pult unlesbar.
→ Mond nach rechts, Pult bis zum Boden, Vignette 0,30 → 0,22, Mini-Gitarre + Herz im Rahmenbild.

**Runde 3** (`out/stilvergleich_3.jpg`): Endstand.

## Messwerte
- `dichte.py` Film: Standbild-Anteil 5 %, Bewegung 5,1 %, Farbigkeit 72,8 (Original: 35 % / 4,7 % / 76,5).
- Timing-Streifen (`out/strip_*.jpg`) bei eins, Lied, nicht, Ton, erstes, erste: Bild steht jeweils ≤ Wortbeginn.

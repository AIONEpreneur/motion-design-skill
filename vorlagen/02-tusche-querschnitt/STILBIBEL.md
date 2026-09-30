# Stilbibel V5 – Grünwerk Gartenbau, im Stil von „A short story about a watermelon“ (Claude/Kevin Ngo, X)

Quelle: `ref/original.mp4` (1080×1080, 24 fps, 29,3 s, Vollbild). 17 Einzelbilder `ref/r_*.png`, Ausschnitte `ref/z_ant.png`, `z_soil.png`, `z_sun.png`, Kontaktbogen `ref/kontakt.jpg`.
Unser Film ist 16:9 (1920×1080); die quadratischen Bildideen werden in die Breite gebaut.

## Die 5 Merkmale, an denen man den Stil sofort erkennt
1. **Creme-Papier mit breiten Diagonalstreifen, die aus feinen Parallellinien bestehen** (fallend, ca. 40°), dazu leichtes Korn.
2. **Erde im Querschnitt:** braune Fläche mit flacher Diagonalschraffur, Sprenkeln, dunklen Klumpen ohne Kontur, Kieseln mit dunkler Kontur und weißem Glanzpunkt, gewellten Schichtlinien.
3. **Die Ameise:** glänzend dunkelbraun, Hinterleib mit konzentrischer Maserung, weiße Glanzbögen, Borsten, dünne schwarze Beine mit grauem „Zweitstrich“ der fernen Beine.
4. **Textur statt Verlauf:** Sonne mit orangeroten Kritzelstrichen und abwechselnd blauen langen / ockerfarbenen kurzen Strahlen, Blätter mit Adern und Schraffur, Rasen als Einzelhalme.
5. **Blaue Konstruktionslinien und Wetterwelten:** zarte blaue Bögen, gestrichelte Linien, Kreuze, Strichliste; Gewitter als eigene nachtblaue Welt mit dunkler Diagonalschraffur, hellen Konturen und Regenstrichen; Hitze als orange Schraffur über dem Bild.

## Palette (mit PIL aus den Referenzbildern gemessen)
| Rolle | Hex | Quelle |
|---|---|---|
| Papier | `#f3efe0` | r_0.5, r_11 |
| Streifen (Grundton der Bänder) | `#efdcbb`–`#f1e8d0` | r_6.5 |
| Kontur | `#121412` (Film `#1b1a22`) | r_11, dunkelste 0,7 % |
| Erde / dunkel / hell | `#997558` / `#6f4f3a` / `#ad9076` | r_2 |
| Kiesel | `#c5a275` (Film `#c9a878`) | r_2 |
| Rasen hell / Halm | `#b0d898`–`#c7dfb2` / `#5c8f48` | r_11, r_17 |
| Ameise | `#482c25`–`#5b3527` | r_6.5 |
| Sonne | `#e59f55` (Film `#eba84f`), Kritzel `#e2703a` | r_6.5 |
| Nachtblau Himmel / Boden | `#333571` / `#25274e` | r_14 |
| Konstruktionsblau | `#4f78d0` | Sonnenstrahlen r_6.5 |
Grünwerk-Grün `#2f6a2c` nur als Akzent (Schlagwort, Schild, Etikett an der Gabel).

## Linien
- Kontur 2,6–3,4 px, dunkel und sauber, kaum Zittern (Amplitude 0,5–1 px). In der Regen-Welt dieselben Linien hell (`#e9e7f4`), Flächen um 62 % ins Nachtblau gezogen.
- Schraffur: Erde flach steigend (x+3y=c, 15 px Abstand), Schatten 56° (3x+2y=c, 8–12 px), Streifen aus 5-px-Linien.
- Blau 2–3 px, oft gestrichelt [14,10].

## Figuren und Objekte
- **Ameise** (Held wie im Original, begleitet die Geschichte): Hinterleib-Ellipse 72×54 mit 7 Maserungsbögen, Stielchen, zweihöckrige Brust, Kopf mit Auge + Glanzpunkt, Kiefer, Fühler mit Knick, 3 Beinpaare mit Laufzyklus, ferne Beine grau versetzt. Trägt in der Hitze einen Wassertropfen (Bild aus dem Original), treibt bei Regen auf einem Blatt.
- **Kinder** in derselben Handschrift: runde Köpfe mit Haar-Strichtextur, Knopfaugen mit Glanz, Wangen; ein Kind schießt am Ende den Ball.
- **Requisiten:** Wasserball, Holzschaukel, Haus mit Fenster (Putzlinien, Schraffur), Grabegabel mit Maserung und Grünwerk-Etikett, Regenwurm mit Ringen, Kompost-Stückchen, Wurzeln mit Seitenwurzeln, Lupe mit Wurzelhaaren (wie der Detailkreis im Original), Holzschild, Bodenprobe im Glasröhrchen.

## Typografie
- Kalam Bold (Handschrift, passt zum „claude“-Signet und zur Strichliste), 80 px, Satzanfang wie im Deutschen, links x = 110, Zeilen y = 150 / 248.
- Erscheint wie geschrieben (von links freigelegt), fertig spätestens am Wortanfang; Schlüsselwort mit blauem, handgezogenem Unterstrich; einzelne Wörter in Themenfarbe (braun, grün).
- Keine Ecktexte, kein Signet in der Ecke.

## Bildaufbau, Kamera, Bewegung
- Nah wie im Original: Ameise, Ball, Schaukel groß (Kamera 1,35–1,46), Horizont unten; für den Querschnitt 1,0 mit Oberfläche bei y = 300 und Schlagzeilen im Himmelstreifen darüber.
- Eine durchgehende Gartenwelt: Regen → harter Schnitt in die Hitze → Fahrt ans Fenster → Fahrt unter die Oberfläche („Der Grund“) → Schicht für Schicht (gestrichelte Linie zuerst, dann füllt sie sich) → Fahrt zurück nach oben → Schnitt aufs Schild.
- Bewegung mit Bedeutung: Pfütze steigt, Tropfen prallen an der verdichteten Schicht ab, Druckpfeile, Gabelstich mit Stoßstrichen, Auflockerung breitet sich vom Stich aus, Kies fällt ein, Wasser läuft durch den Kies ab, Krümel rieseln, Regenwurm kriecht, Wurzeln wachsen Strich für Strich, Ball wird geschossen, Schild wird eingeschlagen.

## Stilvergleich
**Runde 1** (`out/stilvergleich_1.jpg`): Handschrift stimmt (Sonne, Erde, Ameise), aber unsere Bilder waren Totalen, das Original arbeitet nah mit großen Hauptfiguren; Regen-Boden als helle Kiesel wirkte falsch; Schaukel/Haus lagen hinter den Schlagzeilen; Lupe zeigte einen Balken.
**Geändert:** Kameras für Regen, Hitze und Schluss-Garten auf 1,35–1,46 (Ameise 3× größer), Regen-Boden als dunkles Nachtblau mit Spiegelungsstrichen, Schaukel ins Bild zwischen Pfütze und Haus, Sonne nicht mehr hinter Text, Haus/Schaukel blenden beim Abtauchen aus, Lupe mit gebogener Wurzel und Wurzelhaaren, Oberkrume unter der Grasnarbe ergänzt.
**Runde 2** (`out/stilvergleich_2.jpg`): Nah-Einstellungen passen zum Original. Geändert: Maßstab als Papierlineal (war auf Erde unsichtbar), Etikett an der Gabel sichtbar, Ameise läuft im Querschnitt über die Oberfläche, Tropfen prallen an der Verdichtung ab (Standbild-Anteil von 20 % auf 3 %).
**Runde 3** (`out/stilvergleich_3.jpg`): Endstand.

## Messwerte (dichte.py)
| | Original | V5 |
|---|---|---|
| Standbild-Anteil | 3 % | 3 % |
| Bewegung | 14,3 | 6,2 |
| Schnitte je 10 s | 3,8 | 1,4 |
| Farbigkeit | 51,6 | 35,2 |
Timing: `out/strip_*.jpg` um 7 Schlüsselwörter geprüft (Wasser, verdichtet, lockert, Kies, Mutterboden, grün, Bodenprobe).

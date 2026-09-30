# STILBIBEL V5 – 11 Gemalter Cartoon („I'm Upping My P(doom)“, Clawd-Cartoon, p5.js + p5.brush)

Referenz: `ref/vollbild.mp4` = Vollbild-Passage des Musikvideos aus der Bildschirmaufnahme (Quelle 171,6–322 s, Crop
1156×648 ohne Browser/Balken, 150 s). Angesehen: 14 Einzelbilder (`ref/sheet.jpg`), 60er-Raster (`ref/srcsheet.jpg`),
Ausschnitte Figur/Bühne (`ref/z_figur.png`, `ref/z_buehne.png`).
**Wichtigster Fund:** Der Quellcode des Originals liegt im Scratchpad (`repos/PDoomVideo`, MIT, John Heibel). V5 malt mit
genau diesem Werkzeug: `core.js` (Papier, Korn, Vignette, paint/inkLine, Pinsel `ink`/`inkfine`/`marker`/`charcoal`),
`clawd.js`, `cast.js` (Researcher), `props.js` (Bühne, Vorhang, Thermometer). Neu dazu: `figuren.js` (Kind, Backenzahn,
Requisiten) und `film.js` (Szenen) – mit denselben Pinseln gemalt.

## Palette (PIL-Messung, Median-Cut, am Referenzbild)
| Rolle | Hex (gemessen) | im Code |
|---|---|---|
| Vorhang | `#a53a32` `#a2493d` `#92332a`, Schatten `#4f2821` | CURTAIN `#B8323F` / `#7A1C2B` unter Korn + Vignette |
| Nachtwand Labor | `#223655` `#212642` `#34364c` | `#2C3A63` + Indigo-Lasur |
| Holz Tisch/Boden | `#93653e` `#a28158` `#67564e` | WOOD `#B87A4B`, WOOD_DK `#7C4A2C` |
| Papier/Creme | `#e0d3bb` | PAL.paper `#F3EBDC` |
| Finale-Bühne Pfirsich | `#eaba8d` `#ebbb8e` `#aa7e50` `#b0764b` | warmSet `#EFC9A0`, Strahlen `#DE8E68`/`#EDBF78`, Hügel `#C98C5E` |
| Zuschauerraum | `#231216` `#3e1e23` | HEAD `#2A1F33` |
| Dunkle Konzertbühne | `#392238` `#260f23` `#120913` | D-Szene `#1F2550` / `#141A3A` |
| Tusche | nie Schwarz: `#2B2233` | PAL.ink |

## Papier und Textur
Warmes Papier `#F3EBDC` mit 70 Aquarellflecken und 1400 Faserstrichen; darüber multiplizierte Körnung + braune Vignette
(`rgba(120,95,70,.35)` zum Rand). Flächen = deckende Lasur + Aquarell-Füllung mit Pigmentrand (`fill`, `bleed`, `tex`,
`border`), dadurch fleckig-gemalte Wände. Keine Verläufe, kein Glanz.

## Linien
Eine durchgehende, leicht zitternde Tuschekontur je Form (`ink`, Grundstärke 5 × scaleBrushes 5, ≈ 4–7 px bei 1080p),
Details mit `inkfine` (≈ 2–3 px). Linien „boilen“ 12× pro Sekunde (randomSeed je Boil-Bild). Hintergrund-Flächen oft
ohne Kontur. Keine Schraffur außer in der Pinsel-Wischblende (`charcoal`).

## Detailgrad der Figuren
Researcher: großer runder Kopf (R = 2,35 s), runde Brille mit Punktaugen, stachelige Haarkappe, Kittel-Trapez, Stummelbeine,
Rechteck-Arme mit runden Händen. Clawd: 10×6-Block, Schlitzaugen mit Glanzpunkt, vier Stummelbeine. Gefühle über
Augenformen (Punkt, weit, Stern, Herz, X, geschlossen) + gemalte Emotes (!, Schweißtropfen, Herz, Funke). V5: Mia (Kind,
Zöpfe, Ocker-Pulli), Mama und Zahnfee aus `researcher()` (Dutt, ohne Brille bzw. Kittel + Feenflügel + Zauberstab),
der Backenzahn ist Clawd als Zahn (Höcker oben, Wurzeln statt Beine, Loch wächst, Tuch gegen Zahnweh).

## Typografie
Im Original: Schilder in Permanent Marker (P(DOOM), Titel auf dem Vorhang, „BOOM!“/„SLAM!“ als Comic-Schrift mit
Tusche-Schatten), Nebenzeile in Shantell Sans 800 (Gold). V5 genauso: Schlagworte als Holzschilder oder Comic-Laute in
Permanent Marker (Creme/Ocker, Tusche-Schlagschatten, Pop-Einblendung), Schlusszeile in Shantell Sans Gold. Keine
Untertitelkarten.

## Bildaufbau, Kamera, Übergänge
Bühnen-Rahmen nur am Anfang (Vorhang geht auf) und am Ende (Vorhang fällt mit Titel, Figur lugt durch den Spalt) – wie im
Original. Dazwischen Vollbild-Kulissen (Wand-Band + Boden-Band). Kamera driftet/zoomt immer. Übergänge wie im Original:
Iris, Pinsel-Wischblende (5 Farbbahnen), Kamerafahrt in die nächste Situation, Vorhang.

## Die 5 Merkmale, an denen man den Stil sofort erkennt
1. **Gemaltes Aquarell auf Papier mit Korn und Vignette**, gedämpfte Buchillustrations-Farben.
2. **Boilende, leicht zitternde Tuschekontur** um flache Formen.
3. **Die Figurenfamilie**: Researcher mit runder Brille + Clawd-Blockfigur mit Schlitzaugen, Emotionen über Augen + Emotes.
4. **Theaterbühne**: roter Vorhang, Fußrampenlichter, Zuschauerköpfe, Sonnenstrahl-Kulisse, Thermometer-Requisit.
5. **Comic-Lettering in Permanent Marker** auf Schildern und als Laute.

## Runden
**Runde 1** (`out/stilvergleich_1.jpg`): Handschrift identisch (gleiches Werkzeug). Abweichung: jede Szene steckte im roten
Vorhangrahmen mit Zuschauern → zu rot, zu eng; Figuren klein; Zahnfee-Kulisse zu hell-pastellig.
→ Vorhang/Zuschauer nur noch in Anfang und Schluss, Kamera näher (Zoom 1,16–1,24), Figuren größer.
**Runde 2** (`out/stilvergleich_2.jpg`): Szenen wirken wie Original-Kapitel. Sonnenstrahl-Bühne noch zu blass →
warmSet mit gedämpftem Pfirsich/Gold und Hügelband wie die Finale-Bühne; Uhrfläche kräftiger; Timing: „20 MIN“ steht jetzt
bei „zwanzig“, „EIN LEBEN LANG“ bei „ein“; Iris in die Mundszene schließt vor „Kleine Löcher“.
**Runde 3** (`out/stilvergleich_3.jpg`): Schild ZAHNARZT aus dem Vorhang geholt, grüner Mischfarben-Fleck (Lichtkegel
über Blau) entfernt.

## Messwerte
dichte.py V5: Standbild 0 %, Bewegung 17,4 %, Farbigkeit 61,3, 3,0 Schnitte/10 s
(Original: Standbild 3 %, Bewegung 13,4 %, Farbigkeit 46,2, 2,9 Schnitte/10 s).

## Ehrliche Abweichungen
- Etwas bunter als das Original (Farbigkeit 61 statt 46): Mund-Kulisse Rosa/Weinrot und Comic-Laute in Ocker.
- Mehr Schrift im Bild als im Original (dort fast nur Untertitel + P(DOOM)-Schild), weil der Film stumm verständlich sein muss.
- Die Mundszene (Zahnreihe als Kulisse) ist eigene Erfindung; das Original hat keine vergleichbare Innenansicht.

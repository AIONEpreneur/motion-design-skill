# STILBIBEL 16 – LASIK-Explainer (Andy Diep, „Version A“: Papier-Etiketten + Diagramme)

Referenz: Vollbild-Passage neu geschnitten: `ref/vollbild_A.mp4` (KpepgP9xhrg.mp4 ab 60 s, 48 s, crop 1010×568 @ 135,85 –
nur die Filmfläche, ohne Laptoprand; Webcam unten rechts lässt sich nicht vermeiden). Angesehen: 21 Einzelbilder
(3–42 s) plus 3×-Ausschnitte von Etiketten, Auge, Hornhaut-Wortband, Laser-Maschine, Halbton-Rand.

**Wichtigster Fehler von V4:** „Creme-/Pergamentpapier nicht übernommen (kühles Weiß)“ und flache Cartoon-Figuren.
V5 übernimmt Pergament, Nachthimmel und die Etiketten-/Wortmaterial-Logik des Originals.

## Die 5 Merkmale, an denen man den Stil erkennt
1. **Zwei Böden**: gekörnter Nachthimmel `#253c6c` (feine helle Sprenkel, weiche Wolkenflecken) mit einem glühenden
   rot-orangen Strahlenpunkt – und ein Pergamentbogen `#e6ddc3` mit dunklen Wolkenflecken, der sich über den Himmel schiebt.
2. **Papierstreifen mit Schreibmaschinenschrift** (fett, klein geschrieben, mit Punkt am Ende): auf dem Himmel creme
   `#efe7d4` mit Navy-Schrift, verstreut; auf dem Pergament blau `#496fb5` mit Creme-Schrift, **als Stapel oben links**.
   Kanten gezackt, leicht schräg, Schatten; Text tippt sich Zeichen für Zeichen.
3. **Blaue Halbton-Flächen**: Diagramm-Objekte sind flaches Blau mit feinem Punktraster (6-px-Raster) und Korn,
   dünne Creme-/Dunkelblau-Kontur (Auge ↔ bei uns Haus, Erdreich, Kessel, Wärmepumpe, Thermometer).
4. **Material aus seinem eigenen Wort**: das Hornhaut-Band besteht aus „cornea cornea …“ → bei uns die Außenluft aus
   „wärme“ (Bogenband), die Räume aus „kalt“, später „warm“.
5. **Rot-orange Handeingriffe** `#d07a53`: Kringel um ein Wort, Durchstreichen, gestrichelte Schnitt-/Leitungslinie,
   Kreis um das Bauteil; dazu Halbton-Punktrand, sobald die „Maschine“ kommt.

## Palette (PIL, Referenz → V5)
| Rolle | Referenz | V5 |
|---|---|---|
| Nachthimmel | `#253c6c` (5 % `#192958`) | `#253c6c` + Flecken 6–20 % + Korn ±22, 6 % Sprenkel |
| Pergament | `#e6ddc3` (5 % `#dacdb3`) | `#e6ddc3` + Flecken `rgb(165,146,112)` bis 55 % |
| Blau (Flächen, Etiketten) | `#496fb5` / `#3e66a9` | `#446db3` + Punkte `#6189cc` |
| Creme-Etikett | `#efe7d4`-artig | `#efe7d4`, Schrift `#27365f` |
| Rot-Orange | `#d07a53` / Punkt `#e8603a` | `#d9603f` / `#e8784f` |

## Typografie
Courier Prime Bold, Kleinschreibung, Satzpunkte („januar.“, „haus: kalt.“). Etiketten 30–36 px (Stapel), 72–76 px für
Betrag und Marke. Typing 40–60 Zeichen/s, Streifen klatscht 0,1 s vorher auf (Skalierung 1,08 → 1).

## Bildaufbau, Kamera, Bewegung
- Himmel: Punkt Mitte, Etiketten verstreut, Kamera zoomt langsam (1,2 %/s) und driftet 12 px/s.
- Pergament schiebt sich von rechts über den Himmel (0,4 s), am Ende nach links hinaus.
- Kamera-Fahrten über das Diagramm: Haus nah (1,32×) → Garten (1,22×) → Totale (1,0×, Halbton-Rand) → Haus nah (1,3×).
- Etikettenstapel treibt leicht mit; Wärme in der Leitung als laufende Strichelung; Lüfter dreht; Strahlenpunkt pulsiert.

## Geschichte → Bilder (Wärmewerk Haustechnik)
Himmel mit glühendem Punkt (Gasflamme): „ihre gasrechnung:“ / „3.200 €“ (rot umkringelt) / „im jahr.“ → Pergament:
Hausquerschnitt, Stapel „der kessel im keller:“, „25 jahre alt.“, „januar.“, „kessel: ~~läuft.~~ aus.“, Flamme erlischt,
Räume füllen sich mit „kalt“ → Fahrt in den Garten: Luftbogen aus „wärme“, Thermometer „−10 °c“ → Halbton-Rand,
Wärmepumpe senkt sich, „in 3 tagen. tick. tick. tick.“, alter Kessel verschwindet, rote Leitung, Speicher →
Förderantrag-Formular, Stempel „70 % zuschuss“ → Haus nah: Räume füllen sich mit „warm“, „heizkosten: ~~3.200 €~~“,
„neu: 2.130 € (−1/3)“ → Pergament gleitet weg, Nachthimmel mit warmem Punkt, Marke und Kontakt als Creme-Streifen.

## Stilvergleich
**Runde 1** (`out/stilvergleich_1.jpg`): Himmel, Etiketten, Pergament, Halbton, Wortmaterial sitzen. Abweichungen:
Himmel anfangs zu wolkig/zu glatt (vor Runde 1 korrigiert: Flecken 6–20 %, Sprenkel), Wortband zu schmal, Pergament zu
gleichmäßig gelb, Haus ohne Kontur (Original-Auge hat Doppelkontur), „kalt“-Wörter zu groß.
→ Band 630–790 px breit, 14 px Wörter; Pergamentflecken dunkler (bis 55 %); Haus mit dunkelblauer + Creme-Kontur;
Raumwörter 13 px; Etiketten 10 % kleiner.
**Zwischenschritt**: `dichte.py` 47 % Standbild → Himmel mit Dauer-Zoom/-Drift, Pergamentdrift 11 px/s, Stapel treibt → 4 %.
**Runde 2** (`out/stilvergleich_2.jpg`): gleiche Serie. Danach behoben: Pergamentrand wurde beim Heranzoomen sichtbar
(Bogen größer), schwarzes Bild beim Hinausgleiten (Himmel liegt jetzt darunter), alter Kessel schwebte durchs Haus.

## Ehrliche Abweichungen
- Das Original zeigt einen einzigen, sehr großen Bildgegenstand (Auge/Hornhaut); unser Haus ist kleinteiliger.
- Etiketten größer als im Original (Lesbarkeit auf dem Handy).
- Keine Eckmarken (⌐) und keine Webcam – bewusst weggelassen.

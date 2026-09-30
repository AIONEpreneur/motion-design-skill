# STILBIBEL V5 – 07 Kanzlei Weber, nach „Bitcoin, 10 anos“ (Felipe Borges)

Referenz: `ref/vollbild.mp4` (Vollbild-Passage, 1120×630, 13,5 s), Einzelbilder in `ref/bilder/` (15 Stück).
Die Webcam unten links gehört zur Bildschirmaufnahme und wird ignoriert.

## Was V4 falsch gemacht hat
V4 hatte bewusst „Himmel und Boden kräftig indigo/violett bzw. petrol-grün“ getönt, ein Papier-Dokument „Steuerbescheid“
ins Bild gestellt, breite Versalien-Schrift (Archivo Black Wide) und Untertitel. Das Original ist schwarz, gelb, rot, grau – sonst nichts.

## Palette (mit PIL gemessen)
| Rolle | Hex |
|---|---|
| Grund (grünstichiges Schwarz) | `#070a09` (gemessen an 3 Bildern: #070a09, #070a09, #090b0b) |
| Gitterlinien | ca. `#4d524f`–`#5a5a5a`, rot angehaucht in der Nähe der roten Röhre (#5a4749) |
| Röhre steigend | Kern `#fdf643`, Farbe `#e8f510` |
| Röhre fallend | `#f30000` / Flutrot `#da0001` |
| Scheitel/Übergang | Orange `#f7a51c` |
| Tor beleuchtet | `#d2da11` |
| Schrift Weiß | `#eff3f2` |
| Limette (Wert, Akzentwort, Pille) | `#d4f81c` |
| Rot (Wert) | `#ea3036` |
| Glas | Grau `#8a8f90`, Kanten gelb angeleuchtet |
Themenfarbe der Kanzlei: keine eigene – die Rücklage-Röhre ist ein grünstichiges Limette `#8fe81a` (Familie der Originalfarben).

## Hintergrund / Boden
Kein Papier, kein Korn. Schwarze Leere, darunter ein perspektivisches Drahtgitter (Linienbreite ca. 2 px in Kopfnähe),
das nach hinten im Schwarz verschwindet (Nebel). Der Boden färbt sich in Kopfnähe leicht in der Röhrenfarbe.

## Linien / Körper
- Röhre: dicker Zylinder (Radius 0,6 bei Torbreite 5,9 → wie im Original ca. 22 % der Torbreite), Halbkugel-Kopf,
  flach selbstleuchtend mit hellerem Kern, weicher Bloom-Hof (UnrealBloom 0,72). Farbe folgt der Steigung: gelb ↑, orange, rot ↓.
- Tore: quadratische, extrudierte Rahmen (Tiefe 0,7). Unbeleuchtet dunkel-oliv, beim Durchfahren leuchten sie in der Röhrenfarbe auf.
- Glaswand: grauer Scheibenkreis, zerspringt in radiale Scherben mit hellen, gelb angeleuchteten Kanten.
- Keine Handzeichnung, keine Schraffur, keine Deko – das Original ist sauberes 3D.

## Typografie
Archivo ExtraBold (wght 800–880), eng gesetzt, gemischte Groß-/Kleinschreibung.
Block oben links (links 124 px, oben 88 px): Zeile 1 groß weiß (196 px; lange Wörter 150 px), Zeile 2 (136 px) mit weißem Präfix und
Zahl in Limette (gut) bzw. Rot (schlecht). Weicht der Linie aus: bei „Vorauszahlung“ rechtsbündig oben rechts (wie „2022 −77%“).
Zeile 1 kommt erst grau-transparent, dann weiß (0,26 s), Zeile 2 kurz darauf. Harte Ersetzung beim nächsten Beat.
Schlagzeile zentriert 104 px mit einem Limette-Wort („Das muss **nicht** sein.“).
Titel: VERSALIEN 92 px, „KANZLEI WEBER · **STEUERBERATUNG**“, darunter JetBrains Mono Bold, darunter Limette-Pille mit dunkler Schrift.

## Kamera / Bewegung / Übergänge
Ein durchgehender Flug, keine harten Schnitte. Verfolgerkamera am Röhrenkopf, Blickwinkel wechseln per schneller Kamerafahrt
(0,13–0,6 s): von hinten, von vorn-unten (Röhre stürzt auf die Kamera zu → 2–3 Bilder Rotflut), seitlich (Diagonale),
Rausfahren in die Seitenansicht (ganze Kurve als dünne Leuchtlinie, Tore als Strichmarken).

## Die 5 Erkennungsmerkmale – und wie umgesetzt
1. **Leuchtröhre mit rundem Kopf über schwarzem Drahtgitter** → Three.js-Röhre + Kugelkopf, Shader-Gitter mit Nebel und Kopf-Glühen.
2. **Farbe = Richtung (gelb/orange/rot)** → Vertexfarben aus der Steigung; Lauf A wird nach dem Bescheid-Tor rot, Lauf B bleibt gelb.
3. **Quadratische Tore, die beim Durchfahren aufleuchten** → Bescheid-Tor, 4 Wochen-Tore, 12 Monats-Tore, 4 Quartals-Tore, Doppelrahmen „Maschine“.
4. **Zweizeilige fette Schrift oben links, Wert in Limette/Rot** → Bescheid −14.000 €, Fällig in 4 Wochen, Vorauszahlung +3.600 €, Polster 0 €, Maschine gestrichen, Januar…/Q1–Q4, Rücklage 14.000 €, Bescheid Bereit 14.000 €, Maschine gekauft.
5. **Rausfahren in die ganze Kurve + Schlagzeile / Titel mit Pille** → zweimal: beim Zurückspulen („Das muss nicht sein.“) und am Ende (Titel).
   Einziger Effekt-Moment wie im Original: die Glaswand (= der nächste Bescheid) zerspringt.

## Geschichte → Bild (Ton aus V4 unverändert, Ereigniszeiten aus ton/partitur.py übernommen)
Tor-Aufprall 1,09 s → Röhre kippt rot, stürzt durch die Kamera (Rotflut 1,72) · 4 Wochen-Tore 3,6–4,5 · 4 Treppenstufen abwärts 4,82–6,62 ·
Röhre landet auf dem Boden = Polster 0 € (8,21) · Maschinen-Tor erlischt und kippt um (10,06) · Rausfahren, rote Linie spult zurück (11,1–12,7) ·
Lauf B: Monats-Tore (Belege-Klicks), Quartals-Tore (Akkorde), Rücklage-Röhre zweigt bei Q1 ab und wird dicker, zählt bis 14.000 € (Münz-Ticks) ·
Glaswand zerspringt bei „Bescheid“ (21,83), die Rücklage endet dort, die Hauptlinie fliegt ungebremst weiter ·
Maschinen-Tor leuchtet auf (25,5), Röhre steigt steil · Rausfahren, Titel, Pille „Erstgespräch kostenlos“.

## Stilvergleich
**Runde 1** (`out/stilvergleich_1.jpg`): Serie passt (schwarz, Gitter, Röhre, Schrift). Abweichungen:
Wertzeile zu klein (118 → 136 px); roter Boden viel zu rot/rosa (Glühen reduziert, Linien-Tönung 0,3 → 0,18);
roter Röhrenkern wirkte rosa-weiß (Glanzlicht jetzt in Röhrenfarbe gemischt, 0,45 → 0,3);
in der Übersicht war das Gitter zu präsent (im Original fast unsichtbar → Linien in Übersichten auf 20 %);
Glasscherben-Kanten heller (0,6 → 0,85), Scheibe vor dem Aufprall dunkler/transparenter (0,16), Kamera beim Glas seitlich wie im Original.
**Runde 2** (`out/stilvergleich_2.jpg`): Q1-Tore liefen durch die Wertzeile, beim „Maschine gestrichen“ stand das Tor in der Schrift →
Kameras neu ausgerichtet, ferne Tore werden erst 30 Einheiten vor dem Kopf eingeblendet (wie im Original: ein Tor nach dem anderen),
Boden-Aufschlag weniger rot. Rückspul-Übergang lief durch die Kurvenebene (leere Bilder) → Kamera auf dieselbe Seite gelegt.

## Timing
Jede Textzeile beginnt 0,3 s vor ihrer Wortzeit (aus K / vo.json) und ist zur Wortzeit voll deckend (Einblendung 0,22–0,26 s).
Geprüft mit Streifen um 1,34 / 5,39 / 11,0 / 21,83 / 25,3 / 29,96 (`out/strips_all.jpg`).

# Stilbibel V5 – Netzwerk Nord IT, im Stil von „How browsers work in 40 seconds“ (Addy Osmani, X)

Quelle: `ref/original.mp4` (1920×1080, 24 fps, 40 s, Vollbild). 16 Einzelbilder in `ref/r_*.png`, Ausschnitte `ref/z_*.png`, Kontaktbogen `ref/kontakt.jpg`.

## Die 5 Merkmale, an denen man den Stil sofort erkennt
1. **Zwei Welten im harten Schnitt:** Papierwelt mit breiten Pastell-Diagonalstreifen ↔ nachtblaue Blaupause mit Raster und leuchtenden Lavendel-Linien. Kein Überblenden.
2. **Warme Tusche mit Schraffur:** dicke dunkelbraune Kontur (4,5–5,5 px) mit leichtem Zittern, Flächen mit dünner Diagonalschraffur auf der Schattenseite, schraffierte Schlagschatten am Boden und unter Tafeln.
3. **Knuddel-Figuren:** Knopfaugen mit zwei weißen Lichtpunkten, rosa Wangen, kleiner Bogenmund; der rote Roboter mit gelber Antennenkugel; Technik (Server) bekommt ein Gesicht und Gefühle.
4. **Konstruktionslinien:** feine graue Kreise mit Skalenstrichen und Fadenkreuz hinter dem Hauptobjekt, blaue gestrichelte Wege mit Punkt-Enden; in der Blaupause Maßlinien mit Pfeilen, Skalenringe um Symbole, Rahmenwinkel, Funkel-Sterne.
5. **Getippte Schrift:** Inter SemiBold, Satzanfang, erscheint Buchstabe für Buchstabe mit blauem Cursor, darunter ein kurzer gelber (Blaupause: cremefarbener) Marker-Strich; kleine Etiketten in Mono-Schrift in Pillen (wie `<body>`).

## Palette (gemessen mit PIL aus den Referenzbildern)
| Rolle | Hex | Quelle |
|---|---|---|
| Papier Creme | `#efe5cd` | r_5, r_16 |
| Streifen Blaugrau | `#c9d2cf` | r_5, r_0.5 |
| Streifen Mint | `#dbe4cc` (Film `#d8e3c8`) | r_16 |
| Streifen Gelb | `#ebdca4` (Film `#ebdba3`) | r_21 |
| Fensterpapier | `#f8f4ec` | r_0.5 |
| Tusche (dunkelste 1 %) | `#251b16` (Film `#2b211c`) | r_5 |
| Roboter-Rot | `#db6850` (Film `#dc6a52`) | r_5 |
| Server-Körper / Gesichtsfeld | `#79869b` / `#a9b5c6` | r_5 |
| LED Grün | `#91c37d` | r_5 |
| Unterstrich Gelb | `#e9cb7a` (Film `#e4bb45`) | r_0.5 |
| Nachtblau Rand / Mitte | `#0c0f29` / `#191e42` | r_3 |
| Hellste Linie Blaupause | `#e5eafa` | r_3 |
| Magenta (Fehler) | `#c12b89` gemessen, leuchtend `#ff3fa0` | r_3 |
| Mint (Glühen) / Lachs (Innenkontur Roboter) | `#7de6c9` / `#f39579` | r_3, r_24 |
Firmenfarbe von Netzwerk Nord IT = das Nachtblau der Blaupause; sonst keine Fremdfarben.

## Hintergrund und Papier
- Streifen: Winkel **29,8°** steigend (gemessen: Periode senkrecht 323 px, waagrecht 564 px), Bandbreite 140 px, Periode 280 px senkrecht zur Streifenrichtung; driften mit 38 px/s (Original: ca. 25 px/s; schneller wegen Standbild-Grenze).
- Korn: Helligkeitsrauschen Std.-Abw. ≈ 9 (gemessen 9,3) als Overlay 32 %, dazu 2 600 dunkle Sprenkel (0,5–2 px) und feine Fasern.
- Blaupause: Radialverlauf `#20275a` → `#0a0d26`, Raster 40 px (Alpha 5,5 %) und 200 px (9 %), 4 Konstruktionskreise mit Skalen, Rahmenwinkel in allen vier Ecken, Lineal links; Korn 22 % + helle Sprenkel.

## Linien
- Papier: Hauptkontur 4,5–5,4 px (Roboter 5,4, Server 5,2), Nebenlinien 2–3,5 px, Farbe `#2b211c`, runde Enden; Zittern 1–1,6 px Amplitude, dazu zweiter Zug 45 % Stärke leicht versetzt (unregelmäßige Tusche).
- Schraffur: Linien 3x+2y=c (≈56°), Abstand 5,5 px (Schatten, Alpha 0,5–0,75) bzw. 16–20 px (Flächenschattierung in dunklerer Eigenfarbe).
- Blaupause: 1,5–2,6 px Lavendel `#cdd1f3` mit Glühen (shadowBlur 6–14), Fehler in Magenta, Gutes in Mint.

## Figuren und Objekte
- **Roboter (Maskottchen Netzwerk Nord IT):** abgerundetes Quadrat 172×158, Glanz-Rechteck oben links, gelbe Antennenkugel, dünne Tuschearme mit roten Kugelhänden, schwarze Füße, schraffierter Bodenschatten. Hüpft, blinzelt, hebt Arme.
- **Server:** wie der Server im Original: Gesicht im Displayfeld mit 4 Schrauben, 5 Schubfächer mit Schiebestrich, Lüftungsschlitzen, LED mit Glühen, Kabel zum Boden. Zustände: fröhlich / „aus“ (LEDs erlöschen nacheinander, X-Augen, Rauch) / krank (Schweißtropfen, Wellenmund, gelbe Blink-LED).
- **Kolleg:innen:** Knubbel-Figuren wie die Speicher-Objekte im Original (Pastell lila, blau, türkis, gelb, rosa), an Holztischen mit Monitor (Warte-Kreisel / Arbeitszeilen), Denkblasen „…“.
- **Requisiten:** Brief mit rotem Siegel, Rechnung mit €, Festplatte mit Gesicht und Riss, Wanduhr, Sonne/Mond, Wolken mit Schraffur, Hängepflanze mit Ranken (Motiv „Rankpflanze“ des Originals), Holzbalken mit Nieten.

## Typografie
- Inter SemiBold (600), Satzanfang wie im Deutschen, **keine Versalien**, 72 px (Schluss 84–104 px), Laufweite −1 px, links bei x = 110, Zeilen bei y = 150/240/330.
- Bewusst größer als im Original (dort 34 px Kapiteltitel), weil die Schlagworte hier die Botschaft tragen und stumm lesbar sein müssen. Keine Ecktexte, kein Kapitelring.
- Tippen mit blauem (Blaupause: mintfarbenem) Cursor; Marker-Strich unter dem Schlüsselwort.
- Etiketten: IBM Plex Mono SemiBold 22–27 px in Pillen (Papier: Creme + Tusche, Blaupause: Linie mit Glühen).

## Bildaufbau, Kamera, Bewegung
- Hauptobjekt rechts oder Mitte, Konstruktionskreis dahinter, Boden bei ~80 % Höhe; Schlagzeile oben links.
- Kamera: ruhige Schübe (1,00 → 1,03), ein Rausfahren (1,0 → 0,66) für „20 Leute“.
- Bewegung mit Bedeutung: Weg zeichnet sich → Paket läuft; Fehler = Unterbrechung (Magenta-Kreuz im Ring); Verwandlung (Datenpaket bekommt Schloss); Figuren reagieren (Mimik, Hüpfen); Aufmerksamkeitsring dehnt sich aus.
- Übergänge: harte Schnitte zwischen Papier und Blaupause, immer vor dem ersten Wort der neuen Zeile.

## Szenen (Geschichte aus V4)
| Zeit | Welt | Inhalt |
|---|---|---|
| 0–5,2 | Papier blau | Server geht aus, Brief/Rechnung stecken fest, Rausfahren auf 20 wartende Kolleg:innen |
| 5,2–10,6 | Blaupause | leerer Sicherungs-Platz (gestrichelte Pille mit „+“), Kundendaten zerbrechen; Zustandskurve fällt über 6 Wochen |
| 10,6–13,1 | Papier mint | Roboter am Leitstand, Herzschlag-Monitore, Wanduhr mit Sonne und Mond, Bogen „rund um die Uhr“ |
| 13,1–16,45 | Papier gelb | Roboter tauscht die kranke Festplatte, bevor sie ausfällt |
| 16,45–20,0 | Blaupause Nacht | Pakete bekommen Schlösser, fliegen ins Rechenzentrum |
| 20,0–23,3 | Blaupause | Notfall-Alarm, Stoppuhr < 60 min, Daten kommen zurück, Server grün |
| 23,3–25,0 | Papier blau | gleiches Büro, alle arbeiten, Mails fließen |
| 25,0–30,6 | Blaupause | Schluss im Browserfenster (wie das Ende des Originals): Firma, IT-Check kostenlos, Telefon, Adresse |

## Stilvergleich
**Runde 1** (`out/stilvergleich_1.jpg`): Papierwelt und Figuren sitzen (Streifen, Tusche, Schraffur, Server-Gesicht). Abweichungen:
Blaupause zu leer (Original hat Maßlinien, Skalenringe, Knotenpunkte); Wolke lag in der Schlagzeile; Weitwinkel-Büro mit Figuren hinter den Monitoren verdeckt; Brief und Rechnung überlagerten sich; Blaupausen-Wangen als Strich verbunden; Mond falsch.
**Geändert:** `tickRing`, `nodeDot`, `dimLine` eingeführt und in allen Blaupausen-Szenen gesetzt; Lichtpaket auf Verbindung Server → Messkurve; Figuren hinter die Tische gesetzt, Kamera auf 0,66; Wolke verlegt; Brief/Rechnung auf getrennte Haltepunkte; Mond mit Kratern und Schraffur; Rankpflanzen (Hängekorb) im Büro und am Leitstand; Tauschszene neu getaktet.
**Runde 2** (`out/stilvergleich_2.jpg`): Beide Seiten lesen sich als eine Serie. Restpunkte: Weitwinkel unten leer → schraffiertes Erdband ergänzt (wie im Garbage-Collection-Bild des Originals).

**Runde 3** (`out/stilvergleich_3.jpg`): Standbild-Anteil war 24 % → Streifen-Drift 38 px/s, langsame Kamerafahrten (1,00 → 1,05) in allen Blaupausen, schwebende Karten. Wolken und Dach aus der Schlagzeile genommen, Server im Schlussbild des Büros ganz im Bild.

## Messwerte (dichte.py, `out/dichte.json`)
| | Original | V5 |
|---|---|---|
| Standbild-Anteil | 15 % | 11 % |
| Bewegung | 8,5 | 3,9 |
| Schnitte je 10 s | 4,2 | 1,6 |
| Farbigkeit | 22,1 | 26,2 |
Timing: Streifen `out/strip_*.jpg` um 8 Schlüsselwörter geprüft – Bild und Schlagwort stehen jeweils zur Wortzeit.

## V6 – Text-Regie (REGIE_TEXT.md)
Alle getippten Schlagzeilen entfernt (Merkmal 5 „Getippte Schrift“ gilt nicht mehr). Text nur noch als Beschriftung an Objekten
(„MO“ am Kalender, „Kundendaten“, W1–W6, „Netzwerk Nord IT“ auf der Leitstand-Theke, „Festplatte“, Stoppuhr-Ziffern, „< 60 min“) und auf der Schlusskarte (Maske/Stempel, nie getippt).
Bildhandlung ergänzt: Wanduhr springt auf 8:00 + Kalender „MO“ (Szene A und H), Mail/Rechnung prallen am Server ab und werden durchgestrichen,
Fragezeichen-Blasen und Blick zum Server, gestrichelter Speicher-Zylinder als fehlende Sicherung, Pfeil auf erstes Warnzeichen bei W2, Kreuz statt „Ausfall“,
24-h-Umlauf von Sonne/Mond/Zeigern bis „Uhr“, Etikett wandert mit der alten Platte, die auf „ausfallen“ am Boden ausfällt, Logo-Roboter baut sich als Linie auf.
Prüfung: `out/textbogen_teil1–3.jpg`.

## V7 (neu) – keine Sätze, Betonung über Bildmittel (REGIE_TEXT_V7.md)
Wortzeiten mit werkzeuge/wortzeiten.py neu vermessen (bis 0,9 s später als vorher), „IT-Check“ von Hand auf 27,63 s (Sprechpause gemessen).
zeiten.py leitet jetzt alle K und alle Schnitte (CUT) daraus ab; film.js enthält keine festen Sekundenwerte mehr. Partitur neu gemischt.
Text nur am Objekt: ONLINE/OFFLINE (Statuslampe), MO, Kundendaten, W1–W6, Netzwerk Nord IT (Theke), 24/7 (Zifferblatt), Festplatte, < 60 min, Schlusskarte.
Betonung: Status-Ring rot/grün, rotes Durchstreichen, roter Kreis, Lupe mit Vergrößerung bis W2 + Aufleuchten, Maßlinie, alte Platte rot / neue grün mit Häkchen, Rechenzentrum leuchtet auf.

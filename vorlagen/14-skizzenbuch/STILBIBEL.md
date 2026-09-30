# STILBIBEL 14 – g russ „Emergence“, Version 3 „Illustrated (Final)“

Referenz: `ref/v3_crop.mp4` (rechte Hälfte des Seite-an-Seite-Vergleichs, 640×360, 300 s). Angesehen: 24 Einzelbilder
(t = 8, 22, 30, 38, 50, 58, 73, 75, 84, 88, 100, 108, 125, 135, 162, 168, 170, 185, 205, 225, 250, 258, 276, 285)
plus 3×-Ausschnitte (Lego-Pyramide, Glühbirne, Titel, Holz, Navy-Kreise). Tafel-Folge per 1-fps-Farbanalyse bestimmt.

## Die 5 Merkmale, an denen man den Stil erkennt
1. **Wechselnde „Tafeln“ statt Hintergrund**: Holzdielen, Nachtblau mit Haarlinien-Kreisen und Lineal, Karo-Quilt,
   blassblaues Papier mit weißen Schrägbändern, Pergament mit weichen Bernstein-Schrägstreifen, Orangepapier mit Fasern.
   Jede Tafel ist wolkig-fleckig und gekörnt, nie flach.
2. **Kleine, gedeckte Objekte mit Tuschekontur + Schraffur + weichem Schatten**: flache Farbfläche, leicht zittrige
   dunkle Kontur (≈1,3 px bei 640 → 3,5–4 px bei 1080p), feine Diagonalschraffur („/“) im Farbton, hellere Oberkante,
   weicher Schlagschatten nach rechts unten.
3. **Runde Filzstift-Handschrift**, die sich im Sprechtakt von links nach rechts aufwischt (weiche Kante, kein Stift
   sichtbar). Titel dunkel/ cremeweiß, Schlagworte farbig und schräg (Koralle, Petrol, Blau).
4. **Viel Luft**: Objekte klein, Bildmitte, eine dünne Bodenlinie; nie vollgestellt.
5. **Strichfiguren** mit rosa Kopf (Kontur) und dünnen Tuschelinien; auf Navy werden Linien cremeweiß.

## Palette (PIL-Median aus den Referenzbildern)
| Rolle | Referenz | V5 |
|---|---|---|
| Nachtblau | `#0f1327` (1-fps-Median), Wolken `#1d2446` | `#0f1327` + Wolken `#232b52/#1c2347` |
| Pergament | `#d8c8a9` (Median), hell `#e7dbc1`, Streifen `#d4a257`/`#e9d3ab` | `#dccdad`, Streifen `#efc47f` 42 %, Blur 30 |
| Blaupapier | `#bdcacc` | `#bdc9cb`, weiße Bänder 42 % |
| Karo-Quilt | `#c5c2b6` Mittel (Blau `#c9d2d0` / Creme `#e6dabf`) | wie gemessen, Kästchen 124 px, Blütenornament 13 % |
| Holz | `#c29663` (Spanne `#af8655–#d3a46b`) | `#c29663`, Dielen 230–300 px, Fugen `rgba(95,62,32,.55)` |
| Orange | `#cf8c5b` | `#d18c5c` + 2600 Fasern |
| Tusche | `#1f1a14`/`#210700` | `#2a2320` |
| Koralle (Stein/Text) | `#d7795a` / `#ec704f` | `#d7795a` / `#dd6547` |
| Petrol | `#478789` | `#478789` / Text `#3b8a80` |
| Gold | `#d09f48`, Birne `#d1a356` | `#d09f48` |
| Salbei | `#8c9f72` | `#8c9f72` |
| Blau | `#6080aa` | `#6080aa` |
| Kreide auf Navy | `#f9f4f1` | `#efe8dc` |
| Kopf der Strichfigur | `#e6a291`-artig | `#e7a393` |

Firmenfarben (Lernwerk): keine eigene Palette nötig – Petrol/Koralle/Gold der Referenz tragen die Marke.

## Linien, Flächen, Details
- Kontur 3,2–4 px, `lineJoin round`, statisches Handzittern (±1,1 px, niederfrequent, kein Kochen – das Original ist ruhig).
- Schraffur: Linien „/“ im Abstand 5,5–7 px, 1,3 px, Farbton −38 %, 42 % Deckkraft über die ganze Fläche, untere Hälfte doppelt.
- Glanzkante: oberste 16 % der Fläche +22 % heller.
- Schatten: `rgba(55,35,15,.30)`, Versatz 6/7, Blur 9 (auf Navy schwarz 45 %).
- Lego-Steine wie im Original: Körper + 2–4 Noppen, jede Noppe mit eigener Kontur.
- Glühen nur bei Lichtquellen (Lampe auf Navy, Glühbirne, Lücke unter der Lupe), additiv, weich.

## Typografie
- Referenz: Segoe-Print-artige runde Handschrift; Titel fett gemischt („Nature“, „advice“) oder Versalien („EMERGENT“),
  Beschriftungen dünn („simple things“), Schlagworte farbig, leicht schräg („fractal crystals“).
- V5: Kalam Bold (Titel 84–104 px, Versalien 100 px mit +4 px Sperrung, Marke 176 px), Kalam Light (Beschriftungen 54–58 px),
  Kalam Regular 20 % geschert, +2 px Sperrung (Schlagworte 66–84 px). Titel oben links (x≈220–300) oder mittig oben wie im Original.
- Unterstreichung: ein zittriger Strich in Koralle/Petrol unter dem Titel, zeichnet sich nach dem Titel.

## Bildaufbau, Kamera, Bewegung, Übergänge
- Objekte in der Mitte auf dünner Bodenlinie, Titel oben, Schlagwort unter dem Objekt.
- Übergänge: 0,32–0,40 s Überblendung zwischen Tafeln (wie Original), innerhalb einer Tafel Kamerafahrten (Treppe, 8 Wochen).
- Aufbau: Kontur zeichnet sich (0,3 s), Fläche + Schraffur blenden ein; Steine fallen und federn nach; Text wischt auf.
- Dauerbewegung: langsame Kamerafahrt ≈14 px/s je Tafel in wechselnder Richtung, Uhrzeiger, Lampenflackern, schwebender
  Stein, Lupe sucht, Kind läuft nach Hause.

## Geschichte → Bilder (Lernwerk Nachhilfe)
Holz: Klassenarbeit mit roter Fünf, Kind geht nach Hause, „Mathe“, „× 3 schon wieder“ (zwei weitere Arbeiten) →
Nachtblau: „JEDEN ABEND“, Uhr rast, Lampe, Streit-Wolken, „Hausaufgaben“; Fahrt zur Treppe „Klasse 5/6/7“, oberste Stufe
wackelt und reißt, „Versetzung?“ → Karo-Quilt: Lego-Pyramide mit Lücke, „Es fehlt nur ein Baustein“, Lupe findet die Lücke,
Stein fliegt hinein, Banderole „kostenlose PROBESTUNDE“ → Blaupapier: Wochenkarten, Di/Do eingekringelt, Tisch mit drei
Kindern, „max. 3 Kinder“, „eine Gruppe“; Fahrt: 5 → 8 Punkte → grüne 3 → Pergament: Kind mit Glühbirne, „rechnet wieder
gern“ → Orange: LERNWERK-Titelkarte mit Kritzel-Icons wie „EMERGENCE“, Banderole, Kontakt.

## Stilvergleich
**Runde 1** (`out/stilvergleich_1.jpg`): Tafeln, Steine, Schraffur, Banderole treffen das Original. Abweichungen:
Titel zu fett/groß; Lampe auf Navy mit hartem Lichtrechteck; sitzende Strichfiguren zu klein (Kopf auf Tischhöhe);
Bernsteinstreifen zu gesättigt; Streuspan eines leeren Texts sichtbar.
→ Geändert: Titelgrößen −10–12 %, Unterstreichungen angepasst; Lichtkegel als weich geblurrtes Dreieck + runder Lichtfleck;
Tisch tiefer, Figuren 290–300 px; Streifen 42 % statt 50 %, Blur 30; Text mit Fortschritt 0 wird nicht mehr gezeichnet;
„1“ (las sich wie „l“) → Wort „ein“ in Koralle.
**Zwischenschritt**: `dichte.py` ergab 48 % Standbild → Dauer-Kamerafahrt je Tafel (≈14 px/s) und laufendes Kind → 0 %.
**Runde 2** (`out/stilvergleich_2.jpg`): Beide Spalten wirken wie eine Serie (Holz/Navy/Quilt/Blau/Pergament/Orange,
gleiche Stein- und Figurenhandschrift). Geändert danach: Kind läuft vor den Arbeiten statt dahinter.

## Ehrliche Abweichungen
- Kalam ist etwas fetter und kantiger als Segoe Print; die schräge Schreibschrift des Originals ist nur angenähert (gescherte Kalam).
- Unsere Objekte sind größer und dichter als im Original (Werbung muss auf dem Handy lesbar sein).
- Keine Schwärme/Partikel-Simulationen wie im Original; Bewegung kommt aus Aufbau, Kamerafahrt und Figuren.

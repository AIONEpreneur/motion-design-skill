# STILBIBEL 15 – dunkle „Story“-Panels (Jack Roberts, Claude Design: „Reels with custom graphics“ + „Logo + jingle“)

Referenz: Vollbild-Ausschnitt des dunklen Vorschau-Panels (crop 588×330 @ 373,312 aus HOXrLsVqinY.mp4),
`ref/panels.mp4` = 0–30 s Reel-Panel (ab 492 s), 30–60 s Logo+Jingle-Panel (ab 772 s). Angesehen: 10 Einzelbilder
(494, 500, 505, 512, 518, 776, 780, 785, 790, 797 s) + 3×-Ausschnitte von Telefon, Goldpapier, Porträt, Scheibe.

**Wichtigster Fehler von V4:** Sie hat bewusst „Nachtschwarz + Creme + Gold nicht übernommen“ und stattdessen flache
Orange/Grün-Cartoons gebaut. V5 übernimmt genau diese Bildwelt.

## Die 5 Merkmale, an denen man den Stil erkennt
1. **Nachtschwarze Bühne mit warmer Mitte und Horizont-Glut**: `#08080a` am Rand, warme Mitte `#22201b`, unten ein
   flacher glühender Bogen mit goldener Kante.
2. **Ein zentriertes Heldenobjekt aus feinen Linien**: Telefon-Umriss (1,5 px bei 588 → 3,4 px), Innenkante, Dynamic Island,
   Seitentasten; oder die Creme-Scheibe mit Terrakotta-Sonne über dunklem Erdbogen, umgeben von Haarlinien-Kreisen.
3. **Gerissenes Papier als Bildträger**: Goldpapier mit Maserung und eingravierten Zirkel-/Jahresring-Linien + schwarzem
   4-Zack-Stern; Knitterpapier mit Tuschezeichnung (Porträt, Möbel); schwarz-weiß gestreifter Streifen am Rand;
   Fransenkante hell, weicher Schatten. Verbunden durch **gepunktete Bogenpfeile**.
4. **Creme-Serife (Garamond)**, ruhig, zentriert, ein Satz pro Bild; Terrakotta nur als Akzent (das „+“, ein Wort kursiv).
   Kleine Etiketten als dunkle Pillen mit Serifenschrift („Use them together“).
5. **Treffer = Wellenringe**: 2–3 dünne Ringe laufen nach außen und verblassen; die Scheibe wächst aus einem
   Terrakotta-Punkt mit Überschwingen und leert sich zum Umriss.

## Palette (PIL, Referenz)
| Rolle | Referenz | V5 |
|---|---|---|
| Grund Rand | `#08080a` | `#08080a` |
| Grund Mitte | `#22201b`, unten `#312621` | radial `rgb(38,34,30)` → transparent |
| Horizont-Glut | `#928177`–`#b3a293` Kante | Bogen `rgba(200,150,105,.5)` Blur 10 + Kante `rgba(235,205,170,.8)` |
| Goldpapier | `#b48837` (5 % `#976d20`, 95 % `#c8973c`) | `#b48837` + Maserung ±, Rand `#e9d7a6` |
| Knitterpapier | `#c4c0b7` | `#d9d5cd` + Knitterflächen, Vignette |
| Scheibe | `#e7e1d9` | Verlauf `#f6f2ec` → `#cfc6ba` |
| Terrakotta | `#d97558` | `#d9755a` (hell `#ec8669`) |
| Serifenschrift | `#f7f7f5` | `#f4f1ea` |
| Telefon-Umriss | `#a4a4a6` | `#a4a4a6` |

## Linien, Details
- Telefon: Außenkontur 3,4 px `#a4a4a6`, Innenkante 1,5 px 35 %, Radius 15 % der Breite, Schatten 40 px.
- Tusche auf Papier: 2,2–2,6 px `#1d1a17`, Schraffur 1,1–1,4 px 30–35 %, Wangen rosa 18 %.
- Gravur auf Gold: 1,4–1,5 px `rgba(55,36,8,.6)`, teils gestrichelt.
- Hilfskreise: 1,5 px Creme 22 % / 10 %, Speichen, Achskreuz.
- Ringe: 2 px, Deckkraft 45 % → 0 in 1,3 s, 0,16 s gestaffelt.

## Typografie
EB Garamond Regular, durchgehend aufrecht (Sätze 62–120 px); Terrakotta-Akzentwörter und Unterzeilen ebenfalls aufrecht – keine Kursive (Vorgabe des Auftraggebers).
Keine Versalien, keine Sperrung. Wörter blenden einzeln weich ein (0,3 s, 14 px Steigen), fertig zur Wortzeit.

## Bewegung, Kamera, Übergänge
- Scheibe: Punkt fliegt im Bogen ein → wächst mit back-out → Sonne steigt → Ringe.
- Papier schwebt ±4–5 px, dreht ±1°; Pfeile zeichnen sich punktweise.
- Telefon zeichnet seine Kontur (Drahtrahmen), dann gestrichelte Platzhalter, dann Inhalt.
- Überblendungen 0,3–0,35 s; langsame Kamerafahrt ≈9 px/s je Szene.

## Geschichte → Bilder (Werkseite / Tischlerei Holm)
Kunde (Tuscheporträt) → Telefon mit Suche „Tischler in der Nähe“ ↔ Goldpapier mit Jahresringen → alte graue Website;
Terrakotta-Kreise + Papieretiketten „winzige Schrift / kein Foto / keine Nummer“ → Scheibe mit Porträt läuft in 2 s leer,
„weg.“ → Goldpapier „Einbauschrank“ wandert auf dem Punktbogen zum leuchtenden Telefon des Betriebs nebenan →
Tuschezeichnung Einbauschrank + Stern-im-Ring „besser.“ → Werkseite-Scheibe (Haus auf dem Horizont) wächst aus dem
Punkt, Telefon-Drahtrahmen, 14 Punkte füllen sich → neue dunkle Website: Logo (Stern im Kreis), Projektpapiere,
Terrakotta-Knopf → Anruf „Neuer Kunde“ mit Ringen, drei Anfragen-Pillen → Marken-Endbild mit Goldpapier und
Streifen am Rand.

## Stilvergleich
**Runde 1** (`out/stilvergleich_1.jpg`): Bühne, Telefon, Papier, Scheibe und Serife sitzen. Abweichungen: Horizont-Glut
zu breit und zu hell (nach Korrektur der Lage), Auftrags-Papier verdeckte den Kopf der Nachbar-Website, Porträt-Haare
wirkten wie eine Mütze, Textzeilen der alten Seite zu dick, Projektpapiere zu klein.
→ Glut schmaler (8 px, 50 %), Auftrag landet in der Bildschirmmitte, Haare mit Scheitel/Fransen, Zeilen 2 px,
Projekte 60 % statt 42 %, drittes Projekt auf Goldpapier, Goldpapier-Ecke auch in der Werkseite-Szene.
**Runde 2** (`out/stilvergleich_2.jpg`): links/rechts wie aus derselben Serie.

## Ehrliche Abweichungen
- Mehr Text als im Original (die Werbung braucht die Botschaft stumm lesbar); die Referenz zeigt meist nur „Logo + jingle“.
- Porträt und Möbel sind prozedural gezeichnet – etwas einfacher als die Illustration im Original.
- Keine UI-Leiste oben (Player-Pille) übernommen.

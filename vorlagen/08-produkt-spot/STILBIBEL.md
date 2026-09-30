# STILBIBEL V5 – 08 Quellwerk Office, nach dem KI-Getränkespot „EnergyAI Tropical“ (Felipe Borges)

Referenz: `ref/vollbild.mp4` (Spot im Player, 1120×630, 19,6 s), Einzelbilder `ref/bilder/` (14 Stück).
V4 war flache Vektor-Grafik (Clipart-Spender, gerade Farbflächen, Untertitel) – das Original ist ein fotorealistischer Produktspot.
V5 wird deshalb komplett in **Blender/Cycles** gerendert (`blender/*.py`, deterministisch, Metal-GPU) und im Film nur noch geschnitten,
mit Schlagworten versehen und nachbelichtet.

## Palette (Pipette auf Originalbildern, siehe auch ../STIL.md)
| Rolle | Hex |
|---|---|
| Himmel/Bokeh Creme | `#F9DFAE`, Pfirsich `#F9E7AD`, Sonnenkern `#FFFEFA` |
| Bernstein / Gegenlicht-Schatten | `#D19A63` / `#91530A` |
| Etikett Orange → Magenta → Türkis | `#E99216` → `#C72847` → `#2BC3D2` |
| Schriftgelb (Pinsel, dunkle Kante) | `#E0A20D`, Kante `#78143C` |
| Blattgrün | `#3C5412` |
Unsere Umsetzung: Etikett-Verlauf `#F4A21A → #EE6A2A → #D22E6E → #8E3FB8 → #22C4D8`, Himmel `#F1CD93 → #FBE4B2`, Pinsel `#F7BE10` mit Kante `#78143C`,
Marke „Quell“ weiß + „werk“ türkis `#40E2EA` (wie „Energy“ + „AI“).

## Hintergrund / Licht
Immer goldene Stunde im Gegenlicht: Sonne tief hinter dem Produkt, cremig-goldener, stark unscharfer Hintergrund (Blende 2,8–3,2),
Bokeh-Lichter, Lichthof (Bloom im Film). Kein Papier, kein Korn. Statt Meer: dunstige Stadtkante (Büro-Welt), Jalousie-Licht im Problem-Teil.

## Linien / Oberflächen
Keine Linien – Fotooberflächen: Glas mit Brechung, Kondenstropfen (420 Tropfen auf der Flasche), nasser dunkler Lavastein,
Wasserkranz (verformter Torus), Zeitlupen-Spritzer, Kaffeebohnen mit Kerbe, Eiswürfel mit Relief, Monstera-Blätter (durchscheinend).

## Detailgrad der Objekte
- Hero-Flasche: Glas mit Wandstärke, Wasser innen, Rundum-Etikett im Dosen-Stil (Marke, gelbe Pille „BÜRO-SERVICE“, Pinsel „FRISCH“, Zeile mit Mittelpunkten), Deckel eloxiert türkis.
- Tasse mit gleichem Verlauf als Glasur, Crema mit Latte-Art-Herz, türkise Untertasse.
- Chrom-Wandhahn mit türkisem Ring und Druckknopf, Filterkartusche, Lieferkarton (Kraft mit Verlaufsband).

## Typografie
Wie auf dem Etikett des Originals, als Schlagworte im Bild: Poppins ExtraBold weiß mit Schatten (Marke mit türkiser Silbe),
gelbe Pille mit dunkler Schrift (Poppins ExtraBold), gelbe Pinsel-Versalien Knewave mit dunkler Kante, leicht schräg.
Einblendung als „Pop“ mit Überschwinger, beginnt 0,3 s vor dem Wort, steht zum Wort.

## Bildaufbau, Kamera, Übergänge
Produkt groß und zentral, Makro-Details, langsame Push-ins/Drifts; harte Schnitte im Takt, ein **Blatt-Durchflug** (S4, wie Einstellung 2 im Original),
ein **Reißschwenk** in den Packshot (S8→S9, 27,5–28,0 s), langer Packshot am Schluss. Neon-Lichtstreifen pink/türkis beim „Öffnen“ (Karton, S7)
und türkise Blitzbögen über den schwebenden Zutaten (S5).

## Die 5 Erkennungsmerkmale – Umsetzung
1. **Goldene-Stunde-Gegenlicht mit cremigem Bokeh** → Sonnen-Lampe hinter dem Produkt, Himmelskulisse mit Sonnenhof, Blende 2,8, Bokeh-Kugeln, Bloom im Film.
2. **Knallbuntes Etikett Orange→Magenta→Türkis mit Pinsel-Schrift** → eigenes Quellwerk-Etikett (tex.py) auf Flasche, Tasse, Kartusche, Karton.
3. **Makro mit Kondenswasser/Tropfen** → S1 (letzter Kaffeetropfen), Tropfen auf der Flasche in allen Produkteinstellungen.
4. **Zeitlupen-Spritzer, Wasserkranz, schwebende Zutaten** → S5 (Filter, Eis, Perlen), S5c (Flasche im Wasserkranz), S6 (Bohnenkranz um die Tasse), S7 (Explosion aus dem Karton), S8 (Anstoßen).
5. **Blatt-Durchflug + langer Packshot auf nassem Stein mit Monstera** → S4, S9.

## Geschichte → Einstellungen (Ton aus V4)
S1 0–2,62 leere Kanne, letzter Tropfen (1,95) · S2 Wasserkasten landet (3,02), Flasche kippt (3,8) · S3 sechs Kisten stapeln sich (5,28–5,63), Kamera fährt hoch zum „3. OG“ ·
S4 Blatt-Durchflug → Chrom-Hahn, Wasser fließt bei „Leitung“ (11,52) · S5 Filter/Eis/Perlen · S5c Flasche im Wasserkranz, Zeitlupe (15,05–16,95; „Knopfdruck“ als Pille) ·
S6 Bohnenkranz um die Tasse, Mahlen (18,14) · S7 Karton springt auf (22,94) · S8 Glas und Tasse stoßen an (25,31) · S9 Packshot + Angebot.

## Stilvergleich
**Vorab (Probe-Standbilder, 3 Runden in Blender):** Lavastein spiegelte als silberne Fläche (Fresnel) → Specular 0,14, ohne Klarlack;
Tropfen auf dem Etikett wurden schwarz (Totalreflexion) → eigenes Tropfen-Material; Trinkglas schwarz (Solidify) → geschlossenes Profil;
Stadtkulisse las sich wie ein Bücherregal → neuer Himmel mit niedriger, dunstiger Stadtkante; Spender-Klotz (Clipart-Nähe) → Chrom-Wandhahn;
Kistenstapel: Aussparungen fehlten (Schneidkörper nicht mitbewegt) → mitgeführt.
**Runde 1** (`out/stilvergleich_1.jpg`): gleiche Farbfamilie und dieselben Bildideen (Makro-Tropfen, Blätter, Kranz, Explosion, Packshot),
aber blass, milchig, zu wenig Kontrast, Produkte zu klein. → Film: Kontrast 1,25, Sättigung, warmes Gegenlicht (soft-light) mit dunklen Rändern,
Ausschnitt je Einstellung 1,06–1,22× vergrößert (Produkt größer wie im Original). S5b (Knopf-Makro) sah wie ein beiger Klumpen aus → gestrichen,
S5c stattdessen als Zeitlupe mit überblendeten Zwischenbildern gedehnt. Schlagworte aus dem Produkt heraus an freie Bildstellen gelegt.
**Runde 2** (`out/stilvergleich_2.jpg`): jetzt zu zitronengelb/übersättigt → Sättigung 1,45 → 1,18, Lichtfarbe amber statt gelb, Ränder dunkler.
**Runde 3** (`out/stilvergleich_3.jpg`): goldene Stunde, Tiefe und Produktgröße deutlich näher am Original.

## Timing
Schlagworte beginnen 0,3 s vor dem Wort (Pop 0,26 s) und stehen zum Wort; geprüft mit Streifen um 1,84 / 3,8 / 6,04 / 10,51 / 14,98 / 22,89 s (`out/strips_all.jpg`).

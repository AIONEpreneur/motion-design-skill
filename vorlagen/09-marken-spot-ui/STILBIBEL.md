# STILBIBEL V5 – 09 Klarwerk Reinigung, nach dem Nomad-Werbespot (Fernando Araujo, Remotion)

Referenz: `ref/vollbild.mp4` (Player-Ausschnitt 1044×586, der Spot läuft mehrfach), Einzelbilder `ref/bilder/` (17 Stück).
V4 hatte ausdrücklich „Creme-Grund und Nomad-Gelb nicht übernommen“, Mint/Petrol-Flächen, Cartoon-Figuren und Untertitel –
genau das hat den Look zerstört. V5 übernimmt die Farbwelt 1:1.

## Palette (mit PIL gemessen, r_76.png / r_9.png)
| Rolle | Hex |
|---|---|
| Creme-Grund | `#F0EDE0` |
| Markengelb (Kreis, Buttons, Endkarte) | `#FBCC00` |
| Tinte (Headlines, große Zahl, Linie) | `#221004` |
| Sperrbildschirm oben → unten | `#4D2810` → `#1E0C03` |
| Mitteilungskarte | `#E9E6DD` (hell, leicht transparent) |
| Grau-Text UI / Label | ca. `#8C8578` / `#C3BFB2` |
| Telefonrahmen | `#120C09` |
Klarwerk-Farbe = das Gelb (Zitrone/Putz-Gelb passt zur Branche); Akzent Grün `#2DB35B` nur im Häkchen.

## Hintergrund
Plane Creme-Fläche ohne Textur; ein großer gelber Kreis (Ø 860 px) als Bühne hinter dem Telefon; Endkarte vollflächig gelb.
Lifestyle-Bilder: warme Kino-Fotografie (bei uns Cycles-Renderings der Büroküche mit echtem Sonnenlicht durch Jalousien, geringe Schärfentiefe).

## Linien / Formen
Keine Konturen. Weiße UI-Karten mit Radius 18 px, feinem Rand `#E6E1D3`, weichem Schatten; Pillen-Buttons gelb mit dunkler Schrift,
gebucht dunkel mit heller Schrift („✓ Gebucht“ wie „✓ Cartão solicitado“). Segmentierte Linie unter der großen Zahl (4 bzw. 6 Striche à 150 px, 5 px dick).
Logo aus drei abgerundeten Balken (K), die sich zusammenschieben; Wortmarke wird seitlich aufgedeckt (wie NOMAD).

## Detailgrad
Telefon 450×960 px (≈ 89 % Bildhöhe wie im Original), schwarzer Rahmen, Dynamic Island, Statusleiste „9:41“ + drei Punkte, echte App-Oberfläche mit
Mauszeiger (macOS-Pfeil), Tippen, Zustandswechsel. Sperrbildschirm: Datum, große Uhrzeit, Mitteilungen mit App-Icon, Titel, Text, „jetzt“, Foto-Vorschau.

## Typografie
Headlines: Familjen Grotesk Medium (hakiges r), 185 px, linksbündig, Satzpunkt, Wort für Wort aus der Unschärfe (blur 12 → 0, 0,3 s, leicht von unten).
Große Zahl: Familjen Grotesk 150 px Tinte; Label darüber DM Sans 26 px grau mit Farbpunkt; Bildunterschrift 24 px grau.
UI: DM Sans 15–34 px.

## Bildaufbau, Kamera, Bewegung, Schnitt
Telefon fährt von unten ein (quint-out), Kreis wächst gleichzeitig aus der Mitte; bei Zahl-Szenen steht das Telefon links (x 760) und die Zahl rechts
an der Kreiskante. Mitteilungen fallen oben ein und schieben den Stapel nach unten, die Zahl zählt synchron mit. Harte Schnitte zwischen
Einstellungen, Lifestyle 1,5–2,6 s, UI 4–6 s. Kein Glitch, kein Whip.

## Die 5 Erkennungsmerkmale – Umsetzung
1. **Creme + EIN sattes Gelb + dunkelbraune Tinte** → exakt gemessene Werte, keine weiteren Flächenfarben.
2. **Telefon vor großem gelben Kreis, echte UI mit Mauszeiger** → zwei App-Bildschirme (Räume wählen; Fläche/Rhythmus/Festpreis) + Erfolgsbildschirm.
3. **Sperrbildschirm mit fallenden Mitteilungen + große Zahl rechts mit segmentierter Linie** → 9:00-Termin am Morgen; abends 6 Räume als Häkchen mit Foto, „1/6 … 6/6“.
4. **Headline Wort für Wort aus der Unschärfe** → „Montag, 8 Uhr.“, Endkarte „Die erste Reinigung schenken wir Ihnen.“
5. **Warme Lifestyle-Fotos + Endkarte in Vollgelb mit Balken-Logo** → Cycles-Küche (Montag schmutzig, abends Reinigungswagen mit Namensschildern, Morgen glänzend), gelbe Endkarte.

## Stilvergleich
**Runde 1** (`out/stilvergleich_1.jpg`, nur UI-Teile): Farben, Telefon, Kreis, Zahl, Sperrbildschirm wirken wie aus derselben Serie.
Geändert: Headline größer (150 → 185 px) und weiter links wie im Original; Endkarte: Logo + Wortmarke als Block mittig (vorher nach rechts versetzt);
Telefon/Kreis in Zahl-Szenen nach x 760, Zahl an die Kreiskante (x 1190) wie im Original; Mitteilungskarten flacher (96 px), damit 6 Stück passen.
**Runde 2** (`out/stilvergleich_2.jpg`, jetzt mit Lifestyle): UI weiter deckungsgleich. Lifestyle-Renderings wirkten grau, flach, taghell
(„Archviz“) statt warmer Low-Key-Kinobilder. Geändert: Küche bekommt eine echte Fensteröffnung mit Jalousie – die Sonne fällt in Streifen herein;
Umgebungslicht fast aus, AgX Medium High Contrast; Nachtbild dunkel mit warmem Pendel- und Wagenlicht; b1 neu als Totale (Flecken am Boden,
überquellender Müll, Geschirrberg) statt nur Schrankfronten.
**Runde 3** (`out/stilvergleich_3.jpg`): Nachbelichtung im Film (Kontrast 1,3, Sepia/warm, starke Vignette, 3 % Push-in) → Lichtstimmung
jetzt nah an den warmen, dunklen Fotos des Originals.

## Timing & Bewegung
Headline-Wörter, Mitteilungen, Zahl und Labels stehen spätestens am Wortanfang (Streifen um 0,32 / 4,99 / 5,87 / 14,0 / 19,26 / 27,61 s, `out/strips_all.jpg`).
Das Original hat 48 % Standbild (UI-Spot); für die 20-%-Grenze bekommt jede UI-Einstellung einen langsamen Push-in (6 %) Richtung Telefon/Zahl → 11 %.

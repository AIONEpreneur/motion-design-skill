# Stilbibel V5 – 19 elegante Typo (Klarsicht Beratung)

Vorbild: Andy Diep, Typo-Intro „made by an agent“, September-Fassung (KpepgP9xhrg), Vollbild-Ausschnitt `ref/ref_crop.mp4`.
Einzelbilder `ref/frames/f_*.png` (16), Übersicht `ref/sheet_all.jpg`. Maßgeblich sind die Bilder ab 17 s (Licht-Fassung).

## Palette (mit PIL gemessen, Bild f_21)
| Rolle | Original | Film |
|---|---|---|
| Grund | #050302 (Ecke), #0A080D (rechts, leicht violett), #090504 (unten) | #060504 + warmer Radialschein zur Mitte + violetter Hauch rechts oben |
| Lichtkegel | Mitte #342927 | zwei klar begrenzte Schächte, additiv, rgba(255,238,210,.13/.095) |
| Lichtlache auf der Linie | #BE9F78 | Radial rgba(230,190,140,.55), flachgedrückt 0,55 |
| Gold hell / dunkel | #F9DFBC / #9D7E5A | Verlauf #F9DFBC → #C9A273 → #8E6F4C + Glanzstelle, wo der Kegel trifft |
| leichte Grotesk | #B8AA9E | #CBBFB2 |
| Horizontlinie | Spitze #605349, Mitte heller, glühend | Verlauf transparent → #6E5A46 → #F0D2A5 → transparent, 1,6 px, Glow 12 |
| Zeitleiste Beschriftung / aktiv | #807871 / #A49281 | #807871 / #D9C3A2 + glühender Punkt |
| Problem-Zustand (eigene Ableitung) | – | kühles Grau #8F969E, kein Licht (wie die unfertigen Monate im Original) |

## Grund und Licht
Fast Schwarz mit warmem Kern, Vignette .55. **Schräger Lichtkegel von rechts oben**, der als Lache auf der Horizontlinie
landet; der Kegel schwingt langsam (±55 px). Staub: 480 feine Punkte (0,8–2,7 px), die im Kegel heller werden, 26 weiche
Bokeh-Kreise. Das Licht geht erst bei „Klarsicht“ an – vorher ist die Bühne unbeleuchtet und kalt.

## Typografie
- **Schlüsselwort**: große Gold-Serife, 190–300 px, steigt **aus der Horizontlinie** (unter der Linie abgeschnitten, wie „ag…“
  im Original), weich von Unschärfe zu scharf. Original = Kursive; hier **aufrecht** (Baskerville, Versalziffern), weil der
  Auftraggeber Kursiv hasst.
- **Kleine Zeile darüber**: leichte Grotesk (Helvetica Neue Light), klein, gesperrt; die Sperrung zieht sich beim Erscheinen
  zusammen („m a d e  b y“ → „made by“).
- **Pfeilsatz** wie „april → september.“: links leichte Grotesk, Pfeil zeichnet sich, rechts Gold-Serife
  („70 Std. → 50 Std.“, „das erste gespräch → kostenlos.“).
- **Zeitleiste** unten mit Punkten und Mono-Versalien, glühender Punkt wandert (W1 … W12).
- Keine Eck-Kicker (das Original hat „SEP 2026 / light“ oben links – bewusst weggelassen), nichts kursiv.

## Bildaufbau, Bewegung
Alles zentriert auf die Horizontlinie (y = 650). Jede Szene fährt stetig heran und steigt leicht (Zoom +8,5 %, −26 px),
Wörter steigen aus der Linie und sinken beim Abgang wieder hinein; die Linie biegt sich unter dem Aufgabenberg durch;
Aufgaben sortieren sich in drei ruhige Spalten, 27 davon sinken weg; drei Gold-Wörter wandern von „sie“ zu „ihr team“.

## Die 5 Merkmale, an denen man den Stil erkennt
1. Fast schwarzer, warmer Grund mit feinem Staub.
2. Schräger Lichtkegel von oben, Lichtlache auf einer dünnen, glühenden Horizontlinie.
3. Ein Schlüsselwort groß in Gold-Serife mit Verlauf und Glanz, das aus der Linie steigt.
4. Darüber eine kleine, gesperrte, leichte Grotesk-Zeile.
5. Zeitleiste mit Punkten unten; Pfeilsatz „vorher → nachher“.

## Stilvergleich-Runden
- **Runde 1** (`out/stilvergleich_1.jpg`): Grund, Gold, Linie, Grotesk stimmen; Didot-Mediävalziffern („7o“, „± o“) wirkten
  falsch, Lichtkegel war ein weicher, breiter Nebel statt zwei klarer Schächte, zu wenig Staub, Zeitleiste ohne Beschriftung.
  → Serife auf Baskerville (Versalziffern), zwei scharf begrenzte Schächte, Staub 260 → 480 und heller, alle Wochen beschriftet,
  Grotesk heller.
- **Runde 2** (`out/stilvergleich_2.jpg`): Schächte jetzt zu hell und bis zum Bildrand gezogen.
  → Deckkraft gesenkt (.2 → .13), Schächte laufen kurz unter der Linie aus.
- **Runde 3** (`out/stilvergleich_3.jpg`, nach der Bewegungs-Korrektur): wirkt wie dieselbe Serie.
  Bewegung: erster Render hatte 63 % Standbild → jede Szene bekam eine eigene stetige Kamerafahrt, Kegel schwingt stärker,
  Staub schneller → 14 %.

## Messwerte (dichte.py, out/film.mp4)
sekunden 29,6 · Schnitte/10 s 0,0 · Bewegung 1,6 · **Standbild 14 %** · Farbigkeit 11,0
Timing-Streifen: `out/strip_{siebzig,kunden,klarsicht,sortiert,uebernimmt,urlaub}.jpg`; Wortzeit-Bogen `out/sheet3.jpg`.

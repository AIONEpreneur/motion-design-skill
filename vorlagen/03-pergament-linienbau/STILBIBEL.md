# Stilbibel V5 – Bauhütte Architekten, im Stil von „Western Civilization in Motion“ (vittorio, X)

Quelle: `ref/original.mp4` (1920×1080, 30 fps), Vollbild-Passage 8–136 s. 17 Einzelbilder `ref/r_*.png`, Ausschnitte `ref/z_boiler.png`, `ref/z_col.png`, Kontaktbogen `ref/kontakt.jpg` (alle 3 s).

## Die 5 Merkmale, an denen man den Stil sofort erkennt
1. **Pergament mit Vignette und starkem Filmkorn:** heller, warmer Kern, dunkelbraune Ränder, flackerndes Korn.
2. **Versal-Antiqua, zweizeilig, links oben:** erste Zeile schwarz und kleiner, Schlüsselwort groß und **rot** mit Punkt („WE INVENTED / DEMOCRACY.“).
3. **Saubere Tusche-Linienarchitektur in Perspektive:** gleichmäßige schwarze Linien 2–3 px, Seitenflächen fein diagonal schraffiert, wenig Fläche, sparsame Farbakzente (Rot, Ocker, Blau).
4. **Dunkle Welt:** Schwarzbraun mit Strahlenkranz aus der Bildmitte, helle bzw. goldene Linien mit Glühen und rot/cyanen Farbsäumen (chromatische Aberration).
5. **Zahl als Pointe:** große, weiß glühende Zahl über der Goldarchitektur, darüber eine laufende Jahresleiste.

## Palette (mit PIL gemessen)
| Rolle | Hex | Quelle |
|---|---|---|
| Pergament Mitte / hell | `#bfab8b` / `#dbc8a9` | r_10, r_42 |
| Pergament Rand | `#877764`–`#736450` | r_10, r_74 |
| Tusche | `#100400`–`#190e08` (Film `#1a0f08`) | r_74, r_10 |
| Rot (Schlüsselwort) | `#982617`–`#b03321` (Film `#a8301d`) | r_10, r_74 |
| Ocker/Gold (Pendel) | `#8e6822` | r_74 |
| Kirchenfenster-Blau | `#2b4665` | r_42 |
| Dunkel Rand / Mitte | `#080910` / `#8c714a` (Glühkern) | r_90, r_35 |
| Goldschrift | `#c2be6f`, Film `#f6e2a4` mit Glühen | r_90 |
Korn: Standardabweichung 5–40 je nach Szene (Kompression), Film: Overlay 30–32 %, 12 Wechsel/s.

## Linien, Flächen, Detail
- Konturen 2,2–3 px schwarz, keine Zitterlinie (technische Zeichnung). Seitenwand und Dachfläche mit 6-px-Diagonalschraffur, Fenster mit Gegenschraffur, Hölzer mit Maserungslinien, Sockel aus einzeln schraffierten Bruchsteinen.
- Flächen nur lasierend (Putz 45 %, Holz 55 % Deckkraft), damit das Pergament durchscheint wie im Original.
- Dunkel: Linien creme (Gefahr) bzw. gold (Rettung), 2,4 px, shadowBlur 12, Farbsäume ±2,2 px in Rot/Cyan.

## Motive (aus der Firmengeschichte, in der Handschrift des Originals)
- Fachwerk-Altbau als echtes 3D-Linienmodell (Kamera-Orbit, Perspektive): Schwelle, Ständer, Riegel, Streben, Rähm, Ortgang, Sockel, Schornstein.
- Fleck mit Wasserrändern, Schimmelpunkte, Schnitt durch die Ausfachung mit Balkenkopf (Jahresringe, Trockenrisse, Nässe), Tropfen.
- Farbroller, Lupe mit Messingring (zeigt das Haus echt vergrößert), rote Maßketten mit Pfeilspitzen und Zentimeter-Lineal, Zirkelbogen, Plan-Farben (Ocker = bleibt, Rot schraffiert gestrichelt = wird ersetzt), Kelle, Kalkeimer, Holznägel.
- Gold-Schluss: glühendes Haus, Regen perlt an einem Schutzbogen ab, Jahresleiste 2026 → 2126, Zahl „100“ zählt hoch.

## Typografie
- Cinzel 800, Versalien, Laufweite 6 % der Größe; Zeile 1 70 px schwarz, Schlüsselzeile 104–124 px rot; x = 130, y = 190 / 320 / 440.
- Wort für Wort: Einblenden + 16 px Anheben in 0,28 s, fertig spätestens am Wortanfang.
- Maßzahlen und Legende in IBM Plex Mono (funktional, keine Ecktexte). Weggelassen: HUD-Ecken, „ANNO“, Kardaschew-Wert, Kapitelzeilen, Unterzeilen.

## Bildaufbau, Kamera, Übergänge
- Schlagzeile links oben, Architektur rechts; ständiger langsamer Push-in (Distanz −8 %), Orbit in den Dunkel-Szenen.
- Harte Schnitte zwischen Pergament und Dunkel; Hineinfahren in den Fleck als Übergang zum Schnitt.

## Stilvergleich
**Runde 1** (`out/stilvergleich_1.jpg`): Aufbau, Schrift und Dunkelwelt treffen das Original. Abweichungen: unser Pergament grauer und fleckiger; Haus wirkte wie flächig ausgemalte Illustration statt Linienzeichnung (deckendes Holz/Putz/Fenstergrau); Schlüsselworte kleiner als im Original; Haus zu frontal.
**Geändert:** Pergament wärmer/heller, Mottling halbiert, Vignette schwächer; Füllungen lasierend, Fenster nur schraffiert; Schlüsselzeile 104 → 124 px; Kamera-Yaw −0,36 → −0,5; Bogen über dem Dach blendet vor der Jahresleiste aus; Schluss-Haus ohne Fensterlicht hinter der Schrift.
**Runde 2** (`out/stilvergleich_2.jpg`): Serie erkennbar. Geändert: größere Titel stießen an Haus/Wand → Architektur weiter nach rechts; Schluss-Szene mit aufsteigender Glut und Orbit (Standbild-Anteil 13 % → 2 %).
**Runde 3** (`out/stilvergleich_3.jpg`): Endstand.

## Messwerte (dichte.py)
| | Original (8–136 s) | V5 |
|---|---|---|
| Standbild-Anteil | 1 % | 2 % |
| Bewegung | 17,6 | 5,1 |
| Schnitte je 10 s | 3,4 | 1,4 |
| Farbigkeit | 25,4 | 22,9 |
Timing: `out/timing_alle.jpg` (10 Schlüsselwörter, Streifen je −0,3 bis +0,05 s) – jedes Wort steht zur Wortzeit.

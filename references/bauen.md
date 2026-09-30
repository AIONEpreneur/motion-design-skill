# Bauen, prüfen, ausliefern

Pfade:
- Werkzeuge: `W="$SKILL/werkzeuge"` (`$SKILL` = der Ordner dieses Skills, siehe „Base directory“ beim Laden). Dort liegen render.mjs (mit node_modules), vo_kie.py, wortzeiten.py, pegel.py, mix.sh, textbogen.py und dichte.py.
- Projekte: `./erklaervideos/<kunden-slug>/` im aktuellen Arbeitsordner, angelegt mit `scripts/neues_projekt.py`.
- Python mit soundfile: `~/.local/share/voice-tts/.venv-mlx/bin/python` oder `uv run --with soundfile`.
- kie.ai-Schlüssel: wird aus der Umgebungsvariable `KIE_API_KEY` oder aus `~/.claude/settings.json` (`env.KIE_API_KEY`) gelesen. Fehlt er, den Nutzer einmal danach fragen, erklären, wo er ihn bekommt (kie.ai → API Keys) und ihn mit seinem Einverständnis in `~/.claude/settings.json` unter `env` eintragen.

Alle Befehle laufen im Projektordner.

## 1 · Stimme
1. Den freigegebenen Sprechertext nach `skript.txt` schreiben, eine Zeile pro Bild-Beat.
2. `python3 "$W/vo_kie.py" skript.txt --stimme <gewählte Stimme> --out out --szene "<Regieanweisung aus der Hörprobe>"`
   Ergebnis: `out/vo.wav` und `out/vo.json`. Das Tempo nie ändern.
3. Die Aufnahme anhören, also transkribieren lassen: Stimmt jedes Wort, stimmt die Betonung? Wenn nicht, neu erzeugen.

## 2 · Wortzeiten (Pflicht)
1. `python3 "$W/wortzeiten.py" out/vo.wav out/vo.json`
2. Jedes Schlüsselwort, auf das ein Bild, ein Wort oder ein Effekt fällt, an der Pegelkurve prüfen:
   `python3 "$W/pegel.py" out/vo.wav <von> <bis>`
   - Der Wortanfang ist der Sprung auf Sprachpegel, 25–40 dB über Grund.
   - Einatmer liegen nur 10–15 dB über Grund und sind kein Wortanfang.
   - Abweichungen in `out/vo.json` korrigieren.
3. `zeiten.py` an den neuen Text anpassen: Es leitet `K`, die Bildzeitpunkte je Schlüsselwort, und `CUT` ab und schreibt `film/zeiten.js` und `out/zeiten.json`. Dann ausführen.

## 3 · Regie
`REGIE.md` mit einer Tabelle Beat für Beat:

| Beat | Bild | Hervorhebung | Wort am Objekt | fertig bei (K) | Warum |

- Stummtest: Aus Bild, Hervorhebungen und Wörtern allein versteht man Problem, Einsatz, Wendung, Lösung, Ergebnis und Angebot.
- Schlusskarte: Logo und Name, das Angebot in höchstens 3 Wörtern und der Kontakt.

## 4 · Bilder
- Vertrag der Seite `film/index.html`: `window.FILM = { duration, ready, seek(t) }`. `seek(t)` zeichnet exakt das Bild zur Zeit t.
  Kein Math.random, kein Date, keine laufenden Animationen. Zufall nur mit festem Seed.
- Stil nach `STIL.md`: Look, Palette-Logik, Linien, Figuren, Typo, Kamera, Übergänge. Die Farben passt du an Branche und Marke an.
- Die Vorlage in `film/` liefert Hilfsfunktionen und Technik. Szenen und Figuren baust du für die neue Geschichte neu.
- Jede Einblendung startet 0,2–0,4 s vor ihrem K und ist bei K fertig. Keine festen Sekundenwerte.
- Zwischendurch Standbilder rendern und ansehen:
  `node "$W/render.mjs" film/index.html --stills=<t1>,<t2>,… --out=out/stills`

## 5 · Ton
- `ton/partitur.py` für diese Geschichte neu schreiben: eigene Musik (Tonart, Instrumente, Wendepunkt auf dem Wendewort) und Geräusche nur dort, wo im Bild etwas passiert. Alle Zeiten kommen aus `out/zeiten.json`.
  Ausgabe: `out/musik.wav` und `out/sfx.wav`.
- Mischen: `bash "$W/mix.sh" out/vo.wav out/musik.wav out/sfx.wav` ergibt `out/mix.wav` mit −14 LUFS. Die Musik wird unter der Stimme abgesenkt.

## 6 · Rendern
`node "$W/render.mjs" film/index.html --ohne-untertitel --out=out/film.mp4 --audio=out/mix.wav --workers=3`

## 7 · Selbst prüfen, bevor der Nutzer etwas sieht
1. `python3 "$W/textbogen.py" out/film.mp4 out/vo.json out/textbogen`: alle 0,5 s ein Bild mit dem gesprochenen Wort darunter. **Alle Bögen ansehen.**
   - Sitzt jedes Bild auf seinem Wort?
   - Gibt es Sätze im Bild oder Getipptes?
   - Ist der Kontrast überall lesbar?
   - Verdeckt etwas die Hauptaktion?
2. Ein Standbild an jedem Schlüsselwort ansehen, bei K + 0,05 s.
3. `python3 "$W/dichte.py" out/film.mp4`: Der Standbild-Anteil liegt bei höchstens 20 %.
4. Stummtest: Nach 2 Sekunden ist klar, worum es geht.
5. Fehler beheben und neu rendern. Mindestens eine Korrekturrunde.

## 8 · Ausliefern
1. `ffmpeg -i out/film.mp4 -c:v libx264 -preset slow -b:v 3.2M -maxrate 4.5M -bufsize 7M -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 160k out/<slug>_web.mp4`
   Die Datei muss unter 14 MB bleiben.
2. Auf einer Artifact-Seite abspielbar veröffentlichen (`zeigen.md`) und den Link geben.
3. Knapp melden:
   - der Link
   - was ehrlich noch schwach ist

---
name: erklaervideo
description: |
  Baut ein 30-Sekunden-Erklärvideo (16:9) für ein Produkt oder eine Dienstleistung. Der Ablauf ist fest:
  Interview mit dem Nutzer, 3 Stilvorschläge aus einer Bibliothek mit 22 erprobten Stilen, Sprechertext
  und Ablauf zur Freigabe, 3 Hörproben über kie.ai, danach bauen, selbst prüfen und das fertige Video als
  abspielbare Seite ausliefern.
  Auslöser: "Erklärvideo", "Erklärfilm", "Werbevideo für meine Firma", "Video für mein Produkt",
  "Video für meine Dienstleistung", "/erklaervideo".
---

> **Pfade:** `$SKILL` ist der Ordner dieses Skills (steht beim Laden als „Base directory“). Werkzeuge: `$SKILL/werkzeuge`, Stilvorlagen: `$SKILL/vorlagen`, Beispielvideos: `$SKILL/beispiele`. Kundenprojekte entstehen in `./erklaervideos/` im aktuellen Arbeitsordner.
> **Vor dem ersten Video** einmal `python3 "$SKILL/werkzeuge/pruefen.py"` ausführen. Es meldet, was noch fehlt (Node-Pakete, ffmpeg, whisper.cpp mit Modell, Python-Pakete, Chrome, kie.ai-Schlüssel) und wie man es installiert.

# Erklärvideo

Der Nutzer liefert nur den Auftrag. Du schlägst vor, er wählt aus und gibt frei, du baust.
Nie so tun, als gäbe der Nutzer Stil, Text oder Stimme vor: Das erarbeitest du und legst es zur Wahl vor.

Der Ablauf hat fünf Schritte. Erst ganz am Ende wird gebaut.

## 1 · Interview: Produkt oder Dienstleistung verstehen

Es geht zuerst um das Produkt, nicht um den Stil. Stell die vier Fragen **einzeln**, jede in einer eigenen Nachricht, und warte jeweils auf die Antwort:

1. „Erzähl mir von deinem Angebot: Was verkaufst du genau, und was machst du anders als die Konkurrenz?“
2. „Wer ist dein Kunde?“
3. „Welches Problem hat dein Kunde, bevor er zu dir kommt?“
4. „Was soll der Zuschauer am Ende tun, und wo läuft das Video?“ Dazu gehört der Kontakt: Website, Telefon.

Bleibt eine Antwort vage, frag einmal gezielt nach, zum Beispiel nach einer Zahl, einem konkreten Moment oder dem Unterschied zur Konkurrenz. Danach fasst du alles in einer **Briefing-Karte** zusammen: Firma, Leistung, Unterschied, Zielgruppe, Problem, Angebot, Kontakt, Einsatz. Zeig sie dem Nutzer und lass sie bestätigen. Einzelheiten stehen in `references/interview.md`.

## 2 · Drei Stile vorschlagen

1. Lies `references/stile/katalog.md`. Wähle 3 Stile, die zu Produkt, Zielgruppe und Tonfall passen. Nimm drei **verschiedene Arten**, etwa 2D-Illustration, 3D und Typografie, nicht dreimal fast dasselbe.
2. Begründe jeden Vorschlag in einem Satz mit Bezug aufs Briefing, zum Beispiel: „Die Prüfung als Boss-Kampf spricht junge Leute direkt an.“
3. Zeig die drei Beispielvideos **abspielbar** auf einer Artifact-Seite, siehe `references/zeigen.md`. Gib den Link.
4. Lass wählen, am besten per Auswahlfrage mit den drei Stilen als Optionen.

## 3 · Text und Ablauf zur Freigabe

1. Lies `references/stile/<nr>.md` für den gewählten Stil und `references/regeln.md`.
2. Schreib den **Sprechertext**: 70–80 Wörter für rund 30 Sekunden, Ansprache mit „Sie“.
   - Aufbau: Problem des Kunden → was auf dem Spiel steht → Wendung → Lösung → Ergebnis → Angebot.
   - Im Mittelpunkt steht der Kunde, nicht die Firma.
3. Schreib den **Ablauf** in 6–8 Szenen, jede in einem Satz: Was ist in diesem Stil zu sehen?
4. Zeig beides im Chat. Ändere den Text, bis der Nutzer ihn freigibt. Erst dann geht es weiter.

## 4 · Drei Hörproben

1. Nimm die ersten ein bis zwei Sätze des freigegebenen Texts. Schreib eine Regieanweisung: Tonfall am Anfang, ab der Wendung und am Ende, dazu die Wörter, die betont werden sollen.
2. Erzeuge die Proben:
   `python3 ~/.claude/skills/erklaervideo/scripts/stimmproben.py --text "…" --szene "…" --out <projekt>/proben`
   - Stimmen: Charon (männlich, sachlich), Sulafat (weiblich, warm), Achird (männlich, freundlich).
   - Kosten: unter 3 Credits.
3. Zeig die drei Proben abspielbar auf einer Artifact-Seite (`references/zeigen.md`) und lass wählen.

## 5 · Bauen, selbst prüfen, ausliefern

Folge `references/bauen.md` Schritt für Schritt. Kurz:

1. **Projekt anlegen:** `python3 ~/.claude/skills/erklaervideo/scripts/neues_projekt.py <stil-nr> <kunden-slug>`. Die Vorlage des Stils ist nur der technische Startpunkt, die Geschichte baust du neu.
2. **Stimme:** komplette Aufnahme mit der gewählten Stimme, dann die Wortzeiten messen und die Schlüsselwörter an der Pegelkurve nachprüfen.
3. **Regie:** Tabelle Beat für Beat mit Bild, Hervorhebung, Wort am Objekt und Zeitpunkt. Alle Zeiten kommen aus den gemessenen Wortzeiten.
4. **Bilder und Ton bauen:** Film-Code im gewählten Stil, eigene Musik und Geräusche auf die Wörter gelegt.
5. **Rendern und selbst prüfen:** Textbogen und Standbilder an jedem Schlüsselwort ansehen und korrigieren. Mindestens eine Korrekturrunde, bevor der Nutzer etwas sieht.
6. **Ausliefern:** Web-Fassung unter 14 MB auf einer Artifact-Seite, abspielbar, mit Link.

Halte den Nutzer knapp auf dem Laufenden. Jede Meldung hat einen klickbaren Link, Videos und Audio immer abspielbar auf einer Seite.

## Harte Regeln

Die Begründungen stehen in `references/regeln.md`.

- Keine Untertitel.
- Keine Sätze im Bild, nur einzelne Wörter oder Zahlen am Objekt.
- Betont wird mit Lupe, Kreis, Pfeil, Farbe, Durchstreichen, Häkchen oder Zoom.
- Jedes Bild ist spätestens am Wortanfang fertig.
- Stimme nie im Tempo strecken oder stauchen.
- Aus dem Stil die Prinzipien übernehmen, keine Deko-Texte in Ecken und keine kursiven Kicker.
- Farben aus Branche und Marke des Kunden, nicht aus dem Beispielvideo.
- Das Video muss stumm verständlich sein: Nach 2 Sekunden ist klar, worum es geht.

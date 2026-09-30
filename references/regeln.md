# Regeln und warum sie gelten

Alle Regeln stammen aus Korrekturen des Auftraggebers an 22 Erklärvideos (September 2026).

## Text im Bild
- **Keine Sätze und keine Satzstücke im Bild.** Erlaubt sind ein Wort, eine Zahl mit Einheit oder ein Name. Der Text steht **am Objekt**, zum Beispiel als Etikett, Beschriftung, Maß oder Zahl am Zifferblatt.
  Warum: Mitgetippte Sätze fand der Auftraggeber „sehr verwirrend, nicht synchron, nervig“. Hören und Mitlesen desselben Satzes verschlechtert das Verstehen (Mayer: Redundanz).
- **Betonung über Bildmittel,** nicht über Text: Lupe, Kreis, Pfeil, Aufleuchten, Farbwechsel, Durchstreichen, Häkchen, Zoom.
  Warum: „Wenn du etwas deutlich machen willst, dann mit einer Lupe oder irgendwas.“
- **Weder zu viel noch zu wenig.** Ein Video ganz ohne Worte war ebenso falsch („Du kennst nur Schwarz und Weiß“). Entscheide Beat für Beat:
  - Das Bild ist eindeutig: kein Text.
  - Das Bild ist mehrdeutig (Ursache, Dauer, Zahl, Fachbegriff): ein Wort oder eine Zahl am Objekt.
- **Typografie-Stile** (19, 22, teilweise 07, 09, 12): Kurze Headlines dürfen bleiben, wenn der Stil davon lebt. Dann aber in exakt den gesprochenen Wörtern, als Ganzes eingeblendet, nie getippt.
- **Keine Untertitel,** auch keine eingebrannten Wort-für-Wort-Kästen.
- **Keine Deko-Texte:** nichts in den Ecken, keine Timecodes, keine Mono-Kicker, keine Kapitelzeilen, keine kursiven Einleitungszeilen.

## Timing
- Jedes Bild, jede Hervorhebung und jedes Wort ist **spätestens am Wortanfang fertig** und startet 0,2–0,4 s vorher. Kritik dazu: „Bilder kommen zu spät.“
- Die Zeiten aus der Sprachsynthese lagen bis zu 1,2 s daneben. Deshalb gilt:
  - Die Wortzeiten immer neu messen mit `wortzeiten.py`.
  - Jedes Schlüsselwort an der Pegelkurve nachprüfen mit `pegel.py`.
  - Im Film keine festen Sekundenwerte, alle Zeiten kommen aus K.

## Geschichte
- Im Mittelpunkt steht der **Kunde des Kunden**, nicht die Firma. Kritik dazu: „Wen juckt der Anwalt? Es geht doch immer um den Kunden.“
- Aufbau: Problem als konkreter Moment → was auf dem Spiel steht → Wendung → Lösung → Rückkehr in den Alltag → Angebot.
- Nach 2 Sekunden muss klar sein, worum es geht und für wen. Wird das Video wie eine Facebook-Werbung beurteilt, muss es auch stumm verständlich sein.

## Stil
- Vom Stil übernimmst du **Look und Prinzipien**: Palette-Logik, Papier, Linien, Detailgrad, Bewegung. Vor allem aber den Hintergedanken der Bewegungen:
  - Zoom bedeutet genauer hinsehen.
  - Split bedeutet „nicht X, sondern Y“.
  - Verwandlung ersetzt den Schnitt.
  - Ein Lichtkegel bedeutet Fokus.
- Nie kopieren: Format, Deko und Themen des Beispiels übernimmst du nicht. Es bleibt immer 16:9 und farbig.
- Farben leitest du aus Branche und Marke des Kunden ab. Beim Blitzer-Thema also Verkehrsfarben, nicht Beige.

## Stimme und Ton
- kie.ai, Modell `google/gemini-2-5-pro-tts`. Stimmen: Charon, Sulafat, Achird. Welche passt, entscheidet der Nutzer per Hörprobe.
- **Nie im Tempo strecken oder stauchen** (kein atempo): Das verschluckt Silben.
- Musik und Geräusche komponierst du **für jedes Video neu**, passend zu seinen Wörtern. Keine gemeinsamen Presets über mehrere Videos.

## Ausliefern
- Jedes Ergebnis bekommt einen klickbaren Link.
- Audio und Video immer abspielbar auf einer Artifact-Seite, nie als Datei zum Herunterladen.

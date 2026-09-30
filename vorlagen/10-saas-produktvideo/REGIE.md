# REGIE V7 – 10 Domus Hausverwaltung (Shotbase-Produktvideo)

## 1. Wie geht das Original mit Text um?
Original: Shotbase-Launchvideo (`ref/dicht.jpg`, 82 Bilder im 0,5-s-Raster). Befund:
- **Teilweise Typografie-Original.** Es gibt genau 5 kleine Headlines in 45 s („You record your screen“, „or you just paste“,
  „no digging through folders“, „Drop in a background“, „Share you're done“), jede 2–4 Wörter, klein (≈ 5 % Bildhöhe).
- **Rund die Hälfte der Einstellungen hat gar keine Headline** (Tasten-Intro, Toolfolio-Website, Ordner, Wald-Desktop,
  Zeitleiste). Dort sprechen nur die UI und ihre Beschriftungen: Tastenlabel („command“), Icon-Labels, Kartentitel,
  die rote Freihand-Annotation mit Label **„blur this“**.
- Einzige große Typo ist die **Schlusszeile** („Share you're done“, Tauschwort Navy, letztes Wort Blau).

Folge für Domus:
- V5 hat jeden gesprochenen Satz als Headline mitgebaut (9 Headlines, bis 6 Wörter) – das Original tut das nicht.
- V7: **Nur dort eine Headline, wo das Original eine hätte und das Bild allein mehrdeutig wäre** – die Dauer „30 Minuten“
  (eine Zahl ist aus dem Bild nicht ablesbar) und die Schlusszeile. Alles andere trägt die UI selbst:
  Beschriftungen am Objekt (Label, Chip, Knopf, Badge, Balken) mit genau dem gesprochenen Wort, sonst Bildmittel
  (Klick, Aufleuchten, roter Ring, Durchstreichen, Häkchen, Pixel-Auflösung, Zoom).
- Nichts wird getippt. Headlines erscheinen als Ganzes mit der Stil-Geste (Blur-in), fertig auf dem Wort.
- Satzhafte Nebentexte in der UI (Nachrichtenvorschauen, „Zusammenfassung“-Sätze, Mitteilungstexte, Statuszeilen wie
  „3 Anrufe · keine Antwort“) werden entfernt oder auf ein Wort gekürzt – sonst liest man Sätze, während die Stimme spricht.

## 2. Beat für Beat
Zeiten = Wortanfang aus `out/vo.json` (neu vermessen, Schlüsselwörter an der Pegelkurve geprüft). Jede Hervorhebung
startet 0,2–0,3 s vorher und ist auf dem Wort fertig.

| Beat | Hervorhebung (Bild) | Text am Objekt | fertig bei Wort (Zeit) | Warum |
|---|---|---|---|---|
| Sonntagabend | Tasten-Widgets fallen ein, das Datum-Widget leuchtet auf | **SONNTAG 14** und **21:47** im Widget (vorhanden) | „Sonntagabend“ 0,32 | Wochentag + Uhrzeit sagen „Sonntagabend“ genauer als eine Headline; V5-Headline „Sonntagabend.“ war doppelt → weg. |
| Mieter schreibt | Nachrichten-Taste wird gedrückt und glüht, Mitteilung springt heraus, Tipp-Punkte | Absender **Mieter · Whg. 3** (Name) | „schreibt“ 2,18 | Wer schreibt, ist ein Name → am Objekt. Der Nachrichtentext wird **nicht** getippt. |
| Wasser in der Küche | Foto der nassen Küche löst sich aus Pixeln in der Mitteilung auf (fertig auf „Wasser“), dann zeichnet sich ein roter Freihand-Ring um das Foto (fertig auf „Küche“) | – | „Wasser“ 2,77 / „Küche“ 3,49 | Das Foto zeigt Wasser und Küche eindeutig; der getippte Satz „Wasser in der Küche!“ war genau die Redundanz. |
| Sie rufen Handwerker an | Anruf-Leiste wächst, Zeiger klickt nacheinander drei Kontakte, Klingel-Ring | Namen **Sanitär Keller**, **Rohr-Notdienst**, **Hausmeister** (Namen, vorhanden); Knopf **Anrufen** | „Handwerker“ 4,69 (1. Anruf) | Die Namen sagen „Handwerker“. Statuszeile („klingelt …“) weg, stattdessen Klingel-Ring am Kontakt. |
| Niemand geht ran | Jeder Kontakt bekommt ein rotes ✕, dann zieht sich ein **roter Ring** um alle drei | – | „Niemand“ 5,91 | Drei rote ✕ sind eindeutig. V5-Headline und „3 Anrufe · keine Antwort“ weg. |
| Dazu zwanzig Nachrichten | Kartenstapel wächst, roter Zähler zählt hoch | Zähler **20** am Stapel | „zwanzig“ 7,52 | Zahl am Objekt. Vorschautexte der Karten → graue Zeilen, nur Absendernamen bleiben. |
| … und Belege | Belege fliegen von den Seiten an den Stapel | Titel/Beträge auf den Belegen (vorhanden, klein) | „Belege“ 8,84 | Kassenzettel sind als Beleg eindeutig. |
| Ihr Wochenende? | Kalender, Spalten **Sa/So** werden blau hinterlegt, dann stürzen Termine hinein | Kalendereinträge als Einzelwörter (**Wasserschaden**, **Rückruf**, **Belege** …) | „Wochenende“ 9,75 | Hervorhebung durch Farbfläche statt Headline „Ihr Wochenende?“. Einträge auf ein Wort gekürzt. |
| Weg. | Zwei rote Freihand-Striche durch Sa + So, Annotation-Label springt auf | Label **Weg** (wie „blur this“ im Original) | „Weg“ 10,57 | Die Annotation ist ein Originalmotiv und trägt exakt das gesprochene Wort. |
| Mit Domus läuft das anders | Pixel-Blende auf Blau-Wallpaper, Pille wächst zur Domus-Leiste, Icons poppen | Logo-Chip zeigt **Domus** | „Domus“ 11,78 | Name am Objekt (Chip) statt Satz-Headline. |
| Ihr Mieter meldet den Schaden | Zeiger klickt „Melden“, Knopf wird cyan; im Feld springt ein Schaden-Chip auf (als Ganzes) | Chip **⚠ Wasserschaden** | „Schaden“ 14,07 | Ein Wort am Objekt. V5 tippte „Wasserschaden Küche“ → nicht mehr getippt. |
| … im Portal | Logo-Chip wächst | **Mieterportal** im Chip | „Portal“ 14,58 | Fachbegriff → ein Wort am Objekt. |
| … mit Foto | Zeiger klickt Kamera, Blitz, Foto löst sich aus Pixeln im Popover | Icon-Label **Foto** (vorhanden) | „Foto“ 15,40 | Bild eindeutig. |
| In dreißig Minuten | Lichtblitz + Rausfahren: Meldung wird Karte in der Galerie; rechts daneben die Headline | Headline **30 Minuten** (Stil-Headline, „Minuten“ blau) | „dreißig“ 16,42 | Eine Dauer ist aus dem Bild nicht ablesbar → Zahl mit Einheit. Headline, weil das Original an genau dieser Stelle (Karte + Text rechts) eine setzt. „✦ Zusammenfassung“ mit Sätzen weg. |
| … ist der Notdienst beauftragt | Handwerker-Karte blurrt ein, Zeiger klickt den Knopf, Knopf wird blau mit Häkchen | **Rohr-Notdienst Weber** (Name), Knopf **Beauftragen → ✓ Beauftragt** | „Notdienst“ 17,48 / „beauftragt“ 18,09 | Das Wort steht auf dem Knopf, der geklickt wird. „12 Min. entfernt“ entfernt (widersprach „30 Minuten“). |
| Sie sehen alles live | Live-Ansicht der Küche mit Verlaufsrahmen, Live-Badge springt auf, roter Punkt pulsiert | Badge **Live** | „live“ 19,87 | UI-Badge mit exakt dem Wort; V5-Headline „Sie sehen alles live.“ weg. |
| gemeldet, beauftragt, erledigt | Drei Zeitleistenbalken wachsen nacheinander, Abspielkopf läuft; bei „erledigt“ wischt die Küche trocken, grünes Häkchen | Balken **Gemeldet**, **Beauftragt**, **Erledigt** | 20,46 / 21,09 / 21,83 | Jedes Wort sitzt auf seinem Balken und ist auf dem Wort fertig. Status-Chip auf dem Foto (doppelt) weg. |
| Und Sie bleiben am Esstisch sitzen | Kreis-Pixelblende auf das Esstisch-Foto, Kamera fährt langsam auf den Tisch, Mitteilung mit grünem Häkchen | Mitteilung **Domus** / **Erledigt** | „Esstisch“ 23,52 | Das Foto ist eindeutig. V5-Headline und Mitteilungssatz („Rechnung und Fotos liegen bereit.“) weg. |
| Domus Hausverwaltung | Foto schrumpft zur Karte, Logo blurrt ein | **Domus** + **Hausverwaltung** | „Domus“ 24,68 | Name. |
| Der erste Monat ist kostenlos | Schlusszeile im Originalmuster („Share you're done“): erster Teil Navy, letztes Wort Blau, Zeiger klickt | **1. Monat** (Navy) · **kostenlos** (Blau); Kontakt | „Monat“ 26,57 / „kostenlos“ 27,12 | Höchstens 2 Wörter Angebot; jeder Teil als Ganzes auf seinem Wort. Knopf „Monat 1 gratis“ auf der Karte (doppelt) weg. |

## 3. Stummtest
Problem: Sonntag 21:47, Mieter schickt Foto einer nassen Küche. Ursache/Stress: drei Anrufe mit ✕, 20 Nachrichten,
Belege, Wochenende rot durchgestrichen „Weg“. Lösung: Domus-Leiste → Wasserschaden + Mieterportal + Foto → 30 Minuten →
Notdienst ✓ Beauftragt → Live: Gemeldet · Beauftragt · Erledigt. Ergebnis: Esstisch, Mitteilung „Erledigt“.
Angebot: Domus Hausverwaltung, 1. Monat kostenlos, Kontakt.

## 4. Schlusskarte
Logo + **Domus** / **Hausverwaltung**, Angebot **1. Monat kostenlos** (Angebotswort „kostenlos“ auf 27,12), Kontakt
`domus-verwaltung.de · 0221 987 654 0`.

## 5. Ton
Stimme und Musik unverändert (V5). Effekte auf die neuen K gelegt. Tastatur-Tippgeräusche entfernt (es wird nichts mehr
getippt); Anruf-Klicks, Freizeichen und „keine Antwort“ folgen den neuen Anrufzeiten.

# 18 · Riegel 24 Schlüsseldienst – Regie V7 (Text und Timing)

## Wie nutzt das Original Text?
Bild-Original („The Falling Dream“, invertierter Holzschnitt). Der einzige Text ist ein **kleiner weißer Zettel oben links**,
der Buchstabe für Buchstabe getippt wird: Stimmungsfetzen wie „almost asleep.“, „falling.“, „faster.“.
Dazu Zahlen, die **Teil des Bildes** sind: die 7-Segment-Uhr „3:07“.

**Entscheidung zum Zettel oben links: weg.** Begründung:
- Er ist frei schwebend, getippt und immer ein Satzfetzen („Tür zu. Schlüssel drinnen.“, „Festpreis am Telefon.“) –
  genau das, was der Auftraggeber zweimal verworfen hat.
- Im Original trägt er keine Information, nur Stimmung. Bei uns hat er nur wiederholt, was die Stimme sagt (Redundanz).
- Alles, was er sagte, zeigt das Bild bereits: Tür knallt, Schlüssel im Schlüsselloch-Einsatz, Uhr 23:51, Akku 1 %.
Die **Optik** des Zettels (weißer Papierstreifen, runde Comic-Schrift) lebt einmal weiter – aber als **Etikett am Objekt**
mit Führungslinie („Folie“), als Ganzes aufgeklatscht. Zahlen bleiben wie im Original im Bild (Uhr, Akku, Preisschilder, 20 MIN, Nummer).

## Wortzeiten
`wortzeiten.py`, danach an der Pegelkurve geprüft (in `out/vo.json` mit `"geprueft": "pegel"`):
zu 0,47 → **0,57** · schlüssel 1,29 → **1,17** (sch ab 1,175) · mitternacht 2,81 → 2,90 · akku 3,64 → 3,60 · fünfzig 8,87 → 8,80 · hundert 9,87 → 9,82 ·
oder 10,40 → 10,35 · **dreihundert 11,10 → 10,58** (Werkzeug lag 0,5 s daneben; d-Verschluss 10,55) · Riegel 12,12 → **12,01** ·
vierundzwanzig 12,43 → **12,32** (f-Zischen) · festpreis 13,48 → **13,40** · sofort 14,09 → **13,97** · zwanzig 16,04 → **16,19** ·
minuten 16,23 → **16,58** · folie 19,20 → **19,07** · sind 23,24 → 23,32 · drin 23,42 → 23,57 · vierundzwanzig (Schluss) 25,20 → **24,90** ·
und 26,15 → 26,06 · nacht 26,20 → 26,15 · speichern 27,04 → 26,94 · nummer 27,55 → 27,62 (Nasal, geschätzt aus Silbenlage) · brauchen 28,39 → **28,61** (b-Verschluss 28,60).
Bestätigt: tür 0,33 · kurz 2,55 · leer 4,27 · preis 7,94 · Bei (Zeile) 11,80 · da 17,62 · er öffnet 18,30 · ohne 19,94 · bohren 20,25 · klick 21,12 · heil 22,42 · Riegel (Schluss) 24,45 · tag 25,94.
`mitternacht` kommt jetzt aus dem Wort, nicht mehr aus Zeile + 0,3 s. Alle ~45 festen Sekundenwerte im Film sind aus K abgeleitet.

## Beat für Beat
| Beat | Hervorhebung (Bild) | Text am Objekt | fertig bei Wort (Zeit) | Warum |
|---|---|---|---|---|
| Tür zu | Tür schlägt zu, Knall-Strahlen | – | zu 0,57 | Bild eindeutig. |
| Schlüssel drinnen | **Lupen-Einsatz** (Kreis mit Führungslinie vom Schlüsselloch), Schlüssel hängt drinnen und pendelt | – | schlüssel 1,17 | Klassische Lupe: zeigt, was hinter der Tür ist. |
| Kurz vor Mitternacht | 7-Segment-Uhr wie „3:07“ im Original | **23:51** (in der Uhr) | mitternacht 2,90 (Uhr ab kurz) | Uhrzeit = Zahl im Objekt, Stilmerkmal des Originals. |
| Akku fast leer | Handy fährt ins Bild, roter Akku-Balken schrumpft und blinkt, Licht geht aus | **1 %** (rot, am Handy) | leer 4,27 | Zahl mit Einheit am Gerät. |
| Sie suchen einen Notdienst | Handy groß, Suchfeld | **Schlüsselnotdienst** (im Suchfeld, als Ganzes) | notdienst 6,10 | Ein Wort, dort wo es in echt steht; **nicht getippt**, Tastatur ohne Anschläge. |
| jeder nennt einen anderen Preis | Drei Treffer (Namen nur als Balken), rote Preisschilder | **49 €?** · **?? €** · **9 €*** | jeder 6,67 · anderen 7,57 | Die widersprüchlichen Zahlen sind die Aussage; die Firmennamen aus V5 waren Satzstücke. |
| Fünfzig Euro? Hundert? Dreihundert? | Boden bricht, Sturz durch den Flur; Preisschilder fliegen auf die Kamera zu | **50 €?** · **100 €?** · **300 €?** (rot) | 50 8,80 · 100 9,82 · 300 10,58 | Jede Zahl auf ihrem Wort; das Fragezeichen ist das Gefühl. |
| Bei Riegel 24 … | Sternburst öffnet den Anruf-Bildschirm | **Riegel 24** (Anrufername) · **00:01** Zähler | Bei 11,80 | Name am Gerät. „verbunden“ aus V5 entfällt – der laufende Zähler zeigt es. |
| … den Festpreis sofort am Telefon | Preis-Karte knallt als Stempel, Schallbögen am Handy | **FESTPREIS 129 €** (auf der Karte) | festpreis 13,40 · Bögen sofort 13,97 | Antwort auf die drei „?“: ein Wort + eine Zahl auf einem Objekt. 129 € ist nicht gesprochen, macht „fest“ aber sichtbar (Gegenbild zu 50/100/300 €?). |
| In zwanzig Minuten ist der Techniker da | Licht an, Techniker mit Kappe und Koffer läuft ins Treppenhaus, Uhr springt 23:54 → 00:14 | **20 MIN** (7-Segment-Kasten) | in 16,04 (Kasten), zwanzig 16,19 · Ankunft da 17,62 | Dauer = Zahl mit Einheit; die mitlaufende Uhr belegt es. |
| Er öffnet mit einer Folie | Schnitt durchs Schloss, dünne helle Folie schiebt sich in den Spalt | **Folie** (weißer Zettel mit Führungslinie zur Folie) | folie 19,07 | Ein heller Streifen ist ohne Wort nicht als Folie lesbar – Fachbegriff, einziger Zettel im Film. |
| ganz ohne Bohren | Bohrmaschine, **rotes X** zeichnet sich in zwei Strichen | – | ohne 19,94 · bohren 20,25 | Durchstreichen statt Wort. |
| Klick | Falle springt zurück, Klick-Strahlen | – | klick 21,12 | Bild + Ton. |
| Das Schloss bleibt heil | Tür schwingt auf, Lichtfläche; **Lupen-Einsatz** Schlüsselloch mit Häkchen | – | heil 22,42 | Häkchen = heil. |
| Sie sind drin | Figur geht ins Licht | – | sind 23,32 | Bild eindeutig. |
| Riegel 24 | Schlüssel-Logo pendelt, **RIEGEL** geschnitzt, **24** rot | **RIEGEL** · **24** | Riegel 24,45 · 24 24,90 | Name. |
| Tag und Nacht | **Sonne** und **Mond** als Holzschnitt | – | tag 25,94 · nacht 26,15 | Die Wörter „Tag & Nacht“ aus V5 wiederholten nur die Bilder → weg. |
| Speichern Sie die Nummer | Nummer in der 7-Segment-Anzeige, kleines Schlüssel-Logo mit Name, Adresse | **Riegel 24** · **06221 24 24 24** · **riegel24.de** | speichern 26,94 · nummer 27,62 | Kontakt. |
| bevor Sie sie brauchen | weißer Zettel mit **Häkchen** | – | brauchen 28,61 | „gespeichert“ aus V5 entfällt – das Häkchen reicht. |

## Stummtest
Tür zu, Schlüssel innen (Lupe), 23:51, Akku 1 % (Problem) → Suche, Preise 49 €? / ?? € / 9 €*, Sturz mit 50 €? 100 €? 300 €? (Ursache: Preis-Chaos) →
Anruf Riegel 24, FESTPREIS 129 €, 20 MIN, Folie statt Bohrer (Lösung) → Klick, Häkchen am Schloss, Tür offen, Mensch drin (Ergebnis) →
RIEGEL 24, Sonne + Mond, Nummer mit Häkchen (Angebot).

## Korrekturrunde (nach Textbogen 1)
- Zettel „Folie“ war im Schloss-Schnitt zu klein (46 px) → 62 px, schwarzer Grund dahinter größer, damit die Holzmaserung nicht durchscheint.
- Suchbegriff im Handy (30 px) war am Handy kaum lesbar → 36 px; Preisschilder im Handy von 34 auf 50 px.
- Geprüft und so gelassen: Preisschilder im Flur landen jetzt auf 8,80 / 9,82 / 10,58 (V5 zeigte „300 €?“ 0,56 s zu früh bei 10,02; `wortzeiten.py` hätte es mit 11,10 um 0,5 s zu spät gesetzt – erst die Pegelkurve gab 10,58).

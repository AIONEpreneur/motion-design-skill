# REGIE V7 · 14 Lernwerk Nachhilfe (Skizzenbuch, g russ „Emergence“ Illustrated)

## 1. Wie geht das Original mit Text um?
Das Original (`ref/v3_crop.mp4`, Raster alle 10 s) arbeitet sichtbar mit Handschrift, aber fast nur so:
- **Beschriftungen am Objekt**, meist ein Wort in dünner Handschrift unter dem Ding: „stars“, „planets“, „lego“, „bricks“,
  „combine“, „arrange“, „connect“, „intersect“, „technical“, „philosophical“, „encourage“.
- **Ein Kapitelwort** oben links oder in einer Banderole: „Nature“, „advice“, „EMERGENT“, „ADVICE #1“, „1 BUILDING BLOCKS“.
- Selten eine kurze Zeile („two main building blocks“, „So what is emergence?“). Die Ausnahme ist nicht das Muster.

**Entscheidung: Bild-Original mit Handschrift als Stilmittel.** Text ist hier Stil, aber als **Beschriftung**, und das passt
genau zur V7-Regel: ein Wort oder eine Zahl in runder Handschrift **am Objekt**, dazu die Banderole für das Angebot.
Wegfallen die Satz-Überschriften aus V5, weil das Original so etwas nicht macht und der Auftraggeber keine Sätze will:
„Es fehlt nur ein Baustein“, „Lernwerk findet die Lücke“, „rechnet wieder gern“, „JEDEN ABEND“, „2× pro Woche“,
„nach 8 Wochen“, „schon wieder“, „jetzt buchen:“, „eine Gruppe“, „max. 3 Kinder“ als Zeile.
Das Aufwischen der Handschrift bleibt als Stilmerkmal, ist aber kurz (0,3 s) und **auf dem Wort fertig**. Getippt wird nichts
mehr: Kein Satz baut sich Wort für Wort auf.

Betonung sonst mit den Bildmitteln des Originals: Koralle-Kringel und gestrichelte Umrandung (wie „Di/Do“), Lupe, Leuchten,
Häkchen, Riss, Wackeln, Pfeilbogen.

## 2. Wortzeiten
`wortzeiten.py` hat 47 von 64 Wörtern um mehr als 0,2 s verschoben. Ich habe sie an der Pegelkurve (mit Zischanteil)
nachgeprüft und 13 korrigiert (`"geprueft": "pegel"`):

| Wort | Werkzeug | geprüft | Befund |
|---|---|---|---|
| Fünf | 1,51 | **1,38** | f-Zischlaut 1,375–1,45 (Zischanteil 0,44–0,51), Vokal ab 1,475 |
| Abend | 5,01 | **4,97** | Senke 4,95 zwischen „Jeden“ und „Abend“ |
| Streit | 5,34 | **5,45** | „Sch“ 5,45–5,525 (Zisch 0,73–0,85), vorher Vokal von „Abend“ |
| Hausaufgaben | 6,24 | **6,07** | „die“ endet mit Senke 6,05, s von „Haus“ schon bei 6,30 |
| Versetzung | 7,54 | **7,51** | Stille 7,475–7,50, f-Einsatz 7,525 |
| wackelt | 7,99 | **7,95** | Senke 7,915–7,94 vor dem W |
| fehlt | 9,68 | **9,60** | f-Zischlaut ab 9,60 |
| Probestunde | 15,08 | **15,20** | s von „-losen“ 15,025, p-Verschluss 15,175–15,25 |
| zweimal | 16,75 | **16,69** | Pause nach „Dann“, Affrikate ab 16,68 |
| Kinder | 18,88 | **18,76** | k-Verschluss 18,705–18,73, danach Anstieg |
| Gruppe | 19,42 | **19,34** | g-Verschluss 19,32 |
| Drei (Note) | 21,49 | **21,33** | d-Senke 21,325 nach „eine“ |
| Probestunde (Schluss) | 26,89 | **26,99** | s von „kostenlose“ 26,825–26,875, Stille 26,975 = p-Verschluss |

Bestätigt ohne Änderung: Ihr, Kind, Mathe, Schon, Jeden, Dabei, Lernwerk, findet, genau, Lücke, kostenlosen, Dann, pro,
höchstens, drei, Nach, acht, Wochen, eine, Kind, rechnet, gern, Lernwerk, Nachhilfe, Buchen, kostenlose.
Feste Sekunden im Film (Haus, Weg, Kind läuft, Kamerafahrten, `K.nur = 9.64`, `K.wieder2 = 22.62`) sind durch K-Werte ersetzt.

## 3. Beat für Beat
| Beat | Hervorhebung (Bild) | Text am Objekt | fertig bei Wort (Zeit) | Warum |
|---|---|---|---|---|
| Ihr Kind bringt eine Fünf | Klassenarbeit fliegt aus der Hand, die rote **5** schreibt sich, das Kind lässt den Kopf hängen | **5** (Note auf dem Blatt) | Fünf 1,38 | Die Note ist eine Zahl, sie gehört aufs Blatt |
| nach Hause | Haus zeichnet sich, gestrichelter Weg mit Pfeil, Kind läuft | – | Hause 2,11 | Das Bild ist eindeutig |
| In Mathe | Kopfzeile des Blatts: **Mathe** schreibt sich, koralle unterstrichen | **Mathe** (Kopf der Klassenarbeit) | Mathe 2,86 | Das Fach sieht man nicht, es ist ein Name. Früher stand es als freie Überschrift, jetzt steht es auf dem Blatt. |
| Schon wieder | Zwei weitere Arbeiten mit 5 fliegen dazu | **× 3** neben dem Stapel | wieder 3,78 | „schon wieder“ ist eine Häufigkeit, die Zahl sagt sie am Stapel. „schon wieder“ als Text entfällt. |
| Jeden Abend | Nachtblau, Mond, Uhrzeiger rasen, Lampe | – | Jeden 4,72 | Mond und rasende Uhr heißen „Abend für Abend“. Die Überschrift „JEDEN ABEND“ entfällt. |
| Streit | Eltern-Arm hebt sich, Sprechwolken mit Kritzel | – | Streit 5,45 | Das Bild ist eindeutig |
| Hausaufgaben | Heft auf dem Tisch, gestrichelter Zeiger | **Hausaufgaben** am Heft (vorhanden) | Hausaufgaben 6,07 | Worum es geht, ist mehrdeutig (Heft, Buch, Brief?). Ein Wort am Objekt klärt es. |
| Versetzung wackelt | Treppe aus Bausteinen, die oberste Stufe **wackelt, reißt**, „?“ darüber | **Klasse 5 / 6 / 7** an den Stufen (vorhanden) | Versetzung 7,51 (Treppe steht), wackelt 7,95 (Riss) | Die Stufe „Klasse 7“ reißt, das ist die Versetzung. Die Überschrift „Versetzung?“ entfällt. |
| Fehlt nur ein Baustein | Pyramide mit Lücke: **gestrichelter Kringel in Koralle** zieht sich um die Lücke, „?“ darin | – | fehlt 9,60 | Die Lücke ist das Problem. Der Kringel zeigt sie. Die Zeile „Es fehlt nur ein Baustein“ entfällt. |
| ein einziger Baustein | Ein koralle Stein schwebt rechts, Glanzstriche | **Brüche** unter dem Stein (vorhanden) | einziger 10,71 (Stein), Baustein 11,14 (Wort) | Welcher Baustein? Der Fachbegriff macht es konkret. |
| Lernwerk findet genau diese Lücke | **Lupe** fährt ein und bleibt auf „genau“ über der Lücke stehen, auf „Lücke“ leuchtet sie auf | **Lernwerk** auf dem Lupengriff | Lernwerk 11,93 (Griff), genau 12,92 (Lupe steht), Lücke 13,70 (Leuchten) | Wer sucht, ist ein Name, er steht am Werkzeug. Der Satz entfällt. |
| kostenlose Probestunde | Stein fliegt in die Lücke, rastet ein, Funken. Banderole rollt aus | **kostenlose** + Banderole **PROBESTUNDE** | kostenlosen 14,59, Probestunde 15,20 | Das Angebot braucht Worte, 2 Wörter in der Banderole wie „ADVICE #1“ im Original |
| zweimal pro Woche | Wochenkarten Mo–Fr, **Di und Do** werden koralle eingekringelt | **2×** vor der Wochenleiste | zweimal 16,69 (erster Kringel + 2×), Woche 17,30 (zweiter Kringel) | Die Kringel zeigen die Tage, die Zahl die Häufigkeit. „pro Woche“ als Zeile entfällt. |
| höchstens drei Kinder pro Gruppe | Tisch mit Lehrerin, drei Kinder setzen sich, **1 2 3** springen über die Köpfe. Dann zieht sich die gestrichelte Gruppenlinie um den Tisch. | **1 2 3** über den Kindern, dann **max. 3** am Gruppenrahmen | drei 18,52 (1 2 3), Gruppe 19,34 (Rahmen + max. 3) | „höchstens“ ist die Botschaft (kleine Gruppe). Das Schild am Rahmen sagt es als Zahl. „eine Gruppe“ und die Zeile „max. 3 Kinder“ entfallen. |
| nach acht Wochen: eine Drei | Blatt mit 5, Pfeilbogen mit 8 Punkten (je ein Punkt eine Woche), Blatt mit grüner **3**, Strahlen | **8 Wochen** unter dem Bogen, **3** auf dem Blatt | acht 20,34 (Beschriftung), Drei 21,33 (Note fertig) | Die Dauer ist eine Zahl mit Einheit, sie steht am Bogen. Die Überschrift „nach 8 Wochen“ entfällt. |
| Kind rechnet wieder gern | Glühbirne, **7 · 8 = 56** mit Häkchen, Herz und Sterne auf „gern“ | **7 · 8 = 56** am Tisch | rechnet 22,55, gern 23,09 | Rechnung und Häkchen sind das „rechnet“, Herz und Sterne das „gern“. Die Zeile entfällt. |
| Schluss | Bausteine stapeln sich zum Logo, Kritzel-Icons | **LERNWERK** · **Nachhilfe** · Banderole **KOSTENLOSE PROBESTUNDE** · Kontakt | Lernwerk 24,13, Nachhilfe 24,66, kostenlose 26,33, Probestunde 26,99 | Name, 2 Wörter Angebot, Kontakt. „jetzt buchen:“ entfällt. Der Kontakt kommt früher (ab „Buchen“) und steht dadurch länger. |

## 4. Stummtest
- **Problem:** eine 5 in Mathe, dreimal, Streit am Abend über die Hausaufgaben, die Stufe „Klasse 7“ reißt.
- **Ursache:** Die Pyramide hat eine Lücke („Brüche“).
- **Lösung:** Die Lupe „Lernwerk“ findet die Lücke, der Stein rastet ein, kostenlose Probestunde, 2× die Woche, max. 3 Kinder.
- **Ergebnis:** In 8 Wochen wird aus der 5 eine 3, das Kind rechnet mit Häkchen und Herz.
- **Angebot:** Lernwerk Nachhilfe, kostenlose Probestunde, Kontakt.

## 5. Korrekturrunden
- **Runde 1 (Standbilder):** Alle Beschriftungen sitzen am Objekt und sind lesbar. Der Kringel um die Lücke und der Name auf der
  Lupe tragen die Szene ohne Satz.
- **Runde 2 (Textbogen):** Die dritte Klassenarbeit landete erst 0,2 s nach „wieder“, als „× 3“ schon stand. Jetzt liegen alle
  drei auf „wieder“. „Hausaufgaben“ wischte 0,4 s, jetzt 0,3 s, fertig auf dem Wort.
- dichte.py: Standbild 0 %.

## 6. Ehrlich noch schwach
- „Jeden Abend“ steckt nur in Mond und rasender Uhr. Wer stumm schaut, liest eher „abends“ als „jeden Abend“.
- „Lernwerk“ auf dem Lupengriff ist klein (32 px, schräg). Der Name kommt groß erst auf der Schlusskarte.
- Die Wochenleiste „2×“ und die Gruppe „max. 3“ stehen im selben Bild. Das sind zwei Blickpunkte nacheinander, aber in einer Einstellung.

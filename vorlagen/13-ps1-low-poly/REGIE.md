# REGIE V7 · 13 Kistenheld Umzüge (PS1-Casino, Three.js)

## 1. Wie geht das Original mit Text um?
Ich habe das Original (g russ, „Final Version“, `ref/sheet.jpg`, `ref/srcsheet.jpg`) Bild für Bild angesehen. Unten in der Mitte
steht eine Pixelschrift-Zeile in Weiß mit einem gelben Wort und schwarzer Kontur: „LIKE LOSING“, „BLOCK OUT THE“,
„NOW THEIR SENSE“, „WORTH NOTHING“. Das sind **mitlaufende Untertitel**. Sie zeigen jeweils 2–3 Wörter des Sprechtexts und
laufen durch den ganzen Film, auch mitten im Satz („OF TIME AND“, „THEM THEIR NEW“). Überschriften wie bei Notion sind das nicht.

**Entscheidung: Bild-Original. Die V7-Regel gilt.** Die Casino-Zeile ist genau das, was der Auftraggeber in V5 als
„mitgetippt, nicht synchron, nervig“ verworfen hat. Die Projektregel ist außerdem, dass die Videos stumm verständlich sind
**ohne Untertitel**. Übernommen wird deshalb nur die Schrift: Pixelify in Versalien, Weiß/Gelb, schwarze Kontur, harter Einsatz
ohne Einblenden. Sie steht dort, wo Schrift im Casino-Raum ohnehin steht: auf LED-Tafeln, Etiketten, Neon, Kalender und
Wagen, also **am Objekt**. Die Untertitel-Position unten in der Mitte nutze ich nur einmal, für den Firmennamen auf der
Schlusskarte. Das ist ein Name und kein Satz.

Sonst betone ich mit Bildmitteln, die zum PS1-Spiel passen: Pixel-Ring (blinkt wie eine Zielmarkierung), rotes Pixel-✕,
grünes Pixel-Häkchen, „!“-Sprite, Batterie-Anzeige, Lichtschalter, Kamerazoom.

Nur Overlays und Timing geändert. Dazu kommen drei kleine Eingriffe in die Szene, jeder im Code markiert: Der Kalender zeigt
„MO“ und eine Aktentasche statt „MONTAG / NEUER JOB“. Die Handy-Nachrichten zeigen Name und ✕ statt Satzstücken. In der
Montag-Einstellung steht der Mann neben dem Kalender und verdeckt ihn nicht mehr.

## 2. Wortzeiten
`wortzeiten.py` hat 48 von 73 Wörtern um mehr als 0,2 s verschoben, meist um +0,2 bis +0,45 s. Ich habe sie an der
Pegelkurve nachgeprüft und neun Wörter korrigiert (`"geprueft": "pegel"` in `out/vo.json`):

| Wort | Werkzeug | geprüft | Befund |
|---|---|---|---|
| Montag | 8,94 | **9,00** | „Am Mon-“ ist durchgehend stimmhaft, der t-Verschluss liegt bei 9,225. „Am“ dauert etwa 0,12 s. |
| fängt | 9,32 | **9,40** | Zischlaut f setzt bei 9,40 ein |
| Job | 10,27 | **10,22** | Senke bei 10,20–10,25, Anstieg ab 10,275 |
| Tag | 14,93 | **14,84** | t-Verschluss 14,825, Sprengung 14,85 |
| richtigen | 20,81 (interpoliert) | **20,94** | nach „im“ (20,80), Senke 20,925 |
| Raum | 21,38 | **21,36** | Senke 21,325–21,35, danach Anstieg |
| Wohnung | 23,56 | **23,66** | stimmhaftes W mit Zischanteil bei 23,675; Sprechende 24,05 |
| Kistenheld (Schluss) | 25,17 | **25,30** | bis 25,275 Stille, Sprung auf −34/−14 dB bei 25,30 |
| Umzüge | 25,95 | **25,87** | Senke 25,85, U-Einsatz 25,875 |

Bestätigt ohne Änderung: Samstag, Altbau, kein, fest, Nichts, gepackt, Freunde, abgesagt, Der, Am, Kistenheld, anders,
wir, hundert, Kartons, jeder, Zimmer, Das (Sofa), Möbellift, Fenster, Abends, alles, Pizza, Angekommen, Fester, kostenlose,
Besichtigung. Alle Schnitte (`CUT`) und Effektzeiten kommen aus K. Im Film stehen keine festen Sekunden mehr, auch die
Wagenfahrt nicht.

## 3. Beat für Beat
| Beat | Hervorhebung (Bild) | Text am Objekt | fertig bei Wort (Zeit) | Warum |
|---|---|---|---|---|
| Samstag | Die LED-Tafel ist aus und springt auf „Samstag“ an (Flackern) | **SAMSTAG 08:00** (LED, vorhanden) | Samstag 0,34 | Wochentag und Uhrzeit sind nicht zu malen. Die Tafel im Raum sagt es in einem Namen und einer Uhrzeit. |
| Altbau | Treppenhaus mit Holzstufen, Kamerafahrt | – | – | Das Bild ist der Altbau |
| Kein Aufzug | Um das durchgestrichene Aufzug-Schild zieht sich ein **Pixel-Ring** zu und blinkt | – | Aufzug 2,17 | Das Schild ist klein und hängt am Rand. Ohne Markierung übersieht man es. Das Symbol ist eindeutig, Text wäre doppelt. |
| Sofa steckt fest | Nahaufnahme: Sofa klemmt, Mann stemmt, **„!“-Sprite** springt ein, Gesicht wird geschockt | – | fest 3,87 | Das Bild ist eindeutig, das „!“ ist das Warnsymbol des Spiels |
| Nichts gepackt | Volles Zimmer, flache Kartons: **Pixel-Ring** um die ungefalteten Kartons | – | Nichts 4,46 | „Nichts“ lässt sich nur als Zustand zeigen: Die Kartons liegen flach, das Zimmer ist voll. Der Ring lenkt den Blick dorthin. |
| Freunde haben abgesagt | Handy-Chat: TOM, LISA, BEN erscheinen und bekommen je ein **rotes Pixel-✕**, das Handy ruckt beim letzten | Namen im Chat (in der Welt) | Freunde 5,47 / haben 5,91 / abgesagt 6,16 | Drei Namen mit rotem ✕ lesen sich stumm als drei Absagen. Der alte Stempel „ABGESAGT“ und die Satzstücke „BIN KRANK“, „KANN NICHT“ fallen weg. |
| Mietwagen muss heute Abend zurück | Mietwagen, die Straßenuhr rast und wird rot. Das Rückgabe-Schild am Wagen **blinkt rot** | **MIETWAGEN** (Wagen), **RÜCKGABE 20:00** (LED am Wagen), Uhrzeit (vorhanden) | Abend 7,95 (Uhr rot), zurück 8,18 (Schild blinkt) | Die Frist braucht eine Zahl. Sie steht am Wagen. |
| Montag neuer Job | Müdes Gesicht, daneben der Kalender. Um **MO** zieht sich ein Pixel-Ring, darunter eine Aktentasche. Eine **Batterie-Anzeige** läuft leer. | **MO** (Kalender) | Montag 9,00, Job 10,22 (Batterie ab hier leer) | Der Wochentag steht als ein Wort am Kalender, der Job als Aktentasche (Symbol), die Erschöpfung als leere Batterie. Das Wort „KRAFT“ entfällt. |
| Mit Kistenheld | Straße wird hell (Lichtschalter), der Kistenheld-Wagen fährt ein und steht | **KISTENHELD** (Wagen, LED, vorhanden) | Kistenheld 11,22 | Wendepunkt: Licht an, Name am Wagen |
| läuft das anders | Die Crew läuft ins Bild | – | anders 12,31 | Das Bild ist eindeutig |
| 100 Kartons an einem Tag | Draufsicht: Raster füllt sich mit Kartons, der Balken läuft voll | **100** über dem Raster, **1 TAG** am Balkenende | hundert 13,53 / Tag 14,84 | Menge und Dauer sind Zahlen, das Bild allein sagt sie nicht. „KARTONS“ entfällt, man sieht sie. |
| Jeder Karton sein Zimmer | Hand klebt die Etiketten nacheinander auf, das letzte auf „beschriftet“ | **KÜCHE / BAD / KIND / WOHNEN** (Etiketten) | jeder 15,45 … beschriftet 16,54 | Die Etiketten sind die Aussage, am Objekt |
| Sofa per Möbellift durchs Fenster | Lift fährt hoch, Sofa gleitet durchs Fenster | – | Möbellift 18,22, Fenster 19,12 | Das Bild ist eindeutig |
| Abends alles im richtigen Raum | Puppenhaus: Kartons fliegen in die Räume, Licht geht an, pro Raum ein **grünes Pixel-Häkchen** am Raumschild | Raumschilder (vorhanden) | letztes Häkchen auf Raum 21,36 | „richtig“ lässt sich nur mit dem Häkchen zeigen: Etikett passt zu Raum |
| Pizza in neuer Wohnung | Paar isst Pizza, Herzen steigen seitlich auf | – | Pizza 22,43, Wohnung 23,66 (Herzen) | Das Bild ist eindeutig |
| Angekommen | **Kamera-Zoom** auf das Neon, das Neon flackert an | **ANGEKOMMEN** (Neon im Raum, vorhanden) | Angekommen 24,39 | Das Schlusswort der Geschichte steht schon im Raum. Der Zoom macht es lesbar. Das zweite, große „ANGEKOMMEN.“ unten entfällt. |
| Schluss: Name | Wagen, Crew winkt | **KISTENHELD UMZÜGE** als Casino-Zeile unten (Name, als Ganzes) | Kistenheld 25,30 | Name der Firma, einziger Einsatz der Untertitel-Position |
| Fester Preis | – | – | – | Laut Regel höchstens 2 Wörter Angebot. Die kostenlose Besichtigung ist der stärkere Anlass anzurufen, „Fester Preis“ bleibt gesprochen. Die Tafel „FESTER PREIS“ entfällt. |
| Kostenlose Besichtigung | LED-Tafel springt an (Blinken) | **BESICHTIGUNG KOSTENLOS** (LED an der Fassade) | kostenlose 27,64 | Angebot, 2 Wörter, am Haus |
| Kontakt | – | kistenheld-umzuege.de · Telefon | ab Fester 26,73 | Kontakt muss lange genug stehen |

## 4. Stummtest
- **Problem:** Samstag, kein Aufzug, das Sofa klemmt, nichts ist gepackt, drei Absagen, Rückgabe 20:00, Montag Job, die Batterie ist leer.
- **Lösung:** Licht an, der Kistenheld-Wagen kommt, 100 Kartons an 1 Tag, Etiketten, Möbellift.
- **Ergebnis:** Häkchen in jedem Raum, Paar mit Pizza, „ANGEKOMMEN“.
- **Angebot:** Kistenheld Umzüge, Besichtigung kostenlos, Kontakt.

## 5. Korrekturrunden
- **Runde 1 (Standbilder):** Bei „Nichts gepackt“ verdeckte der Mann die flachen Kartons, er steht jetzt links. Das „!“ war
  oben abgeschnitten und sitzt jetzt tiefer. Das Schild „RÜCKGABE 20:00“ war nicht lesbar: 1,8-fach größer und zur Kamera
  gedreht. „1 TAG“ ist größer. Der Zoom auf das Neon ging zu weit (nur Wand), jetzt sind die Köpfe mit im Bild.
- **Runde 2 (Textbogen):** Die Etiketten KÜCHE/BAD/KIND/WOHNEN waren zu klein und sind jetzt 1,7-fach. Der Ring um „MO“ schnitt
  die Buchstaben und ist größer.
- dichte.py: Standbild 3 %, 3,9 Schnitte/10 s.

## 6. Ehrlich noch schwach
- „Fester Preis“ ist gesprochen, steht aber nirgends im Bild. Das ist die Folge der 2-Wort-Regel für das Angebot.
- Die Rückgabe-Tafel ist wegen der PS1-Auflösung (Textur 80 px) nur knapp lesbar. Die rote Uhr trägt die Frist.
- Das Chat-Handy zeigt nur Namen mit ✕. Wer die Geschichte nicht kennt, liest „Absage“ erst beim dritten ✕.

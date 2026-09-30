# REGIE V7 · 15 Werkseite (Brand-Motion, dunkle „Story“-Panels)

## 1. Wie geht das Original mit Text um?
Das Original (`ref/panels.mp4`, `ref/story.mp4`, `ref/reel.mp4`, Raster alle 2–2,5 s) zeigt fast keinen Text:
- **Eine Serifenzeile unter dem Heldenobjekt**, und sie ist ein **Name**: „Logo + jingle“ (mit Terrakotta-„+“).
  Sie steht still, als Ganzes, die ganze Einstellung lang.
- **Eine kleine dunkle Pille als Etikett** am Objekt: „Use them together“.
- Sonst nur Bildmittel: Scheibe wächst aus einem Punkt, Wellenringe, gepunktete Bogenpfeile, Stern-Symbol.

**Entscheidung: Bild-Original. Die V7-Regel gilt, mit der Serifenzeile als Namenszeile.** Die V5 hatte zu jedem Bild einen
ganzen Satz in Garamond, der sich Wort für Wort einblendete: „Er findet Ihre Website.“, „Nach zwei Sekunden“,
„Ihre Arbeit ist besser.“, „Jetzt klingelt Ihr Telefon.“, „baut Ihre neue“, „jede Woche“. Das Original macht das nicht, die
Sätze fallen weg. Wie im Original bleibt die Serifenzeile **nur für den Namen** „Werkseite“ unter der Scheibe.
Die Pille wird zum Etikett am Objekt, mit einem Wort. Betonung sonst mit Terrakotta-Kreis, Durchstreichen, Ringen,
Stern-Plakette und dem Sekundenring.

## 2. Wortzeiten
`wortzeiten.py` hat 52 von 66 Wörtern um mehr als 0,2 s verschoben (bis +0,96 s). Ich habe sie an der Pegelkurve
(mit Zischanteil) nachgeprüft und 13 korrigiert (`"geprueft": "pegel"`):

| Wort | Werkzeug | geprüft | Befund |
|---|---|---|---|
| Schrift | 4,14 | **4,03** | „Sch“ 4,025–4,10 (Zisch 0,50–0,94) |
| kein | 4,77 | **4,90** | Bis 4,80 läuft noch das t von „Schrift“, Pause 4,85–4,875, k-Sprengung 4,90 |
| Foto | 5,00 | **5,10** | f-Zischlaut ab 5,10 (0,44–0,71) |
| keine | 5,47 | **5,42** | k-Verschluss 5,395, Sprengung 5,42 |
| Telefonnummer | 5,83 | **5,80** | T-Verschluss 5,755–5,78 |
| weg | 9,12 | **9,07** | s von „ist“ 8,80–8,875, „er“ 8,925, W ab 9,07, g-Verschluss 9,225 |
| baut | 15,25 | **15,20** | Ende „Werkseite“ 15,2, t von „baut“ 15,37–15,42 |
| Website (neue) | 16,08 | **16,16** | Senke 16,155 zwischen „neue“ und „Website“ |
| vierzehn | 16,84 | **16,74** | Pause 16,66–16,74 nach „in“, f ab 16,74 |
| Logo | 18,27 | **18,08** | Senke nach „Ihr“ 18,02–18,07, L ab 18,08; „go“ endet 18,49 |
| Projekte | 19,46 | **19,37** | ch 19,15–19,225, t-Verschluss 19,25, P-Hauch 19,375 |
| Knopf | 20,59 | **20,50** | k-Verschluss 20,465–20,49, Hauch 20,515 |
| Werkseite (Schluss) | 25,61 | **25,74** | Stille bis 25,735, Einsatz 25,76 |

Bestätigt ohne Änderung: Kunde, Tischler, Er, findet, Website, Winzige, Nach, Auftrag, nebenan, Dabei, Arbeit, besser,
Werkseite, Tagen, Ihr, Ihre, und, Jetzt, klingelt, Telefon, Jede, Woche, Anfragen, Websites, Handwerker, zum, Festpreis.
Die fest eingetragenen Alt-Zeiten im Film (`Object.assign(K, {sucht: .56, er: 1.87, …})`, Kamerafahrten `lin(t, 7, 9)`,
`lin(t, 12, 14.4)`, `lin(t, 25.4, DUR)`) sind entfernt. Alles kommt aus `zeiten.py`.

## 3. Beat für Beat
| Beat | Hervorhebung (Bild) | Text am Objekt | fertig bei Wort (Zeit) | Warum |
|---|---|---|---|---|
| Kunde sucht Tischler | Porträt-Papier, Telefon zeichnet sich. Das Goldpapier mit Jahresringen (Holz) kommt, Bogenpfeil | Suchfeld im Telefon: **Tischler** (als Ganzes, nicht getippt) | Tischler 1,46 | Was gesucht wird, zeigt das Suchfeld. Die Serifenzeile „Tischler gesucht.“ entfällt. |
| Er findet Ihre Website | Ergebnisliste, erster Treffer leuchtet Terrakotta mit Ringen, dann öffnet sich die graue alte Seite | Treffer „Tischlerei Holm“ / **tischlerei-holm.de** (Name, Adresse) | findet 2,40, Website 3,05 | Der Name im Treffer sagt „Ihre“. „Ihre Website“ als Satzstück in der Liste entfällt. |
| Winzige Schrift | Terrakotta-Kreis um die Textzeilen, Papier-Etikett mit Pfeil | **winzig** | Winzige 3,75 | Ein Schlüsseladjektiv am Objekt. Ohne das Wort sieht man nur graue Zeilen. |
| kein Foto | Kreis um den leeren Bildplatzhalter | **~~Foto~~** (durchgestrichen) | Foto 5,10 | Durchstreichen ist das Bildmittel für „fehlt“ |
| keine Telefonnummer | Kreis um die leere Kontaktzeile | **~~Nummer~~** (durchgestrichen) | Telefonnummer 5,80 | wie oben |
| Nach zwei Sekunden ist er weg | Porträt in der Scheibe läuft leer, der Terrakotta-Sekundenring schrumpft, das Porträt fliegt raus, Ringe | Zähler **2,0 s → 0,0 s** unter der Scheibe, am Ende Terrakotta | zwei 7,74 (2,0 s), weg 9,07 (0,0 s) | Die Dauer ist eine Zahl mit Einheit, am Objekt. Das große „weg.“ entfällt, man sieht das Porträt verschwinden. |
| Auftrag geht an den Betrieb nebenan | Links das graue Telefon (Ihre Seite), rechts leuchtet „Tischlerei Nebenan“ auf. Das Goldpapier wandert den Punktbogen hinüber, Ringe beim Ankommen. | **Auftrag** auf dem Goldpapier. Im rechten Telefon der Name „Tischlerei Nebenan“ (vorhanden). | Auftrag 10,14, nebenan 11,40 (Ringe) | Das Goldpapier ist ohne Wort nicht als Auftrag zu lesen. Die Zeilen „Ihr Auftrag“ / „Betrieb nebenan“ unter den Telefonen entfallen. |
| Dabei ist Ihre Arbeit besser | Große Tuschezeichnung Einbauschrank auf Knitterpapier, **Stern-Plakette** springt ein, Ringe | – | besser 13,81 | Die Plakette ist das Qualitätssymbol. Der Satz „Ihre Arbeit ist besser.“ entfällt. |
| Werkseite | Terrakotta-Punkt, die Scheibe wächst, das Haus steht auf dem Horizont, Ringe | **Werkseite** (Serifenzeile unter der Scheibe, wie „Logo + jingle“) | Werkseite 14,61 | Name der Marke, genau wie im Original |
| baut neue Website | Telefon-Drahtrahmen zeichnet sich, Platzhalter füllen sich | – | Website 16,16 | Das Bild ist eindeutig. „baut Ihre neue“ entfällt. |
| in 14 Tagen | 14 Punkte unter dem Telefon füllen sich nacheinander | **14 Tage** über den Punkten | vierzehn 16,74 | Die Frist ist eine Zahl mit Einheit, am Objekt |
| Logo / echte Projekte / Knopf zum Anrufen | Neue Seite: Logo erscheint, Projekt-Papiere fliegen ein, Terrakotta-Knopf springt, Ringe | Pillen **Logo**, **Projekte**, **Anrufen** mit Punktpfeil ans Element | Logo 18,08, Projekte 19,37, Knopf 20,50 | Ein Wort je Pille wie „Use them together“. Satzstücke wie „ein Knopf zum Anrufen“ entfallen. |
| Jetzt klingelt Ihr Telefon | Telefon vibriert, Anruf-Bildschirm mit Porträt, Terrakotta-Ringe | Anrufanzeige im Telefon (vorhanden) | klingelt 22,53 | Das Bild ist eindeutig. Die Zeile „Jetzt klingelt Ihr Telefon.“ entfällt. |
| Jede Woche neue Anfragen | Drei Anfrage-Karten stapeln sich, jede mit Wochentag | **Anfrage** · Einbauschrank **Mo** / Treppe **Mi** / Esstisch **Fr** | Jede 23,86, neue 24,37, Anfragen 24,56 | Die Wochentage zeigen „jede Woche mehrere“. „jede Woche“ als Zeile entfällt. |
| Schluss | Scheibe mit Haus, Goldpapier, Streifen, Ringe | **Werkseite** (Serifenzeile), **Handwerker-Websites**, Pille **Festpreis**, Kontakt | Werkseite 25,74, Handwerker 27,35, Festpreis 28,50 | Name, ein Wort Angebot, Kontakt. Der Kontakt kommt ab „Websites“ und steht dadurch lange genug. |

## 4. Stummtest
- **Problem:** Der Kunde sucht einen Tischler und findet Ihre Seite: winzig, Foto und Nummer durchgestrichen. Nach 2,0 s ist er weg.
- **Folge:** Der Auftrag wandert zur Tischlerei nebenan.
- **Lösung:** Ihre Arbeit hat die Plakette. Die Werkseite baut in 14 Tagen eine neue Seite mit Logo, Projekten und Anruf-Knopf.
- **Ergebnis:** Das Telefon klingelt, Anfragen Mo, Mi, Fr.
- **Angebot:** Werkseite, Handwerker-Websites, Festpreis, Kontakt.

## 5. Korrekturrunden
- **Runde 1 (Standbilder):** Die Überblendung zur Werkseite-Szene begann genau auf „besser“, die Plakette war nie klar zu
  sehen. Jetzt beginnt die Überblendung 0,35 s nach „besser“ (`TR` aus K).
- **Runde 2 (Textbogen):** Ohne die Satzzeilen waren zwei Bilder halb leer. Die Szene „besser“ steht jetzt mittig. Das
  klingelnde Telefon steht erst in der Mitte und rückt nach rechts, wenn die Anfragen kommen.
- dichte.py: Standbild 1 %, Bewegung 3,3 (ruhig wie das Original, das nur überblendet).

## 6. Ehrlich noch schwach
- „besser“ trägt nur die Stern-Plakette. Stumm liest man „Qualität“, aber nicht den Vergleich mit dem Betrieb nebenan.
- Die Durchstreichung auf „Foto“/„Nummer“ ist dünn und bei kleinem Bild schwach.
- Im Telefon stehen Inhalte der Beispiel-Website („Möbel nach Maß“, „Neuer Kunde“, „Jetzt anrufen“). Das ist Bildinhalt,
  aber Text, der gelesen werden will.

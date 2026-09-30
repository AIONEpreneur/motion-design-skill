# REGIE V7 · 21 Pixel-Art · Fahrschule Grün-Pfeil

## 1. Wie geht das Original mit Text um?
Das Original (Ahmed T'aide, „It Wrote Every Frame“, Welt 1) ist ein **Bild-Original**: Die Geschichte erzählen Figuren, Sprung, Treffer und Zerfall.
Text kommt dort nur in der Grammatik eines Videospiels vor:
- **Namen mit Lebensbalken** oben links und rechts („BIT“, „SLIME KING“)
- **Kurze Ausrufe** in Pixelschrift mit RGB-Versatz, jeweils ein oder zwei Wörter im Moment des Ereignisses („!! BOSS !!“, „HIT-STOP“, „VICTORY!“)
- **Kleine Etiketten** direkt über Objekten („12 FPS“, „SMOOTH“) und eine Plakette unten links

Einen Satz gibt es dort nie. **Daraus folgt:** Es gilt die V7-Regel für Bild-Originale. Die Spielgrammatik bleibt, weil sie der Stil ist, aber nur in der Form des Originals:
- **Namen am HUD:** „SIE“ und „PRÜFUNG“ mit Lebensbalken
- **Genau zwei Ausrufe** als Klammer: „DURCHGEFALLEN“ (Game over) und „BESTANDEN!“ (Victory). Jeder ist ein Einzelwort, fällt als Ganzes, ist fertig auf dem gesprochenen Wort und sitzt am Kampfgeschehen.
- **Etiketten am Objekt:** „JOB“ am Turm, „6 WOCHEN“ am Questmarker, „GRÜN-PFEIL“ am Power-up, „LINKSABBIEGEN“ mit Zähler „n/10“ am Fähigkeitsfenster
- **Alles andere entfällt:** die Unterzeilen „SCHON WIEDER.“, „BEIM LINKSABBIEGEN“, „KEIN WEG HIN.“, „ECHTE STRECKE“ und „SELBST ZUR ARBEIT“, die zudem getippt waren, sowie die Kapitel-Titel „2 FEHLER“, „IN 6 WOCHEN:“, „OHNE AUTO:“, „SCHWACHSTELLE:“, „10x LINKS“, „PROBEPRÜFUNG“, „DIESMAL:“ und „MONTAGMORGEN“.
- **Betonung** läuft stattdessen über die Spielmittel: Herzen zerbrechen, rote Kreuze, Pfeil-Geschosse, Durchstreichen, Zielrahmen, Fortschrittsbalken, Häkchen, Hit-Stop mit Punch-in und Aufleuchten.

## 2. Wortzeiten
`wortzeiten.py` neu gemessen, danach jedes Schlüsselwort an der Pegelkurve geprüft (`pegel.py`, Wortanfang = Sprung auf Sprachpegel,
bei Zischlauten der Beginn des Zischens). 34 Werte korrigiert und in `out/vo.json` mit `"geprueft": "pegel"` und dem alten Wert vermerkt.
Die größten Fehler des Werkzeugs: zehnmal 12,41 → **12,90**, üben 10,41 → **10,72**, sitzt 14,89 → **14,63**, arbeit 22,22 → **22,47**,
pfeil (Schluss) 24,32 → **24,12**, schwachstelle 11,43 → **11,64**, fehler 2,77 → **2,92**, wochen 6,00 → **5,82**, job 6,97 → **6,82**.
Alle Zeiten im Film sind Abstände zu diesen K (`zeiten.py` → `film/zeiten.js`). Es gibt keine festen Sekundenwerte mehr, auch nicht in `ton/partitur.py`.

## 3. Beat für Beat
| Beat | Hervorhebung (Bild) | Text am Objekt | fertig bei Wort (Zeit) | Warum |
|---|---|---|---|---|
| Durchgefallen | Ampel-Boss mit rotem Wutgesicht, Treffer-Blitz am Auto, **Lebensbalken SIE läuft leer**, erstes Herz zerbricht | HUD **SIE** / **PRÜFUNG** (Namen), Ausruf **DURCHGEFALLEN** über der Szene, rot mit RGB-Versatz | durchgefallen 0,31 | Das ist der Game-over-Moment des Originals. Ein Einzelwort als Ausruf ist genau dessen Grammatik und benennt das Problem eindeutig. Ein leerer Balken allein ließe offen, wer verloren hat. |
| Schon wieder | **Zweites Herz** zerbricht mit rotem Kreuz und Aufblitzen, ein Ring pulst um die Herzen | – | schon 1,42 | Zwei verlorene Leben zeigen „wieder“ ohne Wort. |
| Zwei Fehler beim Linksabbiegen | Die Ampel schießt zwei **Links-Pfeile** auf das Auto. Jeder Treffer lässt das Auto aufblitzen und setzt ein **rotes Kreuz** darüber. | – | fehler 2,92 (1. Treffer), linksabbiegen 3,30 (2. Treffer) | Zwei Kreuze zählen die Fehler, der Links-Pfeil zeigt die Ursache. Die Zahl steckt im Bild. |
| In sechs Wochen neuer Job | Kamera fährt zur Stadt, ein **Questmarker** fällt auf einen Turm, Sanduhr-Symbol | **6 WOCHEN** am Questmarker, **JOB** am Turm | sechs 5,52 (6 WOCHEN), job 6,82 (JOB) | Dauer und Ziel sind ohne Wort mehrdeutig, deshalb eine Zahl mit Einheit und ein Wort, beide am Objekt. |
| Ohne Auto | Das Auto blinkt und **verpufft**. Zurück bleibt ein gestrichelter Umriss, der **rot durchgestrichen** wird. Die Figur steht zu Fuß da. | – | ohne 7,66 (weg), auto 7,93 (Strich) | Durchstreichen ist das Bildmittel für „ohne“. |
| Kommen Sie nicht hin | Gepunkteter Weg zum JOB-Turm wächst und **bricht mit rotem Kreuz ab**, Schweißtropfen | (JOB bleibt) | nicht 8,64 (Kreuz) | Der abgebrochene Weg ist die Aussage. |
| Bei Grün-Pfeil | **?-Block** wird angestoßen, das Grün-Pfeil-Schild steigt als Power-up heraus, Funkenkranz | **GRÜN-PFEIL** als Etikett über dem Power-up (Name) | bei 9,67 (Stoß), grün 9,99 (Etikett) | Der Name muss einmal eingeführt werden, und zwar am Objekt, so wie „SMOOTH“ im Original. |
| (Auto kommt zurück) | Das Schild fällt auf die Figur, und das Auto baut sich per Raster neu auf, mit Grünpfeil-Dachschild | – | fertig vor üben 10,72 | Bild: Die Lösung gibt das Auto zurück. |
| Üben … Schwachstelle | **Fähigkeitsfenster** springt auf, der Balken blinkt rot auf 2/10, ein **Zielrahmen rastet** um das Fenster ein | **LINKSABBIEGEN** (Name der Fähigkeit), **2/10** | üben 10,72 (Fenster), schwachstelle 11,64 (Rahmen) | Der Zielrahmen ersetzt die Lupe. Welche Fähigkeit schwach ist, zeigt ein Wort am Fenster, denn das Bild allein sagt das nicht. |
| Zehnmal Linksabbiegen | Zehn Links-Pfeile fliegen ein und werden eingesammelt. Der Balken wächst von rot über orange nach grün, der **Zähler** läuft mit. | **n/10** | zehnmal 12,90 (erster Pfeil unterwegs) | Die Zahl zählt sichtbar mit. |
| Bis es sitzt | Balken voll grün, Fenster leuchtet auf, **grünes Häkchen** | **10/10** | sitzt 14,63 | Häkchen statt „SITZT!“ |
| Probeprüfung | Kamera fährt weiter, der **Boss fällt von oben** und landet mit Staub und Wackeln. Das HUD mit den Lebensbalken kommt zurück. | HUD **SIE** / **PRÜFUNG** | probeprüfung 16,12 (Landung) | Boss-Auftritt wie „!! BOSS !!“, aber ohne Ausruf: Der Name im HUD reicht. |
| Echte Strecke | Auf dem Boden zieht sich eine **Fahrbahnmarkierung** ein. Das Auto springt über zwei Pfeil-Geschosse und sammelt Münzen. | – | echten 17,20 (Markierung + 1. Ausweichen) | Die Markierung zeigt „echte Straße statt Übungsplatz“. |
| Und diesmal | Das Auto springt in einer Parabel auf den Boss, die Hieb-Sichel zeichnet sich | – | diesmal 18,90 (Absprung) | Die Bewegung trägt die Spannung. |
| Bestanden | **Hit-Stop**: Standbild, Punch-in 1,4×, der Boss wird weiß, dann rot, dann grün und lächelt. Der PRÜFUNG-Balken fällt auf null, danach Zerfall in Münzen. | Ausruf **BESTANDEN!**, gelb mit RGB-Versatz | bestanden 19,70 (Einschlag = Wortanfang) | Das „VICTORY!“ des Originals, ein Einzelwort als Gegenstück zu DURCHGEFALLEN. |
| Montagmorgen | Himmel wechselt per Raster auf Morgen, die **Sonne steigt** | – | montagmorgen 20,65 | Der Morgen ist im Bild. „Montag“ ist Farbe und kein Kern der Aussage. |
| Selbst zur Arbeit | Das Auto fährt allein zum Gebäude, der Questmarker hüpft darüber, auf dem Wort **leuchten die Fenster auf**, die Fahne wird grün und ein **grünes Häkchen** erscheint | **JOB** am Gebäude (dasselbe Etikett wie vorher = Quest erfüllt) | selbst 21,82 (Auto am Ziel), arbeit 22,47 (Häkchen) | Der Rückbezug auf „JOB“ schließt die Geschichte ohne Satz. |
| Fahrschule Grün-Pfeil | Schild mit grünem Pfeil steigt ein und federt nach | **FAHRSCHULE** (klein, als Ganzes), **GRÜN-PFEIL** (Logo) | fahrschule 23,20, grün 23,87 | Logo und Name |
| Erste Übungsstunde | Plakette (die glatte Schrift des Originals) springt auf | **1. ÜBUNGSSTUNDE** | erste 24,94 | Angebot, 1 Zahl + 1 Wort |
| Kostenlos | Wort springt ein, blinkt, Punktleiste läuft voll, Münzen | **KOSTENLOS** | kostenlos 26,04 | Das Angebotswort landet auf seinem Wort. |
| Kontakt | Web und Telefon als Ganzes | gruenpfeil-fahrschule.de · 0421 55 90 21 | nach kostenlos (26,34) | Kontakt, nicht getippt |

## 4. Stummtest
- **Problem:** leerer Balken, zerbrochene Herzen, DURCHGEFALLEN
- **Ursache:** zwei Links-Pfeil-Treffer
- **Folge:** JOB in 6 WOCHEN, das Auto ist durchgestrichen, der Weg bricht ab
- **Lösung:** Power-up GRÜN-PFEIL, Fenster LINKSABBIEGEN 2/10 → 10/10 ✓
- **Ergebnis:** BESTANDEN!, dann ✓ am JOB
- **Angebot:** 1. ÜBUNGSSTUNDE KOSTENLOS

## 5. Ton
Partitur unverändert in Klang und Aufbau. Alle Einsätze liegen jetzt auf den geprüften K, die festen Werte 7,3 / 15,62 / 15,9 / 19,58 / 19,62 / 23,92 sind ersetzt. Danach wird neu gemischt.

## 6. Korrekturrunden (Textbogen `out/textbogen_teil1/2.jpg`)
1. **Erster Bogen:** Nach dem Neuaufbau blieb das Auto dauerhaft weiß. Ursache: Die Blitz-Bedingung für „ohne“ hatte kein Ende mehr, jetzt nur noch bis K.ohne.
   Weitere Fehler: Der rote Strich für „ohne Auto“ wirkte wie eine lose Linie, der Umriss war kaum sichtbar. Jetzt ist der Umriss dichter gestrichelt und der Strich liegt kürzer mit dunkler Kante quer durch ihn.
   Das Etikett JOB stand zu nah am neuen Etikett GRÜN-PFEIL und endet jetzt vor dem Power-up. So gibt es einen Blickfang pro Einstellung.
2. **Zweiter Bogen:** Die Sanduhr las sich als „I6 WOCHEN“ (= 16). Sie ist jetzt eine echte 6×8-Sanduhr mit roter Füllung und Abstand zum Text. Das Etikett klebte am oberen Rand und sitzt jetzt 2 Pixel tiefer.
   Im Zähler berührte „10/10“ den Balken. Die Segmente sind jetzt schmaler.
3. **Dritter Bogen:** Das Logo fiel beim Einfallen durch „FAHRSCHULE“. Jetzt steigt es von unten ein.
- `dichte.py`: Standbild-Anteil 0 %, Bewegung 8,4, Farbigkeit 84,6

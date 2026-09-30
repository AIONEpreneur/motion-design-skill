# REGIE V7 · 22 SaaS-Launch (Notion-Stil) · Pflegebrücke Personal

## 1. Wie geht das Original mit Text um?
Das Original (Notion-Launch-Video, `ref/player_240-292.mp4`, `ref_frames/sheet.jpg`) ist ein **Typografie-Original**. Der Text ist dort der Stil:
- Kurze Inter-Bold-Headlines in zwei bis drei Zeilen, jeweils mit **genau einem blauen Wort** („Docs here. / Chats there.“, „Get answers, instantly. / With **citations.**“)
- Jede Zeile ist ein eigener kleiner Satz und kommt **als Ganzes** aus der Unschärfe. „Tasks everywhere“ kommt als dritte Zeile dazu.
- Die blaue **Pille mit Punkt** („• Think“ → „• Ship“)
- Die **riesige blaue Zahl** über unscharfer Oberfläche
- Das **Schlussbild** aus Logo, Wortmarke, grauer Tagline, blauem CTA mit Klick und URL

Der Auftraggeber sagt, der Text in 22 sei „schon ganz okay, weil Notion ist das Video auch so“. Der Abgleich mit dem Original bestätigt das.
**Daraus folgt:** Die Headlines bleiben in Wortlaut, Lage und Farbe. Geändert wird nur, was klar besser wird:
1. **Nichts mehr Wort für Wort.** V5 baute jede Zeile Wort für Wort mit, also praktisch getippt. Jetzt kommt jede Zeile als Ganzes (0,25 s aus der Unschärfe) und ist am Anfang ihres gesprochenen Satzes fertig, so wie im Original.
2. **Exaktes Timing** auf die neu gemessenen und an der Pegelkurve geprüften Wortzeiten, keine festen Sekunden mehr, auch nicht in der Partitur.
3. **Weg, was vom Gesprochenen abweicht:**
   - Unterzeile „Datum, Bereich, Anzahl – fertig.“: nie gesprochen, gestrichen
   - Unterzeile „spätestens – dann ist die Schicht besetzt“: „dann“ wird nicht gesagt, und der Satz nimmt die nächste Headline vorweg. Stattdessen steht nur das gesprochene Wort **„spätestens“** grau über der Zahl.
   - „39 Std.“ → „48 Std.“: V5 zählte hoch, sodass beim Wort „achtundvierzig“ eine falsche Zahl stand. Jetzt erscheint **„48 Std.“** als Ganzes auf dem Wort.
4. **Nichts Getipptes in der Oberfläche:** Die Formularfelder springen gefüllt ein (Auswahl mit Häkchen), statt Buchstabe für Buchstabe getippt zu werden. Die Tagline im Schlussbild steht als Ganzes.
- **Bewusst belassen:**
  - „Zwei fallen aus.“ und „Lücke melden.“ bestehen nur aus gesprochenen Wörtern, sind aber verdichtet („Zwei [Pflegekräfte] fallen aus“, „melden Sie die Lücke“). Das ist die knappe Notion-Headline, die der Auftraggeber freigegeben hat. Die ausgeschriebene Form wäre der Skriptsatz und damit genau das „Mittippen“, das in V5 störte.
  - Die UI-Texte (Dienstplan-Namen, „Offen/Krank/Besetzt“, Stoppuhr, Toast „An 14 Fachkräfte gesendet“, „12 km Umkreis“, CTA „Schicht melden → Schicht gemeldet ✓“) sind Produktoberfläche wie im Original und keine Einblendungen.

## 2. Wortzeiten
`wortzeiten.py` neu gemessen, danach die Schlüsselwörter an der Pegelkurve geprüft (`pegel.py`, Wortanfang = Sprung auf Sprachpegel bzw. Beginn des Zischlauts).
40 Werte korrigiert, in `out/vo.json` mit `"geprueft": "pegel"` und dem alten Wert vermerkt. Das Werkzeug lag im 48-Stunden-Satz bis 0,46 s zu früh:
stunden 18,93 → **19,20**, ist 19,29 → **19,75**, die 19,51 → **19,92**, schicht 19,75 → **20,04**, besetzt 20,14 → **20,37**, achtundvierzig 18,38 → **18,49**.
Außerdem: lücke 12,96 → **12,66**, pflegebrücke 11,46 → **11,25**, nachtdienst 0,74 → **0,90**, zum 9,26 → **9,18**, ihnen 22,65 → **22,77**, personal 24,07 → **24,27**, schicht (Schluss) 26,45 → **26,36**.
Die Schnitte kommen aus K: `CUT` in `zeiten.py`, jeweils 0,23–0,35 s vor dem ersten Wort der neuen Zeile.

## 3. Beat für Beat
| Beat | Hervorhebung (Bild) | Text (Headline / am Objekt) | fertig bei Wort (Zeit) | Warum |
|---|---|---|---|---|
| Samstag, Nachtdienst | Dienstplan kippt dunkel ein, Mond-Plakette | Headline **Samstag, / Nachtdienst.** als Ganzes | samstag 0,32 | Ort und Zeit wie „Docs here.“, zwei Zeilen als eine Einheit |
| Zwei Pflegekräfte fallen aus | Zeile 2 wird auf „Zwei“ rot („Krank“), Zeile 4 auf „Pflegekräfte“, beide sind auf „fallen“ **Offen** (gestrichelter roter Kreis) | **Zwei fallen aus.** (blau: fallen aus) | zwei 1,85 | Die Zahl zeigt der Plan, die Headline sagt sie. |
| Krankmeldung hier | Kachel mit rotem Kreuz springt ein | **Krankmeldung hier.** | krankmeldung 3,64 | Jede Zeile ein eigener Satz, wie im Original |
| Anrufe da | Telefon-Kachel mit Zähler 3 vibriert | **Anrufe da.** | anrufe 4,76 | |
| (Nachrichten) | Chat-Kachel | – | da 5,34 | |
| Lücken überall | Kalender-Kachel mit roten Feldern, acht **rote Lücken-Kacheln** | **Lücken überall.** (blau: überall.) | lücken 5,72, Kacheln auf überall 6,27 | |
| (Kollaps) | Alles fällt in einen Lichtpunkt zusammen (Original-Übergang) | – | vor „Und“ | |
| Und wieder springen Sie selbst ein | Müde Figur | **Und wieder springen / Sie selbst ein.** als Ganzes | und 7,27 | Ein Satz = eine Einheit |
| Zum dritten Mal diesen Monat | Zeilen wechseln per Maske. Leiste mit vier Samstagen, **drei Avatare** landen nacheinander, der dritte auf „dritten“. Zähler 03 / 04. | **Zum dritten Mal / diesen Monat.** | zum 9,18, dritter Avatar auf dritten 9,30 | „03 / 04“ wie „01 / 04“ im Original |
| Mit Pflegebrücke | Formular kippt hell ein, Stoppuhr-Pille läuft | Pille **• Pflegebrücke** | pflegebrücke 11,25 | Name als Marken-Pille |
| melden Sie die Lücke | Feld „Wann“ springt gefüllt ein und bekommt ein Häkchen, dann „Wer“ | **Lücke melden.** | melden 12,02, „Wer“ auf lücke 12,66 | Knappe Headline, bewusst belassen (siehe oben) |
| in zwei Minuten | Feld „Wo“, **Senden-Klick**, Stoppuhr steht grün auf **1:47** ✓, Toast | **In 2 Minuten.** (blau: 2 Minuten.) | in 13,14, Klick auf minuten 13,47 | Die Stoppuhr beweist die Zahl. |
| Geprüfte Fachkräfte | Drei Profilkarten, Häkchen „Examiniert …“ | **Geprüfte Fachkräfte.** | geprüfte 15,22 | |
| aus Ihrer Region | Kartenfenster, **Umkreis zeichnet sich** bis „Region“, drei Avatare springen in den Kreis | **Aus Ihrer Region.** (blau: Region.), Etikett „12 km Umkreis“ | aus 16,27, Kreis fertig auf region 16,78 | |
| Nach spätestens | Dienstplan wird unscharf (Overlay wie „24/7“) | **spätestens** grau | spätestens 17,79 | nur das gesprochene Wort |
| achtundvierzig Stunden | Riesige blaue Zahl als Ganzes, wächst langsam | **48 Std.** | achtundvierzig 18,49 | keine hochzählende falsche Zahl mehr |
| ist die Schicht besetzt | Overlay weg. Die zwei roten Zeilen werden nacheinander **blau „Besetzt“** mit neuem Avatar, Kopf-Tag „Alle besetzt“. | **Schicht besetzt.** (blau: besetzt.) | schicht 20,04, erste Zeile blau auf besetzt 20,37 | |
| Und Ihr Samstag gehört wieder Ihnen | Figuren, Plaketten: **Sonne auf „Samstag“**, Tasse auf „gehört“, Herz und Häkchen auf „Ihnen“. Die Pille **„• Ihnen.“ leuchtet** auf ihrem Wort blau auf und wächst kurz. | **Ihr Samstag gehört / wieder • Ihnen.** als Ganzes | und 21,07, Aufleuchten auf ihnen 22,77 | Die Pille ist das „• Ship“ des Originals, die Betonung macht das Aufleuchten statt eines Worts. |
| Pflegebrücke Personal | Logo springt, Wortmarke | **Pflegebrücke** + grau **Personal** | pflegebrücke 23,56, personal 24,27 | |
| Melden Sie heute Ihre offene Schicht | Tagline als Ganzes, CTA mit Glow, Mauszeiger fährt ein und **klickt auf „Schicht“**, danach „Schicht gemeldet ✓“ | Tagline, CTA **Schicht melden**, URL/Telefon | melden 25,00, CTA auf heute 25,53, Klick auf schicht 26,36 | Schlussbild des Originals |

## 4. Stummtest
- **Problem:** Plan mit zwei roten „Offen“, Krankmeldung, Anrufe, Lücken überall
- **Ursache und Folge:** Sie selbst springen ein, zum dritten Mal im Monat
- **Lösung:** Lücke melden in 2 Minuten (Formular + 1:47 ✓)
- **Ergebnis:** geprüfte Fachkräfte aus der Region, 48 Std., Schicht besetzt, der Samstag gehört Ihnen
- **Angebot:** Schicht melden

## 5. Korrekturrunde (Textbogen `out/textbogen_teil1/2.jpg`)
1. **Erster Bogen:** Alle Headlines stehen als Ganzes auf ihrem Wort. Es wird nichts mehr getippt, weder in den Feldern noch in der Tagline. „48 Std.“ steht auf „achtundvierzig“, „Schicht besetzt.“ erst auf „Schicht“ und die blauen Zeilen erst auf „besetzt“.
   Schwach war die Betonung von „Ihnen“: Das Aufleuchten der Pille war kaum sichtbar.
2. **Korrektur:** Die Pille wächst jetzt um 10 % (vorher 7 %), Glow und Füllung sind stärker. Danach neu gerendert und geprüft.
- `dichte.py`: Standbild-Anteil 4 %, Bewegung 4,0, Farbigkeit 16,6 (Original 16,5)

## 6. Ton
Partitur unverändert in Klang und Aufbau. Die festen Zeiten sind durch K ersetzt: Samstags-Ticks, Plaketten und Logo-Tap.
Das Tastaturgeklapper ist durch zwei Auswahl-Klicks je Feld ersetzt, weil nichts mehr getippt wird. Der Zähl-Anlauf läuft jetzt von „spätestens“ bis „achtundvierzig“. Danach wird neu gemischt.

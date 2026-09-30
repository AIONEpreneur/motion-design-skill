# REGIE V7 – 08 Quellwerk Office (nach dem Getränkespot „EnergyAI Tropical“, Felipe Borges)

## 1. Wie geht das Original mit Text um?
**Bild-Original.** Im Spot selbst gibt es **keine einzige Einblendung**: keine Überschrift, keine Pille im Bild, kein Satz.
Die ganze Typografie sitzt **auf dem Produkt** (Dosen-Etikett: Marke weiß + türkise Silbe, gelbe Pille „NOVO SABOR“, Pinsel „TROPICAL“).
Betont wird ausschließlich fotografisch: Makro, Push-in, Zeitlupe, Lichthof, Blitzbögen, Neon-Streifen beim Öffnen, Reißschwenk.

Folge für V7:
- Alle V5-Schlagworte fliegen raus („Die Kanne LEER.“, „AUCH LEER.“, „WER SCHLEPPT?“, „Direkt aus der LEITUNG“, „Jede Tasse FRISCH“,
  „OHNE BESTELLUNG!“, „Ihr Team bleibt FRISCH“, „BIS FEIERABEND“, Pillen „15:00 UHR“, „IN DEN 3. STOCK“, „AUF KNOPFDRUCK“, „FRISCH GEMAHLEN“).
- Betonung über die Bildmittel des Originals: **Push-in auf das Detail** (Kamera „schaut hin“), **Aufleuchten/Lichthof**, **Blitzbogen**, **Neon-Streifen**.
- Text nur, wo das Bild allein mehrdeutig ist – als **Einzelwort oder Zahl am Objekt**, in der Etikett-Typografie des Originals
  (gelbe Pille wie „NOVO SABOR“ bzw. weiße runde Grotesk). Das „3. OG“-Schild steht schon **in der Blender-Szene** und bleibt das einzige Wort dort.
- Die Blender-Bildfolgen werden nicht neu gerendert. Jede Einstellung bekommt in `zeiten.py` Zeitanker, damit ihre eingebauten Ereignisse
  (Tropfen, Kasten, Flasche, Kisten, Wasser, Mahlen, Karton, Anstoßen) auf den gemessenen Wörtern liegen (Tempo 0,85–1,2×, Zwischenbilder überblendet).

## 2. Beat für Beat
| Beat | Hervorhebung (Bild) | Text am Objekt | fertig bei Wort (Zeit) | Warum |
|---|---|---|---|---|
| Drei Uhr nachmittags | Makro, Jalousie-Licht, die Kanne kippt | – | – | Uhrzeit ist Stimmung, nicht Aussage. Das Jalousie-Licht reicht. |
| Die Kanne ist leer | Letzter Tropfen fällt, **Push-in** auf den Aufprall | – | Tropfen 2,25, Push-in fertig „leer“ 2,55 | Ein Tropfen aus einer gekippten Kanne ist eindeutig „leer“. |
| Der Wasserkasten | Kasten landet hart | – | Aufprall 3,20 vor „Wasserkasten“ 3,28 | Bild ist eindeutig. |
| auch | Leere Flasche kippt und rollt, **Push-in** auf die Flasche | – | „auch“ 4,06 | Die leere Flasche ist das „auch leer“. |
| Wer schleppt sechs Kisten | Sechs Kisten krachen aufeinander, Kamera fährt am Stapel hoch | **6 Kisten** (weiße Etikett-Schrift) neben dem Stapel | „sechs“ 6,56 | Die Menge ist nicht zählbar (Stapel oben angeschnitten) → Zahl mit Einheit. |
| in den dritten Stock | Schild **3. OG** (in der Szene) **leuchtet auf**, leichter Push-in | (Schild ist Teil des Renderings) | „dritten“ 7,62 | Stockwerk steht schon am Objekt, es braucht nur den Blick darauf. |
| Mit Quellwerk … aus der Leitung | Blatt-Durchflug, Chrom-Hahn; Wasserstrahl **leuchtet auf** und füllt die Flasche | – | „Leitung“ 11,92 | Hahn + Flasche mit Quellwerk-Etikett erzählen es. |
| Gefiltert | Kartusche fliegt in den Wasserkranz, türkiser **Blitzbogen** | Pille **gefiltert** an der Kartusche | „Gefiltert“ 12,85 | Die Kartusche sieht aus wie eine kleine Flasche → ohne Wort mehrdeutig. |
| gekühlt | Eiswürfel **blitzen auf** (Glanzlichter) | – | „gekühlt“ 13,75 | Eis = kalt, eindeutig. |
| sprudelnd | Perlen steigen, zweiter **Blitzbogen** | – | „sprudelnd“ 14,27 | Perlen = Sprudel, eindeutig. |
| auf Knopfdruck | Flasche dreht sich im Wasserkranz (Zeitlupe) | – | – | Produkt-Moment wie die Dose im Original; ein Wort würde nur das Skript wiederholen. |
| Kaffeemaschine mahlt | Bohnenkranz dreht schneller, Bohnen fallen in die Tasse | – | Mahlen auf „mahlt“ 17,95 | Bild ist eindeutig. |
| jede Tasse frisch | Dampf steigt, **Push-in** auf die Tasse | – | „frisch“ 19,16 | Dampf = frisch. |
| alle vier Wochen | Quellwerk-Karton | Pille **4 Wochen** am Karton | „vier“ 22,27 | Intervall ist aus dem Bild nicht ablesbar → Zahl mit Einheit. |
| ohne Bestellung | Klappen springen auf, Kartuschen und Bohnen fliegen, **Neon-Streifen** | – | „ohne“ 23,38 | Der Karton „kommt von selbst“ – das zeigt das Aufspringen. |
| Team bleibt frisch bis Feierabend | Glas und Tasse **stoßen an**, Spritzer, Neon-Streifen; Sonne sinkt | – | Anstoßen „frisch“ 25,65 | Bild ist eindeutig. |
| Schluss | Reißschwenk in den Packshot | **Quellwerk** (Marke) auf „Quellwerk“ 28,03, **OFFICE** auf „Office“ 28,90, Pille **2 Wochen** auf „Zwei“ 29,83, **kostenlos** als Stempel auf „kostenlos“ 30,56, Kontakt | wie links | Logo + Name, Angebot in 2 Elementen, Kontakt. |

**Stummtest:** Problem (leere Kanne, leere Flasche kippt, 6 Kisten bis 3. OG) → Lösung (Hahn füllt Quellwerk-Flasche; Kartusche „gefiltert“, Eis, Perlen)
→ Kaffee (Bohnen, Dampf) → Service (Karton „4 Wochen“ springt auf) → Ergebnis (Anstoßen im Abendlicht) → Angebot (Quellwerk Office, 2 Wochen kostenlos).

## 3. Timing
- Schnitte, Zeitanker, Push-ins, Blitzbögen, Streifen, Reißschwenk und alle Texte kommen aus K (`zeiten.py`), keine festen Sekundenwerte im Film.
- Push-ins und Pillen starten 0,25–0,3 s vor dem Wort und sind auf dem Wortanfang fertig.

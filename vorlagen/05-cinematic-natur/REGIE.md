# REGIE V7 · 05 Sonnenhof Solar („Heliotrope“, Leon Lin)

## Wie geht das Original mit Text um?
**Bild-Original.** „Heliotrope“ ist fast wortlos: Tropfen, Wolkenmeer, Sonnenblumen, Licht als Zeit. Text gibt es nur einmal –
den Titel „HELIOTROPE“ in weit gesperrten Serifen-Versalien **oben links**, klein und ruhig.
Folge für V7: Alle Satzzeilen aus V5 raus. Es bleiben nur **Zahlen mit Einheit am Tropfen** (die Rechnung), **Einzelwörter am
Objekt** (Planung, Anmeldung, Speicher), der **Name** als Titel oben links wie im Original und die Schlusskarte.
Betonung über Bildmittel des Originals und einfache Symbole: Glanzstern, Blitz (= Strom), roter Pfeil ▲ / grüner Pfeil ▼,
Farbwechsel der Zahl, Hinweislinie, Lichtpuls.
Jedes Wort erscheint als Ganzes (0,25 s Einblendung aus der Unschärfe), fertig auf dem Wort.

## Beat für Beat
| Beat | Hervorhebung (Bild) | Text am Objekt | fertig bei Wort (Zeit) | Warum |
|---|---|---|---|---|
| Schon wieder | Tautropfen am Halm in der Blaustunde | – | – | Stimmung; noch nichts zu erklären. |
| Ihre Stromrechnung steigt | Neben dem Tropfen: **Blitz-Symbol** + Betrag; auf „steigt“ zählt er hoch, wird rötlich, **roter Pfeil ▲** | **1.620 €** → **1.790 €** am Tropfen | „Stromrechnung“ 1,40 / „steigt“ 1,85 | Ein Tropfen sagt nicht „Stromkosten“ – Blitz + Euro-Zahl schon. Der Pfeil zeigt die Richtung ohne Wort. |
| Jedes Jahr hunderte Euro mehr | Tropfen schwillt auf jedem Sprung, Zahl blitzt rot | **1.960 €** / **2.080 €** / **2.140 €** | „Jahr“ 3,07 / „hunderte“ 3,68 / „mehr“ 4,24 | „Hunderte Euro mehr“ als Zahlensprünge ist schneller begriffen als der Satz. |
| Dabei scheint die Sonne | Fahrt in den Tropfen → Sonne geht über dem Wolkenmeer auf | – | „Sonne“ 5,83 | Bild ist eindeutig. |
| jeden Tag auf Ihr Dach | Sonne wird Sonnenblume, daneben das Haus, **Glanzstern auf dem leeren Dach** | – | „Dach“ 7,02 | Der Glanzstern (Mittel des Originals) zeigt genau die Stelle. |
| Sonnenhof Solar macht daraus Ihr eigenes Kraftwerk | Zoom in die Blüte, Samen ordnen sich zu Solarzellen, Modul kippt ins Bild | **SONNENHOF SOLAR** oben links (wie „HELIOTROPE“) | „Sonnenhof“ 7,90 | Name ist Pflicht; Zellen aus Samen zeigen „daraus“ – „Kraftwerk“ braucht kein Wort, man sieht die Solarfläche. |
| Planung | Gestrichelte Maßlinien laufen über das Dach | **PLANUNG** über dem Dachfirst | „Planung“ 10,90 | Gestrichelte Linien allein sind mehrdeutig. |
| Montage | 24 Module fliegen ein und rasten ein | – | „Montage“ 11,64 (erstes Modul) | Bild ist eindeutig. |
| Anmeldung | **Lichtpuls** läuft das Kabel entlang zum Strommast, Mast leuchtet auf | **ANMELDUNG** über dem Mast | „Anmeldung“ 12,20 | Ein Puls am Mast ist ohne Wort ein Rätsel; Fachbegriff → ein Wort. |
| alles aus einer Hand | Transporter fährt vor | **SONNENHOF** auf dem Wagen | „alles“ 12,97 | Name am Wagen = eine Firma macht alles. |
| Tagsüber Sonnenstrom | Kamera fährt näher, Lichtteilchen fließen vom Dach ins Haus | – | „Tagsüber“ 14,32 | Fluss ist eindeutig. |
| Speicher bringt ihn in den Abend | Speicher neben der Tür leuchtet auf, Balken füllen sich; Sonnenuntergang, Fenster gehen an, Glühwürmchen | **SPEICHER** mit Hinweislinie | „Speicher“ 16,87 | Das Gerät ist klein und unbekannt – ein Wort mit Linie. |
| Ihre Rechnung sinkt um bis zu 70 % | Tropfen im Morgenlicht wird kleiner, Betrag zählt herunter, **grüner Pfeil ▼** | **2.140 €** → **642 €**, **−70 %** (grün) | „Rechnung“ 19,12 / „sinkt“ 19,56 / „siebzig“ 20,38 | Dieselbe Zahl am selben Objekt wie am Anfang schließt den Bogen; die Prozentzahl ist das Versprechen. |
| Schluss | Fahrt in den Tropfen → Wolkenmeer | **SONNENHOF SOLAR**, **DACH-CHECK KOSTENLOS**, Web · Telefon | „Sonnenhof“ 21,64 / „Check“ 23,44 / „kostenlos“ 24,02 | Name, zwei Wörter Angebot, Kontakt. |

## Stummtest
Blitz + Euro am Tropfen steigt mit rotem Pfeil → Sonne → Sonnenblume, Glanz auf dem leeren Dach → „Sonnenhof Solar“, Samen werden
Solarzellen → Planung, Module, Anmeldung am Mast, Wagen „Sonnenhof“ → Licht fließt ins Haus → „Speicher“ leuchtet, Nacht mit Licht →
Betrag fällt auf 642 €, grüner Pfeil, −70 % → Sonnenhof Solar · Dach-Check kostenlos.

## Timing
Alle Zeiten aus `zeiten.py` (K, Szenenwechsel `K.cut` aus den Wortzeiten). V5 hatte über 20 feste Sekundenwerte
(Szenen, Kamera, Sonnenstand, Speicher) auf alten, bis zu 0,8 s falschen Wortzeiten – alle ersetzt.

## Korrigierte Wortzeiten (Pegelkurve, in vo.json mit "geprueft": "pegel")
Die Werkzeug-Zeiten lagen hier oft **zu spät** (Vokal statt Zischlaut): Stromrechnung 1,34→1,40 · steigt 1,96→1,85 · Jahr 2,92→3,07 ·
hunderte 3,77→3,68 · mehr 4,44→4,24 · Sonne 5,97→5,83 · Dach 7,05→7,02 · Solar 8,48→8,38 · Planung 10,94→10,90 · Haus 15,23→15,36 ·
Sonnenstrom 15,60→15,67 · Speicher 16,91→16,87 · sinkt 19,67→19,56 · siebzig 20,46→20,38 · Prozent 21,06→20,82 · Solar 22,33→22,25 ·
Dach 23,24→23,17 · Check 23,52→23,44 (u. a., insgesamt 45 Wörter geprüft).

## Korrekturrunde (nach dem ersten Textbogen)
1. „SONNENHOF SOLAR“ stand mittig über den gelben Blütenblättern der Heldenblume (verdeckte die Hauptaktion, schwacher Kontrast)
   → nach oben links, wo auch im Original der Titel steht, mit dunklerem Hof.
2. „SPEICHER“ lief bei der Kamerafahrt an den rechten Bildrand → Position begrenzt.
3. „−70 %“ zu klein neben dem Betrag → größer.

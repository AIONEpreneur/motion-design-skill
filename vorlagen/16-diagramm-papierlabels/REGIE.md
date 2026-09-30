# 16 · Wärmewerk Haustechnik – Regie V7 (Text und Timing)

## Wie nutzt das Original Text?
Bild-Original mit Text als Material (LASIK-Explainer, Version A). Zwei Arten von Text:
1. **Etiketten am Objekt** („cornea“, „lens“ mit dünner Führungslinie) – Einzelwörter, direkt am Ding.
2. **Getippte Satzfetzen** in Stapeln oben links („i thought they opened my lens.“, „tick. tick. tick.“).

Der Auftraggeber hasst Getipptes und Sätze. Also: **Etiketten-Optik bleibt** (Papierstreifen, ausgefranste Kante,
Schreibmaschinenschrift klein, Creme auf Blau / Kobalt auf Papier, rote Hand-Ellipsen, rote Schnittlinien),
aber nur **Einzelwörter oder Zahlen am Objekt, als Ganzes aufgeklatscht** (0,2 s), nie getippt.
Die Stapel oben links fallen komplett weg. Die Wort-Texturen („kalt kalt kalt“ in den Räumen, der „wärme“-Bogen)
bleiben: Sie sind Material wie „cornea cornea“ im Original, keine Sätze, man liest sie als Füllung.

## Wortzeiten
`wortzeiten.py` und danach an der Pegelkurve geprüft (in `out/vo.json` mit `"geprueft": "pegel"`):
dreitausendzweihundert 1,62 → **1,57** (Einsatz nach Stille) · jahr 2,98 → **2,95** · kessel 4,31 → **4,25** (k-Verschluss 4,20, Knall 4,25) ·
fünfundzwanzig 5,61 → **5,47** · tagen 15,80 → **15,75** (t-Verschluss 15,70) · stellt 16,50 → **16,64** · den → 16,75 · förderantrag 16,96 → **16,89** ·
zu 18,17 → 18,12 · siebzig 18,38 → **18,30** (s-Zischen) · prozent 18,68 → 18,79 · zuschuss 18,98 → **19,19** (z-Zischen) · warm 20,81 → **20,87** ·
heizkosten 21,45 → **21,40** · drittel 22,73 → **22,87** (d-Verschluss 22,85).
Bestätigt: gasrechnung 0,58 · januar 7,55 · aus 8,06 · kalt 9,10 · wärme 10,76 · wärmepumpe 14,63 · drei 15,48 · danach 20,20 · wärmewerk 24,14 · beratung 25,77 · kostenlos 26,89.

## Beat für Beat
| Beat | Hervorhebung (Bild) | Text am Objekt | fertig bei Wort (Zeit) | Warum |
|---|---|---|---|---|
| Ihre Gasrechnung | Glühender Punkt im Himmel sitzt jetzt in einer **Gasflamme** (Creme-Kontur mit Zunge, kein Tropfen). Darunter schiebt sich eine **Rechnung** (Papierbogen, Blindzeilen) hoch, rote Führungslinie zur Flamme. | – | gasrechnung 0,58 | Flamme + Blatt mit Zeilen = Gasrechnung, das Bild ist eindeutig. Das Wort „gasrechnung“ braucht es nicht. |
| dreitausendzweihundert Euro | Betrag klatscht als Ganzes auf die Rechnung; **rote Hand-Ellipse** umkreist ihn, fertig auf „Euro“ | **3.200 €** (groß, auf der Rechnung) | dreitausendzweihundert 1,57 · Ellipse euro 2,67 | Zahl ist nicht zeichenbar – genau der Fall für eine Zahl am Objekt. Ellipse = ein Blickfang. |
| im Jahr | Kleiner Kobalt-Streifen klebt sich rechts an den Betrag (auf dem Papier, nicht auf dem Himmel – Kontrast) | **/jahr** | jahr 2,95 | Einheit zur Zahl („Zahl mit Einheit“); ohne sie ist 3.200 € mehrdeutig (Monat? einmalig?). |
| Kessel im Keller | Pergament schiebt sich über den Himmel, Querschnitt Haus, Kessel im Keller glüht | **kessel** (Kobalt-Etikett mit Führungslinie) | kessel 4,25 | Ein Kasten im Keller ist ohne Wort nicht als Heizkessel lesbar – Fachbegriff, genau wie „cornea“ im Original. |
| fünfundzwanzig Jahre alt | Prüfplakette klebt sich auf die Kesselfront | **25 jahre** (Creme-Plakette auf dem Kessel) | fünfundzwanzig 5,47 | Alter ist nicht zeichenbar; Zahl mit Einheit direkt am Ding, wie ein echtes Typenschild. |
| Fällt er im Januar aus | **Schnee** aus Schreibmaschinen-Sternchen fällt draußen am Haus | – | januar 7,55 | „Januar“ = Winter; Schnee zeigt das ohne Wort und im Material des Stils (Zeichen als Textur). |
| … aus | Flamme im Kessel erlischt (Glühen weg, Punkt grau), **roter Hand-Kreis** um den Kessel | – | aus 8,06 | Ausfall ist ein Bildereignis; Kreis = Signal statt Wort. V5-Durchstreichen im Satz entfällt. |
| wird Ihr Haus kalt | Räume füllen sich blau mit „kalt kalt kalt“ | – (Wort-Textur) | kalt 9,10 | Stil des Originals (Material aus seinem Wort), kein Satz. |
| Dabei steckt draußen Wärme | Fahrt in den Garten, Bogen aus „wärme“ zeichnet sich über den Garten, rote Hand-Ellipse auf dem Bogen | – (Wort-Textur) | wärme 10,76 | Unsichtbares (Umweltwärme) wird durch die Wort-Textur sichtbar – das ist der Kern des Stils. |
| Sogar bei minus zehn Grad | Thermometer erscheint, Quecksilber **fällt** tief; Schnee fällt weiter | **−10 °c** am Thermometer | minus 11,81 | Zahl mit Einheit am Messgerät; Schnee + Wärme gleichzeitig ist die Überraschung. |
| Wärmewerk baut Ihre Wärmepumpe | Halbton-Rahmen, Wärmepumpe senkt sich am Seil, Lüfter dreht | **wärmewerk** (Typenschild oben auf dem Gerät) | wärmewerk 13,46 (Schild), Aufsetzen auf wärmepumpe 14,63 | Name am Objekt beantwortet „wer“; das Gerät selbst ist eindeutig, kein Wort „wärmepumpe“ nötig. |
| in drei Tagen | Alter Kessel hebt sich heraus, Speicher kommt; **drei rote Häkchen** zeichnen sich nacheinander | **3 tage** (Streifen an der Leitung) | drei 15,48 | Dauer ist nicht zeichenbar → Zahl mit Einheit; drei Häkchen zählen die Tage mit (Ping pro Häkchen). |
| stellt den Förderantrag | Formular fliegt ein, Blindzeilen (nichts getippt) | **förderantrag** (Kopfzeile des Formulars) | förderantrag 16,89 | Ein leeres Formular ist mehrdeutig; der Name des Dokuments steht dort, wo er auch in echt steht. |
| bis zu siebzig Prozent Zuschuss | **Roter Stempel** knallt aufs Formular | **70 %** im Stempel | siebzig 18,30 | Zahl mit Einheit; der Stempel ist die Hervorhebung. „Zuschuss“ fällt weg: Formular + Stempel sagen „bewilligt“. |
| Danach ist es warm | Zurück zum Haus, Räume füllen sich rot mit „warm warm“, Leitungen fließen, Schnee hört auf | – (Wort-Textur) | warm 20,87 | Spiegel zu „kalt“ – sofort lesbar. |
| Ihre Heizkosten | Kosten-Säule (Kobalt, in drei Teile gegliedert) wächst neben dem Haus | **heizkosten** am Säulenfuß | heizkosten 21,40 | Eine Säule ohne Beschriftung wäre irgendein Balken; das Wort macht sie eindeutig. |
| sinken um ein Drittel | Rote gestrichelte **Schnittlinie** zieht quer (wie im Original), oberes Drittel kippt weg | **−1/3** an der Schnittlinie | Schnitt auf sinken 22,11, Zahl auf drittel 22,87 | Schnitt zeigt „weniger“, die Zahl zeigt „wie viel“. |
| Wärmewerk Haustechnik | Himmel, glühendes Haus | **wärmewerk** groß + **haustechnik** klein, als Ganzes | wärmewerk 24,14 | Name als Ganzes. |
| Kontakt | – | **0711 204 33 90 · waermewerk.de** | nach haustechnik (25,1) | Kontakt bleibt bis zum Ende stehen. |
| Die Beratung vor Ort ist kostenlos | Zwei Streifen, rote Hand-Ellipse um „kostenlos“ | **beratung** · **kostenlos** | beratung 25,77 · kostenlos 26,89 | Angebot in 2 Wörtern, jedes landet auf seinem Wort. |

Entfällt aus V5: „ihre gasrechnung:“, „jeden monat.“, „und es wird mehr.“ (nie gesprochen), alle vier Stapel oben links,
getippte Formularzeilen („antragsteller: ihr name“ …), „zuschuss“ im Stempel, „heizkosten: 3.200 € / neu: 2.130 € (−1/3)“.
Alle Schreibmaschinen-Anschläge im Ton entfallen; pro Etikett ein Aufklatsch-Geräusch.

## Stummtest
Flamme + Rechnung 3.200 €/jahr (Problem) → alter Kessel, 25 jahre, Schnee, Kessel aus, Haus „kalt“ (Ursache) →
draußen „wärme“ trotz −10 °c, Wärmepumpe von wärmewerk, 3 tage, Förderantrag mit 70 %-Stempel (Lösung) →
Haus „warm“, Heizkosten −1/3 (Ergebnis) → wärmewerk haustechnik, beratung kostenlos, Kontakt (Angebot).

## Korrekturrunde (nach Textbogen 1)
- „/jahr“ saß halb auf dem blauen Himmel (Kobalt auf Kobalt, kaum lesbar) → ganz aufs Papier gerückt, Betrag etwas kleiner.
- Die Flammen-Kontur las sich als Wassertropfen → echte Flammenform mit seitlicher Zunge und innerer Flamme, auch das Icon auf der Rechnung.
- Etiketten waren zu klein für Handy (kessel, 25 jahre, wärmewerk, 3 tage, heizkosten) → 20–30 % größer; Schnee-Sternchen größer, damit sie als Flocken lesbar sind.
- Plakette „25 jahre“ saß am unteren Bildrand → auf die obere Kesselhälfte.

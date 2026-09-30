# REGIE V7 – 09 Klarwerk Reinigung (nach dem Nomad-Werbespot, Fernando Araujo)

## 1. Wie geht das Original mit Text um?
**Teilweise Typografie-Original.** Nomad arbeitet mit genau drei Textsorten:
1. **Headline-Karten** auf Creme: 3–4 Wörter mit Punkt („Abra sua conta global.“, „Pague como um local.“), Endkarte „Conta para o mundo.“
2. **Kennzahl rechts neben dem Telefon**: kleines Label mit Farbpunkt + große Zahl + segmentierte Linie („Saldo em euro · € 704,25“).
3. **Echte App-Oberfläche** im Telefon (kleiner UI-Text, Mitteilungen) – Text am Objekt.
Die Lifestyle-Fotos haben **keinen** Text.

Folge für V7:
- Die Headline-Karte **bleibt** (Stil des Originals): „Montag, 8 Uhr.“ – exakt die gesprochenen Wörter, **als Ganzes** (nicht mehr Wort für Wort nachgeschoben),
  fertig auf „Montag“, steht bis zum Schnitt.
- Kennzahlen **bleiben** als Zahl + Label (Label = gesprochenes Wort): „9:00“ / „Wichtigster Kunde“, „289 €“ / „Festpreis“, „1/6 … 6/6“ / „Räume fertig“.
  Die kleinen Satz-Unterzeilen („in 57 Minuten · Küche?“, „pro Monat · 2× pro Woche“, „heute Abend · jeder mit Foto“) fliegen raus.
- Der Festpreis **zählt nicht mehr hoch** – er „steht sofort da“: im Telefon und rechts gleichzeitig, fertig auf „Festpreis“.
- UI-Text im Telefon bleibt (er ist das Objekt).
- Lifestyle-Bilder ohne Text; Betonung über **Push-in** auf das Detail (die Kamerasprache der Lifestyle-Fotos im Original).
- Endkarte: Balken-Logo + Wortmarke, Angebot in 2 Wörtern **„Erstreinigung geschenkt.“** (Headline-Stil des Originals, Punkt am Ende),
  „Erstreinigung“ landet auf „erste“, „geschenkt.“ auf „schenken“, dann Kontakt. Der 6-Wort-Satz aus V5 fliegt raus.

## 2. Beat für Beat
| Beat | Hervorhebung (Bild) | Text | fertig bei Wort (Zeit) | Warum |
|---|---|---|---|---|
| Montag, acht Uhr | Headline-Karte auf Creme | **Montag, 8 Uhr.** (ganz) | „Montag“ 0,30 | Wie die Headline-Karten des Originals; Zeitpunkt ist aus keinem Bild ablesbar. |
| Der Boden klebt | Küche in warmem Licht, **Push-in auf die Flecken** am Boden | – | „klebt“ 2,55 | Flecken sind sichtbar, der Push-in sagt „da“. |
| die Küche quillt über | Geschirrberg, **Push-in** | – | „quillt“ 3,85 | Bild ist eindeutig. |
| Um neun kommt Ihr wichtigster Kunde | Telefon fährt hoch, Mitteilung „9:00 · Brandt GmbH“ fällt ein | **9:00** groß rechts; Label **Wichtigster Kunde** | „neun“ 5,25 / „wichtigster“ 6,22; Linie füllt sich bis „Kunde“ 6,82 | Uhrzeit = Zahl, Label = gesprochenes Wort, Format des Originals. |
| In einer Minute per App buchen | App: Mauszeiger wählt „Büro“ (Klick auf „Reinigung“), „Weiter“ | nur UI | Klick „Reinigung“ 9,33 | Die Bedienung zeigt es. |
| Fläche eingeben, Rhythmus wählen | „180 m²“ wird getippt (UI), Klick „2× / Woche“ | nur UI | „Fläche“ 11,86 / „wählen“ 13,37 | UI am Objekt. |
| Der Festpreis steht sofort da | Preis im Telefon und rechts **gleichzeitig ganz** da, Linie voll, „✓ Gebucht“ | **289 €** / Label **Festpreis** | „Festpreis“ 14,13; Klick „sofort“ 15,13 | „sofort“ = kein Hochzählen. |
| Abends kommt immer dasselbe Team | Reinigungswagen am Abend, **Push-in auf die Namensschilder** Aylin / Marek | (Schilder im Rendering) | „dasselbe“ 17,47 | Dieselben Namen = dasselbe Team, ohne Satz. |
| Jeder fertige Raum als Häkchen mit Foto | Mitteilungen fallen ein (je Raum ✓ + Foto), **Push-in auf den Stapel** ab „Häkchen“ | **1/6 … 6/6** / Label **Räume fertig** | 1. Raum „Jeder“+0,25; 3/6 auf „Häkchen“ 20,37; 4/6 auf „Foto“ 21,05; 5/6 auf „Handy“ 21,89 | Zahl zählt mit den Mitteilungen; der Push-in macht Häkchen und Foto lesbar. |
| Am Morgen glänzt alles | Glänzende Küche, Glanzlichter blitzen | – | „glänzt“ 23,57 | Bild ist eindeutig. |
| Der Kunde kann kommen | **Push-in auf das Kärtchen „Frisch gereinigt“** auf der Arbeitsplatte | (Kärtchen im Rendering) | „Kunde“ 24,77 | Übergabe-Moment, ohne Satz. |
| Schluss | Gelbe Fläche, Balken fügen sich zum K, Wortmarke gleitet heraus | **KLARWERK** / Reinigung, **Erstreinigung geschenkt.**, Kontakt | „Klarwerk“ 26,43 / „Reinigung“ 26,90 / „erste“ 27,92 / „schenken“ 28,87 | Logo + Name + Angebot in 2 Wörtern + Kontakt. |

**Stummtest:** Montag 8 Uhr, dreckige Küche → 9:00 wichtigster Kunde (Problem + Druck) → App: Büro, 180 m², 2×/Woche, 289 € Festpreis, gebucht (Lösung)
→ abends dasselbe Team (Namensschilder) → 6/6 Räume fertig mit Foto → Küche glänzt, „Frisch gereinigt“ (Ergebnis) → Erstreinigung geschenkt (Angebot).

## 3. Timing
Alle Schnitte (`K.cut`), Mitteilungen (`K.pings`), Mauszeiger-Wege, Klicks, Push-ins und Texte aus K (`zeiten.py`), keine festen Sekundenwerte.
Die Lifestyle-Bildfolgen (Blender) werden nicht neu gerendert; die Morgen-Einstellung läuft auf 0,86× gedehnt mit überblendeten Zwischenbildern.

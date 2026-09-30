# 17 · Stadtbote Kurier – Regie V7 (Text und Timing)

## Wie nutzt das Original Text?
Bild-Original (Andy Diep „Saratoga“, animierte historische Karte). Text gibt es dort in drei Formen:
1. **Titelkarte** „Saratoga“ mit Kicker und kursiver Frage – der Titel ist ein **Ortsname**.
2. **Kartuschen-Zeile** unten links mit einem ganzen Satz pro Beat („Three armies meet at Albany.“).
3. **Beschriftung an der Karte**: Ortsnamen in gesperrten Versalien, Heeresnamen kursiv rot an der Route.

Folge für uns: Die Kartusche ist genau der mitlaufende Satz, den der Auftraggeber hasst → **fällt komplett weg**.
Es bleibt nur Nr. 3: **Ortsnamen, Namen und Zahlen direkt an der Karte**, ruhig eingeblendet (nie getippt).
Die Titelkarte „Heute noch / beim Kunden“ war ein Satzstück, frei schwebend → weg; die Frist zeigt die Taschenuhr
mit roter Restzeit. Der Titelstil bleibt nur für den **Namen** am Schluss („Stadtbote“), dort ist er richtig.

## Wortzeiten
`wortzeiten.py`, danach an der Pegelkurve geprüft (in `out/vo.json` mit `"geprueft": "pegel"`):
vertrag 0,56 → **0,49** (v-Zischen 0,50) · heute 1,09 → **1,28** (ss von „muss“ bis 1,27) · weg 3,65 → **3,77** (g-Verschluss 3,75) ·
post 5,18 → **4,84** (p-Verschluss 4,825 – Abweichung 0,34 s) · zweimal 8,37 → 8,32 · direkt 11,09 → **10,89** (Verschluss nach „fährt“) ·
sechzig 12,42 → **12,32** (s-Zischen) · stadt 14,20 → **14,09** · umweg 15,26 → **15,04** · vier 16,49 → **16,35** (f-Zischen) ·
vertrag 17,18 → **17,07** · da 17,88 → **17,57** (Abweichung 0,31 s) · beleg 19,85 → **19,72** · ihnen 21,25 → 21,20 ·
Stadtbote (Schluss) 22,13 → **22,30** (Stille bis 22,28) · zugestellt 25,29 → **25,09**.
Bestätigt: kunden 1,80 · sonst 2,73 · übermorgen 6,23 · verteilzentrum 7,41 · abgeholt 11,75 · quer 13,43 · halb 16,15 · mit 18,12 ·
unterschrift 18,32 · foto 19,36 · kurier 23,00 · rufen 26,27 · holen 27,42 · sofort 27,71.
Alle ~70 festen Sekundenwerte im Film (Kamera-Stützpunkte, Kurierfahrt, Karten-Aufdecken, Ein-/Ausblendungen) sind jetzt aus K abgeleitet.

## Beat für Beat
| Beat | Hervorhebung (Bild) | Text am Objekt | fertig bei Wort (Zeit) | Warum |
|---|---|---|---|---|
| Ihr Vertrag | Vertrag zeichnet sich, rotes Wachssiegel | **VERTRAG** (Kopf des Dokuments) | vertrag 0,49 | Ein Blatt mit Zeilen ist irgendein Papier; das Wort steht dort, wo es auf einem echten Vertrag steht. |
| muss heute noch | Taschenuhr, **roter Restzeit-Sektor** läuft auf XII zu, Ticken | – | heute 1,28 | Frist = Bild. Der alte Titel „Heute noch“ war ein Satzstück. |
| beim Kunden | Karte deckt sich vom Kunden aus auf, **roter Zielring** | **KUNDE** (Ortsname am Ring) | kunden 1,80 | Wer das Ziel ist, sieht man nicht am Ring allein → Name am Ort, wie „ALBANY“. |
| Sonst ist der Auftrag weg | Rotes Auftrags-Kästchen am Kunden, auf „weg“ **Tintenstrich** quer darüber, Kästchen blasst aus | **Auftrag** (rot, am Kästchen) | auftrag 3,24 · Strich weg 3,77 | „48.000 €“ aus V5 wurde nie gesprochen → nur das gesprochene Wort. |
| Mit der Post? | Blaue Post-Einheit am Büro, blauer Federstrich startet | **Post** (am Block) · **BÜRO** (Ortsname) | post 4,84 | Blau vs. Rot braucht einen Namen, sonst ist unklar, wer die blaue Linie fährt. |
| Frühestens übermorgen | Blaue Route schlingert weit über Land und kommt spät an, **Tintenklecks** am Kunden | **+2 Tage** (blau, am Ziel) | übermorgen 6,23 | Dauer ist nicht zeichenbar → Zahl mit Einheit am Ort des Schadens. |
| Über das Verteilzentrum, zweimal umgeladen | Zoom ins Verteilzentrum, Paket springt über das Förderband, zwei rote Bögen | **VERTEILZENTRUM** (Ortsname) · **I** · **II** (an den Bögen) | I auf verteilzentrum 7,41 · II auf zweimal 8,32 | Die römischen Ziffern zählen das Umladen mit – Zahl statt Satz. |
| Der Stadtbote fährt direkt | Post-Umweg zieht sich zurück, bleibt als blasse gestrichelte Geisterlinie; **roter Pinselstrich** Büro → Kunde | **Stadtbote** (rot, an der Einheit) · **9 km** (an der roten Route) · **140 km** blau, rot durchgestrichen (am Umweg) | Stadtbote 9,91 · Route fertig auf direkt 10,89 | Der Vergleich 9 km gegen 140 km ist der Kern; Durchstreichen statt Wort. |
| Abgeholt in sechzig Minuten | Kurier fährt ans Büro, Stoppuhr, **roter Sektor** füllt sich | **60 min** (unter der Stoppuhr) | abgeholt 11,75 · Zahl auf sechzig 12,32 | Zahl mit Einheit am Messgerät. |
| quer durch die Stadt, ohne Umweg | Kamera folgt dem Kurier über den Fluss, Geisterlinie verblasst auf „ohne“ | – | quer 13,43 · ohne 14,77 | Das Bild ist die Aussage. |
| Um halb vier ist Ihr Vertrag da | Kurier erreicht den Ring, **Zielring pulsiert** | **15:30** (mit Führungslinie zum Ring) | halb 16,15 · Puls auf da 17,57 | Uhrzeit ist nicht zeichenbar → Zahl am Ort. „UHR · ZUGESTELLT“ aus V5 entfällt. |
| mit Unterschrift und Foto als Beleg | Beleg-Blatt (nur Tuschezeilen), Unterschrift schreibt sich, Foto der Haustür mit Fotoecken, **roter Stempel mit Häkchen** | – | unterschrift 18,32 · foto 19,36 · Stempel beleg 19,72 | Alle Formularwörter aus V5 (ZUSTELLNACHWEIS, Sendung, Empfänger, FOTO AN DER TÜR, Ringtext) entfallen – Unterschrift, Foto und Häkchen sind eindeutig. |
| Der Auftrag gehört Ihnen | Auftrags-Kästchen kehrt zurück, **rotes Häkchen**, rote Fläche wächst um den Kunden | **Auftrag** (dasselbe Kästchen wie am Anfang) | auftrag 20,48 · Häkchen ihnen 21,20 | Rückbezug auf das verlorene Kästchen: jetzt gewonnen. |
| Stadtbote Kurier | Titelkarte wie „Saratoga“, Kompassrose, roter Pinselstrich unter dem Namen | **Stadtbote** groß · **KURIER** klein | Stadtbote 22,30 · Kurier 23,00 | Name = hier ist der Titelstil des Originals richtig. |
| Heute bestellt, heute zugestellt | – | **heute zugestellt** (rot, unter dem Namen) | zugestellt 25,09 | Angebot in 2 Wörtern, als Ganzes. „Heute bestellt.“ entfällt (4-Wort-Slogan wäre ein Satz). |
| Rufen Sie an, wir holen sofort ab | Kontakt-Kartusche mit Doppelrahmen; auf „sofort“ **roter Federstrich** unter der Nummer | **0621 480 27 90** · **STADTBOTE-KURIER.DE** | rufen 26,27 · Strich sofort 27,71 | Kontakt; „RUFEN SIE AN“ und „Wir holen sofort ab.“ entfallen, „sofort“ wird Bildmittel. |

Weiter als Kartentextur, klein und blass: ALTSTADT, WESTSTADT, NORDSTADT, OSTSTADT, SÜDSTADT, HAFEN, STADTPARK, STADT – Ortsnamen gehören
zur Karte wie im Original, sie tragen keine Aussage.

## Stummtest
Vertrag + Uhr mit roter Restzeit (Frist) → Ziel KUNDE, Auftrag wird mit Tinte durchgestrichen (Problem) →
blaue Post über VERTEILZENTRUM, I, II, +2 Tage, Klecks (Ursache) → roter Stadtbote direkt, 9 km statt 140 km, 60 min (Lösung) →
15:30 am Ziel, Beleg mit Unterschrift, Foto, Häkchen-Stempel, Auftrag mit Häkchen (Ergebnis) → Stadtbote Kurier, heute zugestellt, Telefon (Angebot).

## Korrekturrunde (nach Textbogen 1)
- „140 km“ saß am Umweg weit im Westen und war in der Stadtansicht nie im Bild → an die Stelle der Geisterlinie gesetzt,
  die zwischen Fluss und Kunde sichtbar ist; der rote Strich zieht sich jetzt auf „direkt“ (10,89) durch die Zahl.
- Schlüssel-Beschriftungen (Auftrag, Post, Stadtbote, 9 km, +2 Tage, BÜRO, KUNDE) waren im Übersichtsmaßstab zu klein → 25–35 % größer.
- Standbild-Anteil lag bei 20 % (Grenze) wegen der langen Schlusskarte → Kamerafahrt auf der Schlusskarte doppelt so weit.

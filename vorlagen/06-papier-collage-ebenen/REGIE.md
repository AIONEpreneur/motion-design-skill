# REGIE V7 · 06 Pfotenhaus („Moon Festival“, Ring Hyacinth)

## Wie geht das Original mit Text um?
**Bild-Original.** Die Papiercollage erzählt ohne Worte. Betont wird über **Papierzeichen**: „?“ und „!“ über dem Katzenkopf,
rotes **X**, Walzen, die auf einem Symbol einrasten, der Mond mit dem fehlenden Stück. Schrift gibt es nur einmal: die goldene
Kalligrafie im Schlussbild.
Folge für V7: Alle sechs Satz-Papierstreifen aus V5 raus (auch die Schrift auf dem Ticket und „Gute Nacht“ auf dem Polaroid).
Es bleiben Namen am Objekt (Türschilder, Goldschrift „Pfotenhaus“), Papierzeichen des Originals (?, X) plus Häkchen und ein
Pfoten-Schild als Symbol, und zwei Einzelwörter Angebot im Schlussbild.

## Beat für Beat
| Beat | Hervorhebung (Bild) | Text am Objekt | fertig bei Wort (Zeit) | Warum |
|---|---|---|---|---|
| Ihr Urlaub ist gebucht | Koffer schiebt sich hoch, Katze sitzt drin, Flugticket fliegt an und klebt; **grünes Häkchen** auf dem Ticket | – | „Urlaub“ 0,76 (Ticket) / „gebucht“ 1,34 (Häkchen) | Koffer + Ticket = Urlaub, Häkchen = gebucht. Ticket-Schrift „Bremen → Meer · Sitz 14A“ entfernt (Satzstück, niemand liest es). |
| aber wohin mit der Katze? | Katze macht große Augen, **„?“** und zweites **„?“** poppen | – | „wohin“ 2,35 / „Katze“ 3,04 | Papierzeichen des Originals; Frage ohne Satz. |
| Die Nachbarin | Ältere Nachbarin vor ihrer Tür, eigener Koffer | Türschild **Nachbarin** (vergrößert) | „Nachbarin“ 4,20 | Wer die Figur ist, sagt das Schild an ihrer Tür. |
| hat keine Zeit | **Uhr** poppt, dann **rotes X** | – | „keine“ 5,19 / „Zeit“ 5,49 | Uhr + X = keine Zeit. (In V5 fehlte die Uhr: Zeitwert war nicht definiert.) |
| Fremde Leute in Ihrer Wohnung? | Kamerafahrt zur eigenen Tür: dunkle Gestalt mit Schlüssel, Katze faucht | Türschild **Ihre Wohnung** | „Wohnung“ 7,52 (Fauchen fertig) | Das Schild macht klar, dass es die eigene Tür ist. |
| Lieber nicht. | **Rotes X**, Schlüssel fliegt weg, Gestalt geht | – | „nicht“ 8,54 | Klare Absage im Bild. |
| Im Pfotenhaus | Drei Walzen rasten auf das **Pfoten-Haus** ein, die mittlere genau auf dem Wort, Goldschrift erscheint | **Pfotenhaus** (Gold, wie die Kalligrafie des Originals) | „Pfotenhaus“ 9,74 | Name ist Pflicht; Walzen sind das Mittel des Originals. |
| wohnt sie im eigenen Zimmer | Zimmer mit Fenster auf Bremen; **Pfoten-Schild** poppt an der Wand | – | „Zimmer“ 11,66 | Symbol „Pfote an der Tür/Wand“ = ihr eigenes Zimmer, ohne Wort. |
| mit Fensterplatz | Katze springt aufs Fensterkissen, rollt sich ein | – | „Fensterplatz“ 12,20 (Landung) | Bild ist eindeutig. |
| Morgens und abends frisches Futter | Scheibe dreht Sonne → Mond, Futter rieselt in den Napf | – | „Morgens“ 13,47 / „abends“ 14,17 / „Futter“ 15,03 | Sonne/Mond + Napf sagen alles. |
| dazwischen Spielen und Kuscheln | Spielmaus, Katze springt; Hand streichelt, Herzchen | – | „Spielen“ 16,37 / „Kuscheln“ 17,14 | Bild ist eindeutig. |
| Jeden Abend ein Foto aufs Handy | **Kamerablitz**, Polaroid (Katze schläft, Mond, Herz) fliegt zu Ihnen ans Meer, Handy leuchtet mit der Katze | – | Blitz „Abend“ 18,59 / „Foto“ 19,57 / „Handy“ 20,09 | Blitz + Polaroid + Handy = Foto aufs Handy. |
| So genießen Sie Ihren Urlaub – und Ihre Katze auch | Senkrechter Riss: Sie am Meer | Katze am Fenster; das fehlende **Mondstück rastet ein**, Mond leuchtet auf | – | „so“ 21,35 (Riss) / „auch“ 23,55 (Mond voll) | Der volle Mond ist das Bild für „beide glücklich“ – Rückgriff aufs Original. |
| Schluss | Katze von hinten vor dem vollen Mond, Laternen auf der Weser | **Pfotenhaus** (Gold), Papierstreifen **Kennenlernen** und **kostenlos**, Web · Telefon | „Pfotenhaus“ 24,60 / „Kennenlernen“ 25,89 / „kostenlos“ 26,76 | Name, zwei Wörter Angebot, Kontakt. |

## Stummtest
Koffer + Ticket ✓ → Katze „??“ → Nachbarin: Uhr, X → Fremder an „Ihre Wohnung“, Katze faucht, X → Walzen: Pfotenhaus →
eigenes Zimmer (Pfoten-Schild), Fensterplatz, Sonne/Mond, Futter, Spielen, Kuscheln → Blitz, Foto aufs Handy am Meer →
beide unter dem vollen Mond → Pfotenhaus · Kennenlernen kostenlos.

## Timing
Alle Zeiten aus `zeiten.py` (K). Szenenwechsel `K.cut` in den Sprechpausen, Walzenstopps `K.stops`, Blitz `K.blitz`.
Ersetzt: Szenenplan, Koffer-Einfahrt, Blinzeln, Kamerafahrt im Flur, Tür-Einblendung, Walzenstart, Zimmer-Zoom, Schluss-Zoom,
Kontaktzeile (alles vorher feste Sekunden). Die X-Stempel sind jetzt auf dem Wort fertig (vorher 0,02 s danach).

## Korrigierte Wortzeiten (Pegelkurve, in vo.json mit "geprueft": "pegel")
Katze 3,12→3,04 · Nachbarin 4,26→4,20 · Pfotenhaus 9,66→9,74 · wohnt 10,36→10,57 · Fensterplatz 12,31→12,20 · Futter 15,15→15,03 ·
Spielen 16,59→16,37 · Kuscheln 17,24→17,14 · Foto 19,72→19,57 · Handy 20,18→20,09 · Katze 23,14→23,09 · Kennenlernen 25,83→25,89
(u. a., 30 Wörter geprüft; „mit“ und „ein“ wegen Reihenfolge nachgezogen).

## Korrekturrunde (nach dem ersten Prüfbogen)
1. Türschilder „Nachbarin“ / „Ihre Wohnung“ waren mit 24 px kaum lesbar → 36 px, Schild passt sich der Wortlänge an.
2. „eigenes Zimmer“ war nur ein leeres Zimmer → Pfoten-Schild an der Wand poppt auf „Zimmer“.

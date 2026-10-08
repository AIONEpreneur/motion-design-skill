# Motion Design Skill für Claude Code

Ein Skill, mit dem Claude Code dir ein fertiges **30-Sekunden-Erklärvideo (16:9)** für deine Firma, dein Produkt oder deine Dienstleistung baut, mit Stimme, Musik und Animation. Ganz ohne KI-Videomodelle: Jedes Bild ist Code, den Claude selbst schreibt.

Du sagst einfach:

> Ich brauche ein Erklärvideo für meine Firma.

Dann läuft es so ab:
1. **Interview:** Claude stellt dir vier Fragen: Was verkaufst du? Wer ist dein Kunde? Welches Problem hat er? Was soll er am Ende tun?
2. **Stilwahl:** Du bekommst drei passende Stile aus einer Bibliothek mit 22 erprobten Stilen zur Auswahl, jeweils mit Beispielvideo.
3. **Text:** Claude schreibt Sprechertext und Ablauf und zeigt sie dir zur Freigabe.
4. **Stimme:** Du hörst drei Stimmproben von ElevenLabs, auf Wunsch auch mit deiner eigenen, geklonten Stimme, und wählst eine aus.
5. **Bauen:** Claude baut das Video, prüft es Bild für Bild und liefert es dir fertig aus.

## Voraussetzungen

- [Claude Code](https://claude.com/claude-code). Der Skill rendert Videos lokal, deshalb läuft er nicht in der claude.ai-Web-App.
- Mac, Linux oder Windows mit:
  - Node.js 20+
  - Python 3 mit numpy, soundfile und Pillow
  - ffmpeg
  - whisper.cpp mit dem Modell `large-v3-turbo`, für die Wortzeiten
  - Chrome oder chrome-headless-shell, zum Rendern
- Ein **ElevenLabs-Konto mit API-Schlüssel** für die Stimmen. Für kommerzielle Nutzung und für Stimmen aus der ElevenLabs-Bibliothek brauchst du einen bezahlten Tarif. ElevenLabs rechnet nach Zeichen ab: Ein 30-Sekunden-Skript hat rund 500–600 Zeichen, mit Hörproben und Wiederholungen braucht ein Video ein paar tausend.
- Optional ein **kie.ai-Schlüssel** als Ausweichweg (Google Gemini, ein paar Cent pro Video).

## Installation

```bash
git clone https://github.com/AIONEpreneur/motion-design-skill ~/.claude/skills/erklaervideo
cd ~/.claude/skills/erklaervideo/werkzeuge && npm install
python3 pruefen.py
```

`pruefen.py` zeigt dir, was noch fehlt, und nennt für jeden Punkt den passenden Befehl. Auf dem Mac sind das in der Regel diese:

```bash
brew install ffmpeg whisper-cpp
python3 -m pip install numpy soundfile pillow
mkdir -p ~/.cache/whisper && curl -L -o ~/.cache/whisper/ggml-large-v3-turbo.bin https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin
npx @puppeteer/browsers install chrome-headless-shell@stable --path ~/.cache/puppeteer
```

Den ElevenLabs-Schlüssel (elevenlabs.io → Developers → API Keys) trägst du in `~/.claude/settings.json` ein:

```json
{ "env": { "ELEVENLABS_API_KEY": "dein-schlüssel" } }
```

Weitere Einträge sind optional:

| Eintrag | Wirkung |
|---|---|
| `ELEVENLABS_STIMMEN` | feste Stimmen für die Hörproben, Komma-Liste aus Namen oder Voice-IDs, z. B. `"Meine Stimme,<voice-id>,<voice-id>"`. Ohne den Eintrag sucht Claude jedes Mal drei passende deutsche Stimmen aus der Bibliothek. |
| `ELEVENLABS_MODELL` | anderes Modell als `eleven_v3` |
| `KIE_API_KEY` | Ausweichweg über kie.ai (`--anbieter kie`) |

**Eigene Stimme:** Klon deine Stimme in ElevenLabs. Danach steht sie unter ihrem Namen in `python3 werkzeuge/elevenlabs.py stimmen` und Claude schlägt sie bei den Hörproben immer mit vor.

## Benutzung

Öffne Claude Code in einem Ordner, in dem die Videos landen sollen, und sag: „Ich brauche ein Erklärvideo für meine Firma.“ Jedes Projekt bekommt dort einen eigenen Unterordner in `erklaervideos/`.

## Was drin ist

| Ordner | Inhalt |
|---|---|
| `SKILL.md`, `references/` | Ablauf, Regeln und die 22 Stilkarten |
| `vorlagen/` | technische Vorlage je Stil (Film-Code, Tonspur, Zeitsteuerung) |
| `beispiele/` | ein kurzes Beispielvideo je Stil |
| `werkzeuge/` | Renderer, Stimme (ElevenLabs, kie.ai als Ausweichweg), Wortzeiten, Pegelprüfung, Musik, Mix, Selbstprüfung |
| `scripts/` | Projekt anlegen, Stimmproben |

## Hinweise

- **Schriften:** Drei Stile (10, 12 und 18) nutzen auf dem Mac Systemschriften: SF, DIN und Comic Sans bzw. Superclarendon. Die liegen dort schon vor, deshalb stecken sie nicht im Paket. Auf anderen Systemen springt automatisch eine freie Ersatzschrift ein, die Stile sehen dort also leicht anders aus.
- Lizenzen von Schriften und Bibliotheken: siehe [DRITTANBIETER.md](DRITTANBIETER.md).

## Lizenz

MIT, siehe [LICENSE](LICENSE).

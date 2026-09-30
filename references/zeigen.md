# Stilvorschläge und Hörproben abspielbar zeigen

Videos und Audio zeigst du immer auf einer Artifact-Seite mit Player, nie als lose Datei.

## Stilvorschläge (3 Videos)
Die 22 Beispielvideos liegen im Skill unter `beispiele/<nr>.mp4` (Pfad auch in `stile/katalog.json` unter `video`).

1. **Seite anlegen:** eine kleine HTML-Seite „Stilwahl – <Firma>“ schreiben und einmal mit `capabilities: {"assets": {}}` veröffentlichen.
2. **Videos hochladen:** die drei Beispielvideos in den Projektordner kopieren (der Upload nimmt nur Dateien aus dem Arbeitsordner) und mit Artifact `publish`, `url` = neue Seite, `asset: true`, `file_paths` hochladen. Nur die zurückgegebenen Adressen verwenden.
3. **Seite aufbauen:** pro Stil ein `<video controls preload="metadata" playsinline>`, darunter die Nummer, der Name und die Begründung in einem Satz.
4. **Neu veröffentlichen und verlinken.** Dann per Auswahlfrage wählen lassen.

Ohne Artifact-Werkzeug (z. B. im Terminal ohne claude.ai-Anbindung): dieselbe Seite als `stilwahl.html` in den Projektordner schreiben, die Videos daneben legen und die Datei im Browser öffnen (`open stilwahl.html` bzw. `xdg-open`/`start`).

## Hörproben (3 Audios)
Ohne Artifact-Werkzeug gilt dasselbe wie oben: lokale HTML-Seite mit `<audio controls>` im Projektordner öffnen.

1. **Proben erzeugen:** `stimmproben.py` legt `probe_<Stimme>.mp4` ab. Das ist AAC im MP4-Container. `.m4a` nimmt der Asset-Upload nicht an.
2. **Hochladen:** alle drei mit `asset: true` und `file_paths` hochladen. Die Dateien müssen dafür im Arbeitsverzeichnis liegen, also im Projektordner.
3. **Seite aufbauen:** pro Stimme Name, Charakter und `<audio controls preload="none">`.
4. **Veröffentlichen und verlinken,** dann wählen lassen.

## Fertiges Video
- Die Web-Fassung (< 14 MB) mit `asset: true` in die Projektseite hochladen.
- Eine Seite mit Player und Firmennamen veröffentlichen und den Link geben.

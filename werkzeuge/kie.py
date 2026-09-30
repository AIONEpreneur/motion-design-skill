#!/usr/bin/env python3
"""kie.ai-Client mit Kostenvoranschlag.

Nur Standardbibliothek, kein pip.

    export KIE_API_KEY=...

    # Was würde das kosten? (kein Aufruf an kie.ai, keine Credits)
    python3 kie.py preis grok-imagine/image-to-video --sekunden 8 --stufe 720p
    python3 kie.py preis gpt-image-2-text-to-image --anzahl 6 --stufe 1K

    # Erzeugen (verbraucht Credits)
    python3 kie.py run <modell> '<input-json>' <zieldatei>

    # Datei hochladen, gibt die URL aus (kostenlos, hält 3 Tage)
    python3 kie.py upload <datei> [zielordner]

    # Guthaben
    python3 kie.py guthaben
"""
import json, os, sys, time, urllib.error, urllib.request

BASE = "https://api.kie.ai/api/v1"
USD_PRO_CREDIT = 0.005
EUR_PRO_USD = 1 / 1.1542          # Stand 6.8.2026

# Credits je Einheit. "s" = pro Sekunde, "stk" = pro Stück, "clip" = pro Clip.
PREISE = {
    "gpt-image-2-text-to-image":  {"art": "stk", "1K": 6, "2K": 10, "4K": 16},
    "gpt-image-2-image-to-image": {"art": "stk", "1K": 6, "2K": 10, "4K": 16},
    "nano-banana-2":              {"art": "stk", "1K": 8, "2K": 12, "4K": 18},
    "nano-banana-2-lite":         {"art": "stk", "1K": 4},
    # Achtung: heißt bei kie.ai "nano-banana-pro", nicht "google/nano-banana-pro".
    # Feld für Eingangsbilder ist image_input (nicht image_urls).
    "nano-banana-pro":            {"art": "stk", "1K": 18, "2K": 18, "4K": 24},
    "google/nano-banana-edit":    {"art": "stk", "1K": 4},
    "seedream-5-pro":             {"art": "stk", "1K": 7, "2K": 14},
    "grok-imagine/image-to-video":{"art": "s",   "480p": 2.4, "720p": 4.5, "1080p": 8},
    "bytedance/seedance-1.5-pro": {"art": "s",   "720p": 3.5, "1080p": 7.5},
    "kling-3-0":                  {"art": "s",   "720p": 14, "1080p": 18},
    "bytedance/seedance-2":       {"art": "s",   "720p": 41, "1080p": 102},
    # 2.5 kann nur 480p/720p. Real gemessen am 8.8.2026:
    # 720p 1216 cr/16 s = 76 cr/s · 480p 408 cr/8 s = 51 cr/s.
    "bytedance/seedance-2-5":     {"art": "s",   "480p": 51, "720p": 76},
    "veo3.1":                     {"art": "clip","lite-1080p": 35, "fast-1080p": 65,
                                   "quality-1080p": 255},
    "google/gemini-2-5-pro-tts":  {"art": "stk", "1K": 4},
    # Stand 23.9.2026 (kie.ai/pricing). GPT Image 2.5 = Platz 1 arena.ai Text-to-Image.
    "gpt-image-2-5-sunburst-text-to-image":  {"art": "stk", "1K": 6, "2K": 10, "4K": 16},
    "gpt-image-2-5-sunburst-image-to-image": {"art": "stk", "1K": 6, "2K": 10, "4K": 16},
    "gpt-image-2-5-flare-text-to-image":     {"art": "stk", "1K": 6, "2K": 10, "4K": 16},
    "gpt-image-2-5-flare-image-to-image":    {"art": "stk", "1K": 6, "2K": 10, "4K": 16},
    # MiniMax H3 = Platz 1 arena.ai Image-to-Video; first_frame_url + last_frame_url, 4-15 s
    "minimax-h3/image-to-video":  {"art": "s",   "2K": 13, "768P": 8},
    "minimax-h3/text-to-video":   {"art": "s",   "2K": 13, "768P": 8},
}


def preis(modell, stufe=None, sekunden=0, anzahl=1):
    """Credits + Euro für einen geplanten Lauf. Löst keinen Aufruf aus."""
    if modell not in PREISE:
        raise SystemExit(f"Unbekanntes Modell: {modell}\n"
                         f"Bekannt: {', '.join(sorted(PREISE))}")
    p = dict(PREISE[modell]); art = p.pop("art")
    stufe = stufe or next(iter(p))
    if stufe not in p:
        raise SystemExit(f"Unbekannte Stufe {stufe} für {modell}. "
                         f"Möglich: {', '.join(p)}")
    satz = p[stufe]
    cr = satz * (sekunden if art == "s" else 1) * anzahl
    return cr, cr * USD_PRO_CREDIT * EUR_PRO_USD


def _req(url, method="GET", body=None):
    key = os.environ.get("KIE_API_KEY", "").strip()
    if not key:
        raise SystemExit("KIE_API_KEY fehlt. export KIE_API_KEY=...")
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer " + key)
    req.add_header("Content-Type", "application/json")
    # Ohne das blockt Cloudflare den Upload-Host mit 403/1010.
    req.add_header("User-Agent", "curl/8.7.1")
    for versuch in range(5):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            txt = e.read().decode()
            if e.code in (429, 500, 502, 503) and versuch < 4:
                time.sleep(3 * (versuch + 1)); continue
            raise RuntimeError(f"HTTP {e.code}: {txt}")
        except urllib.error.URLError:
            if versuch < 4:
                time.sleep(3 * (versuch + 1)); continue
            raise
    raise RuntimeError("Anfrage nach fünf Versuchen fehlgeschlagen")


def guthaben():
    return _req(f"{BASE}/chat/credit").get("data")


MIMETYPEN = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
             ".webp": "image/webp", ".mp4": "video/mp4", ".mov": "video/quicktime",
             ".wav": "audio/wav", ".mp3": "audio/mpeg"}


def upload(pfad, ordner="uploads"):
    """Lädt eine Datei hoch und gibt die öffentliche URL zurück.

    Nötig für alle Felder, die URLs erwarten (reference_image_urls,
    reference_video_urls, image_urls ...). Kostet keine Credits.
    Die URL verfällt nach drei Tagen.
    """
    import base64
    endung = os.path.splitext(pfad)[1].lower()
    mime = MIMETYPEN.get(endung, "application/octet-stream")
    roh = open(pfad, "rb").read()
    if len(roh) > 10 * 1024 * 1024:
        raise SystemExit(f"{pfad} ist {len(roh)/1e6:.1f} MB — über dem 10-MB-Limit "
                         f"des base64-Uploads.")
    daten = "data:%s;base64,%s" % (mime, base64.b64encode(roh).decode())
    # Achtung: nicht api.kie.ai — der Upload läuft über einen eigenen Host.
    r = _req("https://kieai.redpandaai.co/api/file-base64-upload", "POST",
             {"base64Data": daten, "uploadPath": ordner,
              "fileName": os.path.basename(pfad)})
    if not r.get("success", r.get("code") == 200):
        raise RuntimeError(f"Upload fehlgeschlagen: {r}")
    d = r.get("data") or {}
    return d.get("downloadUrl") or d.get("fileUrl")


def notiz_schreiben(ziel, modell, eingabe, credits):
    """Schreibt meta.json neben die Datei — Grundlage der Galerie."""
    import datetime
    ordner = os.path.dirname(os.path.abspath(ziel)) or "."
    pfad = os.path.join(ordner, "meta.json")
    eintraege = []
    if os.path.exists(pfad):
        try: eintraege = json.load(open(pfad))
        except Exception: eintraege = []
    endung = os.path.splitext(ziel)[1].lower()
    typ = ("video" if endung in (".mp4", ".mov", ".webm")
           else "audio" if endung in (".wav", ".mp3", ".m4a") else "bild")
    cr = credits or 0
    eintraege.append({
        "zeit": datetime.datetime.now().isoformat(timespec="seconds"),
        "datei": os.path.basename(ziel),
        "typ": typ,
        "modell": modell,
        "prompt": (eingabe.get("prompt") or "")[:600],
        "credits": cr,
        "eur": round(cr * USD_PRO_CREDIT * EUR_PRO_USD, 4),
        "eingabe": {k: v for k, v in eingabe.items() if k != "prompt"},
    })
    json.dump(eintraege, open(pfad, "w"), ensure_ascii=False, indent=1)


def run(modell, eingabe, ziel=None, timeout=900):
    """Auftrag anlegen, warten, Ergebnis herunterladen, protokollieren."""
    r = _req(f"{BASE}/jobs/createTask", "POST", {"model": modell, "input": eingabe})
    if r.get("code") != 200:
        raise RuntimeError(f"createTask fehlgeschlagen: {r}")
    tid = r["data"]["taskId"]
    print(f"    Auftrag {tid}", file=sys.stderr)
    start, letzter = time.time(), None
    while time.time() - start < timeout:
        d = _req(f"{BASE}/jobs/recordInfo?taskId={tid}").get("data", {})
        s = d.get("state")
        if s != letzter:
            print(f"    Status: {s}", file=sys.stderr); letzter = s
        if s == "success":
            urls = (json.loads(d.get("resultJson") or "{}")).get("resultUrls") or []
            cr = d.get("creditsConsumed")
            print(f"    fertig, {cr} Credits", file=sys.stderr)
            if ziel and urls:
                req = urllib.request.Request(urls[0], headers={"User-Agent": "curl/8"})
                with urllib.request.urlopen(req, timeout=180) as q, open(ziel, "wb") as f:
                    f.write(q.read())
                print(f"    gespeichert: {ziel}", file=sys.stderr)
                notiz_schreiben(ziel, modell, eingabe, cr)
            return {"taskId": tid, "urls": urls, "credits": cr}
        if s == "fail":
            raise RuntimeError(f"fehlgeschlagen: {d.get('failMsg') or d.get('failCode')}")
        time.sleep(8)
    raise TimeoutError(f"Zeitüberschreitung bei {tid}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    befehl = sys.argv[1]

    if befehl == "preis":
        args = sys.argv[2:]
        modell = args[0]
        opt = {args[i].lstrip("-"): args[i + 1] for i in range(1, len(args) - 1, 2)}
        cr, eur = preis(modell, opt.get("stufe"),
                        float(opt.get("sekunden", 0)), int(opt.get("anzahl", 1)))
        print(f"{cr:g} Credits · {eur:.3f} €".replace(".", ","))

    elif befehl == "guthaben":
        print(guthaben())

    elif befehl == "upload":
        print(upload(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "uploads"))

    elif befehl == "run":
        print(json.dumps(run(sys.argv[2], json.loads(sys.argv[3]),
                             sys.argv[4] if len(sys.argv) > 4 else None)))
    else:
        raise SystemExit(__doc__)

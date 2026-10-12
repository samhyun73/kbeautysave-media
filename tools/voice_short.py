"""Voice Short: spec JSON -> 9:16 Short with Typecast narration, stock footage (Pixabay / Coverr),
word-by-word captions, v2 "rice mist & celadon" overlays, synthesized BGM ducked under the voice, -14 LUFS.

usage:
  python3 tools/voice_short.py voices <outdir>                          # Typecast voice list + 4 sample mp3s
  python3 tools/voice_short.py candidates specs/<file>.json <outdir>    # stock clips per scene -> candidates.jpg/.json
  python3 tools/voice_short.py render specs/<file>.json <outdir>        # -> <slug>.mp4, cover.png, shots.jpg, credits.txt
  add --mock to any of them for an offline test (silent voice, test-pattern clips)

Env: TYPECAST_API_KEY, PIXABAY_API_KEY, optional COVERR_API_KEY, optional TYPECAST_VOICE_ID (spec "voice_id" wins).
Pexels stopped issuing API keys (2026-10), so it is not used. Coverr requires attribution: meta.json "attribution"
lists it, and the post copy must then carry "🎥 Stock footage: Coverr".
These APIs are not reachable from the Claude workspace; real runs happen in .github/workflows/voice-short.yml.

Spec (specs/YYYY-MM-DD-<slug>-voice.json):
  {"type": "voice_short", "slug": "...", "lang": "en", "hangul": "그라데이션 립", "headline": "...",
   "mood": "bright", "seed": 5, "voice_id": "", "tempo": 1.1,
   "scenes": [{"say": "spoken line", "label": "optional pill", "query": ["stock search", "..."], "clips": ["pb123", "px456"]}],
   "cta": {"line": "Shop the K-beauty picks", "main": "Link in my profile"}}
  The last scene shows the profile card. No discount code or link in the video or its description (decision 2026-10-12). "clips" pins footage (ids from candidates.json); empty = top search hits.
"""
import base64, hashlib, json, os, re, shutil, subprocess, sys, time, urllib.parse, urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / ".cache" / "voice"
W, H, FPS = 1080, 1920, 30
SHOT, T = 3.0, 0.4             # target shot length, crossfade (s)
LEAD, TAIL, HOLD = 0.15, 0.3, 1.2
C = dict(rice=(238, 240, 234), pine=(30, 43, 39), celadon=(157, 189, 176), deep=(63, 107, 94),
         blush=(242, 201, 190), mist=(201, 214, 208), muted=(79, 95, 90))
UA = {"User-Agent": "kbeautysave-voice-short/1.0"}
MOCK = "--mock" in sys.argv
# Voice rotation (user decision 2026-10-12: a different voice each Short). Spec "voice_id" wins; otherwise the
# voice comes from the spec's position among specs/voice/*.json, so it is stable for re-renders of the same Short.
VOICES = [("tc_692799c46508f6b9468c54c7", "Daeun"), ("tc_6aa23da1f9559d89ed550d7e", "Krista"),
          ("tc_6a7446c19f2d7dfed990a900", "Eunkyung"), ("tc_69f2e455ea79fd197aa0476f", "Seohyeon")]
SAMPLE = "Here's the Korean way to make your lip tint last all day, step by step."


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"command failed: {' '.join(map(str, cmd))[:300]}\n{r.stderr[-1500:]}")
    return r.stdout


def probe(p):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]).strip())


def font(size, weight="Bold"):
    for w in ([weight] if weight == "Regular" else [weight, "Black", "Bold", "Regular"]):
        for d in ("/usr/share/fonts/opentype/noto", "/usr/share/fonts/opentype/noto-cjk", "/usr/share/fonts/truetype/noto"):
            p = Path(d) / f"NotoSansCJK-{w}.ttc"
            if p.exists():
                return ImageFont.truetype(str(p), size, index=1)   # index 1 = KR
    raise SystemExit("Noto Sans CJK not found (apt install fonts-noto-cjk)")


def http_json(url, data=None, headers=None, timeout=120):
    req = urllib.request.Request(url, data=json.dumps(data).encode() if data is not None else None,
                                 headers={**UA, "Content-Type": "application/json", **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def download(url, dest):
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300) as r, open(f"{dest}.part", "wb") as f:
            shutil.copyfileobj(r, f)
        os.replace(f"{dest}.part", dest)
    return dest


# ------------------------------------------------------------------ voice ----
def tts(text, voice, tempo=1.0):
    """(mp3 path, duration, [(word, start, end)]) — cached by voice + tempo + text."""
    h = hashlib.sha1(f"{voice}|{tempo}|{text}".encode()).hexdigest()[:12]
    d = CACHE / ("tts-mock" if MOCK else "tts")
    mp3, meta = d / f"{h}.mp3", d / f"{h}.json"
    if mp3.exists() and meta.exists():
        m = json.loads(meta.read_text())
        return mp3, m["duration"], m["words"]
    d.mkdir(parents=True, exist_ok=True)
    if MOCK:
        words, t = [], 0.1
        for w in text.split():
            dur = 0.16 + 0.045 * len(w)
            words.append((w, round(t, 3), round(t + dur, 3)))
            t += dur + (0.25 if w[-1] in ".?!" else 0.08 if w[-1] in ",:" else 0.03)
        dur = t + 0.1
        run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono",
             "-t", f"{dur:.3f}", "-c:a", "libmp3lame", str(mp3)])
    else:
        body = {"voice_id": voice, "text": text, "model": "ssfm-v30", "language": "eng",
                "prompt": {"emotion_type": "smart"}, "output": {"audio_format": "mp3", "audio_tempo": tempo}}
        url = "https://api.typecast.ai/v1/text-to-speech/with-timestamps?granularity=word"
        hdr = {"X-API-KEY": os.environ["TYPECAST_API_KEY"]}
        try:
            res = http_json(url, body, hdr)
        except urllib.error.HTTPError as e:
            if e.code not in (400, 422):
                raise SystemExit(f"Typecast error {e.code}: {e.read()[:300]!r}")
            body.pop("prompt")
            res = http_json(url, body, hdr)
        mp3.write_bytes(base64.b64decode(res["audio"]))
        dur = float(res.get("audio_duration") or probe(mp3))
        words = [(w["text"], float(w["start"]), float(w["end"])) for w in res.get("words") or [] if w.get("text", "").strip()]
        if not words:
            toks = text.split()
            words = [(w, dur * i / len(toks), dur * (i + 1) / len(toks)) for i, w in enumerate(toks)]
    meta.write_text(json.dumps({"duration": dur, "words": words}))
    return mp3, dur, words


def voices(outdir):
    """List English Typecast voices, rank young/adult female conversational ones first, render 4 samples."""
    outdir.mkdir(parents=True, exist_ok=True)
    if MOCK:
        vs = [{"voice_id": f"mock{i}", "voice_name": f"Mock {i}", "gender": "female"} for i in range(4)]
    else:
        res = http_json("https://api.typecast.ai/v3/voices?model=ssfm-v30", headers={"X-API-KEY": os.environ["TYPECAST_API_KEY"]})
        vs = res if isinstance(res, list) else res.get("voices") or res.get("items") or []

    def score(v):
        s = json.dumps(v).lower()
        return (("female" in s) * 3 + ("young_adult" in s) * 3 + ("conversational" in s or "vlog" in s or "beauty" in s) * 2
                + ("bright" in s or "cheerful" in s or "friendly" in s) * 1
                - ("child" in s or "elder" in s or "game" in s or "anime" in s or "news" in s) * 5)
    vs.sort(key=score, reverse=True)
    (outdir / "voices.json").write_text(json.dumps(vs, indent=1, ensure_ascii=False))
    lines = []
    for i, v in enumerate(vs[:4]):
        mp3, _, _ = tts(SAMPLE, v["voice_id"])
        shutil.copy(mp3, outdir / f"voice{i + 1}.mp3")
        lines.append(f"voice{i + 1}.mp3  {v['voice_id']}  {v.get('voice_name')}  {v.get('gender')}  {v.get('age')}  {v.get('use_cases')}")
    (outdir / "voices.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


# ---------------------------------------------------------------- footage ----
def _cached(name, url, headers=None, max_age=None):
    p = CACHE / "search" / (re.sub(r"[^a-z0-9]+", "-", name.lower())[:120] + ".json")
    if p.exists() and (max_age is None or time.time() - p.stat().st_mtime < max_age):
        return json.loads(p.read_text())
    res = http_json(url, headers=headers, timeout=60)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(res))
    return res


def _pixabay(h):
    vs = h.get("videos", {})
    f = next((vs[k] for k in ("large", "medium", "small") if vs.get(k, {}).get("url")
              and min(vs[k].get("width", 0), vs[k].get("height", 0)) >= 720), None)
    if not f:
        return None
    thumb = f.get("thumbnail") or next((vs[k].get("thumbnail") for k in ("small", "tiny", "medium") if vs.get(k, {}).get("thumbnail")), None)
    return {"id": f"pb{h['id']}", "duration": float(h.get("duration", 0)), "link": f["url"], "w": f["width"], "h": f["height"],
            "credit": f"{h.get('user', 'Pixabay')} (Pixabay)", "url": h.get("pageURL"), "tags": h.get("tags", ""), "thumb": thumb}


COVERR = "https://api.coverr.co"
COVERR_AGE = 7 * 86400   # Coverr video URLs carry a token: don't trust older search results


def _coverr_get(name, path):
    """Coverr call (cached); None on any error so Coverr can never break a run."""
    key = os.environ.get("COVERR_API_KEY")
    if not key:
        return None
    try:
        return _cached(name, COVERR + path, {"Authorization": f"Bearer {key}"}, COVERR_AGE)
    except Exception as e:  # noqa: BLE001
        print(f"  Coverr call failed ({str(e)[:100]})")
        return None


def _coverr(v):
    link = (v.get("urls") or {}).get("mp4") if isinstance(v, dict) else None
    try:
        width = int(v.get("max_width") or 0)
    except (TypeError, ValueError, AttributeError):
        width = 0
    if not link or not v.get("id") or width < 720:
        return None
    vert = bool(v.get("is_vertical"))
    tags = v.get("tags") or []
    return {"id": f"cv{v['id']}", "duration": float(v.get("duration") or 0), "link": link,
            "w": 1080 if vert else 1920, "h": 1920 if vert else 1080, "credit": "Coverr", "url": None,
            "tags": ", ".join(map(str, [v.get("title", "")] + (tags if isinstance(tags, list) else [tags]))),
            "thumb": v.get("thumbnail") or v.get("poster")}


def coverr_ping(cid):
    """Coverr asks API users to report downloads. Best effort."""
    key = os.environ.get("COVERR_API_KEY")
    if MOCK or not key or not cid.startswith("cv"):
        return
    try:
        req = urllib.request.Request(f"{COVERR}/videos/{cid[2:]}/stats/downloads", method="PATCH",
                                     headers={**UA, "Authorization": f"Bearer {key}"})
        urllib.request.urlopen(req, timeout=30).close()
    except Exception as e:  # noqa: BLE001
        print(f"  Coverr download ping failed ({str(e)[:80]})")


# Footage must look on-topic and brand-safe: tags need a beauty word and never a blocked one.
BEAUTY = {"lip", "lips", "lipstick", "makeup", "cosmetics", "cosmetic", "beauty", "skincare", "facial", "moisturizer",
          "lotion", "serum", "nail", "nails", "manicure", "hair", "haircare", "hairstyle", "blush", "foundation", "mascara",
          "eyeshadow", "lipgloss", "spa"}
BLOCK = {"cigarette", "smoking", "smoke", "tobacco", "nicotine", "alcohol", "cocktail", "beer", "wine", "drink", "bar",
         "sexy", "sensual", "hot", "lingerie", "bikini", "nude", "drug", "drugs", "blood", "gun", "weapon", "halloween",
         "zombie", "horror", "food", "meal"}
STOP = {"close", "up", "closeup", "applying", "apply", "woman", "women", "girl", "with", "the", "a", "an", "of", "and",
        "on", "in", "mirror", "finger", "fingers", "flat", "lay", "collection", "products", "product"}


def on_topic(c, query):
    tags = set(re.findall(r"[a-z]+", (c.get("tags") or "").lower()))
    return not (tags & BLOCK) and bool(tags & BEAUTY)


def interleave(lists):
    out, seen = [], set()
    for k in range(max(map(len, lists), default=0)):
        for lst in lists:
            if k < len(lst) and lst[k]["id"] not in seen:
                seen.add(lst[k]["id"]); out.append(lst[k])
    return out


def scene_pool(sc):
    """On-topic clips for a scene: per query, Pixabay and Coverr alternate (portrait first); queries alternate too."""
    per_query = []
    for q in sc.get("query", []):
        hits = [c for c in search(q) if MOCK or on_topic(c, q)]
        per_query.append(interleave([[c for c in hits if c["id"].startswith(p)] for p in ("pb", "cv", "mock")]))
    return interleave(per_query)


def search(query):
    """Stock clips for a query, vertical ones first."""
    if MOCK:
        n = int(hashlib.sha1(query.encode()).hexdigest()[:4], 16)
        return [{"id": f"mock{(n + i) % 97}", "duration": 12.0, "link": "", "w": 1080 if i % 2 == 0 else 1920,
                 "h": 1920 if i % 2 == 0 else 1080, "credit": "mock", "url": "", "tags": query, "thumb": None} for i in range(6)]
    out = []
    if os.environ.get("PIXABAY_API_KEY"):
        res = _cached("pixabay-" + query, "https://pixabay.com/api/videos/?" + urllib.parse.urlencode(
            {"key": os.environ["PIXABAY_API_KEY"], "q": query[:100], "video_type": "film", "safesearch": "true", "per_page": 60}))
        out += [c for c in map(_pixabay, res.get("hits", [])) if c]
    res = _coverr_get("coverr-" + query, "/videos?" + urllib.parse.urlencode({"query": query[:100], "page_size": 30, "urls": "true"}))
    hits = res.get("hits") if isinstance(res, dict) else None
    if res is not None and not isinstance(hits, list):
        print(f"  Coverr: unexpected response shape {list(res)[:8] if isinstance(res, dict) else type(res).__name__}")
    cv = [c for c in map(_coverr, hits if isinstance(hits, list) else []) if c]
    print(f"  search '{query}': {len(out)} Pixabay, {len(cv)} Coverr" + ("" if os.environ.get("COVERR_API_KEY") else " (no Coverr key)"))
    out += cv
    return sorted(out, key=lambda c: c["h"] <= c["w"])   # stable: portrait first, search order kept


def clip_by_id(cid):
    if MOCK or cid.startswith("mock"):
        return {"id": cid, "duration": 12.0, "link": "", "w": 1080 if int(re.sub(r"\D", "", cid) or 0) % 2 == 0 else 1920,
                "h": 1920 if int(re.sub(r"\D", "", cid) or 0) % 2 == 0 else 1080, "credit": "mock", "url": "", "tags": "", "thumb": None}
    if cid.startswith("pb"):
        res = _cached("pixabay-id-" + cid, "https://pixabay.com/api/videos/?" + urllib.parse.urlencode(
            {"key": os.environ["PIXABAY_API_KEY"], "id": cid[2:]}))
        c = _pixabay((res.get("hits") or [{}])[0]) if res.get("hits") else None
    else:
        c = _coverr(_coverr_get("coverr-id-" + cid, f"/videos/{cid[2:]}?urls=true") or {})
    if not c:
        raise SystemExit(f"clip {cid} not found or too small")
    return c


def clip_file(c):
    if MOCK or c["id"].startswith("mock"):
        p = CACHE / "mock" / f"{c['id']}.mp4"
        if not p.exists():
            p.parent.mkdir(parents=True, exist_ok=True)
            hue = int(re.sub(r"\D", "", c["id"]) or 0) * 37 % 360
            run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", f"testsrc2=size={c['w']}x{c['h']}:rate=30,hue=h={hue}",
                 "-t", "12", "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", str(p)])
        return p
    dest = CACHE / "clips" / f"{c['id']}-{c['w']}x{c['h']}.mp4"
    new = not dest.exists()
    download(c["link"], dest)
    if new:
        coverr_ping(c["id"])
    return dest


def candidates(spec, outdir):
    """Per scene up to 8 unique clips -> candidates.json + candidates.jpg (one row per scene, ids under thumbs)."""
    outdir.mkdir(parents=True, exist_ok=True)
    seen, rows = set(), []
    for i, sc in enumerate(spec["scenes"]):
        got = [c for c in scene_pool(sc) if c["id"] not in seen][:8]
        seen.update(c["id"] for c in got)
        rows.append(got)
        print(f"scene {i + 1}: {len(got)} on-topic clips ({sum(c['id'].startswith('cv') for c in got)} Coverr)")
    (outdir / "candidates.json").write_text(json.dumps(rows, indent=1, ensure_ascii=False))
    tw, th, head = 230, 300, 64
    sheet = Image.new("RGB", (tw * 8 + 20, len(rows) * (th + head + 40) + 20), C["rice"])
    d = ImageDraw.Draw(sheet)
    f, fs = font(26), font(20, "Regular")
    for i, (sc, got) in enumerate(zip(spec["scenes"], rows)):
        y = 10 + i * (th + head + 40)
        d.text((14, y + 8), f"Scene {i + 1}: {sc['say'][:110]}", font=f, fill=C["pine"])
        for k, c in enumerate(got):
            x = 10 + k * tw
            box = Image.new("RGB", (tw - 10, th), C["mist"])
            try:
                if c.get("thumb"):
                    im = Image.open(download(c["thumb"], CACHE / "thumbs" / f"{c['id']}.jpg")).convert("RGB")
                else:
                    p = CACHE / "thumbs" / f"{c['id']}.png"
                    p.parent.mkdir(parents=True, exist_ok=True)
                    run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "1", "-i", str(clip_file(c)), "-frames:v", "1", str(p)])
                    im = Image.open(p).convert("RGB")
                im.thumbnail((tw - 10, th))
                box.paste(im, ((tw - 10 - im.width) // 2, (th - im.height) // 2))
            except Exception as e:  # noqa: BLE001 - a missing thumbnail must not stop the sheet
                print("thumb failed", c["id"], e)
            sheet.paste(box, (x, y + head))
            d.text((x, y + head + th + 4), f"{c['id']} {'V' if c['h'] > c['w'] else 'H'} {c['duration']:.0f}s", font=fs, fill=C["deep"])
    sheet.save(outdir / "candidates.jpg", quality=85)
    print(f"candidates: {sum(map(len, rows))} clips in {len(rows)} scenes -> {outdir}/candidates.jpg")


# --------------------------------------------------------------- overlays ----
def rounded(d, box, r, fill):
    d.rounded_rectangle(box, r, fill=fill)


def wrap(d, text, f, width):
    lines, cur = [], ""
    for w in text.split():
        t = f"{cur} {w}".strip()
        if d.textlength(t, font=f) <= width or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    return lines + [cur] if cur else lines


def _band(d, spec):
    """Headline band geometry -> (lines, top, bottom, font)."""
    f, lh, pad, top = font(62), 80, 30, 270
    lines = wrap(d, spec["headline"], f, W - 120 - 2 * 56)
    return lines, top, top + 2 * pad + len(lines) * lh, f, lh, pad


def overlay_static(spec, path):
    """Shown for the whole video (no fades, so nothing flickers at cuts): bottom shade for captions, hangul
    watermark on the left, centred headline band and the centred hangul pill under it."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    shade = Image.new("L", (1, 760))
    for y in range(760):
        shade.putpixel((0, y), int(185 * (y / 759) ** 1.5))
    img.paste(Image.new("RGBA", (W, 760), C["pine"] + (255,)), (0, H - 760), shade.resize((W, 760)))
    hg = spec["hangul"].replace(" ", "")
    size = min(150, int(600 / max(1, len(hg))))
    wm = font(size, "Black")
    for k, ch in enumerate(hg):
        d.text((48, 700 + k * size), ch, font=wm, fill=C["rice"] + (70,))
    lines, top, bottom, f, lh, pad = _band(d, spec)
    rounded(d, (60, top, W - 60, bottom), 32, C["pine"] + (232,))
    for k, ln in enumerate(lines):   # anchor "mm" = each line centred on its own slot
        d.text((W // 2, top + pad + k * lh + lh // 2), ln, font=f, fill=C["rice"], anchor="mm")
    _pill(d, spec["hangul"], C["celadon"], bottom + 22)
    img.save(path)


def _pill(d, text, col, y, ph=66):
    pf = font(38)
    pw = d.textlength(text, font=pf) + 64
    x = (W - pw) / 2
    rounded(d, (x, y, x + pw, y + ph), ph // 2, col + (245,))
    d.text((W / 2, y + ph / 2), text, font=pf, fill=C["pine"], anchor="mm")


def overlay(spec, sc, path, last):
    """Per scene: the step label pill (centred, on its own row under the hangul pill) and, on the last scene, the
    profile card (no code or link in the video, user decision 2026-10-12)."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    _, _, bottom, _, _, _ = _band(d, spec)
    if sc.get("label"):
        _pill(d, sc["label"], C["blush"], bottom + 22 + 66 + 14)
    if last:
        cta = spec.get("cta") or {}
        box = (140, 860, W - 140, 1150)
        rounded(d, box, 40, C["rice"] + (246,))
        cx = W // 2
        d.text((cx, 920), cta.get("line", "Shop the K-beauty picks"), font=font(44), fill=C["deep"], anchor="mm")
        main, size = cta.get("main", "Link in my profile"), 84
        while d.textlength(main, font=font(size, "Black")) > box[2] - box[0] - 80:
            size -= 4
        d.text((cx, 1010), main, font=font(size, "Black"), fill=C["pine"], anchor="mm")
        d.text((cx, 1100), "#oliveyoungaffiliate #ad", font=font(32, "Regular"), fill=C["muted"], anchor="mm")
    img.save(path)


# --------------------------------------------------------------- captions ----
def ass_time(t):
    cs = int(round(t * 100))
    return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"


def captions(timed, path):
    """Short word groups; the word being spoken is blush and slightly larger (style of the dog-channel Shorts)."""
    words = []
    for w, s, e in timed:
        if words and re.fullmatch(r"[^\w]+", w):
            words[-1] = (words[-1][0] + w, words[-1][1], e)
        else:
            words.append((w, s, e))
    events, cur = [], []
    for i, (w, s, e) in enumerate(words):
        cur.append((w, s, e))
        nxt = words[i + 1] if i + 1 < len(words) else None
        text = " ".join(x[0] for x in cur)
        if w[-1] in ".?!" or len(text) >= 16 or not nxt or nxt[1] - e > 0.6 or (w[-1] in ",:;" and len(text) >= 10):
            events.append([cur[0][1], cur[-1][2], list(cur)]); cur = []
    for a, b in zip(events, events[1:]):
        if b[0] - a[1] < 0.35:
            a[1] = b[0]
    clean = lambda t: t.replace("{", "(").replace("}", ")")  # noqa: E731
    body = ""
    for s, e, ws in events:
        for i, (w, ws_, _) in enumerate(ws):
            a, b = (s if i == 0 else ws_), (ws[i + 1][1] if i + 1 < len(ws) else e)
            parts = [f"{{\\c&H00BEC9F2&\\fscx108\\fscy108}}{clean(w2)}{{\\r}}" if j == i else clean(w2) for j, (w2, _, _) in enumerate(ws)]
            pop = "{\\fad(60,0)}" if i == 0 else ""
            body += f"Dialogue: 0,{ass_time(a)},{ass_time(b)},Cap,,0,0,0,,{pop}{' '.join(parts)}\n"
    path.write_text(f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Noto Sans CJK KR,88,&H00FFFFFF,&H00FFFFFF,&H00272B1E,&H96000000,1,0,0,0,100,100,0,0,1,6,1,2,90,90,560,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
{body}""")


# ----------------------------------------------------------------- render ----
def shot(clip, L, path):
    """Normalise one clip to a 1080x1920 shot of length L: portrait = slow pan crop, landscape = over a blurred copy."""
    start = max(0.0, min(1.0, (clip["duration"] - L) / 3)) if clip["duration"] > L else 0.0
    loop = ["-stream_loop", "-1"] if clip["duration"] < L + start else []
    if clip["h"] > clip["w"]:
        frame = f"scale={W + 80}:-2,crop={W}:{H}:x='(iw-ow)*t/{L:.3f}':y='(ih-oh)/2'"
    else:
        frame = (f"split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=24:2,"
                 f"eq=brightness=-0.08[bg];[b]scale=-2:1180,crop={W}:ih:x='(iw-ow)*(0.3+0.4*t/{L:.3f})'[fg];[bg][fg]overlay=0:(H-h)/2+40")
    run(["ffmpeg", "-y", "-loglevel", "error", *loop, "-ss", f"{start:.2f}", "-i", str(clip_file(clip)), "-t", f"{L:.3f}", "-an",
         "-vf", f"{frame},fps={FPS},setsar=1,format=yuv420p", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", str(path)])


def xfade(files, lens, out):
    if len(files) == 1:
        shutil.copy(files[0], out)
        return lens[0]
    cmd, g, prev, off = ["ffmpeg", "-y", "-loglevel", "error"], [], "0:v", 0.0
    for f in files:
        cmd += ["-i", str(f)]
    for k in range(1, len(files)):
        off += lens[k - 1] - T
        g.append(f"[{prev}][{k}:v]xfade=transition=fade:duration={T}:offset={off:.3f}[v{k}]")
        prev = f"v{k}"
    run(cmd + ["-filter_complex", ";".join(g), "-map", f"[{prev}]", "-c:v", "libx264", "-preset", "veryfast",
               "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), str(out)])
    return sum(lens) - T * (len(files) - 1)


def rotation_voice(spec):
    names = sorted(p.name for p in (ROOT / "specs" / "voice").glob("*.json"))
    mine = next((n for n in names if json.loads((ROOT / "specs" / "voice" / n).read_text()).get("slug") == spec["slug"]), None)
    vid, name = VOICES[(names.index(mine) if mine else len(names)) % len(VOICES)]
    print(f"voice: {name} ({vid}) from the rotation")
    return vid


def render(spec, outdir):
    outdir.mkdir(parents=True, exist_ok=True)
    work = outdir / "work"
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir()
    scenes = spec["scenes"]
    voice = "mock" if MOCK else (spec.get("voice_id") or rotation_voice(spec))

    # 1. narration and scene timing
    t = 0.0
    for i, sc in enumerate(scenes):
        sc["mp3"], sc["dur"], sc["words"] = tts(sc["say"], voice, float(spec.get("tempo", 1.0)))
        sc["D"] = LEAD + sc["dur"] + TAIL + (HOLD if i == len(scenes) - 1 else 0)
        sc["start"], t = t, t + sc["D"]
    print(f"narration {t:.1f}s, {len(scenes)} scenes")

    # 2. footage: pinned clips first, then top search hits; never the same clip twice
    used, shots, lens, log, credits = set(), [], [], [], {}
    pool_cache = {}
    for i, sc in enumerate(scenes):
        n = max(1, round(sc["D"] / SHOT))
        pinned = [clip_by_id(c) for c in sc.get("clips", [])]
        if len(pinned) < n:
            pool = pool_cache.setdefault(i, scene_pool(sc))
            pinned += [c for c in pool if c["id"] not in used and c["id"] not in {p["id"] for p in pinned}]
        if not pinned:
            raise SystemExit(f"scene {i + 1}: no footage (add clips or queries)")
        for k in range(n):
            c = pinned[k % len(pinned)]
            L = sc["D"] / n + T
            p = work / f"shot{len(shots):03d}.mp4"
            shot(c, L, p)
            shots.append(p); lens.append(L); used.add(c["id"])
            credits[c["id"]] = f"{c['id']}  {c['credit']}  {c.get('url') or ''}"
            log.append(f"{sc['start'] + k * (L - T):6.1f}s  scene {i + 1}  {c['id']}  {c.get('tags', '')}")
    base = work / "base.mp4"
    base_len = xfade(shots, lens, base)

    # 3. narration track padded per scene, captions on the final timeline
    parts = []
    for i, sc in enumerate(scenes):
        p = work / f"narr{i:02d}.wav"
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(sc["mp3"]), "-af",
             f"aresample=44100,aformat=channel_layouts=mono,adelay={int(LEAD * 1000)},apad,atrim=0:{sc['D']:.3f}", str(p)])
        parts.append(p)
    (work / "narr.txt").write_text("".join(f"file '{p.name}'\n" for p in parts))
    narr = work / "narr.wav"
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(work / "narr.txt"),
         "-af", f"apad,atrim=0:{base_len:.3f}", str(narr)])
    ass = work / "captions.ass"
    captions([(w, sc["start"] + LEAD + s, sc["start"] + LEAD + e) for sc in scenes for w, s, e in sc["words"]], ass)
    bgm = work / "bgm.wav"
    run([sys.executable, str(ROOT / "tools" / "bgm.py"), str(bgm), f"{base_len + 1:.1f}", str(spec.get("seed", 1)), spec.get("mood", "bright")])

    # 4. final pass: per-scene overlays, progress bar, captions; voice + ducked BGM, -14 LUFS
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(base), "-i", str(narr), "-i", str(bgm)]
    g, v, idx = [], "0:v", 3
    static = work / "static.png"
    overlay_static(spec, static)
    cmd += ["-loop", "1", "-framerate", str(FPS), "-t", f"{base_len:.3f}", "-i", str(static)]
    g.append(f"[{v}][{idx}:v]overlay=format=auto:shortest=1[st]")
    v, idx = "st", idx + 1
    for i, sc in enumerate(scenes):
        png = work / f"ov{i:02d}.png"
        overlay(spec, sc, png, last=i == len(scenes) - 1)
        a = sc["start"] + (0 if i == 0 else T / 2)
        b = min(base_len, sc["start"] + sc["D"] + (T if i == len(scenes) - 1 else T / 2))
        cmd += ["-loop", "1", "-framerate", str(FPS), "-t", f"{b - a:.3f}", "-i", str(png)]
        fin = "" if i == 0 else "fade=t=in:st=0:d=0.3:alpha=1,"
        fout = "" if i == len(scenes) - 1 else f"fade=t=out:st={b - a - 0.3:.3f}:d=0.3:alpha=1,"
        g.append(f"[{idx}:v]format=rgba,{fin}{fout}setpts=PTS+{a:.3f}/TB[o{i}]")
        g.append(f"[{v}][o{i}]overlay=eof_action=pass:format=auto[w{i}]")
        v, idx = f"w{i}", idx + 1
    cmd += ["-f", "lavfi", "-i", f"color=c=0x9DBDB0:s={W}x10:r={FPS}:d={base_len:.3f}"]
    g.append(f"[{v}][{idx}:v]overlay=x='-w+w*t/{base_len:.3f}':y=0:shortest=1[bar]")
    g.append(f"[bar]subtitles='{str(ass).replace(':', chr(92) + ':')}',format=yuv420p[vout]")
    g.append("[1:a]asplit=2[nv][sc]")
    g.append(f"[2:a]atrim=0:{base_len:.3f},volume=0.30,afade=t=in:d=1,afade=t=out:st={base_len - 2.5:.3f}:d=2.5[bg]")
    g.append("[bg][sc]sidechaincompress=threshold=0.015:ratio=10:attack=15:release=500[duck]")
    g.append(f"[nv][duck]amix=inputs=2:normalize=0,atrim=0:{base_len:.3f},loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[aout]")
    out = outdir / f"{spec['slug']}.mp4"
    run(cmd + ["-filter_complex", ";".join(g), "-map", "[vout]", "-map", "[aout]", "-t", f"{base_len:.3f}",
               "-c:v", "libx264", "-preset", "fast", "-crf", "23", "-maxrate", "2200k", "-bufsize", "4400k", "-r", str(FPS), "-c:a", "aac", "-b:a", "192k",
               "-movflags", "+faststart", str(out)])

    # loudnorm in one pass can land ~2 dB low after the mix: measure and correct to -14 LUFS (video copied)
    m = re.findall(r"I:\s+(-?\d+\.\d) LUFS", subprocess.run(["ffmpeg", "-hide_banner", "-i", str(out), "-af", "ebur128",
                                                         "-f", "null", "-"], capture_output=True, text=True).stderr)
    if m and abs(float(m[-1]) + 14) > 0.5:
        fixed = work / "fixed.mp4"
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(out), "-c:v", "copy", "-af",
             f"volume={-14 - float(m[-1]):.2f}dB,alimiter=limit=0.89", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(fixed)])
        shutil.move(fixed, out)
        print(f"loudness {m[-1]} LUFS -> corrected toward -14")

    # 5. review files: cover (first frame with the headline), shot sheet, credits, meta
    run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "0.5", "-i", str(out), "-frames:v", "1", str(outdir / "cover.png")])
    sheet = Image.new("RGB", (6 * 180, ((len(shots) + 5) // 6) * 320), C["rice"])
    for k, (p, L) in enumerate(zip(shots, lens)):
        f = work / f"still{k:03d}.png"
        run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{L / 2:.2f}", "-i", str(p), "-frames:v", "1", "-vf", "scale=180:320", str(f)])
        sheet.paste(Image.open(f), ((k % 6) * 180, (k // 6) * 320))
    sheet.save(outdir / "shots.jpg", quality=85)
    (outdir / "credits.txt").write_text("Stock footage (Pixabay: no attribution required; Coverr: attribution required):\n"
                                        + "\n".join(credits.values()) + "\n\nShot log:\n" + "\n".join(log) + "\n")
    (outdir / "meta.json").write_text(json.dumps({"slug": spec["slug"], "voice_id": voice, "duration": round(base_len, 2),
                                                  "clips": list(credits),
                                                  "attribution": "Coverr" if any(c.startswith("cv") for c in credits) else ""}, indent=1))
    shutil.rmtree(work, ignore_errors=True)
    print(f"done: {out} ({base_len:.1f}s)")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args or args[0] not in ("voices", "candidates", "render"):
        raise SystemExit(__doc__)
    if args[0] == "voices":
        voices(Path(args[1]))
    else:
        s = json.load(open(args[1], encoding="utf-8"))
        (candidates if args[0] == "candidates" else render)(s, Path(args[2]))

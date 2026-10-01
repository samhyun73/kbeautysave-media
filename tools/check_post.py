"""Quality gate for a day's post. Exit code 0 = OK to schedule, 1 = blocked.

usage:
  python3 tools/check_post.py --spec specs/X.json [--video out/X.mp4] [--caption caption.txt] [--platform instagram|tiktok|weibo|pinterest]

Checks (each prints PASS/FAIL with a reason):
  spec     hangul set, 5-7 frames, hook first / cta last, known frame types, frame text not too long
  caption  #oliveyoungaffiliate + #ad (#广告# on weibo), code KBEAUTY73 with its benefit, no URLs / "link in bio",
           no medical-claim words, no invented-experience phrases, weibo comment-length hint
  video    1080x1920, 12-20 s, has audio, integrated loudness within -16..-12 LUFS
"""
import argparse, json, re, subprocess, sys

FRAME_TYPES = {"hook", "step", "list", "statement", "cta"}
MEDICAL = [r"\bcure[sd]?\b", r"\btreat(s|ment|ing)?\b", r"\bheal(s|ing)?\b", r"\beliminat", r"\bremove[sd]? (acne|wrinkles|scars|pores)",
           r"\banti-?acne\b", r"\bclinically proven\b", r"\bprescription\b", r"\bget rid of (acne|wrinkles)",
           "治疗", "治愈", "祛痘", "去皱", "医学", "疗效", "治る", "除去"]
FAKE_EXPERIENCE = [r"\bI(?:'ve| have) (?:been )?us(?:ed|ing)\b", r"\bmy skin (?:got|became|is now)\b", r"\bI swear by\b",
                   "我用了", "我一直在用", "亲测"]
LINKS = [r"https?://", r"www\.", r"link in bio", r"\.com/", "oliveyoung.com/if"]

results = []
def check(name, ok, why=""):
    results.append(ok)
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f" — {why}" if why and not ok else ""))

def words(x):
    if isinstance(x, list): return " ".join(map(str, x))
    return str(x or "")

def check_spec(path):
    s = json.load(open(path))
    fr = s.get("frames", [])
    check("spec: hangul set", bool(s.get("hangul")), "add \"hangul\": the topic's short Korean word")
    check("spec: 5-7 frames", 5 <= len(fr) <= 7, f"has {len(fr)}")
    check("spec: known frame types", all(f.get("type") in FRAME_TYPES for f in fr))
    check("spec: hook first, cta last", bool(fr) and fr[0].get("type") == "hook" and fr[-1].get("type") == "cta")
    zh = s.get("lang") in ("zh", "ja")
    for i, f in enumerate(fr):
        text = " ".join(words(f.get(k)) for k in ("title", "line", "sub", "items", "lines", "kicker"))
        n = len(re.sub(r"\s", "", text)) if zh else len(text.split())
        lim = 45 if zh else 22
        check(f"spec: frame {i+1} length", n <= lim, f"{n} {'chars' if zh else 'words'} > {lim}")
    allt = json.dumps(s, ensure_ascii=False)
    check("spec: no links", not any(re.search(p, allt, re.I) for p in LINKS))
    check("spec: no medical claims", not any(re.search(p, allt, re.I) for p in MEDICAL),
          next((p for p in MEDICAL if re.search(p, allt, re.I)), ""))
    check("spec: no ALL-CAPS kicker", not any(f.get("kicker", "").isupper() for f in fr))

def check_caption(path, platform):
    t = open(path, encoding="utf-8").read()
    if platform == "weibo":
        check("caption: #广告#", "#广告#" in t)
        check("caption: code + 95折", "KBEAUTY73" in t and "95折" in t)
    else:
        check("caption: #oliveyoungaffiliate", "#oliveyoungaffiliate" in t.lower())
        check("caption: #ad", re.search(r"(^|\s)#ad\b", t, re.I) is not None)
        check("caption: code + 5% benefit", "KBEAUTY73" in t and re.search(r"5\s?%", t) is not None,
              "say \"Extra 5% off with code KBEAUTY73\"")
    if platform == "instagram":
        check("caption: @oliveyoung_global", "@oliveyoung_global" in t)
    hit = next((p for p in LINKS if re.search(p, t, re.I)), None)
    check("caption: no links / link in bio", hit is None, hit or "")
    hit = next((p for p in MEDICAL if re.search(p, t, re.I)), None)
    check("caption: no medical claims", hit is None, hit or "")
    hit = next((p for p in FAKE_EXPERIENCE if re.search(p, t, re.I)), None)
    check("caption: no invented personal experience", hit is None, hit or "")
    if platform == "tiktok":
        check("caption: tiktok title <= 150 chars", len(t.strip()) <= 150, f"{len(t.strip())} chars")
    if platform == "x":
        # X counts most CJK/emoji as 2; stay safely under 280 weighted chars
        w = sum(2 if ord(c) > 0x10FF else 1 for c in t.strip())
        check("caption: X post <= 280 (weighted)", w <= 280, f"{w} weighted chars")

def check_video(path):
    pr = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height:format=duration",
                         "-of", "json", path], capture_output=True, text=True)
    info = json.loads(pr.stdout or "{}")
    st = info.get("streams", [])
    v = next((x for x in st if x.get("codec_type") == "video"), {})
    check("video: 1080x1920", v.get("width") == 1080 and v.get("height") == 1920, f"{v.get('width')}x{v.get('height')}")
    check("video: has audio", any(x.get("codec_type") == "audio" for x in st))
    d = float(info.get("format", {}).get("duration", 0))
    check("video: 12-20 s", 12 <= d <= 20, f"{d:.1f}s")
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True)
    m = re.findall(r"I:\s+(-?\d+\.\d) LUFS", r.stderr)
    lufs = float(m[-1]) if m else None
    check("video: loudness -16..-12 LUFS", lufs is not None and -16 <= lufs <= -12, f"{lufs} LUFS")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec"); ap.add_argument("--video"); ap.add_argument("--caption")
    ap.add_argument("--platform", default="instagram", choices=["instagram", "facebook", "tiktok", "weibo", "pinterest", "x"])
    a = ap.parse_args()
    if a.spec: check_spec(a.spec)
    if a.caption: check_caption(a.caption, a.platform)
    if a.video: check_video(a.video)
    ok = all(results)
    print("\nRESULT:", "OK to schedule" if ok else "BLOCKED — fix the FAIL lines")
    sys.exit(0 if ok else 1)

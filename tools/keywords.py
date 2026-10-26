"""Free YouTube keyword check for the day's topic (runs in GitHub Actions; the workspace can't reach YouTube).

usage: python tools/keywords.py "<seed 1>, <seed 2>, ..." <outdir>

For each seed phrase:
  - YouTube search autocomplete (what people actually type, US English), plus "how to <seed>"
  - the top 10 YouTube search results via yt-dlp (title, views, length, channel), Shorts marked
Writes <outdir>/keywords.md (readable) and keywords.json. No API keys, no credits.
"""
import json, sys, urllib.parse, urllib.request
from pathlib import Path

UA = {"User-Agent": "Mozilla/5.0 (kbeautysave keyword check)"}


def suggest(q):
    url = ("https://suggestqueries.google.com/complete/search?client=firefox&ds=yt&hl=en&gl=US&q="
           + urllib.parse.quote(q))
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20) as r:
        return json.loads(r.read().decode("utf-8", "replace"))[1]


def top_videos(q, n=10):
    import yt_dlp
    opts = {"quiet": True, "skip_download": True, "extract_flat": True, "nowarnings": True}
    with yt_dlp.YoutubeDL(opts) as y:
        res = y.extract_info(f"ytsearch{n}:{q}", download=False) or {}
    out = []
    for e in res.get("entries") or []:
        d = e.get("duration")
        out.append({"title": e.get("title"), "views": e.get("view_count"), "duration": d,
                    "short": bool(d and d <= 60) or "/shorts/" in (e.get("url") or ""),
                    "channel": e.get("channel") or e.get("uploader"), "url": e.get("url")})
    return out


def main(seeds, outdir):
    outdir.mkdir(parents=True, exist_ok=True)
    data, md = [], ["# YouTube keyword check (autocomplete + top results, US English)", ""]
    for s in seeds:
        row = {"seed": s, "autocomplete": [], "how_to": [], "top": [], "errors": []}
        for key, q in (("autocomplete", s), ("how_to", "how to " + s)):
            try:
                row[key] = suggest(q)
            except Exception as e:  # noqa: BLE001 - report and keep going
                row["errors"].append(f"{key}: {e}")
        try:
            row["top"] = top_videos(s)
        except Exception as e:  # noqa: BLE001
            row["errors"].append(f"top: {e}")
        data.append(row)
        views = [v["views"] for v in row["top"] if v["views"]]
        shorts = sum(v["short"] for v in row["top"])
        md += [f"## {s}", "",
               f"- Autocomplete: {', '.join(row['autocomplete'][:10]) or '(none)'}",
               f"- \"how to\": {', '.join(row['how_to'][:6]) or '(none)'}",
               f"- Top 10: {shorts} Shorts; median views {sorted(views)[len(views) // 2]:,}" if views else "- Top 10: (no data)",
               ""]
        for v in row["top"]:
            md.append(f"  - {'[S] ' if v['short'] else ''}{v['title']} · {v['views'] or 0:,} views · {v['channel']}")
        if row["errors"]:
            md += ["", "  Errors: " + "; ".join(row["errors"])]
        md.append("")
    (outdir / "keywords.json").write_text(json.dumps(data, indent=1, ensure_ascii=False))
    (outdir / "keywords.md").write_text("\n".join(md))
    print("\n".join(md))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    main([x.strip() for x in sys.argv[1].split(",") if x.strip()], Path(sys.argv[2]))

"""Olive Young Global event check (runs in GitHub Actions; the workspace can't reach the site and
WebFetch can't see the JavaScript banners).

usage: python tools/events.py <outdir>

Banners differ by shipping country (cookie `dlvCntry`; e.g. Black Friday 1-12 Nov 2026 showed for
Canada/UK/Australia but not for the US or Japan). So the home page and the events page are opened
once per market below, and every banner / event link is listed with the markets that see it.
Writes events.md (readable), events.json, and home-<market>.png screenshots. Read-only.
"""
import json, re, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

MARKETS = {"US": "10", "CA": "20", "UK": "170", "AU": "30", "JP": "110"}   # site codes (dlvCntryList)
PAGES = [("home", "https://global.oliveyoung.com/"),
         ("events", "https://global.oliveyoung.com/event/main")]
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
DATES = re.compile(r"\b\d{1,2}\s*[A-Z][a-z]{2}\w*\s*[-~–]\s*\d{1,2}\s*[A-Z][a-z]{2}\w*\b|\b\d{1,2}/\d{1,2}\s*[-~–]\s*\d{1,2}/\d{1,2}\b")

JS = """() => {
  const out = [];
  for (const a of document.querySelectorAll('a[href]')) {
    let h = a.getAttribute('href') || '';
    const m = h.match(/googleViewPromotion\\("([^"]+)/); if (m) h = decodeURIComponent(m[1]).split('"')[0];
    if (!/plndpNo=|eventNo=/i.test(h)) continue;
    const t = (a.innerText || '').replace(/\\s+/g, ' ').trim();
    const img = a.querySelector('img');
    const alt = img ? (img.getAttribute('alt') || '') : '';
    if (!t && !alt) continue;
    out.push({id: (h.match(/(plndpNo|eventNo)=([\\w]+)/) || [,,h])[2], text: t, alt});
  }
  return out;
}"""


def clean(s):
    """Banners repeat their lines for the slide animation: drop repeated phrases."""
    parts, seen = [], set()
    for w in re.split(r"\s{2,}| · ", s):
        w = w.strip()
        if w and w.lower() not in seen and not w.startswith("category-promotion"):
            seen.add(w.lower()); parts.append(w)
    return " · ".join(parts)


def main(outdir):
    outdir.mkdir(parents=True, exist_ok=True)
    events, errors = {}, []
    with sync_playwright() as p:
        b = p.chromium.launch()
        for mk, code in MARKETS.items():
            ctx = b.new_context(viewport={"width": 1440, "height": 900}, locale="en-US", user_agent=UA)
            ctx.add_cookies([{"name": "dlvCntry", "value": code, "domain": "global.oliveyoung.com", "path": "/"}])
            pg = ctx.new_page()
            for name, url in PAGES:
                try:
                    pg.goto(url, wait_until="domcontentloaded", timeout=60000)
                    pg.wait_for_timeout(7000)   # the site never goes network-idle (trackers)
                    for _ in range(5):
                        pg.mouse.wheel(0, 1500); pg.wait_for_timeout(600)
                    if name == "home":
                        pg.mouse.wheel(0, -20000); pg.wait_for_timeout(400)
                        pg.screenshot(path=str(outdir / f"home-{mk}.png"))
                    for x in pg.evaluate(JS):
                        e = events.setdefault(x["id"], {"id": x["id"], "texts": [], "markets": [], "dates": []})
                        txt = clean(" · ".join(s for s in (x["text"], x["alt"]) if s))
                        if txt and txt not in e["texts"]:
                            e["texts"].append(txt)
                        if mk not in e["markets"]:
                            e["markets"].append(mk)
                        for d in DATES.findall(txt):
                            if d not in e["dates"]:
                                e["dates"].append(d)
                except Exception as ex:  # noqa: BLE001 - report and keep going
                    errors.append(f"{mk} {name}: {str(ex)[:120]}")
            ctx.close()
        b.close()
    rows = sorted(events.values(), key=lambda e: (not e["dates"], -len(e["markets"]), e["id"]))
    md = ["# Olive Young Global events by shipping market (home + /event/main, rendered)",
          "", f"Markets: {', '.join(f'{k}={v}' for k, v in MARKETS.items())}. "
          "Use an event in copy only for the markets that see it; offers differ by shipping country.", ""]
    for e in rows:
        best = max(e["texts"], key=len)[:200]
        md.append(f"- [{'/'.join(e['markets'])}] {'**' + ', '.join(e['dates']) + '** ' if e['dates'] else ''}"
                  f"{best} (id {e['id']})")
    if errors:
        md += ["", "Errors: " + "; ".join(errors)]
    (outdir / "events.json").write_text(json.dumps(rows, indent=1, ensure_ascii=False))
    (outdir / "events.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    main(Path(sys.argv[1]))

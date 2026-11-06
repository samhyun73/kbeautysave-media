"""Olive Young Global event check (runs in GitHub Actions; the workspace can't reach the site and
WebFetch can't see the JavaScript banners).

usage: python tools/events.py <outdir>

Opens the home page and the events page in headless Chromium (US English), collects every banner /
event link with its text (brand, title, dates such as "1 Nov - 12 Nov"), and saves:
  events.md    readable list for the daily run
  events.json  same data
  home.png, events.png  screenshots to check by eye
Read-only: nothing is posted.
"""
import json, re, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

PAGES = [("home", "https://global.oliveyoung.com/"),
         ("events", "https://global.oliveyoung.com/event/main")]
DATES = re.compile(r"\b\d{1,2}\s*[A-Z][a-z]{2}\w*\s*[-~–]\s*\d{1,2}\s*[A-Z][a-z]{2}\w*\b|\b\d{1,2}/\d{1,2}\s*[-~–]\s*\d{1,2}/\d{1,2}\b")

JS = """() => {
  const out = [];
  for (const a of document.querySelectorAll('a[href]')) {
    const h = a.getAttribute('href') || '';
    if (!/event|plndp|planning|promotion|brand/i.test(h)) continue;
    const t = (a.innerText || '').replace(/\\s+\\n/g, '\\n').trim();
    const img = a.querySelector('img');
    const alt = img ? (img.getAttribute('alt') || '') : '';
    if (!t && !alt) continue;
    out.push({href: a.href, text: t, alt});
  }
  return out;
}"""


def main(outdir):
    outdir.mkdir(parents=True, exist_ok=True)
    seen, items, errors = set(), [], []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1440, "height": 900}, locale="en-US")
        for name, url in PAGES:
            try:
                pg.goto(url, wait_until="networkidle", timeout=60000)
                pg.wait_for_timeout(3000)
                for _ in range(6):                      # lazy-loaded sections
                    pg.mouse.wheel(0, 1500); pg.wait_for_timeout(700)
                pg.screenshot(path=str(outdir / f"{name}.png"), full_page=False)
                for x in pg.evaluate(JS):
                    key = (x["href"], x["text"][:80], x["alt"][:80])
                    if key in seen:
                        continue
                    seen.add(key)
                    blob = f'{x["text"]} {x["alt"]}'
                    x["dates"] = DATES.findall(blob)
                    x["page"] = name
                    items.append(x)
            except Exception as e:  # noqa: BLE001 - report and keep going
                errors.append(f"{name}: {e}")
        b.close()
    items.sort(key=lambda x: (not x["dates"], x["page"]))
    md = ["# Olive Young Global events (home + /event/main, rendered)", ""]
    for x in items:
        line = " / ".join(s for s in (x["text"].replace("\n", " · "), x["alt"]) if s)[:220]
        md.append(f"- {'**' + ', '.join(x['dates']) + '** ' if x['dates'] else ''}{line} — {x['href']}")
    if errors:
        md += ["", "Errors: " + "; ".join(errors)]
    (outdir / "events.json").write_text(json.dumps(items, indent=1, ensure_ascii=False))
    (outdir / "events.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    main(Path(sys.argv[1]))

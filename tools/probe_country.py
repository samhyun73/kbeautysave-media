import json, re, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
hits = []
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 1440, "height": 900}, locale="en-US", user_agent=UA)
    pg = ctx.new_page()
    def on_resp(r):
        try:
            if "json" in (r.headers.get("content-type") or ""):
                body = r.text()
                if re.search(r"Philippines|PHILIPPINES|ISRAEL|Israel", body):
                    hits.append((r.url, body[:20000]))
        except Exception:
            pass
    pg.on("response", on_resp)
    pg.goto("https://global.oliveyoung.com/", wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(6000)
    # click anything that looks like the globe / country button in the header
    for sel in ["[class*=lang]", "[class*=country]", "[class*=global]", "[class*=nation]", "header button", "header a"]:
        els = pg.locator(sel).all()
        for el in els[:15]:
            try:
                el.click(timeout=1500); pg.wait_for_timeout(1200)
            except Exception:
                pass
        txt = pg.evaluate("() => document.body.innerText")
        if re.search(r"PHILIPPINES|Philippines|ISRAEL|Israel", txt):
            break
    txt = pg.evaluate("() => document.body.innerText")
    html = pg.content()
    print("PH in text:", bool(re.search(r"Philippines|PHILIPPINES", txt)), "| PH in html:", bool(re.search(r"Philippines|PHILIPPINES", html)))
    m = re.findall(r"[^\n]{0,60}(?:PHILIPPINES|Philippines)[^\n]{0,60}", html)[:5]; print("ctx:", m)
    names = re.findall(r">\s*([A-Z][A-Z .,()&'-]{2,40})\s*<", html)
    print("UPPER NAMES:", sorted(set(names))[:400])
    for u, body in hits[:3]:
        print("JSON", u); print(body[:3000])
    b.close()

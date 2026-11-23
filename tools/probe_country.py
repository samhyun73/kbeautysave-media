import json, re, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 1440, "height": 900}, locale="en-US", user_agent=UA)
    pg = ctx.new_page()
    pg.goto("https://global.oliveyoung.com/", wait_until="domcontentloaded", timeout=60000)
    pg.wait_for_timeout(7000)
    html = pg.content()
    opts = re.findall(r'<(?:option|li|a|button)[^>]*(?:value|data-[a-z-]+)="(\d{2,3})"[^>]*>\s*([A-Za-z][A-Za-z .&\'()-]{2,40})<', html)
    near = re.findall(r'.{0,120}Philippines.{0,120}', html)[:5]
    print("OPTS", opts[:200]); print("NEAR", near)
    ctx.close()
    codes = sorted({c for c, n in opts if "Philipp" in n}) or [str(i*10) for i in range(14, 30)]
    for code in codes:
        ctx = b.new_context(viewport={"width": 1440, "height": 900}, locale="en-US", user_agent=UA)
        ctx.add_cookies([{"name": "dlvCntry", "value": code, "domain": "global.oliveyoung.com", "path": "/"}])
        pg = ctx.new_page()
        pg.goto("https://global.oliveyoung.com/", wait_until="domcontentloaded", timeout=60000)
        pg.wait_for_timeout(6000)
        t = pg.evaluate("() => document.body.innerText")
        ck = {c["name"]: c["value"] for c in ctx.cookies()}
        print("CODE", code, ck.get("dlvCntry"), "BF" if "BLACK FRIDAY" in t.upper() else "-", re.findall(r"Final BLACK FRIDAY[^\n]*|\d+ Nov - \d+ Nov", t)[:3])
        ctx.close()
    b.close()

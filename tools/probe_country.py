import re, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
Path(sys.argv[1]).mkdir(parents=True, exist_ok=True)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
with sync_playwright() as p:
    b = p.chromium.launch()
    for code in ["1710"]:
        ctx = b.new_context(viewport={"width": 1440, "height": 900}, locale="en-US", user_agent=UA)
        ctx.add_cookies([{"name": "dlvCntry", "value": code, "domain": "global.oliveyoung.com", "path": "/"}])
        pg = ctx.new_page()
        pg.goto("https://global.oliveyoung.com/", wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(6000)
        t = pg.evaluate("() => document.body.innerText"); ck = {c["name"]: c["value"] for c in ctx.cookies()}
        print("HOME", code, "dlv", ck.get("dlvCntry"), re.findall(r"[^\n]*(?:BLACK FRIDAY|Free shipping)[^\n]*", t, re.I)[:4])
        pg.goto("https://global.oliveyoung.com/event/planning?plndpNo=3041", wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(7000)
        t = pg.evaluate("() => document.body.innerText")
        print("EVENT", pg.url, re.findall(r"[^\n]*(?:22.28 NOV|ONCE A YEAR|BIGGEST SAVINGS|First Order|Coupon)[^\n]*", t, re.I)[:8])
        ctx.close()
    b.close()

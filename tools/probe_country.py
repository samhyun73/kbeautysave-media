import re, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
Path(sys.argv[1]).mkdir(parents=True, exist_ok=True)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
with sync_playwright() as p:
    b = p.chromium.launch()
    for cc in ["ph", "us", "ca", "jp"]:
        ctx = b.new_context(viewport={"width": 1440, "height": 900}, locale="en-US", user_agent=UA)
        pg = ctx.new_page()
        pg.goto(f"https://global.oliveyoung.com/{cc}/brands/fromlabs", wait_until="domcontentloaded", timeout=60000)
        pg.wait_for_timeout(5000)
        ck = {c["name"]: c["value"] for c in ctx.cookies()}
        pg.goto("https://global.oliveyoung.com/", wait_until="domcontentloaded", timeout=60000)
        pg.wait_for_timeout(6000)
        t = pg.evaluate("() => document.body.innerText")
        ck2 = {c["name"]: c["value"] for c in ctx.cookies()}
        print(cc.upper(), "url", pg.url, "dlv", ck.get("dlvCntry"), "->", ck2.get("dlvCntry"), "strip:", re.findall(r"Final BLACK FRIDAY[^\n]*", t)[:1], re.findall(r"\d+ Nov - \d+ Nov", t)[:1], "| ship-text:", re.findall(r"[^\n]*(?:shoppers|Ship to|Deliver)[^\n]*", t)[:2])
        ctx.close()
    b.close()

import json, re, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
with sync_playwright() as p:
    b = p.chromium.launch()
    # 1) full shipping-country list from the page's own data
    ctx = b.new_context(viewport={"width": 1440, "height": 900}, locale="en-US", user_agent=UA)
    pg = ctx.new_page()
    pg.goto("https://global.oliveyoung.com/", wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(6000)
    opts = pg.evaluate("""() => [...document.querySelectorAll('select option, [data-cntry-cd], [data-dlv-cntry], li[data-value]')]
        .map(e => [e.value || e.getAttribute('data-cntry-cd') || e.getAttribute('data-dlv-cntry') || e.getAttribute('data-value'), (e.innerText||e.textContent||'').trim()]).filter(x=>x[1])""")
    print("OPTIONS", len(opts)); print(json.dumps(opts, ensure_ascii=False)[:6000])
    ctx.close()
    # 2) the event page for markets that are not in the 9-country list
    for code in ["40", "60", "140", "200"]:
        ctx = b.new_context(viewport={"width": 1440, "height": 900}, locale="en-US", user_agent=UA)
        ctx.add_cookies([{"name": "dlvCntry", "value": code, "domain": "global.oliveyoung.com", "path": "/"}])
        pg = ctx.new_page()
        pg.goto("https://global.oliveyoung.com/event/planning?plndpNo=3041", wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(7000)
        t = pg.evaluate("() => document.body.innerText")
        print("CODE", code, pg.url, "| notice:", re.findall(r"[^\n]*unavailable[^\n]*", t)[:2], "| BF:", re.findall(r"[^\n]*(?:22.28 NOV|ONCE A YEAR|BIGGEST SAVINGS)[^\n]*", t, re.I)[:3])
        ctx.close()
    b.close()

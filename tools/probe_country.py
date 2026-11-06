import json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
res = []
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
with sync_playwright() as p:
    b = p.chromium.launch()
    for code in [f"{i:02d}" for i in range(1, 41)]:
        ctx = b.new_context(viewport={"width": 1440, "height": 900}, locale="en-US", user_agent=UA)
        ctx.add_cookies([{"name": "dlvCntry", "value": code, "domain": "global.oliveyoung.com", "path": "/"}])
        pg = ctx.new_page()
        try:
            pg.goto("https://global.oliveyoung.com/", wait_until="domcontentloaded", timeout=45000)
            pg.wait_for_timeout(6000)
            html = pg.content()
            ck = {c["name"]: c["value"] for c in ctx.cookies() if c["domain"].endswith("oliveyoung.com")}
            ship = pg.evaluate("""() => { const t=document.body.innerText; const m=t.match(/(Ship(ping)? to|Deliver(y)? to)[^\\n]{0,40}/i); return m?m[0]:''; }""")
            res.append({"code": code, "dlv": ck.get("dlvCntry"), "cur": ck.get("currency"), "bf": "BLACK FRIDAY" in html.upper(),
                        "bf_dates": __import__("re").findall(r"1 Nov\s*-\s*\d+ Nov", html)[:2], "ship": ship,
                        "title": pg.title()[:40]})
        except Exception as e:
            res.append({"code": code, "err": str(e)[:80]})
        ctx.close()
        print(res[-1], flush=True)
    b.close()
(out/"countries.json").write_text(json.dumps(res, indent=1))

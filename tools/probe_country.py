import json, re, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
MK = {"US": "10", "CA": "20", "UK": "170", "AU": "30", "JP": "110"}
res = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    for mk, code in MK.items():
        ctx = b.new_context(viewport={"width": 1440, "height": 900}, locale="en-US", user_agent=UA)
        ctx.add_cookies([{"name": "dlvCntry", "value": code, "domain": "global.oliveyoung.com", "path": "/"}])
        pg = ctx.new_page()
        try:
            pg.goto("https://global.oliveyoung.com/event/planning?plndpNo=3041", wait_until="domcontentloaded", timeout=60000)
            pg.wait_for_timeout(8000)
            txt = pg.evaluate("() => document.body.innerText")
            imgs = pg.evaluate("() => [...document.images].map(i => i.alt).filter(Boolean).slice(0,40)")
            res[mk] = {"url": pg.url, "title": pg.title(), "text": txt[:3000], "alts": imgs}
            pg.screenshot(path=str(out / f"p3041-{mk}.png"), full_page=False)
        except Exception as e:
            res[mk] = {"err": str(e)[:200]}
        ctx.close()
    b.close()
(out / "p3041.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
for k, v in res.items():
    print("=====", k, v.get("url"), v.get("title"))
    print((v.get("text") or v.get("err", ""))[:1500])
    print("ALTS:", v.get("alts"))

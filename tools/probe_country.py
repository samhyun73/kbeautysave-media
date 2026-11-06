import json, re, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
res = []
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
with sync_playwright() as p:
    b = p.chromium.launch()
    first = True
    for code in [str(i * 10) for i in range(1, 31)]:
        ctx = b.new_context(viewport={"width": 1440, "height": 900}, locale="en-US", user_agent=UA)
        ctx.add_cookies([{"name": "dlvCntry", "value": code, "domain": "global.oliveyoung.com", "path": "/"}])
        pg = ctx.new_page()
        try:
            pg.goto("https://global.oliveyoung.com/", wait_until="domcontentloaded", timeout=45000)
            pg.wait_for_timeout(6000)
            html = pg.content()
            if first:
                (out / "home10.html").write_text(html); first = False
            ck = {c["name"]: c["value"] for c in ctx.cookies() if c["domain"].endswith("oliveyoung.com")}
            sel = re.findall(r'<option[^>]*value="%s"[^>]*>([^<]{1,40})' % code, html)[:2]
            sel2 = re.findall(r'data-[a-z-]*="%s"[^>]*>([^<]{1,40})' % code, html)[:3]
            slides = re.findall(r'(\d+)\s*/\s*(\d+)', pg.evaluate("() => document.body.innerText"))[:1]
            res.append({"code": code, "dlv": ck.get("dlvCntry"), "bf": "BLACK FRIDAY IS HERE" in html.upper(),
                        "opt": sel, "data": sel2, "slides": slides})
        except Exception as e:
            res.append({"code": code, "err": str(e)[:80]})
        ctx.close()
        print(res[-1], flush=True)
    b.close()
(out/"countries.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))

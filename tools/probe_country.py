import json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
log = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 1440, "height": 900}, locale="en-US",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36")
    pg = ctx.new_page()
    reqs = []
    pg.on("request", lambda r: reqs.append(r.url) if ("country" in r.url.lower() or "dlvr" in r.url.lower() or "nation" in r.url.lower()) else None)
    pg.goto("https://global.oliveyoung.com/", wait_until="domcontentloaded", timeout=60000)
    pg.wait_for_timeout(8000)
    log["cookies"] = ctx.cookies()
    log["html_country_bits"] = pg.evaluate("""() => {
      const h = document.documentElement.outerHTML; const out=[];
      const re=/[^\\n]{0,120}(dlvrNatn|natnCd|shipCountry|countryCd|nationCode|ntnCd)[^\\n]{0,160}/gi; let m; let n=0;
      while((m=re.exec(h)) && n<40){out.push(m[0]); n++;} return out; }""")
    # try the globe button
    try:
        btns = pg.locator("header button, header a").all()
        log["header_controls"] = [ (x.get_attribute("class") or "")+" | "+(x.inner_text() or "")[:40] for x in btns][:60]
    except Exception as e:
        log["header_err"] = str(e)
    log["reqs"] = reqs[:50]
    pg.screenshot(path=str(out/"probe.png"))
    b.close()
(out/"probe.json").write_text(json.dumps(log, indent=1, ensure_ascii=False))
print(json.dumps(log, indent=1, ensure_ascii=False)[:20000])

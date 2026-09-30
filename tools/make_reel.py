"""Build a 9:16 slideshow Reel (MP4 + BGM) and optional Pinterest pin PNG from a JSON spec.
usage: python3 make_reel.py spec.json outdir
spec: {"slug":..., "mood":"calm|bright", "seed":1, "frames":[{type,..., "dur":sec}], "pin":{...}?}
frame types: hook | step | list | statement | cta
"""
import json, os, sys, subprocess, html

C = dict(cream="#FBF4EE", ink="#2A1E1C", blush="#F2D9CF", sky="#DCE6EE", accent="#A63F31",
         navy="#2F4B7C", pink="#F2B8A8", mute="#5B4A45", mute2="#D9CBC5", deep="#3A2A27")
FONTS = {
    "en": ("'Noto Serif CJK KR','Noto Serif CJK SC',serif", "'Noto Sans CJK KR','Noto Sans CJK SC',sans-serif"),
    "zh": ("'Noto Serif CJK SC','Noto Serif CJK KR',serif", "'Noto Sans CJK SC','Noto Sans CJK KR',sans-serif"),
    "ja": ("'Noto Serif CJK JP','Noto Serif CJK KR',serif", "'Noto Sans CJK JP','Noto Sans CJK KR',sans-serif"),
}
SERIF, SANS = FONTS["en"]
LANG = "en"
W, H = 1080, 1920
PAD = "padding:260px 160px 440px 96px"  # keeps text out of IG/TikTok UI zones

def e(s): return html.escape(str(s))

def em(s, color):
    """*word* -> accent-colored span"""
    parts = e(s).split("*")
    return "".join(f'<span style="color:{color}">{p}</span>' if i % 2 else p for i, p in enumerate(parts))

def page(bg, fg, inner, extra=""):
    return f"""<!doctype html><html lang="{LANG}"><head><meta charset="utf-8"><style>
html,body{{margin:0;width:{W}px;height:{H}px;overflow:hidden}}
body{{background:{bg};color:{fg};font-family:{SANS}}}
.root{{width:{W}px;height:{H}px;box-sizing:border-box;{PAD};display:flex;flex-direction:column;justify-content:center;gap:48px;position:relative;overflow:hidden}}
h1,h2,p{{margin:0}} .serif{{font-family:{SERIF};letter-spacing:-2px}}
</style></head><body><div class="root">{extra}{inner}</div></body></html>"""

def f_hook(f):
    extra = f'<div style="position:absolute;right:-260px;top:180px;width:760px;height:760px;border-radius:50%;background:{C["deep"]}"></div>'
    inner = f"""<div style="position:relative;font-size:40px;font-weight:700;color:{C['pink']}">{e(f.get('kicker',''))}</div>
<h1 class="serif" style="position:relative;font-size:140px;line-height:1.05;font-weight:700">{em(f['title'], C['pink'])}</h1>
<p style="position:relative;font-size:52px;line-height:1.3;color:{C['mute2']}">{e(f.get('sub',''))}</p>"""
    return page(C["ink"], C["cream"], inner, extra)

def f_step(f):
    col = C["accent"] if f.get("tone", "warm") == "warm" else C["navy"]
    big = C["blush"] if f.get("tone", "warm") == "warm" else C["sky"]
    inner = f"""<div class="serif" style="font-size:300px;line-height:0.8;font-weight:700;color:{big}">{e(f['num'])}</div>
<h2 class="serif" style="font-size:132px;line-height:1.05;font-weight:700">{e(f['title'])}</h2>
<p style="font-size:60px;line-height:1.3;font-weight:700;color:{col}">{e(f.get('line',''))}</p>
<p style="font-size:44px;line-height:1.4;color:{C['mute']}">{e(f.get('sub',''))}</p>"""
    return page(C["cream"], C["ink"], inner)

def f_list(f):
    rows = "".join(f"""<div style="display:flex;align-items:center;gap:36px">
<span style="flex-shrink:0;width:96px;height:96px;border-radius:50%;background:{C['accent']};color:#fff;font-size:44px;font-weight:700;display:flex;align-items:center;justify-content:center">{i+1}</span>
<span class="serif" style="font-size:84px;line-height:1.1;font-weight:700;letter-spacing:-1px">{e(t)}</span></div>""" for i, t in enumerate(f["items"]))
    title = f'<h2 class="serif" style="font-size:96px;line-height:1.05;font-weight:700;margin-bottom:12px">{e(f["title"])}</h2>' if f.get("title") else ""
    foot = f'<p style="margin-top:24px;font-size:44px;line-height:1.4;color:{C["mute"]}">{e(f["sub"])}</p>' if f.get("sub") else ""
    return page(C["blush"], C["ink"], title + rows + foot)

def f_statement(f):
    lines = "".join(f'<h2 class="serif" style="font-size:150px;line-height:1.05;font-weight:700">{em(l, C["pink"])}</h2>' for l in f["lines"])
    return page(C["ink"], C["cream"], lines + f'<p style="margin-top:24px;font-size:52px;line-height:1.3;color:{C["mute2"]}">{e(f.get("sub",""))}</p>')

def f_cta(f):
    inner = f"""<h2 class="serif" style="font-size:120px;line-height:1.05;font-weight:700">{e(f.get('title','Try it tonight.'))}</h2>
<div style="padding:56px 48px;border-radius:32px;border:3px dashed #fff;background:{C['cream']};color:{C['ink']};display:flex;flex-direction:column;align-items:center;gap:16px">
<span style="font-size:34px;font-weight:700;letter-spacing:4px;color:{C['mute']}">{e(f.get('code_label','USE CODE'))}</span>
<span class="serif" style="font-size:116px;font-weight:700;letter-spacing:3px;line-height:1">KBEAUTY73</span></div>
<p style="font-size:46px;line-height:1.4">{f.get('where_html','at checkout on<br><b>Olive Young Global</b> @oliveyoung_global')}</p>
<span style="font-size:30px;opacity:.9">{e(f.get('tags','#oliveyoungaffiliate #ad'))}</span>"""
    return page(C["accent"], "#fff", inner)

RENDER = {"hook": f_hook, "step": f_step, "list": f_list, "statement": f_statement, "cta": f_cta}

def pin_html(p):
    steps = "".join(f"""<div style="padding:36px;border-radius:28px;background:{C['blush'] if i==0 else C['sky']};display:flex;flex-direction:column;gap:14px">
<span class="serif" style="font-size:80px;line-height:.9;font-weight:700;color:{C['accent'] if i==0 else C['navy']}">{i+1:02d}</span>
<span class="serif" style="font-size:44px;font-weight:700;line-height:1.1">{e(s['title'])}</span>
<span style="font-size:25px;line-height:1.5;color:#3D2F2B">{e(s['body'])}</span></div>""" for i, s in enumerate(p["steps"][:2]))
    tips = "".join(f'<div style="display:flex;gap:18px;font-size:30px;align-items:center"><span style="color:{C["accent"]};font-weight:700">✕</span><span>{e(t)}</span></div>' for t in p.get("avoid", []))
    note = f'<div style="padding:28px 32px;border-radius:24px;border:2px solid #E4D3CB;font-size:28px;line-height:1.4">{e(p["note"])}</div>' if p.get("note") else ""
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;width:1000px;height:1500px;overflow:hidden;background:{C['cream']};color:{C['ink']};font-family:{SANS}}}
.serif{{font-family:{SERIF};letter-spacing:-1px}} h1,p{{margin:0}}</style></head><body>
<div style="width:1000px;height:1500px;display:flex;flex-direction:column">
<div style="padding:72px 72px 56px;background:{C['ink']};color:{C['cream']};display:flex;flex-direction:column;gap:20px">
<div style="font-size:24px;font-weight:700;letter-spacing:4px;color:{C['pink']}">{e(p.get('kicker','K-BEAUTY GUIDE'))}</div>
<h1 class="serif" style="font-size:88px;line-height:1.05;font-weight:700">{e(p['title'])}</h1>
<p style="font-size:34px;color:{C['mute2']}">{e(p.get('sub',''))}</p></div>
<div style="flex-grow:1;padding:56px 72px;display:flex;flex-direction:column;gap:32px">
<div style="display:grid;grid-template-columns:1fr 1fr;gap:24px">{steps}</div>
<div style="display:flex;flex-direction:column;gap:18px"><span style="font-size:24px;font-weight:700;letter-spacing:3px;color:{C['accent']}">{'AVOID' if p.get('avoid') else ''}</span>{tips}</div>{note}</div>
<div style="padding:40px 72px;background:{C['accent']};color:#fff;display:flex;justify-content:space-between;align-items:center">
<div style="display:flex;flex-direction:column;gap:6px"><span style="font-size:24px;letter-spacing:3px;font-weight:700">SHOP AT OLIVE YOUNG GLOBAL</span>
<span class="serif" style="font-size:56px;font-weight:700;letter-spacing:2px">Code KBEAUTY73</span></div><span style="font-size:22px">#ad</span></div>
</div></body></html>"""

SHOT_JS = r"""
const { chromium } = require('playwright');
(async () => {
  const jobs = JSON.parse(process.argv[2]);
  const b = await chromium.launch();
  for (const j of jobs) {
    const p = await b.newPage({ viewport: { width: j.w, height: j.h } });
    await p.goto('file://' + j.html); await p.waitForTimeout(150);
    await p.screenshot({ path: j.png }); await p.close();
  }
  await b.close();
})();
"""

def main(spec_path, out):
    global SERIF, SANS, LANG
    spec = json.load(open(spec_path)); os.makedirs(out, exist_ok=True)
    LANG = spec.get("lang", "en"); SERIF, SANS = FONTS.get(LANG, FONTS["en"])
    here = os.path.dirname(os.path.abspath(__file__))
    jobs, durs = [], []
    for i, f in enumerate(spec["frames"]):
        hp = os.path.join(out, f"frame{i+1}.html")
        open(hp, "w").write(RENDER[f["type"]](f))
        jobs.append(dict(html=os.path.abspath(hp), png=os.path.abspath(os.path.join(out, f"frame{i+1}.png")), w=W, h=H))
        durs.append(float(f.get("dur", 3)))
    if spec.get("pin"):
        hp = os.path.join(out, "pin.html"); open(hp, "w").write(pin_html(spec["pin"]))
        jobs.append(dict(html=os.path.abspath(hp), png=os.path.abspath(os.path.join(out, "pin.png")), w=1000, h=1500))
    js = os.path.join(out, "_shot.js"); open(js, "w").write(SHOT_JS)
    env = dict(os.environ, NODE_PATH=subprocess.check_output(["npm", "root", "-g"]).decode().strip())
    subprocess.run(["node", js, json.dumps(jobs)], check=True, env=env)

    X = 0.4  # crossfade seconds
    total = sum(durs) - X*(len(durs)-1)
    wav = os.path.join(out, "bgm.wav")
    subprocess.run([sys.executable, os.path.join(here, "bgm.py"), wav, f"{total:.2f}", str(spec.get("seed", 1)), spec.get("mood", "calm")], check=True)
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    for i, d in enumerate(durs):
        cmd += ["-loop", "1", "-t", f"{d}", "-framerate", "30", "-i", os.path.join(out, f"frame{i+1}.png")]
    cmd += ["-i", wav]
    fl, prev, off = [], "[0:v]", 0.0
    for i in range(len(durs)):
        fl.append(f"[{i}:v]scale={W}:{H},setsar=1,format=yuv420p[s{i}]")
    prev = "[s0]"
    for i in range(1, len(durs)):
        off += durs[i-1] - X
        lab = f"[x{i}]"
        fl.append(f"{prev}[s{i}]xfade=transition=fade:duration={X}:offset={off:.2f}{lab}")
        prev = lab
    mp4 = os.path.join(out, f"{spec.get('slug','reel')}.mp4")
    cmd += ["-filter_complex", ";".join(fl), "-map", prev, "-map", f"{len(durs)}:a",
            "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-r", "30",
            "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", mp4]
    subprocess.run(cmd, check=True)
    print("reel:", mp4, f"({total:.1f}s)")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

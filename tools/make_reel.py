"""Build a 9:16 animated Reel (MP4 + synthesized BGM) and optional Pinterest pin PNG from a JSON spec.
usage: python3 make_reel.py spec.json outdir
spec: {"slug", "lang": "en|zh|ja", "mood": "calm|bright", "seed", "hangul"?, "frames": [...], "pin"?: {...}}
frame types: hook | step | list | statement | cta   (fields: see README in RUNBOOK / existing specs)

Visual system "Rice mist & celadon" (v2, 2026-10-01):
  rice #EEF0EA (light ground) · pine #1E2B27 (ink / dark ground) · celadon #9DBDB0 · celadon-deep #3F6B5E
  blush #F2C9BE · mist #C9D6D0
  Type: Noto Sans CJK Black for display, Noto Sans CJK Regular/Medium for text,
        Noto Serif CJK KR Black for the oversized vertical Hangul topic word (the one signature element).
  Motion: one entrance per slide (text block rises in, staggered), Hangul word drifts slowly; crossfade between slides.
"""
import json, os, re, sys, subprocess, html, shutil

C = dict(rice="#EEF0EA", pine="#1E2B27", celadon="#9DBDB0", deep="#3F6B5E", blush="#F2C9BE",
         mist="#C9D6D0", pine2="#2C3D38", soft="#B9CCC4", muted="#4F5F5A")
FONTS = {
    "en": ("'Noto Sans CJK KR','Noto Sans CJK SC',sans-serif"),
    "zh": ("'Noto Sans CJK SC','Noto Sans CJK KR',sans-serif"),
    "ja": ("'Noto Sans CJK JP','Noto Sans CJK KR',sans-serif"),
}
HANGUL_FONT = "'Noto Serif CJK KR',serif"
W, H, FPS, XF = 1080, 1920, 24, 0.4
BPM = {"calm": 84, "bright": 96}   # must match tools/bgm.py
LANG, SANS = "en", FONTS["en"]

def e(s): return html.escape(str(s))
def plain(s): return e(str(s).replace("*", ""))  # v2: no single-word color accents

def hangul_of(spec):
    if spec.get("hangul"): return spec["hangul"]
    for f in spec["frames"]:
        k = f.get("kicker", "")
        m = re.match(r"\s*([가-힣 ]+)", k)
        if m and m.group(1).strip(): return m.group(1).strip()
    return ""

def page(bg, fg, inner, wm="", wm_color="", progress=(0, 1), dur=3.0, dark=False):
    i, n = progress
    segs = "".join(
        f'<span style="flex:1;height:6px;border-radius:3px;background:{(C["rice"] if dark else C["pine"]) if k <= i else (C["pine2"] if dark else C["mist"])}"></span>'
        for k in range(n))
    wm_html = (f'<div class="wm" style="color:{wm_color}">{e(wm)}</div>' if wm else "")
    # hook slide (i == 0) is fully visible from frame 0: viewers decide in ~1 s (FB data 2026-10-03: avg watch 1.1-1.8 s)
    entrance = "" if i == 0 else ".block>*{animation:rise .6s cubic-bezier(.2,.7,.2,1) both}"
    return f"""<!doctype html><html lang="{LANG}"><head><meta charset="utf-8"><style>
html,body{{margin:0;width:{W}px;height:{H}px;overflow:hidden}}
body{{background:{bg};color:{fg};font-family:{SANS};-webkit-font-smoothing:antialiased}}
.root{{position:relative;width:{W}px;height:{H}px;overflow:hidden}}
.bar{{position:absolute;left:96px;right:160px;top:236px;display:flex;gap:10px}}
.wm{{position:absolute;right:-40px;top:300px;writing-mode:vertical-rl;font-family:{HANGUL_FONT};font-weight:900;
     font-size:400px;line-height:1;letter-spacing:-10px;white-space:nowrap;animation:drift {dur}s linear both}}
.block{{position:absolute;left:96px;right:200px;top:560px;bottom:440px;display:flex;flex-direction:column;justify-content:center;gap:40px}}
{entrance}
.block>*:nth-child(2){{animation-delay:.12s}} .block>*:nth-child(3){{animation-delay:.24s}}
.block>*:nth-child(4){{animation-delay:.36s}} .block>*:nth-child(5){{animation-delay:.48s}}
h1,h2,p{{margin:0}}
.d{{font-weight:900;letter-spacing:-3px;line-height:1.02}}
@keyframes rise{{from{{opacity:0;transform:translateY(36px)}}to{{opacity:1;transform:none}}}}
@keyframes drift{{from{{transform:translateY(0)}}to{{transform:translateY(-70px)}}}}
</style></head><body><div class="root">{wm_html}<div class="bar">{segs}</div><div class="block">{inner}</div></div></body></html>"""

def f_hook(f, ctx):
    inner = (f'<p style="font-size:40px;font-weight:500;color:{C["celadon"]}">{plain(f.get("kicker",""))}</p>'
             f'<h1 class="d" style="font-size:132px">{plain(f["title"])}</h1>'
             f'<p style="font-size:50px;line-height:1.35;color:{C["soft"]}">{plain(f.get("sub",""))}</p>')
    return page(C["pine"], C["rice"], inner, ctx["wm"], C["pine2"], ctx["prog"], ctx["dur"], dark=True)

def f_step(f, ctx):
    inner = (f'<h2 class="d" style="font-size:124px">{plain(f["title"])}</h2>'
             f'<p style="font-size:60px;line-height:1.25;font-weight:700;color:{C["deep"]}">{plain(f.get("line",""))}</p>'
             f'<p style="font-size:44px;line-height:1.4;color:{C["muted"]}">{plain(f.get("sub",""))}</p>')
    return page(C["rice"], C["pine"], inner, ctx["wm"], C["mist"], ctx["prog"], ctx["dur"])

def f_list(f, ctx):
    title = f'<h2 class="d" style="font-size:96px">{plain(f["title"])}</h2>' if f.get("title") else ""
    rows = "".join(
        f'<div style="display:flex;align-items:baseline;gap:32px">'
        f'<span style="font-size:56px;font-weight:900;color:{C["deep"]};min-width:44px">{i+1}</span>'
        f'<span style="font-size:76px;font-weight:700;line-height:1.12;letter-spacing:-1px">{plain(t)}</span></div>'
        for i, t in enumerate(f["items"]))
    rows = f'<div style="display:flex;flex-direction:column;gap:30px">{rows}</div>'
    foot = f'<p style="font-size:44px;line-height:1.4;color:{C["muted"]}">{plain(f["sub"])}</p>' if f.get("sub") else ""
    return page(C["rice"], C["pine"], title + rows + foot, ctx["wm"], C["mist"], ctx["prog"], ctx["dur"])

def f_statement(f, ctx):
    lines = "".join(f'<h2 class="d" style="font-size:150px">{plain(l)}</h2>' for l in f["lines"])
    lines = f'<div style="display:flex;flex-direction:column;gap:8px">{lines}</div>'
    sub = f'<p style="font-size:52px;line-height:1.35;color:{C["soft"]}">{plain(f.get("sub",""))}</p>'
    return page(C["pine"], C["rice"], lines + sub, ctx["wm"], C["pine2"], ctx["prog"], ctx["dur"], dark=True)

def f_cta(f, ctx):
    label = f.get("code_label", "Extra 5% off with code")
    where = f.get("where_html", "at checkout on <b>Olive Young Global</b><br>@oliveyoung_global")
    inner = (f'<h2 class="d" style="font-size:112px">{plain(f.get("title","Try it tonight."))}</h2>'
             f'<div style="align-self:flex-start;padding:44px 56px 48px;border-radius:120px;background:{C["rice"]};color:{C["pine"]};'
             f'display:flex;flex-direction:column;gap:6px;box-shadow:0 0 0 6px {C["pine"]}">'
             f'<span style="font-size:46px;font-weight:700;color:{C["deep"]}">{e(label)}</span>'
             f'<span style="font-size:118px;font-weight:900;letter-spacing:2px;line-height:1">KBEAUTY73</span></div>'
             f'<p style="font-size:46px;line-height:1.4">{where}</p>'
             f'<p style="font-size:30px;color:{C["pine2"]}">{e(f.get("tags","#oliveyoungaffiliate #ad"))}</p>')
    return page(C["celadon"], C["pine"], inner, ctx["wm"], "#B3CDC3", ctx["prog"], ctx["dur"])

RENDER = {"hook": f_hook, "step": f_step, "list": f_list, "statement": f_statement, "cta": f_cta}

def pin_html(p, wm):
    steps = "".join(
        f'<div style="padding:34px 36px;border-radius:28px;background:{C["rice"] if i==0 else "#E2EAE6"};display:flex;flex-direction:column;gap:12px">'
        f'<span style="font-size:30px;font-weight:900;color:{C["deep"]}">{i+1}</span>'
        f'<span style="font-size:42px;font-weight:900;line-height:1.1;letter-spacing:-1px">{plain(s["title"])}</span>'
        f'<span style="font-size:26px;line-height:1.5;color:{C["muted"]}">{plain(s["body"])}</span></div>'
        for i, s in enumerate(p["steps"][:2]))
    avoid = ""
    if p.get("avoid"):
        items = "".join(f'<li style="margin:0 0 10px">{plain(t)}</li>' for t in p["avoid"])
        avoid = (f'<div><p style="font-size:30px;font-weight:900;margin:0 0 12px">Skip these</p>'
                 f'<ul style="margin:0;padding-left:34px;font-size:29px;line-height:1.4">{items}</ul></div>')
    note = f'<p style="font-size:28px;line-height:1.45;color:{C["muted"]}">{plain(p["note"])}</p>' if p.get("note") else ""
    wm_html = (f'<div style="position:absolute;right:-30px;top:40px;writing-mode:vertical-rl;font-family:{HANGUL_FONT};font-weight:900;'
               f'font-size:300px;line-height:1;letter-spacing:-8px;color:{C["pine2"]};white-space:nowrap">{e(wm)}</div>') if wm else ""
    return f"""<!doctype html><html lang="{LANG}"><head><meta charset="utf-8"><style>
html,body{{margin:0;width:1000px;height:1500px;overflow:hidden;background:#F5F7F3;color:{C['pine']};font-family:{SANS}}}
p,h1{{margin:0}}</style></head><body>
<div style="width:1000px;height:1500px;display:flex;flex-direction:column">
<div style="position:relative;overflow:hidden;padding:80px 72px 64px;background:{C['pine']};color:{C['rice']};display:flex;flex-direction:column;gap:22px">
{wm_html}
<p style="position:relative;font-size:30px;font-weight:500;color:{C['celadon']}">{plain(p.get('kicker','Korean skincare guide'))}</p>
<h1 style="position:relative;font-size:84px;line-height:1.04;font-weight:900;letter-spacing:-2px;max-width:760px">{plain(p['title'])}</h1>
<p style="position:relative;font-size:34px;line-height:1.35;color:{C['soft']};max-width:720px">{plain(p.get('sub',''))}</p></div>
<div style="flex-grow:1;padding:52px 72px;display:flex;flex-direction:column;gap:36px">
<div style="display:grid;grid-template-columns:1fr 1fr;gap:24px">{steps}</div>{avoid}{note}</div>
<div style="padding:40px 72px 48px;background:{C['celadon']};display:flex;justify-content:space-between;align-items:flex-end">
<div style="display:flex;flex-direction:column;gap:4px"><span style="font-size:28px;font-weight:500">Extra 5% off at Olive Young Global checkout</span>
<span style="font-size:68px;font-weight:900;letter-spacing:2px;line-height:1.05">KBEAUTY73</span></div>
<span style="font-size:24px">#ad</span></div>
</div></body></html>"""

SHOT_JS = r"""
const { chromium } = require('playwright');
(async () => {
  const jobs = JSON.parse(require('fs').readFileSync(process.argv[2], 'utf8'));
  const b = await chromium.launch();
  for (const j of jobs) {
    const p = await b.newPage({ viewport: { width: j.w, height: j.h } });
    await p.goto('file://' + j.html); await p.evaluate(() => document.fonts.ready);
    if (!j.frames) { await p.screenshot({ path: j.png }); await p.close(); continue; }
    for (let k = 0; k < j.frames; k++) {
      const t = k * 1000 / j.fps;
      await p.evaluate((t) => document.getAnimations().forEach(a => { a.pause(); a.currentTime = t; }), t);
      await p.screenshot({ path: j.pattern.replace('%04d', String(k).padStart(4, '0')) });
    }
    await p.close();
  }
  await b.close();
})();
"""

def main(spec_path, out):
    global LANG, SANS
    spec = json.load(open(spec_path)); os.makedirs(out, exist_ok=True)
    LANG = spec.get("lang", "en"); SANS = FONTS.get(LANG, FONTS["en"])
    wm = hangul_of(spec)
    here = os.path.dirname(os.path.abspath(__file__))
    frames = spec["frames"]; n = len(frames)
    jobs, durs = [], []
    for i, f in enumerate(frames):
        # beat grid: each slide = whole beats + crossfade, so every cut lands on a beat of the BGM
        beat = 60.0 / BPM[spec.get("mood", "calm")]
        nb = max(2, round((float(f.get("dur", 3)) - XF) / beat))
        d = nb * beat + XF; durs.append(d)
        hp = os.path.abspath(os.path.join(out, f"frame{i+1}.html"))
        open(hp, "w").write(RENDER[f["type"]](f, dict(wm=wm, prog=(i, n), dur=d)))
        sd = os.path.abspath(os.path.join(out, f"seq{i+1}")); shutil.rmtree(sd, ignore_errors=True); os.makedirs(sd)
        jobs.append(dict(html=hp, w=W, h=H, fps=FPS, frames=int(round(d * FPS)), pattern=os.path.join(sd, "%04d.png")))
    if spec.get("pin"):
        hp = os.path.abspath(os.path.join(out, "pin.html")); open(hp, "w").write(pin_html(spec["pin"], wm))
        jobs.append(dict(html=hp, png=os.path.abspath(os.path.join(out, "pin.png")), w=1000, h=1500))
    jf = os.path.join(out, "_jobs.json"); json.dump(jobs, open(jf, "w"))
    js = os.path.join(out, "_shot.js"); open(js, "w").write(SHOT_JS)
    env = dict(os.environ, NODE_PATH=subprocess.check_output(["npm", "root", "-g"]).decode().strip())
    subprocess.run(["node", js, jf], check=True, env=env)
    # cover = the hook slide once its entrance has finished
    last = sorted(os.listdir(os.path.join(out, "seq1")))[-1]
    shutil.copy(os.path.join(out, "seq1", last), os.path.join(out, "frame1.png"))

    total = sum(durs) - XF * (n - 1)
    wav = os.path.join(out, "bgm.wav")
    raw = os.path.join(out, "bgm_raw.wav")
    subprocess.run([sys.executable, os.path.join(here, "bgm.py"), raw, f"{total:.2f}", str(spec.get("seed", 1)), spec.get("mood", "calm")], check=True)
    # loudness: -14 LUFS integrated, -1.5 dBTP (Instagram/TikTok/YouTube target)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "44100", wav], check=True)
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    for i in range(n):
        cmd += ["-framerate", str(FPS), "-i", os.path.join(out, f"seq{i+1}", "%04d.png")]
    cmd += ["-i", wav]
    fl = [f"[{i}:v]fps=30,scale={W}:{H},setsar=1,format=yuv420p[s{i}]" for i in range(n)]
    prev, off = "[s0]", 0.0
    for i in range(1, n):
        off += durs[i-1] - XF
        fl.append(f"{prev}[s{i}]xfade=transition=fade:duration={XF}:offset={off:.2f}[x{i}]"); prev = f"[x{i}]"
    mp4 = os.path.join(out, f"{spec.get('slug','reel')}.mp4")
    cmd += ["-filter_complex", ";".join(fl), "-map", prev, "-map", f"{n}:a",
            "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-r", "30",
            "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", mp4]
    subprocess.run(cmd, check=True)
    for i in range(n): shutil.rmtree(os.path.join(out, f"seq{i+1}"), ignore_errors=True)
    print("reel:", mp4, f"({total:.1f}s)")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

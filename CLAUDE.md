# CLAUDE.md — kbeautysave-media

Daily content pipeline for the @kbeautysave Olive Young Global affiliate accounts. A weekday scheduled Claude session clones this repo, follows `RUNBOOK.md`, renders a reel, and schedules it in Metricool. Read `RUNBOOK.md` before doing anything; it is the source of truth for the daily steps and content rules.

## Stack
- Python 3 (numpy, scipy) — `tools/bgm.py` synthesizes royalty-free BGM.
- Node + Playwright (global install, Chromium at /opt/pw-browsers) — renders HTML slides frame by frame.
- ffmpeg — assembles slides, crossfades, loudness-normalizes audio (-14 LUFS).
- Fonts: Noto Sans/Serif CJK (KR/SC/JP) from the system. No web fonts (network is blocked in the workspace).
- Publishing: Metricool connector (brand/blogId 7131683). Media is served from this public repo via raw.githubusercontent.com URLs pinned to a commit hash.

## Layout
- `tools/make_reel.py` — spec JSON → animated 9:16 reel (+ cover `frame1.png`, + Pinterest `pin.png` if the spec has `pin`). Visual system v2 "rice mist & celadon"; Hangul topic word watermark; beat-grid timing.
- `tools/bgm.py` — BGM generator (moods: calm 84 bpm, bright 96 bpm; keep in sync with `BPM` in make_reel.py).
- `tools/check_post.py` — quality gate. Must pass before anything is scheduled.
- `specs/YYYY-MM-DD-<slug>.json` (+ `-zh.json` for Weibo) — one spec per day.
- `media/YYYY-MM-DD/` — published files: `reel.mp4`, `reel_zh.mp4`, `cover.png`, `pin.png`, `post.md` (the user's manual posting kit).
- `topics.md` — topic log; never repeat a topic from the last 30 entries.
- `out/` — scratch renders (git-ignored).

## Commands
```
python3 tools/make_reel.py specs/<file>.json out/<date>          # render
python3 tools/check_post.py --spec specs/<file>.json --video out/<date>/<slug>.mp4 --caption caption.txt [--platform tiktok|weibo|pinterest]
```

## Never
- Never put the affiliate link or "link in bio" anywhere (no-link mode, user decision 2026-09-28).
- Never claim medical effects, never invent personal experience or testimonials.
- Never omit `#oliveyoungaffiliate` + `#ad` (Weibo `#广告#`), or the code benefit ("Extra 5% off with code KBEAUTY73").
- Never schedule if `check_post.py` fails — fix and re-render, or stop and tell the user.
- Never double-post: check Metricool `getScheduledPosts` for the day first.
- Don't hand-build images or videos outside `tools/`; change the generator instead so every day stays consistent.
- Don't force-push or rewrite history on `main` (published raw URLs point at commits).

## Working on the tools (spec → plan → build → test → review)
Changes to `tools/` go in small steps: describe the change, render one existing spec before/after, extract stills (`ffmpeg -ss`) and look at them, run `check_post.py`, then commit. Keep old specs rendering — they are the regression set.

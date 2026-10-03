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
- Never put the affiliate link (a URL) in any caption, comment, frame or pin. Exception (user decision 2026-10-03): Instagram/Facebook captions say the code and shopping link are **in the profile** — the user keeps them in the bio. Other platforms stay code-only.
- Never claim medical effects, never invent personal experience or testimonials.
- Never omit `#oliveyoungaffiliate` + `#ad` (Weibo `#广告#`). Code benefit ("Extra 5% off with code KBEAUTY73") goes in TikTok/X/Weibo/Pinterest copy and the video CTA; IG/FB captions point to the profile instead and must keep `@oliveyoung_global` on IG.
- Never schedule if `check_post.py` fails — fix and re-render, or stop and tell the user.
- Never double-post: check Metricool `getScheduledPosts` for the day first.
- Don't hand-build images or videos outside `tools/`; change the generator instead so every day stays consistent.
- Don't force-push or rewrite history on `main` (published raw URLs point at commits).

## Scope of the daily scheduled run (guardrails)
The unattended daily run may write only: `specs/`, `media/`, `topics.md`, `LEARNINGS.md` (the weekly review run: `reports/` and `LEARNINGS.md` only) — and schedule at most **one** Metricool post per weekday (never more; check the month's count stays within the free plan's 20).
It must NOT edit `tools/`, `RUNBOOK.md` or `CLAUDE.md` on its own. If it thinks a rule or tool should change, it writes the proposal in `LEARNINGS.md` and in its message to the user, and a human-present session makes the change. Every change is a normal git commit, so the history is the audit log.

## Weekly review (Observe step)
Every Monday a separate scheduled run pulls last week's performance from Metricool (Instagram reels IGRE*, TikTok posts TKPO*, Facebook reels) and writes `reports/YYYY-Www.md`: one row per post (date, topic, views, reach, likes, saves, shares, comments, watch/retention where available), the top and bottom posts, what the winners have in common (hook style, topic type, length), and 2–3 concrete suggestions for this week's topics/hooks. Durable lessons go into `LEARNINGS.md`. The daily run reads the latest report before picking a topic.
Data sanity: a post with 0 views/reach 48 h+ after publishing is almost always a data/permission problem (or a platform restriction), not a real result — flag it to the user instead of drawing conclusions from it.

## LEARNINGS.md
Append-only log of what went wrong or what was learned (failed schedules, gate failures, platform errors, things the user corrected). One dated line each, newest at the bottom. Read it before a run so the same mistake isn't repeated.

## Working on the tools (spec → plan → build → test → review)
Changes to `tools/` go in small steps: describe the change, render one existing spec before/after, extract stills (`ffmpeg -ss`) and look at them, run `check_post.py`, then commit. Keep old specs rendering — they are the regression set.

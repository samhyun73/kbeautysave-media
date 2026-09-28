# kbeautysave daily automation — runbook

Owner: kbeautysave (Olive Young Global affiliate). Instagram @kbeautysave, Facebook page "For My Health", TikTok & Pinterest @kbeautysave, Weibo (manual).

## Fixed facts
- Affiliate link: https://global.oliveyoung.com/if/rd?su=Q7NAABDP
- Code: **KBEAUTY73**
- Required tags: `#oliveyoungaffiliate` + `#ad` on every post; mention `@oliveyoung_global` on Instagram.
- Metricool brand (blogId): `7131571`, timezone `Asia/Seoul`. Free plan = 20 scheduled posts / month.
- Media is served from this public repo: `https://raw.githubusercontent.com/samhyun73/kbeautysave-media/main/<path>`

## Schedule
- **Mon–Fri**: one Reel → Instagram (REEL) + Facebook (REEL) + TikTok, one Metricool post, published 19:00 KST the same day.
- **Mon / Wed / Fri**: also a Pinterest pin (1000×1500) — sent to the user to upload manually (keeps within the free-plan post limit).
- **Every weekday**: Weibo caption (Simplified Chinese) sent to the user to post manually with the same video.
- Weekends: nothing.

## Weekly topic rotation
Mon K-beauty basics · Tue skin-type tips · Wed ingredient explainer · Thu Korean beauty culture · Fri routine idea.
Check `topics.md` before choosing; never repeat a topic from the last 30 entries. Append the chosen topic after posting.

## Content rules (must follow)
1. Educational first; the code appears on the last frame and in the caption, never pushy.
2. No medical claims ("treats acne", "removes wrinkles"). Use "helps soothe", "hydrating", etc.
3. Never invent personal experience or testimonials ("I've used this for months…"). Describe products as "popular in Korea", "loved by Korean skincare fans".
4. Only name products that are well known and widely sold; if unsure it is on Olive Young Global, talk about the product type instead of a brand.
5. Links: Instagram/TikTok captions say "link in bio" (no URL). Facebook: code in caption, affiliate link as `firstCommentText`. Pinterest: link goes in the pin link field. Weibo: code only, no link.
6. Word each platform's caption differently (no identical copy-paste).
7. Frames: max ~12 words each; hook frame first (a surprising or "you're doing it wrong" line), CTA frame last.

## Daily steps
1. Pick today's topic (rotation + `topics.md`).
2. Write `specs/YYYY-MM-DD-<slug>.json` (see existing specs; frame types: hook, step, list, statement, cta; 5–7 frames, 14–18 s total; vary `seed`, `mood` calm|bright). On Mon/Wed/Fri add a `"pin"` object: `{title, sub, kicker, steps:[{title, body},{title, body}], avoid:[...], note}`.
3. Render: `python3 tools/make_reel.py specs/<file>.json out/<date>` → copy `out/<date>/<slug>.mp4` to `media/<date>/reel.mp4`, `frame1.png` to `media/<date>/cover.png`, and `pin.png` (if any) to `media/<date>/pin.png`.
   Needs: python3 + numpy + scipy, ffmpeg, node + playwright (global), fonts "Noto Serif CJK KR"/"Noto Sans CJK KR".
4. Commit & push to `main`; verify the raw URL returns 200 before scheduling.
5. Schedule in Metricool (`createScheduledPost`, blogId 7131571): providers instagram + facebook + tiktok, `media: [raw reel URL]`, `instagramData.type: "REEL"`, `facebookData.type: "REEL"`, tiktokData `commercialContentThirdParty: true`, publish 19:00 KST today (if already past, next weekday 19:00). Text = Instagram-style caption; `firstCommentText` = "Shop here 👉 <affiliate link> · Code KBEAUTY73 #ad".
6. Message the user: what was scheduled (with plannerUrl), the Weibo caption (≤140 chars for comments; post body can be longer), and on pin days the pin image + title + description + link + suggested board "Korean Skincare Routine".
7. Append `YYYY-MM-DD | topic | status` to `topics.md`, commit, push.
8. Delete media folders older than 60 days to keep the repo small.

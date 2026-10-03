# kbeautysave daily automation — runbook

Owner: kbeautysave (Olive Young Global affiliate). Instagram @kbeautysave, Facebook page "For My Health", TikTok & Pinterest @kbeautysave, Weibo (manual).

## Fixed facts
- Affiliate link: https://global.oliveyoung.com/if/rd?su=Q7NAABDP — currently NOT used anywhere (see rule 5)
- Code: **KBEAUTY73** = **extra 5% off** at Olive Young Global checkout (confirmed by user 2026-10-01). Always state the benefit: EN "Extra 5% off with code KBEAUTY73", ZH "额外95折 优惠码 KBEAUTY73" (cta `code_label`: "额外95折 优惠码").
- Required tags: `#oliveyoungaffiliate` + `#ad` on every post; mention `@oliveyoung_global` on Instagram.
- Metricool brand (blogId): `7131683` (Metricool userId 5514763; switched from 7131571 on 2026-09-29), timezone `Asia/Seoul`. Free plan = 20 scheduled posts / month.
- Media is served from this public repo: `https://raw.githubusercontent.com/samhyun73/kbeautysave-media/main/<path>`

## Schedule
- **Mon–Fri**: one Reel → Instagram (REEL) + Facebook (REEL), one Metricool post, published 19:00 KST the same day.
- **TikTok = MANUAL (user decision 2026-10-03)**: auto-posted TikToks (09-30..10-02) got 0 views with no violation shown, so the user uploads `reel.mp4` in the TikTok app by hand. Put a TikTok section in `post.md` (caption + reminder to switch on "Content disclosure → Branded content"). Never add `tiktok` to Metricool providers until the user says so.
- **Mon / Wed / Fri**: also a Pinterest pin (1000×1500) — sent to the user to upload manually (keeps within the free-plan post limit).
- **Every weekday**: Weibo caption + Chinese-text reel (`reel_zh.mp4`) sent to the user to post manually.
- **Every weekday**: X (Twitter) post text sent to the user to post manually with the English `reel.mp4` (X is not connected to Metricool).
- **Sat / Sun (manual-only weekend kit, user decision 2026-10-03):** no Metricool post (keeps the free-plan quota for weekdays). Make the same content set — English `reel.mp4`, Chinese `reel_zh.mp4`, Pinterest `pin.png`, `post.md` with X / Weibo / Pinterest copy — and send it to the user, who posts X, Pinterest and Weibo by hand. See "Weekend steps" below.

## Weekly topic rotation
Mon K-beauty basics · Tue skin-type tips · Wed ingredient explainer · Thu Korean beauty culture · Fri routine idea · Sat myth vs fact (a common skincare mix-up, gently corrected) · Sun seasonal / weekly self-care (what Koreans do this time of year).
Check `topics.md` before choosing; never repeat a topic from the last 30 entries. Append the chosen topic after posting.

## Content rules (must follow)
1. Educational first; the code appears on the last frame and in the caption, never pushy.
2. No medical claims ("treats acne", "removes wrinkles"). Use "helps soothe", "hydrating", etc.
3. Never invent personal experience or testimonials ("I've used this for months…"). Describe products as "popular in Korea", "loved by Korean skincare fans".
4. Only name products that are well known and widely sold; if unsure it is on Olive Young Global, talk about the product type instead of a brand.
5. **NO LINKS (account-safety mode, user decision 2026-09-28, until the user says otherwise):** never put the affiliate link (or "link in bio") anywhere — not in captions, first comments, pin link fields, or frames. Promote with the code only: "Use code KBEAUTY73 at checkout on Olive Young Global (@oliveyoung_global)". `firstCommentText` stays empty.
   **IG/FB exception (user decision 2026-10-03):** the Instagram/Facebook caption does NOT carry the code line. End it with a profile pointer instead, e.g. `🛍️ Code + shopping link are in my profile 👆 · extra 5% off at @oliveyoung_global`, then the hashtags. Never paste the URL in the caption itself.
6. Word each platform's caption differently (no identical copy-paste).
7. Frames: max ~12 words each; hook frame first, CTA frame last. **Hook rules (FB data 2026-10-03: avg watch ~1.2 s, so the first second decides everything):** the hook title is a question or a "you're doing X wrong" / myth line the viewer wants answered (e.g. "Oily skin doesn't need moisturizer?", "You're applying toner wrong"), ≤7 words if possible, no slow intro. It renders on a bright blush background and is fully visible at frame 0 (tools/make_reel.py v2.1). Keep the `sub` as a short teaser ("Korean skincare says otherwise ↓"). Zh hook titles ≤8 characters, ending in a question.
8. Visual system v2 (tools/make_reel.py, 2026-10-01): rice-mist/pine/celadon palette, heavy sans display, the topic's **Korean word as an oversized vertical Hangul watermark** (the signature element), animated entrances (except the hook, which is static from frame 0 on a bright blush ground), progress bar. Every spec (en AND zh) must set `"hangul"` to the topic's short Korean word (e.g. "이중세안", "병풀", "유리 피부"). Kickers in sentence case (no ALL CAPS); don't use `*word*` accents (they render plain). Use numbered lists only for real sequences.

## Manual-post style (X, Weibo, Pinterest — the posts the user publishes by hand)
User preference (2026-10-01): **lots of emojis**. Aim for 6–10 per post: one at the start of most lines, emoji bullets for steps (1️⃣ 2️⃣ 3️⃣ or ✅ 💧 🧴 ☀️), a ✨/💕/🔖 near the CTA. Keep them on-topic (skincare, water, plants, sun, sparkles, hearts, Korea 🇰🇷) and never inside the code or hashtags. X still has to fit 280 weighted chars (emojis count double) — trim words before emojis. The auto-scheduled IG/FB/TikTok captions keep their current moderate emoji use.

## Daily steps
0. Call Metricool `getScheduledPosts` (brandId 7131683, today 00:00–23:59 KST). If a Reel is already scheduled for today, skip steps 1–5 (only send the Weibo caption if not already sent) and stop.
1. Pick today's topic (rotation + `topics.md`), informed by the latest `reports/` file and `LEARNINGS.md` (favor topic types and hook styles that performed best).
2. Write `specs/YYYY-MM-DD-<slug>.json` (see existing specs; frame types: hook, step, list, statement, cta; 5–7 frames, 14–18 s total; vary `seed`, `mood` calm|bright). On Mon/Wed/Fri add a `"pin"` object: `{title, sub, kicker, steps:[{title, body},{title, body}], avoid:[...], note}`.
3. Render: `python3 tools/make_reel.py specs/<file>.json out/<date>` → copy `out/<date>/<slug>.mp4` to `media/<date>/reel.mp4`, `frame1.png` to `media/<date>/cover.png`, and `pin.png` (if any) to `media/<date>/pin.png`.
   Needs: python3 + numpy + scipy, ffmpeg, node + playwright (global), fonts "Noto Serif CJK KR"/"Noto Sans CJK KR".
3b. **Weibo Chinese reel (every weekday):** write `specs/YYYY-MM-DD-<slug>-zh.json` — same frames translated to natural Simplified Chinese, `"lang": "zh"`, no `pin`; the cta frame sets `"code_label": "额外95折 优惠码"`, `"where_html": "在 <b>Olive Young Global</b><br>结账时输入"`, `"tags": "#广告"` (see `specs/2026-09-30-centella-zh.json`). Render it and copy the mp4 to `media/<date>/reel_zh.mp4`. Keep Chinese lines short (≈10 characters per line on titles). Same content rules (no medical claims, no links).
3c. **Quality gate (must pass — "if it can't be verified, it doesn't ship"):** write each caption to a temp file and run
   `python3 tools/check_post.py --spec specs/<file>.json --video media/<date>/reel.mp4 --caption <ig caption> --platform instagram`,
   then `--caption <tiktok title> --platform tiktok`, and for Weibo `--spec specs/<file>-zh.json --video media/<date>/reel_zh.mp4 --caption <weibo text> --platform weibo`
   (pin days: `--caption <pin description> --platform pinterest`), and the X post `--caption <x text> --platform x`. Any FAIL → fix the spec/caption, re-render, re-run. If still failing, do not schedule; tell the user what failed.
   Also extract 4–6 stills per video and look at them (layout problems the script can't see).
4. Commit & push to `main`; verify the raw URL returns 200 before scheduling.
5. Schedule in Metricool (`createScheduledPost`, blogId 7131683): providers instagram + facebook (NOT tiktok — manual, see Schedule), `media: [raw reel URL]`, `videoThumbnailUrl: [raw cover.png URL]` (cover = hook slide, auto-saved as frame1.png), `instagramData.type: "REEL"`, `facebookData.type: "REEL"`, facebookData `title`, publish 19:00 KST today (if already past, next weekday 19:00). Text = caption with the code (no link); `firstCommentText` = "" (empty).
6. Write `media/<date>/post.md` (Korean headings; see `media/2026-09-30/post.md` as the template): links to reel.mp4 / reel_zh.mp4 / pin.png, a **TikTok section** (short caption ≤150 chars with the code + 5% benefit, `#oliveyoungaffiliate #ad` + 2–3 topic hashtags, moderate emojis, no link; steps: upload reel.mp4 in the TikTok app → 더보기 옵션 → 콘텐츠 공개 → 브랜드 콘텐츠 ON → 게시, ideally 19:00–21:00 KST), an **X section** (English, ≤280 weighted chars, a punchy 1-line hook + 1–2 lines of value + "Extra 5% off with code KBEAUTY73 at Olive Young Global" + `#oliveyoungaffiliate #ad` + 1–2 topic hashtags, no link; tell them to attach reel.mp4), the Weibo caption (tell them to attach reel_zh.mp4) in a code block, and on pin days the Pinterest board, title and description in code blocks (link field empty). Commit & push it — this is the user's daily "posting kit" page at https://github.com/samhyun73/kbeautysave-media/tree/main/media/<date>.
   Then message the user: what was scheduled (with plannerUrl), the posting-kit link, the Weibo caption (≤140 chars for comments; post body can be longer), and on pin days the pin image + title + description (code only, leave the pin link field empty) + suggested board "Korean Skincare Routine".
7. Append `YYYY-MM-DD | topic | status` to `topics.md`, commit, push.
8. Delete media folders older than 60 days to keep the repo small.

## Weekend steps (Sat / Sun — manual posting only)
Same as Daily steps with these changes:
- Skip step 0's Metricool check and step 5 (no `createScheduledPost`). Nothing goes to IG / FB / TikTok.
- Step 2: always add a `"pin"` object (a pin every weekend day).
- Step 3c: run the gate for `--platform x`, `--platform pinterest` and `--platform weibo` (Instagram/TikTok captions are not needed).
- Step 6: `post.md` header says "주말 · 직접 게시 (X · Pinterest · 웨이보)". Message the user with the posting-kit link, X text, Weibo caption, pin title + description (board "Korean Skincare Routine", link field empty), and send `pin.png`, `reel.mp4`, `reel_zh.mp4` with SendUserFile.
- Step 7: log status as `manual kit (X + Pinterest + Weibo)`.

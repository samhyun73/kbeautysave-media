# kbeautysave daily automation — runbook

Owner: kbeautysave (Olive Young Global affiliate). Instagram @kbeautysave, Facebook page "For My Health", TikTok & Pinterest @kbeautysave, Weibo (manual).

## Fixed facts
- Affiliate link: https://global.oliveyoung.com/if/rd?su=Q7NAABDP — currently NOT used anywhere (see rule 5)
- Code: **KBEAUTY73** = **extra 5% off** at Olive Young Global checkout (confirmed by user 2026-10-01). Always state the benefit: EN "Extra 5% off with code KBEAUTY73", ZH "额外95折 优惠码 KBEAUTY73" (cta `code_label`: "额外95折 优惠码").
- Required tags: `#oliveyoungaffiliate` + `#ad` on every post; mention `@oliveyoung_global` on Instagram.
- **Publishing = Buffer** (user decision 2026-10-03; Buffer account jkk736540@gmail.com, free plan: 3 channels, max 10 scheduled posts queued at a time — we only ever queue today's 3). Connector `Buffer_kbeauty`. Organization `6ac09e1778721e574b910296` ("My organization"), timezone Asia/Seoul. Channels:
  - Instagram kbeautysave: `6ac09f9eea19ca0bde60715b`
  - Facebook page "For My Health": `6ac09fc4ea19ca0bde607267`
  - YouTube kbeautysave (Shorts): `6ac0a281ea19ca0bde608325`
- Metricool brand (blogId) `7131683` is now **analytics only** (weekly review). Do NOT schedule in Metricool: its free plan counts every network separately (IG+FB = 2 of 20 posts/month) and ran out mid-month.
- Media is served from this public repo: `https://raw.githubusercontent.com/samhyun73/kbeautysave-media/main/<path>`

## Schedule
- **Mon–Fri**: the reel → Instagram (reel) + Facebook (reel) + YouTube (Short), three Buffer posts, all published 19:00 KST the same day.
- **TikTok = MANUAL (user decision 2026-10-03)**: auto-posted TikToks (09-30..10-02) got 0 views with no violation shown, so the user uploads `reel.mp4` in the TikTok app by hand. Put a TikTok section in `post.md` (caption + reminder to switch on "Content disclosure → Branded content"). Never schedule TikTok (Buffer or Metricool) until the user says so.
- **Pinterest = 3 pins every day, Mon–Sun (user decision 2026-10-03)**, posted by hand by the user:
  1. **Video pin** — the day's `reel.mp4` (9:16) with its own Pinterest title + description.
  2. **Image pin A** — `pin.png` (default layout: dark header, steps, "skip these").
  3. **Image pin B** — `pin2.png` (`"layout": "list"`: light ground, 3–5 numbered tips) — a *different angle and keyword* from pin A (e.g. A = "trend/colours", B = "how-to at home").
  Each of the 3 gets a different keyword-rich title (see "Pinterest titles") and its own description; never the same title twice. Boards: nails → "Korean Nail Ideas", hair → "Korean Hair Ideas", makeup → "Korean Makeup Looks", skincare → "Korean Skincare Routine" (tell the user to create a board the first time it's needed). Suggested posting times (US evening = KST morning): 09:00, 12:00 and 22:00 KST, spread out — not all at once. Link field empty.
- **Every weekday**: Weibo caption + Chinese-text reel (`reel_zh.mp4`) sent to the user to post manually.
- **Every weekday**: X (Twitter) post text sent to the user to post manually with the English `reel.mp4` (X is not connected to Buffer).
- **Sat / Sun (manual-only weekend kit, user decision 2026-10-03):** no Buffer post (weekend = manual kit only). Make the same content set — English `reel.mp4`, Chinese `reel_zh.mp4`, Pinterest `pin.png`, `post.md` with X / Weibo / Pinterest copy — and send it to the user, who posts X, Pinterest and Weibo by hand. See "Weekend steps" below.

## Weekly topic rotation
**Direction (user decision 2026-10-03): shift naturally toward Korean nails and hair**, where US Pinterest search volume is far larger than skincare (Pinterest Trends, US, "beauty", 2026-09-29: within "korean" keywords — korean makeup 100, korean nails 73, korean skincare 46, korean haircut/hairstyle/perm 25–30, blush nails korean +100% y/y, korean lash lift +1,000% y/y; across all beauty, nails and hairstyles dominate the top 50). Skincare stays, but as 2 of 5 weekdays. All categories exist on Olive Young Global (Makeup › Nail, Eye › Eyelashes, Lip › Tint; Hair › Treatments, Styling, Color & Perms, Devices).

Mon **K-nails** (jelly nails, blush nails, cat eye, short/simple nails, seasonal colours) · Tue **skincare** by skin type / ingredient (centella and "routine order" are rising terms) · Wed **K-hair** (layered cuts, perms, hair oil/treatment, heatless styling, scalp care as cleansing habit) · Thu **Korean makeup** (blush placement, gradient lips, eye makeup) or beauty culture · Fri **nails or hair**, seasonal (alternate weeks) · Sat myth vs fact (any category, gently corrected) · Sun seasonal self-care / skincare reset.
Nails and hair reels are guides, not personal results: "3 Korean nail trends for fall", "how Koreans ask for a layered cut", "jelly nails at home: 3 steps". Name product *types* (gel nail strips, sheer jelly polish, hair oil, heatless curler) unless the brand is well known and on Olive Young Global.

**Seasonal calendar** (Pinterest search starts rising 6–8 weeks before the peak — post pins 4–6 weeks ahead):
- Oct: fall/October nails (burgundy, plum, brown, dark purple, cat eye), Halloween makeup removal (double cleanse), homecoming hair & makeup prep. Halloween nails peak mid/late Oct.
- Nov: holiday/Christmas nails start rising early Nov (peak 2nd week Dec); skincare products & gift sets peak mid-Nov–early Dec.
- late Dec–early Jan: biggest skincare peak of the year (New Year routine reset; "skincare", "skincare routine", "korean skincare" all top out Dec 30–Jan 6); winter hair braids peak Dec.
- Jan–Feb: Valentine's nails (rise mid-Jan, peak ~Feb 10). Feb–Mar: spring nails (peak late Mar). May–Jun: summer nails (peak early Jun).

**Products to feature** (Olive Young Global best sellers, checked 2026-10-03 — these are well known and on the site, so they may be named; still describe, never claim results):
- Nails: ohora Natural Glow Milk Syrup (sheer milky colour → fits "jelly / milky / blush nails" trends).
- Hair: La'dor Perfumed Hair Oil, Longtake Hair Oil, UNOVE Deep Damage Repair Hair Mask, LABO-H Scalp Strengthening Shampoo (scalp *cleansing* only — never hair-loss or regrowth claims; skip "growth" ampoules).
- Makeup: blush is the biggest group (fwee Cheek Chip, 2aN Dual Cheek, espoir Blur Wear Blush, ABOUT_TONE Skin Layer Fit Blusher, freshian Egg-like Cream Blush); lips (fwee 3D Voluming Gloss & Stay-fit Lip Tint, peripera Mood Glowy Tint, CLIO Crystal Glam Tint); eyes (CLIO / 2aN / WAKEMAKE palettes); no-glue lashes (CORINGCO Toktok Hara, BANILA CO Curly Studio) as the safe at-home answer to the "korean lash lift" trend.
- Skincare: Anua (PDRN line, Heartleaf toner), Torriden Dive In, MEDIHEAL sheet masks, Dr. Althea 345, AESTURA Atobarrier 365, Centellian24 Madeca, SKIN1004 centella (incl. Double Cleansing Duo), BANILA CO Clean It Zero, ma:nyo cleansing oil, ROUND LAB Birch Juice sunscreen.
- Never feature supplements / slimming / "eye bag lift" / glutathione items (health and weight claims).

**Product facts for this week** (from brand pages, 2026-10-03 — use for "how to use", never repeat brand test stats like "+419%" or "−32% split ends"):
- ohora Milk Syrup (nails): milky, glossy "natural glow"; 1 coat = sheer wash, 2–3 coats build colour; quick-dry, no base coat or UV lamp. Shades include Cherry Blossom, Rosehip, Chai, Hazelnut, Berry Jam, Ganache, Meringue. Brand calls it a strengthener — we don't claim it strengthens or repairs nails.
- UNOVE Deep Damage Repair Hair Mask: on damp hair after shampoo, mid-lengths to ends (avoid scalp), leave 1–3 min, rinse; 2–3× a week; quarter-sized amount.
- espoir Blur Wear Blush: soft-matte powder; brand applies it on the cheekbones, blending outwards and upwards; shades Nu Pink, Cortado, Proud Pink, Cream Solar, Dazed Mauve, Caramel Rose (Dazed Mauve / Caramel Rose suit fall — good for a `swatch` frame).
- La'dor Perfumed Hair Oil: a few drops on ends, damp or dry; scented (e.g. Osmanthus, Our Leaf, La Pitta).
The Olive Young Global site renders search/product pages with JavaScript, so WebFetch can't read them; event/home/best-seller listings are readable. Check brand pages for usage facts.

**Starter plan** (adapt to reports; skip any already in topics.md):
- Week of 10-05: Mon milky jelly nails for fall (pin) · Tue Halloween makeup removal = Korean double cleanse (cleansing oils/balms are on sale: ma:nyo, BANILA CO, Dr.G Anpanman balm) · Wed **post-summer hair SOS**: mask + oil routine (pin; OYG runs a "Post-Summer Hair SOS" gift-with-purchase event — UNOVE mask, Mise-en-Scene Glazing Hair Milk, La'dor oil) · Thu Korean blush placement (espoir "Rising Brand Week" 7-day flash sale on the Blur blush set; 2aN Dual Cheek, WAKEMAKE) · Fri burgundy & plum fall nails, Korean style (pin) · Sat myth: "hair oil makes hair greasy" · Sun fall skin reset.
- Week of 10-12: Mon blush nails · Tue centella for sensitive skin · Wed fall hair-oil routine for frizz (pin) · Thu gradient lips in fall "cherry/burgundy" shades (WAKEMAKE Off Cherry, peripera, CLIO, 2aN Dewy Fit Tint) · Fri no-glue lashes vs lash lift (pin).

**Sales, new arrivals, events** (checked 2026-10-03): use them as timely hooks, never as price claims.
- Before choosing the day's topic, the run may WebFetch https://global.oliveyoung.com/event/main and /display/page/new-arrivals to pick up a matching event or collab (e.g. a hair event on a hair day).
- Never put prices or % off in the video; deals change daily. A caption may say "this week's Olive Young Global event" only if the run saw it that same day. Never say the code stacks with a sale (unverified).
- Limited collab packaging (Sanrio, Anpanman, Trolls, Bubble Bobble editions) suits Pinterest "aesthetic" and gift content (Nov–Dec) — show product *types*/brand names only, never characters or logos in our frames.
- K-pop: albums/merch aren't our content. "Idol makeup" angles are fine as Korean makeup *style* (no idol names, photos or likeness).
- Skip supplements, slimming, toothpaste/oral care items in sale lists.

**Pinterest titles**: [specific topic] + Korean + simple/easy/classy + ideas/inspo/aesthetic + year, e.g. "Korean Jelly Nails for Fall 2026: Simple Burgundy Ideas", "Skincare Routine Order: Simple Korean Steps (Aesthetic Guide)". Avoid the bare phrase "Korean skincare routine" (−60% y/y); be specific.
Check `topics.md` before choosing; never repeat a topic from the last 30 entries. Append the chosen topic after posting.

## Content rules (must follow)
1. Educational first; the code appears on the last frame and in the caption, never pushy.
2. No medical claims ("treats acne", "removes wrinkles", "stops/prevents hair loss", "regrows hair", "fixes nail fungus"). Use "helps soothe", "hydrating", "smoother-looking", "glossy", etc. Don't encourage salon procedures at home (lash lifts, perms, bleaching chemicals) — talk about aftercare and everyday products instead.
3. Never invent personal experience or testimonials ("I've used this for months…"). Describe products as "popular in Korea", "loved by Korean skincare fans".
4. Only name products that are well known and widely sold; if unsure it is on Olive Young Global, talk about the product type instead of a brand.
5. **NO LINKS (account-safety mode, user decision 2026-09-28, until the user says otherwise):** never put the affiliate link (or "link in bio") anywhere — not in captions, first comments, pin link fields, or frames. Promote with the code only: "Use code KBEAUTY73 at checkout on Olive Young Global (@oliveyoung_global)". `firstCommentText` stays empty.
   **IG/FB exception (user decision 2026-10-03):** the Instagram/Facebook caption does NOT carry the code line. End it with a profile pointer instead, e.g. `🛍️ Code + shopping link are in my profile 👆 · extra 5% off at @oliveyoung_global`, then the hashtags. Never paste the URL in the caption itself.
6. Word each platform's caption differently (no identical copy-paste).
7. Frames: max ~12 words each; hook frame first, CTA frame last. **Hook rules (FB data 2026-10-03: avg watch ~1.2 s, so the first second decides everything):** the hook title is a question or a "you're doing X wrong" / myth line the viewer wants answered (e.g. "Oily skin doesn't need moisturizer?", "You're applying toner wrong"), ≤7 words if possible, no slow intro. It renders on a bright blush background and is fully visible at frame 0 (tools/make_reel.py v2.1). Keep the `sub` as a short teaser ("Korean skincare says otherwise ↓"). Zh hook titles ≤8 characters, ending in a question.
8. Visual system v2 (tools/make_reel.py, 2026-10-01): rice-mist/pine/celadon palette, heavy sans display, the topic's **Korean word as an oversized vertical Hangul watermark** (the signature element), animated entrances (except the hook, which is static from frame 0 on a bright blush ground), progress bar. Every spec (en AND zh) must set `"hangul"` to the topic's short Korean word (e.g. "이중세안", "병풀", "유리 피부"). Kickers in sentence case (no ALL CAPS); don't use `*word*` accents (they render plain). Use numbered lists only for real sequences.

## Caption voice (all English copy, 2026-10-05)
Write like a person talking to a friend, not a brand bot: short plain sentences, concrete details (shade names, number of coats, minutes). No AI-sounding clichés (delve, elevate, unlock, game-changer, seamless, beauty journey, say goodbye to, "in today's … world") and at most one em dash per caption — the gate blocks both (`check_post.py`, all platforms except Weibo).

## Manual-post style (X, Weibo, Pinterest — the posts the user publishes by hand)
User preference (2026-10-01): **lots of emojis**. Aim for 6–10 per post: one at the start of most lines, emoji bullets for steps (1️⃣ 2️⃣ 3️⃣ or ✅ 💧 🧴 ☀️), a ✨/💕/🔖 near the CTA. Keep them on-topic (skincare, water, plants, sun, sparkles, hearts, Korea 🇰🇷) and never inside the code or hashtags. X still has to fit 280 weighted chars (emojis count double) — trim words before emojis. The auto-scheduled IG/FB/TikTok captions keep their current moderate emoji use.

## Daily steps
0. Call Buffer `list_posts` (organizationId above, dueAt today 00:00–23:59 KST, status scheduled/sending/sent). If today's reel is already queued on a channel, don't queue it again on that channel (never double-post); if all three exist, skip steps 1–5 and only send the posting kit if not already sent. If a channel shows `isDisconnected` in `list_channels`, tell the user which one to reconnect in Buffer.
1. Pick today's topic (rotation + `topics.md`), informed by the latest `reports/` file and `LEARNINGS.md` (favor topic types and hook styles that performed best).
2. If `specs/YYYY-MM-DD-*.json` for today already exists (prepared in a human-present session), use it as-is — still run every gate — and only write what's missing (zh spec, captions). Otherwise write `specs/YYYY-MM-DD-<slug>.json` (see existing specs; frame types: hook, step, list, statement, cta, **swatch** — `{"type":"swatch","title","swatches":[{"name","color":"#hex","sheer":true|false,"finish":"gloss|cat eye|shimmer"}],"sub"}`, 3–4 colours drawn as nail tips; use it on nail/lip/blush colour days, and add the same `swatches` to the pin; 5–7 frames, 14–18 s total; vary `seed`, `mood` calm|bright). Every day add a `"pin"` object `{title, sub, kicker, steps:[{title, body},{title, body}], avoid:[...], note, swatches?}` (→ pin.png) **and** `"pins": [{"layout": "list", kicker, title, sub, items:[{title, body}] ×3–5, swatches?}]` (→ pin2.png) — a different angle and keyword from the first pin.
3. Render: `python3 tools/make_reel.py specs/<file>.json out/<date>` → copy `out/<date>/<slug>.mp4` to `media/<date>/reel.mp4`, `frame1.png` to `media/<date>/cover.png`, and `pin.png` + `pin2.png` to `media/<date>/`.
   Needs: python3 + numpy + scipy, ffmpeg, node + playwright (global), fonts "Noto Serif CJK KR"/"Noto Sans CJK KR".
3b. **Weibo Chinese reel (every weekday):** write `specs/YYYY-MM-DD-<slug>-zh.json` — same frames translated to natural Simplified Chinese, `"lang": "zh"`, no `pin`; the cta frame sets `"code_label": "额外95折 优惠码"`, `"where_html": "在 <b>Olive Young Global</b><br>结账时输入"`, `"tags": "#广告"` (see `specs/2026-09-30-centella-zh.json`). Render it and copy the mp4 to `media/<date>/reel_zh.mp4`. Keep Chinese lines short (≈10 characters per line on titles). Same content rules (no medical claims, no links).
3c. **Quality gate (must pass — "if it can't be verified, it doesn't ship"):** write each caption to a temp file and run
   `python3 tools/check_post.py --spec specs/<file>.json --video media/<date>/reel.mp4 --caption <ig caption> --platform instagram`,
   then `--caption <tiktok title> --platform tiktok`, and for Weibo `--spec specs/<file>-zh.json --video media/<date>/reel_zh.mp4 --caption <weibo text> --platform weibo`
   (Pinterest, every day: run `--platform pinterest` on **each** of the 3 pin descriptions), the X post `--caption <x text> --platform x`, and the YouTube description `--caption <yt description> --platform youtube` (+ the title must be ≤100 chars). Any FAIL → fix the spec/caption, re-render, re-run. If still failing, do not schedule; tell the user what failed.
   Also extract 4–6 stills per video and look at them (layout problems the script can't see).
4. Commit & push to `main`; verify the raw URL returns 200 before scheduling.
5. Schedule in **Buffer** (`create_post`, `schedulingType: "automatic"`, `mode: "customScheduled"`, `dueAt: "<date>T19:00:00+09:00"`; if already past, the next weekday 19:00). Same asset for all three: `assets: [{video: {url: <raw reel URL pinned to the commit>}}]` (the cover is the first frame = the hook slide). Three calls:
   - Instagram `6ac09f9eea19ca0bde60715b`: text = IG caption (profile pointer, `@oliveyoung_global`, no code line), `metadata.instagram: {type: "reel", shouldShareToFeed: true, firstComment: ""}`.
   - Facebook `6ac09fc4ea19ca0bde607267`: text = FB caption (profile pointer, no code line), `metadata.facebook: {type: "reel"}`.
   - YouTube `6ac0a281ea19ca0bde608325`: text = YouTube description (hook line + 2–3 emoji value lines + "🛍️ Extra 5% off with code KBEAUTY73 at Olive Young Global checkout" + `#oliveyoungaffiliate #ad #kbeauty #koreanskincare <topic> #shorts`; no link), `metadata.youtube: {title: <hook-style title ≤100 chars ending in #shorts>, categoryId: "26", madeForKids: false, privacy: "public"}`.
   Check each result's `status` is `scheduled` and `error` is null. Buffer has no YouTube "paid promotion" flag: remind the user to tick it in YouTube Studio after 19:00.
6. Write `media/<date>/post.md` (Korean headings; see `media/2026-09-30/post.md` as the template): links to reel.mp4 / reel_zh.mp4 / pin.png, a **YouTube note** (title + reminder to tick 유료 프로모션 in YouTube Studio), a **TikTok section** (short caption ≤150 chars with the code + 5% benefit, `#oliveyoungaffiliate #ad` + 2–3 topic hashtags, moderate emojis, no link; steps: upload reel.mp4 in the TikTok app → 더보기 옵션 → 콘텐츠 공개 → 브랜드 콘텐츠 ON → 게시, ideally 19:00–21:00 KST), an **X section** (English, ≤280 weighted chars, a punchy 1-line hook + 1–2 lines of value + "Extra 5% off with code KBEAUTY73 at Olive Young Global" + `#oliveyoungaffiliate #ad` + 1–2 topic hashtags, no link; tell them to attach reel.mp4), the Weibo caption (tell them to attach reel_zh.mp4) in a code block, and a **Pinterest section with all 3 pins** (① video pin = reel.mp4, ② pin.png, ③ pin2.png): for each the board, title and description in code blocks plus the suggested KST time (link field empty). Commit & push it — this is the user's daily "posting kit" page at https://github.com/samhyun73/kbeautysave-media/tree/main/media/<date>.
   Then message the user: what was scheduled (IG + FB + YouTube at 19:00 via Buffer), the posting-kit link, the Weibo caption (≤140 chars for comments; post body can be longer), and the 3 Pinterest pins (video pin = reel.mp4, pin.png, pin2.png), each with title + description + board (code only, leave the link field empty); send pin.png and pin2.png with SendUserFile.
7. Append `YYYY-MM-DD | topic | status` to `topics.md`, commit, push.
8. Delete media folders older than 60 days to keep the repo small.

## Weekend steps (Sat / Sun — manual posting only)
Same as Daily steps with these changes:
- Skip step 0's Buffer check and step 5 (no `create_post`). Nothing goes to IG / FB / YouTube / TikTok.
- Step 2: same as weekdays — `pin` + `pins` (3 Pinterest pins every day).
- Step 3c: run the gate for `--platform x`, `--platform pinterest` and `--platform weibo` (Instagram/TikTok captions are not needed).
- Step 6: `post.md` header says "주말 · 직접 게시 (X · Pinterest · 웨이보)". Message the user with the posting-kit link, X text, Weibo caption, the 3 Pinterest pins (titles, descriptions, boards; link field empty), and send `pin.png`, `pin2.png`, `reel.mp4`, `reel_zh.mp4` with SendUserFile.
- Step 7: log status as `manual kit (X + Pinterest + Weibo)`.

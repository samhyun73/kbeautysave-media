# kbeautysave daily automation — runbook

Owner: kbeautysave (Olive Young Global affiliate). Instagram @kbeautysave, Facebook page "For My Health", TikTok & Pinterest @kbeautysave, Weibo (manual).

## Fixed facts
- Affiliate link: https://global.oliveyoung.com/if/rd?su=Q7NAABDP — currently NOT used anywhere (see rule 5)
- Code: **KBEAUTY73** = **extra 5% off** at Olive Young Global checkout (confirmed by user 2026-10-01). Always state the benefit: EN "Extra 5% off with code KBEAUTY73", ZH "额外95折 优惠码 KBEAUTY73" (cta `code_label`: "额外95折 优惠码").
- Required tags: `#oliveyoungaffiliate` + `#ad` on every post; mention `@oliveyoung_global` on Instagram.
- Affiliate program page (user pasted 2026-10-16): a sale counts if the buyer comes through the `su=` link (code auto-filled, 30-day cookie) **or** types KBEAUTY73 in the "REDEEM CODE" field — so code-only promotion is credited. Commission 5–13% by monthly code sales (resets monthly); coupon amounts, shipping, tax, points and returns don't count. Site banners that day: "Free shipping over US$60", "SAVE US$20 with OLIVE YOUNG APP", "First Order Coupon Pack" — these change; only use one in copy after seeing it on the site that day, and never claim the code stacks with a sale or coupon (unverified).
- Influencer Terms v1.3 (read 2026-10-16): the code gives buyers 5% off and **works only for signed-in Olive Young Global members** (Art. 5③) — say "sign in, then enter KBEAUTY73" in how-to-save copy. Nothing may look run or sponsored by Olive Young (Art. 7②⑥): no O.Y logo, official-style sale artwork or "official" wording in our frames, pins, profiles or emails. No copying other creators' content and no spam (Art. 10① — membership can be cancelled). Olive Young may reuse our posts that mention it (Art. 9).
- **Publishing = Buffer** (user decision 2026-10-03; Buffer account jkk736540@gmail.com, free plan: 3 channels, max 10 scheduled posts queued at a time — we only ever queue today's 3). Connector `Buffer_kbeauty`. Organization `6ac09e1778721e574b910296` ("My organization"), timezone Asia/Seoul. Channels:
  - Instagram kbeautysave: `6ac09f9eea19ca0bde60715b`
  - Facebook page "For My Health": `6ac09fc4ea19ca0bde607267`
  - YouTube kbeautysave (Shorts): `6ac0a281ea19ca0bde608325`
- Metricool brand (blogId) `7131683` is now **analytics only** (weekly review). Do NOT schedule in Metricool: its free plan counts every network separately (IG+FB = 2 of 20 posts/month) and ran out mid-month.
- Media is served from this public repo: `https://raw.githubusercontent.com/samhyun73/kbeautysave-media/main/<path>`

## Schedule
- **Mon–Fri**: the reel → Instagram (reel) + Facebook (reel) + YouTube (Short), three Buffer posts, all published 19:00 KST the same day.
- **TikTok = PAUSED (user decision 2026-10-20)**: no TikTok cut (`-tiktok.json` / `reel_tiktok.mp4`), no TikTok caption, no TikTok section in `post.md` or the daily message. Never schedule TikTok (Buffer or Metricool). History: auto-posts 09-30..10-02 got 0 views → manual from 10-03; own cut without the code frame 10-14..10-20. Resume only when the user says so.
- **Pinterest = 3 pins every day, Mon–Sun (user decision 2026-10-03)**, posted by hand by the user:
  1. **Video pin** — the day's `reel.mp4` (9:16) with its own Pinterest title + description.
  2. **Image pin A** — `pin.png` (default layout: dark header, steps, "skip these").
  3. **Image pin B** — `pin2.png` (`"layout": "list"`: light ground, 3–5 numbered tips) — a *different angle and keyword* from pin A (e.g. A = "trend/colours", B = "how-to at home").
     (Sundays and sale weeks: pin B is a `"layout": "deal"` pin — see "Deal pins".)
  Each of the 3 gets a different keyword-rich title (see "Pinterest titles") and its own description; never the same title twice. Boards: nails → "Korean Nail Ideas", hair → "Korean Hair Ideas", makeup → "Korean Makeup Looks", skincare → "Korean Skincare Routine" (tell the user to create a board the first time it's needed). Suggested posting times (US evening = KST morning): 09:00, 12:00 and 22:00 KST, spread out — not all at once. Link field empty.
- **Every weekday**: Weibo caption + Chinese-text reel (`reel_zh.mp4`) sent to the user to post manually.
- **Every weekday**: an X (Twitter) **thread of 3–4 posts** sent to the user to post manually, `reel.mp4` attached to the first post (X is not connected to Buffer). See "TikTok & X copy" below.
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

**Deal pins (user decision 2026-10-16)** — sale/code pins got far more Pinterest impressions than how-to pins (user's own pins: sale 1.9K, code 470, how-to 127), so add them on a schedule; keep 70%+ informational overall.
- Layout: `"layout": "deal"` in `pins` (→ pin2.png) — `{layout, kicker, title, dates?, dates_label?, sub, items:[{title, body}] ×3–4, note?}`. The gate blocks prices, % off and "stacks with the sale" claims (the code's own 5% is fine). Hangul e.g. 알뜰 쇼핑 / 올영세일. Never use the Olive Young logo, sale artwork or product photos.
- **Evergreen deal pin: every Sunday**, pin B is a `deal` pin with no `dates` — a new angle each week (how to save on Olive Young Global, what to buy first on a first order, K-beauty gift ideas by category, what to stock up on in a sale). Pinterest title like "How to Save on Olive Young Global: K-Beauty Shopping Tips 2026".
- **Event deal pin**: only when the run (or the user) has seen an official Olive Young Global announcement of the sale and its dates that day (event page, official social, press release). Make it daily as pin B from ~7 days before the start until the end, with `dates` exactly as announced. The Big Bang Sale usually runs 4×/year (Mar, Jun, Sep, Dec — 2024 press release); never guess dates.
- In `post.md`, put the end date next to an event pin and remind the user to **archive it in Pinterest after the sale ends** (old sale pins keep circulating for months). Fill the pin description with search words ("Olive Young Global sale", "Olive Young discount code", "K-beauty deals"), `#ad`, no link.

**Pinterest titles**: [specific topic] + Korean + simple/easy/classy + ideas/inspo/aesthetic + year, e.g. "Korean Jelly Nails for Fall 2026: Simple Burgundy Ideas", "Skincare Routine Order: Simple Korean Steps (Aesthetic Guide)". Avoid the bare phrase "Korean skincare routine" (−60% y/y); be specific.
Check `topics.md` before choosing; never repeat a topic from the last 30 entries. Append the chosen topic after posting.

**Search keywords for titles, captions and hashtags** (YouTube keyword data, user's analysis 2026-10-21, `reports/keywords-youtube-2026-10-21.md`; user decision 2026-10-21: apply on every English platform, not only YouTube). The phrases the channel used had almost no YouTube search ("korean nails", "jelly nails", "milky nails", "korean hair care", "korean lip tint", "olive young best sellers" are all <750/month). Put a searched phrase at the front of the YouTube title (≤100 chars, still ends in `#shorts`) and 2–3 matching hashtags in the description. Buffer can't set YouTube tags, so the title and description carry the keywords.
- **Hair (vidIQ 2026-10-21)**: "Korean hairstyle" is +142% in 30 days (competition 26). Best long tails: "Korean hairstyle tutorial" (5.3k, competition 13, the easiest), "easy hairstyles" (17.9k, +84%), "messy bun hairstyle" (8.8k, +92%). Skip "for school" / "for girls" phrases: they aim at minors, and our posts are affiliate ads. **Caveat**: about 77% of "Korean hairstyle" searches come from Pakistan, then Bangladesh, Nepal and India (small sample). The user checked Olive Young Global's ship-to list on 2026-10-21: **Pakistan, India and Bangladesh are not on it**. So "Korean hairstyle" views mostly come from people who can't buy. Don't grow the share of hair days for this keyword. Keep hair at its current slot (Wed, and Fri in alternate weeks), and on hair days lead with US-oriented style phrases ("curtain bangs", "Korean layered cut", "easy hairstyles"). Use "Korean hairstyle tutorial" as a secondary phrase. Makeup and skincare stay the sales days.
- **Hair**: frame hair days as *styles* ("Korean hairstyle", 58k, rising, low competition; "curtain bangs", "how to cut curtain bangs" 3.3k) rather than "hair care". E.g. "Korean Hairstyle for Flat Hair: Volume at the Roots".
- **Makeup**: "Korean makeup" (48k, rising), "Korean makeup tutorial" (24k), "Korean blush" (5k, low). For lips, a well-known product name that Olive Young Global sells beats the generic term (e.g. "rom&nd Juicy Lasting Tint", 9.9k, low). Check that it is on Olive Young Global first, describe how to use it, and never claim personal use or results.
- **Skincare**: skip the bare "korean skincare" (107k, high competition) as the main phrase. Use concern-based long tails: "Korean skincare for acne-prone skin" (4.7k, low), "glass skin" / "Korean glass skin". "Acne-prone" describes a skin type only. Never promise to clear, treat or fix acne (the gate still blocks those claims).
- **Nails**: keep the trend name in the title, and add the big terms in the title tail and hashtags: "nail art tutorial" (5.3k, low), "nail art", "nails". E.g. "Milky Jelly Nails: Easy Korean Nail Art Tutorial".
- **Umbrella**: "k beauty" (88k, rising) as a hashtag on every Short.
- **Olive Young**: "olive young haul" (17k) is popular, but a haul implies we bought and tried products, so don't title anything a haul. Use "Olive Young shopping list / what to buy at Olive Young" angles only when the content really is a list of well-known items (no first-person claims). The bare "olive young" is high competition and falling.
- **Every English platform uses the same keyword choice** (user decision 2026-10-21), worded differently per platform (no copy-paste):
  - YouTube: searched phrase first in the title, 2–3 matching hashtags in the description.
  - Instagram / Facebook: put the searched phrase naturally in the first line of the caption (Instagram search reads captions), and use the matching hashtags among the 8–12 (e.g. #koreanhairstyle #koreanmakeup #nailart #kbeauty).
  - Pinterest: titles keep the Pinterest pattern above, built around the same searched phrase (e.g. "Korean Hairstyle for Flat Hair: Easy Root Volume Ideas 2026"); put the phrase in the description too.
  - X: the searched phrase in post 1 and 1–2 matching hashtags.
- The "no haul" and "acne-prone = skin type only" rules apply everywhere.
- The numbers are YouTube data; Pinterest Trends notes above still win on Pinterest when they disagree. Weibo (Chinese) and the Japan set keep their own keywords. Korean-language search is a separate audience and out of scope.

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
User preference (2026-10-01): **lots of emojis**. Aim for 6–10 per post: one at the start of most lines, emoji bullets for steps (1️⃣ 2️⃣ 3️⃣ or ✅ 💧 🧴 ☀️), a ✨/💕/🔖 near the CTA. Keep them on-topic (skincare, water, plants, sun, sparkles, hearts, Korea 🇰🇷) and never inside the code or hashtags. Each X post in the thread has to fit 280 weighted chars (emojis count double) — trim words before emojis. The auto-scheduled IG/FB/YouTube captions keep their current moderate emoji use.

## Japan set (user decision 2026-10-16: test for 2 weeks, Mon/Wed/Fri)
First sale came from Japan (ETUDE + peripera, a returning Olive Young Global customer). Test Japanese posts on two manual channels; Lemon8 can't be used (not available in Korea).
- **Channels**: ① Pinterest (same @kbeautysave account, board "韓国コスメ") — 2 pins: `pin_ja.png` (image) **and** `reel_ja.mp4` (video pin), each with its own Japanese title + description (user decision 2026-10-16), posted a few hours apart; ② X **Honeyitem (@loveslaonq)**, the user's unused X account, repurposed as the Japanese account — `reel_ja.mp4` + post. That X account is the only X account that may mention the code (Olive Young terms Art. 7④); the English X copy stays code-free.
- **Spec**: `specs/<date>-<slug>-ja.json` (`"lang": "ja"`), a Japanese adaptation of the day's topic — prefer K-makeup angles (tint, eyeshadow, blush) when the day's topic allows. Same frames as the EN spec; cta `{"title": "保存してね", "code_label": "ログイン後 クーポンコード", "where_html": "<b>Olive Young Global</b> で5%オフ", "tags": "#PR #oliveyoungaffiliate"}`. Add a `pin` with `"code_line": "ログイン後、Olive Young Global の決済で5%オフ"`, `"avoid_label": "やらないこと"`, `"tag": "#PR"`. Keep reel titles to ~7–9 characters so they don't break into a 1-character last line. Render → `media/<date>/reel_ja.mp4` + `pin_ja.png`.
- **Copy**: `#PR` (Japan stealth-marketing rule) + `#oliveyoungaffiliate`; the code line always says to sign in first (the code works only for members): 「ログイン後、クーポンコード KBEAUTY73 で5%オフ」. Hashtags `#韓国コスメ` `#オリヤン` + 1–2 topic tags. No links. Cosmetics law (薬機法): no 美白, spot/wrinkle/pore removal, anti-aging, "治る/改善" claims — the gate blocks these. X = 1–3 posts split by `---` (`--platform x-ja`); Pinterest description `--platform pinterest-ja`. Lots of emojis, natural Japanese (no machine-translation tone).
- **post.md**: a 「日本」 section with the X post(s) and the Japanese Pinterest titles + descriptions (image pin and video pin), each with a Korean translation; send `reel_ja.mp4` and `pin_ja.png` and include the 「日本」 copy in the daily message to the user (step 6). Suggested times: X 21:00–23:00 KST (= JST), Pinterest 22:00 KST.
- After 2 weeks (around 2026-10-30) compare Japan sales on the affiliate dashboard and X/Pinterest views; keep only what works.

## TikTok & X copy (user decision 2026-10-08; TikTok paused 2026-10-20, X still applies)
- **No code line** on TikTok or X: no "Extra 5% off: code KBEAUTY73…" (the video's CTA frame still shows the code). Keep `#oliveyoungaffiliate #ad` (program rule).
- **Detailed and useful**: the reader should feel they learned something they can do today. Explain each step concretely (where exactly, how much, which tool, how long), add the *why* behind the method, one common mistake to avoid, and a save prompt. Plain friendly English, emoji bullets, no claims, no invented experience.
- **TikTok** (paused 2026-10-20, kept for reference): one caption of 400–2200 characters: hook line → 4–5 emoji-bulleted steps with details → a short "why" → save prompt → `#oliveyoungaffiliate #ad` + 3–4 topic hashtags.
- **X**: a thread of 3–4 posts (each ≤280 weighted chars), separated in the caption file by a line containing only `---`. Post 1 = hook + 🧵 + `#oliveyoungaffiliate #ad` (+1 topic tag), with reel.mp4 attached; posts 2–4 = the detailed steps, the why / common mistake, and a save prompt.
- `check_post.py` enforces: no KBEAUTY73 on TikTok/X, TikTok 400–2200 chars, X 3–4 posts each ≤280 with the disclosure in post 1.

## Voice Short scripts: one emotion, a line worth sending (user decision 2026-10-21)
Based on the user's script emotion guide (a hypothesis to check in the weekly review, not a proven rule).
- **One emotion per Short**, set in the spec as `"emotion"`: `relief` ("it's not you, it's the method"), `recognition` ("that's me") or `competence` ("now I can do this"). Don't use fear or "protective" angles ("you're ruining your skin"); they drift into scare claims.
- **4 beats**:
  1. Hook (0–3 s) names the viewer's situation.
  2. One line names the feeling (e.g. "It's not your blush. It's the order you put it on.").
  3. Concrete steps + one common mistake. This is the frame worth saving; use the step checklist when it fits.
  4. Close on `"shareable_line"`: a short, true sentence someone would send to a friend (e.g. "Two thin layers beat one heavy one."), then the profile pointer.
- **Language**: second person, short sentences, examples in threes, no lecturing.
- **No engagement bait**: no "Comment YES", "Tell me in the comments", "Like if…". A real question is fine only if it reads naturally.
- **No same frame twice in a row**: rotate the hook formula (question, "you're doing X wrong", myth, "the Korean way to…", number/time, word of the day). Don't reuse a hook pattern from the previous Short ("…by noon" twice in a row on 10-21/10-22 was the lesson).
- **Honesty**: only facts with a source or common practice, no exaggerated fear or anger, no invented experience.
- Slide-reel hooks follow the same one-emotion and rotation rules where they fit.

## Daily steps
0. Call Buffer `list_posts` (organizationId above, dueAt today 00:00–23:59 KST, status scheduled/sending/sent). If today's reel is already queued on a channel, don't queue it again on that channel (never double-post); if all three exist, skip steps 1–5 and only send the posting kit if not already sent. Exception: if today's queued posts are a **voice Short** a human-present session scheduled (`media/<date>/short.mp4` exists), skip only step 5 — still render the reel and send the full manual kit (X, Weibo, Pinterest ×3), and say in the message that IG/FB/YouTube carry the voice Short today. If a channel shows `isDisconnected` in `list_channels`, tell the user which one to reconnect in Buffer.
1. Pick today's topic (rotation + `topics.md`), informed by the latest `reports/` file and `LEARNINGS.md` (favor topic types and hook styles that performed best).
   **Daily vidIQ keyword check (user request 2026-10-22), before writing any title, description or tag:**
   - **Source, in this order:**
     1. **vidIQ in the built-in browser** (free web Research, no credits) when built-in browser tools are present and reach the user's desktop app: open vidiq.com → Research, search the day's 2–3 candidate phrases.
     2. **Otherwise the vidIQ connector**: `vidiq_balance` first (0 credits), then **one** `vidiq_keyword_research` call per day (mode `research`, seed = the day's main phrase, `country: "US"`; 5 credits). Skip it if the balance is under 20; never use vidIQ write or generate tools (update video, upload, thumbnails, replies, publish).
     3. **Otherwise** the saved reports (`reports/keywords-*.md`). Say which source was used.
   - **Pick** one main phrase with real US demand and low or medium competition, plus 2–3 secondary phrases. Apply "Search keywords" (hair caveat, no "haul", "acne-prone" only as a skin type).
   - **Use** them in every English title, caption and description of the day (YouTube title first words, IG/FB first line + hashtags, Pinterest titles/descriptions, X post 1), worded differently per platform.
   - **YouTube tags**: Buffer can't set them, so write 8–12 comma-separated tags (main + secondary phrases + "k beauty", "korean makeup" etc. that fit) in post.md for the user to paste in YouTube Studio → Details → Tags (≤500 characters).
   - **post.md** gets a short 「키워드」 section (source, main phrase with monthly searches and competition, secondary phrases, the YouTube tags line); add one line to `LEARNINGS.md` only when the data changes a rule.
   - Voice Short days: the human-present session does the same check before writing the captions.
2. If `specs/YYYY-MM-DD-*.json` for today already exists (prepared in a human-present session), use it as-is — still run every gate — and only write what's missing (zh spec, captions). Otherwise write `specs/YYYY-MM-DD-<slug>.json` (see existing specs; frame types: hook, step, list, statement, cta, **swatch** — `{"type":"swatch","title","swatches":[{"name","color":"#hex","sheer":true|false,"finish":"gloss|cat eye|shimmer"}],"sub"}`, 3–4 colours drawn as nail tips; use it on nail/lip/blush colour days, and add the same `swatches` to the pin; 5–7 frames, 14–18 s total; vary `seed`, `mood` calm|bright). Every day add a `"pin"` object `{title, sub, kicker, steps:[{title, body},{title, body}], avoid:[...], note, swatches?}` (→ pin.png) **and** `"pins": [{"layout": "list", kicker, title, sub, items:[{title, body}] ×3–5, swatches?}]` (→ pin2.png) — a different angle and keyword from the first pin.
3. Render: `python3 tools/make_reel.py specs/<file>.json out/<date>` → copy `out/<date>/<slug>.mp4` to `media/<date>/reel.mp4`, `frame1.png` to `media/<date>/cover.png`, and `pin.png` + `pin2.png` to `media/<date>/`.
   Needs: python3 + numpy + scipy, ffmpeg, node + playwright (global), fonts "Noto Serif CJK KR"/"Noto Sans CJK KR".
3b. **Weibo Chinese reel (every weekday):** write `specs/YYYY-MM-DD-<slug>-zh.json` — same frames translated to natural Simplified Chinese, `"lang": "zh"`, no `pin`; the cta frame sets `"code_label": "额外95折 优惠码"`, `"where_html": "在 <b>Olive Young Global</b><br>结账时输入"`, `"tags": "#广告"` (see `specs/2026-09-30-centella-zh.json`). Render it and copy the mp4 to `media/<date>/reel_zh.mp4`. Keep Chinese lines short (≈10 characters per line on titles). Same content rules (no medical claims, no links).
3b2. *(Removed 2026-10-20: TikTok paused — no `-tiktok.json` spec, no `reel_tiktok.mp4`.)*
3c. **Quality gate (must pass — "if it can't be verified, it doesn't ship"):** write each caption to a temp file and run
   `python3 tools/check_post.py --spec specs/<file>.json --video media/<date>/reel.mp4 --caption <ig caption> --platform instagram`,
   then for Weibo `--spec specs/<file>-zh.json --video media/<date>/reel_zh.mp4 --caption <weibo text> --platform weibo`
   (Pinterest, every day: run `--platform pinterest` on **each** of the 3 pin descriptions), the X thread `--caption <x thread file> --platform x`, and the YouTube description `--caption <yt description> --platform youtube` (+ the title must be ≤100 chars). Any FAIL → fix the spec/caption, re-render, re-run. If still failing, do not schedule; tell the user what failed.
   Also extract 4–6 stills per video and look at them (layout problems the script can't see).
4. Commit & push to `main`; verify the raw URL returns 200 before scheduling.
5. Schedule in **Buffer** (`create_post`, `schedulingType: "automatic"`, `mode: "customScheduled"`, `dueAt: "<date>T19:00:00+09:00"`; if already past, the next weekday 19:00). Same asset for all three: `assets: [{video: {url: <raw reel URL pinned to the commit>}}]` (the cover is the first frame = the hook slide). Three calls:
   - Instagram `6ac09f9eea19ca0bde60715b`: text = IG caption (profile pointer, `@oliveyoung_global`, no code line), `metadata.instagram: {type: "reel", shouldShareToFeed: true, firstComment: ""}`.
   - Facebook `6ac09fc4ea19ca0bde607267`: text = FB caption (profile pointer, no code line), `metadata.facebook: {type: "reel"}`.
   - YouTube `6ac0a281ea19ca0bde608325`: text = YouTube description (hook line + 2–3 emoji value lines + "🛍️ Extra 5% off with code KBEAUTY73 at Olive Young Global checkout" + `#oliveyoungaffiliate #ad #kbeauty <2–3 hashtags from "Search keywords"> #shorts`; no link), `metadata.youtube: {title: <searched phrase first + hook, ≤100 chars, ending in #shorts — see "Search keywords">, categoryId: "26", madeForKids: false, privacy: "public"}`.
   Check each result's `status` is `scheduled` and `error` is null. Buffer has no YouTube "paid promotion" flag: remind the user to tick it in YouTube Studio after 19:00.
6. Write `media/<date>/post.md` (Korean headings; see `media/2026-09-30/post.md` as the template): links to reel.mp4 / reel_zh.mp4 / pin.png / pin2.png, a **YouTube note** (title + reminder to tick 유료 프로모션 in YouTube Studio), an **Instagram note** (after the 19:00 reel is live: ⋯ → 수정 → 파트너 콘텐츠 → 협찬 광고 레이블 추가 → 브랜드 파트너 oliveyoung_global; Buffer can't set it — user started doing this 2026-10-17), an **X section** (thread of 3–4 posts per "TikTok & X copy", each in its own code block labelled 1/4, 2/4…, no code line, no link; tell them to attach reel.mp4 to post 1 and add the rest as replies), the Weibo caption (tell them to attach reel_zh.mp4) in a code block, and a **Pinterest section with all 3 pins** (① video pin = reel.mp4, ② pin.png, ③ pin2.png): for each the board, title and description in code blocks plus the suggested KST time (link field empty). Commit & push it — this is the user's daily "posting kit" page at https://github.com/samhyun73/kbeautysave-media/tree/main/media/<date>.
   Then message the user: what was scheduled (IG + FB + YouTube at 19:00 via Buffer), the posting-kit link, the Weibo caption (≤140 chars for comments; post body can be longer), and the 3 Pinterest pins (video pin = reel.mp4, pin.png, pin2.png), each with title + description + board (code only, leave the link field empty); send reel.mp4, reel_zh.mp4, pin.png and pin2.png with SendUserFile. **On Japan-set days (Mon/Wed/Fri, user request 2026-10-16) the same message also carries the 「日本」 part**: the X (Honeyitem) post(s), the Japanese Pinterest image-pin and video-pin titles + descriptions (board 韓国コスメ), each in a code block followed by a Korean translation (해석), and send reel_ja.mp4 + pin_ja.png.
7. Append `YYYY-MM-DD | topic | status` to `topics.md`, commit, push.
8. Delete media folders older than 60 days to keep the repo small.

## Weekend steps (Sat / Sun — manual posting only)
Same as Daily steps with these changes:
- Skip step 0's Buffer check and step 5 (no `create_post`). Nothing goes to IG / FB / YouTube / TikTok.
- Step 2: same as weekdays — `pin` + `pins` (3 Pinterest pins every day).
- Step 3c: run the gate for `--platform x`, `--platform pinterest` and `--platform weibo` (Instagram/TikTok captions are not needed).
- Step 6: `post.md` header says "주말 · 직접 게시 (X · Pinterest · 웨이보)". Message the user with the posting-kit link, X text, Weibo caption, the 3 Pinterest pins (titles, descriptions, boards; link field empty), and send `pin.png`, `pin2.png`, `reel.mp4`, `reel_zh.mp4` with SendUserFile.
- Step 7: log status as `manual kit (X + Pinterest + Weibo)`.

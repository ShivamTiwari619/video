# MarketWolf video work · Handoff context

Paste this file into a new Claude chat (and upload `MarketWolf_handoff.zip` if you want to keep editing the existing builds). Everything below is the state as of 14 Oct 2026.

---

## 1. Who and what

- **Me:** Shivam, Experience Design Lead at 3minds (creative agency, Kolkata). Terse, iterative, short directional feedback. No em dashes, no AI-sounding copy, bullets over prose.
- **Client:** MarketWolf (SEBI-registered stock broker + research analyst, India). Brand: black, lime `#C2F53B`, purple `#8C3FFE`. App fonts look like Gilroy (we use Satoshi as stand-in). Deck/headline font: Clash Display.
- **Audience:** affluent, design-literate traders. South Delhi, Bangalore, South Bombay. Reviewer on client side is very classy, "South Mumbai style". Everything must feel premium, calm, perfect.
- **Figma source:** `https://www.figma.com/design/9bHu8N2ssVIKcFeB6jFsXT/Moxie?node-id=199-2` (MarketWolf sign-up journey: cover + 7 step frames, 900×1600 each).

## 2. Two deliverables

| # | Deliverable | Status |
|---|---|---|
| 1 | **Sign-up journey reel** (9:16) from the Figma screens | v15 delivered: Draft A (clean zoom) and Draft B (exploded 3D), both on the client's own VO |
| 2 | **USP film "The Exit"** (9:16, ~58s) | Draft 2 delivered. Script approved. Shivam is generating the VO elsewhere (Higgsfield / ElevenLabs) |

**Immediate next step:** Shivam will bring a new VO file for the USP film. Cut it at sentence pauses, map lines to chapters, re-time on-screen cues to the actual words, re-render Draft 2.

---

## 3. Client feedback history (do not repeat these mistakes)

1. Early reels: audio too fast. Needs natural pace and clean pronunciation.
2. Voice was **overly excited → sounds AI/fake**. Keep it calm, conversational, unhurried.
3. **No drum & bass / loud music under speech.** Music must sit well below the voice (~12–15 dB).
4. Needs **class**. Premium, minimal, South Mumbai sensibility.
5. They rate **Higgsfield's ElevenLabs model** output above direct ElevenLabs API.
6. Camera: zoom must **never go edge to edge**. Phone always keeps side margins. No light/dark spotlight highlights.
7. Motion: sophisticated and minimal, fuller animation, **zero glitches, perfect alignment**.
8. Scripts: natural, not trying too hard. Witty only lightly. No howls, no gimmicks.

What worked: Viraj voice settings, quiet lounge bed, word-synced visuals, real/faithful app UI, Prompt Motion "AllInvestView" style (reference below).

---

## 4. Deliverable 1 · Sign-up reel (latest: v15)

- **Audio:** the client's own uploaded VO (single take, 29s, v11 classy script read via Higgsfield), cut at sentence pauses. Lines:
  - Intro: "Getting started with Marketwolf is simple."
  - 01: "Begin with your mobile number." · 02: "Then verify it with a quick OTP." · 03: "Set a four-digit PIN" · 04: "and confirm it."
  - 05: "Here's what you get: no annual charges, no hidden charges, and calls with licensed experts, all of it for ninety-nine rupees."
  - 06: "Wolfie, your voice guide, walks you through KYC in the language you prefer."
  - 07: "One last step, complete your KYC," · Outro: "and you're all set." · "Marketwolf."
- **Music:** quiet lounge bed, D major (Rhodes chords Dmaj9 · Bm9 · Gmaj9 · A6sus, soft pad, sub bass, faint brushes), ducked ~12 dB under VO. SFX barely there: muted taps, soft swish on screen change, one bell on logo. Master −15 LUFS.
- **Visuals:** phone mockup with real Figma screens, typing/OTP/PIN dots/button states overlaid, screens cleaned of baked dark corners, screen clipped to phone glass radius (r≈88). Transitions: push, push, fade, slide-up, push, circle reveal. Rigid phone (no squash/stretch).
- **Draft A:** camera pans/zooms (≤ ~97% frame width) onto the element being spoken about. Phone top always stays below step titles (215–335px band in 900×1600 stage).
- **Draft B:** same + exploded view: phone tilts back in 3D, the spoken component lifts off the screen as a live copy with soft shadow. Faint film grain.
- Length: 51s.

## 5. Deliverable 2 · USP film "The Exit" (latest: Draft 2)

### Research (sources: MarketWolf App Store listing, marketwolf.com, CEO letter at marketwolf.com/find-out-why, TechCrunch/press)
- **Core USP: discipline.** Every trade must have exit levels (stop loss + book profit) set before entry. CEO Vishesh Dhingra: entries were fine, exits weren't, because of hope and greed.
- Only liquid instruments, no junk stocks.
- Free trade ideas from SEBI-registered research analysts, each with preset profit and SL levels. Website: 100+ trading calls a month.
- One app: Nifty, Bank Nifty, Sensex, Bankex, Fin Nifty, Midcap Nifty; NSE/BSE stocks; gold, silver, crude, natural gas, copper, zinc, Bulldex. Mini options in gold/silver/crude/natgas till 11:55 PM.
- Pricing (App Store): flat ₹19 per trade, ₹0 AMC, no hidden charges, start with ₹999. Sign-up screen: Pay ₹99 to open account.
- SEBI stock broker INZ000228534 · RA INH000012379 · member NSE, BSE, MCX · 24/7 chat and phone support.
- Founders ex Merrill Lynch, Barclays Capital, Morgan Stanley desks; team "IITians, mathematicians, traders".
- **Avoid:** returns/accuracy claims ("two-thirds of trades profitable", "90% correct") = SEBI risk. Download counts conflict (1.9M+ App Store vs 3M+ website). Confirm ₹19 and 100+ with client before going live.

### Approved VO script (8 lines) and Draft 2 timing

| # | Chapter | Line | Starts | Length |
|---|---|---|---|---|
| 1 | Intro | Every trader knows when to get in. Very few know when to get out. | 0.7s | 4.3s |
| 2 | 01 · The real problem | Most trades don't go wrong at the entry. They go wrong at the exit. | 6.0s | 4.7s |
| 3 | 02 · Exit, preset | On MarketWolf, every trade has its exit set before you enter. A target to book your profit, and a stop loss to protect your capital. | 11.6s | 9.5s |
| 4 | 03 · Trade ideas | You also get trade ideas from SEBI-registered analysts, each one with its profit and stop-loss levels already set. | 23.3s | 7.8s |
| 5 | 04 · One app | Indices, stocks and commodities, all in one app. Even gold and crude, till eleven fifty-five at night. | 32.1s | 8.3s |
| 6 | 05 · Pricing | A flat nineteen rupees a trade. Zero AMC. Nothing hidden. | 41.3s | 4.3s |
| 7 | 06 · Trust | Only liquid instruments. Registered with SEBI. Support whenever you need it. | 46.6s | 5.0s |
| 8 | End | MarketWolf. Trade with discipline. | 52.5s | 2.5s |

Chapter (page) starts: 0, 5.63, 11.24, 22.96, 31.71, 40.96, 46.21, 52.18 · end 57.85s.

**Key word cues** (visual lands on the word): "entry" 7.9 (Greed marker) · "exit" 10.0 (Hope marker) · "target" 17.1 · "stop loss" 19.2 · price hits target ≈22.2 · "analysts" 26.1 / "each" 27.1 (cards) · "already" 30.1 (values pulse) · "gold" 37.0 · "crude" 37.5 · "eleven" 38.7 (11:55 pill) · "zero" 43.5 (₹0 cards lift) · "nothing" 45.0 · "only" 46.6 · "registered" 48.6 · "support" 50.1 · "MarketWolf" 52.5 (logo) · "trade" 53.8 (tagline).

**Pronunciation traps:** "SEBI-registered" was heard as "CB registered" (hence line 7 = "Registered with SEBI"; spell "Sebi" if needed). Keep "MarketWolf" one word (some voices say "Margaret Wolf"). Write numbers as words ("nineteen rupees", "eleven fifty-five").

### Draft 2 visual design (AllInvestView-style)
- Reference: Prompt Motion "AllInvestView product promo" `https://prompt-motion.com/rammanq-f5a90f` (numbered chapters, two-line headline with accent second line, native UI/data animating, caption line, light/dark alternating, end card with CTA).
- Grid: 1080×1920, 88px margins, content column 904px. Label at y236 (Satoshi Bold 24, tracked), headline y290/392 (Clash Medium 96, auto-fit to 904px), caption y1640 (Satoshi 34). Logo lockup top-right.
- Pages slide up over each other (expo in-out), slow 2.2% push-in per page. No crossfades.
- Chapters: Intro hook (dark) · 01 area chart with Greed/Hope pills (light) · 02 entry/target/SL chart + rebuilt Auto Square Off "Target & SL" panel, Fixed SL → Trailing SL (dark) · 03 three rebuilt trade-idea cards (SENSEX, NIFTY, GOLD MINI; real field names) + "SEBI-registered research analysts" + "100+ calls a month" (light) · 04 tab bar Indices/Stocks/Commodities + rebuilt market rows, Mini options 11:55 PM pill (dark) · 05 phone with REAL Figma benefits screen, ₹0 cards lift out (light) · 06 credentials list with check ticks (dark) · End: logo, "Trade with discipline.", "Open your account" CTA, Android · iOS · Web, SEBI disclaimer (light).
- All rebuilt figures labelled "Illustrative. Not a recommendation." / "Prices illustrative".
- Real UI sources: 6 App Store screenshots (1284×2778, values masked "₹₹₹") used as layout reference; website product clips at `marketwolf.com/videos/product-features/*.portrait.mp4` (720p, too soft to use directly).

### Draft 1 (superseded)
"The Exit" line-concept film: one line becomes chart → target/SL → ticket → cards → ticker → numerals → badges → logo underline. Client wanted more real screens and fuller animation, hence Draft 2.

---

## 6. Voice settings (ElevenLabs)

- **Approved voice:** Viraj – Warm Luxury Brand Narrator, ID `NvA7c85NkZVpFBAHHQQ3`, model `eleven_multilingual_v2`, stability 0.65, similarity 0.8, style 0, speaker boost on, speed 0.92–0.95. One API call per line via `/with-timestamps` (gives word timings for sync).
- Other voices tried: Ruhaan `KffkLYpIn624q06dkhs7`, India (husky cosmo) `mmSZflZFDoe6qEecRgIO`, Mona `mKn4iVyn09DrJ8cFw5Rn`, Naina `6BZyx2XekeeXOkTVn8un`, Rahul S `txk8uOzZ0iCh0B9mFSRG`, plus Shivam's picks (Jerry B, Valf, The Duke, Brad: American character voices).
- **QA method:** transcribe every generated line back with ElevenLabs Scribe (`/v1/speech-to-text`, `scribe_v1`) and regenerate on mismatch.
- API key: use your own; do not paste it into shared files. (The key used in the old account was shared in chat, so rotate it.)
- Environment note: in Claude's sandbox, Python urllib to ElevenLabs needs a `User-Agent: curl/8.5` header, and output format `mp3_44100_128` (192 is tier-locked).

---

## 7. Production pipeline (how the videos are made)

1. **One HTML file**, every style computed from time inside `window.seek(t)` (no CSS animations, no timers). Timings come from `timing.js` (`window.TL` for the USP film, `window.CFG` for the reel).
2. **Planner script** (`plan.py` / `plan13.py`) reads VO word timestamps and writes scene starts + word cues into `timing.js`.
3. **Render:** Playwright headless Chromium screenshots. USP film: 90 samples/s, then `ffmpeg tmix=frames=3 → 30fps` for motion blur. Sign-up reel: 60fps direct (frame blending caused ghosting on fast moves there).
4. **Audio:** Python/numpy synth (lounge bed + SFX) + VO placement + ducking, then `ffmpeg loudnorm I=-15`. Mux with ffmpeg.
5. **QA before full render:** render a frame on every key word, check alignment/overlap/edges, fix, then render.
6. Render in batches under ~5 min per command (sandbox timeout); resumable batch scripts skip existing frames.
7. Absolute paths inside scripts point to the old sandbox (`/home/claude/moxie`, `/home/claude/exit`). Update them after unzipping.

### Swapping in a new VO for the USP film
1. Transcribe the new audio with word timestamps (Scribe, `timestamps_granularity=word`).
2. Cut per line at the quietest point in each sentence gap (10 ms RMS min), 12 ms fades, keep the take's natural relative levels.
3. Rebuild `timeline.json` / `timing.js`: scene start = previous end; line starts 0.35s into its scene (0.7s for line 1); scene ends 0.6s after its line (line 3: +1.9s for the price-hits-target beat; line 8: +2.8s hold).
4. Re-run audio build, render, mux.

---

## 8. Bundle contents (`MarketWolf_handoff.zip`)

```
1_signup_reel/   index.html + timing.js (v15, ?mode=A or ?mode=B), assets/ (cleaned screens s1–s7, phone.png, logo, fonts, glow, grain),
                 render.py, batch.py, plan13.py, audio/ (build_v13.py, events.json, v13/ client VO cuts + vo.json, mix_v13.wav)
2_usp_film/      film2/ (index.html, timing.js, assets), timeline.json, plan.py, rend2.py, gen_vo.py,
                 vo/ (Viraj lines l1–l8 + vo.json word timings), audio/ (build_audio2.py, mix2.wav)
3_reference/     MarketWolf_TheExit_prompt.md (Prompt Motion-style master prompt), appstore_screens/ (6 real screenshots),
                 website_clips_contact_sheet.jpg
```

Final MP4s delivered so far (re-upload if needed): `MarketWolf_Reel_v15_DraftA_CleanZoom.mp4`, `MarketWolf_Reel_v15_DraftB_Exploded3D.mp4`, `MarketWolf_USP_Draft2.mp4`.

---

## 9. Open items

- Get the new USP voiceover from Shivam, re-cut and re-sync Draft 2.
- Ask MarketWolf for real Trade Ideas, order ticket and market screens (unmasked) to replace the rebuilt components.
- Client to confirm "₹19 per trade", "100+ calls a month", and which download figure (if any) can be used.
- Optional: deep-house variant of the music bed for the premium audience, kept at the same low level under VO.

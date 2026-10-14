# MarketWolf · "The Exit" · Prompt (Prompt Motion format, adapted for VO)

Combines the Prompt Motion showreel template (direction / structure / build / start) with a VO-led product film. Paste as one prompt. Run on Opus 5.5, effort max.

<direction>
A 50-second 9:16 product film for MarketWolf, a SEBI-registered trading app. Audience: affluent, design-literate traders in South Delhi, Bangalore and South Bombay. Tone: calm, assured, premium. Nothing shouts.
Concept: "The Exit". One thin horizontal line is the whole film. It starts as a price line, becomes a chart that tempts you (GREED) and punishes you (HOPE), splits into a target line and a stop-loss line, frames a trade ticket, multiplies into trade-idea cards, stretches into a ticker of markets, rolls into price numerals, lines up trust badges, and finally becomes the underline under the logo. Every shot is made out of the previous one. No cuts, no crossfades.
Type: Clash Display only (Medium for headlines, Regular for labels).
Palette: lime #C2F53B (target, profit, brand), purple #8C3FFE (brand, UI), coral #FF6B5B (stop loss only), plus black and white. Background: black with a faint 40px grid.
Banned: particle bursts, glows, lens flares, camera shake, RGB split, crossfades, bouncy or elastic easing, emoji, stock icons, anything that looks like a template, any promise of returns or accuracy.
UI shown is illustrative: label trade tickets and ideas "Illustrative. Not a recommendation."
</direction>

<voiceover>
ElevenLabs, voice "Viraj – Warm Luxury Brand Narrator" (NvA7c85NkZVpFBAHHQQ3), model eleven_multilingual_v2, stability 0.65, similarity 0.8, style 0, speed 0.93. One API call per line, request /with-timestamps, transcribe each line back with Scribe and regenerate on any mismatch.
1. Every trader knows when to get in. Very few know when to get out.
2. Most trades don't go wrong at the entry. They go wrong at the exit.
3. On MarketWolf, every trade has its exit set before you enter. A target to book your profit, and a stop loss to protect your capital.
4. You also get trade ideas from SEBI-registered analysts, each one with its profit and stop-loss levels already set.
5. Indices, stocks and commodities, all in one app. Even gold and crude, till eleven fifty-five at night.
6. A flat nineteen rupees a trade. Zero AMC. Nothing hidden.
7. Only liquid instruments. SEBI-registered. Support whenever you need it.
8. MarketWolf. Trade with discipline.
</voiceover>

<structure>
The VO is the clock. Each scene starts 0.3s before its line and ends 0.6s after it. Key visual moments land on the word that names them (GREED on "go wrong", target line on "target", stop line on "stop loss", ₹19 on "nineteen", 11:55 on "eleven fifty-five", logo on "MarketWolf").
Scenes: 1 hook type · 2 chart with GREED / HOPE · 3 target + stop loss → trade ticket, price hits target, exit ticks · 4 ticket multiplies into 3 trade-idea cards + "100+ ideas a month" · 5 cards stretch into a ticker of markets + 11:55 PM clock · 6 ₹19 / ₹0 AMC / No hidden charges numerals · 7 four trust badges · 8 badges collapse into the logo underline, "Trade with discipline.", SEBI risk disclaimer.
</structure>

<sound>
Under the VO: a quiet lounge bed in D major (warm Rhodes chords, soft pad, sub bass, whisper of brushed rhythm), ducked about 12 dB below the voice. SFX only where something physically happens: a soft tick when a line locks, a muted tap on the Buy button, one soft bell on the logo. No risers, no hits, no drums under speech. Master to -15 LUFS.
</sound>

<build>
1. One HTML file at 1080x1920. Every style is computed from time inside window.seek(t): no CSS animations, no timers, no state carried between frames.
2. Exponential and critically damped spring easing written as functions of time. No overshoot on type.
3. Render with Playwright at 90 samples per second, blend every 3 with ffmpeg tmix for motion blur, output 30fps, mux the mixed audio.
4. Before the full render, render one frame per scene and one on every key word. Fix anything cluttered, off-cue, overlapping or hard to read.
</build>

<start>
Show the beat-by-beat storyboard with timings from the VO, then build it without asking anything else. Give me the final MP4.
</start>

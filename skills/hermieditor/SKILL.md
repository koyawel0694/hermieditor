---
name: hermieditor
description: "Use for adaptive long-form YouTube, explainers, vlogs, Shorts/Reels, product videos, and mini-dramas with motion design."
version: 1.3.0
author: John & Nessan
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [video-editing, short-form, long-form, youtube, vlogs, ffmpeg, subtitles, sfx, reels, tiktok, mini-drama, adaptive-profile, hermieditor]
    related_skills: [deepclip, deepcut, deepcaption]
---

# HermiEditor: Autonomous Video Editor for Hermes Agent

HermiEditor turns raw footage, talking-head recordings, product clips, and AI-generated video sequences into polished long-form YouTube videos, creator vlogs, short-form (Reels/TikTok/Shorts), or episodic mini-drama series with designed motion graphics, kinetic titles, word-level captions or clean subtitles, motivated transitions, B-roll, sidechain-ducked BGM, and layered sound effects using local HyperFrames rendering and FFmpeg compositing.

Workspace root: `/home/john/Documents/hermieditor` (repo: `https://github.com/koyawel0694/hermieditor.git`, fallback: `/home/john/Documents/free247editor`)

## Adaptive Editing Profile — PopUpLedger Studio v3.0

Before every project, read repository-root `my-style.md` and `my-rules.md`. Read `references/popupledger-motion-graphics-style-library.md` when planning motion design. For long-form explainers, read `references/popupledger-long-form-explainer-motion-design.md` and create a script-to-visual beat map before final assembly. This is one adaptive profile for 16:9 long-form YouTube, explainers/documentaries, vlogs, 9:16 Shorts/Reels, product/affiliate videos, and mini-dramas.

### Creative-direction gate
If the user has not already supplied a clear visual direction, ask once: (A) Auto-director chooses based on script/assets/references; (B) user chooses from the style menu; (C) user gives custom direction; (D) propose a treatment and wait for approval. Do not re-ask within that project. If A is chosen, make normal scene-level choices autonomously. If D is chosen, wait for approval before full production.

### Motion design beyond kinetic typography
Use the style library as a selectable toolkit: minimalist callouts, diagrams/infographics, data visualization, UI animation, contextual pop-ups, mixed-media collage/cut-outs, 2.5D parallax, supported 3D/isometric visuals, motion tracking, maps/timelines, split screens, illustrations/metaphors, masks/shape transitions, documentary/source graphics, line-art, expressive creator graphics, cinematic graphics, justified HUD overlays, and freeze-frame/subject separation. Choose one primary visual family plus up to two supporting families by default; do not apply every style in every scene.

For explainers, plan each narration beat's visual purpose, style family, exact copy/data, asset/source, animation entry/build/hold/exit, sound cue or `none`, and QC risks. Prefer designed graphics for processes/relationships, verified data visuals for numbers, genuine screenshots for actual interfaces, sourceable footage for factual context, and selective AI video for illustrative/cinematic value. AI-generated footage must not replace accurate diagrams, critical text, verified UI or evidence. Inspect available rendering tools before planning effects; if unsupported, use a faithful supported fallback and disclose the limit.

Profile precedence: direct user instructions → selected creative direction and approved treatment → matching format preset in `my-style.md` → persistent rules in `my-rules.md` → generic production defaults. Do not let older generic defaults silently disable a clearly stated user preference. Keep motion purposeful, legible, accurate and tool-supported.

## Directory Structure

- `inbox/`: Raw clips and voiceover dropped here (`inbox/<project_slug>/`).
- `outbox/`: Final renders (`<slug>-final.mp4`, `.ass`, `.srt`).
- `my-style.md`: Lasting style preferences (dimensions, pacing, framing, text positioning, presets).
- `my-rules.md`: Cumulative rules learned from editorial revision notes and user feedback.
- `my-sounds/`: Curated 69-sound library (`mini-drama/`, `explainer/`, `us-niche/`), indexed in `catalog.json`.
- `kit/`: The Herk Edit Kit engine and video projects (`kit/video-projects/<slug>-YYYY-MM-DD/`).
- `references/`:
  - `references/ADAPTIVE_EDITING_PROFILE.md`: Adaptive Editing Profile specifications and presets.
  - `references/adaptive-long-form-explainer-motion-design.md`: Long-form explainer motion design playbook (diagrams, charts, timing, hybrid visuals).
  - `references/motion-cards-and-telegram-delivery.md`: Motion graphics, HyperFrames mini PC rendering, sound design, Telegram limits.
  - `references/explainer-video-editing.md`: Explainer and documentary assembly, end-image hold rules, clean canvas, and transcription fallbacks.
  - `references/mini-drama-series-editing.md`: Assembly, pacing, simple subtitle styling, sidechain-ducked BGM score integration, and lossless multi-episode compilation.
  - `references/sound-design-and-sfx-library.md`: Sound effects library organization, FFmpeg stream channel mapping, and volume ducking curves.
- `templates/`:
  - `templates/adaptive-long-form-visual-beat-map.csv`: Script-to-visual beat map planning sheet.
  - `templates/adaptive-explainer-project-brief.md`: Explainer brief and quality gate checklist.
- `tools/transcribe.mjs`: Word-level transcription tool (Groq Whisper API or local `faster-whisper`).

- **Visuals & Overlays Discipline**: Follow the user's adaptive profile and selected creative direction. For informational/explainer content, proactively use purposeful diagrams, animated callouts, relevant pop-ups, kinetic key phrases, accurate charts, comparisons, timelines, annotated real screenshots, and B-roll where they clarify meaning. Keep visual hierarchy readable and let clean footage breathe whenever graphics would distract. Do not add decorative HUDs, fake data, or effects simply to fill the frame.

## Sound Design & SFX Sourcing Discipline

- **Strict Priority on Curated `my-sounds/` Library**:
  - Use real curated sound files from `my-sounds/` (`my-sounds/explainer/`, `my-sounds/mini-drama/`, `my-sounds/us-niche/`), indexed in `catalog.json`, when a meaningful visual/action/transition cue calls for an audible accent. Voiceover alone does not require an SFX; clean dialogue, natural ambience, or silence may be the best choice.
  - Avoid synthesizing procedural tones/clicks/beeps when a suitable real recording exists in the curated library. Use procedural sound only as a fallback when no suitable real asset is available and the requested workflow supports it.
- **Affiliate & Explainer SFX Mapping (`my-sounds/explainer/`)**:
  - Solution / Brand Reveal: `pop-clean.mp3` (gain -3.0 dB) on "Ito ang katapat niyan" / brand reveals.
  - Metric / Spec Callout: `ding-bell-subtle.mp3` (gain -3.0 dB) on numbers, thickness, or key specs (e.g. "3mm").
  - Physical Action / Scratch Resistance: `whoosh-transition-fast.mp3` (gain -4.0 dB) on physical friction or demonstrations.
  - Feature Proof & Payoff: `ding-correct-gameshow.mp3` (gain -5.0 dB) on "100% waterproof" / proof claims.
  - Bonus / Inclusions: `ding-bell-subtle.mp3` (gain -4.0 dB) on "Libre pa ang pandikit".
  - Checkout CTA ("Yellow Basket"): `cash-register-cha-ching.mp3` (gain 0.0 dB) timed exactly on "Pindutin mo na ang yellow basket".

## Production Modes

### Mode A: Educational / Explainer Shorts
- **Pacing**: Fast-paced, eliminate breath pauses > 0.35s, jump cuts, subtle punch-in scale zooms (5-8% scale) on narrative topic shifts.
- **Subtitles**: Dynamic word-by-word active tracking captions in bold sans-serif (`Liberation Sans`), bold white with dark drop shadow/stroke, vibrant gold (`#FFD700` / `&H0000D7FF`) or electric cyan active highlight, positioned in upper-middle third safe zone (`MarginV=480`) or lower safe zone (`MarginV=300`).
- **Clean Visual Canvas Rule (STRICTLY NO FLOATING CARDS / POP-UP OVERLAYS)**:
  - In explainer videos (stop-motion, papercraft, claymation, 3D animations, dioramas, and documentary sequences), **DO NOT add motion graphics cards, floating stat boxes, or pop-up windows**. The visuals/art are the hero and the primary hook; overlays block the central action and ruin the viewer's focus on the craft.
  - **What MUST be present**: Clean video footage, dynamic active tracking subtitles, smooth motivated transitions (0.5s fade-in from black, 0.367–0.5s `xfade` crossfades), curated tactical SFX and foley, and video effects (subtle 5–8% punch-ins, speed ramps, reframes).
  - **Where to use cards**: Reserve motion graphics cards, pop-ups, and comparison tables strictly for personal vlogs, talking-head videos, or affiliate product showcases.
- **End-Image Thumbnail Hold**: In explainer videos with an accompanying thumbnail or still diorama, hold at the very END for 0.1–0.2 seconds (e.g. 0.20s), never at the beginning.
- **Audio & SFX Discipline**: Spoken voiceover is always front and center (normalized to -14 LUFS, 80Hz highpass, +2.5dB boost at 2.8kHz). Curated SFX from `my-sounds/` leveled beneath speech.
- **Duration Sync**: Enforce hard duration sync by passing `-t <audio_duration>` directly to ffmpeg or post-trimming (`ffmpeg -y -ss 0.0 -t <audio_duration> -i composite.mp4 -c copy final_trimmed.mp4`).

### Mode B: Mini Drama Series (Vertical Serye / Fiction)
- **Subtitles**:
  - Simple, static, elegant subtitles only — strictly NO word-by-word karaoke highlights or animated bouncing words.
  - Typeface: Clean sans-serif (`Liberation Sans` or `DejaVu Sans`), 46-48pt, bold.
  - Color & Contrast: Pure white (`&H00FFFFFF`) with 2.8–3.0px dark outline stroke and 1.2px shadow for 100% legibility against all backgrounds.
  - Safe Zone: Lower-third center (`MarginV=260–280` on 1080x1920) to stay safely above TikTok/Reels UI overlays without blocking characters' chests or hands.
  - Text & Timing: Aligned exactly to spoken dialogue in Tagalog/Filipino or English.
- **Transitions**:
  - Smooth cinematic transitions: 0.5s gentle crossfade (`xfade=transition=fade:duration=0.5:offset=...`) paired with 0.5s audio cross-dissolve (`acrossfade=d=0.5:c1=tri:c2=tri`).
  - Smooth 0.5s fade-in from black at video intro.
  - Cliffhanger ending: 1.5s freeze-frame hold on the final questioning/tearful close-up, followed by a 1.2–1.3s fade-to-black.
- **Dialogue Timing & Reaction Breathing Room**:
  - When speech in clip A ends near the boundary or clip B starts near 0.0s, pad clip A with a 0.5s reaction hold (`tpad=stop_mode=clone:stop_duration=0.5` and `apad=pad_dur=0.5`) so the crossfade occurs in the pause, preventing overlapping speech.
- **Sound Design & SFX**:
  - Dialogue Primacy & Mastering: Boost voice by 1.35x (`volume=1.35`) with highpass at 80Hz and +2.5dB vocal presence boost at 2.8kHz (`equalizer=f=2800:t=q:w=1.0:g=2.5`).
  - Environmental Bed: Continuous background tone (interior rain, room tone, outdoor street).
  - Tactical Drama SFX: Subtle brass shop door chimes, somatic heartbeat flutter pulses, delicate tactile shimmer on physical brushes, and emotional tension swells/impacts on cliffhangers.
  - BGM Score: Acoustic or ambient instrumental bed leveled to `volume=0.07` with a 6dB scoop at 1200Hz.
  - Sensitive Sidechain Ducking: Always wire sensitive sidechain compression (`threshold=0.02:ratio=3.5:attack=50:release=450`) so music instantly ducks an additional 6–10 dB the moment any character speaks.

### Mode C: Affiliate & Product Commercial Shorts (TikTok / Reels / Shopee / Lazada)
- **Pacing & 5-Step Narrative Arc**:
  1. Hook (0–3s): Problem, craving, or curiosity stop-scroll.
  2. Product Reveal & Scoop (3–7s): First physical action showing product texture/packaging/branding.
  3. Value & Proof (7–14s): Proof of quality, thickness, durability, or authenticity.
  4. Preparation / Serving / Testing (14–20s): Stacking, testing, wiping, or installation demonstration.
  5. Climax & CTA (20–27s): High-satisfaction payoff & call to action ("Pindutin ang yellow basket").
  - Cut strictly on spoken cadence and phrase boundaries so visual actions align directly with spoken descriptions.
- **Captions & Safe Zones**:
  - Dynamic active tracking captions in `Liberation Sans Bold`, white text with 5px dark outline and shadow.
  - Vibrant gold active highlight (`#FFD700` / `&H0000D7FF`) with a 10% scale pop (`\fscx110\fscy110`) as each word is spoken.
  - Safe Zone: Set `MarginV=480` (Alignment=2) in 1080x1920. Captions sit ~25% above bottom edge, staying clear of TikTok/Reels shopping cart buttons and audio tickers.
  - Semantic Phrase Chunking: Group words by natural Tagalog semantic units (e.g. "SA PETSA DE PELIGRO", "PINDUTIN MO NA ANG YELLOW BASKET").
- **Transcription Semantic Verification (Colloquial Tagalog/Taglish)**:
  - Whisper models frequently transcribe rapid colloquial Tagalog phonetically with errors (e.g., "Pindutin" -> "Pintutin", "naka-sale pa" -> "nakasilpa", "petsa" -> "pecha").
  - Always review transcript words and correct typos before embedding into `.ass` or `.srt` files.
- **Tactical Affiliate SFX**:
  - Checkout CTA Chime: Timed exactly on the call-to-action (`cash-register-cha-ching.mp3` from `my-sounds/explainer/`).
  - Accent / Ding SFX: Clean bell ding (`ding-bell-subtle.mp3`) on product reveals, key test moments, and payoff moments.
  - Background Music: Acoustic lifestyle track at `volume=0.07` with a 6dB notch at 1200Hz (`equalizer=f=1200:t=q:w=1.2:g=-6,lowpass=f=7500`) and sensitive sidechain ducking against voiceover.

### Mode D: Long-form YouTube / Explainer / Documentary / Vlog (usually 16:9)
- **Canvas**: Default 1920x1080 for standard 16:9 long-form; preserve requested/source frame rate and higher resolution when the project supports it. Never apply the portrait export preset to a landscape request.
- **Planning**: Analyze the narration/transcript first, then create a visual beat map. Assign each major idea a visual purpose, type, exact labels/data, source/asset path, entrance/build/hold/exit, and sound cue or `none` before final assembly. Align estimated beats to the real narration timecodes before the final render.
- **Hybrid visuals**: This user does not want long-form explainers made entirely from AI-generated video. Alternate editor-built motion graphics (diagrams, flowcharts, timelines, hierarchy/relationship maps, truthful charts, number reveals, comparisons, key phrases), real/sourced B-roll, genuine screenshots/UI/source excerpts, presenter/real footage, and selective clearly illustrative AI cutaways. Prefer a purpose-built diagram whenever it explains an abstract mechanism better than footage. Never use generated video for factual charts, critical UI/text, or evidence.
- **Clean Visual Canvas Rule on Animation/Diorama Explainers**: For crafted animation, stop-motion, papercraft, claymation, and 3D diorama explainer sequences, **DO NOT add floating cards, pop-up windows, or UI graphic boxes over the footage**. Keep the frame clean with pure visuals, motivated transitions, video effects, layered SFX, and subtitles only. Reserve floating motion cards strictly for talking-head, vlog, or product review formats.
- **Graphic rhythm**: Look for a meaningful visual refresh around every 5-10 seconds in dense narration, but do not cut to a timer. Use chapter-level hero graphics and smaller contextual labels/callouts. Reveal diagrams in narration order, hold readable results, and avoid competing simultaneous animations. At least half of major explanatory beats should be planned as designed/sourced explanatory visuals when the subject supports them; treat this as an editorial planning target, not a rigid screen-time quota.
- **Motion and transitions**: Use consistent typography/grid/colors/easing; progressive line/node reveals, masked text, restrained spring settles, and selected motion transitions. Default to clean/match/J/L cuts. Avoid a repetitive transition every clip, constant zooms, gratuitous glitching, and decorative HUDs.
- **Data integrity**: Use only supplied or verified figures, claims, quotations, source details, dates, and UI content. Use truthful chart labels/units/scales; never invent missing values. Prefer SVG/HTML/GSAP or other exact-text-capable tools for readable data and labels.
- **Sound**: Layer voice, appropriate ambience/Foley, music ducking, and selective SFX. SFX must land with a real visual/action beat; do not add one to every sentence or card. Use only sound files that exist in the local catalog.
- **Delivery/QC**: Verify dimensions, frame rate, duration, stream mapping, A/V sync, caption accuracy, text legibility, graphic timing, actual render, dialogue balance, and end frame. Output a 16:9 master unless otherwise requested; do not force Shorts captions or vertical safe zones into landscape.

## AI Video Generation Artifacts & Pitfalls

### Google Omni / Flow Character Reference Image Flaw
- Video generation models frequently flash the static character reference image for the first 8–15 frames (0.3s to 0.65s).
- Run scene change detection on the first 1.5s:
  ```bash
  ffmpeg -ss 0.0 -t 1.5 -i clip.mp4 -filter_complex "select='gt(scene,0.25)',metadata=print" -f null -
  ```
- Pre-trim the raw clip cleanly from the exact scene cut timestamp if detected:
  ```bash
  ffmpeg -y -ss <pts_time> -i raw_clip.mp4 -c:v libx264 -crf 18 -preset fast -c:a aac -b:a 192k trimmed_clip.mp4
  ```

## Critical Production & Delivery Rules

- **FFmpeg Image Overlay Looping**: When overlaying static PNG motion cards onto a video stream with `enable='between(t,start,end)'`, **ALWAYS loop the image input**:
  `-loop 1 -t <duration> -i card.png`
  Without `-loop 1`, FFmpeg treats the image as a 1-frame stream at $t=0$. When the overlay filter evaluates at $t > 0$, the input stream has already ended and the card silently fails to render.
- **Creator Vlog & Affiliate Card Placement**: For 9:16 vertical vlogs with a centered speaker, never use centered or full-width pop-up cards that overlap the forehead, hair, or face. Use a compact **horizontal top pill card** (1000px wide, ~70-85px tall, positioned at `Y=50px`) styled with dark glassmorphism (`rgba(15, 23, 42, 0.92)`). It leaves a clean gap above the crown of the head and keeps lower-third captions unobstructed.
- **Hard Duration Sync (Audio/Video Alignment)**: Always enforce exact target duration explicitly: pass `-t <target_seconds>` on the compositing command, or run a hard trim copy pass:
  ```bash
  ffmpeg -y -ss 0.0 -t <target_seconds> -i composite.mp4 -c copy final_trimmed.mp4
  ```
- **Special Unicode Characters in Filenames**: Files frequently contain ellipses (`…` U+2026), brackets, or symbols. Always quote variables and use glob matching to prevent silent script failures.
- **Single Video Delivery (Final Master Only)**:
  - Generate ONLY 1 video file by default: `<slug>-final.mp4`, using the chosen/requested format (1920x1080 for standard 16:9 long-form, 1080x1920 for 9:16 vertical, or the explicitly requested ratio), CRF 17-19 where appropriate, 192k AAC stereo, and `+faststart`. Preserve source/project FPS where practical.
  - Do NOT generate redundant multi-tier files (`<slug>-under20mb.mp4`, `<slug>-hq-48mb.mp4`, or `<slug>-v1.mp4`) unless explicitly requested by the user.
- **Explicit Stream Mapping (`-map 0:v -map 1:a`)**:
  - When multiplexing base video and master audio, ALWAYS explicitly map video from `0:v` and mixed audio from `1:a` (`-map 0:v -map 1:a`). Omitting `-map` causes FFmpeg to pick `0:a` (the camera/foley track) and completely drop the voiceover track!
- **Frame-Accurate Cut Timing (Preventing Cumulative Drift & End-Hold Truncation)**:
  - Always define sub-clip cut boundaries as integer frame counts (`-vframes <N>` or `duration = N / FPS`). Cutting by arbitrary floating-point seconds (e.g. 5.25s at 30 fps) forces FFmpeg to round up to the next frame (+1 frame / ~33ms per clip). Over 8+ cuts, this accumulates 0.20s+ of drift, causing downstream `-t` clamps to truncate or obliterate the final thumbnail hold frame.
- **Document File Delivery**: When delivery as uncompressed file is requested, dispatch directly via Telegram Bot API `sendDocument`.
- **Standalone Subtitle Deliverables**: Always produce and deliver accompanying `.srt` and `.ass` files in both `inbox/` and `outbox/`.

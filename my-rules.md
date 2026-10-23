# Adaptive Editing Profile — Persistent Rules (v2.0)

Read this file and the root `my-style.md` before every HermiEditor project. For long-form explainers, also read `skills/hermieditor/references/adaptive-long-form-explainer-motion-design.md`.

## Rule 1 — One profile, multiple formats
Use one adaptive quality standard across long-form YouTube, explainers, vlogs, Shorts, Reels, product/affiliate videos, and mini-dramas. Resolve the requested format first. The user's explicit instructions outrank the defaults. Never force vertical output onto a landscape request or treat every genre the same.

## Rule 2 — Explain with designed visuals, not endless AI clips
For long-form informational/explainer projects, AI-generated video is an optional ingredient—not the default canvas. The edit must deliberately mix purpose-built motion graphics, text animation, diagrams, charts, timelines, comparisons, annotated screenshots, authentic/sourceable B-roll, real project footage, and selective AI illustration where it adds value.

Before final assembly, create a visual beat map. Every major narration beat must answer:
1. What is the viewer meant to understand or feel?
2. What visual form makes it easiest to understand (diagram, number, comparison, screenshot, footage, typography, timeline, etc.)?
3. What exact words/data/assets appear on screen, and what is their source?
4. How will the visual enter, develop, hold, and exit?
5. Is sound useful here, or is clean dialogue/silence better?

For explainers, target at least half of major explanatory beats as designed/sourced explanatory visuals when the topic supports them. Do not fake a quota, and do not pad the video with irrelevant graphics. If the script explains a relationship, mechanism, sequence, calculation, hierarchy, or comparison, prefer a custom diagram/graphic before generic AI footage.

## Rule 3 — Match visual medium to meaning
- Abstract mechanisms, systems, causes/effects, and processes → animated diagrams, flowcharts, timelines, network maps, layered cross-sections, or visual metaphors.
- Key concept or definition → kinetic typography plus a concrete supporting icon/example.
- Quantities, comparisons, growth, or decline → a truthful chart, counter, comparison panel, or proportional diagram sourced from real values.
- Actual people, places, events, physical processes → real/sourced footage or stills when factual accuracy matters; label any illustrative AI reconstruction as illustrative when confusion is possible.
- Product/software/UI → real product shots/screenshots and animated callouts/masks/highlights; never use an image/video model to generate critical readable data or UI text.
- Evidence and citations → use actual records/source extracts and concise attribution, never fabricated articles or interface screenshots.
- Emotion, reaction, character, or memory → protect the acting and use naturalistic footage, sound, and story-native graphics rather than generic infographic overlays.

## Rule 4 — Script-to-visual timing
- Use the final VO/transcript as the timeline spine. Align graphic reveals to semantic phrases or key words, not an arbitrary metronome.
- During dense narration, aim for a meaningful visual refresh every ~5–10 seconds, but keep a visual on screen longer if complexity requires it. Use chapters and larger hero graphics for major turns in the argument.
- Build diagrams step-by-step in the same order the narration explains them. Show relationships clearly before animating the next step.
- After a key phrase/stat/diagram reveal, leave enough hold time for comprehension. Do not make the viewer read a label at the same moment another competing animation enters.
- Do not show a graphic too early if it spoils the narrative; do not show it after the narration has already moved on.

## Rule 5 — Graphics must be accurate
- Never invent numbers, chart values, source citations, dates, quotes, URLs, UI labels, product claims, or map routes.
- If a number/value is missing, leave it out or mark it as a placeholder in the planning file—never quietly make one up.
- Charts require correct labels, units, date ranges, and truthful scales. Avoid 3D chart effects, misleading axis cuts, and decorative precision unsupported by the data.
- Prefer editable/precise SVG or HTML/CSS/GSAP-built labels over AI-rendered text. Proofread every label and check for clipping.
- Use image generation for visual metaphors, cutout illustrations, atmospheres, or non-text decorative/supporting assets only when they improve the explanation. Do not generate AI footage just to fill a visual gap that a simpler graphic could explain better.

## Rule 6 — Professional motion, not motion spam
- Use consistent easing, stroke weights, margins, component sizing, typography, and a limited palette.
- Use spring/overshoot for a few energetic entries; use smoother eases for charts, diagrams, maps, and cinematic moments. Let animation settle before introducing another message.
- Do not reuse the same transition for every cut or attach an SFX to every graphic, word, subtitle, or edit.
- Avoid generic HUDs, random glitching, constant wiggle/parallax, gratuitous zooms, unnecessary lens flares, and decorative popups with no clear function.
- Keep screens clean: one main idea, a small amount of supporting text, clear spatial connections, comfortable margins, and readable type at phone scale.
- Always leave time to read charts, diagram labels, and source notes. Do not animate text so fast that the motion becomes a legibility failure.

## Rule 7 — Sound is part of the visual design
- Inspect the real `my-sounds/catalog.json`; use only available sound files. Never invent asset paths or names.
- Use short clicks/ticks for clear UI interactions, whooshes for directional movement, subtle pings for key labels, restrained impacts for major reveals, and real ambience/Foley when the scene calls for it.
- Narration alone does not require an SFX. Clean voice, natural ambience, and silence remain valid design choices.
- Sync sound to the animation's landing/action; fade tails and duck music based on the actual dialogue. Keep speech intelligible and prevent clipping, music masking, or abrupt cuts.

## Rule 8 — Adapt by genre
- **Explainer Videos (Clean Visual Canvas Rule — STRICTLY NO CARDS / POP-UP OVERLAYS)**:
  - In educational and documentary explainer videos (especially animation, stop-motion, papercraft, claymation, 3D dioramas, and visual sequences), **DO NOT add motion graphics cards, floating stat boxes, or pop-up windows over the footage**. The animation/diorama art is already high-production value and is the primary visual hook; floating cards clutter the screen and obstruct the central action.
  - **What MUST be present**: Clean video footage, dynamic active tracking subtitles in safe zone, smooth motivated transitions (0.5s fade-in from black, 0.367–0.5s `xfade` crossfades), curated tactical SFX and foley, and video effects (subtle 5–8% punch-ins, speed ramps, reframes).
  - **Still Image / Thumbnail Hold**: In explainer videos containing an accompanying still image or thumbnail, hold it at the very END of the video for at least 0.1–0.2 seconds (e.g. 0.20s), never at the beginning.
  - **Where to use cards**: Reserve motion graphics cards, pop-ups, and comparison tables strictly for personal vlogs, talking-head videos, or affiliate product showcases.
- **Long-form explainer:** when using full-screen editorial diagrams, use them as full scene takeovers rather than floating cards over animation; alternate designed visuals and relevant footage; use 16:9 unless requested otherwise.
- **Vlog:** preserve personality, spontaneous moments, real ambience, and natural pacing; use context graphics when useful.
- **Shorts/Reels:** faster hooks/captions/graphic changes, 9:16 by default, and platform-safe composition.
- **Product/affiliate:** show the actual item and authentic proof; animate accurate facts and feature labels.
- **Mini-drama:** emotion, dialogue, continuity, and actor/character integrity first. Keep subtitles clean, avoid karaoke text for serious drama, and use only story-relevant graphics.
  - **Original Audio Primacy (STRICTLY NO TTS / Voiceover Dubbing)**: NEVER generate synthetic voiceover or dubbing (e.g., Kokoro TTS, Edge-TTS) for mini drama series. Mini drama footage already contains authentic recorded/generated character dialogue and environmental Foley. Use ONLY original audio from video clips.
  - **Single-Line Cadence for Subtitles**: Clean, static, elegant dialogue subtitles only — NO word-by-word karaoke highlights or animated bouncing words. Display **1 line at a time**, synchronized strictly to what the character is speaking at that moment. Never display multi-line stacked text blocks. Clean sans-serif (Liberation Sans / DejaVu Sans), 46-48pt bold, solid white (`&H00FFFFFF`) with 2.8–3.0px dark outline and 1.2px drop shadow. Centered lower-third with ~260–280px vertical margin (`MarginV=260-280`) staying clear of UI overlays without blocking characters' chests or faces. Strict synchronization with Filipino / Tagalog dialogue.

## Rule 9 — Inspect actual capabilities and assets
- Check installed HyperFrames/GSAP packages, existing style templates, fonts, available image/audio tools, and local SFX before choosing a technique.
- Use the strongest real supported workflow. If an effect requires a tool that is not installed, find a supported fallback or tell the user what is missing; never claim the effect rendered if it did not.
- Never overwrite original footage or raw project assets. Keep generated graphics/assets in a clearly named project subfolder where practical.

## Rule 10 — QC, deliverables, and honesty
Before delivery, verify dimensions/aspect ratio, frame rate, target duration, chosen video/audio streams, sync, dialogue clarity, captions, graphic spelling/legibility, safe zones, visual consistency, transitions, and SFX peaks. Inspect the opening, major graphics, representative middle sections, ending, and known-risk AI shots. Re-render clear defects when possible.

Deliver one requested master by default, plus subtitle sidecars when useful/requested. Do not create extra compression tiers or alternate ratios unless asked. Name the final `<slug>-final.mp4`. Report any unavailable asset, unsupported effect, missing source, or QC check that could not be performed.

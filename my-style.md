# Adaptive Editing Profile — Visual Style Guide (v2.0)

**Profile version:** 2.0  
**Applies to:** 16:9 long-form YouTube, explainers/documentaries, vlogs, creator videos, 9:16 Shorts/Reels, product/affiliate videos, and mini-drama/short film.  
**Core signature:** Premium, story-first editing with purposeful motion design, strong visual explanations, clear hierarchy, motivated transitions, layered sound design, and render verification. One profile adapts to the project; it does not force one identical look onto every genre.

## 1. Non-negotiable master principle

**Do not default to a wall of AI-generated video clips.** Footage is only one visual tool. For informational/explainer content, treat editor-built motion graphics, diagrams, kinetic typography, charts, comparisons, timelines, annotated screenshots, and sourced B-roll as first-class storytelling assets. Use AI-generated footage when it adds atmosphere, a human-scale illustration, an otherwise unavailable establishing shot, or cinematic texture—not as a substitute for a diagram, real data, a UI demonstration, or a precise explanation.

For every section, ask: **What does the viewer need to understand, feel, compare, remember, or verify at this exact line?** Choose the clearest visual. Use the user's direct brief first, then the matching preset below, then the actual assets and verified source material. Do not invent content or claim a tool/effect worked unless it was rendered and checked.

## 2. Before editing: inspect and plan

1. Inspect the full project folder: scripts, narration/audio, source video, reference stills, logos, fonts, existing edits, and the actual files in `my-sounds/catalog.json`.
2. Detect the format, aspect ratio, frame rate, total duration, source audio/video streams, and available graphics engine/templates. Explicit user instructions override inference.
3. For any explainer or long-form informational video, transcribe/inspect the final narration and create a visual beat map using `templates/adaptive-long-form-visual-beat-map.csv` or an equivalent Markdown/JSON plan **before the final edit**. Every major script beat must have a visual purpose, chosen visual type, on-screen text/assets, motion behavior, and audio cue (including “none” where silence is best).
4. If exact narration timecodes are available, anchor each beat to them. If not, map in script order first, then align to the actual voice track. Do not guess precise timecodes and present them as measured.
5. If the user supplies a logo, channel graphic, or reference video, inspect and reuse the real style. Never claim to have studied a channel aesthetic without inspecting actual assets/video.

## 3. Visual identity and system

### Brand handling
- Use actual supplied channel assets if available. If not, fallback informational palette: **graphite `#111318`, off-white `#F5F7FA`, signal lime `#C5FF3D`, and cyan `#58D5FF`**. Lime is the primary highlight; cyan is a secondary information cue. Use colors meaningfully, not as decoration.
- Do not force the fallback palette onto emotional fiction or naturalistic travel/vlog footage. Use it on chapter labels, title cards, or informational overlays only when it fits.
- Prefer one clean sans-serif family (Inter, Manrope, or an installed equivalent) with a disciplined weight hierarchy. Verify font availability. Use no more than two families and keep typography consistent across graphic components.
- Define reusable components: title/section label, lower third, key phrase, stat callout, diagram node, data chart, source tag, UI/screenshot frame, comparison panel, and end card. Keep stroke widths, corner radii, shadows, spacing, easing, and colors consistent.
- Aim for designed, editorial compositions—not a random pile of translucent cards. Glassmorphism is an optional treatment, not the default for every visual. Avoid generic dashboards/HUDs that do not convey information.

### Hierarchy and readability
- One primary message per designed scene. Supporting labels should not compete with the headline or narrated idea.
- Use short phrases for emphasis, not a complete transcription of the voiceover on every frame. Show exact wording when it is a quote, technical term, UI label, or essential claim.
- Keep important text readable on a small phone preview even in a 16:9 video. Avoid microtype, overly long lists, overlapping elements, and simultaneous movement in every layer.
- Preserve clear negative space around key text, diagrams, faces, hands, products, subtitles, and important footage.

## 4. Format presets — one profile, adaptive treatment

### A. Long-form YouTube / Explainer / Documentary (default 16:9)
- **Canvas:** 1920×1080 for a standard 16:9 master. Preserve genuine 4K when the source/workflow supports it; do not upscale merely to claim 4K. Match source/project frame rate where practical, commonly 24/25/30 fps.
- **Explainer Clean Canvas Rule (No Floating Cards):** For stop-motion, papercraft, claymation, and 3D animation explainer sequences, DO NOT add motion graphics cards, pop-up windows, or floating stat boxes over the art. The animation is the hero and retention hook; keep the visual clean with pure footage, motivated transitions, layered SFX, video effects, and subtitles only. Full-screen diagram takeovers are permitted only when replacing footage for abstract systems.
- **Editorial goal:** Every major spoken idea should become visible, not just audible. Mix designed motion graphics, diagrams, typography, charts, carefully chosen real/sourced B-roll, screenshots/UI, maps/timelines, and occasional real or AI-generated footage. The edit should not be 100% AI-generated video just because AI clips are easy to generate.
- **Explainer visual target:** At least half of the *major explanatory beats* should use purpose-built or sourced explanatory visuals (e.g., diagrams, animated text, truthful charts, comparisons, labeled screenshots, maps/timelines, or concrete B-roll) when the topic supports them. This is a planning target, not a rigid screen-time quota; use story and accuracy to decide.
- **Narration rhythm:** In dense voiceover passages, aim for a meaningful visual shift about every 5–10 seconds (graphic build, meaningful crop/reframe, new B-roll, screenshot annotation, diagram phase, or section change). A complex diagram may need 5–12 seconds to develop and remain readable. Hold important facts long enough to read; let emotional or cinematic footage breathe. Never force a cut on a stopwatch.
- **Hero moments:** Give each chapter a few custom hero visuals—an animated mechanism, comparison, timeline, important number, map, or diagram—that do real explanatory work. Use smaller callouts between them to maintain continuity, but do not turn every sentence into a pop-up.
- **Visual refreshes:** Alternate wide/context footage, designed graphics, detail inserts, charts, annotated screens, and clean footage. Avoid several visually identical scenes in sequence when the information changes.
- **Transitions:** Mostly clean cuts, J/L cuts, match cuts, graphic match transitions, motivated push/slide/mask reveals, and occasional short whip/blur transitions. Reserve elaborate transitions for a chapter break, strong visual connection, or genuine energy shift. Never apply the same transition between all shots.
- **Captions:** Do not force karaoke captions onto long-form by default. Use a separate `.srt` when available; burn subtitles only when requested or appropriate. Key-phrase typography is a graphic layer and should not compete with full subtitles.

### B. Vlog / Creator-led Video
- Preserve personality, natural delivery, real ambience, reactions, and useful pauses.
- Use animated lower thirds, location/time stamps, maps/route inserts when supported by real data, chapter labels, contextual lists, receipt/message/screen inserts, occasional kinetic punchlines, and B-roll that proves or illustrates what is being said.
- Use clean cuts, J/L cuts, match cuts, and motivated whip/movement cuts. Keep graphics secondary to the person and moment.
- Use ambience and action Foley sparingly but specifically. Do not turn organic vlog footage into a constant soundboard.

### C. Shorts / Reels / Other Vertical Short-form
- **Canvas:** 1080×1920 9:16 unless another ratio is requested. Reframe each shot intentionally; never blindly center-crop important subjects.
- Start with the strongest visual claim, question, result, conflict, or curiosity gap. Avoid long logo intros.
- **Explainer Clean Canvas Rule (No Floating Cards):** In vertical explainer videos (stop-motion, papercraft, 3D dioramas), remove floating cards or pop-up boxes over the video. Keep the presentation focused: clean visual footage, active word tracking captions in the safe zone, smooth crossfade transitions, layered SFX/foley, and video effects (punch-in zooms, speed ramps, reframes). Reserve motion cards strictly for talking heads, creator vlogs, or affiliate product showcases.
- Punch-ins (roughly 5–8%), speed ramps, masks, whip transitions, freezes, and impact moments are options, not mandatory decorations. Protect comprehension.
- Keep critical text out of platform UI areas and preview the final composition as a phone-sized frame.

### D. Product / Affiliate Video
- Make the real product visible and central. Use accurate feature labels, dimensions, price comparisons only when supplied/verified, test/result callouts only when the footage proves them, before/after comparisons only when genuine, and clean CTA emphasis.
- Sync Foley to physical actions. Use the actual product shot—not a generic AI substitute—when demonstrating texture, size, packaging, controls, or performance.
- Never invent specifications, discounts, stock availability, product certifications, reviews, or performance claims.

### E. Mini-drama / Short film / Episodic Fiction
- Protect acting, dialogue, facial expressions, eyelines, continuity, emotional timing, screen direction, and character identity. Motion design remains available, but must belong to the story.
- Use elegant dialogue subtitles, cinematic title/episode cards, diegetic messages/screens, time/place markers, visual motif transitions, and expressive ambience/Foley when story-relevant. Do not place generic explainer cards or HUDs over serious acting.
- Preserve reaction beats. Crossfades are optional and must never cause unintended dialogue overlap. Silence can be more powerful than a sound effect.

## 5. Long-form explainer visual language

Read `references/adaptive-long-form-explainer-motion-design.md` for the complete visual grammar, motion rules, sample beat maps, and sound design. The following decisions are mandatory:

- **Abstract idea or mechanism:** explain it with an animated diagram, flow, system map, hierarchy, timeline, feedback loop, or visual metaphor—not generic AI footage.
- **Specific place, person, physical activity, or real-world event:** prefer verified/sourceable footage or stills when factual accuracy matters; AI footage can be illustrative but must not be presented as real evidence.
- **A number, trend, or comparison:** use a truthful chart/counter/comparison built from verified values. Never use decorative or fabricated numbers.
- **A named term or key phrase:** introduce it through kinetic typography, then connect it to a concrete icon, object, example, or diagram.
- **A product/software/interface:** use genuine footage or screenshot and build animated pointers, highlights, masks, zooms, or UI callouts around it. Do not ask a video model to render legible UI text.
- **A claim that needs proof or context:** show the relevant source excerpt, document, chart, citation tag, or actual example. Do not add fake reference cards.
- **An emotional or human consequence:** real B-roll, a carefully labeled illustrative image/video, or a human-centered visual may be better than abstract infographics.

## 6. Motion design and effects

- Use varied animation principles: anticipation, eased entry, stagger, reveal/mask, overshoot-and-settle, draw-on lines, progressive diagram assembly, camera parallax, and controlled exit. Choose a small set of behaviors per sequence to establish a visual rhythm.
- Starting ranges: text/callout entrance 0.25–0.55s; line/node build 0.3–0.8s each; hero-stat or main chart reveal 0.6–1.2s; quick exit 0.2–0.4s. These are starting points, not hard limits—match the narration, complexity, and desired emotional weight.
- Use a quick settle after a spring/overshoot; avoid perpetual floating, idle wiggles, and constant parallax behind text.
- Camera punch-ins should usually be subtle for long-form (about 3–6%) and used only when there is a narrative reason. Use split screen or picture-in-picture when it clarifies a comparison or relation.
- Glitch, RGB split, heavy shake, lens flare, excessive motion blur, giant flashes, and 3D spins are rare accents. Do not stack them by default.
- No motion should cause the viewer to lose the information being explained. Allow a hold after major text/diagram reveals and delay the next competing event until the key idea has landed.

## 7. Sound and mix

- Build a clear hierarchy: dialogue/important production sound first; action Foley and meaningful ambience next; music below speech; accent SFX used selectively.
- Inspect `my-sounds/catalog.json` and select files that actually exist. Never invent a sound filename. Use one of the following only when context calls for it: soft UI tick/click for a labelled interaction, a short whoosh for directional movement, a subtle tonal ping for a key term, a restrained impact for a major reveal, or an environmental bed for place/continuity.
- Do not add SFX to every word, caption, cut, or card. A clean voice-only moment, natural ambience, or silence may be the correct design choice.
- Time an SFX to the visual landing/impact, not arbitrarily to the start of a scene. Avoid repetitive identical sounds. Fade tails naturally and check for clipping.
- Set music ducking from the actual voice and music levels, not a fixed volume preset applied blindly. Keep speech intelligible without harsh over-EQ or over-compression.
- As a practical online-master starting point, target roughly -14 to -16 LUFS integrated and true peak no higher than -1 dBTP, while respecting platform, source dynamics, and project requirements. Measure the final mix; do not assume normalization alone makes it balanced.

## 8. Technical and asset integrity

- Use installed HyperFrames/GSAP templates when available for dynamic HTML/SVG motion design. If unavailable, use the strongest supported fallback (e.g., native SVG/HTML/CSS assets, keyframed overlays, or FFmpeg compositing). Inspect the actual project and tools first.
- Do not create a fake “native” effect by merely describing it in notes. If the current renderer cannot animate an element, either create a supported asset/sequence or disclose the limitation and offer the closest working alternative.
- Use actual source data for charts, quotes, labels, maps, and UI. Attribute source-derived claims in a legible source note when appropriate. Preserve copyright/licensing constraints for footage, music, and images.
- Inspect and remove unintended AI character-reference flashes, duplicated/warped frames, visual hallucinations, flickering text, malformed hands/faces, logo/text mutations, unintended black frames, and mismatched audio. Do not remove an intentional story beat without checking context.

## 9. Delivery and QC

- Match the output ratio to the chosen preset: 1920×1080 for standard 16:9 long-form; 1080×1920 for 9:16 vertical; otherwise obey the explicit requested ratio and preserve source/project FPS where practical.
- Default to one polished requested master, named `<slug>-final.mp4`, plus `.srt` and `.ass` only when appropriate/generated. Do not create Telegram-size variants or other extra encodes unless requested.
- Verify exact duration against the master audio/target, stream mapping, frame dimensions, frame rate, A/V sync, voice/music mix, captions, and file integrity with available inspection tools.
- Review the opening, every hero graphic, every complex diagram/chart, representative transitions, the final minute/ending, and known-risk AI clips. Inspect a contact sheet or frames at useful intervals when possible.
- Watch on-screen text at full resolution and a phone-size preview. Verify the story still makes sense with no narration and that graphics do not misstate the narration.
- Correct defects and re-render where tools allow. Never claim an effect, source check, or QC step was completed unless it was actually performed. Report limitations honestly.

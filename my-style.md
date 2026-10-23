# PopUpLedger Studio — Adaptive Editing Style

**Profile version:** 1.0  
**Purpose:** One reusable editing identity for long-form YouTube, vlogs, YouTube Shorts, Reels, and mini-drama series.  
**Core direction:** Premium, story-first editing with purposeful motion graphics, confident pacing, polished sound design, motivated transitions, and a clear visual hierarchy. The result must not feel like a static slideshow or plain sequence of cuts.

## 1. Master Principle

Use one consistent editorial quality bar, not one identical treatment for every format. Adapt graphic density, rhythm, captions, color, transitions, and sound to the content. Every effect must clarify information, guide attention, strengthen emotion, sell an authentic product benefit, or improve rhythm. Do not add effects merely to prove that effects were used.

Priority order:
1. The user's direct instructions for this project.
2. The correct format/genre preset in this file.
3. The available footage, script, recorded audio, brand assets, and factual source material.
4. The default PopUpLedger visual identity below.

Before editing, inspect all project assets, aspect ratios, durations, audio tracks, available fonts, motion-graphics templates, and `my-sounds/catalog.json`. If the brief explicitly names a format, obey it. Otherwise infer from the request and media; state the inference in the edit plan when it could materially affect the result.

## 2. Visual Identity

### Brand handling
- If a supplied logo, channel intro, thumbnail, brand guide, or recurring graphic exists, sample and reuse its real visual language.
- Do not claim to have inspected the PopUpLedger channel's visual branding unless actual channel assets or videos are available in the project.
- If no brand assets exist, use this fallback palette for informational graphics: **graphite `#111318`, off-white `#F5F7FA`, signal lime `#C5FF3D`, and clear cyan `#58D5FF`**. Use lime for the primary highlight and cyan sparingly for secondary information.
- The fallback palette is not mandatory for cinematic fiction or naturalistic vlogs. For those, preserve the scene's emotional color grade and use the brand accent only on chapter cards, opener/ender graphics, or other appropriate overlays.
- Use one clean sans-serif family for most graphics (e.g. Inter, Manrope, or a locally installed equivalent); verify the font exists before rendering. Use a restrained display face for titles only when available.
- Establish a repeatable system for title cards, lower thirds, section labels, statistic callouts, and end cards. Keep corner radius, stroke weight, spacing, easing, and accent usage consistent.

### Design quality
- Prefer layered composition, clear hierarchy, negative space, and purposeful contrast over generic templates.
- Text and cards should enter with motion (spring, masked reveal, tracking/scale, or directional slide) rather than a flat opacity fade alone when the chosen renderer supports it.
- Use animation curves intentionally: quick ease-out for information, spring/back easing for lively emphasis, smooth ease-in-out for cinematic moves.
- Keep all critical text readable at phone size. No cluttered stacks of labels, tiny paragraphs, decorative HUDs with no meaning, or graphics covering faces, hands, product details, or story-critical action.
- Build graphics from actual story/script/data. Never fabricate figures, labels, quotes, map routes, product features, evidence, or interface screenshots.

## 3. Automatic Format Presets

Choose the best matching preset before timeline assembly. When a project combines styles, use a primary preset and borrow secondary elements only where appropriate.

### A. Long-form YouTube / Documentary / Explainer
- **Default canvas:** 16:9, 1920×1080; preserve 4K only when source footage and render resources justify it. Match source frame rate where practical (commonly 24, 25, or 30 fps); do not silently convert frame rates unnecessarily.
- **Narrative:** Cold open or compelling opening beat, clear premise, logical chapters, visual proof, varied pacing, and a satisfying close. Use chapter/section bumpers only where they help orientation.
- **Motion-graphics expectation:** This mode must not be plain talking-head cuts. Add relevant designed visual beats throughout: animated lower thirds, kinetic key phrases, key-point cards, number/stat callouts, diagrams, chart builds, timelines, maps, comparisons, source/reference cards, split screens, picture-in-picture, or labeled B-roll. Use only the elements supported by the actual content.
- **Visual rhythm:** Aim for a meaningful visual refresh about every 6–12 seconds during narration-heavy sections (e.g. B-roll, reframing, a graphic, a crop change, a visual example). Allow longer holds for complex information, important reactions, demonstrations, and cinematic footage. Do not force a cut at a fixed interval.
- **Graphics density:** Create several purposeful hero graphics per chapter and smaller supporting callouts at natural information beats. Key facts, turning points, comparisons, and unfamiliar terms deserve a designed treatment; not every sentence needs a popup.
- **Transitions:** Hard cuts, J-cuts/L-cuts, match cuts, motivated push/slide transitions, and occasional short whip or mask transitions. Save elaborate transitions for chapter changes or genuine visual links. Avoid default crossfades between every clip.
- **Camera treatment:** Subtle reframing/punch-ins (roughly 3–6%) on topic changes or emphasis; split screen and picture-in-picture when they improve comparison or context. Use speed ramps only for footage with a clear motion/action beat.
- **Sound:** Build ambience, music, action Foley, and accent SFX as separate purposeful layers. Give major claims, chapter reveals, visual proofs, and section turns distinct but not repetitive sound cues.

### B. Vlogs / Creator-led Videos / Talking Head
- **Canvas:** Match requested distribution; default to 16:9 landscape for a normal YouTube vlog and 9:16 only when requested or when the footage is clearly made for vertical platforms.
- **Rhythm:** Keep personality and natural delivery. Remove distracting dead air and failed takes but retain meaningful pauses, reactions, laughter, and ambience.
- **Motion graphics:** Animated lower thirds, location/time stamps, map or route inserts when supported by assets, chapter labels, quick lists, message/receipt inserts, contextual labels, playful but restrained stickers, and short kinetic punchlines. Use the brand system consistently.
- **B-roll:** Use cutaways, detail shots, establishing shots, contextual inserts, and occasional split screen to hide edits and make the story easier to follow.
- **Transitions:** Mostly clean cuts, J/L cuts, match cuts, and motivated whip or movement cuts. Use flash, spin, or glitch effects sparingly and only where the footage/style supports them.
- **Sound:** Retain useful real location ambience. Add light Foley for physical actions and short whooshes/pops for a few graphic reveals; keep vlog audio organic, not like a constant soundboard.

### C. YouTube Shorts / Instagram Reels / Other Vertical Short-form
- **Default canvas:** 9:16, 1080×1920. Reframe every shot intentionally instead of blindly center-cropping. For another requested aspect ratio, obey that request.
- **Opening:** Start with the strongest visual, question, conflict, result, or curiosity gap. Avoid long logo intros. Make the point immediately clear.
- **Rhythm:** Higher information density than long-form; remove genuinely empty pauses, use purposeful jump cuts, punch-ins (roughly 5–8%), insert shots, and strong visual changes at narrative beats. Preserve enough breathing room for comprehension.
- **Captions:** Use bold, high-contrast phrase-based captions; word-by-word active highlighting is allowed and preferred for fast explainers, commentary, affiliate demos, and energetic short-form. Use the accent color to emphasize only selected words/numbers, not every word. Keep captions away from faces and platform interface zones.
- **Motion graphics:** Strong kinetic hooks, animated labels, proof callouts, comparison cards, progress markers, chart/stat animations, and clean CTA end beats when relevant. Graphics should help the viewer understand the hook, proof, or payoff.
- **Transitions and VFX:** Quick whip/mask transitions, zoom matches, match cuts, speed ramps, freeze-frame callouts, and short impact frames as motivated. Avoid applying all of them to every cut.
- **Sound:** Tightly synchronized pops, whooshes, ticks, impacts, and accents. Do not place an SFX on every word or every edit.
- **Safe areas:** Keep critical text away from the top and bottom interface zones and validate legibility on a phone-sized preview.

### D. Mini-drama / Short film / Episodic Fiction
- **Default canvas:** Preserve the requested/shot format. Use 9:16 for vertical series and 16:9 for landscape drama.
- **Priority:** Acting, eyelines, dialogue intelligibility, continuity, emotional beats, character identity, and coherent screen direction come before graphic density.
- **Captions:** Clean, static or gently revealed dialogue subtitles; never use bouncing karaoke words for serious/emotional scenes unless explicitly requested. Use a clean sans-serif, white text, dark outline/shadow, and format-specific safe zones. Match spoken language exactly after transcript review.
- **Motion graphics:** Use cinematic title/episode cards, subtle scene labels, diegetic phone messages/screens when story-relevant, flashback/time markers, split-second freeze-frame emphasis, or graphic match transitions when they serve the plot. No random floating explainer cards over emotional dialogue.
- **Transitions:** Choose from motivated cuts, match cuts, short dissolves, sound bridges, whip cuts for action, flash-frame/blur for subjective memory, and deliberate fades. A 0.5s crossfade is an option, not a mandatory transition between every shot. Never crossfade over overlapping dialogue without checking timing.
- **VFX:** Preserve character and location continuity. Use restrained grain, halation, lens bloom, vignette, speed ramp, handheld shake, or flash effects only when they suit the scene and available processing supports them. Never add a visual effect that changes story facts or character appearance.
- **Sound:** Use believable room tone and location ambience; add synchronized tactile Foley (steps, doors, fabric, props), perspective-based movement, emotional score, tension risers, and selective impacts. Silence can be a powerful beat. Cliffhangers may use a deliberate hold, audio drop, or fade only when the scene earns it.

### E. Product / Affiliate / Demonstration Video
- **Narrative:** Problem/need → product reveal → feature proof → real demonstration → value summary → CTA, adjusted to the available footage and truthful claims.
- **Motion graphics:** Animated feature labels, dimensions/prices only when supplied, feature checklists, side-by-side comparisons, product detail magnification, step markers, and clean CTA. Never cover the product or invent a specification.
- **Sound:** Sync Foley to real touches, opening, placement, use, and packaging. Use price/reveal accents tastefully; do not add a checkout sound unless there is an actual CTA context.
- **Product integrity:** Do not alter the shape, logo, color, quantity, or demonstrated performance of the product through misleading VFX.

## 4. Motion Graphics Toolkit

Use whichever options the installed HermiEditor/HyperFrames/GSAP/FFmpeg setup genuinely supports. Prefer the following building blocks:
- Kinetic headline or key-phrase reveal; animated word/line mask; letter-spacing or scale emphasis.
- Animated lower-third with name, role, location, or chapter (only from known information).
- Stat/number count-up, bar build, timeline, comparison table, label pointer, or diagram reveal from supplied facts.
- Floating media window, picture-in-picture, screen mockup, source card, map, annotation, or crop-in detail when assets/data support it.
- Freeze-frame with tracked/anchored callout only if reliable tracking is supported; otherwise use a fixed or manually positioned pointer.
- Chapter bumper, series title, end card, and subtle brand sting.
- For each graphic, define entry, hold, and exit timing; make it readable long enough to process; remove it before it conflicts with the next story beat.

If an advanced animation cannot be rendered reliably, use the best clean supported alternative (e.g. animated SVG/HTML overlay or simpler FFmpeg compositing). Do not silently output a still card when the brief calls for motion without first attempting a feasible animation.

## 5. Transitions and Video FX

- **Default edit is a clean cut.** Pick a transition because the action, camera movement, sound, time, mood, or information connects across shots.
- Short energetic transition: typically 0.12–0.35s. Cinematic transition: typically 0.25–0.65s. Longer fades are reserved for opening/ending or meaningful time/scene changes. These are starting ranges, not rigid requirements.
- Prioritize J-cuts, L-cuts, match cuts, action cuts, motivated whip pans, masking wipes, speed ramps, foreground wipes, and intentional audio bridges.
- Use motion blur only when movement warrants it. Use camera shake only for a real impact/action beat. Use glitch/RGB split only for digital disturbance, deliberate stylization, or a story cue—not as a default transition.
- Stabilize shaky footage only as needed and watch for warping/cropping artifacts. Match white balance, exposure, and contrast across adjacent shots before adding a stylized grade.
- Inspect every effect for bad masks, exposed edges, flashes, duplicate frames, abrupt scale jumps, or mismatched motion.

## 6. Sound Design and Mix

Create a deliberate audio hierarchy: **dialogue/important production audio → story/action Foley → key SFX → music/ambience**. For dialogue-led content, speech must remain clearly intelligible.
- First inspect audio files and `my-sounds/catalog.json`; use actual available curated sounds. Do not invent a filename or assume a sound exists without checking.
- Use real ambience as the bed where appropriate. Add small Foley details for meaningful physical actions and room/location continuity.
- Use short UI pops/clicks for graphics, whooshes for directional movement, soft ticks for data reveals, and low impacts/risers for genuine major beats. Vary or omit cues when repetition becomes noticeable.
- Use sidechain compression or volume automation to duck music under speech, usually by about 4–8 dB as a starting point; make deeper dips for whispers, dense facts, or emotional dialogue. Restore music naturally between speech phrases.
- Do not apply a fixed `volume=0.07` blindly to every BGM file. Levels must be set against the actual source audio and the final mix.
- Clean dialogue with gentle high-pass filtering near 70–100 Hz when appropriate, corrective EQ, light compression, and de-essing if needed. Do not over-process or boost a frequency without listening/checking for harshness.
- Practical final target for a typical online master: about **-14 to -16 LUFS integrated** and **true peak no higher than -1 dBTP**, adjusted for the content and platform. Check meters; do not rely on a guessed filter value. Do not normalize individual tracks to the final-master target before mixing.
- Avoid clipped peaks, phasey dialogue, abrupt music cuts, SFX louder than the story moment, and silent gaps caused by incorrect stream mapping. Ensure the intended voice/music mix is actually mapped into the final render.

## 7. Captions, Text, and Safe Zones

- Review ASR output against actual dialogue, especially names, Filipino/Tagalog/Taglish, slang, products, and numbers. Correct transcription errors; do not paraphrase quoted dialogue unless requested.
- Long-form: phrase-level captions are optional; supply `.srt` when available. Burn subtitles only when asked or when the preset/source calls for it.
- Shorts/Reels: dynamic captions are expected for spoken explainers/commentary/affiliate content unless the user requests otherwise. Emphasize only key terms and retain natural line breaks.
- Vlogs: use full captions if requested; otherwise prefer selective captions for key jokes, names, locations, or important points when useful.
- Mini-drama: use dialogue subtitles, not karaoke animation by default.
- For 16:9, keep titles and lower-thirds comfortably inside frame margins and away from faces. For 9:16, allow wider UI-safe margins at top and bottom and test actual platform composition. Never assume one `MarginV` value fits all sizes.
- Avoid auto-generated subtitle overlap with faces, lips, props, graphics, or platform UI. Keep contrast and line lengths consistent.

## 8. Color, Continuity, and Source Integrity

- Match exposure, white balance, contrast, and skin tone across the sequence before adding a creative look.
- Use a project-consistent look: natural and crisp for informational/vlog content; controlled contrast and motivated palette for fiction; product colors must remain truthful.
- Respect character continuity, wardrobe, setting, screen direction, spatial geography, product identity, and the order of real actions.
- Remove AI-generation reference flashes, single-frame artifacts, unintended black frames, broken frames, and obvious continuity glitches when detectable. Never remove a frame that is a deliberate plot/visual beat without checking context.

## 9. Quality-Control Checklist

Before final delivery:
1. Confirm aspect ratio, dimensions, duration, frame rate, audio sync, and intended audio stream with `ffprobe` or equivalent.
2. Review the opening, every transition-heavy section, graphics, captions, ending, and any known-risk AI clips. Inspect a contact sheet or representative frames when tools permit.
3. Check that motion graphics animate, remain inside safe zones, do not hide story-critical details, and have no off-screen text or unrendered assets.
4. Listen to the beginning, dialogue-heavy sections, major SFX moments, and ending. Verify voice/music balance, no clipping, no unintended silence, and no abrupt SFX tails.
5. Verify that the edit is not static/plain: use purposeful visual changes and designed emphasis appropriate to the preset.
6. Verify that it is not over-edited: remove redundant zooms, repetitive whooshes, irrelevant graphics, random glitching, and transitions that damage comprehension or emotion.
7. Export the requested master and subtitle sidecars where appropriate. Do not create extra compressed/Telegram variants unless requested.
8. Report any unmet requested effect caused by missing tools/assets instead of pretending it rendered.

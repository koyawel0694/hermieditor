# PopUpLedger Studio — Persistent Editing Rules v3.0

These rules apply across harnesses and supported editing/rendering tools.

## Rule 1 — Ask how to choose the style, once
When a new project starts and the user has not already stated a creative-direction mode, ask the one-question selector in `templates/motion-graphics-direction-menu.md`:
- A: Auto-director chooses styles based on brief/script/references;
- B: User chooses from the style library;
- C: User describes a custom direction;
- D: Hybrid proposal then user approval.

Do not ask again within the project once answered. Do not block on low-impact unanswered details. If the user explicitly says “decide for me,” choose A. If their prompt already describes the intended style in detail, infer C or D and proceed unless approval is explicitly required. For a new project with existing style preferences but no fresh answer, honor the saved/project brief choice where available.

## Rule 2 — Style library is a decision menu, not a checklist
Read `references/popupledger-motion-graphics-style-library.md`. Choose one primary visual language and up to two complementary families by default. Use additional families only when the user requests an intentionally mixed style or the story genuinely warrants it. Maintain consistent typography, palette, spacing, line language, easing and audio style.

## Rule 3 — Reference media must be observed honestly
For each supplied reference, inspect accessible video/stills or metadata. Extract movement, visual density, composition, transitions, typography, texture, color and sound cues. If direct playback is inaccessible, mark visual observations as unverified and ask for a still/screen recording only if the missing detail materially changes the project. Never pretend to have watched inaccessible footage. Recreate the underlying design logic rather than copying a reference frame-for-frame.

## Rule 4 — Motion graphics first when they explain better
For explainers, treat diagrams, flowcharts, cause/effect sequences, comparisons, timelines, hierarchy/relationship maps, data visualizations, numbers, UI demonstrations, screenshots, source excerpts, maps, visual metaphors, illustrations, tracked callouts, animated objects and kinetic phrases as first-class visual assets. AI-generated footage is selective support—not a substitute for factual diagrams, evidence, readable text or interface captures.

## Rule 5 — Plan long-form before rendering
Analyze the narration and create `templates/popupledger-long-form-visual-beat-map.csv` or a structured equivalent before final assembly. Each major beat specifies purpose, visual family, design component, exact on-screen copy/data, source/path, entrance/build/hold/exit, audio cue or `none`, and QC risks. Align estimated times to the real narration/audio before final timing; label estimates honestly.

## Rule 6 — Make visuals progressive and legible
Build diagrams in narration order. Reveal anchor → component → relationship → consequence → complete model. Hold the finished visual long enough to understand. One dominant visual message per scene; short labels rather than transcript-sized cards. Move, reveal, and settle before dense copy must be read. Never use a graph, arrow, icon or map that misstates the content.

## Rule 7 — Use transitions with purpose
Prefer clean cuts, match cuts, J/L cuts, motion-matched wipes, shape transitions, masks and camera movement when they support continuity. Save stronger whip, glitch, flash, zoom blur, impact or distortion for a genuine energy change or dramatic beat. No automatic transition on every cut.

## Rule 8 — Sound design is intentional
Dialogue/narration remains intelligible and primary. Use the real curated sound catalog if available. A graphic SFX must be synchronized to a meaningful graphic/action/transition. Use silence or natural ambience when best. Do not insert an SFX for every word or UI element. Mix music with listening/meters/automation instead of a universal fixed level.

## Rule 9 — Tool and source honesty
Inspect available renderers and project assets first. Never claim to have created 3D, tracking, particles, parallax, or advanced transitions unless the actual toolchain supports and renders them. If unsupported, choose a faithful alternative and disclose what could not be executed. Critical text and data should be created with exact-text/vector-capable tools. Source factual claims and never invent chart values, quotes, source URLs, product features, or attributions.

## Rule 10 — Adaptive aspect ratios
Respect explicit format. Standard 16:9 long-form: usually 1920×1080. 9:16 vertical: usually 1080×1920. Vlog, product, and mini-drama can use the requested format. Never apply vertical export or vertical safe-zone settings to landscape work by default.

## Rule 11 — Captions follow the format
Long-form: subtitles/captions are optional or provided as a sidecar unless the user requests burn-in; do not force karaoke by default. Shorts/Reels: readable phrase-led captions are usually useful. Mini-drama: accurate dialogue subtitles with character/story timing. Verify proper nouns, technical words, dates, numbers, and Tagalog/Taglish. Never claim a transcript was verified if it wasn't.

## Rule 12 — Preflight and final QC
Before rendering, check format/duration, narrative order, asset paths, missing media, font availability, readable text, data/source accuracy, audio mapping, and tool availability. After rendering, inspect the actual output for aspect ratio, duration, frame rate, A/V sync, dialogue/music balance, typography, clipping/overlap, animation glitches, transition artifacts, caption timing, missing assets and proper end frame. Report real failures plainly.

## Rule 13 — Keep project outputs lean
Deliver one requested final master and appropriate subtitle/working files. Do not create alternate resolutions, compressed variants, thumbnails or extra deliverables unless requested. Keep a design brief, style choices, asset/source manifest and beat map for complex explainer projects.

## Rule 14 — Explainer Clean Canvas Rule (No Floating Cards over Craft Footage)
In crafted explainer videos (stop-motion, papercraft, claymation, 3D animations, dioramas, and documentary sequences), **DO NOT add motion graphics cards, floating stat boxes, or pop-up windows over the footage**. The visual art is the hero and primary hook; overlays block the central action and ruin the viewer's focus on the craft. Keep the presentation focused: clean visual footage, active word-tracking subtitles in the safe zone, smooth motivated transitions (0.5s fade-in from black, 0.367–0.5s crossfades), curated tactical SFX/foley, and video effects (subtle punch-in zooms, speed ramps, reframes). Reserve floating motion cards strictly for personal vlogs, talking-head videos, or affiliate product showcases.

## Rule 15 — Tangible Motion Graphics & Kinetic Typography (Zero UI Box Rule)
For dedicated motion graphics, kinetic typography, and music video samples, avoid generic SaaS dashboard cards, grey bordered boxes, and floating badges. Treat typography and visual metaphors as **living elements in 3D environment space**:
1. Words as physical architecture/props (casting light, extruded in 3D space, wrapped in chains, anchored behind terrain, hanging on ropes).
2. Diegetic visual metaphors (opening doors, radios, speech bubbles, clocks, lanterns, snare drums) directly interacting with lyrics.
3. Continuous kinetic camera flight (zooming through letter counters, Dutch angle tilts, seamless spatial dollying) rather than static slide cuts.

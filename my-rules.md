# PopUpLedger Studio — Persistent Editing Rules

These are persistent preferences for this user's HermiEditor workspace. Read them with `my-style.md` before editing every new project.

## Rule 1 — One Adaptive Profile for Everything
- This is the single editing profile for long-form YouTube, vlogs, Shorts, Reels, affiliate/product videos, and mini-drama series. Do not create disconnected styles for each format.
- Use the matching preset in `my-style.md` and preserve the shared quality bar: polished pacing, designed visual hierarchy, deliberate motion, layered sound, consistent typography, clean finishing, and quality control.
- A profile request for professional, motion-rich editing counts as explicit permission to use appropriate motion graphics, transitions, VFX, and SFX. Do not fall back to a plain-cut-only edit simply because the user did not name each effect individually.
- Match effects to context. Motion-rich does not mean every clip needs an effect; it means each section has intentional visual and audio design where the content supports it.

## Rule 2 — Resolve Format Before Editing
- Inspect the user's brief first. The user's explicit format, aspect ratio, tone, duration, language, and platform take priority.
- If not explicit, use the media's aspect ratio and project context to infer a preset. Do not crop a landscape project into vertical or a vertical project into landscape without a reason.
- For mixed-format delivery, build the primary requested format first. Make alternate reframes only when requested or when the source composition supports them.
- For long-form 16:9, use `my-style.md`'s long-form preset. For vlogs, preserve human moments and useful real-world ambience. For Shorts/Reels, use faster visual changes and platform-safe captions. For mini-drama, protect performances, dialogue, continuity, and dramatic timing.

## Rule 3 — Default to Designed, Not Plain
For informational, narrative-explainer, creator-led, and product content, actively look for moments that benefit from:
- kinetic titles and section labels;
- animated lower thirds and callouts;
- number/stat/chart/diagram builds based on supplied facts;
- comparison layouts, picture-in-picture, screen inserts, source cards, maps, timelines, or labeled B-roll;
- speed ramps, motivated zooms, match cuts, masked transitions, and other appropriate video treatments;
- layered ambience, Foley, graphic-entry sounds, transition whooshes, and selective emphasis impacts.

Do not use an element merely to hit a quota. Every design beat must support the story, clarity, emotion, comedy, proof, or retention.

## Rule 4 — No Repetitive Effects
- Do not use the same transition between every clip.
- Do not apply automatic punch-ins on a fixed timer if they conflict with the shot, speaker, or emotion.
- Do not add an SFX to every cut, word, caption, or graphic. Rotate, soften, or omit cues to avoid a cheap, repetitive soundboard feeling.
- Avoid default glitch, RGB split, camera shake, lens flare, spin, and overdone whoosh effects. Use them only when motivated by the footage or genre.
- Never let an overlay obscure a face, important action, product proof, chart label, subtitle, or other essential detail.

## Rule 5 — Mini-drama Exception: Emotion Comes First
- **Original Audio Primacy (STRICTLY NO TTS / Voiceover Dubbing)**: NEVER generate synthetic voiceover or dubbing (e.g., Kokoro TTS, Edge-TTS) for mini drama series. Mini drama footage already contains authentic recorded/generated character dialogue and environmental Foley. Use ONLY the original audio from the video clips.
- **Subtitles & Single-Line Cadence**: Clean, static, elegant dialogue subtitles only — NO word-by-word karaoke highlights or animated bouncing words. Display **1 line at a time**, synchronized strictly to what the character is speaking at that moment. Never display multi-line stacked text blocks. Clean sans-serif (Liberation Sans / DejaVu Sans), 46-48pt bold, solid white (`&H00FFFFFF`) with 2.8–3.0px dark outline and 1.2px drop shadow. Centered lower-third with ~260–280px vertical margin (`MarginV=260-280`) staying clear of UI overlays without blocking characters' chests or faces. Strict synchronization with Filipino / Tagalog dialogue.
- Do not place non-diegetic HUDs, explainer cards, or generic popup windows on top of serious acting. Use cinematic title/episode cards, story-native text messages, flashback markers, sound bridges, carefully motivated VFX, and purposeful Foley instead.
- Preserve reaction pauses, eyelines, dialogue timing, character continuity, and geography. Crossfades are optional and must not cause dialogue overlap.
- Use silence or a sustained sound cue when it creates a stronger dramatic beat than another impact.

## Rule 6 — Use Real Assets; Verify Effects Exist
- Inspect `my-sounds/catalog.json` and the installed template/reference directories before choosing sound files or animation templates.
- Do not invent filenames, assume unavailable packages are installed, or claim a graphic is tracked if only fixed positioning is supported.
- Prefer curated audio assets already in `my-sounds/`. If a requested asset/effect is missing, use a clean supported substitute or clearly report the limitation.
- Use user-provided logos, photos, footage, fonts, and data accurately. Do not invent facts, prices, citations, statistics, product specifications, or story details.

## Rule 7 — Audio Must Be Designed and Intelligible
- Keep dialogue/important production audio in front. Automate or sidechain-duck BGM under speech based on actual source levels; do not copy a fixed BGM volume value across all projects.
- Add appropriate room tone/ambience, real-action Foley, music transitions, and selective accent SFX. Include fade/tail handling so sounds do not terminate abruptly.
- Prevent clipping, missing audio streams, voice masking, unintended silence, and music/SFX overpowering dialogue. Verify the final mixed audio and stream mapping.

## Rule 8 — Inspect and Audit Every Render
- Before rendering, check source duration, aspect ratio, audio, and any AI-video artifacts. Verify the edit plan against the requested output.
- After rendering, verify the file with `ffprobe` or equivalent and inspect representative frames/timeline sections when available.
- Check opening hook, scene/section flow, caption correctness, safe areas, animation timing, transition artifacts, sound balance, the ending, and audio/video sync.
- Render a corrected version if clear mistakes are found and the tools permit it. Never state an issue was fixed unless the final output was checked.

## Rule 9 — Deliver Cleanly
- Default to one polished master in the requested aspect ratio plus `.srt` (and `.ass` if generated/needed). Provide extra compressed versions, alternate ratios, or multi-tier exports only when requested.
- Use descriptive filenames and do not overwrite raw footage or original finals.
- If a requested effect or quality check could not be performed, state that limitation transparently.

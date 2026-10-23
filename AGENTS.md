# HermiEditor: Hermes Agent Operational Instructions


## PopUpLedger Adaptive Editing Profile v3.0 — Creative Direction Gate

At the start of a new project, if the user has not already given a clear visual direction, ask exactly once using `templates/motion-graphics-direction-menu.md`: A) Auto-director, B) user selects from styles, C) custom user direction, D) propose treatment and wait for approval. Remember the choice in the project brief. Don't repeatedly request approval for routine choices when Auto-director is selected.

Read `my-style.md`, `my-rules.md`, and `references/popupledger-motion-graphics-style-library.md`. For long-form explainers, use `references/popupledger-long-form-explainer-motion-design.md` and create a visual beat map before final assembly. Choose one primary style family plus up to two supporting families by default; use diagram animation, pop-ups, UI motion, collage, parallax, tracking, charts, timelines and other techniques based on the content, not as a checklist. Use accurate designed graphics and sourceable footage as appropriate; AI video remains selective. Match aspect ratio to the requested format, use sound effects only when motivated, and inspect the actual rendered master.


HermiEditor is an adaptive video editing suite for Hermes Agent, covering 16:9 long-form YouTube explainers/documentaries, vlogs, 9:16 Shorts/Reels, product/affiliate videos, and episodic mini-dramas from footage, narration, graphics, and selected AI-generated assets.

## Workspace Layout

- `skills/hermieditor/SKILL.md`: The Hermes skill definition. Auto-linked to `~/.hermes/skills/media/hermieditor/` by `setup.mjs`.
- `my-style.md`: Lasting style preferences and format presets.
- `my-rules.md`: Cumulative rules and persistent instructions.
- `inbox/`: Working folder where raw video footage and voiceover tracks are placed (`inbox/<slug>/`).
- `outbox/`: Requested master `<slug>-final.mp4` plus relevant `.srt`/`.ass` sidecars; extra compression tiers only when requested.
- `my-sounds/`: Curated 69-sound library (`mini-drama/`, `explainer/`, `us-niche/`), indexed in `catalog.json`.
- `templates/`: Boilerplate scripts and planning templates (`adaptive-long-form-visual-beat-map.csv`, `adaptive-explainer-project-brief.md`, `generate_captions.py`, `build_audio.py`, `render_pipeline.py`).
- `references/`: Reference playbooks including `adaptive-long-form-explainer-motion-design.md`.
- `tools/`: Free word-level transcription via Groq or local faster-whisper.
- `kit/`: Herk Edit Kit engine (sparse-checked-out for HyperFrames and motion cards).

## How Hermes Operates HermiEditor

When the user asks you to edit a video:
1. **Identify the project folder** in `inbox/<slug>`.
2. **Transcribe voiceover**: Run `node tools/transcribe.mjs <audio_path>`.
3. **Inspect clips and timeline**:
   - Check duration of audio and clips with `ffprobe`.
   - Check first 1.5s for AI video reference image flash artifacts (`ffmpeg -ss 0.0 -t 1.5 -i clip.mp4 -filter_complex "select='gt(scene,0.25)',metadata=print" -f null -`).
4. **Plan visuals and captions**:
    - Ask the A/B/C/D creative-direction question once if the project direction is not already explicit. For long-form explainers, create a visual beat map and asset/source manifest before final assembly.
    - Match visuals to meaning: designed diagrams for mechanisms, factual charts for verified numbers, genuine screenshots for real interfaces, sourced footage for factual context, and selective AI footage for illustrative/cinematic purpose.
    - Captions depend on format: long-form subtitles/sidecars rather than forced karaoke; dynamic phrase emphasis for Shorts/Reels where useful; accurate dialogue subtitles for mini-drama. Verify names, numbers and language.
    - Use format-specific safe zones and follow the requested aspect ratio.
5. **Master Audio**:
    - Prioritize dialogue clarity; apply cleanup/EQ/compression only where appropriate and listen to the actual result.
    - Balance music with listening, metering and automation/sidechain as appropriate; avoid one fixed BGM level for every file.
    - Use sound effects for meaningful visual/action/transition cues only. Voiceover alone does not require SFX; ambience or silence can be best.
6. **Composite & Export Deliverables**:
    - Match requested/project ratio: standard 16:9 long-form is typically 1920x1080; 9:16 vertical is typically 1080x1920; preserve source/project FPS where practical.
    - Deliver one requested master plus relevant subtitle sidecars by default. Avoid extra compression tiers or alternate ratios unless requested.
    - Inspect the actual final render for dimensions, duration, A/V sync, audio mapping, captions, motion graphics, artifacts and end frame.

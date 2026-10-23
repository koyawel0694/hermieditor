# HermiEditor: Hermes Agent Operational Instructions

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
   - For long-form explainers, read the adaptive explainer motion-design reference and create a script-to-visual beat map before final assembly. Use diagrams, progressive graphic builds, truthful charts, comparisons, timelines, annotated real screenshots/source inserts, and relevant B-roll; AI-generated footage is selective, not the default for every sentence.
   - Captions depend on format: long-form uses an optional subtitle sidecar and no karaoke by default; Shorts/Reels can use dynamic phrase/word emphasis; mini-drama uses clean dialogue subtitles. Verify transcription, especially names, figures, and Tagalog/Taglish.
   - Use format-specific safe zones. Do not reuse a 1080x1920 portrait `MarginV` value in landscape projects.
5. **Master Audio**:
   - Set dialogue clarity by listening and checking actual levels; use gentle cleanup/EQ/compression only where appropriate, not a fixed chain blindly on every voice.
   - Set music under speech with listening, metering, and automation/sidechain as appropriate. Avoid a universal hard-coded BGM volume for every source file.
   - Use curated SFX from `my-sounds/` only for meaningful graphic/action/transition cues. Voiceover alone does not require SFX; clean dialogue, ambience, or silence can be the best design.
6. **Composite & Export Deliverables**:
   - Use the requested/project aspect ratio: standard 16:9 long-form is 1920x1080; 9:16 vertical is 1080x1920; obey any other explicit request and preserve project FPS where practical.
   - Deliver one requested master (`<slug>-final.mp4`) by default plus appropriate/generated subtitle sidecars. Do not generate `under20mb`/`hq-48mb` variants or alternate ratios unless requested.
   - Keep the final master in `outbox/`; verify dimensions, duration, A/V sync, audio stream mapping, captions, graphics, and the actual final render before delivery.

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

### Universal Trigger: "Edit this mini drama series" or alike prompts
When John says **"Edit this mini drama series"** (or provides an episodic drama prompt like "edit this video using adaptive editing profile"):
1. Automatically activate the complete **PopUpLedger v3.0 Mode B: Mini Drama Series** pipeline.
2. Ingest the 4-track Signature BGM Suite with **Silence vs. Music Discipline (Anti-Wall-to-Wall BGM Rule)**:
   - **DO NOT play BGM wall-to-wall in every scene**. Music is only as powerful as the silence that precedes it.
   - **Keep in pure diegetic silence (NO BGM)**:
     * Administrative deadlines, ticking clocks, and heavy mechanical stamp/document thuds.
     * Hushed gossiping corridors, whispering student clusters, and forum phone chat screens.
     * Confrontations, standoffs, and verbal dominance: cut to **DEAD SILENCE** when an adversary steps in so resonant spoken dialogue commands absolute moral authority.
   - **Score ONLY when specifically motivated by story progression**:
     * Track 1 (Climactic Triumph / Reward Swell): Peaks at **-8 dBFS** on system reward triggers & breakthrough dings.
     * Track 2 (Emotional Core / Romance): Strictly **-16 dBFS to -18 dBFS under dialogue** (tender gratitude, relief).
     * Track 3 (Underdog Resolve): Leveled at **-14 dBFS to -16 dBFS** (unbothered swagger walk / quiet confidence).
     * Track 4 (Suspicion & Antagonist Intrigue): Ducked to **-20 dBFS** during dialogue, swelling to **-10 dBFS to -12 dBFS** on cliffhangers (villain entrances & staredowns).
   - Notch filter: 1.2 kHz parametric notch scoop (`equalizer=f=1200:t=q:w=1.5:g=-3.5`) across all BGM for crisp voice intelligibility.
3. STRICTLY NO SFX (dialogue primacy). Voice mastered to -14 to -15 LUFS / -1.5 True Peak with 80Hz highpass and +2.5dB at 2.8kHz.
4. Cinematic color grading (filmic S-curve, lifted deep blacks, teal shadows, warm midtones).
5. Cut wrong parts: Pre-trim AI reference flash frames (0.04s–0.17s) with tail cloned padding; mute off-screen prompt vocal leaks.
6. Motivated transitions: Hard cuts for continuous action/dialogue; dip to black (0.4s–0.5s) for location/act shifts; 1.5s freeze-frame hold on cliffhangers.
7. Subtitles: Static, elegant, 46pt Liberation Sans Bold at MarginV=280 lower-third safe zone, burned + .ass/.srt sidecars.
8. Multi-episode compilation: Compile all episodes into 1 unified feature film with MP4 chapter markers.
9. Deliverables: Master `<slug>-final.mp4` + Telegram mobile stream `<slug>-final-45mb.mp4` tagged with `MEDIA:/home/john/Documents/hermieditor/outbox/<slug>-final-45mb.mp4`.

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

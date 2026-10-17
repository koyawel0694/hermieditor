# HermiEditor: Hermes Agent Operational Instructions

HermiEditor is an autonomous video editing suite designed specifically for Hermes Agent. It produces high-retention short-form videos (Reels, TikTok, YouTube Shorts) and vertical episodic mini-dramas from raw footage and voiceover.

## Workspace Layout

- `skills/hermieditor/SKILL.md`: The Hermes skill definition. Auto-linked to `~/.hermes/skills/media/hermieditor/` by `setup.mjs`.
- `inbox/`: Working folder where raw video footage and voiceover tracks are placed (`inbox/<slug>/`).
- `outbox/`: Deliverables destination (`<slug>-final.mp4`, `<slug>-under20mb.mp4`, `<slug>-hq-48mb.mp4`, `.ass`, `.srt`).
- `my-sounds/`: Curated 69-sound library (`mini-drama/`, `explainer/`, `us-niche/`), indexed in `catalog.json`.
- `templates/`: Boilerplate scripts for captioning (`generate_captions.py`), audio mastering (`build_audio.py`), and video compositing (`render_pipeline.py`).
- `tools/`: Free word-level transcription via Groq or local faster-whisper.
- `kit/`: Herk Edit Kit engine (sparse-checked-out for HyperFrames and motion cards).

## How Hermes Operates HermiEditor

When the user asks you to edit a video:
1. **Identify the project folder** in `inbox/<slug>`.
2. **Transcribe voiceover**: Run `node tools/transcribe.mjs <audio_path>`.
3. **Inspect clips and timeline**:
   - Check duration of audio and clips with `ffprobe`.
   - Check first 1.5s for AI video reference image flash artifacts (`ffmpeg -ss 0.0 -t 1.5 -i clip.mp4 -filter_complex "select='gt(scene,0.25)',metadata=print" -f null -`).
4. **Generate Dynamic Captions**:
   - Create word-by-word active tracking `.ass` and `.srt` with semantic phrase chunking in `Liberation Sans Bold`, white text, 5px dark outline/shadow, and vibrant gold `#FFD700` active word pop.
   - Safe zone: `MarginV=480` (Alignment=2) in 1080x1920.
5. **Master Audio**:
   - Vocal: Highpass 80Hz, +2.5dB boost at 2.8kHz, loudnorm -14 LUFS.
   - BGM: Volume 0.07, 1.2kHz scoop (-6dB), lowpass 7500Hz, sensitive sidechain ducking.
   - SFX: Synchronize tactical cues from `my-sounds/` with gain -3 to -5 dB.
6. **Composite & Export Deliverables**:
   - Master Final (1080x1920 @ 30fps).
   - Inline mobile preview (`<slug>-under20mb.mp4`).
   - HQ master (`<slug>-hq-48mb.mp4`).
   - Accompanying `.ass` and `.srt` files in both `inbox/` and `outbox/`.

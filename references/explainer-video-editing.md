# Explainer & Documentary Video Editing Reference

This reference covers established workflows and editorial rules for editing educational, scientific, historical, and documentary explainer videos in HermiEditor.

## 1. Clean Visual Canvas Rule

- **High-Value Animation & Dioramas**: For stop-motion, papercraft, claymation, and 3D visual sequences, **DO NOT add motion graphics cards, pop-up windows, or UI overlays**.
- **Reasoning**: The handcrafted physical or 3D art is the primary visual hook and retention driver. Overlays clutter the frame, block central actions, and degrade visual production value.
- **Where to Use Graphics**: Reserve motion graphics cards, GSAP spring pop-ups, and comparison tables strictly for personal vlogs, talking-head videos, or affiliate product showcases.

## 2. Still Image / Thumbnail Hold Rule

- In explainer videos containing an accompanying still image or thumbnail (e.g., `.jpg` or `.png` reference diorama):
  - **Position**: Place the image at the **very END** of the video.
  - **Duration**: Hold for **at least 0.1 to 0.2 seconds** (e.g., 6 frames at 30 fps = 0.20s).
  - **Reasoning**: Provides a clean visual anchor and thumbnail frame for social platforms (TikTok, Reels, Shorts) at completion without interrupting narrative flow at the intro.

## 3. Spoken Dialogue & Voiceover Primacy

- Spoken voiceover is always the primary foreground audio element.
- Mastered to **-14 LUFS** (`loudnorm=I=-14:LRA=7:TP=-1.5`) with highpass filtering at 80 Hz and +2.5 dB presence boost at 2.8 kHz.
- Ambient clip foley audio should be leveled and mixed beneath the voiceover bed.
- **CRITICAL FFmpeg Stream Mapping Rule**:
  - When muxing base video with master audio in FFmpeg, **ALWAYS explicitly specify `-map 0:v -map 1:a`**.
  - Without explicit mapping, FFmpeg defaults to stream `0:a` from the base video, which completely omits the voiceover!

## 4. Single Video Delivery Standard

- Produce **ONLY 1 video deliverable** by default:
  - `<slug>-final.mp4` (1080x1920, CRF 17-19, 192k AAC stereo, `+faststart`).
- Do NOT generate redundant multi-tier files (`<slug>-under20mb.mp4`, `<slug>-hq-48mb.mp4`, or `<slug>-v1.mp4`) unless explicitly requested by the user.
- Accompanying subtitle files: `<slug>.ass` (active gold word pop) and `<slug>.srt` saved in both `inbox/` and `outbox/`.

## 5. Local Transcription Fallback

- When Groq Whisper API keys are unavailable, use local `faster-whisper` on CPU/GPU:
  - Environment: `/home/john/.venvs/whisper2/bin/python`
  - Model: `faster-whisper-medium` or `faster-whisper-base` cached in `~/.cache/huggingface/hub/`
  - Output: Word-level timestamps (`text`, `start`, `end`) formatted into JSON for subtitle chunking and timing.

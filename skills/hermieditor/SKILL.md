---
name: hermieditor
description: "Use when editing videos, shorts, or reels with HermiEditor."
version: 1.1.0
author: John & Nessan
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [video-editing, short-form, ffmpeg, subtitles, sfx, reels, tiktok, hermieditor]
    related_skills: [deepclip, deepcut, deepcaption]
---

# HermiEditor: Autonomous Video Editor for Hermes Agent

HermiEditor turns raw footage, talking-head recordings, product clips, and AI-generated video sequences into polished short-form (Reels/TikTok/Shorts) or episodic mini-drama videos with word-level captions, jump cuts, mistake removal, dynamic hooks, B-roll, sidechain-ducked BGM, and sound effects using local HyperFrames rendering and FFmpeg compositing.

Workspace root: `/home/john/Documents/hermieditor` (repo: `https://github.com/koyawel0694/hermieditor.git`, fallback: `/home/john/Documents/free247editor`)

## Directory Structure

- `inbox/`: Raw clips and voiceover dropped here (`inbox/<project_slug>/`).
- `outbox/`: Final renders (`<slug>-final.mp4`, `.ass`, `.srt`).
- `my-style.md`: Lasting style preferences (dimensions, pacing, framing, text positioning).
- `my-rules.md`: Cumulative rules learned from editorial revision notes.
- `my-sounds/`: Curated 69-sound library (`mini-drama/`, `explainer/`, `us-niche/`), indexed in `catalog.json`.
- `kit/`: The Herk Edit Kit engine and video projects (`kit/video-projects/<slug>-YYYY-MM-DD/`).
- `references/`:
  - `references/motion-cards-and-telegram-delivery.md`: Motion graphics, HyperFrames mini PC rendering, sound design, Telegram limits.
  - `references/explainer-video-editing.md`: Explainer and documentary assembly, end-image hold rules, clean canvas, and transcription fallbacks.
- `tools/transcribe.mjs`: Word-level transcription tool (Groq Whisper API or local `faster-whisper`).
- `references/`:
  - `motion-cards-and-telegram-delivery.md`: Motion graphics, procedural SFX generation, and under-20MB Telegram delivery encoding.
  - `mini-drama-series-editing.md`: Assembly, pacing, simple subtitle styling, sidechain-ducked BGM score integration, and lossless multi-episode compilation.
  - `sound-design-and-sfx-library.md`: Sound effects library organization, FFmpeg stream channel mapping, and volume ducking curves.

## Sound Design & SFX Sourcing Discipline

- **Strict Priority on Curated `my-sounds/` Library**:
  - Spoken voiceover must ALWAYS be accompanied by real, curated sound files directly from `my-sounds/` (`my-sounds/explainer/`, `my-sounds/mini-drama/`, `my-sounds/us-niche/`), indexed in `catalog.json`.
  - Strictly avoid synthesizing artificial procedural tones, clicks, or beeps with scipy/numpy when real recordings exist in the curated library. Procedural audio is strictly an emergency fallback.
- **Affiliate & Explainer SFX Mapping (`my-sounds/explainer/`)**:
  - Solution / Brand Reveal: `pop-clean.mp3` (gain -3.0 dB) on "Ito ang katapat niyan" / brand reveals.
  - Metric / Spec Callout: `ding-bell-subtle.mp3` (gain -3.0 dB) on numbers, thickness, or key specs (e.g. "3mm").
  - Physical Action / Scratch Resistance: `whoosh-transition-fast.mp3` (gain -4.0 dB) on physical friction or demonstrations.
  - Feature Proof & Payoff: `ding-correct-gameshow.mp3` (gain -5.0 dB) on "100% waterproof" / proof claims.
  - Bonus / Inclusions: `ding-bell-subtle.mp3` (gain -4.0 dB) on "Libre pa ang pandikit".
  - Checkout CTA ("Yellow Basket"): `cash-register-cha-ching.mp3` (gain 0.0 dB) timed exactly on "Pindutin mo na ang yellow basket".

## Production Modes

### Mode A: Educational / Explainer Shorts
- **Pacing**: Fast-paced, eliminate breath pauses > 0.35s, jump cuts, subtle punch-in scale zooms (5-8% scale) on narrative topic shifts.
- **Subtitles**: Dynamic word-by-word active tracking captions in bold sans-serif (`Liberation Sans`), bold white with dark drop shadow/stroke, vibrant gold (`#FFD700` / `&H0000D7FF`) or electric cyan active highlight, positioned in upper-middle third safe zone (`MarginV=480`).
- **Visuals & Overlays Discipline**: Default to clean visual footage + subtitles only. Do NOT add unsolicited motion graphic cards or HUD badges unless explicitly requested by the user. Let the footage breathe.
- **Audio & SFX Discipline**: Spoken voiceover is always front and center (normalized to -14 LUFS, 80Hz highpass, +2.5dB boost at 2.8kHz). Keep initial audio clean with voiceover only; add SFX on explicit request or from `my-sounds/`.
- **Duration Sync**: Enforce hard duration sync by passing `-t <audio_duration>` directly to ffmpeg or post-trimming (`ffmpeg -y -ss 0.0 -t <audio_duration> -i composite.mp4 -c copy final_trimmed.mp4`).

### Mode B: Mini Drama Series (Vertical Serye / Fiction)
- **Subtitles**:
  - Simple, static, elegant subtitles only — strictly NO word-by-word karaoke highlights or animated bouncing words.
  - Typeface: Clean sans-serif (`Liberation Sans` or `DejaVu Sans`), 46-48pt, bold.
  - Color & Contrast: Pure white (`&H00FFFFFF`) with 2.8–3.0px dark outline stroke and 1.2px shadow for 100% legibility against all backgrounds.
  - Safe Zone: Lower-third center (`MarginV=260–280` on 1080x1920) to stay safely above TikTok/Reels UI overlays without blocking characters' chests or hands.
  - Text & Timing: Aligned exactly to spoken dialogue in Tagalog/Filipino or English.
- **Transitions**:
  - Smooth cinematic transitions: 0.5s gentle crossfade (`xfade=transition=fade:duration=0.5:offset=...`) paired with 0.5s audio cross-dissolve (`acrossfade=d=0.5:c1=tri:c2=tri`).
  - Smooth 0.5s fade-in from black at video intro.
  - Cliffhanger ending: 1.5s freeze-frame hold on the final questioning/tearful close-up, followed by a 1.2–1.3s fade-to-black.
- **Dialogue Timing & Reaction Breathing Room**:
  - When speech in clip A ends near the boundary or clip B starts near 0.0s, pad clip A with a 0.5s reaction hold (`tpad=stop_mode=clone:stop_duration=0.5` and `apad=pad_dur=0.5`) so the crossfade occurs in the pause, preventing overlapping speech.
- **Sound Design & SFX**:
  - Dialogue Primacy & Mastering: Boost voice by 1.35x (`volume=1.35`) with highpass at 80Hz and +2.5dB vocal presence boost at 2.8kHz (`equalizer=f=2800:t=q:w=1.0:g=2.5`).
  - Environmental Bed: Continuous background tone (interior rain, room tone, outdoor street).
  - Tactical Drama SFX: Subtle brass shop door chimes, somatic heartbeat flutter pulses, delicate tactile shimmer on physical brushes, and emotional tension swells/impacts on cliffhangers.
  - BGM Score: Acoustic or ambient instrumental bed leveled to `volume=0.07` with a 6dB scoop at 1200Hz.
  - Sensitive Sidechain Ducking: Always wire sensitive sidechain compression (`threshold=0.02:ratio=3.5:attack=50:release=450`) so music instantly ducks an additional 6–10 dB the moment any character speaks.

### Mode C: Affiliate & Product Commercial Shorts (TikTok / Reels / Shopee / Lazada)
- **Pacing & 5-Step Narrative Arc**:
  1. Hook (0–3s): Problem, craving, or curiosity stop-scroll.
  2. Product Reveal & Scoop (3–7s): First physical action showing product texture/packaging/branding.
  3. Value & Proof (7–14s): Proof of quality, thickness, durability, or authenticity.
  4. Preparation / Serving / Testing (14–20s): Stacking, testing, wiping, or installation demonstration.
  5. Climax & CTA (20–27s): High-satisfaction payoff & call to action ("Pindutin ang yellow basket").
  - Cut strictly on spoken cadence and phrase boundaries so visual actions align directly with spoken descriptions.
- **Captions & Safe Zones**:
  - Dynamic active tracking captions in `Liberation Sans Bold`, white text with 5px dark outline and shadow.
  - Vibrant gold active highlight (`#FFD700` / `&H0000D7FF`) with a 10% scale pop (`\fscx110\fscy110`) as each word is spoken.
  - Safe Zone: Set `MarginV=480` (Alignment=2) in 1080x1920. Captions sit ~25% above bottom edge, staying clear of TikTok/Reels shopping cart buttons and audio tickers.
  - Semantic Phrase Chunking: Group words by natural Tagalog semantic units (e.g. "SA PETSA DE PELIGRO", "PINDUTIN MO NA ANG YELLOW BASKET").
- **Transcription Semantic Verification (Colloquial Tagalog/Taglish)**:
  - Whisper models frequently transcribe rapid colloquial Tagalog phonetically with errors (e.g., "Pindutin" -> "Pintutin", "naka-sale pa" -> "nakasilpa", "petsa" -> "pecha").
  - Always review transcript words and correct typos before embedding into `.ass` or `.srt` files.
- **Tactical Affiliate SFX**:
  - Checkout CTA Chime: Timed exactly on the call-to-action (`cash-register-cha-ching.mp3` from `my-sounds/explainer/`).
  - Accent / Ding SFX: Clean bell ding (`ding-bell-subtle.mp3`) on product reveals, key test moments, and payoff moments.
  - Background Music: Acoustic lifestyle track at `volume=0.07` with a 6dB notch at 1200Hz (`equalizer=f=1200:t=q:w=1.2:g=-6,lowpass=f=7500`) and sensitive sidechain ducking against voiceover.

## AI Video Generation Artifacts & Pitfalls

### Google Omni / Flow Character Reference Image Flaw
- Video generation models frequently flash the static character reference image for the first 8–15 frames (0.3s to 0.65s).
- Run scene change detection on the first 1.5s:
  ```bash
  ffmpeg -ss 0.0 -t 1.5 -i clip.mp4 -filter_complex "select='gt(scene,0.25)',metadata=print" -f null -
  ```
- Pre-trim the raw clip cleanly from the exact scene cut timestamp if detected:
  ```bash
  ffmpeg -y -ss <pts_time> -i raw_clip.mp4 -c:v libx264 -crf 18 -preset fast -c:a aac -b:a 192k trimmed_clip.mp4
  ```

## Critical Production & Delivery Rules

- **Hard Duration Sync (Audio/Video Alignment)**: Always enforce exact target duration explicitly: pass `-t <target_seconds>` on the compositing command, or run a hard trim copy pass:
  ```bash
  ffmpeg -y -ss 0.0 -t <target_seconds> -i composite.mp4 -c copy final_trimmed.mp4
  ```
- **Special Unicode Characters in Filenames**: Files frequently contain ellipses (`…` U+2026), brackets, or symbols. Always quote variables and use glob matching to prevent silent script failures.
- **Single Video Delivery (Final Master Only)**:
  - Generate ONLY 1 video file by default: `<slug>-final.mp4` (1080x1920, CRF 17-19, 192k AAC stereo, `+faststart`).
  - Do NOT generate redundant multi-tier files (`<slug>-under20mb.mp4`, `<slug>-hq-48mb.mp4`, or `<slug>-v1.mp4`) unless explicitly requested by the user.
- **Explicit Stream Mapping**:
  - When multiplexing base video and master audio, ALWAYS explicitly map video from `0:v` and mixed audio from `1:a` (`-map 0:v -map 1:a`). Omitting `-map` causes FFmpeg to pick `0:a` (the camera/foley track) and completely drop the voiceover track!
- **Document File Delivery**: When delivery as uncompressed file is requested, dispatch directly via Telegram Bot API `sendDocument`.
- **Standalone Subtitle Deliverables**: Always produce and deliver accompanying `.srt` and `.ass` files in both `inbox/` and `outbox/`.

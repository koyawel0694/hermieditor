# HermiEditor 🎬

> **Autonomous AI Video Editor for Hermes Agent**  
> Turn raw clips, voiceover recordings, and AI-generated footage into polished vertical shorts (Reels, TikTok, Shorts) and mini-drama series with dynamic word-by-word active tracking captions, sidechain-ducked BGM, and curated sound design.

---

## Highlights

- **Native Hermes Skill**: Built to be driven autonomously by [Hermes Agent](https://hermes-agent.nousresearch.com/docs). Simply drop your assets into `inbox/` and prompt Hermes: *"edit this affiliate video in inbox/my-project"*.
- **Dynamic Word-by-Word Active Captions**: Automatically generates high-retention `.ass` and `.srt` subtitles with vibrant gold highlights, subtle scale pop, and safe-zone positioning that never overlaps TikTok/Reels UI buttons or shopping carts.
- **Mastered Voiceover & Sensitive Sidechain Ducking**: Spoken dialogue is always front-and-center (80Hz highpass, +2.5dB vocal presence boost at 2.8kHz, normalized to -14 LUFS). Background music instantly ducks 6–10 dB whenever a character speaks.
- **Curated 69-Sound SFX Library**: Includes pre-indexed sound effects for explainers, dramatic mini-series, and comedic accents (`my-sounds/`), indexed in `catalog.json`.
- **Artifact Cleansing**: Automatically detects and trims AI video generator glitches (such as the Google Flow / Omni 1.1 Flash 0.3s character reference image flash).
- **Multi-Tier Deliverables**:
  - `*-final.mp4`: Master 1080x1920 @ 30fps high fidelity.
  - `*-under20mb.mp4`: Encoded for seamless inline streaming and mobile preview.
  - `*-hq-48mb.mp4`: High-bitrate master strictly under Telegram's 50MB bot upload limit.
  - `*.ass` & `*.srt`: Standalone subtitles exported to both `inbox/` and `outbox/`.

---

## ⚡ Quick Start

### 1. Prerequisites

- **FFmpeg & FFprobe**: `sudo apt install ffmpeg` / `brew install ffmpeg` / `winget install Gyan.FFmpeg`
- **Node.js 18+**: `https://nodejs.org`
- **Python 3.10+**: `pip install numpy scipy faster-whisper`
- **Git**

### 2. Clone & Run Setup

```bash
git clone https://github.com/koyawel0694/hermieditor.git
cd hermieditor
./setup.sh
```

The setup script will:
1. Verify system dependencies (FFmpeg, Node, Python, Git).
2. Install the Herk Edit Kit engine into `kit/`.
3. Auto-link the `hermieditor` skill into `~/.hermes/skills/media/hermieditor/` so Hermes Agent immediately indexes it.
4. Scaffold `inbox/` and `outbox/`.

### 3. (Optional) Fast Transcription API

HermiEditor includes local transcription via `faster-whisper`. For ultra-fast cloud transcription:
1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Add your free Groq Whisper API key from [console.groq.com](https://console.groq.com):
   ```env
   GROQ_API_KEY=gsk_your_groq_api_key
   ```

---

## 🎯 How to Use with Hermes

1. **Drop your raw footage and audio** into an inbox folder:
   ```text
   inbox/my-product/
     ├── Clip_1.mp4
     ├── Clip_2.mp4
     ├── Clip_3.mp4
     └── voiceover.wav
   ```

2. **In your Hermes session, simply prompt**:
   > *"Edit this affiliate video in inbox/my-product"*  
   > or  
   > *"Edit this mini-drama episode in inbox/ep1"*

Hermes will automatically:
- Transcribe the audio at the word level.
- Sequence clips according to narrative pacing (Hook → Product Reveal → Proof → Demonstration → CTA).
- Generate dynamic active-highlight ASS/SRT captions.
- Mix BGM with sidechain ducking and place tactical SFX from `my-sounds/`.
- Composite and export deliverables into `outbox/`.

---

## 📁 Repository Structure

```text
hermieditor/
├── skills/
│   └── hermieditor/          # The Hermes Skill definition & reference guides
│       ├── SKILL.md
│       └── references/       # Mini-drama, motion cards, and SFX guides
├── my-sounds/                # Curated 69-sound SFX library (explainer, mini-drama, us-niche)
│   ├── catalog.json
│   ├── explainer/
│   ├── mini-drama/
│   └── us-niche/
├── tools/                    # Transcription tools (Groq + faster-whisper)
│   ├── transcribe.mjs
│   └── transcribe_local.py
├── templates/                # Production pipeline templates
│   ├── generate_captions.py
│   ├── build_audio.py
│   └── render_pipeline.py
├── inbox/                    # Drop raw footage here
├── outbox/                   # Finished videos and subtitles land here
├── my-style.md               # User style preferences
├── my-rules.md               # Cumulative revision rules
├── setup.sh                  # Linux/macOS setup wrapper
├── setup.mjs                 # Cross-platform installer & skill linker
├── HERMES.md                 # Agent guidance for Hermes
└── package.json
```

---

## 🎬 Production Modes

### Mode A: Educational / Explainer Shorts
- Fast-paced, eliminating dead air > 0.35s.
- Dynamic word-by-word gold highlight captions.
- Subtle Ken Burns push-in zoom cuts (5-8% scale) resetting visual attention every 3–5 seconds.

### Mode B: Mini-Drama Series (Vertical Serye / Fiction)
- Gentle 0.5s visual crossfades (`xfade=fade:0.5`) paired with audio cross-dissolves.
- Elegant, static subtitles in lower-third safe zone (`MarginV=260–280`).
- Dialogue reaction breathing room (0.5s hold pads on clip boundaries).
- Continuous environmental ambient tone + cinematic cliffhanger freeze holds.

### Mode C: Affiliate & Product Commercial Shorts (TikTok / Reels / Shopee / Lazada)
- 5-step commercial narrative arc: Problem Hook → Product Reveal → Value Proof → Usage/Installation → CTA Payoff.
- Dynamic active tracking captions in `Liberation Sans Bold` with gold active word pop (`\fscx110\fscy110`).
- Safe zone set at `MarginV=480` to stay clear of TikTok shopping cart buttons and audio tickers.
- Tactical SFX: Cash register checkout chime (`cash-register-cha-ching.mp3`) on CTA and subtle bell dings on spec reveals.

---

## 📄 License

MIT License. Created by John & Nessan.

# Video Editing Rules

Persistent editorial rules learned from John's feedback and notes during revisions.

## Mini Drama Series Rules (e.g. Pintig ng Puso / SERYE)
- **Subtitles**:
  - Simple, static, elegant subtitles only — NO word-by-word karaoke highlights or animated bouncing words.
  - Typeface: Clean sans-serif (Liberation Sans / DejaVu Sans), 46-48pt, bold.
  - Color & Contrast: Crisp solid white text (`&H00FFFFFF`) with a 2.8–3.0px dark outline stroke and 1.2px drop shadow for 100% legibility against both dark clothing and bright daylight backgrounds.
  - Safe Zone: Centered lower-third with ~260–280px vertical margin from bottom to stay well above TikTok / Reels / Shorts descriptions, account handles, and audio ticker UI overlays without blocking characters' chests or faces.
  - Language: Strict synchronization with Filipino / Tagalog dialogue and voiceover lines.
- **Transitions**:
  - Only apply smooth visual transitions: 0.5s gentle crossfade (`xfade=transition=fade:duration=0.5`) between consecutive clips, paired with 0.5s audio cross-dissolve (`acrossfade=d=0.5`).
  - Smooth 0.5s fade-in from black on Clip 1, and 1.2–1.5s freeze-frame hold followed by fade-to-black on the final cliffhanger frame.
- **Sound Design & SFX**:
  - Balanced dialogue mastering: Dialogue leveled to ~ -24 dBFS RMS, peak -1.4 dBFS.
  - Contextual ambient world sound: Continuous environmental bed (interior rain, daylight room tone, street atmosphere).
  - Tactical drama SFX: Subtle brass shop door chimes, somatic heartbeat flutter pulses (phantom memory / chest scar reactions), delicate tactile shimmer on physical brushes, and emotional tension swells/impacts on cliffhangers.
  - Character Voice Primacy & Clarity: Spoken dialogue is ALWAYS the dominant foreground element. Voices must be leveled to ~ -18 to -22 dBFS RMS with a highpass filter at 80Hz and a +2.5dB vocal presence boost at 2.8kHz to guarantee every Filipino/Tagalog word and whisper is 100% intelligible.
  - BGM Music Leveling & Vocal Corridor: AI-generated scores (Suno/Udio) are mastered loud (~ -14 dBFS) and MUST be dramatically attenuated to `volume=0.07` to `0.08` (~ -38 to -42 dBFS RMS, at least 18–22 dB BELOW dialogue). A 6dB mid-frequency scoop (`equalizer=f=1200:t=q:w=1.2:g=-6`) MUST be applied to carve out the vocal formant corridor so guitars/pianos never mask speech.
  - Aggressive Dialogue Sidechain Ducking: Always wire sensitive sidechain compression (`threshold=0.02:ratio=3.5:attack=50:release=450`) to duck the score an additional 6–10 dB the moment any character speaks, even on quiet whispers. The score only gently breathes during scene transitions and cliffhanger holds.
  - Tactical drama SFX: Sourced from `my-sounds/mini-drama/`. Subtle brass shop door chimes (`shop-door-bell.mp3`), somatic heartbeat flutter pulses (`heartbeat-pulse-loop.mp3` or `heartbeat-stress.mp3`), delicate tactile shimmer on memory flashbacks (`dream-harp-flashback.mp3` / `wind-chimes-memory.mp3`), and emotional tension swells/impacts on cliffhangers (`cinematic-braam.mp3`, `cinematic-sub-boom.mp3`).
  - SFX Leveling: Never mix SFX at full 0 dB. Dialogue is always primary. UI pops/clicks: volume=0.20-0.25; transitions: volume=0.25-0.30; drama braams/booms: volume=0.30-0.35.
- **Motion Graphics & Pop-up Windows**:
  - Strictly avoid static flat PNG cards with linear FFmpeg opacity fades. Use native HyperFrames + GSAP spring animations (`back.out(1.75)`) with macOS dark glassmorphic window chrome (traffic light controls, code/tab header, line-by-line staggered reveals). Reference template: `kit/style-templates/explainer-popup-window/`.
  - In short-form explainers, coordinate camera stage motion: subtly zoom out / pull back (scale: 0.95) and dim the host video when the pop-up window springs in.
- **Delivery Outputs**:
  - Master Final: Full CRF 19 / 192k AAC 1080x1920.
  - Telegram HQ Master: `<slug>-hq-48mb.mp4` (~43–48 MB, under 50 MB bot API limit).
  - Telegram Mobile Inline Preview: `<slug>-under20mb.mp4` (~17–18 MB for auto-streaming).
  - Standalone Subtitles: Accompanying `.srt` and `.ass` files saved in both inbox and outbox.

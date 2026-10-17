# Mini Drama Series Video Editing & Assembly

Reference guide for editing vertical mini-drama series (TikTok/Reels/Shorts/Serye, e.g. Pintig ng Puso) with free247editor.

## 1. Editorial Rules & Constraints
- **Workflow Order & Existing Finals Check**:
  - Before assembling clips from scratch, check if rendered episode finals already exist in `inbox/<series>/` or `outbox/` (`<slug>-epX-final.mp4`). If the user asks to compile episodes or add BGM scores, build directly from the existing episode finals rather than re-cutting raw shot clips.
- **Subtitles**:
  - Simple, static, elegant subtitles only — strictly NO word-by-word karaoke highlights or animated bouncing words.
  - Font: Clean sans-serif (`Liberation Sans` or `DejaVu Sans`), 46–48pt, bold.
  - Colors: Pure white (`&H00FFFFFF`) with 2.8–3.0px dark outline stroke and 1.2px shadow for contrast against both dark outfits and bright sunlight.
  - Positioning: Lower-third center (`MarginV=280` on 1080x1920) to stay safely above platform UI overlays (descriptions, sound titles, interaction buttons) without covering actors' chests or hands.
- **Transitions**:
  - Only apply smooth cinematic transitions: 0.5s gentle crossfade (`xfade=transition=fade:duration=0.5:offset=...`) paired with 0.5s audio cross-dissolve (`acrossfade=d=0.5:c1=tri:c2=tri`).
  - Add 0.5s fade-in from black at video intro.
  - Cliffhanger ending: 1.5s freeze-frame hold on the final questioning/tearful close-up, followed by a 1.2–1.3s fade-to-black.
- **Dialogue Timing & Reaction Breathing Room**:
  - Pitfall: In AI-generated clips (e.g. Google Flow / Omni 1.1 Flash), dialogue often starts immediately at 0.0s or continues up to 9.8s at the clip boundary.
  - Fix: When speech in clip A ends near the boundary or clip B starts near 0.0s, pad clip A with a 0.5s reaction hold (`tpad=stop_mode=clone:stop_duration=0.5` and `apad=pad_dur=0.5`) so the crossfade occurs in the pause, preventing overlapping speech.

## 2. Audio & Sound Design
- **Dialogue Mastering**: Level dialogue to ~ -24 dBFS RMS, peak -1.4 dBFS.
- **Contextual Environmental Ambiance**:
  - Continuous ambient bed: soft indoor rain on window glass, daytime shop atmosphere, or outdoor storm.
- **Tactical Drama SFX**:
  - Somatic heartbeat flutter: Double/triple-thump low-frequency pulse (52–68Hz) with exponential damping for transplant scar / phantom memory / arrhythmia reactions.
  - Flashback shimmer: High-harmonic bell shimmer (1318Hz, 1760Hz, 2637Hz) marking memory transitions.
  - Tactile foley: Latch clicks, rain tapping on glass, kraft paper rustle.
  - Cliffhanger swell: Bowed string tension swell in D-minor / A-minor + deep resonant acoustic sub-bass drop into silence.
- **Drama Score & Dynamic Sidechain Ducking**:
  - Spoken dialogue is ALWAYS the primary foreground element. Boost `vox` by 1.35x (`volume=1.35`) with highpass at 80Hz and a +2.5dB vocal presence boost at 2.8kHz (`equalizer=f=2800:t=q:w=1.0:g=2.5`).
  - Raw BGM tracks (e.g. Suno/Udio normalized to ~ -14 dBFS) MUST be scaled down to `volume=0.07` (~ -38 to -42 dBFS RMS, at least 18–22 dB below dialogue) with a 6dB vocal corridor scoop at 1200Hz (`equalizer=f=1200:t=q:w=1.2:g=-6`) and `lowpass=f=7500` to prevent competing with vocal sibilance.
  - Wire sensitive sidechain compression triggered by speech with a low threshold so even soft whispers trigger ducking:
    `sidechaincompress=threshold=0.02:ratio=3.5:attack=50:release=450`.
  - Always use `normalize=0` on `amix` to prevent halving speech volume:
    `[0:a]highpass=f=80,equalizer=f=2800:t=q:w=1.0:g=2.5,equalizer=f=400:t=q:w=1.5:g=-1.5,volume=1.35,aresample=48000,asplit=2[vox_clean][vox_sc];[1:a]volume=0.07,equalizer=f=1200:t=q:w=1.2:g=-6,lowpass=f=7500,aresample=48000[bgm_in];[bgm_in][vox_sc]sidechaincompress=threshold=0.02:ratio=3.5:attack=50:release=450[bgm_ducked];[vox_clean][bgm_ducked]amix=inputs=2:duration=first:normalize=0,afade=t=out:st=<st>:d=<dur>,alimiter=limit=0.95[afinal]`
  - Use `-c:v copy` when re-scoring existing episode finals — this avoids generational video re-encoding loss and finishes in under 2 seconds.

## 3. Multi-Episode Compilation / Marathon Feature
- When compiling N rendered episodes into an omnibus feature:
  - Generate a concat list file with `file '<path>'` entries.
  - Run stream-copy concatenation:
    `ffmpeg -y -f concat -safe 0 -i list.txt -c copy -movflags +faststart <slug>-episodes-1-N-compilation-master.mp4`
  - Because all episodes share 1080x1920 24fps h264 and 48kHz AAC, stream copy joins them losslessly and instantaneously.
  - Episodic pauses: The natural 1.2–1.3s fade-to-black cliffhanger tail of episode N followed by the 0.5s fade-in of episode N+1 creates an organic episodic chapter transition.

## 4. Multi-Clip FFmpeg Assembly Pipeline Pattern
```bash
# Example 9-clip vertical drama pipeline:
# 1. Normalize clips: fps=24, settb=AVTB, audio resample 48000
# 2. Chain xfade and acrossfade at calculated offsets
# 3. Burn simple subtitles (.ass)
# 4. Mix speech audio with sfx/score bed (amix with sidechain ducking)
# 5. Export master, HQ (<50MB), and preview (<20MB)
```

## 5. Render Scripts & Process Execution Pitfalls
- **FFmpeg Subprocess Output**: Always suppress or redirect FFmpeg progress stderr (`stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL`) when running batch renders in Python or shell scripts. Uncaptured stderr spews thousands of frame lines, overflowing agent buffers and triggering command timeouts.
- **Compilation Size Target**: For 4–5 minute multi-episode compilations, Telegram's 50MB mobile upload limit requires a dedicated mobile encode:
  `-c:v libx264 -preset fast -b:v 1350k -maxrate 1600k -bufsize 3000k -c:a aac -b:a 128k -pix_fmt yuv420p -movflags +faststart` (~46–48MB for ~4.5 minutes).

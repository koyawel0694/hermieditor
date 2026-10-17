# Sound Design & SFX Library Reference

Comprehensive guide for sourcing, inspecting, and mixing sound effects in `free247editor`.

## 1. Library Organization (`my-sounds/`)

The workspace library at `/home/john/Documents/free247editor/my-sounds/` is categorized into 3 production tiers, indexed in `catalog.json` and documented in `README.md`:

### A. Mini Drama Series (`my-sounds/mini-drama/`)
Tailored for Mode B cinematic vertical series (*Pintig ng Puso*, *SERYE*):
- **Somatic & Arrhythmia**: `heartbeat-pulse-loop.mp3` (0.72s repeating lub-dub), `heartbeat-stress.mp3` (6.90s rapid panic/scar reaction).
- **Tension & Suspense**: `suspense-tension-riser.mp3` (10.08s rising string swell), `sudden-suspense-hit.mp3` (1.37s sharp sting).
- **Cliffhangers & Impacts**: `cinematic-braam.mp3` (3.04s massive brass hit), `cinematic-sub-boom.mp3` (5.38s sub-bass boom), `cinematic-orchestral-hit.mp3` (4.35s full chord), `cinematic-bass-drop.mp3` (3.31s pitch dive).
- **Emotional Score**: `sad-violin-solo.mp3` (6.01s mournful violin), `dramatic-violin-climax.mp3` (8.33s dramatic crescendo).
- **Tactile Foley**: `dream-harp-flashback.mp3` (5.50s harp glissando), `wind-chimes-memory.mp3` (4.08s chime shimmer), `shop-door-bell.mp3` (3.06s brass counter bell), `apartment-doorbell.mp3` (2.69s ding-dong), `realistic-door-knocking.mp3` (9.14s rapid wooden knocks), `heavy-door-slam.mp3` (1.83s exit slam), `broken-glass-shatter.mp3` (1.36s), `face-slap.mp3` (1.59s), `punch-impact.mp3` (1.53s), `shocked-gasp.mp3` (1.42s), `thunder-crack.mp3` (3.47s), `thunder-rumble.mp3` (7.13s).

### B. Video Explainer (`my-sounds/explainer/`)
Tailored for Mode A educational, tech, financial, and affiliate Shorts/Reels:
- **Kinetic Text & Graphic Reveals**: `pop-clean.mp3` (0.29s crisp UI pop), `bubble-pop.mp3` (0.26s organic pop), `whoosh-transition-fast.mp3` (0.98s punch-in swish), `whoosh-transition-cinematic.mp3` (2.16s slide wipe), `cinematic-thud-metric.mp3` (2.71s deep impact for major stats).
- **Tech & Desktop Foley**: `mouse-click-clean.mp3` (1.44s single click), `mouse-click-double.mp3` (3.07s navigation), `keyboard-typing-fast.mp3` (10.06s typing bed), `camera-shutter-flash.mp3` (2.02s screenshot proof), `camera-snap-fast.mp3` (0.88s DSLR snap).
- **Paper & Document**: `page-turn-flip.mp3` (1.20s citation/page flip), `paper-crumple.mp3` (7.66s contract/bad advice handling).
- **Signals & Earnings**: `ding-correct-gameshow.mp3` (1.27s aha! reveal), `ding-bell-chime.mp3` (2.95s pro-tip bell), `cash-register-cha-ching.mp3` (2.17s profit/commission), `cash-register-drawer.mp3` (2.43s), `apple-pay-chime.mp3` (1.41s mobile checkout), `wrong-buzzer.mp3` (1.06s myth-busting), `error-buzzer.mp3` (1.12s), `record-scratch-stop.mp3` (0.78s pivot halt), `tape-rewind-fast.mp3` (0.78s rewind scrub), `digital-glitch.mp3` (1.33s).

### C. US Niche & Viral Social (`my-sounds/us-niche/`)
Viral retention hooks and comedic punctuation on US TikTok, Shorts, and Reels:
- **Punctuation & Beats**: `vine-boom.mp3` (1.25s #1 viral emphasis boom), `bruh.mp3` (0.82s deadpan reaction), `dun-dun-dun-brass.mp3` (5.12s comedic reveal), `metal-pipe-clang.mp3` (2.79s chaotic clang), `taco-bell-bong.mp3` (1.91s blunt statement bell).
- **Cartoon & Fails**: `spongebob-fail-womp.mp3` (3.38s womp-womp-womp), `price-is-right-losing-horn.mp3` (5.07s tuba fail), `cartoon-slip-fall.mp3` (1.85s slide and crash), `awkward-cricket.mp3` (4.44s awkward pause).
- **Memes & Hooks**: `discord-ping.mp3` (0.61s attention hook), `iphone-text-notification.mp3` (2.88s iOS chime), `emotional-damage.mp3` (3.32s), `fbi-open-up.mp3` (2.01s), `anime-wow.mp3` (4.18s), `mlg-airhorn.mp3` (2.97s), `windows-xp-error.mp3` (0.99s), `among-us-reveal.mp3` (4.57s), `sad-violin-meme.mp3` (4.55s), `rizz-sound.mp3` (1.93s), `undertaker-bell.mp3` (4.21s), `omg-hell-nah.mp3` (10.40s).

---

## 2. Technical Quirks & Pitfalls

### Sourcing from MyInstants: 404 on Empty Search
- **Pitfall**: When querying `https://www.myinstants.com/en/search/?name=<query>`, MyInstants returns an `HTTP 404 Not Found` status rather than an empty 200 HTML page when zero results match.
- **Rule**: Always wrap `urllib.request.urlopen` in `try...except urllib.error.HTTPError as e:` and treat 404 as `[]` empty results.

### FFmpeg MP3 Inspection: Embedded Cover Art Stream 0
- **Pitfall**: Many soundboard MP3s embed ID3 APIC cover art as video stream 0 (`Stream #0:0: Video: mjpeg`). Running `volumedetect` or `silencedetect` without stream mapping defaults to stream 0, reporting `n_samples: 0` or false trailing silences.
- **Rule**: Always pass `-map a:0` explicitly when probing volume or silence on MP3s:
  ```bash
  ffmpeg -i sound.mp3 -map a:0 -af volumedetect -f null -
  ```

---

## 3. Mixing & Layering Recipes

### Spoken Voice Primacy
Dialogue is always front-and-center at -18 to -22 dBFS RMS. SFX must be scaled to avoid masking vocals:
- Clicks, pops, page turns: `volume=0.20-0.25`
- Whooshes and camera shutters: `volume=0.25-0.30`
- Dramatic impacts, braams, and vine booms: `volume=0.30-0.35`
- Always use `normalize=0` on `amix` to prevent halving speech level.

### Timestamped Multi-SFX Overlay
```bash
ffmpeg -y -i speech_video.mp4 \
  -i /home/john/Documents/free247editor/my-sounds/explainer/pop-clean.mp3 \
  -i /home/john/Documents/free247editor/my-sounds/explainer/whoosh-transition-fast.mp3 \
  -filter_complex "
    [1:a]adelay=3200|3200,volume=0.25[sfx1];
    [2:a]adelay=7800|7800,volume=0.25[sfx2];
    [0:a][sfx1][sfx2]amix=inputs=3:duration=first:normalize=0[aout]
  " \
  -map 0:v -map "[aout]" -c:v copy output_with_sfx.mp4
```

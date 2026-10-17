# Motion Graphics, Procedural Sound Design & Telegram Delivery

Reference guide for producing enhanced social video deliverables (Shorts, Reels, TikTok) with free247editor.

## 1. Telegram Upload Limits & Delivery Recipes

The Telegram ecosystem enforces two distinct size boundaries:
1. **20 MB Inline Playback Boundary**: Telegram mobile clients optimize inline auto-play for media <= 20 MB. Larger files often display as non-streaming file tiles or require explicit taps to download.
2. **50.0 MB Bot API Server Ceiling**: The standard Telegram Bot API strictly refuses any upload > 50 MB with `HTTP 413: Request Entity Too Large`. Bots cannot upload single files exceeding 50 MB to `api.telegram.org`.

### Tier A: Inline Streaming Recipe (Target 18 MB for safety headroom):
```bash
# Calculate target bitrate in kbps:
# target_bits = 18.0 * 1024 * 1024 * 8 = 150,994,944 bits
# total_kbps = int(target_bits / duration_seconds / 1000)
# video_kbps = total_kbps - 128 (assuming 128k AAC audio)

ffmpeg -y -i input_master.mp4 \
  -c:v libx264 -preset medium \
  -b:v ${video_kbps}k -maxrate $((video_kbps * 115 / 100))k -bufsize $((video_kbps * 2))k \
  -c:a aac -b:a 128k \
  -pix_fmt yuv420p -movflags +faststart \
  output-under20mb.mp4
```
Deliver via `MEDIA:/absolute/path/to/output-under20mb.mp4`.

### Tier B: Single-File High-Quality Master (< 50 MB):
When the user requests the master video in high fidelity directly in Telegram, encode an under-50MB master (target ~44-48 MB):
```bash
# Target 46 MB for safe headroom under 50 MB:
# target_bits = 46.0 * 1024 * 1024 * 8 = 385,875,968 bits
# total_kbps = int(target_bits / duration_seconds / 1000)
# video_kbps = total_kbps - 160 (assuming 160k AAC audio)

ffmpeg -y -i input_master.mp4 \
  -c:v libx264 -preset slow \
  -b:v ${video_kbps}k -maxrate $((video_kbps * 115 / 100))k -bufsize $((video_kbps * 2))k \
  -c:a aac -b:a 160k \
  -pix_fmt yuv420p -movflags +faststart \
  output-hq-48mb.mp4
```

### Tier C: Document / File Delivery ("Send via File, not photo/video"):
When the user explicitly asks to receive the video as a **File / Document** (to avoid inline compressed video playback or preserve bit-for-bit quality), **DO NOT use `MEDIA:/path/to/file.mp4` or `sendVideo`** (which trigger Telegram's video transcoding). Send directly as an uncompressed document via Telegram Bot API `sendDocument`:
```bash
TOKEN=$(grep "^TELEGRAM_BOT_TOKEN=" ~/.hermes/.env | cut -d= -f2-)
curl -s -m 180 "https://api.telegram.org/bot${TOKEN}/sendDocument" \
  -F chat_id=1361019810 \
  -F document=@/home/john/Documents/free247editor/outbox/<file>.mp4 \
  -F caption="🎬 <Title> — Master File"
```
Verify `{"ok": true}` and `message_id` in response.

### Tier D: Bit-for-Bit Delivery for Masters > 50 MB:
Split into 40MB 7z volumes and upload each volume via `sendDocument`:
```bash
7z a -v40m <slug>-master.7z <slug>-final.mp4
# Delivers <slug>-master.7z.001, <slug>-master.7z.002, etc.
```

---

## 2. FFmpeg Image Overlay Streaming (`-loop 1`)

When overlaying static graphics, cards, or badges onto video at arbitrary timestamps using `overlay=x:y:enable='between(t, start, end)'`:
- **The Pitfall**: An input without `-loop 1` (e.g. `-i card.png`) only contains one frame at t=0. At t > 0.04s, the input stream reaches EOF. Any subsequent `enable` condition evaluates against an empty/dead stream, rendering nothing.
- **The Correct Pattern**:
```bash
ffmpeg -y \
  -i base_video.mp4 \
  -loop 1 -framerate 30 -i card1.png \
  -loop 1 -framerate 30 -i card2.png \
  -filter_complex "
    [1:v]format=rgba,fade=t=in:st=6.0:d=0.3:alpha=1,fade=t=out:st=11.7:d=0.3:alpha=1[c1];
    [0:v][c1]overlay=0:0:enable='between(t,5.9,12.1)'[v1]
  " \
  -map "[v1]" -map 0:a -t <duration> output.mp4
```
- **Duration Boundary Warning with `-shortest`**: When combining `-loop 1` infinite image streams with `filter_complex` (especially with subtitles or overlay chains), FFmpeg's `-shortest` flag frequently fails to stop at the master audio/video boundary, leaving 1-2s of trailing frozen video. Never rely on `-shortest` alone: always pass `-t <duration>` explicitly or immediately post-trim with `ffmpeg -y -ss 0.0 -t <duration> -i composite.mp4 -c copy final_trimmed.mp4`.

---

## 3. Motion Card Layout & Pop-Up Windows (HyperFrames + GSAP)

To achieve high-retention, fluid motion design as seen in `herk-edit-kit`:
- **Retire Static PIL PNG Cards**: Static PNGs with FFmpeg linear opacity fades look stiff and lack physics. Always prefer native HyperFrames + GSAP rendering at 60 FPS.
- **Reusable Template**: Reference `kit/style-templates/explainer-popup-window/`.
  - macOS dark glassmorphic window chrome: Traffic light dots (red `#ff5f56`, yellow `#ffbd2e`, green `#27c93f`), tab title, status badge.
  - Spring pop-in physics: `gsap.from("#popup-window", { scale: 0.82, opacity: 0, y: 50, duration: 0.55, ease: "back.out(1.75)" })`.
  - Staggered line-by-line item cascade: `gsap.to(".detail-item", { opacity: 1, x: 0, stagger: 0.08, ease: "power3.out" })`.
  - Light sheen sweep: diagonal highlight bar traveling across the glass card.
- **Camera Stage Coordination**: Subtly scale down the host camera footage (scale: 0.95) and dim slightly when the pop-up appears to guide the viewer's eye.
- **Sound Design Sync**: Always pair motion keyframes with `my-sounds/explainer/`:
  - Entry pop: `pop-clean.mp3` (`volume=0.25`)
  - Detail rows: `mouse-click-clean.mp3` (`volume=0.20`)
  - Big metric / stat reveal: `cinematic-thud-metric.mp3` (`volume=0.30`)
  - Exit swoosh: `whoosh-transition-fast.mp3` (`volume=0.25`)
- **Safe Zones**: Center cards between y=420 and y=1100 (upper-middle zone), safely below top status bar and well above lower-third captions and platform UI controls.

---

## 4. Multi-Clip Speed Ramping, Zoom & Hard Duration Sync

When compiling multiple fixed-duration raw clips (e.g., 5 x 10s AI generation clips = 50s) to fit a longer voiceover narrative (e.g., 84s):
1. **Sub-Clip Speed Ramping**:
   - Split each clip into narrative beats:
     - Hyperlapse / fast-motion (1.2x – 1.6x) for high-energy hooks and technical surges: `setpts=(T_target / T_src)*PTS`.
     - Dramatic Slow-motion (0.35x – 0.6x) for emotional reveals, disaster moments, and fluid dynamics.
2. **Dynamic Ken Burns Zoom (FFmpeg native)**:
   - Push-in zoom: `scale=eval=frame:w='1080*(1.0 + 0.12*t/D)':h='1920*(1.0 + 0.12*t/D)',crop=1080:1920:(in_w-out_w)/2:(in_h-out_h)/2`
   - Sudden punch-in cut (5–8% scale): `scale=1.08*in_w:1.08*in_h,crop=1080:1920:(in_w-out_w)/2:(in_h-out_h)/2`
3. **Hard Duration Sync**:
   - Audio duration is the master clock.
   - Avoid trailing silence or desync: Always explicitly trim final render to match audio duration exactly:
     `ffmpeg -y -i composite.mp4 -t <audio_duration_seconds> -c copy final_trimmed.mp4`

---

## 5. Procedural SFX Generation (Python scipy/numpy)

When external audio assets are unavailable, synthesize high-quality procedural WAV sound effects:

```python
import numpy as np
import scipy.io.wavfile as wav

sr = 48000

# Sub impact / braam: exponential frequency drop + low sub-bass + noise burst
dur = 3.5
t = np.linspace(0, dur, int(sr * dur), endpoint=False)
f_sweep = 65.0 * np.exp(-t * 2.2) + 38.0
sub = np.sin(2 * np.pi * f_sweep * t) * np.exp(-t * 1.4)
noise = np.random.uniform(-1, 1, len(t)) * np.exp(-t * 15.0) * 0.4
intro_impact = sub + noise
wav.write('intro_impact.wav', sr, (intro_impact / np.max(np.abs(intro_impact)) * 0.85 * 32767).astype(np.int16))

# Whoosh transition: bandpassed noise envelope
dur = 0.85
t = np.linspace(0, dur, int(sr * dur), endpoint=False)
noise = np.random.uniform(-1, 1, len(t))
env = np.sin(np.pi * (t / dur)) ** 3
whoosh = noise * env
wav.write('whoosh.wav', sr, (whoosh / np.max(np.abs(whoosh)) * 0.85 * 32767).astype(np.int16))

# Telemetry ping / card reveal: high frequency bell transient
dur = 0.6
t = np.linspace(0, dur, int(sr * dur), endpoint=False)
ping = (np.sin(2 * np.pi * 2600.0 * t) * 0.6 + np.sin(2 * np.pi * 3900.0 * t) * 0.3) * np.exp(-t * 12.0)
wav.write('tech_ping.wav', sr, (ping / np.max(np.abs(ping)) * 0.85 * 32767).astype(np.int16))

# Ambient science pulse bed (-22 dB relative to voice):
dur_bed = 84.04
t_full = np.linspace(0, dur_bed, int(sr * dur_bed), endpoint=False)
pad = 0.35 * np.sin(2 * np.pi * 55.0 * t_full) + 0.25 * np.sin(2 * np.pi * 82.41 * t_full)
swell = 0.75 + 0.25 * np.sin(2 * np.pi * 0.12 * t_full)
bed = pad * swell * 0.15
wav.write('ambient_bed.wav', sr, (bed * 32767).astype(np.int16))

# Service desk bell ding / brand accent:
dur_ding = 1.6
t_ding = np.linspace(0, dur_ding, int(sr * dur_ding), endpoint=False)
f0 = 2093.0
partials = [(1.0, 1.0, 4.2), (1.503, 0.45, 5.8), (2.0, 0.35, 7.2), (2.756, 0.25, 8.8), (3.404, 0.15, 10.5)]
bell = sum(amp * np.sin(2 * np.pi * f0 * ratio * t_ding) * np.exp(-t_ding * decay) for ratio, amp, decay in partials)
transient = np.random.uniform(-1, 1, len(t_ding)) * np.exp(-t_ding * 140.0) * 0.35
bell_ding = (bell + transient) / np.max(np.abs(bell + transient)) * 0.90
wav.write('bell_ding.wav', sr, (bell_ding * 32767).astype(np.int16))

# Cash register / checkout ka-ching (mechanical latch + brass bell chime):
dur_cr = 2.0
t_cr = np.linspace(0, dur_cr, int(sr * dur_cr), endpoint=False)
click = np.sin(2 * np.pi * 920.0 * t_cr) * np.exp(-t_cr * 95.0) * 0.6 + np.sin(2 * np.pi * 1550.0 * np.maximum(0, t_cr - 0.028)) * np.exp(-np.maximum(0, t_cr - 0.028) * 110.0) * 0.7 * (t_cr >= 0.028)
coin = np.sin(2 * np.pi * 3350.0 * np.maximum(0, t_cr - 0.045)) * np.exp(-np.maximum(0, t_cr - 0.045) * 50.0) * 0.4 * (t_cr >= 0.045)
t_b = np.maximum(0, t_cr - 0.075)
reg_bell = (np.sin(2 * np.pi * 2349.32 * t_b) * 1.0 * np.exp(-t_b * 3.6) + np.sin(2 * np.pi * 3477.0 * t_b) * 0.55 * np.exp(-t_b * 4.8)) * (t_cr >= 0.075)
checkout = (click + coin + reg_bell) / np.max(np.abs(click + coin + reg_bell)) * 0.90
wav.write('checkout_kaching.wav', sr, (checkout * 32767).astype(np.int16))
```

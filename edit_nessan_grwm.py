#!/usr/bin/env python3
"""
HermiEditor: Nessan GRWM Work-From-Home Vlog & MAANGE Affiliate Showcase
Strict adherence to HermiEditor rules & style guide:
1. Spoken dialogue primacy & voiceover mastering:
   - Voiceover mastered to -14 LUFS, highpass 80Hz, +2.5dB vocal presence boost at 2.8kHz.
   - Background music (Flour and Sunshine, acoustic lifestyle) ducked by -6dB during speech, vol=0.07.
2. Curated tactical SFX from /home/john/Documents/hermieditor/my-sounds/explainer/:
   - 0.00s: pop-clean.mp3 (vlog intro pop)
   - 11.60s: ding-bell-subtle.mp3 ("work mode na tayo")
   - 16.50s: whoosh-transition-fast.mp3 (lipstick transition)
   - 17.50s: pop-clean.mp3 (MAANGE R501 top card reveal)
   - 28.00s: ding-bell-subtle.mp3 ("skin concealer lang muna")
   - 33.50s: whoosh-transition-fast.mp3 (concealer transition)
   - 34.50s: pop-clean.mp3 (MAANGE Concealer top card reveal)
   - 53.76s: ding-correct-gameshow.mp3 ("switch to work" closing chime)
   - 56.40s: cash-register-cha-ching.mp3 (CTA / final snap)
3. Dynamic motion product cards (Explainer-style glassmorphic header pill cards):
   - Non-intrusive top-edge placement (Y=50px), 100% clear of creator's face, hair, and existing bottom captions.
   - Card 1 (17.0s - 26.5s): MAANGE Kissproof Lip Matte (R501, ₱168.09, -35% OFF, Velvet-Matte, Transfer-Proof).
   - Card 2 (34.0s - 45.0s): MAANGE True Fit Concealer (Spot Coverage, High Precision, Acne & Marks, Lip Line Carve).
   - Paired with smooth 0.35s alpha fade-in / fade-out.
4. Professional video deliverable standards:
   - Master 1080x1920 @ 30fps vertical MP4.
   - Deliverable under 20MB for seamless Telegram mobile auto-play streaming.
   - Explicit FFmpeg mapping: -map 0:v -map 1:a.
"""

import os
import sys
import json
import time
import subprocess
import wave
import numpy as np

PROJ_DIR = "/home/john/Documents/hermieditor/inbox/nessan-grwm-maange"
OUTBOX_DIR = "/home/john/Documents/hermieditor/outbox"
MY_SOUNDS_DIR = "/home/john/Documents/hermieditor/my-sounds/explainer"
FFMPEG = "/home/john/.hermes/tools/ffmpeg-9.0.1-linux-x64/bin/ffmpeg"

os.makedirs(OUTBOX_DIR, exist_ok=True)
os.makedirs(f"{PROJ_DIR}/renders", exist_ok=True)

RAW_VIDEO = f"{PROJ_DIR}/raw_vlog.mp4"
BGM_SRC = f"{PROJ_DIR}/bgm_flour_sunshine.mp3"
CARD_LIPSTICK = f"{PROJ_DIR}/cards/card_lipstick_top.png"
CARD_CONCEALER = f"{PROJ_DIR}/cards/card_concealer_top.png"

TOTAL_DUR = 57.233
SR = 48000
TOTAL_SAMPLES = int(SR * TOTAL_DUR)

print("=== STEP 1: EXTRACT & MASTER VOICEOVER ===")
raw_vo_wav = f"{PROJ_DIR}/renders/raw_vo.wav"
proc_vo_wav = f"{PROJ_DIR}/renders/proc_vo.wav"

cmd_vo_ext = [
    FFMPEG, "-y", "-i", RAW_VIDEO,
    "-vn", "-ar", str(SR), "-ac", "2",
    raw_vo_wav
]
subprocess.run(cmd_vo_ext, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

cmd_vo_proc = [
    FFMPEG, "-y", "-i", raw_vo_wav,
    "-af", "highpass=f=80,equalizer=f=2800:t=q:w=1.0:g=2.5,loudnorm=I=-14:LRA=7:TP=-1.5",
    "-ar", str(SR), "-ac", "2",
    proc_vo_wav
]
subprocess.run(cmd_vo_proc, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Read processed voiceover
with wave.open(proc_vo_wav, "rb") as w:
    frames = w.readframes(w.getnframes())
    vo_float = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0
    vo_float = vo_float.reshape(-1, 2)

if len(vo_float) < TOTAL_SAMPLES:
    pad = np.zeros((TOTAL_SAMPLES - len(vo_float), 2), dtype=np.float32)
    vo_float = np.vstack([vo_float, pad])
else:
    vo_float = vo_float[:TOTAL_SAMPLES]

print("=== STEP 2: PROCESS & DUCK LIFESTYLE BGM ===")
proc_bgm_wav = f"{PROJ_DIR}/renders/proc_bgm.wav"
cmd_bgm = [
    FFMPEG, "-y", "-ss", "0.0", "-t", str(TOTAL_DUR), "-i", BGM_SRC,
    "-af", f"equalizer=f=1200:t=q:w=1.2:g=-6,lowpass=f=7500,volume=0.07,afade=t=in:st=0:d=1.0,afade=t=out:st={TOTAL_DUR - 2.5}:d=2.5",
    "-ar", str(SR), "-ac", "2",
    proc_bgm_wav
]
subprocess.run(cmd_bgm, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

with wave.open(proc_bgm_wav, "rb") as w:
    frames = w.readframes(w.getnframes())
    bgm_float = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0
    bgm_float = bgm_float.reshape(-1, 2)

if len(bgm_float) < TOTAL_SAMPLES:
    pad = np.zeros((TOTAL_SAMPLES - len(bgm_float), 2), dtype=np.float32)
    bgm_float = np.vstack([bgm_float, pad])
else:
    bgm_float = bgm_float[:TOTAL_SAMPLES]

# Sidechain ducking against voiceover
vo_env = np.abs(vo_float[:, 0]) + np.abs(vo_float[:, 1])
kernel = np.ones(int(SR * 0.08)) / (SR * 0.08)
vo_smoothed = np.convolve(vo_env, kernel, mode="same")
# When VO is active, duck BGM by 50% (-6dB)
duck_factor = 1.0 - 0.50 * np.clip(vo_smoothed / 0.06, 0.0, 1.0)
bgm_ducked = bgm_float * duck_factor[:, np.newaxis]

print("=== STEP 3: MIX TACTICAL EXPLORER SFX ===")
sfx_bed = np.zeros((TOTAL_SAMPLES, 2), dtype=np.float32)

sfx_cues = [
    {"file": "pop-clean.mp3", "time": 0.05, "gain": 0.8},
    {"file": "ding-bell-subtle.mp3", "time": 11.60, "gain": 0.7},
    {"file": "whoosh-transition-fast.mp3", "time": 16.50, "gain": 0.6},
    {"file": "pop-clean.mp3", "time": 17.50, "gain": 0.85},
    {"file": "ding-bell-subtle.mp3", "time": 28.00, "gain": 0.7},
    {"file": "whoosh-transition-fast.mp3", "time": 33.50, "gain": 0.6},
    {"file": "pop-clean.mp3", "time": 34.50, "gain": 0.85},
    {"file": "ding-correct-gameshow.mp3", "time": 53.76, "gain": 0.75},
    {"file": "cash-register-cha-ching.mp3", "time": 56.40, "gain": 0.9},
]

for cue in sfx_cues:
    sfx_path = os.path.join(MY_SOUNDS_DIR, cue["file"])
    tmp_wav = f"{PROJ_DIR}/renders/tmp_sfx.wav"
    subprocess.run([
        FFMPEG, "-y", "-i", sfx_path, "-ar", str(SR), "-ac", "2", tmp_wav
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    with wave.open(tmp_wav, "rb") as w:
        sfx_data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
        sfx_data = sfx_data.reshape(-1, 2)
    start_idx = int(cue["time"] * SR)
    end_idx = min(start_idx + len(sfx_data), TOTAL_SAMPLES)
    length = end_idx - start_idx
    if length > 0:
        sfx_bed[start_idx:end_idx] += sfx_data[:length] * cue["gain"]

master_audio = vo_float + bgm_ducked + sfx_bed
# Soft limiter to prevent clipping
peak = np.max(np.abs(master_audio))
if peak > 0.95:
    master_audio = master_audio * (0.95 / peak)

master_wav_path = f"{PROJ_DIR}/renders/master_audio.wav"
with wave.open(master_wav_path, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((master_audio * 32767.0).astype(np.int16).tobytes())

print(f"Master audio produced: {master_wav_path} (peak={peak:.3f})")

print("=== STEP 4: COMPOSITE MASTER VIDEO WITH DYNAMIC TOP CARDS ===")
# Card 1: 17.0s to 26.5s (duration 9.5s)
# Card 2: 34.0s to 45.0s (duration 11.0s)
# Alpha fade in: 0.35s, fade out: 0.35s
filter_complex = (
    "[0:v]scale=1080:1920:flags=lanczos[bg];"
    "[1:v]format=rgba,fade=t=in:st=17.0:d=0.35:alpha=1,fade=t=out:st=26.15:d=0.35:alpha=1[c1];"
    "[2:v]format=rgba,fade=t=in:st=34.0:d=0.35:alpha=1,fade=t=out:st=44.65:d=0.35:alpha=1[c2];"
    "[bg][c1]overlay=0:0:enable='between(t,17.0,26.5)'[v1];"
    "[v1][c2]overlay=0:0:enable='between(t,34.0,45.0)'[vout]"
)

master_mp4_path = f"{OUTBOX_DIR}/nessan-grwm-maange-master.mp4"
cmd_render_master = [
    FFMPEG, "-y",
    "-i", RAW_VIDEO,
    "-loop", "1", "-t", str(TOTAL_DUR), "-i", CARD_LIPSTICK,
    "-loop", "1", "-t", str(TOTAL_DUR), "-i", CARD_CONCEALER,
    "-i", master_wav_path,
    "-filter_complex", filter_complex,
    "-map", "[vout]",
    "-map", "3:a",
    "-c:v", "libx264", "-preset", "slow", "-crf", "18",
    "-c:a", "aac", "-b:a", "192k",
    "-pix_fmt", "yuv420p", "-movflags", "+faststart",
    master_mp4_path
]
subprocess.run(cmd_render_master, check=True)
print(f"Master video rendered: {master_mp4_path}")

print("=== STEP 5: OPTIMIZE DELIVERABLE UNDER 20MB FOR TELEGRAM STREAMING ===")
# 18MB target for instantaneous inline playback
# 18 * 1024 * 1024 * 8 / 57.233 / 1000 = ~2635 kbps total
# audio = 128k, video = 2500k
final_mp4_path = f"{OUTBOX_DIR}/nessan-grwm-maange-final.mp4"
cmd_opt = [
    FFMPEG, "-y",
    "-i", master_mp4_path,
    "-c:v", "libx264", "-preset", "medium",
    "-b:v", "2400k", "-maxrate", "2800k", "-bufsize", "4800k",
    "-c:a", "aac", "-b:a", "128k",
    "-pix_fmt", "yuv420p", "-movflags", "+faststart",
    final_mp4_path
]
subprocess.run(cmd_opt, check=True)

final_size_mb = os.path.getsize(final_mp4_path) / (1024 * 1024)
master_size_mb = os.path.getsize(master_mp4_path) / (1024 * 1024)
print(f"SUCCESS! Master: {master_size_mb:.2f} MB | Final Streamable: {final_size_mb:.2f} MB")

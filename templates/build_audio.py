#!/usr/bin/env python3
"""
Template: Master Audio Builder with Voiceover EQ, BGM Ducking, and SFX Mixing.
Part of HermiEditor for Hermes Agent.
"""

import os
import subprocess
import numpy as np
import scipy.io.wavfile as wav

SR = 48000

def build_master_audio(vo_raw_path, bgm_raw_path, total_dur, sfx_list, out_path, bgm_vol=0.07):
    """
    vo_raw_path: path to raw voiceover wav
    bgm_raw_path: path to background music mp3/wav
    total_dur: total duration in seconds
    sfx_list: list of dicts: [{"path": "...", "timestamp": float, "gain_db": float}]
    out_path: destination wav path
    """
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    total_samples = int(SR * total_dur)

    # 1. Process voiceover (highpass 80Hz, +2.5dB boost at 2.8kHz, loudnorm -14 LUFS)
    vo_proc = out_path + ".vo.wav"
    subprocess.run([
        "ffmpeg", "-y", "-i", vo_raw_path,
        "-af", "highpass=f=80,equalizer=f=2800:t=q:w=1.0:g=2.5,loudnorm=I=-14:LRA=7:TP=-1.5",
        "-ar", str(SR), "-ac", "2",
        vo_proc
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    _, vo_data = wav.read(vo_proc)
    vo_float = vo_data.astype(np.float32) / 32768.0
    if len(vo_float) < total_samples:
        pad = np.zeros((total_samples - len(vo_float), 2), dtype=np.float32)
        vo_float = np.vstack([vo_float, pad])
    else:
        vo_float = vo_float[:total_samples]
    if os.path.exists(vo_proc): os.remove(vo_proc)

    # 2. Process BGM (1.2kHz notch, lowpass 7500Hz, volume leveling)
    bgm_proc = out_path + ".bgm.wav"
    subprocess.run([
        "ffmpeg", "-y", "-ss", "0.0", "-t", str(total_dur), "-i", bgm_raw_path,
        "-af", f"equalizer=f=1200:t=q:w=1.2:g=-6,lowpass=f=7500,volume={bgm_vol},afade=t=out:st={max(0, total_dur-1.8)}:d=1.8",
        "-ar", str(SR), "-ac", "2",
        bgm_proc
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    _, bgm_data = wav.read(bgm_proc)
    bgm_float = bgm_data.astype(np.float32) / 32768.0
    if len(bgm_float) < total_samples:
        pad = np.zeros((total_samples - len(bgm_float), 2), dtype=np.float32)
        bgm_float = np.vstack([bgm_float, pad])
    else:
        bgm_float = bgm_float[:total_samples]
    if os.path.exists(bgm_proc): os.remove(bgm_proc)

    # Sidechain ducking BGM against VO
    vo_envelope = np.abs(vo_float[:, 0]) + np.abs(vo_float[:, 1])
    kernel = np.ones(int(SR * 0.05)) / int(SR * 0.05)
    vo_smoothed = np.convolve(vo_envelope, kernel, mode='same')
    duck_factor = 1.0 - 0.50 * np.clip(vo_smoothed / 0.08, 0.0, 1.0)
    bgm_ducked = bgm_float * duck_factor[:, np.newaxis]

    master = vo_float + bgm_ducked

    # 3. Mix SFX
    for sfx in sfx_list:
        sfx_path = sfx["path"]
        start_sec = sfx["timestamp"]
        gain_db = sfx.get("gain_db", 0.0)

        tmp_sfx = out_path + ".sfx.wav"
        subprocess.run([
            "ffmpeg", "-y", "-i", sfx_path,
            "-ar", str(SR), "-ac", "2",
            tmp_sfx
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        _, sfx_data = wav.read(tmp_sfx)
        sfx_f = sfx_data.astype(np.float32) / 32768.0
        if sfx_f.ndim == 1:
            sfx_f = np.column_stack([sfx_f, sfx_f])
        sfx_f *= (10.0 ** (gain_db / 20.0))

        start_idx = int(SR * start_sec)
        end_idx = min(start_idx + len(sfx_f), total_samples)
        master[start_idx:end_idx] += sfx_f[:(end_idx - start_idx)]
        if os.path.exists(tmp_sfx): os.remove(tmp_sfx)

    # 4. Limiter (ceiling -1.0 dBFS)
    peak = np.max(np.abs(master))
    target_peak = 10.0 ** (-1.0 / 20.0)
    if peak > target_peak:
        master = master * (target_peak / peak)

    wav.write(out_path, SR, (master * 32767).astype(np.int16))
    print(f"Master audio saved to {out_path} ({total_dur:.2f}s)")

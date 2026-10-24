#!/usr/bin/env python3
"""
HermiEditor: The 10X Heart System - Episode 1: "The Boy Who Ate Garbage"
Autonomous Video Editor Pipeline (Mode B: Mini Drama Series)

Strictly adheres to HermiEditor rules & user specifications:
- Pure Original Audio: Strictly NO TTS or voiceover dubbing (authentic dialogue & Foley only).
- 1 Line at a Time Subtitles: Synced directly to when each character is talking.
- Single Video Delivery: Only 1 final video (10x-ep01-final.mp4, 1080x1920, CRF 18, 192k AAC).
- 13-Scene Assembly with 0.5s Cinematic Crossfades (xfade=transition=fade)
- Paired Audio Cross-dissolves (acrossfade=d=0.5:c1=tri:c2=tri) for seamless foley & dialogue bed
- 0.5s Fade-in from Black on Scene 1
- Cliffhanger 1.5s freeze-frame hold + 1.2s fade to black on Scene 13
- Audio Blooper Fix: Smoothly duck prompt bleed in Scene 12 while preserving crisp system activation line
- Vocal Presence EQ: Highpass 80Hz + 2.5dB vocal presence boost at 2.8kHz
- Curated Tactical Drama SFX from my-sounds/ matching script actions & emotional beats
- Standalone .ass and .srt files saved in both inbox and outbox
"""

import os
import sys
import time
import shutil
import subprocess
import wave
import numpy as np

INBOX = "/home/john/Documents/hermieditor/inbox/10x"
OUTBOX = "/home/john/Documents/hermieditor/outbox"
MY_SOUNDS = "/home/john/Documents/hermieditor/my-sounds"
WORK_DIR = "/home/john/Documents/hermieditor/.10x_ep01_tmp"

FFMPEG = "ffmpeg"
SLUG = "10x-ep01"
FPS = 24
WIDTH = 1080
HEIGHT = 1920
TRANS_DUR = 0.5
END_HOLD_DUR = 1.5
SR = 48000

# 13 Dramatic Shots matching script & raw video files
CLIPS = [
    {
        "file": "Student_eating_lunch_in_cafeteria_20261022145853.mp4",
        "dur": 8.0,
        "scene": 1,
        "desc": "Scene 1: Rafa eating humble lunch alone at cafeteria corner table"
    },
    {
        "file": "Woman_confronting_man_at_table_20261022145858.mp4",
        "dur": 6.0,
        "scene": 2,
        "desc": "Scene 2: Celine marches in arrogantly, slams hand on table next to Rafa"
    },
    {
        "file": "Hand_shoving_lunchbox_across_table_20261022145847.mp4",
        "dur": 6.0,
        "scene": 3,
        "desc": "Scene 3: Aggressive shove of metal lunchbox across table, spilling rice"
    },
    {
        "file": "Celine_mocking_Rafa_in_cafeteria_20261022145851.mp4",
        "dur": 8.0,
        "scene": 4,
        "desc": "Scene 4: Celine towering over Rafa, cutting mockery across cafeteria"
    },
    {
        "file": "Man_clenching_fists_in_rage_20261022150320.mp4",
        "dur": 4.0,
        "scene": 5,
        "desc": "Scene 5: Rafa's hands tightening into composed fists with quiet resilience"
    },
    {
        "file": "Young_man_speaks_with_resolve_20261022145921.mp4",
        "dur": 8.0,
        "scene": 6,
        "desc": "Scene 6: Rafa looks Celine in the eye, defends his mother's hard work"
    },
    {
        "file": "Students_mocking_in_crowded_cafe…_20261022145942.mp4",
        "dur": 6.0,
        "scene": 7,
        "desc": "Scene 7: Celine smugly laughing as surrounding students point and mock"
    },
    {
        "file": "Ella_sits_beside_Rafa_1080p_20261022145952.mp4",
        "dur": 8.0,
        "scene": 8,
        "desc": "Scene 8: Ella walks calmly through crowd, sits directly beside Rafa"
    },
    {
        "file": "Ella_defying_Celine_at_table_20261022145956.mp4",
        "dur": 6.0,
        "scene": 9,
        "desc": "Scene 9: Ella speaks with gentle defiance to Rafa; Celine shocked"
    },
    {
        "file": "Woman_turns_away_in_disgust_20261022150006.mp4",
        "dur": 4.0,
        "scene": 10,
        "desc": "Scene 10: Celine rolls eyes in disgust, spins on heels and stomps away"
    },
    {
        "file": "Student_walking_in_campus_courtyard_20261022150027.mp4",
        "dur": 8.0,
        "scene": 11,
        "desc": "Scene 11: Rafa walking down sunlit courtyard walkway in emotional contemplation"
    },
    {
        "file": "Man_activates_holographic_system_1080p_20261022150042.mp4",
        "dur": 8.0,
        "scene": 12,
        "desc": "Scene 12: Rafa stops as golden holographic HUD panel flickers to life"
    },
    {
        "file": "Student_reveals_cash_in_backpack_20261022150036.mp4",
        "dur": 8.0,
        "scene": 13,
        "desc": "Scene 13: Rafa reveals stacks of ₱100k cash in backpack; cliffhanger hold"
    }
]

TOTAL_SCENES = len(CLIPS)
TOTAL_BASE_DUR = sum(c["dur"] for c in CLIPS)  # 88.0s
TOTAL_DUR = TOTAL_BASE_DUR + END_HOLD_DUR       # 89.5s
TOTAL_SAMPLES = int(SR * TOTAL_DUR)

# Tactical SFX Cues from my-sounds/ matching narrative beats
SFX_CUES = [
    # Scene 2 (8.0s): Celine hand slam on table + shocked student gasp
    {"file": "mini-drama/punch-impact.mp3", "time": 8.25, "gain": 0.28, "desc": "Celine hand slam on wooden table"},
    {"file": "mini-drama/shocked-gasp.mp3", "time": 8.35, "gain": 0.20, "desc": "Surrounding students shocked gasp"},
    # Scene 3 (14.0s): Lunchbox shove whoosh across table + table scraping suspense impact
    {"file": "explainer/whoosh-transition-fast.mp3", "time": 14.15, "gain": 0.22, "desc": "Hand shoving lunchbox whoosh"},
    {"file": "mini-drama/sudden-suspense-hit.mp3", "time": 14.25, "gain": 0.25, "desc": "Table scraping suspense impact"},
    # Scene 4 (20.0s): Celine mockery tension riser
    {"file": "mini-drama/suspense-tension-riser.mp3", "time": 23.50, "gain": 0.18, "desc": "Mockery tension riser"},
    # Scene 5 (28.0s): Rafa clenching fists somatic stress heartbeat
    {"file": "mini-drama/heartbeat-stress.mp3", "time": 28.20, "gain": 0.25, "desc": "Rafa clenching fists somatic heartbeat"},
    # Scene 6 (32.0s): Emotional violin resonance as Rafa honors his mother's hard work
    {"file": "mini-drama/sad-violin-solo.mp3", "time": 34.65, "gain": 0.18, "desc": "Emotional violin honoring mother's sacrifice"},
    # Scene 7 (40.0s): Smartphones snapping mocking photos in cafeteria
    {"file": "explainer/camera-snap-fast.mp3", "time": 41.00, "gain": 0.20, "desc": "Smartphones snapping photos in crowd"},
    # Scene 8 (46.0s): Ella calm entrance grace harp shimmer
    {"file": "mini-drama/dream-harp-flashback.mp3", "time": 46.50, "gain": 0.22, "desc": "Ella calm entrance grace harp shimmer"},
    # Scene 9 (54.0s): Celine offended shock hit
    {"file": "mini-drama/sudden-suspense-hit.mp3", "time": 58.70, "gain": 0.25, "desc": "Celine offended shock hit"},
    # Scene 10 (60.0s): Celine heels spin-around whoosh
    {"file": "explainer/whoosh-transition-fast.mp3", "time": 61.20, "gain": 0.20, "desc": "Celine spin around on heels whoosh"},
    # Scene 11 (64.0s): Courtyard golden contemplation breeze & chimes
    {"file": "mini-drama/wind-chimes-memory.mp3", "time": 64.50, "gain": 0.20, "desc": "Courtyard contemplation breeze chimes"},
    # Scene 12 (72.0s): Holographic system activation deep bass drop + digital glitch + celestial chime
    {"file": "mini-drama/cinematic-bass-drop.mp3", "time": 72.10, "gain": 0.35, "desc": "System activation deep bass drop"},
    {"file": "explainer/digital-glitch.mp3", "time": 72.40, "gain": 0.25, "desc": "Golden HUD glitch bloom"},
    {"file": "explainer/ding-bell-chime.mp3", "time": 72.70, "gain": 0.30, "desc": "Celestial activation chime"},
    # Scene 13 (80.0s): Cash reveal whoosh + polymer notes rustle + cha-ching + cliffhanger braam & sub-boom
    {"file": "explainer/whoosh-transition-cinematic.mp3", "time": 80.50, "gain": 0.25, "desc": "Backpack cash reveal golden whoosh"},
    {"file": "explainer/paper-crumple.mp3", "time": 80.80, "gain": 0.20, "desc": "Polymer cash banknotes rustle"},
    {"file": "explainer/cash-register-cha-ching.mp3", "time": 85.00, "gain": 0.30, "desc": "₱100k cash confirmation cha-ching"},
    {"file": "mini-drama/cinematic-orchestral-hit.mp3", "time": 87.00, "gain": 0.35, "desc": "Dramatic orchestral hit swell"},
    {"file": "mini-drama/cinematic-braam.mp3", "time": 88.00, "gain": 0.38, "desc": "Cliffhanger ending tension braam"},
    {"file": "mini-drama/cinematic-sub-boom.mp3", "time": 88.20, "gain": 0.35, "desc": "Cliffhanger sub-bass boom echo"}
]

# 1-Line-At-A-Time Subtitle Schedule strictly synced to original speech
SUBTITLE_SCHEDULE = [
    # Scene 1 [0:00 - 8:00] RAFA: Eating humble lunch in cafeteria
    {
        "start": 1.50, "end": 4.20, "style": "Default", "speaker": "RAFA",
        "text": "Kahit ganito lang ang tanghalian ko araw-araw..."
    },
    {
        "start": 4.35, "end": 7.10, "style": "Default", "speaker": "RAFA",
        "text": "magtitiis ako para makapagtapos."
    },
    # Scene 2 [8:00 - 14:00] CELINE: Slams table & confronts Rafa
    {
        "start": 10.45, "end": 11.55, "style": "Default", "speaker": "CELINE",
        "text": "Look at you, Rafa."
    },
    {
        "start": 11.60, "end": 13.95, "style": "Default", "speaker": "CELINE",
        "text": "Kumakain ka pa rin ng pagkaing basura sa harap ng lahat?"
    },
    # Scene 3 [14:00 - 20:00] STUDENTS: Table shove reaction
    {
        "start": 18.80, "end": 20.00, "style": "Default", "speaker": "STUDENTS",
        "text": "Uy, tignan n'yo!"
    },
    # Scene 4 [20:00 - 28:00] CELINE: Cutting mockery
    {
        "start": 21.05, "end": 24.30, "style": "Default", "speaker": "CELINE",
        "text": "Seriously Rafa, hanggang ngayon ba naman ganyan ka pa rin?"
    },
    {
        "start": 24.35, "end": 27.50, "style": "Default", "speaker": "CELINE",
        "text": "Nakakahiya ka, buti na lang talaga iniwan kita!"
    },
    # Scene 6 [32:00 - 40:00] RAFA: Core emotional gut-punch & dignity
    {
        "start": 32.45, "end": 34.55, "style": "Default", "speaker": "RAFA",
        "text": "Tinatawanan mo ang kinakain ko..."
    },
    {
        "start": 34.65, "end": 37.35, "style": "Default", "speaker": "RAFA",
        "text": "Pero Celine, pinaghirapan 'to ni Nanay."
    },
    {
        "start": 37.45, "end": 39.85, "style": "Default", "speaker": "RAFA",
        "text": "Hindi ako nahihiya, dahil wala akong ninanakaw."
    },
    # Scene 7 [40:00 - 46:00] STUDENTS: Cruel laughter & mocking
    {
        "start": 40.50, "end": 42.80, "style": "Default", "speaker": "STUDENTS",
        "text": "Drama naman!"
    },
    {
        "start": 43.00, "end": 45.10, "style": "Default", "speaker": "STUDENTS",
        "text": "Pulubi na nga, ang yabang pa!"
    },
    # Scene 9 [54:00 - 60:00] ELLA & CELINE: Gentle defiance & Celine shock
    {
        "start": 54.45, "end": 56.60, "style": "Default", "speaker": "ELLA",
        "text": "Huwag mo silang pansinin, Rafa."
    },
    {
        "start": 56.95, "end": 58.35, "style": "Default", "speaker": "ELLA",
        "text": "Ako ang tatabi sa'yo."
    },
    {
        "start": 58.60, "end": 59.40, "style": "Default", "speaker": "CELINE",
        "text": "Ha?!"
    },
    # Scene 10 [60:00 - 64:00] CELINE: Retreat in disgust
    {
        "start": 60.30, "end": 62.30, "style": "Default", "speaker": "CELINE",
        "text": "Whatever, losers."
    },
    {
        "start": 62.50, "end": 63.95, "style": "Default", "speaker": "CELINE",
        "text": "Bagay kayong dalawa!"
    },
    # Scene 12 [72:00 - 80:00] SYSTEM: Holographic system activation
    {
        "start": 72.50, "end": 74.80, "style": "SystemVoice", "speaker": "SYSTEM",
        "text": "[10X HEART SYSTEM ACTIVATION DETECTED]"
    },
    {
        "start": 75.10, "end": 77.40, "style": "SystemVoice", "speaker": "SYSTEM",
        "text": "[THE 10X HEART SYSTEM HAS BEEN ACTIVATED]"
    },
    {
        "start": 77.50, "end": 79.95, "style": "SystemVoice", "speaker": "SYSTEM",
        "text": "Initial user confirmed: Rafael Navarro."
    },
    # Scene 13 [80:00 - 89:50] RAFA: ₱100,000 Cliffhanger discovery
    {
        "start": 84.70, "end": 87.00, "style": "Default", "speaker": "RAFA",
        "text": "Isang... daang libo?!"
    }
]

def run_cmd(cmd, desc=""):
    print(f"\n>>> [START] {desc}")
    t0 = time.time()
    res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if res.returncode != 0:
        print(f"FAILED: {desc}")
        # Run again with output visible to diagnose
        res2 = subprocess.run(cmd, capture_output=True, text=True)
        print("STDERR:", res2.stderr[-1000:])
        raise RuntimeError(f"Command failed: {desc}")
    print(f"<<< [DONE] {desc} ({time.time() - t0:.1f}s)")
    return res

def clean_shot12_audio(in_clip, out_clip):
    """
    Cleans audio blooper in Shot 12 where video engine read prompt text
    'Continuous background campus atmosphere' between 0.85s and 3.10s.
    Smoothly ducks that region, leaving 'Ding!' and the authentic system line.
    """
    tmp_orig_wav = f"{WORK_DIR}/tmp_shot12_orig.wav"
    tmp_clean_wav = f"{WORK_DIR}/tmp_shot12_clean.wav"
    
    subprocess.run([
        FFMPEG, "-y", "-i", in_clip,
        "-ar", str(SR), "-ac", "2",
        tmp_orig_wav
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    with wave.open(tmp_orig_wav, "rb") as w:
        data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
        data = data.reshape(-1, 2)
        
    idx_start = int(0.85 * SR)
    idx_end = int(3.10 * SR)
    fade_len = int(0.05 * SR)
    
    cleaned = data.copy()
    fade_in = np.linspace(1.0, 0.0, fade_len)[:, None]
    fade_out = np.linspace(0.0, 1.0, fade_len)[:, None]
    
    cleaned[idx_start:idx_start+fade_len] *= fade_in
    cleaned[idx_start+fade_len:idx_end-fade_len] *= 0.0
    cleaned[idx_end-fade_len:idx_end] *= fade_out
    
    with wave.open(tmp_clean_wav, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((cleaned * 32767.0).astype(np.int16).tobytes())
        
    # Mux clean audio back into video
    subprocess.run([
        FFMPEG, "-y",
        "-i", in_clip,
        "-i", tmp_clean_wav,
        "-map", "0:v", "-map", "1:a",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        out_clip
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("  Shot 12 audio blooper successfully cleaned and re-muxed.")

def step1_assemble_base_video():
    """
    Standardizes 13 clips to 1080x1920 @ 24fps with 0.5s clone padding,
    chains xfade 0.5s transitions and acrossfade original audio dissolves,
    applies intro fade-in and cliffhanger hold.
    """
    print("\n=== STEP 1: ASSEMBLE VIDEO TIMELINE & TRANSITIONS (ORIGINAL SOUNDS) ===")
    os.makedirs(WORK_DIR, exist_ok=True)
    os.makedirs(OUTBOX, exist_ok=True)
    
    std_parts = []
    for idx, c in enumerate(CLIPS):
        in_clip = os.path.join(INBOX, c["file"])
        out_part = f"{WORK_DIR}/clip_{idx+1}_std.mp4"
        
        # Pre-clean Shot 12 audio blooper if applicable
        if c["scene"] == 12:
            clean_clip = f"{WORK_DIR}/clip_12_preclean.mp4"
            clean_shot12_audio(in_clip, clean_clip)
            in_clip = clean_clip
        
        # Scenes 1 to 12 get 0.5s reaction hold padding (tpad/apad) so the 0.5s xfade occurs during hold
        # Scene 13 gets 1.5s freeze-frame hold + 1.2s fade to black at cliffhanger
        if idx < TOTAL_SCENES - 1:
            vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=24,tpad=stop_mode=clone:stop_duration=0.5"
            af = "aformat=sample_rates=48000:channel_layouts=stereo,highpass=f=80,equalizer=f=2800:t=q:w=1.5:g=2.5,apad=pad_dur=0.5"
        else:
            # Scene 13: 1.5s freeze-frame hold on the final frame (total 9.5s)
            vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=24,tpad=stop_mode=clone:stop_duration=1.5,fade=t=out:st=8.3:d=1.2"
            af = "aformat=sample_rates=48000:channel_layouts=stereo,highpass=f=80,equalizer=f=2800:t=q:w=1.5:g=2.5,apad=pad_dur=1.5,afade=t=out:st=8.3:d=1.2"

        cmd = [
            FFMPEG, "-y",
            "-i", in_clip,
            "-vf", vf,
            "-af", af,
            "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
            out_part
        ]
        run_cmd(cmd, f"Standardizing {c['desc']}")
        std_parts.append(out_part)

    # Multi-input xfade + acrossfade assembly: 12 transitions
    assembled_video = f"{WORK_DIR}/assembled_base.mp4"
    cmd_trans = [FFMPEG, "-y"]
    for p in std_parts:
        cmd_trans.extend(["-i", p])

    v_filter = []
    a_filter = []
    # Fade in from black on Scene 1 (first 0.5s)
    v_filter.append("[0:v]fade=t=in:st=0:d=0.5[v0_in]")
    a_filter.append("[0:a]afade=t=in:st=0:d=0.5[a0_in]")
    last_v = "v0_in"
    last_a = "a0_in"

    cum_offset = 0.0
    for i in range(1, TOTAL_SCENES):
        cum_offset += CLIPS[i - 1]["dur"]
        next_v = f"v_trans_{i}"
        next_a = f"a_trans_{i}"
        v_filter.append(
            f"[{last_v}][{i}:v]xfade=transition=fade:duration={TRANS_DUR:.4f}:offset={cum_offset:.4f}[{next_v}]"
        )
        a_filter.append(
            f"[{last_a}][{i}:a]acrossfade=d={TRANS_DUR:.4f}:c1=tri:c2=tri[{next_a}]"
        )
        last_v = next_v
        last_a = next_a

    filter_complex_str = ";\n".join(v_filter + a_filter)
    cmd_trans.extend([
        "-filter_complex", filter_complex_str,
        "-map", f"[{last_v}]",
        "-map", f"[{last_a}]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-t", str(TOTAL_DUR),
        assembled_video
    ])
    run_cmd(cmd_trans, f"Assembling {TOTAL_SCENES} Scenes with 0.5s Cinematic Crossfades and Original Audio")
    return assembled_video

def step2_build_master_audio(base_video):
    """
    Extracts original audio bed (characters' real voices & Foley) from base_video,
    adds the tactical SFX cues from my-sounds/, and performs transparent soft-limiting.
    Strictly NO synthetic voiceover / TTS.
    """
    print("\n=== STEP 2: BUILD MASTER AUDIO MIX (PURE ORIGINAL AUDIO + TACTICAL SFX) ===")
    orig_wav = f"{WORK_DIR}/original_audio.wav"
    subprocess.run([
        FFMPEG, "-y", "-i", base_video,
        "-vn",
        "-ar", str(SR), "-ac", "2",
        orig_wav
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    with wave.open(orig_wav, "rb") as w:
        data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
        orig_float = data.reshape(-1, 2)
    if len(orig_float) < TOTAL_SAMPLES:
        pad = np.zeros((TOTAL_SAMPLES - len(orig_float), 2), dtype=np.float32)
        orig_float = np.vstack([orig_float, pad])
    else:
        orig_float = orig_float[:TOTAL_SAMPLES]

    # Tactical SFX Track
    sfx_track = np.zeros((TOTAL_SAMPLES, 2), dtype=np.float32)
    for cue in SFX_CUES:
        sfx_path = os.path.join(MY_SOUNDS, cue["file"])
        tmp_sfx_wav = f"{WORK_DIR}/tmp_sfx_{int(cue['time']*100)}.wav"
        subprocess.run([
            FFMPEG, "-y", "-i", sfx_path,
            "-ar", str(SR), "-ac", "2",
            tmp_sfx_wav
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        with wave.open(tmp_sfx_wav, "rb") as w:
            data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
            data = data.reshape(-1, 2)
        start_idx = int(cue["time"] * SR)
        end_idx = min(start_idx + len(data), TOTAL_SAMPLES)
        length = end_idx - start_idx
        if length > 0:
            sfx_track[start_idx:end_idx] += data[:length] * cue["gain"]
        if os.path.exists(tmp_sfx_wav):
            os.remove(tmp_sfx_wav)

    # Master Mix: 100% Original Audio + Tactical SFX Accents
    master_mix = orig_float + sfx_track
    peak = np.max(np.abs(master_mix))
    target_peak = 0.85  # ~ -1.4 dBFS
    if peak > target_peak:
        master_mix = master_mix * (target_peak / peak)

    master_audio_wav = f"{WORK_DIR}/master_audio.wav"
    with wave.open(master_audio_wav, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((master_mix * 32767.0).astype(np.int16).tobytes())

    print(f"Master Audio Mix generated: {master_audio_wav} (Peak: {peak:.3f} -> {np.max(np.abs(master_mix)):.3f}, Duration: {TOTAL_DUR:.2f}s)")
    return master_audio_wav

def step3_generate_subtitles():
    """Generates 1-line-at-a-time ASS and SRT subtitles synced to characters' original speech."""
    print("\n=== STEP 3: GENERATE 1-LINE-AT-A-TIME SUBTITLES (.ASS & .SRT) ===")
    ass_path_outbox = f"{OUTBOX}/{SLUG}.ass"
    srt_path_outbox = f"{OUTBOX}/{SLUG}.srt"
    ass_path_inbox = f"{INBOX}/{SLUG}.ass"
    srt_path_inbox = f"{INBOX}/{SLUG}.srt"

    def format_ass_time(sec):
        h = int(sec // 3600)
        m = int((sec % 3600) // 60)
        s = sec % 60
        return f"{h}:{m:02d}:{s:05.2f}"

    def format_srt_time(sec):
        h = int(sec // 3600)
        m = int((sec % 3600) // 60)
        s = int(sec % 60)
        ms = int(round((sec - int(sec)) * 1000))
        if ms >= 1000: ms = 999
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    ass_header = f"""[Script Info]
Title: The 10X Heart System - Episode 1: The Boy Who Ate Garbage
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Liberation Sans,46,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3.0,1.2,2,80,80,280,1
Style: SystemVoice,Liberation Sans,46,&H00D7FFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3.0,1.2,2,80,80,280,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    ass_lines = []
    srt_lines = []
    for idx, item in enumerate(SUBTITLE_SCHEDULE, 1):
        st = item["start"]
        en = item["end"]
        style = item["style"]
        speaker = item["speaker"]
        txt = item["text"]
        
        ass_lines.append(f"Dialogue: 0,{format_ass_time(st)},{format_ass_time(en)},{style},{speaker},0,0,0,,{txt}")
        srt_lines.append(f"{idx}\n{format_srt_time(st)} --> {format_srt_time(en)}\n{txt}\n")

    ass_content = ass_header + "\n".join(ass_lines) + "\n"
    srt_content = "\n".join(srt_lines) + "\n"

    for p in [ass_path_outbox, ass_path_inbox]:
        with open(p, "w", encoding="utf-8") as f:
            f.write(ass_content)
    for p in [srt_path_outbox, srt_path_inbox]:
        with open(p, "w", encoding="utf-8") as f:
            f.write(srt_content)

    print(f"1-Line-at-a-Time Subtitles written ({len(SUBTITLE_SCHEDULE)} cues): {ass_path_outbox} & {srt_path_outbox}")
    return ass_path_outbox

def step4_render_final_master(base_video, master_audio, ass_subtitles):
    """
    Renders ONLY 1 single video file (final master) with burned subtitles,
    explicit stream mapping (-map [vout] -map 1:a), CRF 18, 192k AAC stereo.
    """
    print("\n=== STEP 4: RENDER MASTER FINAL DELIVERABLE (ONLY 1 VIDEO) ===")
    final_master_mp4 = f"{OUTBOX}/{SLUG}-final.mp4"

    cmd = [
        FFMPEG, "-y",
        "-i", base_video,
        "-i", master_audio,
        "-filter_complex", f"[0:v]subtitles='{ass_subtitles}'[vout]",
        "-map", "[vout]",
        "-map", "1:a",
        "-c:v", "libx264", "-preset", "slow", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        "-t", str(TOTAL_DUR),
        final_master_mp4
    ]
    run_cmd(cmd, "Rendering Master Final 1080x1920 Video")

    size_mb = os.path.getsize(final_master_mp4) / (1024 * 1024)
    print(f"\n=======================================================")
    print(f"SUCCESS! Master Video Delivered: {final_master_mp4}")
    print(f"File Size: {size_mb:.2f} MB | Duration: {TOTAL_DUR:.2f}s")
    print(f"Resolution: 1080x1920 (9:16 vertical) @ 24fps")
    print(f"Audio: Pure Original Video Dialogue + Foley Bed + Tactical Drama SFX")
    print(f"Subtitles: 1-Line-At-A-Time Synced to Character Cadence")
    print(f"=======================================================")

def main():
    t_start = time.time()
    # Reset tmp dir
    if os.path.exists(WORK_DIR):
        shutil.rmtree(WORK_DIR)
    os.makedirs(WORK_DIR, exist_ok=True)

    base_video = step1_assemble_base_video()
    master_audio = step2_build_master_audio(base_video)
    ass_subs = step3_generate_subtitles()
    step4_render_final_master(base_video, master_audio, ass_subs)
    print(f"\nTotal Pipeline Execution Time: {time.time() - t_start:.1f}s")

if __name__ == "__main__":
    main()

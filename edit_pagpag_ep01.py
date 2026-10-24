#!/usr/bin/env python3
"""
HermiEditor: Gintong Pag-pag (The Infinite Empathy System) - Episode 1
Autonomous Video Editor Pipeline (Mode B: Mini Drama Series)
Strictly adheres to HermiEditor rules & user specifications:
- Pure Original Audio: Strictly NO TTS or voiceover dubbing (no Kokoro TTS, no Edge-TTS).
- 1 Line at a Time Subtitles: Synced directly to when each character is talking.
- Single Video Delivery: Only 1 final video (pagpag-ep01-final.mp4)
- 10-Scene Assembly with 0.5s Cinematic Crossfades (xfade=transition=fade)
- Paired Audio Cross-dissolves (acrossfade=d=0.5:c1=tri:c2=tri) for seamless original foley & dialogue bed
- 0.5s Fade-in from Black on Scene 1
- Cliffhanger 1.5s freeze-frame hold + 1.2s fade to black on Scene 10
- Curated Tactical Drama SFX from my-sounds/ matching script actions
- Standalone .ass and .srt files saved in both inbox and outbox
"""

import os
import sys
import json
import time
import shutil
import subprocess
import wave
import numpy as np

INBOX = "/home/john/Documents/hermieditor/inbox/Pagpag cashmultipliersystem"
OUTBOX = "/home/john/Documents/hermieditor/outbox"
MY_SOUNDS = "/home/john/Documents/hermieditor/my-sounds"
WORK_DIR = "/home/john/Documents/hermieditor/.pagpag_tmp"

FFMPEG = "ffmpeg"
SLUG = "pagpag-ep01"
FPS = 24
WIDTH = 1080
HEIGHT = 1920
SCENE_DUR = 6.0
TRANS_DUR = 0.5
PAD_DUR = 0.5
END_HOLD_DUR = 1.5
TOTAL_SCENES = 10
TOTAL_DUR = TOTAL_SCENES * SCENE_DUR + END_HOLD_DUR  # 61.5s
SR = 48000
TOTAL_SAMPLES = int(SR * TOTAL_DUR)

CLIPS = [
    {
        "file": "Ren_eating_on_fire_escape_20261020144412.mp4",
        "scene": 1,
        "desc": "Scene 1: Ren eating pag-pag chicken on fire escape in rain"
    },
    {
        "file": "Chloe_opening_school_fire_doors_20261020144446.mp4",
        "scene": 2,
        "desc": "Scene 2: Chloe opening school fire doors on livestream"
    },
    {
        "file": "Chloe_kicking_lunchbox_1080p_20261020144443.mp4",
        "scene": 3,
        "desc": "Scene 3: Chloe kicking stainless lunchbox out of Ren's hands"
    },
    {
        "file": "Lunchbox_splashes_into_muddy_water_20261020144443.mp4",
        "scene": 4,
        "desc": "Scene 4: Lunchbox splashes into muddy water puddle"
    },
    {
        "file": "Ren_gathering_food_in_rain_20261020144428.mp4",
        "scene": 5,
        "desc": "Scene 5: Ren gathering scattered food in rain with quiet dignity"
    },
    {
        "file": "Maya_placing_biscuit_for_Ren_20261020144422.mp4",
        "scene": 6,
        "desc": "Scene 6: Maya placing SkyFlakes biscuit packet next to Ren"
    },
    {
        "file": "Ren_unlocking_sci-fi_system_window_20261020144432.mp4",
        "scene": 7,
        "desc": "Scene 7: Ren unlocking sci-fi system window as rain freezes"
    },
    {
        "file": "Ren's_eyes_widen_in_shock_20261020144438.mp4",
        "scene": 8,
        "desc": "Scene 8: Ren's eyes widen in shock as ₱100k balance is deposited"
    },
    {
        "file": "Man_opening_backpack_with_money_20261020144437.mp4",
        "scene": 9,
        "desc": "Scene 9: Man opening backpack filled with bundled cash"
    },
    {
        "file": "Ren_accepting_anime_quest_1080p_20261020144406.mp4",
        "scene": 10,
        "desc": "Scene 10: Ren accepting anime quest with fiery confident eyes"
    }
]

# Tactical SFX Cues from my-sounds/ matching script actions
SFX_CUES = [
    # Scene 2 (6.0s): Heavy fire door slams open as Chloe bursts in
    {"file": "mini-drama/heavy-door-slam.mp3", "time": 6.10, "gain": 0.35, "desc": "Fire door burst open"},
    # Scene 3 (12.0s): Loud kick impact on metal lunchbox + whoosh
    {"file": "mini-drama/punch-impact.mp3", "time": 14.10, "gain": 0.35, "desc": "Kick impact on stainless lunchbox"},
    {"file": "explainer/whoosh-transition-fast.mp3", "time": 14.15, "gain": 0.20, "desc": "Scattered rice flying whoosh"},
    # Scene 4 (18.0s): Splash in puddle + live stream camera snap & ding
    {"file": "explainer/whoosh-transition-fast.mp3", "time": 18.20, "gain": 0.20, "desc": "Puddle splash whoosh"},
    {"file": "explainer/camera-snap-fast.mp3", "time": 23.00, "gain": 0.25, "desc": "Livestream shutter snap"},
    {"file": "explainer/ding-bell-subtle.mp3", "time": 23.20, "gain": 0.20, "desc": "Livestream notification ding"},
    # Scene 5 (24.0s): Sorrowful resilient violin sting over rain
    {"file": "mini-drama/sad-violin-solo.mp3", "time": 24.30, "gain": 0.15, "desc": "Emotional violin resonance"},
    # Scene 6 (30.0s): Distant thunder rumble + biscuit placement rustle
    {"file": "mini-drama/thunder-rumble.mp3", "time": 30.50, "gain": 0.25, "desc": "Distant storm thunder rumble"},
    {"file": "explainer/paper-crumple.mp3", "time": 31.50, "gain": 0.12, "desc": "SkyFlakes biscuit packet placement rustle"},
    # Scene 7 (36.0s): Deep bass drop + digital time freeze glitch + celestial chime
    {"file": "mini-drama/cinematic-bass-drop.mp3", "time": 36.10, "gain": 0.40, "desc": "Time freeze deep bass drop"},
    {"file": "explainer/digital-glitch.mp3", "time": 36.40, "gain": 0.25, "desc": "Digital holographic bloom glitch"},
    {"file": "explainer/ding-bell-chime.mp3", "time": 36.70, "gain": 0.30, "desc": "System unlock celestial chime"},
    # Scene 8 (42.0s): Cash register deposit ding + gameshow reward confirmation
    {"file": "explainer/cash-register-cha-ching.mp3", "time": 44.80, "gain": 0.30, "desc": "₱100k cash deposit cha-ching"},
    {"file": "explainer/ding-correct-gameshow.mp3", "time": 45.20, "gain": 0.20, "desc": "Inventory deposit confirmation ding"},
    # Scene 9 (48.0s): Ethereal whoosh + crisp polymer cash paper rustle
    {"file": "explainer/whoosh-transition-cinematic.mp3", "time": 48.20, "gain": 0.25, "desc": "Backpack golden glow whoosh"},
    {"file": "explainer/paper-crumple.mp3", "time": 48.70, "gain": 0.20, "desc": "Polymer banknotes rustling"},
    # Scene 10 (54.0s): Anime orchestral swell + cliffhanger tension braam
    {"file": "mini-drama/cinematic-orchestral-hit.mp3", "time": 57.70, "gain": 0.35, "desc": "Epic quest banner reveal hit"},
    {"file": "mini-drama/cinematic-braam.mp3", "time": 60.00, "gain": 0.40, "desc": "Cliffhanger ending tension braam"}
]

# 1-Line-At-A-Time Subtitle Schedule strictly synced to original speech
SUBTITLE_SCHEDULE = [
    # Scene 1 [0:00 - 0:06] REN: Eating pag-pag on fire escape
    {
        "start": 0.64, "end": 3.50, "style": "Default", "speaker": "REN",
        "text": "Day 100 na nako nagakaon og pag-pag dinhi sa Maynila..."
    },
    {
        "start": 3.80, "end": 5.80, "style": "Default", "speaker": "REN",
        "text": "Lami man gihapon bai, basta gikan sa kasing-kasing."
    },
    # Scene 2 [0:06 - 0:12] CHLOE: School fire doors livestream
    {
        "start": 7.25, "end": 9.40, "style": "Default", "speaker": "CHLOE",
        "text": "OMG guys, look! Like ew!"
    },
    {
        "start": 9.55, "end": 11.85, "style": "Default", "speaker": "CHLOE",
        "text": "Sabi ko na nga ba eh, he's eating literally garbage again!"
    },
    # Scene 3 [0:12 - 0:18] CHLOE & REN: Lunchbox kick
    {
        "start": 12.00, "end": 14.70, "style": "Default", "speaker": "CHLOE",
        "text": "Shoo! Kadiri ka, don't eat that here!"
    },
    {
        "start": 15.30, "end": 17.90, "style": "Default", "speaker": "REN",
        "text": "Hoy! Giatay man ka bai oy! Pagkaon na gud na!"
    },
    # Scene 4 [0:18 - 0:24] CHLOE: Puddle splash & mock
    {
        "start": 18.60, "end": 19.90, "style": "Default", "speaker": "CHLOE",
        "text": "Oops, my bad!"
    },
    {
        "start": 20.20, "end": 22.80, "style": "Default", "speaker": "CHLOE",
        "text": "Next time sa basurahan ka na dumiretso kumain, okay?"
    },
    {
        "start": 22.95, "end": 23.85, "style": "Default", "speaker": "CHLOE",
        "text": "Bye, squammy boy!"
    },
    # Scene 5 [0:24 - 0:30] REN: Gathering food in rain
    {
        "start": 24.00, "end": 25.80, "style": "Default", "speaker": "REN",
        "text": "Bakit ka nagka-ganyan, Chloe?"
    },
    {
        "start": 26.15, "end": 28.20, "style": "Default", "speaker": "REN",
        "text": "Nagtitipid lang ako para sa matrikula ko..."
    },
    {
        "start": 28.30, "end": 29.85, "style": "Default", "speaker": "REN",
        "text": "Pero hindi ako susuko."
    },
    # Scene 6 [0:30 - 0:36] MAYA: Soft biscuit placement
    {
        "start": 32.10, "end": 34.10, "style": "Default", "speaker": "MAYA",
        "text": "K-Kuya Ren... ito oh. Bago pa 'yan."
    },
    {
        "start": 34.20, "end": 35.80, "style": "Default", "speaker": "MAYA",
        "text": "Huwag ka na umiyak..."
    },
    # Scene 7 [0:36 - 0:42] SYSTEM: Time freeze & activation
    {
        "start": 37.25, "end": 39.30, "style": "SystemVoice", "speaker": "SYSTEM",
        "text": "[CONDITION MET: 100 DAYS OF PAG-PAG ENDURED]"
    },
    {
        "start": 39.40, "end": 41.90, "style": "SystemVoice", "speaker": "SYSTEM",
        "text": "Bisaya Resilience Karma Overload. Empathy System Activated!"
    },
    # Scene 8 [0:42 - 0:48] SYSTEM & REN: ₱100k cash balance
    {
        "start": 42.00, "end": 43.50, "style": "SystemVoice", "speaker": "SYSTEM",
        "text": "Welcome, Master Ren."
    },
    {
        "start": 43.80, "end": 46.30, "style": "SystemVoice", "speaker": "SYSTEM",
        "text": "Initial Balance: ₱100,000 Cash has been deposited to your inventory."
    },
    {
        "start": 46.35, "end": 47.90, "style": "Default", "speaker": "REN",
        "text": "Hala ka diha... unsa ni?! Ginoo ko!"
    },
    # Scene 9 [0:48 - 0:54] REN: Backpack cash reveal
    {
        "start": 48.00, "end": 49.80, "style": "Default", "speaker": "REN",
        "text": "T-Tinuod ni?!"
    },
    {
        "start": 50.10, "end": 51.60, "style": "Default", "speaker": "REN",
        "text": "Tag-iisang libo?!"
    },
    {
        "start": 51.90, "end": 53.50, "style": "Default", "speaker": "REN",
        "text": "Isang daang libo 'to ah!"
    },
    # Scene 10 [0:54 - 1:00] SYSTEM & REN: First Quest & Cliffhanger
    {
        "start": 54.00, "end": 57.50, "style": "SystemVoice", "speaker": "SYSTEM",
        "text": "[FIRST QUEST: SPEND ₱50,000 ON A DESERVING WOMAN WITHIN 2 HOURS]"
    },
    {
        "start": 57.55, "end": 59.25, "style": "SystemVoice", "speaker": "SYSTEM",
        "text": "Reward: 10x Cash Multiplier (₱500,000)"
    },
    {
        "start": 59.30, "end": 61.20, "style": "Default", "speaker": "REN",
        "text": "Fifty thousand para sa babae? Heh. Chloe, tan-awa ra kung kinsang pag-pag ang gub-on nimo unya!"
    }
]

def run_cmd(cmd, desc=""):
    print(f"\n>>> [START] {desc}")
    t0 = time.time()
    res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if res.returncode != 0:
        print(f"FAILED: {desc}")
        raise RuntimeError(f"Command failed: {desc}")
    print(f"<<< [DONE] {desc} ({time.time() - t0:.1f}s)")
    return res

def step1_assemble_base_video():
    """
    Standardizes 10 clips to 1080x1920 @ 24fps with 0.5s clone padding,
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
        
        # Scenes 1 to 9 get 0.5s reaction hold padding (tpad/apad) so the 0.5s xfade occurs during the hold
        # Scene 10 gets 1.5s freeze-frame hold + 1.2s fade to black at cliffhanger
        if idx < TOTAL_SCENES - 1:
            vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=24,tpad=stop_mode=clone:stop_duration=0.5"
            af = "aformat=sample_rates=48000:channel_layouts=stereo,highpass=f=60,apad=pad_dur=0.5"
        else:
            # Scene 10: 1.5s freeze-frame hold on the final frame (total 7.5s)
            vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=24,tpad=stop_mode=clone:stop_duration=1.5,fade=t=out:st=6.3:d=1.2"
            af = "aformat=sample_rates=48000:channel_layouts=stereo,highpass=f=60,apad=pad_dur=1.5,afade=t=out:st=6.3:d=1.2"

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

    # Multi-input xfade + acrossfade assembly: 9 transitions at 6.0s intervals
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

    # Offsets: 6.0, 12.0, 18.0, 24.0, 30.0, 36.0, 42.0, 48.0, 54.0
    for i in range(1, TOTAL_SCENES):
        offset = i * SCENE_DUR
        next_v = f"v_trans_{i}"
        next_a = f"a_trans_{i}"
        v_filter.append(
            f"[{last_v}][{i}:v]xfade=transition=fade:duration={TRANS_DUR:.4f}:offset={offset:.4f}[{next_v}]"
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
    Extracts the pure original audio bed (characters' real voices & Foley) from base_video,
    adds the tactical SFX cues from my-sounds/, and performs transparent soft-limiting.
    Strictly NO synthetic voiceover / TTS.
    """
    print("\n=== STEP 2: BUILD MASTER AUDIO MIX (PURE ORIGINAL AUDIO + TACTICAL SFX) ===")
    orig_wav = f"{WORK_DIR}/original_audio.wav"
    subprocess.run([
        FFMPEG, "-y", "-i", base_video,
        "-vn", "-af", "highpass=f=60",
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
    if peak > 0.95:
        master_mix = master_mix * (0.95 / peak)

    master_audio_wav = f"{WORK_DIR}/master_audio.wav"
    with wave.open(master_audio_wav, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((master_mix * 32767.0).astype(np.int16).tobytes())

    print(f"Master Audio Mix generated: {master_audio_wav} (Peak: {peak:.3f}, Duration: {TOTAL_DUR:.2f}s)")
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
Title: Gintong Pag-pag: The Infinite Empathy System - Episode 1
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
    explicit stream mapping (-map 0:v -map 1:a), CRF 18, 192k AAC stereo.
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

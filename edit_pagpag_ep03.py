#!/usr/bin/env python3
"""
HermiEditor: Gintong Pag-pag (The Infinite Empathy System) - Episode 3
Title: "Ang 10x Multiplier at ang Liwanag ni Maya"
Autonomous Video Editor Pipeline (Mode B: Mini Drama Series)

Strictly adheres to HermiEditor rules & user specifications:
- Pure Original Audio: Strictly NO TTS or voiceover dubbing (no Kokoro TTS, no Edge-TTS).
- 1 Line at a Time Subtitles: Synced directly to when each character is talking.
- Single Video Delivery: Only 1 final video (pagpag-ep03-final.mp4)
- 10-Scene Assembly with 0.5s Cinematic Crossfades (xfade=transition=fade)
- Paired Audio Cross-dissolves (acrossfade=d=0.5:c1=tri:c2=tri) for seamless original foley & dialogue bed
- 0.5s Fade-in from Black on Scene 1
- Cliffhanger 1.5s freeze-frame hold + 1.2s fade to black on Scene 10
- Curated Tactical Drama SFX from my-sounds/ matching script actions
- Standalone .ass and .srt files saved in both inbox and outbox
"""

import os
import sys
import time
import shutil
import subprocess
import wave
import numpy as np

INBOX = "/home/john/Documents/hermieditor/inbox/Pagpag cashmultipliersystem/Ep3"
OUTBOX = "/home/john/Documents/hermieditor/outbox"
MY_SOUNDS = "/home/john/Documents/hermieditor/my-sounds"
WORK_DIR = "/home/john/Documents/hermieditor/.pagpag_ep03_tmp"

FFMPEG = "ffmpeg"
SLUG = "pagpag-ep03"
FPS = 24
WIDTH = 1080
HEIGHT = 1920
SCENE_DUR = 6.0
TRANS_DUR = 0.5
PAD_DUR = 0.5
END_HOLD_DUR = 1.5
TOTAL_SCENES = 10
TOTAL_DUR = 9 * SCENE_DUR + SCENE_DUR + END_HOLD_DUR  # 61.5s
SR = 48000
TOTAL_SAMPLES = int(SR * TOTAL_DUR)

CLIPS = [
    {
        "file": "Clerk_hands_laptop_to_Maya_20261020173136.mp4",
        "scene": 1,
        "desc": "Scene 1: Clerk hands flagship laptop box with blue ribbon to Maya",
        "gain_db": 0.0
    },
    {
        "file": "Ren_smiling_in_tech_store_20261020173112.mp4",
        "scene": 2,
        "desc": "Scene 2: Ren smiling warmly with gentle amber eyes",
        "gain_db": 0.0
    },
    {
        "file": "Woman_clutching_laptop_box_weeping_20261020173056.mp4",
        "scene": 3,
        "desc": "Scene 3: Maya clutching laptop box weeping tears of gratitude",
        "gain_db": 2.0
    },
    {
        "file": "Woman_wipes_away_stray_tear_20261020173114.mp4",
        "scene": 4,
        "desc": "Scene 4: Maya gently removes wire glasses to wipe stray tear",
        "gain_db": 4.0
    },
    {
        "file": "Maya_removing_glasses_at_sunset_20261020173101.mp4",
        "scene": 5,
        "desc": "Scene 5: Breathtaking goddess reveal illuminated by golden sunset",
        "gain_db": 6.0
    },
    {
        "file": "Ren_staring_at_Maya_in_20261020173120.mp4",
        "scene": 6,
        "desc": "Scene 6: Ren frozen in awe staring at Maya's true face",
        "gain_db": 0.0
    },
    {
        "file": "Chloe_reacts_in_jealous_disbelief_20261020173131.mp4",
        "scene": 7,
        "desc": "Scene 7: Chloe shrieks in jealous disbelief outside store window",
        "gain_db": 0.0
    },
    {
        "file": "Holographic_system_panel_bursts_…_20261020173126.mp4",
        "scene": 8,
        "desc": "Scene 8: Luminous holographic panel bursts open 10X Multiplier",
        "gain_db": 0.0
    },
    {
        "file": "Eyes_reflecting_golden_light_and…_20261020173107.mp4",
        "scene": 9,
        "desc": "Scene 9: Ren's eyes reflecting golden light as Quest Clear is confirmed",
        "gain_db": 0.0
    },
    {
        "file": "Ren_and_Maya_walking_together_20261020173127.mp4",
        "scene": 10,
        "desc": "Scene 10: Ren and Maya walking together into twilight mall lights",
        "gain_db": 0.0
    }
]

# Tactical SFX Cues from my-sounds/ matching script actions
SFX_CUES = [
    # Scene 1 (0.0s - 6.0s): Retail cash register print chime & gentle entry
    {"file": "explainer/apple-pay-chime.mp3", "time": 0.50, "gain": 0.20, "desc": "Retail checkout receipt chime"},

    # Scene 2 (6.0s - 12.0s): Soft transition whoosh & gentle warm dialogue
    {"file": "explainer/whoosh-transition-fast.mp3", "time": 6.00, "gain": 0.15, "desc": "Gentle transition whoosh"},

    # Scene 3 (12.0s - 18.0s): Emotional gratitude violin melody
    {"file": "mini-drama/sad-violin-solo.mp3", "time": 12.50, "gain": 0.18, "desc": "Emotional gratitude violin resonance"},

    # Scene 4 (18.0s - 24.0s): Soft fabric rustle & delicate piano tear chime
    {"file": "explainer/paper-crumple.mp3", "time": 18.50, "gain": 0.12, "desc": "Fabric rustle and glasses adjustment"},
    {"file": "explainer/ding-bell-chime.mp3", "time": 19.00, "gain": 0.15, "desc": "Delicate tear drop chime"},

    # Scene 5 (24.0s - 30.0s): Shinkai goddess reveal golden sparkles & ethereal harp
    {"file": "mini-drama/wind-chimes-memory.mp3", "time": 24.50, "gain": 0.25, "desc": "Golden hour sparkle wind chimes"},
    {"file": "mini-drama/dream-harp-flashback.mp3", "time": 25.00, "gain": 0.20, "desc": "Goddess reveal ethereal harp shimmer"},

    # Scene 6 (30.0s - 36.0s): Loud startled heartbeat thump skipping a beat
    {"file": "mini-drama/heartbeat-stress.mp3", "time": 30.20, "gain": 0.35, "desc": "Loud startled heartbeat thump"},

    # Scene 7 (36.0s - 42.0s): Chloe jealous shock suspense hit
    {"file": "mini-drama/sudden-suspense-hit.mp3", "time": 36.20, "gain": 0.25, "desc": "Chloe jealous shock suspense hit"},

    # Scene 8 (42.0s - 48.0s): Deep bass drop, 10x holographic bloom glitch & celestial chime
    {"file": "mini-drama/cinematic-bass-drop.mp3", "time": 42.10, "gain": 0.40, "desc": "Time freeze deep bass drop"},
    {"file": "explainer/digital-glitch.mp3", "time": 42.30, "gain": 0.25, "desc": "10x holographic system bloom glitch"},
    {"file": "explainer/ding-bell-chime.mp3", "time": 42.50, "gain": 0.30, "desc": "System activation celestial chime"},

    # Scene 9 (48.0s - 54.0s): Quest complete confirmation ding & swirling starlight whoosh
    {"file": "explainer/ding-correct-gameshow.mp3", "time": 48.20, "gain": 0.25, "desc": "Quest complete reward confirmation ding"},
    {"file": "explainer/whoosh-transition-cinematic.mp3", "time": 48.50, "gain": 0.20, "desc": "Swirling golden starlight whoosh"},

    # Scene 10 (54.0s - 61.5s): Triumphant orchestral hit, cliffhanger tension braam & sub-bass drop
    {"file": "mini-drama/cinematic-orchestral-hit.mp3", "time": 54.20, "gain": 0.35, "desc": "Triumphant anime orchestral swell"},
    {"file": "mini-drama/cinematic-braam.mp3", "time": 60.00, "gain": 0.40, "desc": "Cliffhanger ending tension braam"},
    {"file": "mini-drama/cinematic-sub-boom.mp3", "time": 60.00, "gain": 0.35, "desc": "Cliffhanger deep resonant sub-bass drop"}
]

# 1-Line-At-A-Time Subtitle Schedule strictly synced to original speech
SUBTITLE_SCHEDULE = [
    # Scene 1 [0:00 - 0:06] MAYA: Stunned at laptop gift
    {
        "start": 1.60, "end": 3.80, "style": "Default", "speaker": "MAYA",
        "text": "Kuya Ren... hindi ko 'to matatanggap,"
    },
    {
        "start": 3.90, "end": 5.60, "style": "Default", "speaker": "MAYA",
        "text": "sobrang mahal nito!"
    },
    # Scene 2 [0:06 - 0:12] REN: Warm Tagalog-Bisaya comfort
    {
        "start": 6.20, "end": 7.80, "style": "Default", "speaker": "REN",
        "text": "Dawata na, Maya."
    },
    {
        "start": 7.90, "end": 11.50, "style": "Default", "speaker": "REN",
        "text": "Ikaw lang ang nagbigay sa'kin ng pagkain nung tinapakan nila ako."
    },
    # Scene 3 [0:12 - 0:18] MAYA: Tearful gratitude
    {
        "start": 14.70, "end": 17.20, "style": "Default", "speaker": "MAYA",
        "text": "S-Salamat... salamat talaga, Kuya Ren."
    },
    # Scene 4 [0:18 - 0:24] (No speech: Maya removes glasses & wipes tear)
    # Scene 5 [0:24 - 0:30] (No speech: Goddess reveal in golden sunset)
    # Scene 6 [0:30 - 0:36] REN: Breathless Bisdak shock at Maya's beauty
    {
        "start": 31.30, "end": 32.70, "style": "Default", "speaker": "REN",
        "text": "Ginoo ko..."
    },
    {
        "start": 32.90, "end": 34.80, "style": "Default", "speaker": "REN",
        "text": "pagka-guwapa man diay nimo, bai!"
    },
    # Scene 7 [0:36 - 0:42] CHLOE: Jealous disbelief outside
    {
        "start": 37.50, "end": 39.50, "style": "Default", "speaker": "CHLOE",
        "text": "No way! Si Maya ba 'yan?!"
    },
    {
        "start": 39.80, "end": 41.70, "style": "Default", "speaker": "CHLOE",
        "text": "How could that squammy boy buy that?!"
    },
    # Scene 8 [0:42 - 0:48] SYSTEM: 10X Multiplier Activation
    {
        "start": 42.20, "end": 45.20, "style": "SystemVoice", "speaker": "SYSTEM",
        "text": "[DING! SINCERE GRATITUDE CONFIRMED.]"
    },
    {
        "start": 45.80, "end": 47.60, "style": "SystemVoice", "speaker": "SYSTEM",
        "text": "[TEN TIMES MULTIPLIER TRIGGERED!]"
    },
    # Scene 9 [0:48 - 0:54] SYSTEM: Quest Clear Confirmation
    {
        "start": 48.20, "end": 49.50, "style": "SystemVoice", "speaker": "SYSTEM",
        "text": "[QUEST COMPLETE.]"
    },
    {
        "start": 49.70, "end": 52.80, "style": "SystemVoice", "speaker": "SYSTEM",
        "text": "[REWARD CONFIRMED AND STORED IN ACCOUNT!]"
    },
    # Scene 10 [0:54 - 1:01.5] REN: Proud invitation & Cliffhanger
    {
        "start": 55.20, "end": 56.60, "style": "Default", "speaker": "REN",
        "text": "Tara na, Maya."
    },
    {
        "start": 57.00, "end": 59.40, "style": "Default", "speaker": "REN",
        "text": "Librehon pa tika'g panihapon!"
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
    Standardizes 10 clips to 1080x1920 @ 24fps with 0.5s reaction hold padding,
    equalization & volume balance for dialogue clarity,
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

        # Vocal presence boost at 2.8kHz + highpass 80Hz + optional leveling gain
        af_filters = ["aformat=sample_rates=48000:channel_layouts=stereo", "highpass=f=80", "equalizer=f=2800:t=q:w=1.0:g=2.5"]
        if c.get("gain_db", 0.0) != 0.0:
            af_filters.append(f"volume={c['gain_db']}dB")

        # Scenes 1 to 9: 6.0s active + 0.5s clone padding = 6.5s total (156 frames @ 24fps)
        if idx < TOTAL_SCENES - 1:
            vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=24,tpad=stop_mode=clone:stop_duration=0.6"
            af_filters.append("apad=pad_dur=0.6")
            af = ",".join(af_filters)
            target_dur = "6.5"
        else:
            # Scene 10: 6.0s active + 1.5s freeze-frame hold = 7.5s total (180 frames @ 24fps)
            # Fade to black starting at 6.3s for 1.2s ending at 7.5s
            vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=24,tpad=stop_mode=clone:stop_duration=1.6,fade=t=out:st=6.3:d=1.2"
            af_filters.append("apad=pad_dur=1.6")
            af_filters.append("afade=t=out:st=6.3:d=1.2")
            af = ",".join(af_filters)
            target_dur = "7.5"

        cmd = [
            FFMPEG, "-y",
            "-i", in_clip,
            "-vf", vf,
            "-af", af,
            "-t", target_dur,
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
Title: Gintong Pag-pag: The Infinite Empathy System - Episode 3
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

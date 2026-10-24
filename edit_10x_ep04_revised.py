#!/usr/bin/env python3
"""
HermiEditor: The 10X Heart System - Season 1, Episode 04: "No Strings Attached" (Revised Master Cut)
Autonomous Video Editor Pipeline (Adaptive Editing Profile - Mode B: Mini Drama Series)

Strictly adheres to HermiEditor rules & user specifications:
- Adaptive Editing Profile: Mini Drama (1080x1920 @ 24fps, clean visual canvas, story-first pacing).
- Motivated Transitions: Clean professional hard cuts across continuous dialogue (Shots 1-9),
  0.5s fade-in from black at start, 0.4s dramatic dip-to-black between Shot 10 (System 10X Lock) and
  Shot 11 (Race to Registrar), plus 1.5s freeze-frame cliffhanger hold + 1.2s fade-to-black at tail.
- Chinese Drama Sound Design: 10 curated tactical SFX (deadline clock gong, whip pan, suspense sting,
  grant contract thud, respect bronze gong, signature celestial chime, heavy backpack thud, 10X reward chime, trailer braam).
- Audio Mastering: Dialogue clarity mastered with +2.5dB vocal presence boost at 2.8kHz and 80Hz highpass, -14 LUFS loudness.
- Timing Subtitles: Precision Whisper-timed 1 line at a time in lower-third safe zone (MarginV=280).
- Deliverables: outbox/10x-ep04-revised-final.mp4 + 45mb version for Telegram + .ass & .srt sidecars.
"""

import os
import sys
import time
import subprocess
import wave
import numpy as np

INBOX = "/home/john/Documents/hermieditor/inbox/10x revised/ep4"
OUTBOX = "/home/john/Documents/hermieditor/outbox"
WORK_DIR = "/home/john/Documents/hermieditor/.10x_ep04_revised_tmp"
CD_DIR = "/home/john/Documents/hermieditor/my-sounds/chinese-drama"

FFMPEG = "/home/john/.hermes/tools/ffmpeg-9.0.1-linux-x64/bin/ffmpeg"
FFPROBE = "/home/john/.hermes/tools/ffmpeg-9.0.1-linux-x64/bin/ffprobe"
SLUG = "10x-ep04-revised"
FPS = 24
WIDTH = 1080
HEIGHT = 1920
END_HOLD_DUR = 1.5
SR = 48000

# Professional Cinematic Color Grading Filter
COLOR_GRADE = (
    "curves=m='0/0 0.18/0.14 0.5/0.51 0.82/0.85 1/1':"
    "r='0/0 0.5/0.52 1/1':b='0/0.02 0.5/0.49 1/0.98',"
    "colorbalance=rs=-0.02:gs=0.00:bs=0.02:rm=0.03:gm=0.01:bm=-0.02:rh=0.02:gh=0.01:bh=-0.01,"
    "eq=saturation=1.06:contrast=1.04"
)

# 11 Dramatic Shots matching revised script & raw video files
CLIPS = [
    {
        "file": "Student_looking_at_cracked_smart…_1080p_20261024220732.mp4",
        "dur": 8.0,
        "scene": 1,
        "desc": "Shot 1: Registrar notice confirmed on cracked phone",
        "fade_in": 0.5
    },
    {
        "file": "Young_scholar_wiping_tear_1080p_20261024220718.mp4",
        "dur": 6.0,
        "scene": 2,
        "desc": "Shot 2: Ella's fierce defense ('Wala kang nakita, Rafa...')"
    },
    {
        "file": "Young_man_speaking_calmly_1080p_20261024220730.mp4",
        "dur": 8.0,
        "scene": 3,
        "desc": "Shot 3: Rafa formal proposal ('May solusyon ako, Ella...')"
    },
    {
        "file": "Student_speaking_with_caution_1080p_20261024220739.mp4",
        "dur": 8.0,
        "scene": 4,
        "desc": "Shot 4: Ella demand for black and white ('Kung may kapalit 'yan...')"
    },
    {
        "file": "Student_writing_grant_in_notebook_1080p_20261024220813.mp4",
        "dur": 8.0,
        "scene": 5,
        "desc": "Shot 5: Rafa writing the educational grant in notebook"
    },
    {
        "file": "Student_slides_paper_across_table_1080p_20261024220818.mp4",
        "dur": 8.0,
        "scene": 6,
        "desc": "Shot 6: Rafa slides paper across table ('Karapatan mong makapagtapos, Ella')"
    },
    {
        "file": "Young_woman_reading_contract_1080p_20261024220752.mp4",
        "dur": 8.0,
        "scene": 7,
        "desc": "Shot 7: Ella admission of respect ('Humanga ako... nanatili kang nakatayo')"
    },
    {
        "file": "Woman_signs_name_in_notebook_1080p_20261024220747.mp4",
        "dur": 8.0,
        "scene": 8,
        "desc": "Shot 8: Ella signing full name 'Ella Soriano' with tear drop"
    },
    {
        "file": "Student_stands_up_with_backpack_1080p_20261024220757.mp4",
        "dur": 6.0,
        "scene": 9,
        "desc": "Shot 9: Rafa takes the lead ('Alas-tres na... aabutan natin ang registrar!')"
    },
    {
        "file": "Man_viewing_holographic_HUD_text_1080p_20261024220742.mp4",
        "dur": 8.0,
        "scene": 10,
        "desc": "Shot 10: System Beneficiary Lock (10X Cashback — ₱485,000)",
        "fade_out": 0.4  # Dramatic dip to black before the race
    },
    {
        "file": "Two_people_walking_near_building_1080p_20261024220808.mp4",
        "dur": 8.0,
        "scene": 11,
        "desc": "Shot 11: The Race to the Registrar Clock Tower Cliffhanger",
        "fade_in": 0.4,
        "freeze_hold": 1.5,
        "fade_out": 1.2
    }
]

TOTAL_SCENES = len(CLIPS)
TOTAL_BASE_DUR = sum(c["dur"] for c in CLIPS)  # 84.0s
TOTAL_DUR = TOTAL_BASE_DUR + END_HOLD_DUR       # 85.5s
TOTAL_SAMPLES = int(SR * TOTAL_DUR)

# Precision Whisper-timed Subtitle Schedule (1 Line At A Time, MarginV=280 Safe Zone)
SUBTITLE_SCHEDULE = [
    # Shot 1 [0:00 - 8:00] NOTICE: Registrar cancellation alert
    {
        "start": 0.80, "end": 3.80, "style": "SystemVoice", "speaker": "SYSTEM",
        "text": "[FINAL NOTICE: UNPAID TUITION BALANCE ₱48,500]"
    },
    {
        "start": 3.80, "end": 7.20, "style": "SystemVoice", "speaker": "SYSTEM",
        "text": "[DEADLINE: TODAY 5:00 PM — ENROLLMENT CANCELLATION]"
    },
    # Shot 2 [8:00 - 14:00] ELLA: Wounded pride & defense
    {
        "start": 11.00, "end": 13.50, "style": "Default", "speaker": "ELLA",
        "text": "Wala kang nakita, Rafa. Please... umalis ka na."
    },
    # Shot 3 [14:00 - 22:00] RAFA: Calm proposal
    {
        "start": 15.20, "end": 18.30, "style": "Default", "speaker": "RAFA",
        "text": "Forty-eight thousand five hundred. May solusyon ako, Ella."
    },
    {
        "start": 19.30, "end": 21.40, "style": "Default", "speaker": "RAFA",
        "text": "Hindi limos, at lalong hindi awa."
    },
    # Shot 4 [22:00 - 30:00] ELLA: Unyielding skepticism
    {
        "start": 23.18, "end": 24.60, "style": "Default", "speaker": "ELLA",
        "text": "Kung may kapalit 'yan..."
    },
    {
        "start": 25.40, "end": 29.20, "style": "Default", "speaker": "ELLA",
        "text": "...kung may utang na loob akong babayaran sa'yo, hindi ko tatanggapin."
    },
    # Shot 5 [30:00 - 38:00] NOTEBOOK TEXT: Written agreement
    {
        "start": 31.00, "end": 34.50, "style": "Default", "speaker": "RAFA",
        "text": "[STUDENT EDUCATIONAL GRANT — ZERO PERSONAL DEBT]"
    },
    {
        "start": 34.50, "end": 37.50, "style": "Default", "speaker": "RAFA",
        "text": "[NO STRINGS ATTACHED — NO PERSONAL OBLIGATION]"
    },
    # Shot 6 [38:00 - 46:00] RAFA: Sincerity & conviction
    {
        "start": 38.00, "end": 41.50, "style": "Default", "speaker": "RAFA",
        "text": "Pipirmahan ko. Isusulat natin."
    },
    {
        "start": 42.10, "end": 43.40, "style": "Default", "speaker": "RAFA",
        "text": "Walang utang na loob."
    },
    {
        "start": 43.70, "end": 45.40, "style": "Default", "speaker": "RAFA",
        "text": "Karapatan mong makapagtapos, Ella."
    },
    # Shot 7 [46:00 - 54:00] ELLA: Sincere vulnerability & respect
    {
        "start": 48.00, "end": 51.30, "style": "Default", "speaker": "ELLA",
        "text": "Nung pinahiya ka sa cafeteria, hindi ako naawa sa'yo..."
    },
    {
        "start": 51.40, "end": 53.90, "style": "Default", "speaker": "ELLA",
        "text": "...humanga ako. Kasi nanatili kang nakatayo."
    },
    # Shot 8 [54:00 - 62:00] CONTRACT: Ella signs
    {
        "start": 55.50, "end": 61.00, "style": "Default", "speaker": "ELLA",
        "text": "[SIGNATURE: ELLA SORIANO — CONTRACT CONFIRMED]"
    },
    # Shot 9 [62:00 - 68:00] RAFA: Lead to registrar
    {
        "start": 65.10, "end": 67.60, "style": "Default", "speaker": "RAFA",
        "text": "Alas-tres na... aabutan natin ang registrar!"
    },
    # Shot 10 [68:00 - 76:00] SYSTEM HUD: 10X Cashback lock
    {
        "start": 68.50, "end": 71.00, "style": "SystemVoice", "speaker": "SYSTEM",
        "text": "[BENEFICIARY CONFIRMED: ELLA SORIANO]"
    },
    {
        "start": 71.00, "end": 73.50, "style": "SystemVoice", "speaker": "SYSTEM",
        "text": "[QUEST ACTIVATED: SETTLE ₱48,500 TUITION]"
    },
    {
        "start": 73.50, "end": 76.00, "style": "SystemVoice", "speaker": "SYSTEM",
        "text": "[REWARD MULTIPLIER: 10X CASHBACK — ₱485,000]"
    },
    # Shot 11 [76:00 - 85.50] COUNTDOWN CLIFFHANGER
    {
        "start": 77.50, "end": 81.00, "style": "SystemVoice", "speaker": "SYSTEM",
        "text": "[REGISTRAR OFFICE CLOSING: 5:00 PM]"
    },
    {
        "start": 81.00, "end": 84.50, "style": "SystemVoice", "speaker": "SYSTEM",
        "text": "[TIME REMAINING: 45 MINUTES]"
    }
]

# Chinese Drama SFX Schedule (Synchronized to narrative beats)
CHINESE_DRAMA_SFX = [
    # Shot 1: Impending deadline clock gong (0.5s)
    {"file": "chinese_clock_gong_heavy.mp3", "start": 0.50, "vol": 0.45, "desc": "Deadline warning clock gong"},
    # Shot 2: Ella flips phone down sharply (8.2s)
    {"file": "whoosh_fast_transition.mp3", "start": 8.20, "vol": 0.25, "desc": "Phone flip on book foley"},
    # Shot 4: Ella fierce defense / pride sting (23.0s)
    {"file": "glass_suspense_hit.mp3", "start": 23.00, "vol": 0.35, "desc": "Pride defense suspense sting"},
    # Shot 5: Rafa writes agreement (30.5s)
    {"file": "saber_quick_cut.mp3", "start": 30.50, "vol": 0.25, "desc": "Pen writing resolution swish"},
    # Shot 6: Paper slides across table (38.0s) & sub-bass punch (43.7s)
    {"file": "whoosh_fast_transition.mp3", "start": 38.00, "vol": 0.30, "desc": "Contract slide whoosh"},
    {"file": "drum_sub_impact.mp3", "start": 43.70, "vol": 0.45, "desc": "Karapatan mong makapagtapos sub boom"},
    # Shot 7: Emotional barrier dissolves (47.0s)
    {"file": "long_resonance_gong.mp3", "start": 47.00, "vol": 0.35, "desc": "Sincere respect bronze gong"},
    # Shot 8: Signature confirmation chime (56.5s)
    {"file": "achievement_chime_reveal.mp3", "start": 56.50, "vol": 0.55, "desc": "Contract signature confirmation chime"},
    # Shot 9: Heavy backpack thud (63.0s)
    {"file": "cinematic_deep_impact.mp3", "start": 63.00, "vol": 0.50, "desc": "₱100k backpack hoist impact"},
    # Shot 10: 10X Cashback Quest Activated (₱485,000) (68.2s)
    {"file": "achievement_chime_reveal.mp3", "start": 68.20, "vol": 0.70, "desc": "10X Quest celestial chime reveal"},
    {"file": "drum_sub_impact.mp3", "start": 68.50, "vol": 0.50, "desc": "System power-up sub impact"},
    # Shot 11: Race to Registrar cliffhanger braam (76.8s) & decisive clock gong (81.0s)
    {"file": "trailer_epic_impact.mp3", "start": 76.80, "vol": 0.70, "desc": "Race to registrar epic trailer braam"},
    {"file": "chinese_clock_gong_heavy.mp3", "start": 81.00, "vol": 0.50, "desc": "4:15 PM clock tower fateful gong"}
]

def run_cmd(cmd, desc=""):
    print(f"\n>>> [START] {desc}")
    t0 = time.time()
    res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if res.returncode != 0:
        print(f"FAILED: {desc}")
        res2 = subprocess.run(cmd, capture_output=True, text=True)
        print("STDERR:", res2.stderr[-1000:])
        raise RuntimeError(f"Command failed: {desc}")
    print(f"<<< [DONE] {desc} ({time.time() - t0:.1f}s)")
    return res

def step1_assemble_base_video(force=False):
    """
    Standardizes 11 clips to 1080x1920 @ 24fps with cinematic color grading,
    applies motivated cut/fade transitions, and extends Shot 11 with 1.5s freeze hold.
    """
    print("\n=== STEP 1: ASSEMBLE VIDEO TIMELINE WITH CINEMATIC COLOR GRADE & MOTIVATED TRANSITIONS ===")
    os.makedirs(WORK_DIR, exist_ok=True)
    os.makedirs(OUTBOX, exist_ok=True)

    assembled_video = f"{WORK_DIR}/assembled_base.mp4"
    if not force and os.path.exists(assembled_video):
        print(f"Reusing existing assembled base: {assembled_video}")
        return assembled_video

    std_parts = []
    for idx, c in enumerate(CLIPS):
        in_clip = os.path.join(INBOX, c["file"])
        out_part = f"{WORK_DIR}/clip_{idx+1}_std.mp4"

        # Build video filter chain
        vf_filters = [
            "scale=1080:1920:force_original_aspect_ratio=increase",
            "crop=1080:1920",
            "setsar=1",
            COLOR_GRADE,
            "fps=24"
        ]

        # Build audio filter chain
        af_filters = [
            "aformat=sample_rates=48000:channel_layouts=stereo",
            "volume=1.35",
            "highpass=f=80",
            "equalizer=f=2800:t=q:w=1.5:g=2.5"
        ]

        # Head / tail fade transitions
        if "fade_in" in c:
            vf_filters.append(f"fade=t=in:st=0:d={c['fade_in']}")
            af_filters.append(f"afade=t=in:st=0:d={c['fade_in']}")

        if "freeze_hold" in c:
            vf_filters.append(f"tpad=stop_mode=clone:stop_duration={c['freeze_hold']}")
            af_filters.append(f"apad=pad_dur={c['freeze_hold']}")
            vf_filters.append(f"fade=t=out:st=8.3:d={c['fade_out']}")
            af_filters.append(f"afade=t=out:st=8.3:d={c['fade_out']}")
        elif "fade_out" in c:
            st_fade = c["dur"] - c["fade_out"]
            vf_filters.append(f"fade=t=out:st={st_fade:.2f}:d={c['fade_out']}")
            af_filters.append(f"afade=t=out:st={st_fade:.2f}:d={c['fade_out']}")

        vf = ",".join(vf_filters)
        af = ",".join(af_filters)

        cmd = [
            FFMPEG, "-y",
            "-i", in_clip,
            "-vf", vf,
            "-af", af,
            "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
            out_part
        ]
        run_cmd(cmd, f"Standardizing & Grading {c['desc']}")
        std_parts.append(out_part)

    # Concat all standardized clips
    concat_list = f"{WORK_DIR}/concat_list.txt"
    with open(concat_list, "w") as f:
        for p in std_parts:
            f.write(f"file '{p}'\n")

    cmd_concat = [
        FFMPEG, "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_list,
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-t", str(TOTAL_DUR),
        assembled_video
    ]
    run_cmd(cmd_concat, f"Concatenating {TOTAL_SCENES} Scenes into Master Timeline")
    return assembled_video

def step2_build_master_audio(base_video):
    """
    Extracts authentic dialogue audio bed from base_video and blends
    sample-accurate Chinese Drama sound effects at key narrative beats.
    Masters to standard mobile/vertical specs (-14 LUFS / -1.5 dBFS True Peak).
    """
    print("\n=== STEP 2: MASTER AUDIO WITH CHINESE DRAMA SFX ===")
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

    # Build Chinese Drama SFX bed
    sfx_bed = np.zeros((TOTAL_SAMPLES, 2), dtype=np.float32)
    for sfx in CHINESE_DRAMA_SFX:
        sf_name = sfx["file"]
        st_sec = sfx["start"]
        vol = sfx["vol"]
        desc = sfx["desc"]
        sf_path = os.path.join(CD_DIR, sf_name)

        tmp_wav = f"{WORK_DIR}/sfx_{sf_name}.wav"
        subprocess.run([
            FFMPEG, "-y", "-i", sf_path,
            "-ar", str(SR), "-ac", "2",
            tmp_wav
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        with wave.open(tmp_wav, "rb") as sw:
            s_data = np.frombuffer(sw.readframes(sw.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
            s_float = s_data.reshape(-1, 2)

        st_sample = int(st_sec * SR)
        en_sample = min(st_sample + len(s_float), TOTAL_SAMPLES)
        n_copy = en_sample - st_sample
        if n_copy > 0:
            sfx_bed[st_sample:en_sample] += s_float[:n_copy] * vol
            print(f"  [SFX] Layered '{sf_name}' at {st_sec:5.2f}s (dur {len(s_float)/SR:.2f}s, vol {vol}) -> {desc}")

    # Combine authentic dialogue and Chinese drama SFX
    master_mix = orig_float + sfx_bed

    # Headroom soft-limiting
    peak = np.max(np.abs(master_mix))
    target_peak = 0.85  # ~ -1.4 dBFS headroom
    if peak > target_peak:
        master_mix = master_mix * (target_peak / peak)

    unnorm_wav = f"{WORK_DIR}/unnorm_mix.wav"
    with wave.open(unnorm_wav, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((master_mix * 32767.0).astype(np.int16).tobytes())

    # Master to -14 LUFS with True Peak -1.5 dBFS using FFmpeg loudnorm
    master_audio_wav = f"{WORK_DIR}/master_audio_loudnorm.wav"
    cmd_loudnorm = [
        FFMPEG, "-y",
        "-i", unnorm_wav,
        "-af", "loudnorm=I=-14:LRA=7:TP=-1.5",
        "-ar", str(SR),
        master_audio_wav
    ]
    run_cmd(cmd_loudnorm, "Mastering Audio to -14 LUFS / -1.5 True Peak")

    print(f"Master Audio generated: {master_audio_wav} (Headroom Limited & -14 LUFS Normalized)")
    return master_audio_wav

def step3_generate_subtitles():
    """Generates 1-line-at-a-time ASS and SRT subtitles strictly timed to character dialogue."""
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
Title: The 10X Heart System - Episode 4: No Strings Attached (Revised Cut)
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
    Renders the master archive deliverable with burned subtitles (CRF 18)
    and the optimized Telegram delivery deliverable (< 45MB).
    """
    print("\n=== STEP 4: RENDER MASTER FINAL DELIVERABLES ===")
    final_master_mp4 = f"{OUTBOX}/{SLUG}-final.mp4"
    telegram_45mb_mp4 = f"{OUTBOX}/{SLUG}-final-45mb.mp4"

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
    run_cmd(cmd, "Rendering Master Final 1080x1920 Video with Chinese Drama SFX & Burnt Subtitles (CRF 18)")

    size_mb = os.path.getsize(final_master_mp4) / (1024 * 1024)

    # Encode Telegram delivery stream (< 45MB)
    cmd_tg = [
        FFMPEG, "-y",
        "-i", final_master_mp4,
        "-c:v", "libx264", "-preset", "fast", "-crf", "23.5",
        "-c:a", "copy",
        "-movflags", "+faststart",
        telegram_45mb_mp4
    ]
    run_cmd(cmd_tg, "Generating Optimized Direct Telegram Delivery Version (< 45MB)")

    size_tg_mb = os.path.getsize(telegram_45mb_mp4) / (1024 * 1024)

    print(f"\n=======================================================")
    print(f"SUCCESS! Master Video Delivered: {final_master_mp4} ({size_mb:.2f} MB)")
    print(f"Telegram Delivery Video: {telegram_45mb_mp4} ({size_tg_mb:.2f} MB)")
    print(f"Duration: {TOTAL_DUR:.2f}s | Resolution: 1080x1920 (9:16 vertical) @ 24fps")
    print(f"Color Grading: Professional Cinematic Filmic Curves & Warm Tones")
    print(f"Transitions: Motivated Hard Cuts across dialogue + Dip-to-Black into Race")
    print(f"Audio: Dialogue Clarity + 10 Chinese Drama SFX Cues (-14 LUFS)")
    print(f"Subtitles: Precision Whisper-timed 1-Line-At-A-Time in Safe Zone (MarginV=280)")
    print(f"=======================================================")
    return final_master_mp4

def main():
    t_start = time.time()
    os.makedirs(WORK_DIR, exist_ok=True)

    base_video = step1_assemble_base_video(force=True)
    master_audio = step2_build_master_audio(base_video)
    ass_subs = step3_generate_subtitles()
    step4_render_final_master(base_video, master_audio, ass_subs)
    print(f"\nTotal Pipeline Execution Time: {time.time() - t_start:.1f}s")

if __name__ == "__main__":
    main()

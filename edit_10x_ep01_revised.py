#!/usr/bin/env python3
"""
HermiEditor: The 10X Heart System - Season 1, Episode 01: "The Boy Who Ate Garbage" (Revised Cut)
Autonomous Video Editor Pipeline (Adaptive Editing Profile - Mode B: Mini Drama Series)

Strictly adheres to HermiEditor rules & user specifications:
- Adaptive Editing Profile: Mini Drama (1080x1920 @ 24fps, clean visual canvas, story-first pacing).
- Authentic Audio & Chinese Drama SFX: Character dialogue clarity mastered with vocal presence boost (+2.5dB at 2.8kHz, 80Hz highpass)
  layered with curated Chinese drama tactical SFX (slap impact, metal shove crash, heartbeat boom, temple gongs, celestial chimes, epic braam).
- Cinematic Color Grading: Filmic curves, warm skin midtones, cool teal shadows, gentle saturation.
- Professional Transitions: 0.5s fade-in from black, 0.5s cinematic dissolves (xfade=fade),
  paired with smooth audio cross-dissolves (acrossfade=d=0.5:c1=tri:c2=tri), 0.5s reaction holds,
  and 1.5s freeze-frame cliffhanger hold + 1.2s fade-to-black.
- Cut Wrong Parts: Cut Shot 12's AI reference image flash artifact on frame 0 seamlessly.
- Timing Subtitles: Precision Whisper-timed 1 line at a time synced directly to characters' spoken cadence in the lower-third safe zone (MarginV=280).
- Single Video Deliverable: outbox/10x-ep01-revised-final.mp4 + .ass & .srt sidecars in inbox & outbox.
"""

import os
import sys
import time
import shutil
import subprocess
import wave
import numpy as np

INBOX = "/home/john/Documents/hermieditor/inbox/10x revised/ep1"
OUTBOX = "/home/john/Documents/hermieditor/outbox"
WORK_DIR = "/home/john/Documents/hermieditor/.10x_ep01_revised_tmp"
CD_DIR = "/home/john/Documents/hermieditor/my-sounds/chinese-drama"

FFMPEG = "/home/john/.hermes/tools/ffmpeg-9.0.1-linux-x64/bin/ffmpeg"
FFPROBE = "/home/john/.hermes/tools/ffmpeg-9.0.1-linux-x64/bin/ffprobe"
SLUG = "10x-ep01-revised"
FPS = 24
WIDTH = 1080
HEIGHT = 1920
TRANS_DUR = 0.5
END_HOLD_DUR = 1.5
SR = 48000

# Professional Cinematic Color Grading Filter
COLOR_GRADE = (
    "curves=m='0/0 0.18/0.14 0.5/0.51 0.82/0.85 1/1':"
    "r='0/0 0.5/0.52 1/1':b='0/0.02 0.5/0.49 1/0.98',"
    "colorbalance=rs=-0.02:gs=0.00:bs=0.02:rm=0.03:gm=0.01:bm=-0.02:rh=0.02:gh=0.01:bh=-0.01,"
    "eq=saturation=1.06:contrast=1.04"
)

# 13 Dramatic Shots matching revised script & raw video files
CLIPS = [
    {
        "file": "Young_man_eating_lunch_quietly_20261023205705.mp4",
        "dur": 8.0,
        "scene": 1,
        "desc": "Scene 1: Rafa eats quiet humble lunch alone at corner table"
    },
    {
        "file": "Woman_slams_hand_on_table_20261023205709.mp4",
        "dur": 6.0,
        "scene": 2,
        "desc": "Scene 2: Celine marches in arrogantly, slams manicured hand on table"
    },
    {
        "file": "Woman_shoves_metal_lunchbox_1080p_20261023205716.mp4",
        "dur": 4.0,
        "scene": 3,
        "desc": "Scene 3: Macro insert: Celine shoves metal lunchbox across table"
    },
    {
        "file": "Student_confronting_student_in_c…_20261023205831.mp4",
        "dur": 8.0,
        "scene": 4,
        "desc": "Scene 4: Celine towering over Rafa, cutting mockery across cafeteria"
    },
    {
        "file": "Student_clenching_fists_at_table_20261023205719.mp4",
        "dur": 4.0,
        "scene": 5,
        "desc": "Scene 5: Rafa's hands tighten into composed fists with quiet resilience"
    },
    {
        "file": "Young_man_confronting_woman_1080p_20261023205701.mp4",
        "dur": 8.0,
        "scene": 6,
        "desc": "Scene 6: Rafa looks Celine in the eye, defends his mother's sacrifice"
    },
    {
        "file": "Student_mocking_Rafa_in_cafeteria_20261023205745.mp4",
        "dur": 6.0,
        "scene": 7,
        "desc": "Scene 7: Celine smugly laughing as surrounding students point and mock"
    },
    {
        "file": "Woman_sits_at_table_with_20261023205754.mp4",
        "dur": 8.0,
        "scene": 8,
        "desc": "Scene 8: Ella walks calmly through crowd, sits directly beside Rafa"
    },
    {
        "file": "Scholar_speaking_to_peers_at_20261023205736.mp4",
        "dur": 6.0,
        "scene": 9,
        "desc": "Scene 9: Ella speaks with gentle defiance to Rafa; Celine shocked"
    },
    {
        "file": "Woman_stomping_away_in_disgust_20261023205740.mp4",
        "dur": 4.0,
        "scene": 10,
        "desc": "Scene 10: Celine rolls eyes in disgust, spins on heels and stomps away"
    },
    {
        "file": "Student_walking_down_campus_walkway_20261023205708.mp4",
        "dur": 8.0,
        "scene": 11,
        "desc": "Scene 11: Rafa walking down sunlit campus walkway in contemplation"
    },
    {
        "file": "Man_activating_holographic_system_1080p_20261023205726.mp4",
        "dur": 8.0,
        "scene": 12,
        "desc": "Scene 12: Rafa stops as golden holographic HUD panel flickers to life",
        "cut_flash": True  # Remove frame 0 reference image flash artifact
    },
    {
        "file": "Student_unzipping_backpack_with_…_20261023205731.mp4",
        "dur": 8.0,
        "scene": 13,
        "desc": "Scene 13: Rafa reveals stacks of ₱100k cash in backpack; cliffhanger hold"
    }
]

TOTAL_SCENES = len(CLIPS)
TOTAL_BASE_DUR = sum(c["dur"] for c in CLIPS)  # 86.0s
TOTAL_DUR = TOTAL_BASE_DUR + END_HOLD_DUR       # 87.5s
TOTAL_SAMPLES = int(SR * TOTAL_DUR)

# Precision Whisper-timed Subtitle Schedule (1 Line At A Time, MarginV=280 Safe Zone)
SUBTITLE_SCHEDULE = [
    # Scene 1 [0:00 - 8:00] RAFA: Eating humble lunch in cafeteria
    {
        "start": 3.04, "end": 5.70, "style": "Default", "speaker": "RAFA",
        "text": "Kahit ganito lang ang tanghalian ko araw-araw..."
    },
    {
        "start": 5.75, "end": 7.80, "style": "Default", "speaker": "RAFA",
        "text": "magtitiis ako para makapagtapos."
    },
    # Scene 2 [8:00 - 14:00] CELINE: Slams table & confronts Rafa
    {
        "start": 10.48, "end": 11.55, "style": "Default", "speaker": "CELINE",
        "text": "Look at you, Rafa."
    },
    {
        "start": 11.75, "end": 13.75, "style": "Default", "speaker": "CELINE",
        "text": "Kumakain ka pa rin ng ganyan sa harap ng lahat?"
    },
    # Scene 4 [18:00 - 26:00] CELINE: Cutting mockery
    {
        "start": 19.45, "end": 22.75, "style": "Default", "speaker": "CELINE",
        "text": "Seriously Rafa? Hanggang ngayon ba naman ganyan ka pa rin?"
    },
    {
        "start": 23.00, "end": 25.65, "style": "Default", "speaker": "CELINE",
        "text": "Nakakahiya ka! Buti na lang talaga iniwan kita!"
    },
    # Scene 6 [30:00 - 38:00] RAFA: Core emotional gut-punch & dignity
    {
        "start": 31.10, "end": 32.65, "style": "Default", "speaker": "RAFA",
        "text": "Tinatawanan mo ang kinakain ko..."
    },
    {
        "start": 32.80, "end": 35.05, "style": "Default", "speaker": "RAFA",
        "text": "Pero Celine, pinaghirapan 'to ni Nanay."
    },
    {
        "start": 35.25, "end": 37.60, "style": "Default", "speaker": "RAFA",
        "text": "Hindi ako nahihiya, dahil wala akong ninanakaw."
    },
    # Scene 7 [38:00 - 44:00] STUDENTS: Cruel laughter & mocking
    {
        "start": 41.35, "end": 43.70, "style": "Default", "speaker": "STUDENTS",
        "text": "Wala na ngang pera, ang yabang pa!"
    },
    # Scene 9 [52:00 - 58:00] ELLA & CELINE: Gentle defiance & Celine shock
    {
        "start": 52.00, "end": 53.80, "style": "Default", "speaker": "ELLA",
        "text": "Huwag mo silang pansinin, Rafa."
    },
    {
        "start": 54.30, "end": 55.95, "style": "Default", "speaker": "ELLA",
        "text": "Ako ang tatabi sa'yo."
    },
    {
        "start": 56.80, "end": 57.30, "style": "Default", "speaker": "CELINE",
        "text": "Huh?!"
    },
    # Scene 10 [58:00 - 62:00] CELINE: Retreat in disgust
    {
        "start": 58.95, "end": 60.40, "style": "Default", "speaker": "CELINE",
        "text": "Whatever, losers."
    },
    {
        "start": 60.50, "end": 61.55, "style": "Default", "speaker": "CELINE",
        "text": "Bagay kayong dalawa!"
    },
    # Scene 12 [70:00 - 78:00] SYSTEM: Holographic system activation
    {
        "start": 71.10, "end": 74.65, "style": "SystemVoice", "speaker": "SYSTEM",
        "text": "[THE 10X HEART SYSTEM HAS BEEN ACTIVATED]"
    },
    {
        "start": 75.10, "end": 77.75, "style": "SystemVoice", "speaker": "SYSTEM",
        "text": "Initial user confirmed: Rafael Navarro."
    },
    # Scene 13 [78:00 - 87.50] RAFA: ₱100,000 Cliffhanger discovery
    {
        "start": 81.50, "end": 83.60, "style": "Default", "speaker": "RAFA",
        "text": "Isang... daang libo?!"
    }
]

# Chinese Drama SFX Schedule (Tactical placement synchronized to narrative beats)
CHINESE_DRAMA_SFX = [
    # Scene 1 -> 2 transition whoosh
    {"file": "whoosh_fast_transition.mp3", "start": 7.20, "vol": 0.25, "desc": "Scene 1->2 transition whoosh"},
    # Scene 2: Celine slams table (slam hit at 9.80s)
    {"file": "slap_loud_impact.mp3", "start": 9.69, "vol": 0.55, "desc": "Celine hand slam table impact"},
    # Scene 3: Metal lunchbox shoved across table (hit at 16.20s)
    {"file": "metal_explosion_hit.mp3", "start": 16.13, "vol": 0.50, "desc": "Lunchbox shove metallic impact"},
    # Scene 4: Celine towering over Rafa mockery riser
    {"file": "trailer_suspense_riser.mp3", "start": 18.20, "vol": 0.25, "desc": "Celine mockery suspense riser"},
    # Scene 5: Rafa clenches fists in quiet resilience (heartbeat at 27.00s)
    {"file": "heartbeat_deep_impact.mp3", "start": 26.90, "vol": 0.60, "desc": "Clenched fist dramatic heartbeat"},
    # Scene 6: Rafa moral victory line ("wala akong ninanakaw" at 35.25s)
    {"file": "drum_sub_impact.mp3", "start": 35.08, "vol": 0.45, "desc": "Rafa dignity bass sub-impact"},
    # Scene 7: Crowd mocking transition
    {"file": "glass_suspense_hit.mp3", "start": 38.00, "vol": 0.30, "desc": "Mocking crowd tension hit"},
    # Scene 8: Ella calm entrance & solidarity gong
    {"file": "long_resonance_gong.mp3", "start": 44.50, "vol": 0.30, "desc": "Ella solidarity resonant gong"},
    # Scene 9: Celine shock ("Huh?!")
    {"file": "chinese_clock_gong_heavy.mp3", "start": 56.50, "vol": 0.45, "desc": "Celine shock dramatic clock gong"},
    # Scene 10: Celine spin & stomps away whip
    {"file": "whoosh_swish_whip.mp3", "start": 58.00, "vol": 0.40, "desc": "Celine disgust spin whip"},
    # Scene 11: Campus walkway transition
    {"file": "whoosh_fast_transition.mp3", "start": 61.80, "vol": 0.25, "desc": "Campus walkway transition whoosh"},
    # Scene 12: Celestial system "Ding!" activation chime (chime at 71.12s)
    {"file": "achievement_chime_reveal.mp3", "start": 71.00, "vol": 0.65, "desc": "System Ding celestial chime reveal"},
    # Scene 12: Holographic HUD power-up sub impact
    {"file": "drum_sub_impact.mp3", "start": 72.13, "vol": 0.45, "desc": "Holographic HUD power-up sub boom"},
    # Scene 13: Cliffhanger cash reveal epic braam (hit at 81.50s)
    {"file": "trailer_epic_impact.mp3", "start": 80.58, "vol": 0.70, "desc": "Cash reveal cliffhanger epic trailer impact"},
    # Scene 13: Climax resonant Chinese gong into freeze hold
    {"file": "chinese_clock_gong_heavy.mp3", "start": 81.50, "vol": 0.45, "desc": "Cliffhanger resonant clock gong"}
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
    Standardizes 13 clips to 1080x1920 @ 24fps with cinematic color grading,
    cuts Shot 12 reference image flash, applies 0.5s clone reaction padding,
    chains xfade 0.5s transitions and acrossfade original audio dissolves,
    applies intro fade-in and cliffhanger hold.
    """
    print("\n=== STEP 1: ASSEMBLE VIDEO TIMELINE WITH CINEMATIC COLOR GRADE & TRANSITIONS ===")
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

        # Check if shot has wrong part (Shot 12 has frame 0 AI reference image flash)
        cut_flash = c.get("cut_flash", False)

        if idx < TOTAL_SCENES - 1:
            if cut_flash:
                # Shot 12: cut frame 0 flash (1/24s = 0.041667s), pad by 0.541667s so exact total is 8.5s
                vf = (
                    f"select='gte(n,1)',setpts=PTS-STARTPTS,"
                    f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,"
                    f"{COLOR_GRADE},fps=24,tpad=stop_mode=clone:stop_duration=0.541667"
                )
                af = (
                    "aselect='gte(t,0.041667)',asetpts=PTS-STARTPTS,"
                    "aformat=sample_rates=48000:channel_layouts=stereo,"
                    "volume=1.35,highpass=f=80,equalizer=f=2800:t=q:w=1.5:g=2.5,apad=pad_dur=0.541667"
                )
            else:
                # Scenes 1 to 11: 0.5s reaction hold padding
                vf = (
                    f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,"
                    f"{COLOR_GRADE},fps=24,tpad=stop_mode=clone:stop_duration=0.5"
                )
                af = (
                    "aformat=sample_rates=48000:channel_layouts=stereo,"
                    "volume=1.35,highpass=f=80,equalizer=f=2800:t=q:w=1.5:g=2.5,apad=pad_dur=0.5"
                )
        else:
            # Scene 13: 1.5s freeze-frame hold on the final frame (total 9.5s) + 1.2s fade to black
            vf = (
                f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,"
                f"{COLOR_GRADE},fps=24,tpad=stop_mode=clone:stop_duration=1.5,fade=t=out:st=8.3:d=1.2"
            )
            af = (
                "aformat=sample_rates=48000:channel_layouts=stereo,"
                "volume=1.35,highpass=f=80,equalizer=f=2800:t=q:w=1.5:g=2.5,apad=pad_dur=1.5,afade=t=out:st=8.3:d=1.2"
            )

        cmd = [
            FFMPEG, "-y",
            "-i", in_clip,
            "-vf", vf,
            "-af", af,
            "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
            out_part
        ]
        run_cmd(cmd, f"Standardizing & Color Grading {c['desc']}")
        std_parts.append(out_part)

    # Multi-input xfade + acrossfade assembly: 12 transitions
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
    run_cmd(cmd_trans, f"Assembling {TOTAL_SCENES} Scenes with 0.5s Cinematic Dissolves & Transitions")
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

    print(f"Master Audio generated: {master_audio_wav} (Initial Peak: {peak:.3f} -> Headroom Limited & -14 LUFS Normalized)")
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
Title: The 10X Heart System - Episode 1: The Boy Who Ate Garbage (Revised Cut)
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
    CRF 18, 192k AAC stereo, faststart flag for streaming optimization.
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
    run_cmd(cmd, "Rendering Master Final 1080x1920 Video with Chinese Drama SFX & Burnt Subtitles")

    size_mb = os.path.getsize(final_master_mp4) / (1024 * 1024)
    print(f"\n=======================================================")
    print(f"SUCCESS! Master Video Delivered: {final_master_mp4}")
    print(f"File Size: {size_mb:.2f} MB | Duration: {TOTAL_DUR:.2f}s")
    print(f"Resolution: 1080x1920 (9:16 vertical) @ 24fps")
    print(f"Color Grading: Professional Cinematic Filmic Curves & Warm Tones")
    print(f"Audio: Dialogue Clarity + 15 Curated Chinese Drama SFX Layered (-14 LUFS)")
    print(f"Cut Wrong Parts: Eliminated Shot 12 Reference Image Flash Glitch")
    print(f"Subtitles: Precision Whisper-timed 1-Line-At-A-Time in Safe Zone (MarginV=280)")
    print(f"=======================================================")
    return final_master_mp4

def main():
    t_start = time.time()
    os.makedirs(WORK_DIR, exist_ok=True)

    base_video = step1_assemble_base_video(force=False)
    master_audio = step2_build_master_audio(base_video)
    ass_subs = step3_generate_subtitles()
    step4_render_final_master(base_video, master_audio, ass_subs)
    print(f"\nTotal Pipeline Execution Time: {time.time() - t_start:.1f}s")

if __name__ == "__main__":
    main()

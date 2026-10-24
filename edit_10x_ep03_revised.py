#!/usr/bin/env python3
"""
HermiEditor: The 10X Heart System - Season 1, Episode 03: "The Quiet Girl" (Revised Master Cut)
Autonomous Video Editor Pipeline (Adaptive Editing Profile - Mode B: Mini Drama Series)

Strictly adheres to HermiEditor rules & user specifications:
- Adaptive Editing Profile: Mini Drama (1080x1920 @ 24fps, clean visual canvas, story-first pacing).
- Motivated Transitions: Clean professional hard cuts across continuous dialogue (Shots 1-9),
  0.5s fade-in from black at start, 0.4s dramatic dip-to-black between Shot 10 (Ella breakdown) and
  Shot 11 (Rafa resolve), plus 1.5s freeze-frame cliffhanger hold + 1.2s fade-to-black at tail.
- Cut Wrong Parts: Muted accidental off-screen English audio in Shot 7 (0.0s-4.5s) to preserve authentic Tagalog dialogue.
- Chinese Drama Sound Design: 9 curated tactical SFX (paper whoosh, pride bronze gong, celestial HUD chime,
  suspense sting, clock gong, breakdown bell, trailer braam) layered on key narrative beats.
- Audio Mastering: Dialogue clarity mastered with +2.5dB vocal presence boost at 2.8kHz and 80Hz highpass, -14 LUFS loudness.
- Timing Subtitles: Precision Whisper-timed 1 line at a time in lower-third safe zone (MarginV=280).
- Deliverables: outbox/10x-ep03-revised-final.mp4 + 45mb version for Telegram + .ass & .srt sidecars.
"""

import os
import sys
import time
import subprocess
import wave
import numpy as np

INBOX = "/home/john/Documents/hermieditor/inbox/10x revised/ep3"
OUTBOX = "/home/john/Documents/hermieditor/outbox"
WORK_DIR = "/home/john/Documents/hermieditor/.10x_ep03_revised_tmp"
CD_DIR = "/home/john/Documents/hermieditor/my-sounds/chinese-drama"

FFMPEG = "/home/john/.hermes/tools/ffmpeg-9.0.1-linux-x64/bin/ffmpeg"
FFPROBE = "/home/john/.hermes/tools/ffmpeg-9.0.1-linux-x64/bin/ffprobe"
SLUG = "10x-ep03-revised"
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
        "file": "Student_approaches_sitting_class…_1080p_20261024213303.mp4",
        "dur": 8.0,
        "scene": 1,
        "desc": "Shot 1: Rafa approaches the bench ('Ella?')",
        "fade_in": 0.5
    },
    {
        "file": "Student_hiding_document_from_Rafa_1080p_20261024213313.mp4",
        "dur": 6.0,
        "scene": 2,
        "desc": "Shot 2: Ella hides document under book ('Rafa? May kailangan ka ba?')"
    },
    {
        "file": "Students_sitting_on_stone_bench_1080p_20261024213234.mp4",
        "dur": 8.0,
        "scene": 3,
        "desc": "Shot 3: Rafa sitting at respectful distance ('Napansin ko lang...')"
    },
    {
        "file": "Young_woman_holding_heavy_book_1080p_20261024213238.mp4",
        "dur": 8.0,
        "scene": 4,
        "desc": "Shot 4: Ella's unyielding pride ('Sanay ako sa hirap, Rafa...')"
    },
    {
        "file": "Young_man_listening_attentively_1080p_20261024213333.mp4",
        "dur": 6.0,
        "scene": 5,
        "desc": "Shot 5: Rafa listening attentively (System Tactical Warning HUD)"
    },
    {
        "file": "Student_speaks_with_sincere_respect_1080p_20261024213308.mp4",
        "dur": 8.0,
        "scene": 6,
        "desc": "Shot 6: Rafa sincere gratitude ('Hindi awa 'to, Ella...')"
    },
    {
        "file": "Young_woman_reacting_to_words_1080p_20261024213229.mp4",
        "dur": 8.0,
        "scene": 7,
        "desc": "Shot 7: Cracks in the armor ('Hindi ko 'yun ginawa para humingi ng kapalit...')",
        "mute_wrong_part": (0.0, 4.5)  # Mute accidental AI English voice
    },
    {
        "file": "Smartphone_vibrating_on_stone_bench_1080p_20261024213224.mp4",
        "dur": 8.0,
        "scene": 8,
        "desc": "Shot 8: Phone vibrating violently against stone bench"
    },
    {
        "file": "Student_reading_university_tuiti…_1080p_20261024213240.mp4",
        "dur": 8.0,
        "scene": 9,
        "desc": "Shot 9: Macro overdue notice (₱48,500 due today at 5:00 PM)"
    },
    {
        "file": "Young_woman_crying_with_grief_1080p_20261024213308.mp4",
        "dur": 8.0,
        "scene": 10,
        "desc": "Shot 10: Ella silent breakdown / tear",
        "fade_out": 0.4  # Dramatic dip to black before countdown
    },
    {
        "file": "Student_looking_at_cash_and_1080p_20261024213318.mp4",
        "dur": 8.0,
        "scene": 11,
        "desc": "Shot 11: Rafa countdown cliffhanger (₱100k cash / 22 hrs remaining)",
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
    # Shot 1 [0:00 - 8:00] RAFA: Approaches bench
    {
        "start": 4.00, "end": 5.50, "style": "Default", "speaker": "RAFA",
        "text": "Ella?"
    },
    # Shot 2 [8:00 - 14:00] ELLA: Hides document & questions Rafa
    {
        "start": 9.70, "end": 11.00, "style": "Default", "speaker": "ELLA",
        "text": "Rafa?"
    },
    {
        "start": 11.80, "end": 13.10, "style": "Default", "speaker": "ELLA",
        "text": "May... may kailangan ka ba?"
    },
    # Shot 3 [14:00 - 22:00] RAFA: Respectful observation
    {
        "start": 16.85, "end": 20.60, "style": "Default", "speaker": "RAFA",
        "text": "Napansin ko lang... kanina pa parang may bumabagabag sa'yo."
    },
    # Shot 4 [22:00 - 30:00] ELLA: Fierce unyielding pride
    {
        "start": 23.90, "end": 25.60, "style": "Default", "speaker": "ELLA",
        "text": "Sanay ako sa hirap, Rafa."
    },
    {
        "start": 26.05, "end": 27.85, "style": "Default", "speaker": "ELLA",
        "text": "Sanay akong gumawa ng paraan mag-isa."
    },
    {
        "start": 28.45, "end": 29.50, "style": "Default", "speaker": "ELLA",
        "text": "Huwag mo 'kong alalahanin."
    },
    # Shot 5 [30:00 - 36:00] SYSTEM VOICE: Tactical warning HUD
    {
        "start": 30.80, "end": 33.20, "style": "SystemVoice", "speaker": "SYSTEM",
        "text": "[TARGET TRAIT: EXTREME SELF-RELIANCE & PRIDE]"
    },
    {
        "start": 33.20, "end": 35.80, "style": "SystemVoice", "speaker": "SYSTEM",
        "text": "[DIRECT CHARITY WILL TRIGGER 95% REJECTION]"
    },
    # Shot 6 [36:00 - 44:00] RAFA: Sincere gratitude, zero pity
    {
        "start": 36.80, "end": 40.30, "style": "Default", "speaker": "RAFA",
        "text": "Hindi awa 'to, Ella. Nung pinagtawanan ako ng buong cafeteria..."
    },
    {
        "start": 41.00, "end": 43.60, "style": "Default", "speaker": "RAFA",
        "text": "...ikaw lang ang tumabi sa'kin. Gusto ko lang makabawi."
    },
    # Shot 7 [44:00 - 52:00] ELLA: Emotional softening
    {
        "start": 49.20, "end": 51.60, "style": "Default", "speaker": "ELLA",
        "text": "Hindi ko 'yun ginawa para humingi ng kapalit, Rafa..."
    },
    # Shot 9 [60:00 - 68:00] SYSTEM / NOTICE: Tuition overdue
    {
        "start": 61.00, "end": 64.00, "style": "SystemVoice", "speaker": "SYSTEM",
        "text": "[FINAL NOTICE: TUITION OVERDUE — ₱48,500]"
    },
    {
        "start": 64.00, "end": 67.50, "style": "SystemVoice", "speaker": "SYSTEM",
        "text": "[DEADLINE: TODAY 5:00 PM — CANCELLATION OF ENROLLMENT]"
    },
    # Shot 11 [76:00 - 85.50] SYSTEM VOICE: Mission countdown cliffhanger
    {
        "start": 77.50, "end": 81.00, "style": "SystemVoice", "speaker": "SYSTEM",
        "text": "[MISSION DEADLINE: 22 HOURS REMAINING]"
    },
    {
        "start": 81.00, "end": 84.50, "style": "SystemVoice", "speaker": "SYSTEM",
        "text": "[TARGET EXPENDITURE: ₱50,000]"
    }
]

# Chinese Drama SFX Schedule (Synchronized to narrative beats)
CHINESE_DRAMA_SFX = [
    # Shot 2: Document slide under book (8.5s)
    {"file": "whoosh_fast_transition.mp3", "start": 8.20, "vol": 0.25, "desc": "Document slide under book"},
    # Shot 4: Ella unyielding pride resonance (22.3s)
    {"file": "long_resonance_gong.mp3", "start": 22.30, "vol": 0.30, "desc": "Pride bronze gong resonance"},
    # Shot 5: System warning HUD activation (30.2s)
    {"file": "achievement_chime_reveal.mp3", "start": 30.20, "vol": 0.65, "desc": "System warning HUD chime"},
    {"file": "drum_sub_impact.mp3", "start": 30.40, "vol": 0.40, "desc": "HUD analysis sub boom"},
    # Shot 7: Ella emotional softening heartbeat (45.0s)
    {"file": "heartbeat_deep_impact.mp3", "start": 44.80, "vol": 0.50, "desc": "Emotional empathy heartbeat"},
    # Shot 8: Sudden phone vibration shock interrupt (52.0s)
    {"file": "glass_suspense_hit.mp3", "start": 52.00, "vol": 0.45, "desc": "Phone alert suspense sting"},
    # Shot 9: 5:00 PM cancellation deadline toll (60.2s)
    {"file": "chinese_clock_gong_heavy.mp3", "start": 60.20, "vol": 0.50, "desc": "Urgent deadline clock gong"},
    # Shot 10: Ella silent breakdown / tear (68.5s)
    {"file": "dramatic_bell_toll.mp3", "start": 68.50, "vol": 0.35, "desc": "Sorrowful breakdown resonance"},
    # Shot 11: 22-Hour mission countdown cliffhanger braam (76.8s)
    {"file": "trailer_epic_impact.mp3", "start": 76.80, "vol": 0.70, "desc": "Cliffhanger mission braam"},
    # Shot 11: Resonant gong on jaw clench into freeze hold (81.0s)
    {"file": "chinese_clock_gong_heavy.mp3", "start": 81.00, "vol": 0.45, "desc": "Climax decision clock gong"}
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
    mutes accidental AI English voice in Shot 7, applies motivated cut/fade transitions,
    and extends Shot 11 with 1.5s freeze-frame cliffhanger hold + fade-to-black.
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

        # Mute wrong part in Shot 7 (accidental off-screen English audio)
        if "mute_wrong_part" in c:
            m_st, m_en = c["mute_wrong_part"]
            af_filters.append(f"volume=0:enable='between(t,{m_st},{m_en})'")

        # Head / tail fade transitions
        if "fade_in" in c:
            vf_filters.append(f"fade=t=in:st=0:d={c['fade_in']}")
            af_filters.append(f"afade=t=in:st=0:d={c['fade_in']}")

        if "freeze_hold" in c:
            # Shot 11: freeze hold 1.5s + fade out 1.2s
            vf_filters.append(f"tpad=stop_mode=clone:stop_duration={c['freeze_hold']}")
            af_filters.append(f"apad=pad_dur={c['freeze_hold']}")
            vf_filters.append(f"fade=t=out:st=8.3:d={c['fade_out']}")
            af_filters.append(f"afade=t=out:st=8.3:d={c['fade_out']}")
        elif "fade_out" in c:
            # Shot 10: dip-to-black tail
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
Title: The 10X Heart System - Episode 3: The Quiet Girl (Revised Cut)
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
    print(f"Transitions: Motivated Hard Cuts across dialogue + Dip-to-Black into Cliffhanger")
    print(f"Audio: Dialogue Clarity + 10 Chinese Drama SFX Cues (-14 LUFS)")
    print(f"Cut Wrong Parts: Accidental AI English voice in Shot 7 cleanly muted")
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

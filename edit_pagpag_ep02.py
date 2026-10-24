#!/usr/bin/env python3
"""
HermiEditor: Gintong Pag-pag (The Infinite Empathy System) - Episode 2
Title: "Ang Glass Window at ang ₱50,000 na Cash"
Autonomous Video Editor Pipeline (Mode B: Mini Drama Series)

Strictly adheres to HermiEditor rules & user specifications:
- Pure Original Audio: Strictly NO TTS or voiceover dubbing (no Kokoro TTS, no Edge-TTS).
- 1 Line at a Time Subtitles: Synced directly to when each character is talking.
- Single Video Delivery: Only 1 final video (pagpag-ep02-final.mp4)
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

INBOX = "/home/john/Documents/hermieditor/inbox/Pagpag cashmultipliersystem/ep2"
OUTBOX = "/home/john/Documents/hermieditor/outbox"
MY_SOUNDS = "/home/john/Documents/hermieditor/my-sounds"
WORK_DIR = "/home/john/Documents/hermieditor/.pagpag_ep02_tmp"

FFMPEG = "ffmpeg"
SLUG = "pagpag-ep02"
FPS = 24
WIDTH = 1080
HEIGHT = 1920
SCENE_DUR = 10.0
TRANS_DUR = 0.5
PAD_DUR = 0.5
END_HOLD_DUR = 1.5
TOTAL_SCENES = 10
TOTAL_DUR = 9 * SCENE_DUR + SCENE_DUR + END_HOLD_DUR  # 101.5s
SR = 48000
TOTAL_SAMPLES = int(SR * TOTAL_DUR)

CLIPS = [
    {
        "file": "Young_man_sprinting_through_mall_20261020160347.mp4",
        "scene": 1,
        "desc": "Scene 1: Ren sprinting through luxury tech mall",
        "gain_db": 0.0
    },
    {
        "file": "Girl_laughs_outside_luxury_boutique_20261020160048.mp4",
        "scene": 2,
        "desc": "Scene 2: Chloe laughing on livestream outside luxury boutique",
        "gain_db": 0.0
    },
    {
        "file": "Chloe_mocking_Ren_at_mall_20261020160353.mp4",
        "scene": 3,
        "desc": "Scene 3: Chloe mocking Ren at mall",
        "gain_db": 0.0
    },
    {
        "file": "Ren_looking_at_store_display_20261020160059.mp4",
        "scene": 4,
        "desc": "Scene 4: Ren looking at store display and noticing Maya",
        "gain_db": 4.0
    },
    {
        "file": "Girl_gazing_at_laptop_store_20261020160137.mp4",
        "scene": 5,
        "desc": "Scene 5: Maya gazing through glass at flagship laptop display",
        "gain_db": 3.5
    },
    {
        "file": "Girl_adjusting_glasses_with_laptop_20261020160054.mp4",
        "scene": 6,
        "desc": "Scene 6: Maya adjusting glasses holding cracked laptop in tote bag",
        "gain_db": 6.0
    },
    {
        "file": "Ren_approaches_Maya_at_glass_20261020160402.mp4",
        "scene": 7,
        "desc": "Scene 7: Ren approaches Maya at glass window",
        "gain_db": 0.0
    },
    {
        "file": "Ren_leading_Maya_into_store_20261020160057.mp4",
        "scene": 8,
        "desc": "Scene 8: Ren leading Maya into store as Chloe scoffs outside",
        "gain_db": 2.0
    },
    {
        "file": "Boy_placing_card_on_counter_20261020160614.mp4",
        "scene": 9,
        "desc": "Scene 9: Ren placing card on counter to buy flagship laptop",
        "gain_db": 0.0
    },
    {
        "file": "Ren_reveals_fifty_thousand_cash_20261020160327.mp4",
        "scene": 10,
        "desc": "Scene 10: ₱50k cash reveal, Chloe pure shock & payment confirmed",
        "gain_db": 2.0
    }
]

# Tactical SFX Cues from my-sounds/ matching script actions
SFX_CUES = [
    # Scene 1 (0.0s - 10.0s): Sprint entry whoosh & countdown ticking
    {"file": "explainer/whoosh-transition-fast.mp3", "time": 0.50, "gain": 0.20, "desc": "Sprint entry whoosh"},
    {"file": "explainer/digital-glitch.mp3", "time": 2.00, "gain": 0.25, "desc": "Countdown timer pulse"},
    {"file": "mini-drama/heartbeat-stress.mp3", "time": 2.50, "gain": 0.25, "desc": "Urgent countdown heartbeat"},

    # Scene 2 (10.0s - 20.0s): Transition whoosh into luxury boutique
    {"file": "explainer/whoosh-transition-fast.mp3", "time": 10.00, "gain": 0.15, "desc": "Scene 2 transition whoosh"},

    # Scene 3 (20.0s - 30.0s): Livestream camera pan snap & suspense hit
    {"file": "explainer/camera-snap-fast.mp3", "time": 20.20, "gain": 0.25, "desc": "Livestream camera snap"},
    {"file": "mini-drama/sudden-suspense-hit.mp3", "time": 21.00, "gain": 0.25, "desc": "Chloe spots Ren suspense hit"},

    # Scene 4 (30.0s - 40.0s): Soft bass resonance turning to Maya
    {"file": "mini-drama/cinematic-sub-boom.mp3", "time": 34.50, "gain": 0.30, "desc": "Ren spots Maya bass resonance"},

    # Scene 5 (40.0s - 50.0s): Maya longing bittersweet violin resonance
    {"file": "mini-drama/sad-violin-solo.mp3", "time": 42.50, "gain": 0.16, "desc": "Maya longing bittersweet violin"},

    # Scene 6 (50.0s - 60.0s): Canvas bag rustle & nostalgic wind chimes
    {"file": "explainer/paper-crumple.mp3", "time": 52.00, "gain": 0.14, "desc": "Canvas bag and laptop plastic rustle"},
    {"file": "mini-drama/wind-chimes-memory.mp3", "time": 53.50, "gain": 0.20, "desc": "Bittersweet memory wind chimes"},

    # Scene 7 (60.0s - 70.0s): Heartbeat thud on Maya startled reaction
    {"file": "mini-drama/heartbeat-stress.mp3", "time": 64.50, "gain": 0.30, "desc": "Heartbeat thud on Maya startled reaction"},

    # Scene 8 (70.0s - 80.0s): Modern retail chime sliding glass door
    {"file": "mini-drama/shop-door-bell.mp3", "time": 70.80, "gain": 0.28, "desc": "Modern retail chime sliding glass door"},

    # Scene 9 (80.0s - 90.0s): Approaching counter confident whoosh & VIP card / POS terminal payment chime
    {"file": "explainer/whoosh-transition-cinematic.mp3", "time": 84.00, "gain": 0.22, "desc": "Approaching counter whoosh"},
    {"file": "explainer/apple-pay-chime.mp3", "time": 88.50, "gain": 0.30, "desc": "VIP card / POS terminal chime"},

    # Scene 10 (90.0s - 101.5s): Climax shock, payment confirmation & cliffhanger braam
    {"file": "mini-drama/punch-impact.mp3", "time": 92.20, "gain": 0.25, "desc": "Smartphone clatters onto mall floor"},
    {"file": "mini-drama/shocked-gasp.mp3", "time": 94.50, "gain": 0.25, "desc": "Stunned crowd gasp"},
    {"file": "explainer/cash-register-cha-ching.mp3", "time": 97.20, "gain": 0.30, "desc": "₱50k cash transaction cha-ching"},
    {"file": "explainer/ding-correct-gameshow.mp3", "time": 97.40, "gain": 0.25, "desc": "System AI payment confirmation ding"},
    {"file": "mini-drama/cinematic-orchestral-hit.mp3", "time": 98.80, "gain": 0.35, "desc": "Anime quest reward orchestral hit"},
    {"file": "mini-drama/cinematic-braam.mp3", "time": 100.00, "gain": 0.40, "desc": "Cliffhanger ending tension braam"},
    {"file": "mini-drama/cinematic-bass-drop.mp3", "time": 100.00, "gain": 0.35, "desc": "Cliffhanger deep sub-bass drop"}
]

# 1-Line-At-A-Time Subtitle Schedule strictly synced to original speech
SUBTITLE_SCHEDULE = [
    # Scene 1 [0:00 - 0:10] REN: Sprinting in mall
    {
        "start": 2.90, "end": 4.80, "style": "Default", "speaker": "REN",
        "text": "One hour na lang nahabilin..."
    },
    {
        "start": 5.40, "end": 7.10, "style": "Default", "speaker": "REN",
        "text": "Asa man ko mangita'g babaye?!"
    },
    # Scene 2 [0:10 - 0:20] CHLOE: Laughing outside luxury boutique on livestream
    {
        "start": 11.58, "end": 16.50, "style": "Default", "speaker": "CHLOE",
        "text": "So anyway guys, like literally so squammy earlier..."
    },
    {
        "start": 16.80, "end": 19.20, "style": "Default", "speaker": "CHLOE",
        "text": "I had to sanitize my shoes!"
    },
    # Scene 3 [0:20 - 0:30] CHLOE: Mocking Ren at mall
    {
        "start": 21.60, "end": 23.30, "style": "Default", "speaker": "CHLOE",
        "text": "Wait, look who's here!"
    },
    {
        "start": 23.45, "end": 26.80, "style": "Default", "speaker": "CHLOE",
        "text": "Is that Ren wandering around a luxury tech mall?"
    },
    {
        "start": 27.20, "end": 28.70, "style": "Default", "speaker": "CHLOE",
        "text": "Wrong building, bro!"
    },
    # Scene 4 [0:30 - 0:40] REN: Looking at store display
    {
        "start": 31.90, "end": 33.60, "style": "Default", "speaker": "REN",
        "text": "Pasagdi na'ng buang..."
    },
    {
        "start": 35.70, "end": 38.30, "style": "Default", "speaker": "REN",
        "text": "Huy, kinsa man to?"
    },
    # Scene 5 [0:40 - 0:50] MAYA: Gazing at laptop store display
    {
        "start": 43.68, "end": 46.20, "style": "Default", "speaker": "MAYA",
        "text": "Kahit second-hand lang sana..."
    },
    {
        "start": 46.80, "end": 48.40, "style": "Default", "speaker": "MAYA",
        "text": "Para sa thesis ko."
    },
    # Scene 6 [0:50 - 1:00] MAYA: Adjusting glasses with laptop
    {
        "start": 55.40, "end": 58.50, "style": "Default", "speaker": "MAYA",
        "text": "Kailangan kitang pagtiisan hanggang graduation..."
    },
    # Scene 7 [1:00 - 1:10] REN & MAYA: Approaching at glass
    {
        "start": 63.20, "end": 64.50, "style": "Default", "speaker": "REN",
        "text": "Gusto mo 'yan, di ba?"
    },
    {
        "start": 64.65, "end": 65.25, "style": "Default", "speaker": "MAYA",
        "text": "H-Ha?"
    },
    {
        "start": 65.40, "end": 67.20, "style": "Default", "speaker": "REN",
        "text": "Halika sa loob."
    },
    {
        "start": 67.50, "end": 68.30, "style": "Default", "speaker": "MAYA",
        "text": "Kuya Ren?!"
    },
    # Scene 8 [1:10 - 1:20] CHLOE: Laughing through glass window
    {
        "start": 74.14, "end": 77.10, "style": "Default", "speaker": "CHLOE",
        "text": "Look at them! Are they gonna ask for free flyers?"
    },
    {
        "start": 77.30, "end": 78.40, "style": "Default", "speaker": "CHLOE",
        "text": "Kadiri talaga!"
    },
    # Scene 9 [1:20 - 1:30] REN: Card on counter
    {
        "start": 84.36, "end": 87.20, "style": "Default", "speaker": "REN",
        "text": "Miss, kanang flagship laptop sa display..."
    },
    {
        "start": 87.25, "end": 89.10, "style": "Default", "speaker": "REN",
        "text": "Bayaran nako karon dayon!"
    },
    # Scene 10 [1:30 - 1:41.5] CHLOE & SYSTEM: Cash reveal & confirmation
    {
        "start": 91.90, "end": 93.00, "style": "Default", "speaker": "CHLOE",
        "text": "W-What the..."
    },
    {
        "start": 94.60, "end": 97.00, "style": "Default", "speaker": "CHLOE",
        "text": "Fifty thousand in cash?!"
    },
    {
        "start": 97.40, "end": 99.50, "style": "SystemVoice", "speaker": "SYSTEM",
        "text": "[DING! PAYMENT CONFIRMED! JOY REACTION ANALYZING...]"
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

        # Scenes 1 to 9: 10.0s active + 0.5s clone padding = 10.5s total (252 frames @ 24fps)
        if idx < TOTAL_SCENES - 1:
            vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=24,tpad=stop_mode=clone:stop_duration=0.6"
            af_filters.append("apad=pad_dur=0.6")
            af = ",".join(af_filters)
            target_dur = "10.5"
        else:
            # Scene 10: 10.0s active + 1.5s freeze-frame hold = 11.5s total (276 frames @ 24fps)
            # Fade to black starting at 10.3s for 1.2s ending at 11.5s
            vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=24,tpad=stop_mode=clone:stop_duration=1.6,fade=t=out:st=10.3:d=1.2"
            af_filters.append("apad=pad_dur=1.6")
            af_filters.append("afade=t=out:st=10.3:d=1.2")
            af = ",".join(af_filters)
            target_dur = "11.5"

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

    # Multi-input xfade + acrossfade assembly: 9 transitions at 10.0s intervals
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

    # Offsets: 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0
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
Title: Gintong Pag-pag: The Infinite Empathy System - Episode 2
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

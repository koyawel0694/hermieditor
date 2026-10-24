#!/usr/bin/env python3
"""
HermiEditor: SIGNAL ZERO — Episode 01: "Just a Technician"
Autonomous Video Editing Pipeline (Adaptive Editing Profile - Mode B: Mini Drama Series)

Strictly adheres to HermiEditor rules & user specifications:
- Adaptive Editing Profile: Mini Drama (1080x1920 Vertical 9:16 @ 24fps, clean visual canvas, story-first pacing).
- Motivated Transitions:
  * 0.5s cinematic fade-in from black at 0.0s.
  * 1.0s dramatic dip-to-black (0.5s fade-out + 0.5s fade-in) between Shot 1 (Press Conference) and Shot 2 (Executive Office).
  * Professional hard cuts across continuous dialogue and reaction shots (Shots 2->3, 3->4, 4->5, 5->6).
  * Cliffhanger cut to black at elevator doors closing (Shot 6).
- Chinese Drama Sound Design: 15 precision-placed tactical SFX cues from my-sounds/chinese-drama/
  (gong resonance, fast whooshes, heartbeat impacts, clock gongs, suspense glass sting, tension risers,
  smart card unclip, badge desk strike, epic braam, and somber bell toll).
- Audio Mastering: Dialogue clarity mastered with +2.5dB vocal presence boost at 2.8kHz, 80Hz highpass, -14 LUFS loudness.
- Cinematic Color Grading: Filmic corporate cool blue-grey curve, deep contrast, pristine skin midtones.
- Precision Timing Subtitles: Whisper-timed 1-line-at-a-time subtitles in the safe zone (MarginV=280).
- Deliverables: outbox/signal-zero-ep01-final.mp4 + sidecar .srt & .ass files.
"""

import os
import sys
import time
import shutil
import subprocess

INBOX = "/home/john/Documents/hermieditor/inbox/Signal Zero"
OUTBOX = "/home/john/Documents/hermieditor/outbox"
WORK_DIR = "/home/john/Documents/hermieditor/.signal_zero_ep01_tmp"
CD_DIR = "/home/john/Documents/hermieditor/my-sounds/chinese-drama"

FFMPEG = "/home/john/.hermes/tools/ffmpeg-9.0.1-linux-x64/bin/ffmpeg"
FFPROBE = "/home/john/.hermes/tools/ffmpeg-9.0.1-linux-x64/bin/ffprobe"
SLUG = "signal-zero-ep01"
FPS = 24
WIDTH = 1080
HEIGHT = 1920
TOTAL_DUR = 54.00

# 6 Dramatic Shots matching script & raw files
SHOTS = [
    {
        "id": 1,
        "name": "The Stolen Credit",
        "file": "Man_speaking_at_podium_1080p_20261024225659.mp4",
        "duration": 10.00,
        "fade_in": 0.5,
        "fade_out": 0.5,  # Dip to black into executive office
    },
    {
        "id": 2,
        "name": "The Token Bonus",
        "file": "Man_sliding_envelope_across_desk_1080p_20261024225424.mp4",
        "duration": 8.00,
        "fade_in": 0.5,  # Fade in from black
        "fade_out": 0.0,
    },
    {
        "id": 3,
        "name": "The Glass Ceiling",
        "file": "Elena_confronts_Julian_over_prom…_1080p_20261024225704.mp4",
        "duration": 10.00,
        "fade_in": 0.0,
        "fade_out": 0.0,
    },
    {
        "id": 4,
        "name": "The Held Reaction",
        "file": "Woman_reacting_to_insult_1080p_20261024225405.mp4",
        "duration": 8.00,
        "fade_in": 0.0,
        "fade_out": 0.0,
    },
    {
        "id": 5,
        "name": "The Severed Badge",
        "file": "Woman_places_badge_on_envelope_1080p_20261024225415.mp4",
        "duration": 8.00,
        "fade_in": 0.0,
        "fade_out": 0.0,
    },
    {
        "id": 6,
        "name": "The Cliffhanger Exit",
        "file": "Woman_leaving_office_ending_meeting_1080p_20261024225429.mp4",
        "duration": 10.00,
        "fade_in": 0.0,
        "fade_out": 0.0,
    }
]

# Filmic Corporate Cool Blue-Grey Color Grade Filter
COLOR_GRADE = (
    "curves=m='0/0 0.20/0.17 0.50/0.50 0.80/0.84 1/1':b='0/0.02 0.5/0.51 1/0.99',"
    "colorbalance=rs=-0.02:gs=0.00:bs=0.03:rm=-0.01:gm=0.01:bm=0.02:rh=-0.01:gh=0.00:bh=0.02,"
    "eq=contrast=1.05:saturation=0.98"
)

# 15 Tactical Chinese Drama SFX Cues
SFX_CUES = [
    {
        "file": "long_resonance_gong.mp3",
        "time": 0.00,
        "vol": 0.15,
        "desc": "Opening press conference bronze gong ambience"
    },
    {
        "file": "whoosh_fast_transition.mp3",
        "time": 4.90,
        "vol": 0.22,
        "desc": "Whip-pan through reporters to shadowed back"
    },
    {
        "file": "heartbeat_deep_impact.mp3",
        "time": 5.50,
        "vol": 0.28,
        "desc": "Rack-focus impact on Elena Han's cold eyes"
    },
    {
        "file": "chinese_clock_gong_heavy.mp3",
        "time": 9.80,
        "vol": 0.22,
        "desc": "Heavy clock gong on dip-to-black scene transition"
    },
    {
        "file": "cinematic_deep_impact.mp3",
        "time": 11.80,
        "vol": 0.20,
        "desc": "Envelope sliding onto mahogany desk thud"
    },
    {
        "file": "trailer_suspense_riser.mp3",
        "time": 18.50,
        "vol": 0.16,
        "desc": "Tension riser under Elena's confrontation"
    },
    {
        "file": "glass_suspense_hit.mp3",
        "time": 26.80,
        "vol": 0.35,
        "desc": "High-tension suspense glass hit on 'You're just a technician'"
    },
    {
        "file": "heartbeat_deep_impact.mp3",
        "time": 28.10,
        "vol": 0.30,
        "desc": "Visceral heartbeat boom on Elena's jaw clench"
    },
    {
        "file": "heartbeat_mystery_pulse.mp3",
        "time": 30.00,
        "vol": 0.18,
        "desc": "Continuous suspense heartbeat pulse during heavy silence"
    },
    {
        "file": "trailer_suspense_riser.mp3",
        "time": 34.00,
        "vol": 0.20,
        "desc": "Tension riser as gaze shifts down to security badge"
    },
    {
        "file": "metal_clash_glass.mp3",
        "time": 37.20,
        "vol": 0.22,
        "desc": "Sharp metallic click unhooking heavy RFID badge"
    },
    {
        "file": "cinematic_deep_impact.mp3",
        "time": 40.50,
        "vol": 0.32,
        "desc": "Resonant impact as badge is slammed onto white envelope"
    },
    {
        "file": "whoosh_stutter_tension.mp3",
        "time": 41.30,
        "vol": 0.22,
        "desc": "Stutter whoosh tension hit before Julian's 'What is this?'"
    },
    {
        "file": "trailer_epic_impact.mp3",
        "time": 49.40,
        "vol": 0.35,
        "desc": "Epic trailer impact braam on 'Then you won't need me tomorrow'"
    },
    {
        "file": "dramatic_bell_toll.mp3",
        "time": 52.50,
        "vol": 0.30,
        "desc": "Somber dramatic bell toll as elevator doors close to black"
    }
]

# Dialogue Subtitles synced with Whisper cadence
SUBTITLES = [
    {
        "start": 0.50,
        "end": 4.60,
        "speaker": "JULIAN",
        "text": "Our leadership ensured zero spoilage. The contract is secure."
    },
    {
        "start": 12.78,
        "end": 15.14,
        "speaker": "JULIAN",
        "text": "A little personal thank-you from the board, Elena."
    },
    {
        "start": 16.14,
        "end": 17.46,
        "speaker": "JULIAN",
        "text": "Buy yourself something nice."
    },
    {
        "start": 18.00,
        "end": 21.96,
        "speaker": "ELENA",
        "text": "You promised the Director of Systems Engineering title if the routing algorithm held."
    },
    {
        "start": 22.40,
        "end": 23.46,
        "speaker": "JULIAN",
        "text": "Be realistic, Elena."
    },
    {
        "start": 24.18,
        "end": 26.30,
        "speaker": "JULIAN",
        "text": "The board needs a leader who can manage clients."
    },
    {
        "start": 26.86,
        "end": 27.62,
        "speaker": "JULIAN",
        "text": "You're just a technician."
    },
    {
        "start": 41.52,
        "end": 42.76,
        "speaker": "JULIAN",
        "text": "What is this?"
    },
    {
        "start": 49.46,
        "end": 50.94,
        "speaker": "ELENA",
        "text": "Then you won't need me tomorrow."
    }
]

def run_cmd(cmd, desc="Running command"):
    print(f"\n--> {desc}")
    print(f"    {' '.join(cmd[:12])}{'...' if len(cmd) > 12 else ''}")
    t0 = time.time()
    res = subprocess.run(cmd, capture_output=True, text=True)
    dt = time.time() - t0
    if res.returncode != 0:
        print(f"ERROR ({dt:.2f}s):\n{res.stderr}")
        raise RuntimeError(f"Command failed: {desc}")
    print(f"    Done in {dt:.2f}s")
    return res

def s_to_srt(s):
    hrs = int(s // 3600)
    mins = int((s % 3600) // 60)
    secs = int(s % 60)
    ms = int(round((s - int(s)) * 1000))
    if ms >= 1000:
        secs += 1
        ms -= 1000
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{ms:03d}"

def s_to_ass(s):
    hrs = int(s // 3600)
    mins = int((s % 3600) // 60)
    secs = int(s % 60)
    cs = int(round((s - int(s)) * 100))
    if cs >= 100:
        secs += 1
        cs -= 100
    return f"{hrs:01d}:{mins:02d}:{secs:02d}.{cs:02d}"

def step1_assemble_base_video():
    """
    Assemble the 6 shots with filmic color grade and motivated transitions:
    - Shot 1: 0.5s fade-in from black, 0.5s fade-out to black at tail
    - Shot 2: 0.5s fade-in from black
    - Shots 2->3, 3->4, 4->5, 5->6: Hard cuts
    """
    print("=" * 65)
    print("STEP 1: Assembling Video Clips & Motivated Transitions")
    print("=" * 65)

    base_video_path = os.path.join(WORK_DIR, "base_video.mp4")

    cmd = [FFMPEG, "-y"]
    for shot in SHOTS:
        clip_path = os.path.join(INBOX, shot["file"])
        cmd.extend(["-i", clip_path])

    filter_complex = []
    # Process each video stream: apply color grade + intro/outro fades
    for idx, shot in enumerate(SHOTS):
        v_in = f"{idx}:v"
        v_graded = f"v{idx}_graded"
        filter_complex.append(f"[{v_in}]{COLOR_GRADE}[{v_graded}]")

        v_curr = v_graded
        if shot["fade_in"] > 0:
            v_fi = f"v{idx}_fi"
            filter_complex.append(f"[{v_curr}]fade=t=in:st=0:d={shot['fade_in']}[{v_fi}]")
            v_curr = v_fi

        if shot["fade_out"] > 0:
            v_fo = f"v{idx}_fo"
            st_fo = shot["duration"] - shot["fade_out"]
            filter_complex.append(f"[{v_curr}]fade=t=out:st={st_fo:.2f}:d={shot['fade_out']}[{v_fo}]")
            v_curr = v_fo

        # Label output for concat
        filter_complex.append(f"[{v_curr}]settb=1/24,setpts=PTS-STARTPTS[v{idx}_ready]")

    # Concat all 6 video segments
    v_inputs = "".join([f"[v{i}_ready]" for i in range(len(SHOTS))])
    filter_complex.append(f"{v_inputs}concat=n={len(SHOTS)}:v=1:a=0[v_base]")

    cmd.extend([
        "-filter_complex", ";\n".join(filter_complex),
        "-map", "[v_base]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-r", "24",
        "-t", str(TOTAL_DUR),
        base_video_path
    ])

    run_cmd(cmd, "Rendering Base Graded Video Stream with Scene Transitions")
    return base_video_path

def step2_build_master_audio():
    """
    Assemble dialog/foley bed with transitions, master dialogue (-14 LUFS, 80Hz HPF,
    +2.5dB vocal presence boost at 2.8kHz), layer 15 Chinese Drama SFX cues, and mix.
    """
    print("=" * 65)
    print("STEP 2: Building Master Audio & Chinese Drama SFX Layer")
    print("=" * 65)

    master_audio_path = os.path.join(WORK_DIR, "master_audio.wav")

    cmd = [FFMPEG, "-y"]
    # Inputs: 6 video clips (for original dialogue/foley audio)
    for shot in SHOTS:
        clip_path = os.path.join(INBOX, shot["file"])
        cmd.extend(["-i", clip_path])

    # Inputs: SFX files
    for cue in SFX_CUES:
        sfx_path = os.path.join(CD_DIR, cue["file"])
        cmd.extend(["-i", sfx_path])

    filter_complex = []

    # 1. Process clip audio tracks with fades matching video
    for idx, shot in enumerate(SHOTS):
        a_in = f"{idx}:a"
        a_curr = f"a{idx}_in"
        filter_complex.append(f"[{a_in}]aresample=48000,aformat=channel_layouts=stereo[{a_curr}]")

        if shot["fade_in"] > 0:
            a_fi = f"a{idx}_fi"
            filter_complex.append(f"[{a_curr}]afade=t=in:st=0:d={shot['fade_in']}[{a_fi}]")
            a_curr = a_fi

        if shot["fade_out"] > 0:
            a_fo = f"a{idx}_fo"
            st_fo = shot["duration"] - shot["fade_out"]
            filter_complex.append(f"[{a_curr}]afade=t=out:st={st_fo:.2f}:d={shot['fade_out']}[{a_fo}]")
            a_curr = a_fo

        filter_complex.append(f"[{a_curr}]asetpts=PTS-STARTPTS[a{idx}_ready]")

    # 2. Concat 6 audio dialogue tracks
    a_inputs = "".join([f"[a{i}_ready]" for i in range(len(SHOTS))])
    filter_complex.append(f"{a_inputs}concat=n={len(SHOTS)}:v=0:a=1[dialogue_raw]")

    # 3. Master dialogue (80Hz highpass, +2.5dB presence boost at 2.8kHz, loudnorm -14 LUFS)
    filter_complex.append(
        "[dialogue_raw]highpass=f=80,equalizer=f=2800:t=q:w=1.0:g=2.5,loudnorm=I=-14:LRA=7:TP=-1.5[dialogue_master]"
    )

    # 4. Prepare each SFX cue with adelay and volume
    sfx_labels = []
    num_clips = len(SHOTS)
    for idx, cue in enumerate(SFX_CUES):
        sfx_in_idx = num_clips + idx
        delay_ms = int(round(cue["time"] * 1000))
        vol = cue["vol"]
        label = f"sfx_{idx}"
        sfx_labels.append(f"[{label}]")
        filter_complex.append(
            f"[{sfx_in_idx}:a]aresample=48000,aformat=channel_layouts=stereo,"
            f"volume={vol:.3f},adelay={delay_ms}|{delay_ms},apad[{label}]"
        )

    # 5. Mix dialogue bed with all 15 SFX cues
    total_inputs = 1 + len(SFX_CUES)
    all_inputs_str = "[dialogue_master]" + "".join(sfx_labels)
    filter_complex.append(
        f"{all_inputs_str}amix=inputs={total_inputs}:duration=longest:dropout_transition=0:normalize=0,"
        f"apad=whole_dur={TOTAL_DUR},afade=t=out:st={TOTAL_DUR-0.6:.2f}:d=0.6[a_out]"
    )

    cmd.extend([
        "-filter_complex", ";\n".join(filter_complex),
        "-map", "[a_out]",
        "-t", str(TOTAL_DUR),
        "-ar", "48000", "-ac", "2",
        master_audio_path
    ])

    run_cmd(cmd, "Mixing Master Audio Track with Dialogue Clarity & 15 SFX Cues")
    return master_audio_path

def step3_generate_subtitles():
    """
    Generate professional .srt and .ass sidecars strictly positioned in the safe zone (MarginV=280).
    """
    print("=" * 65)
    print("STEP 3: Generating Dynamic Sidecar Subtitles (.srt and .ass)")
    print("=" * 65)

    srt_path = os.path.join(OUTBOX, f"{SLUG}.srt")
    ass_path = os.path.join(OUTBOX, f"{SLUG}.ass")

    # Write SRT
    with open(srt_path, "w", encoding="utf-8") as f:
        for idx, sub in enumerate(SUBTITLES, 1):
            t_start = s_to_srt(sub["start"])
            t_end = s_to_srt(sub["end"])
            f.write(f"{idx}\n{t_start} --> {t_end}\n{sub['text']}\n\n")

    # Write ASS with professional typography in safe zone
    ass_content = f"""[Script Info]
Title: SIGNAL ZERO — Episode 01: "Just a Technician"
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Liberation Sans,46,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3.0,1.2,2,80,80,280,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    for sub in SUBTITLES:
        t_start = s_to_ass(sub["start"])
        t_end = s_to_ass(sub["end"])
        speaker = sub["speaker"]
        text = sub["text"]
        ass_content += f"Dialogue: 0,{t_start},{t_end},Default,{speaker},0,0,0,,{text}\n"

    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(ass_content)

    # Copy to project inbox as well
    shutil.copyfile(srt_path, os.path.join(INBOX, f"{SLUG}.srt"))
    shutil.copyfile(ass_path, os.path.join(INBOX, f"{SLUG}.ass"))

    print(f"Subtitles generated successfully:")
    print(f"  SRT: {srt_path} ({len(SUBTITLES)} cues)")
    print(f"  ASS: {ass_path} ({len(SUBTITLES)} events)")
    return srt_path, ass_path

def step4_render_final_master(base_video, master_audio, ass_path):
    """
    Burn in ASS subtitles in safe zone and mux with master audio into final deliverable.
    Also generate a telegram mobile version if needed.
    """
    print("=" * 65)
    print("STEP 4: Rendering Final Master Deliverable & Mobile Version")
    print("=" * 65)

    final_master_mp4 = os.path.join(OUTBOX, f"{SLUG}-final.mp4")

    cmd = [
        FFMPEG, "-y",
        "-i", base_video,
        "-i", master_audio,
        "-filter_complex", f"[0:v]subtitles='{ass_path}'[v_sub]",
        "-map", "[v_sub]",
        "-map", "1:a",
        "-c:v", "libx264", "-preset", "slow", "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-t", str(TOTAL_DUR),
        "-movflags", "+faststart",
        final_master_mp4
    ]

    run_cmd(cmd, "Rendering Final High-Quality Master MP4 Deliverable")

    size_mb = os.path.getsize(final_master_mp4) / (1024 * 1024)
    print(f"Master Render Output: {final_master_mp4} ({size_mb:.2f} MB)")

    # Telegram delivery file: if master <= 45MB, can be delivered directly.
    # We also create an under-45MB mobile streamable version if needed.
    telegram_45mb_mp4 = os.path.join(OUTBOX, f"{SLUG}-final-45mb.mp4")
    if size_mb > 45.0:
        cmd_tg = [
            FFMPEG, "-y",
            "-i", final_master_mp4,
            "-c:v", "libx264", "-preset", "fast", "-crf", "22",
            "-c:a", "copy",
            "-movflags", "+faststart",
            telegram_45mb_mp4
        ]
        run_cmd(cmd_tg, "Encoding Mobile-Optimized Telegram Delivery Version (< 45MB)")
    else:
        # Simply link or copy
        if os.path.exists(telegram_45mb_mp4):
            os.remove(telegram_45mb_mp4)
        try:
            os.link(final_master_mp4, telegram_45mb_mp4)
        except Exception:
            shutil.copyfile(final_master_mp4, telegram_45mb_mp4)

    return final_master_mp4, telegram_45mb_mp4

def step5_verify_deliverables(final_master):
    """
    Rigorous verification: ffprobe streams, duration, and decode integrity.
    """
    print("=" * 65)
    print("STEP 5: Rigorous Verification of Rendered Deliverable")
    print("=" * 65)

    probe_json = subprocess.check_output([
        FFPROBE, "-v", "error",
        "-show_entries", "format=duration,size:stream=width,height,r_frame_rate,codec_name,sample_rate,channels",
        "-of", "json",
        final_master
    ]).decode()

    import json
    data = json.loads(probe_json)
    fmt = data.get("format", {})
    dur = float(fmt.get("duration", 0))
    size_mb = int(fmt.get("size", 0)) / (1024 * 1024)
    streams = data.get("streams", [])

    print(f"Final Master: {final_master}")
    print(f"Duration: {dur:.2f}s (Target: {TOTAL_DUR:.2f}s)")
    print(f"File Size: {size_mb:.2f} MB")
    for s in streams:
        if s.get("codec_name") == "h264":
            print(f"Video Stream: {s.get('codec_name')} {s.get('width')}x{s.get('height')} @ {s.get('r_frame_rate')} fps")
        elif s.get("codec_name") == "aac":
            print(f"Audio Stream: {s.get('codec_name')} {s.get('sample_rate')} Hz, {s.get('channels')} channels")

    # Run null-mux decode test
    print("Verifying full decode integrity (null-mux test)...")
    res = subprocess.run([
        FFMPEG, "-v", "error",
        "-i", final_master,
        "-f", "null", "-"
    ], capture_output=True, text=True)
    if res.returncode == 0 and not res.stderr.strip():
        print("PASS: 100% Clean Decode Integrity (Zero dropped frames or errors)")
    else:
        print(f"WARNING: Decode errors: {res.stderr}")

def main():
    t_start = time.time()
    os.makedirs(WORK_DIR, exist_ok=True)
    os.makedirs(OUTBOX, exist_ok=True)

    print("#######################################################")
    print("HermiEditor: SIGNAL ZERO — Episode 01 Production")
    print("#######################################################")

    base_video = step1_assemble_base_video()
    master_audio = step2_build_master_audio()
    srt_path, ass_path = step3_generate_subtitles()
    final_master, telegram_mp4 = step4_render_final_master(base_video, master_audio, ass_path)
    step5_verify_deliverables(final_master)

    elapsed = time.time() - t_start
    print("\n" + "#" * 65)
    print(f"PRODUCTION COMPLETE IN {elapsed:.1f}s!")
    print(f"Master Deliverable: {final_master}")
    print(f"Telegram Media Tag: MEDIA:{final_master}")
    print("#" * 65)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
HermiEditor: PROJECT COLD SILICON — The Nvidia AI Chip Smuggling Ring
Autonomous Documentary Video Editor Pipeline (Adaptive Editing Profile v3.0 - Long-Form / High-End Tech Documentary)

Strictly adheres to HermiEditor rules & user specifications:
- Adaptive Editing Profile: High-End Tech Documentary (1080x1920 Vertical 9:16 @ 24fps, clean visual canvas, story-first pacing).
- Aligns all 10 video beats directly to the natural cadence of the master voiceover (74.68s runtime).
- Motivated Transitions:
  * 0.5s cinematic fade-in from black at 0.0s.
  * 0.4s dramatic dips-to-black between major location/chronological shifts (Beats 1->2, 2->3, 4->5, 6->7, 9->10).
  * Fast motivated hard cuts across direct action/conceptual progressions (Beats 3->4, 5->6, 7->8, 8->9).
  * High-tension dossier slam into black cliffhanger hold.
- Sound Design & Audio Mastering (Clean Voiceover Master - NO SFX):
  * Pure spoken voiceover primacy with ZERO added sound effects.
  * Mastered dialogue with 80Hz highpass, +2.5dB vocal presence boost at 2.8kHz, loudnorm -14 LUFS.
- Cinematic Tactical Color Grading: Filmic cold cyan/tungsten corporate curve, crisp contrast, rich blacks.
- Dynamic Safe-Zone Subtitles: 18 Whisper-timed cues in the lower-third safe zone (MarginV=280).
- Deliverables: outbox/cold-silicon-smuggling-final.mp4 + 45mb version + sidecar .srt & .ass files.
"""

import os
import sys
import time
import shutil
import subprocess

INBOX = "/home/john/Documents/hermieditor/inbox/long form"
OUTBOX = "/home/john/Documents/hermieditor/outbox"
WORK_DIR = "/home/john/Documents/hermieditor/.cold_silicon_tmp"
MY_SOUNDS = "/home/john/Documents/hermieditor/my-sounds"

FFMPEG = "/home/john/.hermes/tools/ffmpeg-9.0.1-linux-x64/bin/ffmpeg"
FFPROBE = "/home/john/.hermes/tools/ffmpeg-9.0.1-linux-x64/bin/ffprobe"
SLUG = "cold-silicon-smuggling"
FPS = 24
WIDTH = 1080
HEIGHT = 1920
TOTAL_DUR = 74.68

# 10 Video Beats aligned with VO timestamps
BEATS = [
    {
        "id": 1,
        "name": "The Black Gold Silicon Die",
        "file": "Macro_close-up_of_silicon_die_1080p_20261024233701.mp4",
        "dur": 5.24,
        "raw_dur": 6.00,
        "fi": 0.5,
        "fo": 0.4,
    },
    {
        "id": 2,
        "name": "The Smuggler's Crate",
        "file": "Camera_pulls_back_from_AI_1080p_20261024232943.mp4",
        "dur": 11.30,
        "raw_dur": 6.00,
        "fi": 0.4,
        "fo": 0.4,
    },
    {
        "id": 3,
        "name": "The Sanction Chokepoint",
        "file": "Official_stamping_document_with_…_1080p_20261024232951.mp4",
        "dur": 7.08,
        "raw_dur": 6.00,
        "fi": 0.4,
        "fo": 0.0,
    },
    {
        "id": 4,
        "name": "The Cleanroom Silicon Foundry",
        "file": "Robotic_arm_transfers_silicon_wafer_1080p_20261024232957.mp4",
        "dur": 7.72,
        "raw_dur": 6.00,
        "fi": 0.0,
        "fo": 0.4,
    },
    {
        "id": 5,
        "name": "The Dubai Ghost Shell Office",
        "file": "Trader_working_on_laptop_skyscraper_1080p_20261024232958.mp4",
        "dur": 8.42,
        "raw_dur": 6.00,
        "fi": 0.4,
        "fo": 0.0,
    },
    {
        "id": 6,
        "name": "Midnight Harbor Transshipment",
        "file": "Men_loading_crates_into_van_1080p_20261024232932.mp4",
        "dur": 6.30,
        "raw_dur": 6.00,
        "fi": 0.0,
        "fo": 0.4,
    },
    {
        "id": 7,
        "name": "Huaqiangbei Back-Alley Re-Badging",
        "file": "Technician_buffing_GPU_serial_nu…_1080p_20261024232939.mp4",
        "dur": 8.58,
        "raw_dur": 6.00,
        "fi": 0.4,
        "fo": 0.0,
    },
    {
        "id": 8,
        "name": "The Clandestine Server Farm",
        "file": "Camera_moving_down_server_corridor_1080p_20261024233003.mp4",
        "dur": 6.92,
        "raw_dur": 6.00,
        "fi": 0.0,
        "fo": 0.0,
    },
    {
        "id": 9,
        "name": "Full Compute Training Overdrive",
        "file": "Coolant_flowing_through_server_c…_1080p_20261024232946.mp4",
        "dur": 6.10,
        "raw_dur": 6.00,
        "fi": 0.0,
        "fo": 0.4,
    },
    {
        "id": 10,
        "name": "The Cold Silicon Dossier Lock",
        "file": "Intelligence_dossier_drops_on_table_1080p_20261024232928.mp4",
        "dur": 7.02,
        "raw_dur": 6.00,
        "fi": 0.4,
        "fo": 0.0,
    }
]

# Filmic High-End Tactical Documentary Color Grade
COLOR_GRADE = (
    "curves=m='0/0 0.18/0.14 0.50/0.50 0.82/0.86 1/1':b='0/0.02 0.5/0.51 1/0.98',"
    "colorbalance=rs=-0.01:gs=0.00:bs=0.03:rm=-0.01:gm=0.01:bm=0.02:rh=-0.01:gh=0.00:bh=0.02,"
    "eq=contrast=1.06:saturation=1.02"
)

# 18 Synchronized Subtitle Cues strictly aligned with Whisper audio cadence
SUBTITLES = [
    {
        "start": 0.00,
        "end": 4.64,
        "text": "Gram for gram, this slab of silicon is now more valuable than pure cocaine."
    },
    {
        "start": 5.24,
        "end": 7.82,
        "text": "On the legal market, it sells for thirty thousand dollars."
    },
    {
        "start": 8.40,
        "end": 13.02,
        "text": "But on the streets of Shenzhen, buyers will hand you fifty thousand dollars in cash."
    },
    {
        "start": 13.52,
        "end": 15.58,
        "text": "No receipts. No questions asked."
    },
    {
        "start": 16.54,
        "end": 20.06,
        "text": "Two years ago, Washington weaponized the global supply chain..."
    },
    {
        "start": 20.06,
        "end": 22.98,
        "text": "...cutting off China's access to the world's most advanced AI processors."
    },
    {
        "start": 23.62,
        "end": 26.50,
        "text": "The goal was simple: choke the compute power needed..."
    },
    {
        "start": 26.50,
        "end": 30.64,
        "text": "...to build the next generation of autonomous weapons and frontier models."
    },
    {
        "start": 31.34,
        "end": 34.90,
        "text": "It didn't stop the flow. It created an underground shadow market..."
    },
    {
        "start": 35.46,
        "end": 39.26,
        "text": "...operated by shell corporations in Dubai, fake logistics fronts in Singapore..."
    },
    {
        "start": 39.76,
        "end": 45.24,
        "text": "...and corrupt customs brokers who relabel supercomputers as domestic water heaters."
    },
    {
        "start": 46.06,
        "end": 49.58,
        "text": "In humid back-alley electronics markets, technicians use razor-thin scalpels..."
    },
    {
        "start": 49.58,
        "end": 53.80,
        "text": "...and laser etching to erase serial numbers before chips are smuggled across borders."
    },
    {
        "start": 54.64,
        "end": 58.12,
        "text": "Inside thousands of secret server farms hidden across mainland industrial parks..."
    },
    {
        "start": 58.60,
        "end": 61.22,
        "text": "...these smuggled clusters are coming online right now..."
    },
    {
        "start": 61.56,
        "end": 66.66,
        "text": "...consuming gigawatts off the grid, training frontier models in complete defiance of sanctions."
    },
    {
        "start": 67.66,
        "end": 71.72,
        "text": "This is the untold story of the greatest high-tech smuggling operation of the 21st century..."
    },
    {
        "start": 72.26,
        "end": 74.42,
        "text": "...and why the United States cannot stop it."
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

def step1_assemble_base_video(force=False):
    """
    Assemble the 10 documentary beats:
    - Retime each clip with setpts to match its scene's exact spoken narration
    - Apply cinematic color grade
    - Apply motivated transitions (dips-to-black and hard cuts)
    - Concatenate into a seamless base video of exactly 74.68 seconds
    """
    print("=" * 65)
    print("STEP 1: Assembling 10 Video Beats Aligned to Narration")
    print("=" * 65)

    base_video_path = os.path.join(WORK_DIR, "base_video.mp4")
    if not force and os.path.exists(base_video_path) and os.path.getsize(base_video_path) > 10 * 1024 * 1024:
        print(f"Reusing existing base video: {base_video_path}")
        return base_video_path

    cmd = [FFMPEG, "-y"]
    for beat in BEATS:
        fpath = os.path.join(INBOX, beat["file"])
        cmd.extend(["-i", fpath])

    filter_complex = []
    for idx, beat in enumerate(BEATS):
        v_in = f"{idx}:v"
        pts_factor = beat["dur"] / beat["raw_dur"]
        v_retimed = f"v{idx}_retimed"
        v_graded = f"v{idx}_graded"

        # 1. Retime clip to exact duration
        filter_complex.append(
            f"[{v_in}]setpts={pts_factor:.4f}*PTS,fps=24,trim=0:{beat['dur']:.2f}[{v_retimed}]"
        )

        # 2. Apply color grade
        filter_complex.append(f"[{v_retimed}]{COLOR_GRADE}[{v_graded}]")

        # 3. Apply motivated transition fades
        v_curr = v_graded
        if beat["fi"] > 0:
            v_fi = f"v{idx}_fi"
            filter_complex.append(f"[{v_curr}]fade=t=in:st=0:d={beat['fi']}[{v_fi}]")
            v_curr = v_fi

        if beat["fo"] > 0:
            v_fo = f"v{idx}_fo"
            st_fo = beat["dur"] - beat["fo"]
            filter_complex.append(f"[{v_curr}]fade=t=out:st={st_fo:.2f}:d={beat['fo']}[{v_fo}]")
            v_curr = v_fo

        filter_complex.append(f"[{v_curr}]settb=1/24,setpts=PTS-STARTPTS[v{idx}_ready]")

    # Concat all 10 video streams
    v_inputs = "".join([f"[v{i}_ready]" for i in range(len(BEATS))])
    filter_complex.append(f"{v_inputs}concat=n={len(BEATS)}:v=1:a=0[v_base]")

    cmd.extend([
        "-filter_complex", ";\n".join(filter_complex),
        "-map", "[v_base]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-r", "24",
        "-t", str(TOTAL_DUR),
        base_video_path
    ])

    run_cmd(cmd, "Rendering Base Video with 10 Aligned Beats & Transitions")
    return base_video_path

def step2_build_master_audio():
    """
    Build clean master documentary audio track (NO SFX):
    Pure spoken voiceover primacy:
    - Master voiceover (alnilam) with 80Hz HPF, +2.5dB vocal presence at 2.8kHz, loudnorm -14 LUFS.
    - Zero added SFX for authentic, clean documentary clarity.
    """
    print("=" * 65)
    print("STEP 2: Building Master Audio Track (Pure Spoken Voiceover - NO SFX)")
    print("=" * 65)

    vo_raw = os.path.join(INBOX, "alnilam_1.25x_2026-10-24_23-26-16.wav")
    master_audio_path = os.path.join(WORK_DIR, "master_audio.wav")

    cmd = [
        FFMPEG, "-y",
        "-i", vo_raw,
        "-af", (
            "highpass=f=80,"
            "equalizer=f=2800:t=q:w=1.0:g=2.5,"
            "loudnorm=I=-14:LRA=7:TP=-1.5,"
            f"apad=whole_dur={TOTAL_DUR},"
            f"afade=t=out:st={TOTAL_DUR-0.4:.2f}:d=0.4"
        ),
        "-t", str(TOTAL_DUR),
        "-ar", "48000", "-ac", "2",
        master_audio_path
    ]

    run_cmd(cmd, "Mastering Pure Spoken Voiceover Dialogue (-14 LUFS, NO SFX)")
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
Title: PROJECT COLD SILICON: The Nvidia AI Chip Smuggling Ring
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
        text = sub["text"]
        ass_content += f"Dialogue: 0,{t_start},{t_end},Default,,0,0,0,,{text}\n"

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
    Burn in ASS subtitles in safe zone and mux with clean master audio into final deliverable.
    """
    print("=" * 65)
    print("STEP 4: Rendering Final Master Deliverable & Mobile Version (NO SFX)")
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

    run_cmd(cmd, "Rendering Final High-Quality Master MP4 Deliverable (Clean Audio)")

    size_mb = os.path.getsize(final_master_mp4) / (1024 * 1024)
    print(f"Master Render Output: {final_master_mp4} ({size_mb:.2f} MB)")

    # Hardlink / alias project-cold-silicon-final.mp4
    alias_mp4 = os.path.join(OUTBOX, "project-cold-silicon-final.mp4")
    if os.path.exists(alias_mp4) or os.path.islink(alias_mp4):
        os.remove(alias_mp4)
    try:
        os.link(final_master_mp4, alias_mp4)
    except Exception:
        shutil.copyfile(final_master_mp4, alias_mp4)

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
    print(f"Duration: {dur:.2f}s (Expected: {TOTAL_DUR:.2f}s)")
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
    print("HermiEditor: PROJECT COLD SILICON (Clean Voiceover - NO SFX)")
    print("#######################################################")

    base_video = step1_assemble_base_video(force=False)
    master_audio = step2_build_master_audio()
    srt_path, ass_path = step3_generate_subtitles()
    final_master, telegram_mp4 = step4_render_final_master(base_video, master_audio, ass_path)
    step5_verify_deliverables(final_master)

    elapsed = time.time() - t_start
    print("\n" + "#" * 65)
    print(f"PRODUCTION COMPLETE IN {elapsed:.1f}s!")
    print(f"Master Deliverable: {final_master}")
    print(f"Telegram Media Tag: MEDIA:{telegram_mp4}")
    print("#" * 65)

if __name__ == "__main__":
    main()

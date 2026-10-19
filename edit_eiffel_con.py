#!/usr/bin/env python3
"""
HermiEditor: Victor Lustig Eiffel Tower Con - Explainer Video Assembly Pipeline
Adheres strictly to HermiEditor rules:
- Clean visuals: No pop-up cards or overlays on papercraft animations
- Still image held at the very END for 0.20s (at least 0.1-0.2s hold)
- Exact 30fps frame-accurate cuts (no rounding drift)
- Word-level active gold tracking captions in safe zone
- Mastered voiceover (-14 LUFS) + original clip foley audio bed
- Deliverables: final, v1, under20mb, hq-48mb, .ass, .srt
"""

import os
import sys
import json
import time
import subprocess

INBOX = "/home/john/Documents/hermieditor/inbox/Eifel"
OUTBOX = "/home/john/Documents/hermieditor/outbox"
MY_SOUNDS = "/home/john/Documents/hermieditor/my-sounds"
WORK_DIR = "/home/john/Documents/hermieditor/.eiffel_tmp"

SLUG = "eiffel-tower-con"
FPS = 30
WIDTH = 1080
HEIGHT = 1920

# Timeline Definitions (Frame-accurate at 30fps)
# User rule: "the image should be at least 0.1-0.2 second at the end of the video. Remember this."
END_IMAGE_FRAMES = 6  # 6 frames = exactly 0.20s
END_IMAGE_DUR = END_IMAGE_FRAMES / FPS  # 0.200s
END_IMAGE_FILE = "Paper_Eiffel_Tower_and_figure_2K_20261019170100.jpg"

BEATS = [
    {
        "clip": "Paper_Eiffel_Tower_pops_up_20261019170701.mp4",
        "frames": 186,  # 6.20s
        "desc": "Beat 1: 1925 Eiffel Tower rusting & Paris budget crisis"
    },
    {
        "clip": "Papercut_figure_unrolling_vintag…_1080p_20261019170713.mp4",
        "frames": 156,  # 5.20s
        "desc": "Beat 2: Reading newspaper, Victor Lustig sees opportunity"
    },
    {
        "clip": "Man_sliding_envelopes_across_table_20261019170702.mp4",
        "frames": 207,  # 6.90s
        "desc": "Beat 3: Posing as official in luxury suite summoning dealers"
    },
    {
        "clip": "Paper_Eiffel_Tower_blueprint_unr…_20261019170708.mp4",
        "frames": 162,  # 5.40s
        "desc": "Beat 4: State secret - Eiffel Tower demolition and scrap"
    },
    {
        "clip": "Paper_businessman_slides_confide…_1080p_20261019170653.mp4",
        "frames": 270,  # 9.00s
        "desc": "Beat 5: Dealer pays $50,000 cash bribe to secure winning bid"
    },
    {
        "clip": "Miniature_train_moves_across_map_20261019170658.mp4",
        "frames": 138,  # 4.60s
        "desc": "Beat 6: Lustig packs suitcase and flees to Vienna by train"
    },
    {
        "clip": "Paper_silhouette_sitting_at_desk_20261019170655.mp4",
        "frames": 114,  # 3.80s
        "desc": "Beat 7: Victim humiliated, never reported to police"
    },
    {
        "clip": "Man_tipping_fedora_in_stop-motion_20261019170648.mp4",
        "frames": 132,  # 4.40s
        "desc": "Beat 8: Months later, Lustig returns to Paris to sell it again"
    }
]

for b in BEATS:
    b["dur"] = round(b["frames"] / FPS, 4)

CLIPS_FRAMES = sum(b["frames"] for b in BEATS)  # 1365 frames = 45.50s
TOTAL_VIDEO_FRAMES = CLIPS_FRAMES + END_IMAGE_FRAMES  # 1371 frames = 45.70s
TOTAL_DURATION = round(TOTAL_VIDEO_FRAMES / FPS, 4)  # 45.7000s
CLIPS_DURATION = round(CLIPS_FRAMES / FPS, 4)  # 45.5000s

def run_cmd(cmd, desc=""):
    print(f"\n>>> [START] {desc}")
    t0 = time.time()
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"FAILED: {desc}\nSTDOUT:\n{res.stdout}\nSTDERR:\n{res.stderr}")
        raise RuntimeError(f"Command failed: {desc}")
    print(f"<<< [DONE] {desc} ({time.time() - t0:.1f}s)")
    return res

def step1_assemble_base_video():
    """
    Assemble the 8 video clips with preserved foley audio,
    followed by the 0.20s still image hold at the very END.
    """
    os.makedirs(WORK_DIR, exist_ok=True)
    os.makedirs(OUTBOX, exist_ok=True)
    rendered_parts = []

    # 1. Render each video beat with foley audio preserved using exact frame counts
    for idx, b in enumerate(BEATS):
        clip_path = os.path.join(INBOX, b["clip"])
        out_part = os.path.join(WORK_DIR, f"part_{idx+1}.mp4")

        vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30"
        af = "highpass=f=60,volume=1.0"

        cmd = [
            "ffmpeg", "-y",
            "-ss", "0.0",
            "-i", clip_path,
            "-vframes", str(b["frames"]),
            "-vf", vf,
            "-af", af,
            "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
            out_part
        ]
        run_cmd(cmd, f"Rendering Beat {idx+1} ({b['frames']} frames, {b['dur']}s): {b['desc']}")
        rendered_parts.append(out_part)

    # 2. Render end image frame (exact 6 frames = 0.20s hold at the very END)
    end_img_path = os.path.join(INBOX, END_IMAGE_FILE)
    end_part = os.path.join(WORK_DIR, f"part_{len(BEATS)+1}_end_img.mp4")

    cmd_end_img = [
        "ffmpeg", "-y",
        "-loop", "1", "-framerate", str(FPS),
        "-i", end_img_path,
        "-f", "lavfi", "-t", str(END_IMAGE_DUR), "-i", "anullsrc=r=48000:cl=stereo",
        "-vframes", str(END_IMAGE_FRAMES),
        "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30",
        "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        end_part
    ]
    run_cmd(cmd_end_img, f"Rendering {END_IMAGE_DUR}s still image hold at the END ({END_IMAGE_FRAMES} frames)")
    rendered_parts.append(end_part)

    # Concat all parts (Beats 1-8 + End Image)
    concat_txt = os.path.join(WORK_DIR, "concat_parts.txt")
    with open(concat_txt, "w") as f:
        for p in rendered_parts:
            f.write(f"file '{p}'\n")

    base_video = os.path.join(WORK_DIR, "base_assembled.mp4")
    run_cmd([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_txt,
        "-c", "copy",
        base_video
    ], "Concatenating all base video parts with end image hold")

    return base_video

def step2_build_master_audio(base_video):
    """
    Master audio: Voiceover (-14 LUFS) + original video foley audio bed.
    Pad to total duration (45.70s) and apply clean end fade out.
    """
    vo_raw = os.path.join(INBOX, "iapetus_1.25x_2026-10-19_16-50-57.wav")
    master_audio = os.path.join(WORK_DIR, "master_audio.wav")

    # Extract original foley audio bed from base_video
    orig_audio = os.path.join(WORK_DIR, "original_audio_bed.wav")
    run_cmd([
        "ffmpeg", "-y",
        "-i", base_video,
        "-vn",
        "-af", "volume=1.0,equalizer=f=300:t=q:w=1.0:g=1.5",
        "-ar", "48000", "-ac", "2",
        orig_audio
    ], "Extracting original video foley audio bed")

    cmd = [
        "ffmpeg", "-y",
        "-i", orig_audio,
        "-i", vo_raw,
        "-filter_complex",
        (
            "[1:a]highpass=f=80,equalizer=f=2800:t=q:w=1.0:g=2.5,loudnorm=I=-14:LRA=7:TP=-1.5[vo];"
            "[0:a]volume=0.9[orig];"
            "[orig][vo]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,"
            f"apad=whole_dur={TOTAL_DURATION},afade=t=out:st={TOTAL_DURATION-0.10:.2f}:d=0.10[aout]"
        ),
        "-map", "[aout]",
        "-t", str(TOTAL_DURATION),
        "-ar", "48000", "-ac", "2",
        master_audio
    ]

    run_cmd(cmd, "Mixing Master Audio (VO + Original Foley Bed with End Fade)")
    return master_audio

def step3_generate_subtitles():
    """
    Generate dynamic word-by-word active tracking .ass and .srt subtitles.
    Vibrant gold active word pop (#FFD700) on Liberation Sans Bold in safe zone.
    """
    with open(os.path.join(INBOX, "transcript_raw.json")) as f:
        words = json.load(f)

    # Clean splits like '$50' + ',000' -> '$50,000'
    cleaned_words = []
    skip = False
    for i in range(len(words)):
        if skip:
            skip = False
            continue
        w = words[i]
        txt = w["text"]
        if i + 1 < len(words) and words[i+1]["text"].startswith(","):
            merged_text = txt + words[i+1]["text"]
            cleaned_words.append({
                "text": merged_text,
                "start": w["start"],
                "end": words[i+1]["end"]
            })
            skip = True
        else:
            cleaned_words.append(w)

    # Split into clean balanced chunks (3-4 words per line, clause aware)
    sentences = []
    curr_s = []
    for w in cleaned_words:
        curr_s.append(w)
        if w["text"].endswith((".", "!", "?")):
            sentences.append(curr_s)
            curr_s = []
    if curr_s:
        sentences.append(curr_s)

    chunks = []
    for s in sentences:
        n = len(s)
        if n <= 5:
            chunks.append(s)
        else:
            k = (n + 3) // 4
            base = n // k
            rem = n % k
            idx = 0
            for part in range(k):
                size = base + (1 if part < rem else 0)
                chunks.append(s[idx:idx+size])
                idx += size

    # Build ASS
    ass_header = """[Script Info]
Title: Victor Lustig Eiffel Tower Con Captions
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Liberation Sans,58,&H00FFFFFF,&H0000D7FF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,4.5,2.5,2,60,60,300,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ass_events = []
    for ch in chunks:
        ch_start = ch[0]["start"]
        ch_end = ch[-1]["end"]
        for active_idx, target_w in enumerate(ch):
            w_st = target_w["start"]
            w_et = target_w["end"]
            line_parts = []
            for j, w in enumerate(ch):
                txt = w["text"]
                if j == active_idx:
                    line_parts.append(f"{{\\c&H0000D7FF\\fscx108\\fscy108}}{txt}{{\\r}}")
                else:
                    line_parts.append(txt)
            text_str = " ".join(line_parts)

            st_fmt = format_ass_time(w_st)
            et_fmt = format_ass_time(w_et)
            ass_events.append(f"Dialogue: 0,{st_fmt},{et_fmt},Default,,0,0,0,,{text_str}")

    ass_content = ass_header + "\n".join(ass_events) + "\n"

    # Build SRT
    srt_lines = []
    for idx, ch in enumerate(chunks, 1):
        st_fmt = format_srt_time(ch[0]["start"])
        et_fmt = format_srt_time(ch[-1]["end"])
        txt = " ".join(w["text"] for w in ch)
        srt_lines.append(f"{idx}\n{st_fmt} --> {et_fmt}\n{txt}\n")
    srt_content = "\n".join(srt_lines)

    ass_inbox = os.path.join(INBOX, f"{SLUG}.ass")
    ass_outbox = os.path.join(OUTBOX, f"{SLUG}.ass")
    srt_inbox = os.path.join(INBOX, f"{SLUG}.srt")
    srt_outbox = os.path.join(OUTBOX, f"{SLUG}.srt")

    for p in [ass_inbox, ass_outbox]:
        with open(p, "w") as f:
            f.write(ass_content)
    for p in [srt_inbox, srt_outbox]:
        with open(p, "w") as f:
            f.write(srt_content)

    print(f"Subtitles written to:\n - {ass_inbox}\n - {ass_outbox}\n - {srt_inbox}\n - {srt_outbox}")
    return ass_outbox

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

def step4_composite_master_and_tiers(base_video, master_audio, ass_path):
    """
    Composite final deliverables (ONLY 1 video as requested: the final master):
    1. eiffel-tower-con-final.mp4 (Master 1080x1920 with explicit -map 0:v and -map 1:a for voiceover)
    """
    master_final = os.path.join(OUTBOX, f"{SLUG}-final.mp4")

    # Clean up any obsolete previous tier files
    for old_name in [
        f"{SLUG}-v1.mp4", f"{SLUG}-hq-48mb.mp4", f"{SLUG}-under20mb.mp4",
        "eifel-v1.mp4", "eifel-hq-48mb.mp4", "eifel-under20mb.mp4"
    ]:
        old_path = os.path.join(OUTBOX, old_name)
        if os.path.exists(old_path):
            os.remove(old_path)

    # Master final: Explicitly map video from 0:v and mixed voiceover audio from 1:a
    cmd_master = [
        "ffmpeg", "-y",
        "-i", base_video,
        "-i", master_audio,
        "-vf", f"ass={ass_path}",
        "-map", "0:v",
        "-map", "1:a",
        "-c:v", "libx264", "-preset", "medium", "-crf", "17",
        "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        "-vframes", str(TOTAL_VIDEO_FRAMES),
        master_final
    ]
    run_cmd(cmd_master, "Compositing Master Final with Subtitles & Voiceover Master Audio")

    # Also provide eifel-final.mp4 alias
    eifel_final = os.path.join(OUTBOX, "eifel-final.mp4")
    if os.path.exists(eifel_final):
        os.remove(eifel_final)
    os.link(master_final, eifel_final)

    return master_final

def step5_verify(master_final):
    """
    Verify output using ffprobe: duration, resolution, size, audio levels, and last frame.
    """
    print("\n" + "="*60)
    print("VERIFICATION AUDIT:")
    print("="*60)

    for p in [master_final]:
        sz_mb = os.path.getsize(p) / (1024 * 1024)
        res = subprocess.run([
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration,size:stream=width,height,r_frame_rate,codec_name",
            "-of", "json", p
        ], capture_output=True, text=True)
        data = json.loads(res.stdout)
        dur = float(data["format"]["duration"])
        streams = data.get("streams", [])
        v_stream = next((s for s in streams if s["codec_name"] == "h264"), {})
        w = v_stream.get("width")
        h = v_stream.get("height")
        fps = v_stream.get("r_frame_rate")
        print(f"File: {os.path.basename(p)}")
        print(f"  Size: {sz_mb:.2f} MB")
        print(f"  Duration: {dur:.2f}s (Expected: {TOTAL_DURATION}s)")
        print(f"  Resolution: {w}x{h} @ {fps} fps")

        # Verify audio loudness contains voiceover
        vol_res = subprocess.run([
            "ffmpeg", "-i", p, "-ss", "2.0", "-t", "5.0", "-af", "volumedetect", "-f", "null", "-"
        ], capture_output=True, text=True)
        for line in vol_res.stderr.splitlines():
            if "mean_volume" in line or "max_volume" in line:
                print(f"  Audio {line.strip()}")

    # Extract frame at TOTAL_DURATION - 0.08s (during the 0.20s end image hold)
    end_check_frame = "/tmp/eifel_end_frame_audit.jpg"
    subprocess.run([
        "ffmpeg", "-y",
        "-ss", str(TOTAL_DURATION - 0.08),
        "-i", master_final,
        "-frames:v", "1",
        end_check_frame
    ], capture_output=True)
    print(f"\nExtracted end-hold frame to {end_check_frame} for audit.")

def main():
    print("="*60)
    print(f"Starting HermiEditor Pipeline for: {SLUG}")
    print(f"Clips Duration: {CLIPS_DURATION:.2f}s | End Image Duration: {END_IMAGE_DUR:.2f}s | Total: {TOTAL_DURATION:.2f}s")
    print(f"Total frames: {TOTAL_VIDEO_FRAMES} (Clips: {sum(b['frames'] for b in BEATS)}, End Image: {END_IMAGE_FRAMES})")
    print("="*60)

    base_video = step1_assemble_base_video()
    master_audio = step2_build_master_audio(base_video)
    ass_path = step3_generate_subtitles()
    master_final = step4_composite_master_and_tiers(base_video, master_audio, ass_path)
    step5_verify(master_final)

    print("\n" + "="*60)
    print("HermiEditor Pipeline Complete!")
    print("="*60)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
HermiEditor: Emperor Napoleon III & The Aluminum Prestige Con/Explainer Pipeline
Adheres strictly to HermiEditor rules:
- Explainer discipline: Clean visuals, no unsolicited pop-up cards or overlays on papercraft animation.
- End-image hold rule: Still image held at the very END for 0.20s (6 frames @ 30fps).
- Flaw mitigation: Scene change detection / trim frame 0 AI reference image flash on utensils clip (-ss 0.05).
- Exact 30fps frame-accurate cuts (no rounding drift).
- Word-level active gold tracking captions (\c&H0000D7FF\fscx108\fscy108) in safe zone.
- Mastered voiceover (-14 LUFS, 80Hz highpass, +2.5dB at 2.8kHz) + original clip foley audio bed.
- Deliverables: final master (1080x1920 CRF 17), .ass, .srt in both inbox and outbox.
"""

import os
import sys
import json
import time
import subprocess

INBOX = "/home/john/Documents/hermieditor/inbox/napoleon"
OUTBOX = "/home/john/Documents/hermieditor/outbox"
MY_SOUNDS = "/home/john/Documents/hermieditor/my-sounds"
WORK_DIR = "/home/john/Documents/hermieditor/.napoleon_tmp"

SLUG = "napoleon-aluminum"
FPS = 30
WIDTH = 1080
HEIGHT = 1920

# Timeline Definitions (Frame-accurate at 30fps)
# Still image held at the very END for 0.20s (6 frames)
END_IMAGE_FRAMES = 6
END_IMAGE_DUR = END_IMAGE_FRAMES / FPS  # 0.200s
END_IMAGE_FILE = "Papercraft_fork_on_red_pedestal_2K_20261019182646.jpg"

BEATS = [
    {
        "clip": "Paper_book_opens_on_desk_20261019182834.mp4",
        "ss": "0.0",
        "frames": 193,  # 6.433s (0.00s -> 6.433s)
        "desc": "Beat 1: In the 1850s, Emperor Napoleon III hosted Europe's royal elites at lavish banquets."
    },
    {
        "clip": "Kings_eating_at_paper_table_20261019182848.mp4",
        "ss": "0.0",
        "frames": 224,  # 7.467s (6.433s -> 13.900s)
        "desc": "Beat 2: Kings and princes ate from plates of solid gold, but emperor dined with something far more prestigious."
    },
    {
        "clip": "Paper_utensils_on_pedestal_scale_20261019182838.mp4",
        "ss": "0.05",  # Pre-trim 1-frame AI reference image flash at pts 0
        "frames": 209,  # 6.967s (13.900s -> 20.867s)
        "desc": "Beat 3: Aluminum forks and spoons. At the time, rarer and more expensive than gold or silver."
    },
    {
        "clip": "Paper_animation_geological_cross…_1080p_20261019182823.mp4",
        "ss": "0.0",
        "frames": 184,  # 6.133s (20.867s -> 27.000s)
        "desc": "Beat 4: Extracting pure aluminum from raw bauxite clay was an excruciating microscopic nightmare."
    },
    {
        "clip": "Papercraft_French_imperial_nurse…_1080p_20261019182910.mp4",
        "ss": "0.0",
        "frames": 233,  # 7.767s (27.000s -> 34.767s)
        "desc": "Beat 5: Napoleon commissioned an aluminum baby rattle and carriage, flexing supreme imperial wealth."
    },
    {
        "clip": "Chemists_demonstrate_paper_smelt…_1080p_20261019182844.mp4",
        "ss": "0.0",
        "frames": 233,  # 7.767s (34.767s -> 42.533s)
        "desc": "Beat 6: In 1886, two independent chemists discovered modern electrolysis, unlocking industrial smelting."
    },
    {
        "clip": "Paper_price_chart_crashing_downward_20261019182936.mp4",
        "ss": "0.0",
        "frames": 170,  # 5.667s (42.533s -> 48.200s)
        "desc": "Beat 7: Virtually overnight, the price of aluminum crashed from thousands of dollars per kilo to mere pennies."
    },
    {
        "clip": "Paper_banquet_hall_transforms_in…_20261019182854.mp4",
        "ss": "0.0",
        "frames": 230,  # 7.667s (48.200s -> 55.867s)
        "desc": "Beat 8: The ultimate status symbol became disposable kitchen foil. Value is never permanent. Only scarcity is."
    }
]

for b in BEATS:
    b["dur"] = round(b["frames"] / FPS, 4)

CLIPS_FRAMES = sum(b["frames"] for b in BEATS)  # 1676 frames = 55.867s
TOTAL_VIDEO_FRAMES = CLIPS_FRAMES + END_IMAGE_FRAMES  # 1682 frames = 56.067s
TOTAL_DURATION = round(TOTAL_VIDEO_FRAMES / FPS, 4)  # 56.0667s
CLIPS_DURATION = round(CLIPS_FRAMES / FPS, 4)  # 55.8667s

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
            "-ss", b["ss"],
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
    Master audio: Voiceover (-14 LUFS, 80Hz highpass, +2.5dB at 2.8kHz) + original video foley audio bed.
    Pad to total duration (56.07s) and apply clean end fade out.
    """
    vo_raw = os.path.join(INBOX, "iapetus_1.25x_2026-10-19_18-21-35.wav")
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
    transcript_file = os.path.join(INBOX, "iapetus_1.25x_2026-10-19_18-21-35.json")
    with open(transcript_file) as f:
        words = json.load(f)["words"]

    # Clean words and clamp any timestamps beyond speech end
    cleaned_words = []
    for w in words:
        start_t = round(w["start"], 2)
        end_t = min(round(w["end"], 2), CLIPS_DURATION)
        if end_t > start_t:
            cleaned_words.append({
                "text": w["text"].strip(),
                "start": start_t,
                "end": end_t
            })

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
Title: Napoleon III Aluminum Explainer Captions
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

    # Also provide napoleon.ass/srt aliases
    alias_ass_inbox = os.path.join(INBOX, "napoleon.ass")
    alias_ass_outbox = os.path.join(OUTBOX, "napoleon.ass")
    alias_srt_inbox = os.path.join(INBOX, "napoleon.srt")
    alias_srt_outbox = os.path.join(OUTBOX, "napoleon.srt")

    for p in [ass_inbox, ass_outbox, alias_ass_inbox, alias_ass_outbox]:
        with open(p, "w") as f:
            f.write(ass_content)
    for p in [srt_inbox, srt_outbox, alias_srt_inbox, alias_srt_outbox]:
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

def step4_composite_master(base_video, master_audio, ass_path):
    """
    Composite final deliverables (Single video master):
    1. napoleon-aluminum-final.mp4 (Master 1080x1920 with explicit -map 0:v and -map 1:a)
    2. napoleon-final.mp4 (hardlinked alias)
    """
    master_final = os.path.join(OUTBOX, f"{SLUG}-final.mp4")

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

    # Also provide napoleon-final.mp4 alias
    alias_final = os.path.join(OUTBOX, "napoleon-final.mp4")
    if os.path.exists(alias_final):
        os.remove(alias_final)
    os.link(master_final, alias_final)

    return master_final

def step5_verify(master_final):
    """
    Verify output using ffprobe: duration, resolution, size, audio levels, and last frame.
    """
    print("\n" + "="*60)
    print("VERIFICATION AUDIT:")
    print("="*60)

    sz_mb = os.path.getsize(master_final) / (1024 * 1024)
    res = subprocess.run([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration,size:stream=width,height,r_frame_rate,codec_name",
        "-of", "json", master_final
    ], capture_output=True, text=True)
    data = json.loads(res.stdout)
    dur = float(data["format"]["duration"])
    streams = data.get("streams", [])
    v_stream = next((s for s in streams if s["codec_name"] == "h264"), {})
    w = v_stream.get("width")
    h = v_stream.get("height")
    fps = v_stream.get("r_frame_rate")
    print(f"File: {os.path.basename(master_final)}")
    print(f"  Size: {sz_mb:.2f} MB")
    print(f"  Duration: {dur:.2f}s (Expected: {TOTAL_DURATION}s)")
    print(f"  Resolution: {w}x{h} @ {fps} fps")

    # Verify audio loudness contains voiceover
    vol_res = subprocess.run([
        "ffmpeg", "-i", master_final, "-ss", "2.0", "-t", "5.0", "-af", "volumedetect", "-f", "null", "-"
    ], capture_output=True, text=True)
    for line in vol_res.stderr.splitlines():
        if "mean_volume" in line or "max_volume" in line:
            print(f"  Audio {line.strip()}")

    # Extract frame during the 0.20s end image hold for visual audit
    end_check_frame = "/tmp/napoleon_end_frame_audit.jpg"
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
    master_final = step4_composite_master(base_video, master_audio, ass_path)
    step5_verify(master_final)

    print("\n" + "="*60)
    print("HermiEditor Pipeline Complete!")
    print("="*60)

if __name__ == "__main__":
    main()

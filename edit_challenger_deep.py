#!/usr/bin/env python3
"""
HermiEditor: Challenger Deep Video Assembly & Motion Graphics Pipeline
Created for Hermes Agent pair programming.
"""

import os
import sys
import json
import time
import subprocess

INBOX = "/home/john/Documents/hermieditor/inbox/Challenger deep"
OUTBOX = "/home/john/Documents/hermieditor/outbox"
MY_SOUNDS = "/home/john/Documents/hermieditor/my-sounds"
WORK_DIR = "/home/john/Documents/hermieditor/.challenger_deep_tmp"

SLUG = "challenger-deep"
FPS = 30
WIDTH = 1080
HEIGHT = 1920

# 1. Timeline Definitions
# Note: 0.20s thumbnail at start
THUMBNAIL_DUR = 0.20

BEATS = [
    {
        "clip": "Paper_Everest_descending_into_tr…_20261018152456.mp4",
        "dur": 5.40,
        "card_id": "card1",
        "card_st": 1.20,
        "card_et": 4.80,
    },
    {
        "clip": "Pop-up_book_reveals_Mariana_Trench_20261018152529.mp4",
        "dur": 6.90,
        "card_id": "card2",
        "card_st": 6.60,
        "card_et": 11.40,
    },
    {
        "clip": "Paper_tectonic_display_showing_s…_20261018152807.mp4",
        "dur": 5.70,
        "card_id": "card3",
        "card_st": 13.20,
        "card_et": 17.40,
    },
    {
        "clip": "Paper_submersible_descending_oce…_1080p_20261018152458.mp4",
        "dur": 7.10,
        "card_id": "card4",
        "card_st": 19.20,
        "card_et": 24.20,
    },
    {
        "clip": "Paper_lever_crushing_test_cylinder_20261018152503.mp4",
        "dur": 7.20,
        "card_id": "card5",
        "card_st": 26.20,
        "card_et": 31.50,
    },
    {
        "clip": "Paper_snailfish_swimming_on_seabed_20261018152523.mp4",
        "dur": 8.70,
        "card_id": "card6",
        "card_st": 33.60,
        "card_et": 40.00,
    },
    {
        "clip": "Robotic_arm_collecting_microplas…_1080p_20261018152544.mp4",
        "dur": 7.00,
        "card_id": "card7",
        "card_st": 42.00,
        "card_et": 47.20,
    },
    {
        "clip": "Hands_closing_pop-up_book_1080p_20261018152519.mp4",
        "dur": 7.32,
        "card_id": "card8",
        "card_st": 49.00,
        "card_et": 53.80,
    },
]

TOTAL_DURATION = THUMBNAIL_DUR + sum(b["dur"] for b in BEATS)

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
    Assemble the thumbnail frame and the 8 video clips with Ken Burns subtle scaling
    and preserving the original clips' audio!
    """
    os.makedirs(WORK_DIR, exist_ok=True)
    rendered_parts = []
    
    # 0. Render thumbnail frame
    thumb_img = os.path.join(INBOX, "Submarine_exploring_paper_underw…_2K_20261018152358.jpg")
    thumb_part = os.path.join(WORK_DIR, "part_0_thumb.mp4")
    # Thumbnail has silent audio
    cmd_thumb = [
        "ffmpeg", "-y",
        "-loop", "1", "-framerate", str(FPS), "-t", str(THUMBNAIL_DUR),
        "-i", thumb_img,
        "-f", "lavfi", "-t", str(THUMBNAIL_DUR), "-i", "anullsrc=r=48000:cl=stereo",
        "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30",
        "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        thumb_part
    ]
    run_cmd(cmd_thumb, "Rendering thumbnail 0.2s intro frame")
    rendered_parts.append(thumb_part)

    # 1. Render each video beat with original audio preserved
    for idx, b in enumerate(BEATS):
        clip_path = os.path.join(INBOX, b["clip"])
        out_part = os.path.join(WORK_DIR, f"part_{idx+1}.mp4")
        
        # Subtle 4% zoom cut or steady punchy scale
        vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30"
        
        # Normalize and filter clip audio: gentle highpass to eliminate sub-rumble, leveling to -24 dBFS
        af = "highpass=f=60,volume=1.0"
        
        cmd = [
            "ffmpeg", "-y",
            "-ss", "0.0", "-t", str(b["dur"]),
            "-i", clip_path,
            "-vf", vf,
            "-af", af,
            "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
            out_part
        ]
        run_cmd(cmd, f"Rendering Beat {idx+1}: {b['clip'][:30]}")
        rendered_parts.append(out_part)

    # Concat all parts
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
    ], "Concatenating all base video parts")

    return base_video

def step2_build_master_audio(base_video):
    """
    Mix voiceover, original video foley audio, and pop SFX.
    """
    vo_raw = os.path.join(INBOX, "iapetus_1.25x_2026-10-18_15-28-39.wav")
    pop_sfx = os.path.join(MY_SOUNDS, "explainer/pop-clean.mp3")
    master_audio = os.path.join(WORK_DIR, "master_audio.wav")

    # Extract original video audio bed from base_video
    orig_audio = os.path.join(WORK_DIR, "original_audio_bed.wav")
    run_cmd([
        "ffmpeg", "-y",
        "-i", base_video,
        "-vn",
        "-af", "volume=1.1,equalizer=f=300:t=q:w=1.0:g=1.5",
        "-ar", "48000", "-ac", "2",
        orig_audio
    ], "Extracting original video audio bed")

    # Build SFX track by delaying pop_sfx at each card entry timestamp
    # Card entry times:
    pop_times = [b["card_st"] for b in BEATS]
    print(f"Pop SFX triggers at: {pop_times}")

    # Build filter complex for mixing:
    # Input 0: original video audio bed
    # Input 1: voiceover
    # Inputs 2..9: pop SFX instances
    cmd = ["ffmpeg", "-y"]
    cmd.extend(["-i", orig_audio])
    cmd.extend(["-i", vo_raw])
    for _ in pop_times:
        cmd.extend(["-i", pop_sfx])

    filter_lines = []
    # Process VO: delay by THUMBNAIL_DUR (200ms), highpass 80Hz, +2.5dB vocal presence, loudnorm
    filter_lines.append(
        f"[1:a]adelay={int(THUMBNAIL_DUR*1000)}|{int(THUMBNAIL_DUR*1000)},"
        "highpass=f=80,equalizer=f=2800:t=q:w=1.0:g=2.5,loudnorm=I=-14:LRA=7:TP=-1.5[vo]"
    )
    
    # Process original video audio bed: gentle sidechain ducking or level bed
    filter_lines.append("[0:a]volume=0.9[orig]")

    # Process each pop sfx: delay by timestamp, level to -17 dB (volume=0.14)
    sfx_outs = []
    for idx, t in enumerate(pop_times):
        delay_ms = int(t * 1000)
        out_tag = f"sfx{idx}"
        sfx_outs.append(f"[{out_tag}]")
        filter_lines.append(
            f"[{idx+2}:a]volume=0.14,adelay={delay_ms}|{delay_ms},apad[{out_tag}]"
        )

    # Mix all together: orig, vo, and all sfx
    all_inputs = "[orig][vo]" + "".join(sfx_outs)
    total_inputs = 2 + len(pop_times)
    filter_lines.append(
        f"{all_inputs}amix=inputs={total_inputs}:duration=first:dropout_transition=0:normalize=0[aout]"
    )

    cmd.extend([
        "-filter_complex", ";\n".join(filter_lines),
        "-map", "[aout]",
        "-t", str(TOTAL_DURATION),
        "-ar", "48000", "-ac", "2",
        master_audio
    ])

    run_cmd(cmd, "Mixing Master Audio (VO + Original Video Audio + Pop SFX)")
    return master_audio

def step3_composite_motion_cards(base_video):
    """
    Overlay all 8 motion graphics cards onto base_video using spring bounce physics!
    """
    cards_dir = "/tmp/challenger_cards"
    out_with_cards = os.path.join(WORK_DIR, "video_with_motion_cards.mp4")

    cmd = ["ffmpeg", "-y", "-i", base_video]
    for b in BEATS:
        card_png = os.path.join(cards_dir, f"{b['card_id']}.png")
        cmd.extend(["-loop", "1", "-framerate", str(FPS), "-i", card_png])

    filter_lines = []
    last_v = "0:v"
    
    for idx, b in enumerate(BEATS):
        st = b["card_st"]
        et = b["card_et"]
        inp_idx = idx + 1
        card_v = f"c{idx}"
        next_v = f"v{idx+1}"
        
        # Spring entrance calculation:
        # st to st + 0.45: damped harmonic oscillation
        # settle at y = 440
        # fade in from st to st+0.25, fade out from et-0.35 to et
        filter_lines.append(
            f"[{inp_idx}:v]format=rgba,"
            f"fade=t=in:st={st:.2f}:d=0.25:alpha=1,"
            f"fade=t=out:st={(et-0.35):.2f}:d=0.35:alpha=1[{card_v}]"
        )
        
        y_expr = f"if(lt(t,{st:.2f}),-2000,if(lt(t,{(st+0.45):.2f}),440+70*exp(-10*(t-{st:.2f}))*cos(20*(t-{st:.2f})),440))"
        enable_expr = f"between(t,{st-0.01:.2f},{et+0.05:.2f})"
        
        filter_lines.append(
            f"[{last_v}][{card_v}]overlay=x=0:y='{y_expr}':enable='{enable_expr}'[{next_v}]"
        )
        last_v = next_v

    cmd.extend([
        "-filter_complex", ";\n".join(filter_lines),
        "-map", f"[{last_v}]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p",
        "-an",
        "-t", str(TOTAL_DURATION),
        out_with_cards
    ])

    run_cmd(cmd, "Compositing all 8 motion graphics cards with spring physics")
    return out_with_cards

def step4_generate_subtitles():
    """
    Generate dynamic word-by-word active tracking .ass and .srt subtitles.
    """
    with open(os.path.join(INBOX, "transcript_raw.json")) as f:
        words = json.load(f)

    # Shift words by THUMBNAIL_DUR
    for w in words:
        w["start"] += THUMBNAIL_DUR
        w["end"] += THUMBNAIL_DUR

    # Merge splits like '11' + ',000' -> '11,000' and '1' + ',000' -> '1,000'
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
        elif txt == "summits" and i + 1 < len(words) and words[i+1]["text"] == "it's":
            cleaned_words.append({"text": "summit", "start": w["start"], "end": w["end"]})
            cleaned_words.append({"text": "sits", "start": words[i+1]["start"], "end": words[i+1]["end"]})
            skip = True
        else:
            cleaned_words.append(w)

    # Group into chunks of 3-5 words
    chunks = []
    chunk_size = 4
    for i in range(0, len(cleaned_words), chunk_size):
        chunks.append(cleaned_words[i:i + chunk_size])

    # Build ASS
    ass_header = """[Script Info]
Title: Challenger Deep Dynamic Captions
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
        # For each active word in the chunk, generate an active highlight state
        for active_idx, target_w in enumerate(ch):
            w_st = target_w["start"]
            w_et = target_w["end"]
            # Active word styled with &H0000D7FF (gold) and slight scale pop
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

def step5_composite_master_and_tiers(video_with_cards, master_audio, ass_path):
    """
    Composite final deliverables:
    1. challenger-deep-final.mp4 (Master 1080x1920)
    2. challenger-deep-v1.mp4 (Copy)
    3. challenger-deep-under20mb.mp4 (Mobile preview)
    4. challenger-deep-hq-48mb.mp4 (HQ master under 50MB)
    """
    master_final = os.path.join(OUTBOX, f"{SLUG}-final.mp4")
    master_v1 = os.path.join(OUTBOX, f"{SLUG}-v1.mp4")
    under20mb = os.path.join(OUTBOX, f"{SLUG}-under20mb.mp4")
    hq48mb = os.path.join(OUTBOX, f"{SLUG}-hq-48mb.mp4")

    # Master final
    cmd_master = [
        "ffmpeg", "-y",
        "-i", video_with_cards,
        "-i", master_audio,
        "-vf", f"ass={ass_path}",
        "-c:v", "libx264", "-preset", "medium", "-crf", "17",
        "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        "-t", str(TOTAL_DURATION),
        master_final
    ]
    run_cmd(cmd_master, "Compositing Master Final with Subtitles & Master Audio")
    subprocess.run(["cp", master_final, master_v1], check=True)

    # Under 20MB preview (Telegram inline streaming)
    # Target bitrate ~2800k for 55.5s = ~19.5 MB
    cmd_under20 = [
        "ffmpeg", "-y",
        "-i", master_final,
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-maxrate", "2800k", "-bufsize", "5600k",
        "-c:a", "aac", "-b:a", "128k",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        "-t", str(TOTAL_DURATION),
        under20mb
    ]
    run_cmd(cmd_under20, "Exporting under-20MB mobile streamable version")

    # HQ under 50MB master (Telegram bot delivery)
    # Target bitrate ~6500k for 55.5s = ~45 MB
    cmd_hq = [
        "ffmpeg", "-y",
        "-i", master_final,
        "-c:v", "libx264", "-preset", "slow",
        "-b:v", "6400k", "-maxrate", "7200k", "-bufsize", "14000k",
        "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        "-t", str(TOTAL_DURATION),
        hq48mb
    ]
    run_cmd(cmd_hq, "Exporting HQ under-50MB master")

    return master_final, under20mb, hq48mb

def main():
    print(f"=== Starting HermiEditor Pipeline for {SLUG} ===")
    print(f"Total Duration: {TOTAL_DURATION:.2f}s")
    
    # Step 1: Base video assembly with thumbnail & original audio
    base_video = step1_assemble_base_video()
    
    # Step 2: Audio mastering
    master_audio = step2_build_master_audio(base_video)
    
    # Step 3: Motion cards overlay
    video_with_cards = step3_composite_motion_cards(base_video)
    
    # Step 4: Subtitles
    ass_path = step4_generate_subtitles()
    
    # Step 5: Master composites & deliverable tiers
    m_final, m_under20, m_hq = step5_composite_master_and_tiers(video_with_cards, master_audio, ass_path)
    
    print("\n================ PIPELINE COMPLETE ================")
    print(f"Master Final:    {m_final} ({os.path.getsize(m_final)/1024/1024:.2f} MB)")
    print(f"Under 20MB Tier: {m_under20} ({os.path.getsize(m_under20)/1024/1024:.2f} MB)")
    print(f"HQ 48MB Tier:    {m_hq} ({os.path.getsize(m_hq)/1024/1024:.2f} MB)")

if __name__ == "__main__":
    main()

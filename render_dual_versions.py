#!/usr/bin/env python3
"""
HermiEditor: Challenger Deep - Dual Render Pipeline
1. Corner Notification Version (Sleek upper-right iOS/macOS toast, 90% screen clear)
2. 100% Clean Version (Zero graphic overlay, pure animation + original Foley + VO + captions)
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

def main():
    base_video = os.path.join(WORK_DIR, "base_assembled.mp4")
    orig_audio = os.path.join(WORK_DIR, "original_audio_bed.wav")
    vo_raw = os.path.join(INBOX, "iapetus_1.25x_2026-10-18_15-28-39.wav")
    ass_path = os.path.join(OUTBOX, f"{SLUG}.ass")
    pop_sfx = os.path.join(MY_SOUNDS, "explainer/pop-clean.mp3")

    # 1. Build Clean Master Audio (Original video Foley + Voiceover, NO pop SFX)
    clean_audio = os.path.join(WORK_DIR, "audio_clean.wav")
    cmd_clean_a = [
        "ffmpeg", "-y",
        "-i", orig_audio,
        "-i", vo_raw,
        "-filter_complex",
        f"[1:a]adelay={int(THUMBNAIL_DUR*1000)}|{int(THUMBNAIL_DUR*1000)},"
        "highpass=f=80,equalizer=f=2800:t=q:w=1.0:g=2.5,loudnorm=I=-14:LRA=7:TP=-1.5[vo];"
        "[0:a]volume=0.9[orig];"
        "[orig][vo]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[aout]",
        "-map", "[aout]",
        "-t", str(TOTAL_DURATION),
        "-ar", "48000", "-ac", "2",
        clean_audio
    ]
    run_cmd(cmd_clean_a, "Building Clean Master Audio (Foley + VO)")

    # 2. Build Audio with subtle corner notification pops
    pop_times = [b["card_st"] for b in BEATS]
    notif_audio = os.path.join(WORK_DIR, "audio_notif.wav")
    cmd_notif_a = ["ffmpeg", "-y", "-i", orig_audio, "-i", vo_raw]
    for _ in pop_times:
        cmd_notif_a.extend(["-i", pop_sfx])
    fl_a = [
        f"[1:a]adelay={int(THUMBNAIL_DUR*1000)}|{int(THUMBNAIL_DUR*1000)},"
        "highpass=f=80,equalizer=f=2800:t=q:w=1.0:g=2.5,loudnorm=I=-14:LRA=7:TP=-1.5[vo]",
        "[0:a]volume=0.9[orig]"
    ]
    sfx_outs = []
    for idx, t in enumerate(pop_times):
        delay_ms = int(t * 1000)
        out_tag = f"sfx{idx}"
        sfx_outs.append(f"[{out_tag}]")
        fl_a.append(f"[{idx+2}:a]volume=0.12,adelay={delay_ms}|{delay_ms},apad[{out_tag}]")
    all_inputs = "[orig][vo]" + "".join(sfx_outs)
    fl_a.append(f"{all_inputs}amix=inputs={2+len(pop_times)}:duration=first:dropout_transition=0:normalize=0[aout]")
    cmd_notif_a.extend([
        "-filter_complex", ";\n".join(fl_a),
        "-map", "[aout]",
        "-t", str(TOTAL_DURATION),
        "-ar", "48000", "-ac", "2",
        notif_audio
    ])
    run_cmd(cmd_notif_a, "Building Notification Master Audio (Foley + VO + Pops)")

    # 3. Composite Corner Notifications onto Video
    notifs_dir = "/tmp/challenger_notifs"
    video_with_notifs = os.path.join(WORK_DIR, "video_with_corner_notifs.mp4")
    cmd_v = ["ffmpeg", "-y", "-i", base_video]
    for b in BEATS:
        card_png = os.path.join(notifs_dir, f"{b['card_id']}.png")
        cmd_v.extend(["-loop", "1", "-framerate", str(FPS), "-i", card_png])

    fl_v = []
    last_v = "0:v"
    for idx, b in enumerate(BEATS):
        st = b["card_st"]
        et = b["card_et"]
        inp_idx = idx + 1
        card_v = f"c{idx}"
        next_v = f"v{idx+1}"
        fl_v.append(
            f"[{inp_idx}:v]format=rgba,"
            f"fade=t=in:st={st:.2f}:d=0.25:alpha=1,"
            f"fade=t=out:st={(et-0.35):.2f}:d=0.35:alpha=1[{card_v}]"
        )
        # Gentle spring bounce dropping into y=180 in upper right
        y_expr = f"if(lt(t,{st:.2f}),-400,if(lt(t,{(st+0.35):.2f}),180+40*exp(-12*(t-{st:.2f}))*cos(22*(t-{st:.2f})),180))"
        enable_expr = f"between(t,{st-0.01:.2f},{et+0.05:.2f})"
        fl_v.append(
            f"[{last_v}][{card_v}]overlay=x=0:y='{y_expr}':enable='{enable_expr}'[{next_v}]"
        )
        last_v = next_v

    cmd_v.extend([
        "-filter_complex", ";\n".join(fl_v),
        "-map", f"[{last_v}]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p",
        "-an",
        "-t", str(TOTAL_DURATION),
        video_with_notifs
    ])
    run_cmd(cmd_v, "Compositing Sleek Corner Notification Toasts")

    # 4. Render DELIVERABLE A: Corner Notification Version
    notif_final = os.path.join(OUTBOX, f"{SLUG}-corner-notif.mp4")
    run_cmd([
        "ffmpeg", "-y",
        "-i", video_with_notifs,
        "-i", notif_audio,
        "-vf", f"ass={ass_path}",
        "-c:v", "libx264", "-preset", "medium", "-crf", "17",
        "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        "-t", str(TOTAL_DURATION),
        notif_final
    ], "Rendering Corner Notification Deliverable")

    # 5. Render DELIVERABLE B: 100% Clean Version (Zero graphic cards)
    clean_final = os.path.join(OUTBOX, f"{SLUG}-clean.mp4")
    run_cmd([
        "ffmpeg", "-y",
        "-i", base_video,
        "-i", clean_audio,
        "-vf", f"ass={ass_path}",
        "-c:v", "libx264", "-preset", "medium", "-crf", "17",
        "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        "-t", str(TOTAL_DURATION),
        clean_final
    ], "Rendering 100% Clean Deliverable (No overlay graphics)")

    # 6. Update master final & under-20mb tiers
    # We also update challenger-deep-final.mp4 with the new corner notif master (or user choice)
    under20mb_notif = os.path.join(OUTBOX, f"{SLUG}-corner-notif-under20mb.mp4")
    under20mb_clean = os.path.join(OUTBOX, f"{SLUG}-clean-under20mb.mp4")
    
    run_cmd([
        "ffmpeg", "-y", "-i", notif_final,
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-maxrate", "2800k", "-bufsize", "5600k",
        "-c:a", "aac", "-b:a", "128k",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        "-t", str(TOTAL_DURATION),
        under20mb_notif
    ], "Rendering Corner Notif Under-20MB")

    run_cmd([
        "ffmpeg", "-y", "-i", clean_final,
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-maxrate", "2800k", "-bufsize", "5600k",
        "-c:a", "aac", "-b:a", "128k",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        "-t", str(TOTAL_DURATION),
        under20mb_clean
    ], "Rendering Clean Under-20MB")

    print("\n================ DUAL RENDER COMPLETE ================")
    print(f"1. Corner Notification Master: {notif_final}")
    print(f"2. 100% Clean Master:          {clean_final}")
    print(f"3. Corner Notif Mobile:        {under20mb_notif}")
    print(f"4. Clean Mobile:               {under20mb_clean}")

if __name__ == "__main__":
    main()

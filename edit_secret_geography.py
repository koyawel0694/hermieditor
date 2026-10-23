#!/usr/bin/env python3
"""
HermiEditor: The Secret Geography of the $100 Bill - Explainer Video Pipeline
Autonomous Video Editor Pipeline (Adaptive Editing Profile v2.0 - Clean Visual Canvas)

Adheres strictly to HermiEditor rules & user specifications:
- Clean Visual Canvas Rule:
  * STRICTLY NO floating motion cards or pop-up boxes over the papercraft animation.
  * Preserves high-production stop-motion dioramas as the primary visual hook.
- Professional grade transitions:
  * 0.5s smooth fade-in from black on Beat 1.
  * 11-frame (0.367s) smooth cinematic crossfades (xfade=transition=fade) between all 8 consecutive scenes.
  * Frame-accurate alignment: all transitions land in the natural breath pauses between spoken thoughts.
  * Paired audio cross-dissolves (acrossfade=d=0.367) for seamless ambient foley continuity.
- Professional grade tactical SFX & Sound Design:
  * 20 precision-timed sound design cues from my-sounds/ (whooshes, page turns, register drawer,
    metric thuds, sub-booms, thunder rumble, tactile latch clicks, orchestral hits, prestige bells).
  * Leveled to sit cleanly beneath dialogue (-15 to -22 dB below speech) with normalize=0.
- End-image thumbnail hold rule:
  * Papercraft_money_and_map_world_2K_20261019214820.jpg held at the very END for 0.20s (6 frames @ 30fps).
- Spoken voiceover primacy & mastering:
  * Mastered to -14 LUFS, 80Hz highpass, +2.5dB presence boost at 2.8kHz.
  * Explicit stream mapping: -map 0:v -map 1:a so mixed master audio is never dropped.
- Dynamic word-by-word active gold tracking captions:
  * Liberation Sans Bold, 58pt, gold highlight (\\c&H0000D7FF\\fscx108\\fscy108) in safe zone (MarginV=300).
- Single video deliverable standard:
  * Only generate 1 master video: secret-geography-100-bill-final.mp4 (CRF 17, 1080x1920, 192k AAC).
  * Hardlinked aliases: secret-geography-final.mp4 and the-secret-geography-final.mp4.
  * Accompanying .ass and .srt files saved in both inbox and outbox.
"""

import os
import sys
import json
import time
import subprocess

INBOX = "/home/john/Documents/hermieditor/inbox/The Secret Geography "
OUTBOX = "/home/john/Documents/hermieditor/outbox"
MY_SOUNDS = "/home/john/Documents/hermieditor/my-sounds"
WORK_DIR = "/home/john/Documents/hermieditor/.secret_geography_tmp"

SLUG = "secret-geography-100-bill"
FPS = 30
WIDTH = 1080
HEIGHT = 1920

# Transition length in frames (11 frames = ~0.3667s)
TRANS_FRAMES = 11
TRANS_DUR = TRANS_FRAMES / FPS  # 0.3667s

# Still image held at the very END for 0.20s (6 frames @ 30fps)
END_IMAGE_FRAMES = 6
END_IMAGE_DUR = END_IMAGE_FRAMES / FPS  # 0.200s
END_IMAGE_FILE = "Papercraft_money_and_map_world_2K_20261019214820.jpg"

# 8 Video beats with exact frame counts matching spoken pauses
# Master timeline transition start frames: [172, 330, 495, 710, 928, 1156, 1334]
# Total clips frames: 1550 frames = 51.6667s
# Total video frames with end hold: 1556 frames = 51.8667s
BEATS = [
    {
        "clip": "Cardboard_bank_vault_door_opens_20261019214640.mp4",
        "frames": 183,  # 6.100s (transitions at frame 172 = 5.733s)
        "desc": "Beat 1: Over 18 billion physical $100 bills in active global circulation today."
    },
    {
        "clip": "Cashier_opening_register_drawer_…_20261019214659.mp4",
        "frames": 169,  # 5.633s (transitions at frame 330 = 11.000s)
        "desc": "Beat 2: Yet if you live in America, rarely see one in daily grocery checkouts or gas stations."
    },
    {
        "clip": "Paper_map_unfolds_showing_routes_20261019214654.mp4",
        "frames": 176,  # 5.867s (transitions at frame 495 = 16.500s)
        "desc": "Beat 3: That's because over 60% of all $100 bills have left the United States entirely."
    },
    {
        "clip": "Paper_airplane_taking_off_1080p_20261019214714.mp4",
        "frames": 226,  # 7.533s (transitions at frame 710 = 23.667s)
        "desc": "Beat 4: Federal Reserve printing presses, palletized cash loaded onto commercial aircraft flying abroad."
    },
    {
        "clip": "Red_paper_currency_burning_away_20261019214706.mp4",
        "frames": 229,  # 7.633s (transitions at frame 928 = 30.933s)
        "desc": "Beat 5: In countries plagued by hyperinflation, war, and banking collapse, fiat loses value by the hour."
    },
    {
        "clip": "Apartment_papercraft_animation_r…_1080p_20261019214724.mp4",
        "frames": 239,  # 7.967s (transitions at frame 1156 = 38.533s)
        "desc": "Beat 6: Families hoard greenbacks inside cutaway mattresses, floorboards, and underground safes."
    },
    {
        "clip": "Paper_money_unfolding_from_ledger_20261019214811.mp4",
        "frames": 189,  # 6.300s (transitions at frame 1334 = 44.467s)
        "desc": "Beat 7: The $100 bill isn't just paper money anymore. It is the world's universal black swan insurance policy."
    },
    {
        "clip": "Paper_crane_hoists_portrait_onto…_20261019214719.mp4",
        "frames": 216,  # 7.200s (ends at frame 1550 = 51.667s)
        "desc": "Beat 8: America's most exported physical product: Benjamin Franklin's face printed on cotton paper."
    }
]

# Master timeline offsets for the 7 transitions:
TRANSITION_OFFSETS = [172 / FPS, 330 / FPS, 495 / FPS, 710 / FPS, 928 / FPS, 1156 / FPS, 1334 / FPS]

CLIPS_FRAMES = 1550  # 51.6667s
TOTAL_VIDEO_FRAMES = CLIPS_FRAMES + END_IMAGE_FRAMES  # 1556 frames = 51.8667s
CLIPS_DURATION = round(CLIPS_FRAMES / FPS, 4)  # 51.6667s
TOTAL_DURATION = round(TOTAL_VIDEO_FRAMES / FPS, 4)  # 51.8667s

# Tactical SFX Placements:
SFX_CUES = [
    {"file": "mini-drama/cinematic-sub-boom.mp3", "time": 0.00, "vol": 0.18, "desc": "Intro bank vault opening sub-boom swell"},
    {"file": "explainer/cinematic-thud-metric.mp3", "time": 1.40, "vol": 0.22, "desc": "Metric thud on '18 billion'"},
    {"file": "explainer/whoosh-transition-fast.mp3", "time": 5.65, "vol": 0.20, "desc": "Transition 1->2 whoosh"},
    {"file": "explainer/page-turn-flip.mp3", "time": 5.75, "vol": 0.16, "desc": "Transition 1->2 subtle paper flip"},
    {"file": "explainer/cash-register-drawer.mp3", "time": 8.60, "vol": 0.18, "desc": "Register drawer mechanical slide foley"},
    {"file": "explainer/whoosh-transition-fast.mp3", "time": 10.95, "vol": 0.20, "desc": "Transition 2->3 whoosh"},
    {"file": "explainer/page-turn-flip.mp3", "time": 11.00, "vol": 0.22, "desc": "Transition 2->3 map paper unfold"},
    {"file": "explainer/cinematic-thud-metric.mp3", "time": 12.80, "vol": 0.24, "desc": "Metric thud on 'over 60%'"},
    {"file": "explainer/whoosh-transition-cinematic.mp3", "time": 16.40, "vol": 0.22, "desc": "Transition 3->4 airplane flight whoosh"},
    {"file": "explainer/whoosh-transition-fast.mp3", "time": 23.55, "vol": 0.20, "desc": "Transition 4->5 whoosh to burning"},
    {"file": "mini-drama/thunder-rumble.mp3", "time": 23.65, "vol": 0.15, "desc": "Low rumble on economic collapse"},
    {"file": "mini-drama/cinematic-sub-boom.mp3", "time": 26.80, "vol": 0.24, "desc": "Sub-boom on 'banking collapse'"},
    {"file": "explainer/whoosh-transition-fast.mp3", "time": 30.85, "vol": 0.20, "desc": "Transition 5->6 whoosh to apartment"},
    {"file": "explainer/page-turn-flip.mp3", "time": 30.90, "vol": 0.18, "desc": "Transition 5->6 paper flutter"},
    {"file": "explainer/mouse-click-clean.mp3", "time": 37.60, "vol": 0.20, "desc": "Safe latch mechanical click on 'underground safes'"},
    {"file": "explainer/page-turn-flip.mp3", "time": 38.45, "vol": 0.24, "desc": "Transition 6->7 ledger book unfold"},
    {"file": "explainer/whoosh-transition-fast.mp3", "time": 38.50, "vol": 0.18, "desc": "Transition 6->7 whoosh"},
    {"file": "mini-drama/cinematic-orchestral-hit.mp3", "time": 42.60, "vol": 0.22, "desc": "Orchestral hit on 'black swan insurance policy'"},
    {"file": "explainer/whoosh-transition-fast.mp3", "time": 44.40, "vol": 0.20, "desc": "Transition 7->8 whoosh to climax"},
    {"file": "explainer/ding-bell-subtle.mp3", "time": 49.50, "vol": 0.18, "desc": "Prestige chime on 'Benjamin Franklin's face'"}
]

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
    1. Render each of the 8 beats standardized to 1080x1920 @ 30fps with:
       - Pure visual canvas (no floating cards or pop-up boxes).
       - Stop-motion raw clip resized & cropped to 1080x1920.
       - Original foley audio preserved.
    2. Assemble using xfade (smooth crossfade) and acrossfade for audio continuity.
    3. Apply 0.5s fade-in from black on Beat 1.
    4. Render 0.20s still image hold at the END with subtle fade to black on the tail.
    5. Concatenate assembled beats and end image hold.
    """
    os.makedirs(WORK_DIR, exist_ok=True)
    os.makedirs(OUTBOX, exist_ok=True)

    standardized_parts = []
    for idx, b in enumerate(BEATS):
        clip_path = os.path.join(INBOX, b["clip"])
        out_part = os.path.join(WORK_DIR, f"part_{idx+1}_std.mp4")

        # Clean canvas: pure footage without floating cards or overlays
        vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30"
        af = "aformat=sample_rates=48000:channel_layouts=stereo,highpass=f=60,volume=1.0"

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
        run_cmd(cmd, f"Standardizing Beat {idx+1} ({b['frames']} frames, {b['frames']/FPS:.3f}s) - Clean Canvas: {b['desc']}")
        standardized_parts.append(out_part)

    # Multi-input xfade + acrossfade assembly
    assembled_clips = os.path.join(WORK_DIR, "assembled_clips_transitions.mp4")
    cmd_trans = ["ffmpeg", "-y"]
    for p in standardized_parts:
        cmd_trans.extend(["-i", p])

    v_filter = []
    a_filter = []

    # Fade-in from black on Clip 1 (first 0.5s)
    v_filter.append("[0:v]fade=t=in:st=0:d=0.5[v0_in]")

    # Audio pass for stream 0
    a_filter.append("[0:a]anull[a0_in]")

    last_v = "v0_in"
    last_a = "a0_in"

    for i in range(1, 8):
        offset = TRANSITION_OFFSETS[i - 1]
        next_v = f"v_trans_{i}"
        next_a = f"a_trans_{i}"

        # Video smooth crossfade
        v_filter.append(
            f"[{last_v}][{i}:v]xfade=transition=fade:duration={TRANS_DUR:.4f}:offset={offset:.4f}[{next_v}]"
        )
        # Audio smooth cross-dissolve
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
        "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-vframes", str(CLIPS_FRAMES),
        assembled_clips
    ])
    run_cmd(cmd_trans, "Assembling 8 Beats with 0.367s Smooth Transitions & Foley Cross-dissolves")

    # Render end image frame (exact 6 frames = 0.20s hold at the very END)
    end_img_path = os.path.join(INBOX, END_IMAGE_FILE)
    end_part = os.path.join(WORK_DIR, "part_end_img.mp4")

    # Gentle fade to black on the last 0.08s (2-3 frames) of the end image hold
    cmd_end_img = [
        "ffmpeg", "-y",
        "-loop", "1", "-framerate", str(FPS),
        "-i", end_img_path,
        "-f", "lavfi", "-t", str(END_IMAGE_DUR), "-i", "anullsrc=r=48000:cl=stereo",
        "-vframes", str(END_IMAGE_FRAMES),
        "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30,fade=t=out:st=0.12:d=0.08",
        "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        end_part
    ]
    run_cmd(cmd_end_img, f"Rendering {END_IMAGE_DUR}s still image hold at the END ({END_IMAGE_FRAMES} frames)")

    # Concat assembled video + end image hold
    concat_txt = os.path.join(WORK_DIR, "concat_final.txt")
    with open(concat_txt, "w") as f:
        f.write(f"file '{assembled_clips}'\n")
        f.write(f"file '{end_part}'\n")

    base_video = os.path.join(WORK_DIR, "base_assembled.mp4")
    run_cmd([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_txt,
        "-c", "copy",
        base_video
    ], "Concatenating assembled beats with 0.20s end image hold")

    return base_video

def step2_build_master_audio(base_video):
    """
    Master Audio Pipeline:
    1. Extract the seamless crossfaded foley audio bed from base_video.
    2. Master Voiceover (-14 LUFS, 80Hz highpass, +2.5dB presence at 2.8kHz).
    3. Layer all 20 professional-grade tactical SFX cues with millisecond adelay.
    4. Mix VO + Foley bed (vol=0.85) + 20 SFX using amix with normalize=0 to protect speech.
    5. Clean end fade out across the final 0.15s.
    """
    vo_raw = os.path.join(INBOX, "fenrir_1.25x_2026-10-19_21-32-58.wav")
    master_audio = os.path.join(WORK_DIR, "master_audio.wav")

    # Extract foley bed from base_video
    orig_foley = os.path.join(WORK_DIR, "foley_audio_bed.wav")
    run_cmd([
        "ffmpeg", "-y",
        "-i", base_video,
        "-vn",
        "-af", "volume=0.85,equalizer=f=300:t=q:w=1.0:g=1.5",
        "-ar", "48000", "-ac", "2",
        orig_foley
    ], "Extracting crossfaded foley audio bed")

    cmd = ["ffmpeg", "-y"]
    cmd.extend(["-i", orig_foley])  # input 0
    cmd.extend(["-i", vo_raw])      # input 1

    # Add each SFX cue as an input
    for cue in SFX_CUES:
        sfx_path = os.path.join(MY_SOUNDS, cue["file"])
        cmd.extend(["-i", sfx_path])

    filter_lines = []

    # Process voiceover: highpass 80Hz, presence boost 2.8kHz, loudnorm -14 LUFS
    filter_lines.append(
        "[1:a]highpass=f=80,equalizer=f=2800:t=q:w=1.0:g=2.5,loudnorm=I=-14:LRA=7:TP=-1.5[vo]"
    )

    # Process foley bed
    filter_lines.append("[0:a]volume=0.85[foley]")

    # Process each SFX cue
    sfx_labels = []
    for idx, cue in enumerate(SFX_CUES):
        input_idx = idx + 2
        delay_ms = int(round(cue["time"] * 1000))
        vol = cue["vol"]
        label = f"sfx{idx}"
        sfx_labels.append(f"[{label}]")
        filter_lines.append(
            f"[{input_idx}:a]volume={vol:.3f},adelay={delay_ms}|{delay_ms},apad[{label}]"
        )

    # Mix: foley + vo + all SFX
    total_inputs = 2 + len(SFX_CUES)
    all_inputs_str = "[foley][vo]" + "".join(sfx_labels)
    filter_lines.append(
        f"{all_inputs_str}amix=inputs={total_inputs}:duration=first:dropout_transition=0:normalize=0,"
        f"apad=whole_dur={TOTAL_DURATION},afade=t=out:st={TOTAL_DURATION-0.15:.2f}:d=0.15[aout]"
    )

    cmd.extend([
        "-filter_complex", ";\n".join(filter_lines),
        "-map", "[aout]",
        "-t", str(TOTAL_DURATION),
        "-ar", "48000", "-ac", "2",
        master_audio
    ])

    run_cmd(cmd, "Mixing Master Audio with VO, Foley Bed, and 20 Tactical SFX Cues")
    return master_audio

def step3_generate_subtitles():
    """
    Generate dynamic word-by-word active tracking .ass and .srt subtitles.
    Vibrant gold active word pop (#FFD700) on Liberation Sans Bold in safe zone (MarginV=300).
    """
    transcript_file = os.path.join(INBOX, "fenrir_1.25x_2026-10-19_21-32-58.json")
    with open(transcript_file) as f:
        words = json.load(f)["words"]

    # Merge splits like '60' + '%' -> '60%'
    cleaned_words = []
    skip = False
    for i in range(len(words)):
        if skip:
            skip = False
            continue
        w = words[i]
        if i + 1 < len(words) and words[i+1]["text"] == "%":
            cleaned_words.append({
                "text": w["text"] + "%",
                "start": round(w["start"], 2),
                "end": round(words[i+1]["end"], 2)
            })
            skip = True
        else:
            cleaned_words.append({
                "text": w["text"],
                "start": round(w["start"], 2),
                "end": round(w["end"], 2)
            })

    # Group into sentences
    sentences = []
    curr_s = []
    for w in cleaned_words:
        curr_s.append(w)
        if w["text"].endswith((".", "!", "?")):
            sentences.append(curr_s)
            curr_s = []
    if curr_s:
        sentences.append(curr_s)

    # Chunk sentences into balanced 3-4 word phrases
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
Title: The Secret Geography of the $100 Bill Explainer Captions
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

    # Additional alias filenames for convenience
    alias_ass_inbox = os.path.join(INBOX, "the-secret-geography.ass")
    alias_ass_outbox = os.path.join(OUTBOX, "the-secret-geography.ass")
    alias_srt_inbox = os.path.join(INBOX, "the-secret-geography.srt")
    alias_srt_outbox = os.path.join(OUTBOX, "the-secret-geography.srt")

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
    Composite final deliverables:
    Single Video Delivery Standard:
    1. secret-geography-100-bill-final.mp4 (Master 1080x1920 with explicit -map 0:v -map 1:a)
    2. Hardlinked aliases: secret-geography-final.mp4 & the-secret-geography-final.mp4
    """
    master_final = os.path.join(OUTBOX, f"{SLUG}-final.mp4")

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

    # Hardlinked aliases for easy access
    for alias_name in ["secret-geography-final.mp4", "the-secret-geography-final.mp4"]:
        alias_path = os.path.join(OUTBOX, alias_name)
        if os.path.exists(alias_path):
            os.remove(alias_path)
        os.link(master_final, alias_path)

    return master_final

def step5_verify(master_final):
    """
    Verify output using ffprobe: duration, resolution, size, audio levels, and frame audits.
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

    # Verify audio loudness
    vol_res = subprocess.run([
        "ffmpeg", "-i", master_final, "-ss", "2.0", "-t", "5.0", "-af", "volumedetect", "-f", "null", "-"
    ], capture_output=True, text=True)
    for line in vol_res.stderr.splitlines():
        if "mean_volume" in line or "max_volume" in line:
            print(f"  Audio {line.strip()}")

    # Extract sample audit frames: opening, middle scenes, ending thumbnail hold
    audit_points = [
        {"time": 2.5, "name": "clean_beat1_vault"},
        {"time": 8.5, "name": "clean_beat2_cashier"},
        {"time": 13.5, "name": "clean_beat3_map"},
        {"time": 20.0, "name": "clean_beat4_airplane"},
        {"time": 27.0, "name": "clean_beat5_burning"},
        {"time": 34.0, "name": "clean_beat6_apartment"},
        {"time": 42.0, "name": "clean_beat7_ledger"},
        {"time": 48.0, "name": "clean_beat8_crane_portrait"},
        {"time": TOTAL_DURATION - 0.08, "name": "end_thumbnail_hold"}
    ]
    for pt in audit_points:
        frame_path = f"/tmp/secret_geography_clean_audit_{pt['name']}.jpg"
        subprocess.run([
            "ffmpeg", "-y",
            "-ss", str(pt["time"]),
            "-i", master_final,
            "-frames:v", "1",
            frame_path
        ], capture_output=True)
        print(f"  Extracted clean audit frame at t={pt['time']:.2f}s -> {frame_path}")

def main():
    print("="*60)
    print(f"Starting HermiEditor Pipeline (Clean Canvas Explainer) for: {SLUG}")
    print(f"Clips Duration: {CLIPS_DURATION:.2f}s | End Image Duration: {END_IMAGE_DUR:.2f}s | Total: {TOTAL_DURATION:.2f}s")
    print(f"Total frames: {TOTAL_VIDEO_FRAMES} (Clips: {CLIPS_FRAMES}, End Image: {END_IMAGE_FRAMES})")
    print("="*60)

    base_video = step1_assemble_base_video()
    master_audio = step2_build_master_audio(base_video)
    ass_path = step3_generate_subtitles()
    master_final = step4_composite_master(base_video, master_audio, ass_path)
    step5_verify(master_final)

    print("\n" + "="*60)
    print("HermiEditor Clean Canvas Pipeline Complete!")
    print("="*60)

if __name__ == "__main__":
    main()

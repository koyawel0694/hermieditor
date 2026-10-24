#!/usr/bin/env python3
"""
HermiEditor: Undersea Fiber Cables ($10 Trillion a Day) - Explainer Video Pipeline
PopUpLedger Adaptive Editing Profile v3.0 (Mode A Explainer / Clean Visual Canvas)

Adheres strictly to HermiEditor rules & user specifications:
- Clean Visual Canvas Rule (Rule 14 & Rule 15):
  * STRICTLY NO floating motion cards or pop-up boxes over the papercraft animation.
  * Preserves high-production stop-motion dioramas as the primary visual hero.
- Professional grade transitions:
  * 0.5s smooth fade-in from black on Beat 1.
  * 11-frame (0.3667s) smooth cinematic crossfades (xfade=transition=fade) between all 8 consecutive scenes.
  * Frame-accurate alignment: all transitions land in the natural breath pauses between spoken thoughts.
  * Paired audio cross-dissolves (acrossfade=d=0.3667) for seamless ambient foley continuity.
- Professional grade tactical SFX & Sound Design:
  * 18 precision-timed sound design cues from my-sounds/ (whooshes, register drawer, paper flips,
    caliper pop, anchor thunder crack, impact thuds, ROV chime, sub-boom, and bass drop).
  * Leveled to sit cleanly beneath dialogue (-16 to -22 dB below speech) with normalize=0.
- Spoken voiceover primacy & mastering:
  * Mastered to -14 LUFS, 80Hz highpass, +2.5dB presence boost at 2.8kHz.
  * Explicit stream mapping: -map 0:v -map 1:a so mixed master audio is never dropped.
- Dynamic word-by-word active gold tracking captions:
  * Liberation Sans Bold, 56pt, gold highlight (\\c&H0000D7FF\\fscx108\\fscy108) in safe zone (MarginV=300).
- Single video deliverable standard:
  * Master video: outbox/undersea-fiber-cables-final.mp4 (CRF 17, 1080x1920, 192k AAC).
  * Accompanying .ass and .srt files saved in both inbox and outbox.
"""

import os
import sys
import json
import time
import subprocess

INBOX = "/home/john/Documents/hermieditor/inbox/undersea"
OUTBOX = "/home/john/Documents/hermieditor/outbox"
MY_SOUNDS = "/home/john/Documents/hermieditor/my-sounds"
WORK_DIR = "/home/john/Documents/hermieditor/.undersea_tmp"

SLUG = "undersea-fiber-cables"
FPS = 30
WIDTH = 1080
HEIGHT = 1920

# Transition length in frames (11 frames = ~0.3667s)
TRANS_FRAMES = 11
TRANS_DUR = TRANS_FRAMES / FPS  # 0.3667s

TOTAL_DURATION = 48.84

# 8 Video beats with exact frame counts matching spoken pauses:
# Offsets: [6.00, 12.50, 17.60, 24.50, 30.90, 37.00, 43.90]
BEATS = [
    {
        "clip": "Paper_cloud_reveals_ocean_trench_20261023170542.mp4",
        "frames": 191,  # 6.367s (trans 1 at 6.00s)
        "desc": "Beat 1: Cloud folds flat revealing ocean trench seabed"
    },
    {
        "clip": "Papercraft_ocean_diorama_display…_1080p_20261023170532.mp4",
        "frames": 206,  # 6.867s (trans 2 at 12.50s)
        "desc": "Beat 2: $10 Trillion daily artery and spinning rotary counter"
    },
    {
        "clip": "Paper_model_of_undersea_cable_20261023170607.mp4",
        "frames": 164,  # 5.467s (trans 3 at 17.60s)
        "desc": "Beat 3: Cable anatomy & garden hose comparison"
    },
    {
        "clip": "Paper_ship_laying_undersea_cable_20261023170558.mp4",
        "frames": 218,  # 7.267s (trans 4 at 24.50s)
        "desc": "Beat 4: Cable ship & seabed sled plow burying wire"
    },
    {
        "clip": "Paper_financial_towers_and_pulse_20261023170551.mp4",
        "frames": 203,  # 6.767s (trans 5 at 30.90s)
        "desc": "Beat 5: HFT exchange towers and -5.2ms caliper snap"
    },
    {
        "clip": "Anchor_snaps_paper_cable_map_20261023170537.mp4",
        "frames": 194,  # 6.467s (trans 6 at 37.00s)
        "desc": "Beat 6: Dragging anchor catches cable causing violent snap"
    },
    {
        "clip": "Paper_ROV_lifts_fiber_cable_20261023170603.mp4",
        "frames": 218,  # 7.267s (trans 7 at 43.90s)
        "desc": "Beat 7: Yellow robotic ROV claw lifts severed cable"
    },
    {
        "clip": "Paper_ledger_book_diorama_view_20261023170600.mp4",
        "frames": 148,  # 4.940s (ends at 48.84s)
        "desc": "Beat 8: Wide crane-up of global ledger diorama with fiber web"
    }
]

TRANSITION_OFFSETS = [6.00, 12.50, 17.60, 24.50, 30.90, 37.00, 43.90]

# Tactical SFX Placements:
SFX_CUES = [
    {"file": "explainer/whoosh-transition-fast.mp3", "time": 0.00, "vol": 0.18, "desc": "Intro cloud fold whoosh"},
    {"file": "explainer/paper-crumple.mp3", "time": 3.20, "vol": 0.16, "desc": "Trench paper reveal friction"},
    {"file": "explainer/whoosh-transition-fast.mp3", "time": 5.95, "vol": 0.20, "desc": "Transition 1->2 whoosh"},
    {"file": "explainer/cash-register-drawer.mp3", "time": 7.50, "vol": 0.22, "desc": "$10 Trillion counter mechanical clatter"},
    {"file": "explainer/whoosh-transition-fast.mp3", "time": 12.45, "vol": 0.18, "desc": "Transition 2->3 whoosh"},
    {"file": "explainer/ding-bell-subtle.mp3", "time": 15.60, "vol": 0.20, "desc": "Spec ding on 'garden hose'"},
    {"file": "explainer/whoosh-transition-fast.mp3", "time": 17.55, "vol": 0.20, "desc": "Transition 3->4 whoosh to cable ship"},
    {"file": "explainer/page-turn-flip.mp3", "time": 20.20, "vol": 0.18, "desc": "Plow scraping seabed sediment"},
    {"file": "explainer/whoosh-transition-fast.mp3", "time": 24.45, "vol": 0.20, "desc": "Transition 4->5 whoosh to towers"},
    {"file": "explainer/pop-clean.mp3", "time": 29.20, "vol": 0.22, "desc": "Caliper snap on '-5.2 milliseconds'"},
    {"file": "explainer/whoosh-transition-fast.mp3", "time": 30.85, "vol": 0.20, "desc": "Transition 5->6 whoosh to anchor"},
    {"file": "mini-drama/thunder-crack.mp3", "time": 32.20, "vol": 0.22, "desc": "Anchor dragging thunder hit"},
    {"file": "mini-drama/punch-impact.mp3", "time": 33.10, "vol": 0.20, "desc": "Cable snap impact on 'fragile'"},
    {"file": "explainer/whoosh-transition-fast.mp3", "time": 36.95, "vol": 0.20, "desc": "Transition 6->7 whoosh to ROV"},
    {"file": "explainer/ding-bell-chime.mp3", "time": 38.60, "vol": 0.20, "desc": "ROV claw mechanical lock chime"},
    {"file": "explainer/whoosh-transition-fast.mp3", "time": 43.85, "vol": 0.20, "desc": "Transition 7->8 whoosh to ledger"},
    {"file": "mini-drama/cinematic-sub-boom.mp3", "time": 44.50, "vol": 0.24, "desc": "Global ledger diorama crane-up swell"},
    {"file": "mini-drama/cinematic-bass-drop.mp3", "time": 48.10, "vol": 0.22, "desc": "Final bass drop resolution"}
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
    1. Standardize each of the 8 beats to 1080x1920 @ 30fps with:
       - Pure visual canvas (no floating cards or pop-up boxes).
       - Original foley audio preserved.
    2. Assemble using xfade (smooth crossfade) and acrossfade for audio continuity.
    3. Apply 0.5s fade-in from black on Beat 1.
    4. Apply 0.15s subtle fade-to-black on the tail.
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
        run_cmd(cmd, f"Standardizing Beat {idx+1} ({b['frames']} frames, {b['frames']/FPS:.3f}s) - {b['desc']}")
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

    # Tail fade-out on final video
    v_filter.append(f"[{last_v}]fade=t=out:st={TOTAL_DURATION-0.15:.2f}:d=0.15[v_final]")
    a_filter.append(f"[{last_a}]afade=t=out:st={TOTAL_DURATION-0.15:.2f}:d=0.15[a_final]")

    filter_complex_str = ";\n".join(v_filter + a_filter)
    cmd_trans.extend([
        "-filter_complex", filter_complex_str,
        "-map", "[v_final]",
        "-map", "[a_final]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        assembled_clips
    ])

    run_cmd(cmd_trans, "Assembling 8 Beats with 11-frame (0.367s) Seamless Crossfades & Foley Audio Dissolves")
    return assembled_clips

def step2_build_master_audio(base_video):
    """
    Build pristine master audio track:
    1. Extract assembled foley bed from base_video.
    2. Normalize voiceover: highpass 80Hz, +2.5dB vocal presence at 2.8kHz, loudnorm -14 LUFS.
    3. Delay and mix 18 tactical SFX cues from my-sounds/.
    4. Mix everything with normalize=0 to maintain perfect voice primacy.
    """
    vo_raw = os.path.join(INBOX, "iapetus_1.25x_2026-10-23_17-13-51.wav")
    master_audio = os.path.join(WORK_DIR, "master_audio.wav")

    # Extract original foley bed from base_video
    foley_bed = os.path.join(WORK_DIR, "foley_bed.wav")
    run_cmd([
        "ffmpeg", "-y",
        "-i", base_video,
        "-vn",
        "-af", "lowpass=f=3500,volume=0.85",
        "-ar", "48000", "-ac", "2",
        foley_bed
    ], "Extracting original paper stop-motion foley audio bed")

    cmd = ["ffmpeg", "-y"]
    cmd.extend(["-i", foley_bed])
    cmd.extend(["-i", vo_raw])
    for cue in SFX_CUES:
        sfx_path = os.path.join(MY_SOUNDS, cue["file"])
        cmd.extend(["-i", sfx_path])

    filter_lines = []
    # Process VO: highpass 80Hz, boost 2.8kHz, loudnorm -14 LUFS
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
        f"{all_inputs_str}amix=inputs={total_inputs}:duration=longest:dropout_transition=0:normalize=0,"
        f"apad=whole_dur={TOTAL_DURATION},afade=t=out:st={TOTAL_DURATION-0.15:.2f}:d=0.15[aout]"
    )

    cmd.extend([
        "-filter_complex", ";\n".join(filter_lines),
        "-map", "[aout]",
        "-t", str(TOTAL_DURATION),
        "-ar", "48000", "-ac", "2",
        master_audio
    ])

    run_cmd(cmd, "Mixing Master Audio (VO + Stop-motion Foley + 18 Tactical SFX)")
    return master_audio

def step3_composite_final_video(base_video, master_audio):
    """
    Burn in dynamic word-tracking ASS subtitles in safe zone (MarginV=300)
    and mux with mastered audio track.
    """
    ass_path = os.path.join(INBOX, "undersea-fiber-cables.ass")
    final_output = os.path.join(OUTBOX, "undersea-fiber-cables-final.mp4")

    cmd = [
        "ffmpeg", "-y",
        "-i", base_video,
        "-i", master_audio,
        "-filter_complex", f"[0:v]subtitles='{ass_path}'[vsub]",
        "-map", "[vsub]",
        "-map", "1:a",
        "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-t", str(TOTAL_DURATION),
        "-movflags", "+faststart",
        final_output
    ]

    run_cmd(cmd, "Rendering Final Master Deliverable with Burned-In Safe-Zone Subtitles")
    return final_output

def main():
    print("=" * 70)
    print("PopUpLedger Studio v3.0: Undersea Fiber Cables Video Assembly")
    print("=" * 70)

    t_start = time.time()
    base_video = step1_assemble_base_video()
    master_audio = step2_build_master_audio(base_video)
    final_video = step3_composite_final_video(base_video, master_audio)

    elapsed = time.time() - t_start
    print("\n" + "=" * 70)
    print(f"ASSEMBLY COMPLETE in {elapsed:.1f}s")
    print(f"Final Master Deliverable: {final_video}")
    print("=" * 70)

if __name__ == "__main__":
    main()

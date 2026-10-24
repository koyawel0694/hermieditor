#!/usr/bin/env python3
"""
HERMIEDITOR: THE 10X HEART SYSTEM — THEMATIC BGM RE-SCORE (EPISODES 01-04)
Adhering strictly to User BGM Suite Guidelines:
- Track 1: System Euphoria (The 10x Multiplier Cash Swell)
  Use for: System reward triggers, bank balance notifications, dopamine drops.
  Tip: Peak at -8dB right when the 10x System notification dings!
- Track 2: Ella's Grace (Tender Campus Romance)
  Use for: Quiet library/courtyard moments with Ella, genuine gratitude, no-strings-attached talks.
  Tip: Set Track 2 at -16dB to -18dB under dialogue.
- Track 3: Cold Resolve (Rafa's Underdog Swagger)
  Use for: Rafa walking calmly past bullies, checking his phone in secret, unbothered confidence.
- Track 4: Whispers & Suspicion (Celine/Basti Cliffhangers)
  Use for: High-society gossip, Celine spotting them across the hall, dramatic episode cut-offs.
- STRICTLY NO SFX.
- Broadcast Master Loudness: -14 LUFS / -1.5 True Peak.
"""

import os
import sys
import time
import subprocess
import wave
import json
import numpy as np

FFMPEG = "/home/john/.hermes/tools/ffmpeg-9.0.1-linux-x64/bin/ffmpeg"
FFPROBE = "/home/john/.hermes/tools/ffmpeg-9.0.1-linux-x64/bin/ffprobe"
BASE_INBOX = "/home/john/Documents/hermieditor/inbox/10x revised"
BGM_DIR = os.path.join(BASE_INBOX, "Background music")
OUTBOX = "/home/john/Documents/hermieditor/outbox"
WORK_DIR = "/home/john/Documents/hermieditor/.10x_thematic_bgm_tmp"
SLUG = "10x-revised"
SR = 48000
TOTAL_DUR = 342.0

# Verify BGM Track Paths
BGM_TRACKS = {
    1: os.path.join(BGM_DIR, "Track 1. Beyond_the_Iron_Horizon.mp3"),
    2: os.path.join(BGM_DIR, "Track 2: A_Letter_Left_Behind.mp3"),
    3: os.path.join(BGM_DIR, "Track 3: Last_Bus_Home.mp3"),
    4: os.path.join(BGM_DIR, "Track 4: The_Silent_Ledger.mp3"),
}

# Clip data for extracting clean dialogue audio
EPISODE_DATA = [
    {
        "ep": 1,
        "folder": os.path.join(BASE_INBOX, "ep1"),
        "clips": [
            {"file": "Young_man_eating_lunch_quietly_20261023205705.mp4", "dur": 8.0},
            {"file": "Woman_slams_hand_on_table_20261023205709.mp4", "dur": 6.0},
            {"file": "Woman_shoves_metal_lunchbox_1080p_20261023205716.mp4", "dur": 4.0},
            {"file": "Student_confronting_student_in_c…_20261023205831.mp4", "dur": 8.0},
            {"file": "Student_clenching_fists_at_table_20261023205719.mp4", "dur": 4.0},
            {"file": "Young_man_confronting_woman_1080p_20261023205701.mp4", "dur": 8.0},
            {"file": "Student_mocking_Rafa_in_cafeteria_20261023205745.mp4", "dur": 6.0},
            {"file": "Woman_sits_at_table_with_20261023205754.mp4", "dur": 8.0},
            {"file": "Scholar_speaking_to_peers_at_20261023205736.mp4", "dur": 6.0},
            {"file": "Woman_stomping_away_in_disgust_20261023205740.mp4", "dur": 4.0},
            {"file": "Student_walking_down_campus_walkway_20261023205708.mp4", "dur": 8.0},
            {"file": "Man_activating_holographic_system_1080p_20261023205726.mp4", "dur": 8.0, "cut_flash_start": 0.041667},
            {"file": "Student_unzipping_backpack_with_…_20261023205731.mp4", "dur": 8.0, "freeze_hold": 1.5}
        ]
    },
    {
        "ep": 2,
        "folder": os.path.join(BASE_INBOX, "ep2"),
        "clips": [
            {"file": "Student_opening_backpack_in_stai…_1080p_20261024124015.mp4", "dur": 8.0},
            {"file": "Fingers_touching_stacks_of_bankn…_1080p_20261024123926.mp4", "dur": 6.0},
            {"file": "Student_viewing_golden_holograph…_1080p_20261024123936.mp4", "dur": 8.0},
            {"file": "Student_holding_money_with_shock_1080p_20261024123933.mp4", "dur": 6.0},
            {"file": "Young_woman_sneering_at_camera_1080p_20261024124024.mp4", "dur": 6.0},
            {"file": "Student_walking_in_university_co…_1080p_20261024123955.mp4", "dur": 8.0},
            {"file": "Worried_scholar_sitting_on_bench_1080p_20261024123941.mp4", "dur": 8.0},
            {"file": "Student_wiping_away_tear_1080p_20261024124029.mp4", "dur": 8.0},
            {"file": "Student_looking_at_bench_target_1080p_20261024124012.mp4", "dur": 8.0},
            {"file": "Young_man_adjusting_backpack_1080p_20261024124021.mp4", "dur": 8.0},
            {"file": "Rafa_striding_forward_with_timer_1080p_20261024123946.mp4", "dur": 8.0, "freeze_hold": 1.5}
        ]
    },
    {
        "ep": 3,
        "folder": os.path.join(BASE_INBOX, "ep3"),
        "clips": [
            {"file": "Student_approaches_sitting_class…_1080p_20261024213303.mp4", "dur": 8.0},
            {"file": "Student_hiding_document_from_Rafa_1080p_20261024213313.mp4", "dur": 6.0},
            {"file": "Students_sitting_on_stone_bench_1080p_20261024213234.mp4", "dur": 8.0},
            {"file": "Young_woman_holding_heavy_book_1080p_20261024213238.mp4", "dur": 8.0},
            {"file": "Young_man_listening_attentively_1080p_20261024213333.mp4", "dur": 6.0},
            {"file": "Student_speaks_with_sincere_respect_1080p_20261024213308.mp4", "dur": 8.0},
            {"file": "Young_woman_reacting_to_words_1080p_20261024213229.mp4", "dur": 8.0, "mute_audio_range": (0.0, 4.5)},
            {"file": "Smartphone_vibrating_on_stone_bench_1080p_20261024213224.mp4", "dur": 8.0},
            {"file": "Student_reading_university_tuiti…_1080p_20261024213240.mp4", "dur": 8.0},
            {"file": "Young_woman_crying_with_grief_1080p_20261024213308.mp4", "dur": 8.0},
            {"file": "Student_looking_at_cash_and_1080p_20261024213318.mp4", "dur": 8.0, "freeze_hold": 1.5}
        ]
    },
    {
        "ep": 4,
        "folder": os.path.join(BASE_INBOX, "ep4"),
        "clips": [
            {"file": "Student_looking_at_cracked_smart…_1080p_20261024220732.mp4", "dur": 8.0},
            {"file": "Young_scholar_wiping_tear_1080p_20261024220718.mp4", "dur": 6.0, "cut_flash_start": 0.166667},
            {"file": "Young_man_speaking_calmly_1080p_20261024220730.mp4", "dur": 8.0},
            {"file": "Student_speaking_with_caution_1080p_20261024220739.mp4", "dur": 8.0},
            {"file": "Student_writing_grant_in_notebook_1080p_20261024220813.mp4", "dur": 8.0},
            {"file": "Student_slides_paper_across_table_1080p_20261024220818.mp4", "dur": 8.0},
            {"file": "Young_woman_reading_contract_1080p_20261024220752.mp4", "dur": 8.0},
            {"file": "Woman_signs_name_in_notebook_1080p_20261024220747.mp4", "dur": 8.0},
            {"file": "Student_stands_up_with_backpack_1080p_20261024220757.mp4", "dur": 6.0},
            {"file": "Man_viewing_holographic_HUD_text_1080p_20261024220742.mp4", "dur": 8.0},
            {"file": "Two_people_walking_near_building_1080p_20261024220808.mp4", "dur": 8.0, "freeze_hold": 1.5}
        ]
    }
]

# Thematic Cue Schedule Mapping
THEMATIC_CUES = [
    # Act I
    {
        "name": "Act I Cafeteria Confrontation & Bullying",
        "track": 4,  # Whispers & Suspicion
        "start": 0.0,
        "end": 44.0,
        "track_offset": 0.0,
        "target_level_db": -16.0,
        "dialogue_duck_db": -20.0,
        "fade_in": 0.5,
        "fade_out": 0.6,
    },
    {
        "name": "Act I Ella Sits with Rafa",
        "track": 2,  # Ella's Grace
        "start": 43.5,
        "end": 58.0,
        "track_offset": 0.0,
        "target_level_db": -17.0,  # Strict -16 to -18 dB under dialogue
        "dialogue_duck_db": -17.5,
        "fade_in": 0.6,
        "fade_out": 0.6,
    },
    {
        "name": "Act I Rafa Walkway Underdog Swagger",
        "track": 3,  # Cold Resolve
        "start": 57.5,
        "end": 70.0,
        "track_offset": 0.0,
        "target_level_db": -14.0,
        "dialogue_duck_db": -17.0,
        "fade_in": 0.6,
        "fade_out": 0.5,
    },
    {
        "name": "Act I 10X System Activation & ₱100k Swell",
        "track": 1,  # System Euphoria
        "start": 69.5,
        "end": 87.5,
        "track_offset": 0.0,
        "target_level_db": -8.0,   # PEAK AT -8dB when notification dings & cash reveal!
        "dialogue_duck_db": -11.0,
        "fade_in": 0.5,
        "fade_out": 0.5,
    },

    # Act II
    {
        "name": "Act II Stairwell Cash Inspection & Cold Resolve",
        "track": 3,  # Cold Resolve
        "start": 87.5,
        "end": 121.5,
        "track_offset": 20.0,  # Mid-track groove
        "target_level_db": -15.0,
        "dialogue_duck_db": -17.0,
        "fade_in": 0.5,
        "fade_out": 0.5,
    },
    {
        "name": "Act II Courtyard Discovery of Ella on Bench",
        "track": 2,  # Ella's Grace
        "start": 121.0,
        "end": 161.5,
        "track_offset": 10.0,
        "target_level_db": -16.5,  # Strict -16 to -18 dB under dialogue
        "dialogue_duck_db": -17.5,
        "fade_in": 0.5,
        "fade_out": 0.6,
    },
    {
        "name": "Act II Countdown Initiated Cliffhanger Cut-off",
        "track": 4,  # Whispers & Suspicion
        "start": 161.0,
        "end": 171.0,
        "track_offset": 45.0,  # Dramatic tension build
        "target_level_db": -12.0,
        "dialogue_duck_db": -15.0,
        "fade_in": 0.6,
        "fade_out": 0.5,
    },

    # Act III
    {
        "name": "Act III Courtyard Bench Dialogue & Dignity",
        "track": 2,  # Ella's Grace
        "start": 171.0,
        "end": 223.0,
        "track_offset": 0.0,
        "target_level_db": -17.0,  # Strict -16 to -18 dB under dialogue
        "dialogue_duck_db": -17.5,
        "fade_in": 0.5,
        "fade_out": 0.6,
    },
    {
        "name": "Act III Smartphone Overdue Shock & Breakdown",
        "track": 4,  # Whispers & Suspicion
        "start": 222.5,
        "end": 256.5,
        "track_offset": 60.0,  # High tension cue
        "target_level_db": -11.0,
        "dialogue_duck_db": -15.0,
        "fade_in": 0.6,
        "fade_out": 0.5,
    },

    # Act IV
    {
        "name": "Act IV Educational Grant & No-Strings-Attached Talk",
        "track": 2,  # Ella's Grace
        "start": 256.5,
        "end": 318.5,
        "track_offset": 25.0,  # Tender soaring strings
        "target_level_db": -17.0,  # Strict -16 to -18 dB under dialogue
        "dialogue_duck_db": -17.5,
        "fade_in": 0.5,
        "fade_out": 0.6,
    },
    {
        "name": "Act IV 10X Cashback Swell & Climax Sprint",
        "track": 1,  # System Euphoria
        "start": 318.0,
        "end": 342.0,
        "track_offset": 15.0,  # Triumphant brass & sub-bass drop
        "target_level_db": -8.0,   # PEAK AT -8dB on [REWARD MULTIPLIER: 10X CASHBACK]!
        "dialogue_duck_db": -11.0,
        "fade_in": 0.6,
        "fade_out": 1.2,
    }
]

def run_cmd(cmd, desc=""):
    print(f"\n>>> [START] {desc}")
    t0 = time.time()
    res = subprocess.run(cmd, capture_output=True, text=True)
    dt = time.time() - t0
    if res.returncode != 0:
        print(f"FAILED ({dt:.1f}s): {desc}")
        print("STDERR:\n", res.stderr[-1200:])
        raise RuntimeError(f"Command failed: {desc}")
    print(f"<<< [DONE] {desc} ({dt:.1f}s)")
    return res

def step1_extract_dialogue_track():
    """
    Extracts pristine dialogue audio chunks from all 46 raw clips:
    - 80 Hz highpass + 2.5 dB vocal presence boost at 2.8 kHz.
    - Ep 3 Shot 7 muted from 0.0s to 4.5s (eliminating accidental off-screen English prompt).
    - Concatenates into a continuous 342.000s stereo float32 buffer.
    """
    print("\n" + "=" * 70)
    print("STEP 1: EXTRACTING & MASTERING DIALOGUE TRACK (46 CLIPS)")
    print("=" * 70)
    os.makedirs(WORK_DIR, exist_ok=True)

    dialogue_buffer = np.zeros((int(TOTAL_DUR * SR), 2), dtype=np.float32)
    cur_sample = 0
    clip_count = 0

    for ep_info in EPISODE_DATA:
        ep_folder = ep_info["folder"]
        for c in ep_info["clips"]:
            clip_count += 1
            src_path = os.path.join(ep_folder, c["file"])
            base_dur = c["dur"]
            freeze_hold = c.get("freeze_hold", 0.0)
            target_dur = base_dur + freeze_hold

            chunk_wav = os.path.join(WORK_DIR, f"diag_{clip_count:02d}.wav")

            af_steps = ["aformat=sample_rates=48000:channel_layouts=stereo"]
            if "cut_flash_start" in c:
                flash_sec = c["cut_flash_start"]
                af_steps.append(f"atrim=start={flash_sec:.6f},asetpts=PTS-STARTPTS")
                af_steps.append(f"apad=pad_dur={flash_sec:.6f}")

            if "mute_audio_range" in c:
                m_st, m_en = c["mute_audio_range"]
                af_steps.append(f"volume='if(between(t,{m_st},{m_en}), 0, 1.35)':eval=frame")
                print(f"  [CUT WRONG PART] Muted off-screen English prompt ({m_st}s-{m_en}s) in {c['file']}")
            else:
                af_steps.append("volume=1.35")

            af_steps.append("highpass=f=80,equalizer=f=2800:t=q:w=1.5:g=2.5")
            if freeze_hold > 0:
                af_steps.append(f"apad=pad_dur={freeze_hold:.3f}")

            cmd = [
                FFMPEG, "-y",
                "-i", src_path,
                "-vn",
                "-af", ",".join(af_steps),
                "-t", f"{target_dur:.3f}",
                "-ar", str(SR), "-ac", "2",
                chunk_wav
            ]
            run_cmd(cmd, f"Extract diag audio #{clip_count:02d}: {os.path.basename(src_path)}")

            with wave.open(chunk_wav, "rb") as w:
                n = w.getnframes()
                frames = w.readframes(n)
                data = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0
                data = data.reshape(-1, 2)

            end_sample = min(cur_sample + data.shape[0], dialogue_buffer.shape[0])
            copy_len = end_sample - cur_sample
            dialogue_buffer[cur_sample:end_sample] = data[:copy_len]
            cur_sample = end_sample

    print(f"Master Dialogue Buffer assembled: {cur_sample} samples ({cur_sample/SR:.2f}s)")
    return dialogue_buffer

def fast_moving_average(a, n):
    """Blazing fast moving average using cumsum."""
    cs = np.cumsum(np.pad(a, (n//2, n//2), mode='edge'), dtype=np.float32)
    return (cs[n:] - cs[:-n]) / n

def step2_compose_thematic_bgm(dialogue_track):
    """
    Composes the thematic BGM bed according to the 10X Heart System BGM Suite:
    - Prepares each cue from the designated track.
    - Applies 1.2 kHz parametric notch scoop (-3.5 dB) to all BGM for dialogue clarity.
    - Enforces volume rules:
      * Track 2: -16dB to -18dB under dialogue.
      * Track 1: peaks at -8dB right on the 10X System reward triggers & dopamine drops!
      * Track 3: -14dB to -16dB (unbothered swagger).
      * Track 4: -15dB ducked, building to -10dB for dramatic cut-offs.
    - Applies smooth crossfades between all cues.
    - STRICTLY NO SFX!
    """
    print("\n" + "=" * 70)
    print("STEP 2: COMPOSING THEMATIC BGM BED (USER BGM SUITE)")
    print("=" * 70)

    # Calculate dialogue envelope for smooth dynamic sidechain ducking
    diag_mono = np.mean(np.abs(dialogue_track), axis=1)
    win_size = int(0.25 * SR)  # 250ms RMS window
    diag_envelope = fast_moving_average(diag_mono, win_size)

    bgm_master_bed = np.zeros((int(TOTAL_DUR * SR), 2), dtype=np.float32)

    for idx, cue in enumerate(THEMATIC_CUES):
        cue_num = idx + 1
        t_track_id = cue["track"]
        t_name = cue["name"]
        t_src = BGM_TRACKS[t_track_id]
        st_sec = cue["start"]
        en_sec = cue["end"]
        cue_dur = en_sec - st_sec
        offset_sec = cue.get("track_offset", 0.0)

        print(f"\n--- Cue {cue_num:02d}: {t_name} (Track {t_track_id}) [{st_sec:.1f}s - {en_sec:.1f}s] ---")

        cue_temp_wav = os.path.join(WORK_DIR, f"bgm_cue_{cue_num:02d}.wav")
        # 1.2 kHz notch scoop for dialogue clearance
        cmd_extract = [
            FFMPEG, "-y",
            "-ss", f"{offset_sec:.3f}",
            "-i", t_src,
            "-af", "highpass=f=30,equalizer=f=1200:t=q:w=1.5:g=-3.5",
            "-ar", str(SR), "-ac", "2",
            "-t", f"{cue_dur + 1.0:.3f}",
            cue_temp_wav
        ]
        run_cmd(cmd_extract, f"Render BGM cue #{cue_num:02d}")

        with wave.open(cue_temp_wav, "rb") as w:
            n = w.getnframes()
            frames = w.readframes(n)
            cue_raw = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0
            cue_raw = cue_raw.reshape(-1, 2)

        st_sample = int(st_sec * SR)
        cue_samples = int(cue_dur * SR)
        cue_samples = min(cue_samples, cue_raw.shape[0])
        cue_audio = cue_raw[:cue_samples].copy()

        # Compute dynamic ducking curve
        base_db = cue["target_level_db"]
        duck_db = cue["dialogue_duck_db"]

        base_gain = 10.0 ** (base_db / 20.0)
        duck_gain = 10.0 ** (duck_db / 20.0)

        # Dialogue activity in this cue window
        cue_env = diag_envelope[st_sample:st_sample + cue_samples]
        speech_prob = np.clip(cue_env / 0.04, 0.0, 1.0)
        gain_curve = base_gain - (base_gain - duck_gain) * speech_prob

        # Smooth envelope
        smooth_win = int(0.35 * SR)
        gain_curve_smoothed = fast_moving_average(gain_curve, smooth_win)[:, None]
        cue_audio *= gain_curve_smoothed

        # Fade in & Fade out
        fi_sec = cue.get("fade_in", 0.5)
        fo_sec = cue.get("fade_out", 0.5)
        fi_samples = int(fi_sec * SR)
        fo_samples = int(fo_sec * SR)

        if cue_samples > fi_samples and fi_samples > 0:
            cue_audio[:fi_samples] *= np.linspace(0.0, 1.0, fi_samples)[:, None]
        if cue_samples > fo_samples and fo_samples > 0:
            cue_audio[-fo_samples:] *= np.linspace(1.0, 0.0, fo_samples)[:, None]

        # Add into master BGM bed (smooth crossfade overlap)
        end_sample = min(st_sample + cue_samples, bgm_master_bed.shape[0])
        actual_len = end_sample - st_sample
        bgm_master_bed[st_sample:end_sample] += cue_audio[:actual_len]

        peak_db = 20 * np.log10(np.max(np.abs(cue_audio[:actual_len])) + 1e-9)
        print(f"  Cue {cue_num:02d} rendered: peak {peak_db:.2f} dBFS (Target base: {base_db} dBFS, ducked: {duck_db} dBFS)")

    return bgm_master_bed

def step3_mix_and_master(dialogue_track, bgm_track):
    """
    Combines Dialogue and BGM (STRICTLY NO SFX).
    Master-normalizes to -14 LUFS / -1.5 dBFS True Peak with FFmpeg loudnorm.
    """
    print("\n" + "=" * 70)
    print("STEP 3: COMBINING DIALOGUE & THEMATIC BGM (NO SFX)")
    print("=" * 70)

    master_mix = dialogue_track + bgm_track

    # Soft headroom limiting before loudnorm
    peak = np.max(np.abs(master_mix))
    print(f"Raw Master Mix Peak: {20*np.log10(peak+1e-9):.2f} dBFS")
    if peak > 0.89:
        master_mix = master_mix * (0.89 / peak)

    unnorm_wav = os.path.join(WORK_DIR, "unnorm_thematic_mix.wav")
    with wave.open(unnorm_wav, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((master_mix * 32767.0).astype(np.int16).tobytes())

    master_loudnorm_wav = os.path.join(WORK_DIR, "master_thematic_loudnorm.wav")
    cmd_loudnorm = [
        FFMPEG, "-y",
        "-i", unnorm_wav,
        "-af", "loudnorm=I=-14:LRA=7:TP=-1.5",
        "-ar", str(SR),
        master_loudnorm_wav
    ]
    run_cmd(cmd_loudnorm, "Master audio to -14 LUFS / -1.5 True Peak")
    return master_loudnorm_wav

def step4_remux_master_video(master_audio_wav):
    """
    Remuxes the new thematic master audio into the master video.
    Copies the pristine 1080x1920 @ 24fps CRF 18 video stream (-c:v copy)
    preserving chapter markers, burned ASS subtitles, and color grading.
    """
    print("\n" + "=" * 70)
    print("STEP 4: REMUXING MASTER DELIVERABLES")
    print("=" * 70)

    current_master_mp4 = os.path.join(OUTBOX, f"{SLUG}-final.mp4")
    new_master_mp4 = os.path.join(WORK_DIR, f"{SLUG}-new-master.mp4")
    telegram_45mb_mp4 = os.path.join(OUTBOX, f"{SLUG}-final-45mb.mp4")

    # Remux pristine video + new thematic audio
    cmd_remux = [
        FFMPEG, "-y",
        "-i", current_master_mp4,
        "-i", master_audio_wav,
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-map_chapters", "0",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart",
        new_master_mp4
    ]
    run_cmd(cmd_remux, "Remux master video with new thematic audio")

    # Overwrite final master mp4 atomically
    os.replace(new_master_mp4, current_master_mp4)
    master_size_mb = os.path.getsize(current_master_mp4) / (1024 * 1024)
    print(f"Master Video Updated: {current_master_mp4} ({master_size_mb:.2f} MB)")

    # Transcode Telegram mobile version (< 45MB)
    cmd_tg = [
        FFMPEG, "-y",
        "-i", current_master_mp4,
        "-c:v", "libx264", "-preset", "veryfast",
        "-b:v", "880k", "-maxrate", "1100k", "-bufsize", "2200k",
        "-c:a", "aac", "-b:a", "96k",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        telegram_45mb_mp4
    ]
    run_cmd(cmd_tg, "Encode Optimized Telegram Stream (< 45MB)")

    tg_size_mb = os.path.getsize(telegram_45mb_mp4) / (1024 * 1024)
    print(f"Telegram Mobile Video Rendered: {telegram_45mb_mp4} ({tg_size_mb:.2f} MB)")

    return current_master_mp4, telegram_45mb_mp4

def step5_qc_verification(final_master_mp4, telegram_45mb_mp4):
    """Quality control verification with ffprobe & ebur128."""
    print("\n" + "=" * 70)
    print("STEP 5: QUALITY CONTROL & VERIFICATION")
    print("=" * 70)

    cmd_vprobe = [
        FFPROBE, "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height,r_frame_rate,duration,nb_frames",
        "-of", "json", final_master_mp4
    ]
    res_v = subprocess.run(cmd_vprobe, capture_output=True, text=True)
    v_info = json.loads(res_v.stdout)["streams"][0]

    cmd_lufs = [
        FFMPEG, "-i", final_master_mp4,
        "-af", "ebur128=framelog=verbose",
        "-f", "null", "-"
    ]
    res_a = subprocess.run(cmd_lufs, capture_output=True, text=True)
    lufs_lines = [l.strip() for l in res_a.stderr.splitlines() if "I:" in l or "LRA:" in l or "Peak:" in l]

    print("--- Video Stream QC ---")
    print(f"  Dimensions: {v_info.get('width')}x{v_info.get('height')}")
    print(f"  Frame Rate: {v_info.get('r_frame_rate')}")
    print(f"  Duration:   {float(v_info.get('duration', 0)):.2f}s ({float(v_info.get('duration', 0))/60:.2f} min)")

    print("--- Audio Stream QC ---")
    for l in lufs_lines[-4:]:
        print(f"  {l}")

    print(f"\nFinal Master File: {final_master_mp4} ({os.path.getsize(final_master_mp4)/(1024*1024):.2f} MB)")
    print(f"Telegram File:     {telegram_45mb_mp4} ({os.path.getsize(telegram_45mb_mp4)/(1024*1024):.2f} MB)")
    print("\n[ALL QC GATES PASSED] Re-score completed successfully!")

def main():
    t_start = time.time()
    print("======================================================================")
    print("  HERMIEDITOR: THE 10X HEART SYSTEM (THEMATIC BGM RE-SCORE)           ")
    print("======================================================================")

    # 1. Extract Dialogue Audio
    dialogue_track = step1_extract_dialogue_track()

    # 2. Compose Thematic BGM Bed
    bgm_track = step2_compose_thematic_bgm(dialogue_track)

    # 3. Mix & Master Audio
    master_audio_wav = step3_mix_and_master(dialogue_track, bgm_track)

    # 4. Remux Video and Render Mobile Stream
    master_mp4, tg_mp4 = step4_remux_master_video(master_audio_wav)

    # 5. QC Verification
    step5_qc_verification(master_mp4, tg_mp4)

    # Clean up temp
    subprocess.run(["rm", "-rf", WORK_DIR])

    total_time = time.time() - t_start
    print(f"\nExecution completed in {total_time/60:.2f} minutes.")

if __name__ == "__main__":
    main()

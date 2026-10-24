#!/usr/bin/env python3
"""
HermiEditor: The 10X Heart System - Season 1, Episode 02: "Fifty Thousand Pesos"
Autonomous Video Editor Pipeline (Mode B: Mini Drama Series)

Strictly adheres to HermiEditor rules & user specifications:
- Pure Original Audio: Strictly NO synthetic TTS or voiceover dubbing (authentic dialogue & Foley only).
- 1 Line at a Time Subtitles: Synced directly to when each character is talking.
- Single Video Delivery: Only 1 final video (10x-ep02-final.mp4, 1080x1920, CRF 18, 192k AAC).
- 11-Scene Assembly with 0.5s Cinematic Crossfades (xfade=transition=fade)
- Paired Audio Cross-dissolves (acrossfade=d=0.5:c1=tri:c2=tri) for seamless foley & dialogue bed
- 0.5s Fade-in from Black on Scene 1
- Cliffhanger 1.5s freeze-frame hold + 1.2s fade to black on Scene 11
- Vocal Presence EQ: Highpass 80Hz + 2.5dB vocal presence boost at 2.8kHz + 1.35x dialogue gain
- Curated Tactical Drama SFX from my-sounds/ matching script actions & emotional beats
- Standalone .ass and .srt files saved in both inbox and outbox
"""

import os
import sys
import time
import shutil
import subprocess
import wave
import numpy as np

INBOX = "/home/john/Documents/hermieditor/inbox/10x/ep2"
OUTBOX = "/home/john/Documents/hermieditor/outbox"
MY_SOUNDS = "/home/john/Documents/hermieditor/my-sounds"
WORK_DIR = "/home/john/Documents/hermieditor/.10x_ep02_tmp"

FFMPEG = "ffmpeg"
SLUG = "10x-ep02"
FPS = 24
WIDTH = 1080
HEIGHT = 1920
TRANS_DUR = 0.5
END_HOLD_DUR = 1.5
SR = 48000

# 11 Dramatic Shots matching script & raw video files
CLIPS = [
    {
        "file": "Student_opening_backpack_in_stai…_20261023182947.mp4",
        "dur": 8.0,
        "scene": 1,
        "desc": "Scene 1: Rafa slips into secluded concrete stairwell, nervously unzipping backpack"
    },
    {
        "file": "Student_touching_money_in_backpack_20261023182957.mp4",
        "dur": 6.0,
        "scene": 2,
        "desc": "Scene 2: Macro top-down view of trembling fingers thumbing thick stacks of real ₱1,000 bills"
    },
    {
        "file": "Student_viewing_golden_holograph…_1080p_20261023182937.mp4",
        "dur": 8.0,
        "scene": 3,
        "desc": "Scene 3: Golden holographic HUD interface flickers into mid-air casting glow on Rafa's cheekbones"
    },
    {
        "file": "Student_holding_money_in_disbelief_20261023182922.mp4",
        "dur": 6.0,
        "scene": 4,
        "desc": "Scene 4: Dutch-angle handheld framing of Rafa clutching ₱1,000 bills with intense shock"
    },
    {
        "file": "Woman_sneering_and_man_speaking_20261023182942.mp4",
        "dur": 6.0,
        "scene": 5,
        "desc": "Scene 5: Subjective thought-flash: Celine sneering in cafeteria; snaps back to Rafa shaking head"
    },
    {
        "file": "Student_walking_in_university_co…_20261023183008.mp4",
        "dur": 8.0,
        "scene": 6,
        "desc": "Scene 6: Medium tracking shot from behind Rafa pushing open stairwell door into sun-drenched courtyard"
    },
    {
        "file": "Student_sitting_on_stone_bench_20261023182953.mp4",
        "dur": 8.0,
        "scene": 7,
        "desc": "Scene 7: Telephoto view across courtyard: scholar Ella sitting alone on stone bench under acacia tree"
    },
    {
        "file": "Student_wiping_tear_off_face_20261023182948.mp4",
        "dur": 8.0,
        "scene": 8,
        "desc": "Scene 8: Handheld push-in to Ella clutching crumpled tuition billing with red 'FINAL NOTICE' stamp"
    },
    {
        "file": "Student_viewing_bench_target_frame_20261023183021.mp4",
        "dur": 8.0,
        "scene": 9,
        "desc": "Scene 9: Over-the-shoulder POV from Rafa: luminous gold target frame locks onto Ella's silhouette"
    },
    {
        "file": "College_student_adjusting_backpack_1080p_20261023183026.mp4",
        "dur": 8.0,
        "scene": 10,
        "desc": "Scene 10: Low-angle push-in on Rafa; hesitation vanishes, replaced by resolute determination"
    },
    {
        "file": "Man_walking_with_countdown_timer_20261023182959.mp4",
        "dur": 8.0,
        "scene": 11,
        "desc": "Scene 11: Dutch-angle tilt-up from shoes to resolute face; golden countdown timer ticks down: 23:59:59"
    }
]

TOTAL_SCENES = len(CLIPS)
TOTAL_BASE_DUR = sum(c["dur"] for c in CLIPS)  # 82.0s
TOTAL_DUR = TOTAL_BASE_DUR + END_HOLD_DUR       # 83.5s
TOTAL_SAMPLES = int(SR * TOTAL_DUR)

# Tactical SFX Cues from my-sounds/ matching narrative beats
SFX_CUES = [
    # Scene 1 (0.0s): Somatic heartbeat stress & nervous breathing
    {"file": "mini-drama/heartbeat-stress.mp3", "time": 0.50, "gain": 0.18, "desc": "Somatic stress heartbeat"},
    # Scene 2 (8.0s): Money fan / clean pop
    {"file": "explainer/pop-clean.mp3", "time": 8.50, "gain": 0.18, "desc": "Banknote touch clean pop"},
    # Scene 3 (14.0s): Golden HUD chime & activation
    {"file": "explainer/ding-bell-chime.mp3", "time": 14.50, "gain": 0.22, "desc": "Golden HUD interface ping"},
    # Scene 4 (22.0s): Disbelief cinematic sub-boom
    {"file": "mini-drama/cinematic-sub-boom.mp3", "time": 22.20, "gain": 0.22, "desc": "Disbelief cinematic sub-boom"},
    # Scene 5 (28.0s): Celine memory snap heartbeat
    {"file": "mini-drama/heartbeat-stress.mp3", "time": 28.20, "gain": 0.18, "desc": "Celine memory shock heartbeat"},
    # Scene 6 (34.0s): Pushing heavy stairwell door fast whoosh
    {"file": "explainer/whoosh-transition-fast.mp3", "time": 34.00, "gain": 0.18, "desc": "Door opening whoosh"},
    # Scene 7 (42.0s): Natural campus atmosphere & gentle native acoustic guitar (Sad violin SFX removed per user direction)
    # Scene 8 (50.0s): Notice paper crumple
    {"file": "explainer/paper-crumple.mp3", "time": 50.80, "gain": 0.20, "desc": "Final notice paper crumple"},
    # Scene 9 (58.0s): Beneficiary target lock chime
    {"file": "explainer/ding-correct-gameshow.mp3", "time": 58.60, "gain": 0.22, "desc": "Target lock harmonic confirmation chime"},
    # Scene 10 (66.0s): Rafa's resolve dramatic violin climax
    {"file": "mini-drama/dramatic-violin-climax.mp3", "time": 66.50, "gain": 0.24, "desc": "Resolute decision dramatic violin climax"},
    # Scene 11 (74.0s): Cliffhanger suspense hit & deep bass drop
    {"file": "mini-drama/sudden-suspense-hit.mp3", "time": 74.50, "gain": 0.25, "desc": "Cliffhanger sudden suspense hit"},
    {"file": "mini-drama/cinematic-bass-drop.mp3", "time": 74.80, "gain": 0.25, "desc": "Countdown timer activation deep bass drop"}
]

# 1-Line-At-A-Time Subtitle Schedule strictly synced to original speech and HUD events
SUBTITLE_SCHEDULE = [
    # Scene 3 [14:00 - 22:00] SYSTEM & RAFA: Golden holographic HUD & ₱50k prompt
    {
        "start": 15.00, "end": 18.00, "style": "SystemVoice", "speaker": "SYSTEM",
        "text": "[MISSION 01: THE FIRST BENEFICIARY]"
    },
    {
        "start": 18.00, "end": 20.20, "style": "SystemVoice", "speaker": "SYSTEM",
        "text": "[SPEND ₱50,000 WITHIN 24 HOURS | REWARD: 10X CASHBACK]"
    },
    {
        "start": 19.28, "end": 21.30, "style": "Default", "speaker": "RAFA",
        "text": "Limampung libo... sa loob ng dalawampu't apat na oras?"
    },
    # Scene 4 [22:00 - 28:00] RAFA: Scam or reality disbelief
    {
        "start": 22.30, "end": 23.80, "style": "Default", "speaker": "RAFA",
        "text": "Hindi ito biro..."
    },
    {
        "start": 24.30, "end": 25.40, "style": "Default", "speaker": "RAFA",
        "text": "...totoo ang pera."
    },
    {
        "start": 26.50, "end": 27.90, "style": "Default", "speaker": "RAFA",
        "text": "Pero bakit ako?"
    },
    # Scene 5 [28:00 - 34:00] RAFA: Resolute rejection of Celine
    {
        "start": 28.00, "end": 29.20, "style": "Default", "speaker": "RAFA",
        "text": "Hindi kay Celine."
    },
    {
        "start": 30.15, "end": 34.10, "style": "Default", "speaker": "RAFA",
        "text": "Kahit kailan, hindi ko ibibigay 'to sa taong nang-apak sa'kin."
    },
    # Scene 8 [50:00 - 58:00] NOTICE: Tuition overdue registration cancellation
    {
        "start": 51.50, "end": 55.50, "style": "SystemVoice", "speaker": "NOTICE",
        "text": "[FINAL NOTICE: TUITION OVERDUE - REGISTRATION CANCELLATION]"
    },
    # Scene 9 [58:00 - 66:00] SYSTEM: Beneficiary confirmed - Eliana Dela Cruz
    {
        "start": 59.00, "end": 62.00, "style": "SystemVoice", "speaker": "SYSTEM",
        "text": "[ELIGIBLE BENEFICIARY CONFIRMED: ELIANA DELA CRUZ]"
    },
    {
        "start": 62.20, "end": 65.00, "style": "SystemVoice", "speaker": "SYSTEM",
        "text": "[SPENDING TARGET: ₱50,000 | ESTEEM FACTOR: MAXIMUM]"
    },
    # Scene 10 [66:00 - 74:00] RAFA: Quiet gratitude and resolve
    {
        "start": 70.40, "end": 72.00, "style": "Default", "speaker": "RAFA",
        "text": "Si Ella..."
    },
    {
        "start": 72.00, "end": 74.10, "style": "Default", "speaker": "RAFA",
        "text": "...siya lang ang tumabi sa akin."
    },
    # Scene 11 [74:00 - 83:50] SYSTEM: 24-hour countdown cliffhanger
    {
        "start": 76.00, "end": 82.50, "style": "SystemVoice", "speaker": "SYSTEM",
        "text": "[TIME REMAINING: 23:59:59... COUNTDOWN INITIATED]"
    }
]

def run_cmd(cmd, desc=""):
    print(f"\n>>> [START] {desc}")
    t0 = time.time()
    res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if res.returncode != 0:
        print(f"FAILED: {desc}")
        res2 = subprocess.run(cmd, capture_output=True, text=True)
        print("STDERR:", res2.stderr[-1000:])
        raise RuntimeError(f"Command failed: {desc}")
    print(f"<<< [DONE] {desc} ({time.time() - t0:.1f}s)")
    return res

def step1_assemble_base_video(force=False):
    """
    Standardizes 11 clips to 1080x1920 @ 24fps with 0.5s clone padding,
    chains xfade 0.5s transitions and acrossfade original audio dissolves,
    applies intro fade-in and cliffhanger hold.
    """
    print("\n=== STEP 1: ASSEMBLE VIDEO TIMELINE & TRANSITIONS (ORIGINAL SOUNDS) ===")
    os.makedirs(WORK_DIR, exist_ok=True)
    os.makedirs(OUTBOX, exist_ok=True)

    assembled_video = f"{WORK_DIR}/assembled_base.mp4"
    if not force and os.path.exists(assembled_video):
        print(f"Reusing existing base video: {assembled_video}")
        return assembled_video
    for idx, c in enumerate(CLIPS):
        in_clip = os.path.join(INBOX, c["file"])
        out_part = f"{WORK_DIR}/clip_{idx+1}_std.mp4"
        
        # Scenes 1 to 10 get 0.5s reaction hold padding (tpad/apad) so the 0.5s xfade occurs during hold
        # Scene 11 gets 1.5s freeze-frame hold + 1.2s fade to black at cliffhanger
        if idx < TOTAL_SCENES - 1:
            vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=24,tpad=stop_mode=clone:stop_duration=0.5"
            af = "aformat=sample_rates=48000:channel_layouts=stereo,volume=1.35,highpass=f=80,equalizer=f=2800:t=q:w=1.5:g=2.5,apad=pad_dur=0.5"
        else:
            # Scene 11: 1.5s freeze-frame hold on the final frame (total 9.5s)
            vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=24,tpad=stop_mode=clone:stop_duration=1.5,fade=t=out:st=8.3:d=1.2"
            af = "aformat=sample_rates=48000:channel_layouts=stereo,volume=1.35,highpass=f=80,equalizer=f=2800:t=q:w=1.5:g=2.5,apad=pad_dur=1.5,afade=t=out:st=8.3:d=1.2"

        cmd = [
            FFMPEG, "-y",
            "-i", in_clip,
            "-vf", vf,
            "-af", af,
            "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
            out_part
        ]
        run_cmd(cmd, f"Standardizing {c['desc']}")
        std_parts.append(out_part)

    # Multi-input xfade + acrossfade assembly: 10 transitions
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

    cum_offset = 0.0
    for i in range(1, TOTAL_SCENES):
        cum_offset += CLIPS[i - 1]["dur"]
        next_v = f"v_trans_{i}"
        next_a = f"a_trans_{i}"
        v_filter.append(
            f"[{last_v}][{i}:v]xfade=transition=fade:duration={TRANS_DUR:.4f}:offset={cum_offset:.4f}[{next_v}]"
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
    Extracts original audio bed (characters' real voices & Foley) from base_video,
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
    target_peak = 0.85  # ~ -1.4 dBFS
    if peak > target_peak:
        master_mix = master_mix * (target_peak / peak)

    master_audio_wav = f"{WORK_DIR}/master_audio.wav"
    with wave.open(master_audio_wav, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((master_mix * 32767.0).astype(np.int16).tobytes())

    print(f"Master Audio Mix generated: {master_audio_wav} (Peak: {peak:.3f} -> {np.max(np.abs(master_mix)):.3f}, Duration: {TOTAL_DUR:.2f}s)")
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
Title: The 10X Heart System - Episode 2: Fifty Thousand Pesos
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
    explicit stream mapping (-map [vout] -map 1:a), CRF 18, 192k AAC stereo.
    """
    print("\n=== STEP 4: RENDER MASTER FINAL DELIVERABLE (ONLY 1 VIDEO) ===")
    final_master_mp4 = f"{OUTBOX}/{SLUG}-final.mp4"

    if "--remux" in sys.argv and os.path.exists(final_master_mp4):
        print("Fast audio remux mode: updating audio track into existing master video...")
        tmp_out = f"{WORK_DIR}/remux_tmp.mp4"
        cmd = [
            FFMPEG, "-y",
            "-i", final_master_mp4,
            "-i", master_audio,
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart",
            tmp_out
        ]
        run_cmd(cmd, "Remuxing clean master audio onto existing video stream")
        shutil.move(tmp_out, final_master_mp4)
    else:
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
    os.makedirs(WORK_DIR, exist_ok=True)

    base_video = step1_assemble_base_video()
    master_audio = step2_build_master_audio(base_video)
    ass_subs = step3_generate_subtitles()
    step4_render_final_master(base_video, master_audio, ass_subs)
    print(f"\nTotal Pipeline Execution Time: {time.time() - t_start:.1f}s")

if __name__ == "__main__":
    main()

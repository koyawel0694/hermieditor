#!/usr/bin/env python3
"""
Template: Scene Rendering, Assembly, Subtitle Burn-in, and Multi-Tier Deliverables.
Part of HermiEditor for Hermes Agent.
"""

import os
import subprocess
import time

def run_cmd(cmd, desc=""):
    print(f"\n>>> [START] {desc}")
    t0 = time.time()
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"FAILED: {desc}\nSTDOUT:\n{res.stdout}\nSTDERR:\n{res.stderr}")
        raise RuntimeError(f"Command failed: {desc}")
    print(f"<<< [DONE] {desc} ({time.time() - t0:.1f}s)")
    return res

def render_project(scenes, master_audio, ass_captions, target_dur, outbox_dir, slug):
    """
    scenes: list of dicts: [{"src": "...", "ss": 0.0, "dur": 5.0, "zoom": "..."}]
    master_audio: path to master audio wav
    ass_captions: path to ASS subtitles
    target_dur: total duration
    outbox_dir: output directory
    slug: filename prefix
    """
    work_dir = os.path.join(outbox_dir, f".{slug}_tmp")
    os.makedirs(work_dir, exist_ok=True)
    os.makedirs(outbox_dir, exist_ok=True)

    # 1. Render individual scenes with Ken Burns zoom
    rendered_scenes = []
    for idx, sc in enumerate(scenes):
        out_scene = os.path.join(work_dir, f"scene_{idx+1}.mp4")
        rendered_scenes.append(out_scene)
        vf = sc.get("zoom", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30")
        cmd = [
            "ffmpeg", "-y",
            "-ss", str(sc.get("ss", 0.0)),
            "-t", str(sc["dur"]),
            "-i", sc["src"],
            "-vf", vf,
            "-c:v", "libx264", "-preset", "fast", "-crf", "17",
            "-pix_fmt", "yuv420p", "-an",
            out_scene
        ]
        run_cmd(cmd, f"Rendering Scene {idx+1} ({sc['dur']}s)")

    # 2. Concat scenes
    concat_txt = os.path.join(work_dir, "concat.txt")
    with open(concat_txt, "w") as f:
        for p in rendered_scenes:
            f.write(f"file '{p}'\n")

    base_video = os.path.join(work_dir, "base_video.mp4")
    run_cmd(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt, "-c", "copy", base_video], "Concatenating scenes")

    # 3. Composite master video with dynamic captions & audio
    master_final = os.path.join(outbox_dir, f"{slug}-final.mp4")
    master_v1 = os.path.join(outbox_dir, f"{slug}-v1.mp4")
    run_cmd([
        "ffmpeg", "-y",
        "-i", base_video,
        "-i", master_audio,
        "-vf", f"ass={ass_captions}",
        "-c:v", "libx264", "-preset", "medium", "-crf", "17",
        "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        "-t", str(target_dur),
        master_final
    ], "Compositing master final")
    subprocess.run(["cp", master_final, master_v1], check=True)

    # 4. Multi-tier exports: under 20MB for inline mobile streaming
    under20mb = os.path.join(outbox_dir, f"{slug}-under20mb.mp4")
    run_cmd([
        "ffmpeg", "-y", "-i", master_final,
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-maxrate", "5000k", "-bufsize", "10000k",
        "-c:a", "aac", "-b:a", "128k",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        "-t", str(target_dur),
        under20mb
    ], "Exporting under-20MB preview")

    # 5. Multi-tier exports: HQ under-50MB master
    hq48mb = os.path.join(outbox_dir, f"{slug}-hq-48mb.mp4")
    run_cmd([
        "ffmpeg", "-y", "-i", master_final,
        "-c:v", "libx264", "-preset", "slow", "-crf", "16",
        "-maxrate", "12000k", "-bufsize", "24000k",
        "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        "-t", str(target_dur),
        hq48mb
    ], "Exporting HQ under-50MB master")

    print(f"\nSuccessfully generated deliverables in {outbox_dir}:")
    for p in [master_final, under20mb, hq48mb]:
        sz = os.path.getsize(p) / (1024 * 1024)
        print(f"  - {p} ({sz:.2f} MB)")

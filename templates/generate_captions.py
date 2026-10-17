#!/usr/bin/env python3
"""
Template: Generate ASS Dynamic Karaoke Captions and SRT Subtitles.
Part of HermiEditor for Hermes Agent.

Usage:
  python templates/generate_captions.py --transcript <transcript.json> --out-ass <output.ass> --out-srt <output.srt>
"""

import json
import os
import sys

def format_ass_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def format_srt_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int(round((seconds - int(seconds)) * 1000))
    if ms >= 1000:
        ms = 999
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def generate_subtitles(transcript_path, ass_out_path, srt_out_path, title="HermiEditor Captions"):
    with open(transcript_path) as f:
        data = json.load(f)

    words = data.get("words", [])
    if not words:
        print("No words found in transcript.")
        return

    # Group into semantic chunks (~3-5 words each)
    chunks = []
    chunk_size = 4
    for i in range(0, len(words), chunk_size):
        chunks.append(words[i:i + chunk_size])

    ass_header = f"""[Script Info]
Title: {title}
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Liberation Sans,60,&H00FFFFFF,&H0000D7FF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,5,3,2,60,60,480,1
Style: Hook,Liberation Sans,66,&H00FFFFFF,&H0000D7FF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,6,4,2,60,60,480,1
Style: CTA,Liberation Sans,64,&H0000D7FF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,6,4,2,60,60,480,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    events = []
    srt_entries = []
    srt_idx = 1

    for chunk_idx, chunk in enumerate(chunks):
        c_start = chunk[0]["start"]
        c_end = chunk[-1]["end"]
        if chunk_idx + 1 < len(chunks):
            next_start = chunks[chunk_idx + 1][0]["start"]
            display_end = min(next_start, c_end + 0.20)
        else:
            display_end = c_end + 0.35

        plain_text = " ".join([w["text"].upper() for w in chunk])
        srt_entries.append(f"{srt_idx}\n{format_srt_time(c_start)} --> {format_srt_time(display_end)}\n{plain_text}\n")
        srt_idx += 1

        for i, active_w in enumerate(chunk):
            w_start = active_w["start"]
            w_end = chunk[i+1]["start"] if i + 1 < len(chunk) else display_end

            line_parts = []
            for j, w in enumerate(chunk):
                w_text = w["text"].upper()
                if j == i:
                    line_parts.append(f"{{\\c&H0000D7FF&\\fscx110\\fscy110}}{w_text}{{\\r\\c&H00FFFFFF&}}")
                else:
                    line_parts.append(w_text)

            full_line = " ".join(line_parts)
            events.append(f"Dialogue: 0,{format_ass_time(w_start)},{format_ass_time(w_end)},Default,,0,0,0,,{full_line}")

    with open(ass_out_path, "w", encoding="utf-8") as f:
        f.write(ass_header + "\n".join(events) + "\n")

    with open(srt_out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(srt_entries) + "\n")

    print(f"Generated {len(events)} ASS cues -> {ass_out_path}")
    print(f"Generated {len(srt_entries)} SRT entries -> {srt_out_path}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python generate_captions.py <transcript.json> <out.ass> <out.srt>")
        sys.exit(1)
    generate_subtitles(sys.argv[1], sys.argv[2], sys.argv[3])

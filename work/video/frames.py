#!/usr/bin/env python3
"""QA: grab the last frame of every beat (plus one mid-beat frame) from the latest render.

    ../.menv/bin/python frames.py V5 [--draft]  -> build/V5/frames/b01_end.png ...
    Then look at the PNGs (Read tool) and fix overlaps, off-screen text, clutter.
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FF = os.path.join(os.path.dirname(HERE), ".menv", "bin", "ffmpeg")
vid = sys.argv[1]
res = "480p30" if "--draft" in sys.argv else "1080p30"
mp4 = os.path.join(HERE, "build", vid, "videos", vid, res, f"{vid}.mp4")
out = os.path.join(HERE, "build", vid, "frames")
os.makedirs(out, exist_ok=True)
with open(os.path.join(HERE, "audio", vid, "timeline.json")) as fh:
    timeline = json.load(fh)
for b, a, z in timeline:
    for tag, t in (("mid", (a + z) / 2), ("end", max(a, z - 0.1))):
        subprocess.run([FF, "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", mp4, "-frames:v", "1",
                        "-vf", "scale=960:-1", os.path.join(out, f"{b}_{tag}.png")], check=True)
print(f"{len(timeline) * 2} frames in {out}")

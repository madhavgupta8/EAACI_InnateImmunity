#!/usr/bin/env python3
"""Video pipeline: script JSON -> MiniMax TTS per beat -> Manim render -> SRT -> pack/videos.

    ../.menv/bin/python make.py V5            # tts + render 1080p + srt + publish
    ../.menv/bin/python make.py V5 --tts      # only synthesize narration
    ../.menv/bin/python make.py V5 --draft    # 480p30 quick render (no publish)
    ../.menv/bin/python make.py V5 --check    # validate script against fact ledger only
    ../.menv/bin/python make.py V5 --publish  # rebuild subtitles + compressed MP4 from existing render

Run from work/video/. Reads MINIMAX_API_KEY from ../../.env.
"""
import csv, glob, hashlib, json, os, re, shutil, subprocess, sys, time

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
ENV_BIN = os.path.join(ROOT, "work", ".menv", "bin")
PACK_VID = os.path.join(ROOT, "pack", "videos")

MODEL = "speech-2.6-hd"
VOICE = "English_expressive_narrator"
SPEED = 0.97


def load_env():
    env = {}
    with open(os.path.join(ROOT, ".env")) as fh:
        for line in fh:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def load_script(vid):
    with open(os.path.join(HERE, "scripts", f"{vid}.json"), encoding="utf-8") as fh:
        return json.load(fh)


def check(vid):
    """Every beat cites ledger facts that exist; narration is not empty; ids unique."""
    s = load_script(vid)
    ids = set()
    for f in glob.glob(os.path.join(ROOT, "work", "ledger", "M*.csv")):
        with open(f, newline="", encoding="utf-8") as fh:
            ids |= {r["fact_id"] for r in csv.DictReader(fh)}
    errs, seen, words = [], set(), 0
    for b in s["beats"]:
        if b["id"] in seen:
            errs.append(f"duplicate beat {b['id']}")
        seen.add(b["id"])
        if not b.get("text", "").strip():
            errs.append(f"{b['id']}: empty text")
        words += len(b["text"].split())
        for fid in b.get("facts", []):
            if fid not in ids:
                errs.append(f"{b['id']}: unknown fact {fid}")
        if not b.get("facts") and not b.get("no_facts_reason"):
            errs.append(f"{b['id']}: no facts cited (add facts or no_facts_reason)")
        for sent in re.split(r"(?<=[.!?])\s+", b["text"]):
            if len(sent.split()) > 28:
                errs.append(f"{b['id']}: long sentence ({len(sent.split())} words): {sent[:60]}…")
    print(f"{vid}: {len(s['beats'])} beats, {words} words ≈ {words / 115:.1f} min")
    for e in errs:
        print("  !", e)
    return not errs


def tts(vid):
    key = load_env().get("MINIMAX_API_KEY")
    base = load_env().get("MINIMAX_BASE_URL") or "https://api.minimax.io"
    s = load_script(vid)
    out = os.path.join(HERE, "audio", vid)
    os.makedirs(out, exist_ok=True)
    durations, chars = {}, 0
    for b in s["beats"]:
        spoken = b.get("say", b["text"])  # optional pronunciation-friendly variant
        h = hashlib.sha1(json.dumps([spoken, MODEL, VOICE, SPEED]).encode()).hexdigest()[:12]
        mp3, keyf = os.path.join(out, f"{b['id']}.mp3"), os.path.join(out, f"{b['id']}.key")
        cached = os.path.join(out, "cache", f"{h}.mp3")  # content-addressed: survives beat renumbering
        if not (os.path.exists(mp3) and os.path.exists(keyf) and open(keyf).read() == h) and os.path.exists(cached):
            shutil.copyfile(cached, mp3)
            with open(keyf, "w") as fh:
                fh.write(h)
        if not (os.path.exists(mp3) and os.path.exists(keyf) and open(keyf).read() == h):
            payload = {"model": MODEL, "text": spoken, "stream": False,
                       "voice_setting": {"voice_id": VOICE, "speed": SPEED, "vol": 1, "pitch": 0},
                       "audio_setting": {"sample_rate": 44100, "bitrate": 128000, "format": "mp3", "channel": 1}}
            for attempt in range(5):
                try:
                    r = requests.post(f"{base}/v1/t2a_v2", json=payload, timeout=120,
                                      headers={"Authorization": f"Bearer {key}"})
                    d = r.json()
                    if d.get("base_resp", {}).get("status_code") == 0:
                        break
                    print(f"  {b['id']}: {d.get('base_resp')} (retry {attempt + 1})")
                except Exception as e:  # network hiccup
                    print(f"  {b['id']}: {e} (retry {attempt + 1})")
                time.sleep(3 * (attempt + 1))
            else:
                sys.exit(f"TTS failed for {vid}/{b['id']}")
            with open(mp3, "wb") as fh:
                fh.write(bytes.fromhex(d["data"]["audio"]))
            with open(keyf, "w") as fh:
                fh.write(h)
            os.makedirs(os.path.dirname(cached), exist_ok=True)
            shutil.copyfile(mp3, cached)
            chars += len(spoken)
            print(f"  tts {b['id']} ({len(spoken)} chars)")
        durations[b["id"]] = probe(mp3)
    # drop stale beats
    for f in glob.glob(os.path.join(out, "b*.mp3")):
        if os.path.basename(f)[:-4] not in durations:
            os.remove(f)
            if os.path.exists(f[:-4] + ".key"):
                os.remove(f[:-4] + ".key")
    with open(os.path.join(out, "durations.json"), "w") as fh:
        json.dump(durations, fh, indent=1)
    print(f"{vid}: narration {sum(durations.values()) / 60:.1f} min, {chars} new chars synthesized")


def probe(path):
    r = subprocess.run([os.path.join(ENV_BIN, "ffprobe"), "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", path], capture_output=True, text=True, check=True)
    return round(float(r.stdout.strip()), 3)


def render(vid, draft=False):
    q = "-ql" if draft else "-qh"
    cmd = [os.path.join(ENV_BIN, "manim"), q, "--disable_caching", "--media_dir", os.path.join(HERE, "build", vid),
           os.path.join(HERE, "scenes", f"{vid}.py"), vid]
    env = dict(os.environ, PATH=ENV_BIN + os.pathsep + os.environ["PATH"], PYTHONPATH=HERE)
    subprocess.run(cmd, cwd=HERE, env=env, check=True)
    res = "480p30" if draft else "1080p30"
    return os.path.join(HERE, "build", vid, "videos", vid, res, f"{vid}.mp4")


def fmt(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"


def chunks(text, max_chars=84):
    """Split narration into subtitle-sized pieces: sentences, then equal-length word splits."""
    out = []
    for sent in re.split(r"(?<=[.!?])\s+", text.strip()):
        n = -(-len(sent) // max_chars)  # pieces needed
        if n <= 1:
            if sent:
                out.append(sent)
            continue
        spaces = [i for i, ch in enumerate(sent) if ch == " "]
        cuts = sorted({min(spaces, key=lambda i: abs(i - k * len(sent) / n)) for k in range(1, n)})
        for a, z in zip([0] + cuts, cuts + [len(sent)]):
            out.append(sent[a:z].strip())
    return out


def srt(vid):
    s = load_script(vid)
    with open(os.path.join(HERE, "audio", vid, "timeline.json")) as fh:
        timeline = {b: (a, z) for b, a, z in json.load(fh)}
    lines, n = [], 0
    for b in s["beats"]:
        a, z = timeline[b["id"]]
        parts = chunks(b["text"])
        total = sum(len(p) for p in parts)
        t = a
        for p in parts:
            d = (z - a) * len(p) / total
            n += 1
            lines.append(f"{n}\n{fmt(t)} --> {fmt(t + d - 0.05)}\n{p}\n")
            t += d
    return "\n".join(lines)


def publish(vid, mp4):
    s = load_script(vid)
    os.makedirs(PACK_VID, exist_ok=True)
    name = f"{vid}-{s['slug']}"
    srt_path = os.path.join(PACK_VID, name + ".srt")
    with open(srt_path, "w", encoding="utf-8") as fh:
        fh.write(srt(vid))
    out = os.path.join(PACK_VID, name + ".mp4")
    subprocess.run([os.path.join(ENV_BIN, "ffmpeg"), "-y", "-v", "error", "-i", mp4, "-i", srt_path,
                    "-map", "0:v", "-map", "0:a", "-map", "1", "-c:v", "libx264", "-crf", "22", "-preset", "medium",
                    "-tune", "animation", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                    "-c:s", "mov_text", "-metadata:s:s:0", "language=eng",
                    "-metadata", f"title={s['title']}", "-movflags", "+faststart", out], check=True)
    # WebVTT for the HTML player
    with open(os.path.join(PACK_VID, name + ".vtt"), "w", encoding="utf-8") as fh:
        fh.write("WEBVTT\n\n" + re.sub(r"(\d\d:\d\d:\d\d),(\d\d\d)", r"\1.\2", srt(vid)))
    print(f"published {out} ({probe(out) / 60:.1f} min)")


if __name__ == "__main__":
    vid = sys.argv[1]
    flags = set(sys.argv[2:])
    ok = check(vid)
    if "--check" in flags:
        sys.exit(0 if ok else 1)
    tts(vid)
    if "--tts" in flags:
        sys.exit(0)
    if "--publish" in flags:  # re-mux subtitles / re-encode the existing 1080p render
        publish(vid, os.path.join(HERE, "build", vid, "videos", vid, "1080p30", f"{vid}.mp4"))
        sys.exit(0)
    mp4 = render(vid, draft="--draft" in flags)
    if "--draft" not in flags:
        publish(vid, mp4)
    else:
        print("draft:", mp4)

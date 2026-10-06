"""Chalkboard theme + beat-synced scene base for the innate immunity videos.

Usage in a scene file (work/video/scenes/V5.py):

    from chalk import *

    class V5(ChalkScene):
        VIDEO_ID = "V5"
        def construct(self):
            with self.beat("b01"):          # plays audio/V5/b01.mp3, waits until it ends
                t = self.title_card("Complement made easy")
                self.play(Write(t), run_time=self.fit(2))
            ...

Rules: every beat id in scripts/<VIDEO_ID>.json must be used exactly once, in order.
"""
import json
import os
from contextlib import contextmanager

import numpy as np
from manim import *  # noqa: F401,F403

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------- palette (chalk on dark green board) ----------
BOARD = "#1E3A2F"
CHALK = "#F2F0E6"     # main text
YELLOW = "#F4E285"    # emphasis, key terms
PINK = "#F2A2B8"      # disease, danger, defects
BLUE = "#9AD1F5"      # cells, receptors
GREEN = "#A8E6A1"     # good outcome, normal
ORANGE = "#F7B57A"    # drugs, interventions
GREY = "#9BA89F"      # secondary labels, sources
FONT = "Chalkboard SE"

config.background_color = BOARD
config.frame_rate = 30


def _board_texture():
    """Make a subtle chalk-dust texture PNG once and reuse it."""
    path = os.path.join(HERE, "assets", "board.png")
    if os.path.exists(path):
        return path
    os.makedirs(os.path.dirname(path), exist_ok=True)
    from PIL import Image, ImageFilter
    rng = np.random.default_rng(7)
    w, h = 1920, 1080
    base = np.array([0x1E, 0x3A, 0x2F], dtype=float)
    noise = rng.normal(0, 1, (h // 4, w // 4))
    img = Image.fromarray(((noise - noise.min()) / np.ptp(noise) * 255).astype("uint8"))
    img = img.resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(6))
    n = np.asarray(img, dtype=float) / 255 - 0.5
    # radial vignette + faint eraser smudges
    yy, xx = np.mgrid[0:h, 0:w]
    vig = 1 - 0.35 * (((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    grain = rng.normal(0, 2.0, (h, w))
    rgb = np.clip(base[None, None, :] * vig[..., None] + n[..., None] * 14 + grain[..., None], 0, 255)
    Image.fromarray(rgb.astype("uint8")).save(path)
    return path


# ---------- text helpers ----------
def T(text, size=36, color=CHALK, weight=NORMAL, **kw):
    """Chalk text. Use for every on-screen word."""
    return Text(text, font=FONT, font_size=size, color=color, weight=weight, **kw)


def Tm(markup, size=36, color=CHALK, **kw):
    """Pango markup text, e.g. Tm('C3 <span foreground=\"#F4E285\">convertase</span>')."""
    return MarkupText(markup, font=FONT, font_size=size, color=color, **kw)


def bullet_list(items, size=32, color=CHALK, bullet="•", buff=0.28, width=None):
    rows = VGroup(*[
        VGroup(T(bullet, size, YELLOW), T(it, size, color)).arrange(RIGHT, buff=0.2, aligned_edge=UP)
        for it in items])
    rows.arrange(DOWN, aligned_edge=LEFT, buff=buff)
    if width and rows.width > width:
        rows.scale_to_fit_width(width)
    return rows


def chalk_box(mob, color=CHALK, buff=0.25, corner=0.15, stroke=3):
    return RoundedRectangle(corner_radius=corner, width=mob.width + 2 * buff, height=mob.height + 2 * buff,
                            stroke_color=color, stroke_width=stroke).move_to(mob)


def label_box(text, color=BLUE, size=30, buff=0.22, fill_opacity=0.12):
    """A boxed label (node in a pathway)."""
    t = T(text, size, color)
    b = chalk_box(t, color, buff).set_fill(color, fill_opacity)
    return VGroup(b, t)


def _bbox_exit(mob, direction):
    """Point where a ray from mob's centre along `direction` leaves its bounding box."""
    c = mob.get_center()
    hw, hh = mob.width / 2, mob.height / 2
    dx, dy = direction[0], direction[1]
    sx = hw / abs(dx) if abs(dx) > 1e-9 else np.inf
    sy = hh / abs(dy) if abs(dy) > 1e-9 else np.inf
    s = min(sx, sy)
    return c + np.array([dx * s, dy * s, 0.0])


bbox_exit = _bbox_exit  # public alias for custom connectors


def chalk_arrow(a, b, color=CHALK, buff=0.15, stroke=4, tip=0.22, **kw):
    """Arrow between two points or mobjects."""
    ca = a.get_center() if isinstance(a, Mobject) else np.array(a, dtype=float)
    cb = b.get_center() if isinstance(b, Mobject) else np.array(b, dtype=float)
    d = cb - ca
    start = _bbox_exit(a, d) if isinstance(a, Mobject) else ca
    end = _bbox_exit(b, -d) if isinstance(b, Mobject) else cb
    return Arrow(start, end, buff=buff, color=color, stroke_width=stroke, tip_length=tip,
                 max_tip_length_to_length_ratio=0.3, **kw)


def strike(mob, color=PINK, stroke=6):
    """Red-chalk cross-out over a mobject (knock-out / deficiency)."""
    return VGroup(Line(mob.get_corner(UL), mob.get_corner(DR), color=color, stroke_width=stroke),
                  Line(mob.get_corner(DL), mob.get_corner(UR), color=color, stroke_width=stroke))


def cell(radius=0.6, color=BLUE, nucleus=True, label=None, size=26):
    """Simple cartoon cell."""
    c = Circle(radius, color=color, stroke_width=4).set_fill(color, 0.12)
    g = VGroup(c)
    if nucleus:
        g.add(Ellipse(width=radius * 0.9, height=radius * 0.65, color=color, stroke_width=3)
              .set_fill(color, 0.25).shift(RIGHT * radius * 0.15 + UP * radius * 0.1))
    if label:
        g.add(T(label, size, color).next_to(c, DOWN, buff=0.15))
    return g


# ---------- scene base ----------
class ChalkScene(Scene):
    VIDEO_ID = None

    def setup(self):
        super().setup()
        with open(os.path.join(HERE, "scripts", f"{self.VIDEO_ID}.json"), encoding="utf-8") as fh:
            self.script = json.load(fh)
        dur_path = os.path.join(HERE, "audio", self.VIDEO_ID, "durations.json")
        with open(dur_path, encoding="utf-8") as fh:
            self.durations = json.load(fh)
        self.beat_order = [b["id"] for b in self.script["beats"]]
        self.used = []
        self.timeline = []          # (beat_id, start_s, end_s) -> SRT
        self.add(ImageMobject(_board_texture()).scale_to_fit_height(config.frame_height).set_z_index(-100))
        self._beat_start = None
        self._beat_dur = 0

    # -- timing helpers --
    @property
    def t(self):
        return self.renderer.time

    def elapsed(self):
        return self.t - self._beat_start

    def remaining(self):
        """Seconds of narration left in the current beat (never < 0.3)."""
        return max(0.3, self._beat_dur - self.elapsed())

    def fit(self, seconds):
        """Clamp a run_time so it does not overrun the beat audio."""
        return max(0.3, min(seconds, self._beat_dur - self.elapsed() - 0.1))

    @property
    def bd(self):
        """Duration of the current beat's audio."""
        return self._beat_dur

    @contextmanager
    def beat(self, beat_id, pad=0.35):
        expected = self.beat_order[len(self.used)] if len(self.used) < len(self.beat_order) else None
        if beat_id != expected:
            raise ValueError(f"{self.VIDEO_ID}: beat {beat_id!r} used out of order (expected {expected!r})")
        self.used.append(beat_id)
        self._beat_dur = self.durations[beat_id]
        self._beat_start = self.t
        self.add_sound(os.path.join(HERE, "audio", self.VIDEO_ID, f"{beat_id}.mp3"))
        yield
        left = self._beat_dur - self.elapsed()
        if left > 0:
            self.wait(left)
        self.timeline.append((beat_id, self._beat_start, self._beat_start + self._beat_dur))
        self.wait(pad)

    def tear_down(self):
        missing = [b for b in self.beat_order if b not in self.used]
        if missing:
            raise ValueError(f"{self.VIDEO_ID}: beats never played: {missing}")
        out = os.path.join(HERE, "audio", self.VIDEO_ID, "timeline.json")
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(self.timeline, fh, indent=1)
        super().tear_down()

    # -- common layouts --
    def title_card(self, title, subtitle=None):
        t = T(title, 64, YELLOW)
        g = VGroup(t)
        if subtitle:
            g.add(T(subtitle, 34, CHALK).next_to(t, DOWN, buff=0.4))
        line = Line(LEFT * 3, RIGHT * 3, color=CHALK, stroke_width=3).next_to(g, DOWN, buff=0.35)
        g.add(line)
        return g.move_to(ORIGIN)

    def header(self, text, color=YELLOW):
        """Section header at the top edge."""
        h = T(text, 44, color).to_edge(UP, buff=0.4)
        u = Line(h.get_corner(DL), h.get_corner(DR), color=color, stroke_width=3).shift(DOWN * 0.12)
        return VGroup(h, u)

    def source_tag(self, text):
        """Small grey citation in the bottom-right corner, e.g. 'Abbas p.307'.
        Replaces the previous tag if it is still on screen (no stacking)."""
        old = getattr(self, "_src_tag", None)
        if old is not None and old in self.mobjects:
            self.remove(old)
        self._src_tag = T(text, 20, GREY).to_corner(DR, buff=0.3)
        return self._src_tag

    def clear_board(self, run_time=0.6):
        mobs = [m for m in self.mobjects if not isinstance(m, ImageMobject)]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=run_time)

from chalk import *


# ---------- local helpers (V5 only) ----------
def membrane(x0, x1, y, color=GREY, gap=0.45):
    """Lipid bilayer: two chalk lines with little head-groups."""
    g = VGroup()
    for yy in (y + gap / 2, y - gap / 2):
        g.add(Line([x0, yy, 0], [x1, yy, 0], color=color, stroke_width=3))
    n = int((x1 - x0) / 0.3)
    for i in range(n + 1):
        x = x0 + i * (x1 - x0) / n
        g.add(Dot([x, y + gap / 2, 0], radius=0.05, color=color))
        g.add(Dot([x, y - gap / 2, 0], radius=0.05, color=color))
    return g


def antibody(x, y_tip, color=BLUE, h=1.2):
    """Antibody 'Y' standing on a surface: arms touch the surface at y_tip, stem points up."""
    fork = y_tip + h * 0.45
    top = y_tip + h
    return VGroup(Line([x - 0.35, y_tip, 0], [x, fork, 0], color=color, stroke_width=5),
                  Line([x + 0.35, y_tip, 0], [x, fork, 0], color=color, stroke_width=5),
                  Line([x, fork, 0], [x, top, 0], color=color, stroke_width=5))


def flame(scale=1.0, color=YELLOW):
    pts = [[0, 1.0, 0], [0.35, 0.35, 0], [0.4, -0.1, 0], [0.2, -0.45, 0], [0, -0.5, 0],
           [-0.2, -0.45, 0], [-0.4, -0.1, 0], [-0.35, 0.35, 0]]
    f = Polygon(*pts, color=color, stroke_width=4).set_fill(color, 0.25)
    f.round_corners(0.12)
    return f.scale(scale)


def blk(text, color=BLUE, w=0.7, h=1.3, size=26):
    """Vertical protein block for the MAC."""
    r = RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=color,
                         stroke_width=3).set_fill(color, 0.18)
    return VGroup(r, T(text, size, color).move_to(r))


def tag(text, color=YELLOW, size=24):
    return label_box(text, color, size, buff=0.1, fill_opacity=0.15)


class V5(ChalkScene):
    VIDEO_ID = "V5"

    def src(self, text):
        """Show one citation tag at a time."""
        old = getattr(self, "_src", None)
        if old is not None and old in self.mobjects:
            self.remove(old)
        self._src = self.source_tag(text)
        self.add(self._src)

    def rt(self, frac):
        """Run time as a fraction of the current beat, clamped to the audio."""
        return self.fit(self.bd * frac)

    def construct(self):
        # ---------------- b01 hook ----------------
        with self.beat("b01"):
            title = self.title_card("Complement made easy", "Innate immunity · Video 5")
            self.play(Write(title), run_time=self.rt(0.25))
            soup_txt = ["C3b", "C4b2a", "C5a", "Bb", "iC3b", "C1q", "MAC", "C3bBb", "C5b-9", "MASP2"]
            rng = np.random.default_rng(3)
            soup = VGroup()
            spots = [(-5, 2.6), (-2.8, 2.9), (2.6, 2.9), (5, 2.5), (-5.3, -1.0), (-3.3, -2.6),
                     (0, -2.9), (3.2, -2.6), (5.3, -1.1), (5.5, 1.7)]
            for s, (x, y) in zip(soup_txt, spots):
                soup.add(T(s, 30, rng.choice([BLUE, PINK, GREEN, YELLOW])).move_to([x, y, 0])
                         .rotate(rng.uniform(-0.3, 0.3)))
            self.play(LaggedStart(*[FadeIn(m, scale=0.6) for m in soup], lag_ratio=0.12),
                      run_time=self.rt(0.3))
            rules = T("a few simple rules", 36, GREEN).next_to(title, DOWN, buff=0.5)
            self.play(soup.animate.arrange_in_grid(2, 5, buff=(0.5, 0.3)).scale(0.8).to_edge(DOWN, buff=0.6)
                      .set_color(CHALK).set_opacity(0.8),
                      Write(rules), run_time=self.rt(0.3))

        # ---------------- b02 what it is ----------------
        with self.beat("b02"):
            self.clear_board(0.5)
            h = self.header("What is complement?")
            comp = label_box("Complement", YELLOW, 40)
            comp.move_to([0, 1.7, 0])
            ab = label_box("antibody immunity", BLUE, 30).move_to([-3.3, 0.2, 0])
            inn = label_box("innate immunity", GREEN, 30).move_to([3.3, 0.2, 0])
            self.play(FadeIn(h), Write(comp), run_time=self.rt(0.12))
            self.play(GrowArrow(chalk_arrow(comp, ab)), FadeIn(ab, shift=DOWN * 0.3), run_time=self.rt(0.12))
            self.play(GrowArrow(chalk_arrow(comp, inn)), FadeIn(inn, shift=DOWN * 0.3), run_time=self.rt(0.12))
            self.src(("Abbas p.300; Janeway p.49"))
            zym = label_box("zymogen (inactive)", GREY, 30).move_to([-3.2, -2.1, 0])
            act = label_box("active protease", YELLOW, 30).move_to([3.4, -2.1, 0])
            self.play(FadeIn(zym, shift=RIGHT * 0.3), run_time=self.rt(0.12))
            cut = chalk_arrow(zym, act, YELLOW)
            lbl = T("cleaved", 26, YELLOW).next_to(cut, UP, buff=0.1)
            self.play(GrowArrow(cut), Write(lbl), run_time=self.rt(0.12))
            self.play(TransformFromCopy(zym, act), run_time=self.rt(0.15))
            self.play(Indicate(act, color=YELLOW), run_time=self.rt(0.1))

        # ---------------- b03 amplification ----------------
        with self.beat("b03"):
            self.clear_board(0.5)
            h = self.header("Amplification")
            self.play(FadeIn(h), run_time=0.4)
            cols = [1, 3, 9, 27]
            xs = [-4.8, -2.2, 0.6, 3.6]
            levels = []
            for n, x in zip(cols, xs):
                ys = np.linspace(-2.6, 2.0, n) if n > 1 else [ -0.3]
                levels.append(VGroup(*[Dot([x, y, 0], radius=0.13 if n < 27 else 0.07, color=YELLOW) for y in ys]))
            self.play(FadeIn(levels[0], scale=2), run_time=self.rt(0.08))
            for i in range(1, 4):
                lines = VGroup()
                for j, d in enumerate(levels[i]):
                    parent = levels[i - 1][j // 3]
                    lines.add(Line(parent.get_center(), d.get_center(), color=GREY, stroke_width=2))
                self.play(Create(lines), FadeIn(levels[i], lag_ratio=0.05), run_time=self.rt(0.15))
            note = T("each step cleaves many more", 30, GREEN).move_to([1.5, -3.2, 0])
            self.play(Write(note), run_time=self.rt(0.15))
            dom = T("≈ falling dominoes", 28, GREY).next_to(levels[3], RIGHT, buff=0.3)
            self.play(FadeIn(dom), run_time=self.rt(0.1))
            self.src(("Janeway p.49"))

        # ---------------- b04 naming ----------------
        with self.beat("b04"):
            self.clear_board(0.5)
            h = self.header("Two naming rules")
            self.play(FadeIn(h), run_time=0.4)
            r1 = T("1. big = b, small = a", 32, YELLOW).move_to([-3.6, 2.3, 0])
            c3 = label_box("C3", BLUE, 34).move_to([-4.5, 1.0, 0])
            c3a = label_box("C3a", PINK, 24).move_to([-1.6, 1.6, 0])
            c3b = label_box("C3b", GREEN, 40).move_to([-1.4, 0.3, 0])
            self.play(Write(r1), FadeIn(c3), run_time=self.rt(0.1))
            self.play(GrowArrow(chalk_arrow(c3, c3a)), GrowArrow(chalk_arrow(c3, c3b)),
                      TransformFromCopy(c3, c3a), TransformFromCopy(c3, c3b), run_time=self.rt(0.1))
            exc = T("exception: C2", 30, PINK).move_to([3.6, 2.3, 0])
            c2 = label_box("C2", BLUE, 34).move_to([2.2, 1.0, 0])
            c2a = label_box("C2a", GREEN, 40).move_to([5.0, 1.6, 0])
            c2b = label_box("C2b", PINK, 24).move_to([5.0, 0.3, 0])
            self.play(Write(exc), FadeIn(c2), run_time=self.rt(0.1))
            self.play(GrowArrow(chalk_arrow(c2, c2a)), GrowArrow(chalk_arrow(c2, c2b)),
                      TransformFromCopy(c2, c2a), TransformFromCopy(c2, c2b), run_time=self.rt(0.1))
            self.play(Circumscribe(c2a, color=YELLOW), run_time=self.rt(0.08))
            r2 = T("2. numbers = order of discovery, not order of action", 30, YELLOW).move_to([0, -1.1, 0])
            self.play(Write(r2), run_time=self.rt(0.12))
            seq = ["C1", "C4", "C2", "C3", "C5", "C6", "C7", "C8", "C9"]
            row = VGroup(*[label_box(s, BLUE if i < 4 else GREEN, 28, buff=0.14) for i, s in enumerate(seq)])
            row.arrange(RIGHT, buff=0.42).move_to([0, -2.4, 0])
            arrows = VGroup(*[chalk_arrow(a, b, GREY, buff=0.05, stroke=3, tip=0.15) for a, b in zip(row, row[1:])])
            self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.2) for m in row], lag_ratio=0.15),
                      Create(arrows), run_time=self.rt(0.2))
            self.play(Indicate(VGroup(row[1], row[2]), color=PINK), run_time=self.rt(0.08))
            self.src(("Janeway p.49; Abbas p.305"))

        # ---------------- b05 three pathways ----------------
        with self.beat("b05"):
            self.clear_board(0.5)
            h = self.header("Three ways in")
            self.play(FadeIn(h), run_time=0.4)
            specs = [("Classical", "antibody + antigen", BLUE),
                     ("Lectin", "lectins bind microbial sugars", BLUE),
                     ("Alternative", "microbial surface, no antibody", BLUE)]
            paths = VGroup()
            for i, (n, trig, c) in enumerate(specs):
                b = label_box(n, YELLOW, 32)
                t = T(trig, 26, c)
                g = VGroup(b, t).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
                g.move_to([-4.2, 1.9 - i * 1.75, 0], aligned_edge=LEFT).shift(LEFT * 0)
                g.to_edge(LEFT, buff=0.6).set_y(1.9 - i * 1.75)
                paths.add(g)
            for g in paths:
                self.play(FadeIn(g[0], shift=RIGHT * 0.3), Write(g[1]), run_time=self.rt(0.15))
            jan = T("Janeway: all three can start without antibody", 26, GREY).move_to([0, -3.2, 0])
            self.play(FadeIn(jan), run_time=self.rt(0.12))
            self.src(("Abbas p.301; Janeway p.71"))

        # ---------------- b06 central event ----------------
        with self.beat("b06"):
            self.play(FadeOut(jan), run_time=0.4)
            conv = label_box("C3 convertase", YELLOW, 32).move_to([0.9, 0.2, 0])
            arrs = VGroup(*[chalk_arrow(g[0].get_right() + RIGHT * 0.1, conv, CHALK) for g in paths])
            self.play(LaggedStart(*[GrowArrow(a) for a in arrs], lag_ratio=0.2), FadeIn(conv),
                      run_time=self.rt(0.15))
            c3 = label_box("C3", BLUE, 30).move_to([3.9, 0.2, 0])
            self.play(GrowArrow(chalk_arrow(conv, c3)), FadeIn(c3), run_time=self.rt(0.08))
            c3a = label_box("C3a", PINK, 26).move_to([5.6, 1.6, 0])
            mem = membrane(2.2, 6.4, -2.6)
            surf = T("target surface", 24, GREY).next_to(mem, DOWN, buff=0.1)
            c3b = label_box("C3b", GREEN, 32).move_to([4.2, -1.95, 0])
            self.play(TransformFromCopy(c3, c3a), Create(mem), FadeIn(surf), run_time=self.rt(0.12))
            self.play(TransformFromCopy(c3, c3b), run_time=self.rt(0.1))
            bond = T("covalent bond", 24, GREEN).next_to(c3b, LEFT, buff=0.15)
            self.play(Flash(c3b.get_bottom(), color=YELLOW), Write(bond), run_time=self.rt(0.1))
            self.src(("Abbas p.301; Janeway p.52"))
            miss = label_box("C3b", GREEN, 28).move_to([5.7, 0.2, 0])
            self.play(FadeIn(miss), run_time=self.rt(0.06))
            dead = T("no surface → hydrolyzed, inactive", 26, PINK).move_to([3.0, -0.95, 0])
            self.play(miss.animate.set_color(GREY).set_opacity(0.4), Write(dead), run_time=self.rt(0.15))

        # ---------------- b07 host vs microbe ----------------
        with self.beat("b07"):
            self.clear_board(0.5)
            h = self.header("Why microbes, not us?")
            host = cell(1.3, GREEN).move_to([-3.4, -0.1, 0])
            host.add(T("host cell", 30, GREEN).next_to(host, DOWN, buff=0.4))
            bug = Ellipse(width=3.2, height=1.9, color=PINK, stroke_width=4).set_fill(PINK, 0.12).move_to([3.4, 0.0, 0])
            bug_l = T("microbe", 30, PINK).next_to(bug, DOWN, buff=0.2)
            self.play(FadeIn(h), FadeIn(host), FadeIn(bug), Write(bug_l), run_time=self.rt(0.15))
            shields = VGroup()
            for ang in np.linspace(0, TAU, 8, endpoint=False):
                p = host[0].get_center() + 1.3 * np.array([np.cos(ang), np.sin(ang), 0])
                shields.add(Square(0.28, color=GREEN, stroke_width=3).set_fill(GREEN, 0.6).move_to(p).rotate(ang))
            reg = T("regulators", 28, GREEN).next_to(host, UP, buff=0.35)
            self.play(LaggedStart(*[GrowFromCenter(s) for s in shields], lag_ratio=0.1), Write(reg),
                      run_time=self.rt(0.25))
            dots = VGroup()
            for ang in np.linspace(0, TAU, 12, endpoint=False):
                p = bug.get_center() + np.array([1.6 * np.cos(ang), 0.95 * np.sin(ang), 0])
                dots.add(Dot(p, radius=0.11, color=YELLOW))
            c3bl = T("C3b everywhere", 28, YELLOW).next_to(bug, UP, buff=0.35)
            self.play(LaggedStart(*[FadeIn(d, scale=2) for d in dots], lag_ratio=0.06), Write(c3bl),
                      run_time=self.rt(0.3))
            self.src(("Abbas p.301"))

        # ---------------- b08 classical: C1 ----------------
        with self.beat("b08"):
            self.clear_board(0.5)
            h = self.header("Classical pathway")
            surf = Line([-6, -2.4, 0], [1.8, -2.4, 0], color=PINK, stroke_width=5)
            surf_l = T("antigen on microbe", 24, PINK).next_to(surf, DOWN, buff=0.12)
            self.play(FadeIn(h), Create(surf), FadeIn(surf_l), run_time=self.rt(0.08))
            ab1, ab2 = antibody(-2.9, -2.4), antibody(-1.3, -2.4)
            self.play(Create(ab1), Create(ab2), run_time=self.rt(0.1))
            # C1q "bouquet" docking on the two Fc stems
            body = Circle(0.35, color=YELLOW, stroke_width=4).set_fill(YELLOW, 0.2).move_to([-2.1, 0.35, 0])
            legs = VGroup(*[Line(body.get_bottom(), [x, -1.05, 0], color=YELLOW, stroke_width=4) for x in (-2.9, -1.3)])
            heads = VGroup(*[Dot([x, -1.1, 0], radius=0.13, color=YELLOW) for x in (-2.9, -1.3)])
            c1q = VGroup(body, legs, heads)
            c1q_l = T("C1q", 30, YELLOW).next_to(body, LEFT, buff=0.2)
            rs = T("C1r, C1s = proteases", 26, BLUE).next_to(body, UP, buff=0.2)
            self.play(FadeIn(c1q, shift=DOWN * 0.5), Write(c1q_l), run_time=self.rt(0.12))
            self.play(Write(rs), run_time=self.rt(0.1))
            facts = bullet_list(["IgG: CH2 domain", "IgM: CH3 domain"], 28).move_to([4.3, 1.2, 0])
            self.play(Write(facts), run_time=self.rt(0.15))
            two = T("needs ≥ 2 heavy chains", 28, GREEN).move_to([4.2, -0.4, 0])
            self.play(Write(two), Indicate(heads, color=GREEN), run_time=self.rt(0.12))
            free_ab = antibody(4.2, -2.7, GREY, 0.9)
            free_l = T("free antibody: no", 26, PINK).next_to(free_ab, UP, buff=0.2)
            self.play(FadeIn(free_ab), run_time=self.rt(0.06))
            self.play(Create(strike(free_ab, PINK)), Write(free_l), run_time=self.rt(0.08))
            self.src(("Abbas p.305"))

        # ---------------- b09 antibody ranking ----------------
        with self.beat("b09"):
            self.clear_board(0.5)
            h = self.header("Who fixes complement best?")
            self.play(FadeIn(h), run_time=0.4)
            rows = [("IgM", "binds ≥ 2 C1q  →  best", GREEN),
                    ("IgG1, IgG3", "efficient", GREEN),
                    ("IgG2", "weak", YELLOW),
                    ("IgG4", "no activation", PINK)]
            grp = VGroup()
            for i, (a, b, c) in enumerate(rows):
                l = label_box(a, c, 32).move_to([-2.6, 1.7 - i * 1.3, 0])
                r = T(b, 30, c).next_to(l, RIGHT, buff=0.6)
                r.set_x(-0.5 + r.width / 2)
                grp.add(VGroup(l, r))
            for g in grp:
                self.play(FadeIn(g[0], shift=RIGHT * 0.3), Write(g[1]), run_time=self.rt(0.17))
            self.play(Create(strike(grp[3][0])), run_time=self.rt(0.08))
            self.src(("Abbas p.305"))

        # ---------------- b10 classical cascade ----------------
        with self.beat("b10"):
            self.clear_board(0.5)
            h = self.header("Classical cascade")
            mem = membrane(-6.2, 6.2, -2.3)
            self.play(FadeIn(h), Create(mem), run_time=self.rt(0.06))
            c1 = VGroup(*[label_box(s, BLUE, 30) for s in ("C1q", "C1r", "C1s")]).arrange(RIGHT, buff=0.8)
            c1.move_to([-3.6, 1.4, 0])
            a1, a2 = chalk_arrow(c1[0], c1[1]), chalk_arrow(c1[1], c1[2])
            self.play(FadeIn(c1[0]), run_time=self.rt(0.05))
            self.play(GrowArrow(a1), FadeIn(c1[1]), run_time=self.rt(0.08))
            self.play(GrowArrow(a2), FadeIn(c1[2]), run_time=self.rt(0.08))
            c4 = label_box("C4", BLUE, 30).move_to([1.2, 1.4, 0])
            self.play(GrowArrow(chalk_arrow(c1[2], c4)), FadeIn(c4), run_time=self.rt(0.08))
            c4b = label_box("C4b", GREEN, 32).move_to([1.0, -1.65, 0])
            self.play(TransformFromCopy(c4, c4b), run_time=self.rt(0.1))
            c2 = label_box("C2", BLUE, 30).move_to([4.2, 1.4, 0])
            self.play(FadeIn(c2, shift=LEFT * 0.4), run_time=self.rt(0.06))
            cut = T("cut by C1s", 24, BLUE).next_to(c2, DOWN, buff=0.15)
            c2a = label_box("C2a", GREEN, 32).next_to(c4b, RIGHT, buff=0.0)
            self.play(Write(cut), run_time=self.rt(0.06))
            self.play(TransformFromCopy(c2, c2a), run_time=self.rt(0.1))
            res = T("C4b2a = classical C3 convertase", 32, YELLOW).move_to([0, -3.3, 0])
            self.play(Write(res), Circumscribe(VGroup(c4b, c2a), color=YELLOW), run_time=self.rt(0.15))
            self.src(("Abbas p.305"))

        # ---------------- b11 lectin ----------------
        with self.beat("b11"):
            self.clear_board(0.5)
            h = self.header("Lectin pathway: the twin")
            self.play(FadeIn(h), run_time=0.4)
            lt = T("Classical", 32, YELLOW).move_to([-3.4, 2.3, 0])
            rt_ = T("Lectin", 32, YELLOW).move_to([3.4, 2.3, 0])
            l1 = label_box("C1q reads antibody", BLUE, 28).move_to([-3.4, 1.2, 0])
            l2 = label_box("C1s", BLUE, 28).move_to([-3.4, -0.3, 0])
            r1 = label_box("MBL, ficolins read sugars", BLUE, 28).move_to([3.4, 1.2, 0])
            r2 = label_box("MASP2", BLUE, 28).move_to([3.4, -0.3, 0])
            self.play(Write(lt), FadeIn(l1), GrowArrow(chalk_arrow(l1, l2)), FadeIn(l2), run_time=self.rt(0.15))
            self.play(Write(rt_), FadeIn(r1), run_time=self.rt(0.15))
            self.play(GrowArrow(chalk_arrow(r1, r2)), FadeIn(r2), run_time=self.rt(0.1))
            lock = label_box("cleave C4 + C2  →  C4b2a", GREEN, 32).move_to([0, -2.0, 0])
            self.play(GrowArrow(chalk_arrow(l2, lock)), GrowArrow(chalk_arrow(r2, lock)), FadeIn(lock),
                      run_time=self.rt(0.15))
            keys = T("two keys, one lock", 28, GREY).move_to([0, -3.2, 0])
            self.play(Write(keys), Indicate(lock, color=YELLOW), run_time=self.rt(0.12))
            self.src(("Abbas p.306–307; Janeway p.54"))

        # ---------------- b12 tick-over ----------------
        with self.beat("b12"):
            self.clear_board(0.5)
            h = self.header("Alternative pathway: always idling")
            fl = flame(0.8).move_to([-5.6, 1.5, 0])
            fll = T("pilot light", 24, YELLOW).next_to(fl, DOWN, buff=0.15)
            self.play(FadeIn(h), Create(fl), FadeIn(fll), run_time=self.rt(0.08))
            c3 = label_box("C3", BLUE, 30).move_to([-4.0, 1.5, 0])
            h2o = label_box("C3(H2O)", BLUE, 30).move_to([-0.6, 1.5, 0])
            tick = T("tick-over: 1–2 % per hour", 26, YELLOW).next_to(VGroup(c3, h2o), UP, buff=0.25)
            self.play(FadeIn(c3), run_time=self.rt(0.06))
            self.play(GrowArrow(chalk_arrow(c3, h2o)), FadeIn(h2o), Write(tick), run_time=self.rt(0.15))
            fb = label_box("factor B", BLUE, 30).move_to([2.6, 1.5, 0])
            plus = T("+", 36).move_to((h2o.get_right() + fb.get_left()) / 2)
            self.play(FadeIn(plus), FadeIn(fb, shift=LEFT * 0.3), run_time=self.rt(0.1))
            fd = label_box("factor D cuts B", YELLOW, 28).move_to([4.6, 0.0, 0])
            self.play(FadeIn(fd), GrowArrow(chalk_arrow(fd, fb, YELLOW)), run_time=self.rt(0.1))
            fluid = label_box("C3(H2O)Bb: short-lived fluid-phase C3 convertase", GREEN, 28).move_to([0, -0.9, 0])
            self.play(TransformFromCopy(VGroup(h2o, fb), fluid), run_time=self.rt(0.15))
            note = label_box("factor D circulates already active (not a zymogen)", YELLOW, 28).move_to([0, -2.6, 0])
            self.play(FadeIn(note, shift=UP * 0.3), run_time=self.rt(0.12))
            self.src(("Abbas p.301; Janeway p.58, p.61"))

        # ---------------- b13 C3bBb + properdin ----------------
        with self.beat("b13"):
            self.clear_board(0.5)
            h = self.header("Alternative C3 convertase")
            mem = membrane(-6.2, 1.2, -1.6)
            surf = T("microbial surface", 24, GREY).next_to(mem, DOWN, buff=0.1)
            c3b = label_box("C3b", GREEN, 32).move_to([-3.6, -0.9, 0])
            self.play(FadeIn(h), Create(mem), FadeIn(surf), FadeIn(c3b), run_time=self.rt(0.1))
            fb = label_box("B", BLUE, 32).move_to([-1.6, 1.6, 0])
            self.play(FadeIn(fb, shift=DOWN * 0.3), run_time=self.rt(0.06))
            self.play(fb.animate.next_to(c3b, RIGHT, buff=0), run_time=self.rt(0.08))
            fd = T("factor D", 28, YELLOW).move_to([-1.0, 0.6, 0])
            self.play(Write(fd), Flash(fb.get_top(), color=YELLOW), run_time=self.rt(0.08))
            bb = label_box("Bb", BLUE, 32).next_to(c3b, RIGHT, buff=0)
            ba = label_box("Ba", GREY, 24).move_to(fb)
            self.play(ReplacementTransform(fb, bb), FadeIn(ba), run_time=self.rt(0.05))
            self.play(ba.animate.shift(UP * 2 + RIGHT * 1.6).set_opacity(0.2), run_time=self.rt(0.08))
            name = T("C3bBb = alternative C3 convertase", 28, YELLOW).move_to([-2.6, 2.3, 0])
            self.play(FadeOut(ba), FadeOut(fd), Write(name), run_time=self.rt(0.1))
            prop = label_box("properdin", GREEN, 26).next_to(VGroup(c3b, bb), UP, buff=0.12)
            st = T("stabilizes, prefers microbes", 24, GREEN).next_to(prop, UP, buff=0.12)
            self.play(FadeIn(prop, shift=DOWN * 0.3), Write(st), run_time=self.rt(0.12))
            twins = VGroup(T("Twins", 32, YELLOW),
                           T("C3  ↔  C4", 30), T("factor B  ↔  C2", 30), T("C3bBb  ↔  C4b2a", 30, GREEN))
            twins.arrange(DOWN, buff=0.35).move_to([4.3, -0.2, 0])
            box = chalk_box(twins, YELLOW)
            self.play(Create(box), LaggedStart(*[Write(t) for t in twins], lag_ratio=0.3), run_time=self.rt(0.2))
            self.src(("Abbas p.301–302, p.306"))

        # ---------------- b14 amplification loop ----------------
        with self.beat("b14"):
            self.clear_board(0.5)
            h = self.header("The amplification loop")
            top = label_box("C3bBb", YELLOW, 36).move_to([0, 1.6, 0])
            bot = label_box("C3b", GREEN, 36).move_to([0, -1.6, 0])
            self.play(FadeIn(h), FadeIn(top), run_time=self.rt(0.06))
            ca1 = CurvedArrow(top.get_right() + RIGHT * 0.1, bot.get_right() + RIGHT * 0.1, angle=-PI / 1.6,
                              color=CHALK, stroke_width=4)
            ca2 = CurvedArrow(bot.get_left() + LEFT * 0.1, top.get_left() + LEFT * 0.1, angle=-PI / 1.6,
                              color=CHALK, stroke_width=4)
            l1 = T("makes", 26, GREY).next_to(ca1, RIGHT, buff=0.1)
            l2 = T("builds", 26, GREY).next_to(ca2, LEFT, buff=0.1)
            self.play(Create(ca1), FadeIn(bot), Write(l1), run_time=self.rt(0.1))
            self.play(Create(ca2), Write(l2), run_time=self.rt(0.1))
            ins = VGroup(*[label_box(s, BLUE, 26) for s in ("classical", "lectin", "alternative")])
            ins.arrange(RIGHT, buff=0.35).move_to([-2.6, -3.0, 0])
            in_arrows = VGroup(*[chalk_arrow(b, bot, BLUE, stroke=3) for b in ins])
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.3) for b in ins], lag_ratio=0.2),
                      LaggedStart(*[GrowArrow(a) for a in in_arrows], lag_ratio=0.2), run_time=self.rt(0.2))
            self.play(Indicate(top), Indicate(bot), run_time=self.rt(0.08))
            fl = flame(0.5).move_to([4.8, 0.5, 0])
            pl = T("pilot light", 26, YELLOW).next_to(fl, DOWN, buff=0.15)
            self.play(Create(fl), Write(pl), run_time=self.rt(0.1))
            fire = T("→ fire on a microbe", 26, YELLOW).move_to([4.6, -2.3, 0])
            self.play(fl.animate.scale(2.2).shift(UP * 0.4), pl.animate.shift(DOWN * 0.25),
                      Write(fire), run_time=self.rt(0.15))
            self.src(("Abbas p.301"))

        # ---------------- b15 C5 convertases ----------------
        with self.beat("b15"):
            self.clear_board(0.5)
            h = self.header("C5 convertase = C3 convertase + C3b")
            self.play(FadeIn(h), run_time=0.4)
            rows = VGroup()
            for i, (lab, a, res) in enumerate([("Classical / lectin", "C4b2a", "C4b2a3b"),
                                               ("Alternative", "C3bBb", "C3bBb3b")]):
                y = 1.6 - i * 1.7
                l = T(lab, 28, GREY).move_to([-4.6, y, 0])
                b1 = label_box(a, BLUE, 32).move_to([-1.6, y, 0])
                p = T("+", 36).move_to([-0.1, y, 0])
                b2 = label_box("C3b", GREEN, 32).move_to([1.2, y, 0])
                eq = T("=", 36).move_to([2.6, y, 0])
                b3 = label_box(res, YELLOW, 32).move_to([4.6, y, 0])
                rows.add(VGroup(l, b1, p, b2, eq, b3))
            for r in rows:
                self.play(Write(r[0]), FadeIn(r[1]), run_time=self.rt(0.08))
                self.play(FadeIn(r[2]), FadeIn(r[3], shift=LEFT * 0.3), run_time=self.rt(0.08))
                self.play(FadeIn(r[4]), TransformFromCopy(VGroup(r[1], r[3]), r[5]), run_time=self.rt(0.1))
            jw = T("Janeway writes: C3b₂Bb", 26, GREY).next_to(rows[1][5], DOWN, buff=0.2)
            self.play(Write(jw), run_time=self.rt(0.1))
            c5 = label_box("C5", BLUE, 30).move_to([-3.2, -2.4, 0])
            cut = T("cut by C2a or Bb", 26, YELLOW).move_to([-0.6, -2.0, 0])
            c5a = label_box("C5a", PINK, 26).move_to([2.2, -1.85, 0])
            c5b = label_box("C5b", GREEN, 30).move_to([2.2, -2.75, 0])
            self.play(FadeIn(c5), Write(cut), run_time=self.rt(0.1))
            self.play(TransformFromCopy(c5, c5a), TransformFromCopy(c5, c5b), run_time=self.rt(0.1))
            self.src(("Abbas p.303, p.306; Janeway p.62"))

        # ---------------- b16 MAC assembly ----------------
        with self.beat("b16"):
            self.clear_board(0.5)
            h = self.header("Membrane attack complex (MAC)")
            mem = membrane(-6.2, 6.2, -1.4, gap=0.7)
            self.play(FadeIn(h), Create(mem), run_time=self.rt(0.06))
            c5b = blk("C5b", GREEN).move_to([-4.6, 0.4, 0])
            nb = T("not covalent", 24, GREY).next_to(c5b, UP, buff=0.15)
            self.play(FadeIn(c5b, shift=DOWN * 0.3), Write(nb), run_time=self.rt(0.1))
            c6 = blk("C6").next_to(c5b, RIGHT, buff=0.05)
            c7 = blk("C7").next_to(c6, RIGHT, buff=0.05)
            self.play(FadeIn(c6, shift=LEFT * 0.4), run_time=self.rt(0.08))
            self.play(FadeIn(c7, shift=LEFT * 0.4), run_time=self.rt(0.08))
            c57 = VGroup(c5b, c6, c7)
            ins = T("C5b-7 inserts", 26, YELLOW).move_to([-3.85, 1.8, 0])
            self.play(FadeOut(nb), c57.animate.shift(DOWN * 1.0), Write(ins), run_time=self.rt(0.12))
            c8 = blk("C8").next_to(c7, RIGHT, buff=0.05)
            pore = T("small, unstable pore", 24, BLUE).next_to(c8, RIGHT, buff=0.3).shift(UP * 0.6)
            self.play(FadeIn(c8, shift=LEFT * 0.4), Write(pore), run_time=self.rt(0.15))
            c9 = blk("C9", PINK).next_to(c8, RIGHT, buff=0.05)
            self.play(FadeOut(pore), FadeIn(c9, shift=DOWN * 0.4), run_time=self.rt(0.1))
            rl = label_box("first C9 = rate-limiting step", PINK, 28).move_to([2.6, 1.8, 0])
            self.play(Write(rl), Indicate(c9, color=PINK), run_time=self.rt(0.15))
            self.src(("Abbas p.307; Janeway p.62"))

        # ---------------- b17 pore + lysis ----------------
        with self.beat("b17"):
            more = VGroup(*[blk("C9", PINK) for _ in range(4)]).arrange(RIGHT, buff=0.05)
            more.next_to(c9, RIGHT, buff=0.05)
            self.play(FadeOut(rl), FadeOut(ins), LaggedStart(*[FadeIn(m, shift=DOWN * 0.4) for m in more], lag_ratio=0.2),
                      run_time=self.rt(0.15))
            mac = VGroup(c5b, c6, c7, c8, c9, more)
            brace = Brace(mac, UP, color=YELLOW)
            ml = T("C5b-9 = MAC (poly-C9)", 30, YELLOW).next_to(brace, UP, buff=0.1)
            self.play(GrowFromCenter(brace), Write(ml), run_time=self.rt(0.1))
            src = T("C9 count: Abbas up to 18 · Janeway 10–16", 24, GREY).move_to([0, -3.1, 0])
            self.play(FadeIn(src), run_time=self.rt(0.12))
            water = VGroup(*[Arrow([x, 0.6, 0], [x, -2.4, 0], color=BLUE, stroke_width=3, buff=0)
                             for x in (more[1].get_x(), more[2].get_x())])
            wl = T("water in", 26, BLUE).next_to(more, RIGHT, buff=0.3).shift(UP * 0.6)
            self.play(LaggedStart(*[GrowArrow(w) for w in water], lag_ratio=0.3), Write(wl), run_time=self.rt(0.12))
            burst = T("cell swells, bursts", 26, PINK).next_to(wl, DOWN, buff=0.15).align_to(wl, LEFT)
            self.play(mem.animate.set_color(PINK), Write(burst), run_time=self.rt(0.1))
            nei = label_box("key target: thin-walled Neisseria", PINK, 28).move_to([0, -2.45, 0])
            self.play(FadeOut(src), FadeOut(water), FadeIn(nei, shift=UP * 0.3), run_time=self.rt(0.15))
            self.src(("Abbas p.307, p.314; Janeway p.66"))

        # ---------------- b18 opsonization ----------------
        with self.beat("b18"):
            self.clear_board(0.5)
            h = self.header("Opsonization: the main job")
            ph = cell(1.5, BLUE, label="phagocyte", size=30).move_to([-3.6, 0.4, 0])
            self.play(FadeIn(h), FadeIn(ph), run_time=self.rt(0.1))
            bug = Ellipse(width=2.2, height=1.3, color=PINK, stroke_width=4).set_fill(PINK, 0.12).move_to([3.2, 0.6, 0])
            t1 = tag("C3b", GREEN).move_to(bug.get_left() + LEFT * 0.1 + UP * 0.35)
            t2 = tag("iC3b", GREEN).move_to(bug.get_left() + LEFT * 0.15 + DOWN * 0.45)
            self.play(FadeIn(bug), FadeIn(t1), FadeIn(t2), run_time=self.rt(0.1))
            cr1 = label_box("CR1", BLUE, 26, buff=0.1).move_to(ph[0].get_right() + UP * 0.6 + RIGHT * 0.25)
            cr3 = label_box("CR3", BLUE, 26, buff=0.1).move_to(ph[0].get_right() + DOWN * 0.5 + RIGHT * 0.25)
            self.play(GrowFromCenter(cr1), run_time=self.rt(0.06))
            l1 = T("C3b, C4b  →  CR1: weak alone", 28, CHALK).move_to([0, -2.2, 0])
            self.play(Write(l1), run_time=self.rt(0.12))
            self.play(GrowFromCenter(cr3), run_time=self.rt(0.06))
            l2 = T("iC3b  →  CR3, CR4: enough alone", 28, GREEN).move_to([0, -3.0, 0])
            self.play(Write(l2), run_time=self.rt(0.12))
            prey = VGroup(bug, t1, t2)
            self.play(prey.animate.scale(0.55).move_to(ph[0].get_center() + LEFT * 0.4 + DOWN * 0.2),
                      run_time=self.rt(0.2))
            self.src(("Janeway p.62, p.64; Abbas p.312–313"))

        # ---------------- b19 spleen ----------------
        with self.beat("b19"):
            self.clear_board(0.5)
            h = self.header("Clinical link: the spleen")
            spleen = Ellipse(width=3.4, height=2.0, color=GREEN, stroke_width=4).set_fill(GREEN, 0.12).move_to([-2.6, 0.5, 0])
            sl = T("spleen", 30, GREEN).move_to(spleen)
            self.play(FadeIn(h), Create(spleen), Write(sl), run_time=self.rt(0.12))
            bugs = VGroup(*[Circle(0.2, color=PINK, stroke_width=3).set_fill(PINK, 0.2).move_to([x, y, 0])
                            for x, y in [(2.0, 1.4), (3.0, 0.6), (2.4, -0.2), (3.6, 1.6), (4.1, 0.0)]])
            bl = T("pneumococci, meningococci", 26, PINK).move_to([3.0, 2.4, 0])
            igm = T("IgM + classical pathway", 26, BLUE).move_to([3.0, -1.0, 0])
            self.play(FadeIn(bugs, lag_ratio=0.2), Write(bl), Write(igm), run_time=self.rt(0.2))
            self.play(LaggedStart(*[b.animate.move_to(spleen.get_center()).scale(0.2).set_opacity(0) for b in bugs],
                                  lag_ratio=0.1), run_time=self.rt(0.15))
            no = strike(spleen)
            sep = label_box("no spleen → disseminated septicemia", PINK, 30).move_to([0, -2.5, 0])
            self.play(Create(no), FadeIn(sep, shift=UP * 0.3), run_time=self.rt(0.2))
            self.src(("Abbas p.313"))

        # ---------------- b20 anaphylatoxins ----------------
        with self.beat("b20"):
            self.clear_board(0.5)
            h = self.header("Anaphylatoxins: C3a, C4a, C5a")
            mast = cell(1.3, BLUE).move_to([-3.6, 0.4, 0])
            mast_l = T("mast cell", 28, BLUE).move_to([-3.6, -2.0, 0])
            gran = VGroup(*[Dot(mast[0].get_center() + 0.85 * np.array([np.cos(a), np.sin(a), 0]),
                                radius=0.08, color=YELLOW) for a in np.linspace(0, TAU, 9, endpoint=False)])
            self.play(FadeIn(h), FadeIn(mast), FadeIn(mast_l), FadeIn(gran), run_time=self.rt(0.1))
            hist = T("histamine released", 26, YELLOW).move_to([-3.6, -2.8, 0])
            self.play(*[g.animate.shift(1.1 * (g.get_center() - mast[0].get_center())) for g in gran],
                      Write(hist), run_time=self.rt(0.2))
            ranks = VGroup(T("C5a  most potent", 40, PINK),
                           T("C3a  ~20× weaker", 32, YELLOW),
                           T("C4a  ~2500× weaker", 26, GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
            ranks.move_to([2.6, 0.2, 0])
            for r in ranks:
                self.play(Write(r), run_time=self.rt(0.13))
            self.src(("Abbas p.313–314"))

        # ---------------- b21 allergy link ----------------
        with self.beat("b21"):
            self.clear_board(0.5)
            h = self.header("C5a and the allergist")
            hub = label_box("C5a", PINK, 40).move_to([0, 0.6, 0])
            self.play(FadeIn(h), FadeIn(hub, scale=1.4), run_time=self.rt(0.08))
            m = label_box("mast cells: degranulate without IgE", BLUE, 26).move_to([-3.4, 2.1, 0])
            e = label_box("eosinophils: attracted", BLUE, 26).move_to([3.6, 2.1, 0])
            n = label_box("neutrophils: motility", BLUE, 26).move_to([3.6, -0.9, 0])
            for b in (m, e, n):
                self.play(GrowArrow(chalk_arrow(hub, b)), FadeIn(b), run_time=self.rt(0.13))
            sh = label_box("large systemic amounts → shock-like syndrome", PINK, 28).move_to([0, -2.4, 0])
            self.play(GrowArrow(chalk_arrow(hub, sh, PINK)), FadeIn(sh), run_time=self.rt(0.15))
            self.src(("Abbas p.313, p.470, p.473; Janeway p.64"))

        # ---------------- b22 adaptive help ----------------
        with self.beat("b22"):
            self.clear_board(0.5)
            h = self.header("Help for adaptive immunity")
            rbc = cell(0.75, CHALK, nucleus=False, label="red cell (CR1)", size=26).move_to([-4.6, 0.8, 0])
            ic = tag("immune complex", PINK, 24).next_to(rbc[0], UP, buff=0.05)
            ls = label_box("liver, spleen", GREEN, 28).move_to([-4.0, -2.4, 0])
            self.play(FadeIn(h), FadeIn(rbc), FadeIn(ic), run_time=self.rt(0.12))
            self.play(GrowArrow(chalk_arrow(rbc, ls)), FadeIn(ls), run_time=self.rt(0.15))
            self.play(ic.animate.move_to(ls.get_top() + DOWN * 0.1).set_opacity(0), run_time=self.rt(0.1))
            bc = cell(1.0, BLUE, label="B cell", size=28).move_to([2.6, -0.6, 0])
            cr2 = label_box("CR2", BLUE, 24, buff=0.08).move_to(bc[0].get_top() + UP * 0.25)
            ag = VGroup(Star(5, outer_radius=0.35, color=PINK).set_fill(PINK, 0.3), T("C3d", 26, GREEN))
            ag[1].next_to(ag[0], RIGHT, buff=0.12)
            ag.move_to([2.8, 2.2, 0])
            self.play(FadeIn(bc), FadeIn(cr2), FadeIn(ag), run_time=self.rt(0.15))
            self.play(ag.animate.next_to(cr2, UP, buff=0.05), run_time=self.rt(0.1))
            go = T("activation ↑", 30, GREEN).next_to(bc, RIGHT, buff=0.3)
            self.play(Write(go), run_time=self.rt(0.1))
            self.src(("Abbas p.307, p.314"))

        # ---------------- b23 brakes overview ----------------
        with self.beat("b23"):
            self.clear_board(0.5)
            h = self.header("The brakes: regulators")
            self.play(FadeIn(h), run_time=0.4)
            stages = VGroup(*[label_box(s, BLUE, 28) for s in ("start: C1, MASP2", "convertases", "MAC")])
            stages.arrange(RIGHT, buff=1.1).move_to([0, 1.8, 0])
            sarr = VGroup(*[chalk_arrow(a, b) for a, b in zip(stages, stages[1:])])
            why = T("C3b cannot tell host from microbe", 30, PINK).move_to([0, 0.2, 0])
            self.play(Write(why), run_time=self.rt(0.2))
            self.play(LaggedStart(*[FadeIn(s, shift=DOWN * 0.3) for s in stages], lag_ratio=0.3),
                      Create(sarr), run_time=self.rt(0.25))
            slots = VGroup(*[DashedVMobject(RoundedRectangle(corner_radius=0.12, width=2.4, height=0.7,
                                                             color=GREEN), num_dashes=24)
                             .next_to(s, DOWN, buff=0.25) for s in stages])
            self.play(FadeOut(why), Create(slots), run_time=self.rt(0.2))
            self.src(("Janeway p.68; Abbas p.311"))

        # ---------------- b24 C1-INH ----------------
        with self.beat("b24"):
            f1 = T("C1-INH", 28, GREEN).move_to(slots[0])
            self.play(Write(f1), Indicate(stages[0], color=GREEN), run_time=self.rt(0.1))
            bl = bullet_list(["serpin: removes C1r, C1s from C1q",
                              "also inactivates MASP2",
                              "inhibits kallikrein, factor XII → bradykinin"], 28).move_to([0, -0.9, 0])
            for row in bl:
                self.play(FadeIn(row, shift=RIGHT * 0.2), run_time=self.rt(0.15))
            hae = label_box("C1-INH deficiency → hereditary angioedema (HAE)", PINK, 28).move_to([0, -3.0, 0])
            self.play(FadeIn(hae, shift=UP * 0.3), run_time=self.rt(0.15))
            self.src(("Abbas p.311"))

        # ---------------- b25 convertase brakes ----------------
        with self.beat("b25"):
            self.play(FadeOut(bl), FadeOut(hae), run_time=0.4)
            f2 = T("DAF, H, C4BP, I", 24, GREEN).scale_to_fit_width(2.1).move_to(slots[1])
            self.play(Write(f2), Indicate(stages[1], color=GREEN), run_time=self.rt(0.06))
            dh = T("Decay: pull apart", 30, YELLOW).move_to([-3.4, -0.3, 0])
            dl = bullet_list(["DAF (CD55): both C3 convertases", "factor H: displaces Bb",
                              "C4BP: displaces C2"], 26).next_to(dh, DOWN, buff=0.3)
            self.play(Write(dh), run_time=self.rt(0.06))
            for row in dl:
                self.play(FadeIn(row, shift=RIGHT * 0.2), run_time=self.rt(0.09))
            ih = T("Factor I: scissors", 30, YELLOW).move_to([3.4, -0.3, 0])
            il = bullet_list(["needs a cofactor:", "factor H, MCP (CD46)", "C4BP, CR1"], 26).next_to(ih, DOWN, buff=0.3)
            self.play(Write(ih), run_time=self.rt(0.08))
            for row in il:
                self.play(FadeIn(row, shift=RIGHT * 0.2), run_time=self.rt(0.1))
            self.src(("Abbas p.310; Janeway p.68"))

        # ---------------- b26 MAC brakes ----------------
        with self.beat("b26"):
            self.play(FadeOut(VGroup(dh, dl, ih, il)), run_time=0.4)
            f3 = T("CD59, S protein", 24, GREEN).scale_to_fit_width(2.1).move_to(slots[2])
            self.play(Write(f3), Indicate(stages[2], color=GREEN), run_time=self.rt(0.08))
            bl2 = bullet_list(["CD59 (protectin): joins C5b-8, blocks C9",
                               "S protein: binds soluble C5b-7"], 28).move_to([0, -0.8, 0])
            for row in bl2:
                self.play(FadeIn(row, shift=RIGHT * 0.2), run_time=self.rt(0.18))
            pnh = label_box("no GPI anchor → no DAF, no CD59 → PNH", PINK, 28).move_to([0, -2.6, 0])
            self.play(FadeIn(pnh, shift=UP * 0.3), run_time=self.rt(0.15))
            self.src(("Abbas p.311–312; Janeway p.70"))

        # ---------------- b27 five things ----------------
        with self.beat("b27"):
            self.clear_board(0.5)
            h = self.header("Five things to remember")
            self.play(FadeIn(h), run_time=0.4)
            items = ["3 pathways → one central event: C3 cleavage",
                     "C4b2a (classical, lectin) · C3bBb (alternative)",
                     "the alternative loop amplifies everything",
                     "C3b opsonizes · C5a strongest · MAC lyses Neisseria",
                     "regulators act at 3 levels"]
            rows = VGroup()
            for i, it in enumerate(items):
                n = T(f"{i + 1}", 34, YELLOW)
                t = T(it, 30, CHALK)
                rows.add(VGroup(n, t).arrange(RIGHT, buff=0.35))
            rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, -0.3, 0])
            if rows.width > 12.4:
                rows.scale_to_fit_width(12.4)
            marks = [0.02, 0.2, 0.42, 0.58, 0.85]
            for r, mk in zip(rows, marks):
                wait = self.bd * mk - self.elapsed()
                if wait > 0.05:
                    self.wait(wait)
                self.play(FadeIn(r, shift=RIGHT * 0.3), run_time=self.fit(1.0))

        # ---------------- b28 trap + next ----------------
        with self.beat("b28"):
            self.clear_board(0.5)
            h = self.header("Exam trap", PINK)
            self.play(FadeIn(h), run_time=0.4)
            wrong = T("factor H  →  pulls apart C4b2a", 34, CHALK).move_to([0, 1.5, 0])
            self.play(Write(wrong), run_time=self.rt(0.12))
            sl = Line(wrong.get_left() + LEFT * 0.1, wrong.get_right() + RIGHT * 0.1, color=PINK, stroke_width=6)
            no = T("wrong", 30, PINK).next_to(wrong, UP, buff=0.25)
            self.play(Create(sl), FadeIn(no), run_time=self.rt(0.08))
            right = bullet_list(["factor H: alternative pathway only (Bb)",
                                 "C4b brake in plasma: C4-binding protein"], 30, GREEN).move_to([0, -0.2, 0])
            self.play(FadeIn(right[0], shift=RIGHT * 0.2), run_time=self.rt(0.12))
            self.play(FadeIn(right[1], shift=RIGHT * 0.2), run_time=self.rt(0.15))
            self.src(("Abbas p.310–311"))
            nxt = T("Next: complement deficiencies & HAE", 34, YELLOW).move_to([0, -2.6, 0])
            self.play(Write(nxt), run_time=self.rt(0.2))

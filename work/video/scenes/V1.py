from chalk import *


# ---------- local helpers (V1 only) ----------
def fit_w(mob, w):
    if mob.width > w:
        mob.scale_to_fit_width(w)
    return mob


def epithelium(n=8, w=1.3, h=1.1, y=-0.9, color=BLUE):
    cells = VGroup(*[RoundedRectangle(corner_radius=0.12, width=w, height=h, color=color, stroke_width=3)
                     .set_fill(color, 0.10) for _ in range(n)]).arrange(RIGHT, buff=0).move_to([0, y, 0])
    nuclei = VGroup(*[Ellipse(width=w * 0.4, height=h * 0.3, color=color, stroke_width=2)
                      .set_fill(color, 0.3).move_to(c.get_center() + DOWN * h * 0.12) for c in cells])
    return VGroup(cells, nuclei)


def microbe(color=PINK, w=0.55, h=0.32):
    return Ellipse(width=w, height=h, color=color, stroke_width=3).set_fill(color, 0.35)


def spiky_microbe(color=PINK, r=0.7, spikes=10, spike_color=YELLOW):
    body = Circle(r, color=color, stroke_width=4).set_fill(color, 0.35)
    sp = VGroup()
    for k in range(spikes):
        a = TAU * k / spikes
        d = np.array([np.cos(a), np.sin(a), 0])
        sp.add(Triangle(color=spike_color, stroke_width=2).set_fill(spike_color, 0.7)
               .scale(0.12).rotate(a - PI / 2).move_to(d * (r + 0.1)))
    return VGroup(body, sp)


def shield(color=GREEN, s=1.0):
    pts = [[-0.8, 0.9, 0], [0.8, 0.9, 0], [0.8, 0.1, 0], [0, -1.0, 0], [-0.8, 0.1, 0]]
    return Polygon(*pts, color=color, stroke_width=5).set_fill(color, 0.15).scale(s)


def clock(r=0.45, color=CHALK, hour_angle=PI / 3):
    c = Circle(r, color=color, stroke_width=3)
    h1 = Line(ORIGIN, UP * r * 0.75, color=color, stroke_width=3)
    h2 = Line(ORIGIN, rotate_vector(UP * r * 0.5, -hour_angle), color=color, stroke_width=3)
    return VGroup(c, h1, h2)


class V1(ChalkScene):
    VIDEO_ID = "V1"

    # ---- small timing / board helpers ----
    def w(self, s):
        s = min(s, self.remaining() - 0.2)
        if s > 0.05:
            self.wait(s)

    def tag(self, text):
        new = self.source_tag(text)
        old = getattr(self, "_tag", None)
        if old is not None and old in self.mobjects:
            self.play(FadeOut(old), FadeIn(new), run_time=0.4)
        else:
            self.play(FadeIn(new), run_time=0.4)
        self._tag = new

    def clear(self):
        self.clear_board()
        self._tag = None

    def construct(self):
        # ================= INTRO =================
        with self.beat("b01"):
            title = self.title_card("Innate immunity", "the first 4 hours")
            self.play(Write(title), run_time=self.fit(2.5))
            self.w(1.0)
            self.play(title.animate.scale(0.75).to_edge(UP, buff=0.5), run_time=self.fit(1))
            goals = bullet_list(["Compare innate vs adaptive immunity",
                                 "Name the barrier molecules",
                                 "Place each phase on a time line"], size=34).next_to(title, DOWN, buff=0.8)
            exam = T("Exam goals", 30, YELLOW).next_to(goals, UP, buff=0.3).align_to(goals, LEFT)
            self.play(FadeIn(exam), run_time=0.4)
            for g in goals:
                self.play(FadeIn(g, shift=RIGHT * 0.3), run_time=self.fit(0.8))
                self.w(1.0)

        # ================= INNATE vs ADAPTIVE: speed =================
        with self.beat("b02"):
            self.clear()
            div = Line(UP * 3.2, DOWN * 3.2, color=GREY, stroke_width=2)
            lt = T("INNATE", 48, YELLOW).move_to([-3.4, 2.8, 0])
            sh = shield(GREEN, 0.9).move_to([-4.6, 1.0, 0])
            ck = clock().move_to([-2.2, 1.0, 0])
            ckl = T("hours", 28, GREEN).next_to(ck, DOWN, buff=0.15)
            self.play(Create(div), Write(lt), run_time=self.fit(1))
            self.play(DrawBorderThenFill(sh), run_time=self.fit(1))
            b = bullet_list(["ready before infection", "continuous barrier defense",
                             "acts in hours to days"], size=30).move_to([-3.4, -1.6, 0])
            self.play(FadeIn(b[0], shift=RIGHT * 0.2), run_time=self.fit(0.8))
            self.w(1.5)
            self.play(FadeIn(b[1], shift=RIGHT * 0.2), run_time=self.fit(0.8))
            self.w(1.2)
            self.play(Create(ck), FadeIn(ckl), FadeIn(b[2], shift=RIGHT * 0.2), run_time=self.fit(1))
            self.play(Rotate(ck[2], -PI, about_point=ck[0].get_center()), run_time=self.fit(1.5))
            self.tag("Abbas p.3")

        with self.beat("b03"):
            rt = T("ADAPTIVE", 48, YELLOW).move_to([3.4, 2.8, 0])
            ly = cell(0.6, BLUE, label="lymphocyte", size=26).move_to([2.2, 0.9, 0])
            cal = VGroup(*[Square(0.32, color=CHALK, stroke_width=2) for _ in range(5)]).arrange(RIGHT, buff=0.06)
            cal.move_to([4.6, 1.1, 0])
            call = T("days", 28, PINK).next_to(cal, DOWN, buff=0.15)
            self.play(Write(rt), run_time=self.fit(0.8))
            self.play(GrowFromCenter(ly), run_time=self.fit(1))
            b2 = bullet_list(["needs exposure to the microbe", "activation takes several days",
                              "so innate protects first"], size=30).move_to([3.4, -1.6, 0])
            self.play(FadeIn(b2[0], shift=RIGHT * 0.2), run_time=self.fit(0.8))
            self.w(1.0)
            self.play(LaggedStart(*[FadeIn(s) for s in cal], lag_ratio=0.3), FadeIn(call),
                      FadeIn(b2[1], shift=RIGHT * 0.2), run_time=self.fit(2))
            self.w(1.5)
            b2[2][1].set_color(GREEN)
            self.play(FadeIn(b2[2], shift=RIGHT * 0.2), run_time=self.fit(0.8))
            self.play(Indicate(b2[2], color=GREEN), run_time=self.fit(1))
            self.tag("Abbas p.3, p.10")

        # ================= D1 comparison table =================
        with self.beat("b04"):
            self.clear()
            hdr = self.header("Innate vs adaptive")
            self.play(Write(hdr), run_time=self.fit(1))
            XL, XI, XA = -5.0, -0.9, 3.9
            ch_i = T("Innate", 34, YELLOW).move_to([XI, 2.45, 0])
            ch_a = T("Adaptive", 34, YELLOW).move_to([XA, 2.45, 0])
            self.play(FadeIn(ch_i), FadeIn(ch_a), run_time=self.fit(0.6))
            ys = [1.75, 0.85, -0.05, -0.95, -1.85, -2.75]
            rows_spec = [
                ("Speed", "hours", "days", GREEN, CHALK),
                ("Recognizes", "~1000 shared molecules", "millions of antigens", CHALK, CHALK),
                ("Receptors", "germline, invariant\n< 100 types", "Ig + TCR only\nrearranged, millions", CHALK, CHALK),
                ("Distribution", "nonclonal", "clonal", CHALK, CHALK),
                ("Memory", "limited", "yes: faster, bigger", CHALK, GREEN),
                ("Self", "no reaction", "no reaction", GREEN, GREEN),
            ]
            rows = []
            for y, (lab, a, b, ca, cb) in zip(ys, rows_spec):
                l = T(lab, 28, GREY).move_to([0, y, 0]).align_to([XL - 1.3, 0, 0], LEFT)
                ta = fit_w(T(a, 26, ca, line_spacing=0.8), 4.3).move_to([XI, y, 0])
                tb = fit_w(T(b, 26, cb, line_spacing=0.8), 4.3).move_to([XA, y, 0])
                rows.append(VGroup(l, ta, tb))
            lines = VGroup(*[Line([-6.4, y - 0.45, 0], [6.3, y - 0.45, 0], color=GREY, stroke_width=1.5)
                             for y in ys[:-1]])
            # speed row is a recap of b02/b03
            self.play(FadeIn(rows[0]), run_time=self.fit(0.8))
            self.w(2.0)
            self.play(Create(lines[0]), FadeIn(rows[1][0]), run_time=self.fit(0.6))
            self.w(1.5)
            self.play(Write(rows[1][1]), run_time=self.fit(1.2))
            self.w(3.5)
            self.play(Write(rows[1][2]), run_time=self.fit(1.2))
            self.play(Circumscribe(rows[1][2], color=YELLOW), run_time=self.fit(1))
            self.tag("Abbas p.4, p.63")
            self.d1 = (rows, lines)

        with self.beat("b05"):
            rows, lines = self.d1
            self.play(Create(lines[1]), FadeIn(rows[2][0]), run_time=self.fit(0.6))
            self.w(0.6)
            self.play(Write(rows[2][1]), run_time=self.fit(1.5))
            self.w(3.0)
            self.play(Write(rows[2][2]), run_time=self.fit(1.5))
            self.w(3.0)
            self.play(Indicate(rows[2][2], color=YELLOW), run_time=self.fit(1))
            self.tag("Abbas p.63-64")

        with self.beat("b06"):
            self.play(Create(lines[2]), FadeIn(rows[3][0]), run_time=self.fit(0.5))
            # mini cells: identical (nonclonal) vs different (clonal)
            same = VGroup(*[cell(0.16, BLUE, nucleus=False) for _ in range(3)]).arrange(RIGHT, buff=0.08)
            diff = VGroup(*[cell(0.16, c, nucleus=False) for c in (BLUE, ORANGE, GREEN)]).arrange(RIGHT, buff=0.08)
            self.play(Write(rows[3][1]), run_time=self.fit(0.8))
            same.next_to(rows[3][1], RIGHT, buff=0.3)
            self.play(LaggedStart(*[GrowFromCenter(c) for c in same], lag_ratio=0.3), run_time=self.fit(1))
            self.w(0.8)
            self.play(Write(rows[3][2]), run_time=self.fit(0.8))
            diff.next_to(rows[3][2], RIGHT, buff=0.3)
            self.play(LaggedStart(*[GrowFromCenter(c) for c in diff], lag_ratio=0.3), run_time=self.fit(1))
            self.tag("Abbas p.64")
            self.mini = VGroup(same, diff)

        with self.beat("b07"):
            self.play(Create(lines[3]), FadeIn(rows[4][0]), run_time=self.fit(0.5))
            self.play(Write(rows[4][1]), run_time=self.fit(0.8))
            self.w(5.5)
            self.play(Write(rows[4][2]), run_time=self.fit(1))
            self.w(1.5)
            self.play(Circumscribe(rows[4][2], color=GREEN), run_time=self.fit(1))
            self.tag("Abbas p.4, p.6")

        with self.beat("b08"):
            self.play(Create(lines[4]), FadeIn(rows[5]), run_time=self.fit(1))
            self.w(2.0)
            others = [m for m in self.mobjects if not isinstance(m, ImageMobject) and m is not self._tag]
            self.play(*[FadeOut(m) for m in others], run_time=self.fit(0.6))
            hdr2 = self.header("Innate ignores healthy cells", GREEN)
            hc = cell(0.8, GREEN, label="healthy cell", size=26).move_to([-4.4, -0.2, 0])
            reasons = bullet_list(["normal cells lack most ligands",
                                   "receptors sit in separate compartments",
                                   "regulatory proteins block activation"], size=30).move_to([1.6, -0.2, 0])
            self.play(Write(hdr2), GrowFromCenter(hc), run_time=self.fit(1))
            for r in reasons:
                self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=self.fit(0.8))
                self.w(1.4)
            self.tag("Abbas p.4, p.65")

        # ================= PAMPs / DAMPs =================
        with self.beat("b09"):
            self.clear()
            hdr = self.header("What innate immunity sees")
            self.play(Write(hdr), run_time=self.fit(1))
            div = DashedLine(UP * 2.6, DOWN * 3.4, color=GREY, stroke_width=2)
            mic = spiky_microbe().move_to([-5.0, 1.2, 0])
            ph = cell(0.6, BLUE, nucleus=True).move_to([-1.5, 1.2, 0])
            rec = VGroup(*[Line(ph[0].get_left() + UP * dy, ph[0].get_left() + UP * dy + LEFT * 0.3,
                                color=BLUE, stroke_width=4) for dy in (-0.25, 0, 0.25)])
            pl = T("PAMPs", 34, YELLOW).next_to(mic, UP, buff=0.2)
            self.play(Create(div), GrowFromCenter(mic), run_time=self.fit(1))
            self.w(2.0)
            self.play(Write(pl), Indicate(mic[1], color=YELLOW), run_time=self.fit(1.2))
            self.play(GrowFromCenter(ph), Create(rec), run_time=self.fit(0.8))
            arr = chalk_arrow(mic, ph, YELLOW)
            self.play(GrowArrow(arr), run_time=self.fit(0.8))
            pb = bullet_list(["shared by classes of microbes",
                              "essential for microbe survival",
                              "so microbes cannot drop them"], size=28).move_to([-3.4, -1.4, 0])
            self.play(FadeIn(pb[0], shift=RIGHT * 0.2), run_time=self.fit(0.7))
            self.w(1.5)
            self.play(FadeIn(pb[1], shift=RIGHT * 0.2), run_time=self.fit(0.7))
            self.w(1.5)
            pb[2][1].set_color(GREEN)
            self.play(FadeIn(pb[2], shift=RIGHT * 0.2), run_time=self.fit(0.7))
            self.tag("Abbas p.63")

        with self.beat("b10"):
            dc = Circle(0.6, color=PINK, stroke_width=4).set_fill(PINK, 0.12).move_to([2.0, 1.2, 0])
            cracked = DashedVMobject(dc.copy(), num_dashes=10)
            dl = T("DAMPs", 34, YELLOW).move_to([2.0, 2.5, 0])
            frags = VGroup(*[Dot(radius=0.07, color=YELLOW).move_to(dc.get_center()) for _ in range(7)])
            self.play(GrowFromCenter(dc), run_time=self.fit(0.8))
            self.play(ReplacementTransform(dc, cracked), Write(dl), run_time=self.fit(0.8))
            self.play(*[f.animate.shift(rotate_vector(RIGHT * 0.85, TAU * k / 7 + 0.3)) for k, f in enumerate(frags)],
                      run_time=self.fit(1.2))
            db = bullet_list(["from damaged or dying cells",
                              "also sterile injury: burns, trauma",
                              "apoptosis: generally no DAMPs",
                              "alarmins = DAMP cytokines"], size=28).move_to([3.3, -1.5, 0])
            self.play(FadeIn(db[0], shift=RIGHT * 0.2), run_time=self.fit(0.7))
            self.w(1.0)
            self.play(FadeIn(db[1], shift=RIGHT * 0.2), run_time=self.fit(0.7))
            self.w(1.6)
            ap = Circle(0.35, color=GREY, stroke_width=3).set_fill(GREY, 0.2).move_to([5.3, 1.2, 0])
            apl = T("apoptotic", 24, GREY).next_to(ap, DOWN, buff=0.4)
            self.play(FadeIn(ap), FadeIn(apl), FadeIn(db[2], shift=RIGHT * 0.2), run_time=self.fit(0.8))
            self.play(Create(strike(VGroup(ap).copy().scale(1.3))), run_time=self.fit(0.6))
            self.w(1.0)
            self.play(FadeIn(db[3], shift=RIGHT * 0.2), run_time=self.fit(0.7))
            self.tag("Abbas p.63")

        # ================= BARRIERS =================
        with self.beat("b11"):
            self.clear()
            hdr = self.header("Epithelial barriers")
            self.play(Write(hdr), run_time=self.fit(1))
            sites = T("skin  ·  gut  ·  airways  ·  genitourinary tract", 30, CHALK).move_to([0, 2.2, 0])
            self.play(Write(sites), run_time=self.fit(2))
            epi = epithelium(y=-1.4)
            out = T("outside world", 26, GREY).move_to([-4.2, -0.2, 0])
            ins = T("tissue", 26, GREY).move_to([-4.6, -2.5, 0])
            self.play(LaggedStart(*[Create(c) for c in epi[0]], lag_ratio=0.1), FadeIn(epi[1]),
                      FadeIn(out), FadeIn(ins), run_time=self.fit(2))
            self.w(2.0)
            kinds = VGroup(label_box("mechanical", BLUE, 30), label_box("chemical", ORANGE, 30),
                           label_box("microbiological", GREEN, 30)).arrange(RIGHT, buff=0.6).move_to([0.8, 0.8, 0])
            for k in kinds:
                self.play(FadeIn(k, shift=DOWN * 0.3), run_time=self.fit(0.8))
                self.w(0.6)
            self.tag("Abbas p.79; Janeway p.43")

        with self.beat("b12"):
            self.clear(),
            an = T("Analogy", 30, GREY).to_corner(UL, buff=0.4)
            ground = Line([-6, -2.2, 0], [6, -2.2, 0], color=GREY, stroke_width=2)
            wall = Rectangle(width=5.0, height=2.6, color=CHALK, stroke_width=4).move_to([-2.7, -0.9, 0])
            crens = VGroup(*[Square(0.45, color=CHALK, stroke_width=4).move_to(wall.get_top() + RIGHT * x + UP * 0.225)
                             for x in np.arange(-2.25, 2.3, 0.9)])
            castle = VGroup(wall, crens)
            pot = VGroup(Arc(radius=0.4, start_angle=PI, angle=PI, color=ORANGE, stroke_width=5),
                         Line(LEFT * 0.4, RIGHT * 0.4, color=ORANGE, stroke_width=5)).move_to(crens[0].get_top() + UP * 0.35)
            drops = VGroup(*[Dot(radius=0.06, color=ORANGE).move_to(pot.get_left() + LEFT * 0.15 + DOWN * k * 0.3)
                             for k in range(1, 4)])
            tenants = VGroup(*[Circle(0.16, color=GREEN, stroke_width=3).set_fill(GREEN, 0.4) for _ in range(10)])
            tenants.arrange_in_grid(2, 5, buff=0.4).move_to(wall.get_center() + DOWN * 0.2)
            labs = VGroup(T("wall = physical barrier", 30, BLUE),
                          T("boiling oil = chemical barrier", 30, ORANGE),
                          T("tenants = microbiota", 30, GREEN)).arrange(DOWN, aligned_edge=LEFT, buff=0.55)
            labs.move_to([3.3, 0.3, 0])
            self.play(FadeIn(an), Create(ground), Create(castle), run_time=self.fit(1.5))
            self.play(FadeIn(labs[0], shift=LEFT * 0.2), run_time=self.fit(0.7))
            self.w(0.6)
            self.play(Create(pot), FadeIn(labs[1], shift=LEFT * 0.2), run_time=self.fit(0.8))
            self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.3) for d in drops], lag_ratio=0.3), run_time=self.fit(0.8))
            self.w(0.5)
            self.play(LaggedStart(*[GrowFromCenter(t) for t in tenants], lag_ratio=0.1),
                      FadeIn(labs[2], shift=LEFT * 0.2), run_time=self.fit(1.5))

        with self.beat("b13"):
            self.clear()
            hdr = self.header("1 · Physical barrier", BLUE)
            epi = epithelium(y=-1.4)
            self.play(Write(hdr), FadeIn(epi), run_time=self.fit(1))
            cells = epi[0]
            tj = VGroup(*[Rectangle(width=0.1, height=0.3, color=YELLOW, stroke_width=1).set_fill(YELLOW, 1)
                          .move_to([(cells[i].get_right()[0]), cells[i].get_top()[1] - 0.18, 0])
                          for i in range(len(cells) - 1)])
            self.play(LaggedStart(*[GrowFromCenter(t) for t in tj], lag_ratio=0.1), run_time=self.fit(1))
            tjl = T("tight junctions", 28, YELLOW).move_to([3.6, 0.1, 0])
            tja = chalk_arrow(tjl.get_bottom() + DOWN * 0.05, tj[5].get_top() + UP * 0.05, YELLOW, buff=0.05)
            self.play(FadeIn(tjl), GrowArrow(tja), run_time=self.fit(0.8))
            m = microbe().move_to([cells[2].get_right()[0], 0.6, 0])
            self.play(FadeIn(m), run_time=0.3)
            self.play(m.animate.move_to([cells[2].get_right()[0], -0.45, 0]), run_time=self.fit(0.8), rate_func=rush_into)
            self.play(m.animate.move_to([cells[2].get_right()[0] - 0.8, 0.5, 0]), run_time=self.fit(0.6), rate_func=rush_from)
            pb = bullet_list(["tight junctions block passage between cells",
                              "skin: outer keratin layer blocks penetration",
                              "skin infection usually follows a breach"], size=28).move_to([0, 1.75, 0])
            for p in pb:
                self.play(FadeIn(p, shift=RIGHT * 0.2), run_time=self.fit(0.7))
                self.w(1.8)
            self.tag("Abbas p.80")
            self.epi13 = (epi, tj, tjl, tja, m, pb)

        with self.beat("b14"):
            epi, tj, tjl, tja, m, pb = self.epi13
            self.play(FadeOut(pb), FadeOut(tjl), FadeOut(tja), FadeOut(m), run_time=self.fit(0.6))
            cells = epi[0]
            cilia = VGroup(*[Line([x, cells.get_top()[1], 0], [x + 0.06, cells.get_top()[1] + 0.25, 0],
                                  color=BLUE, stroke_width=2)
                             for c in cells for x in np.linspace(c.get_left()[0] + 0.15, c.get_right()[0] - 0.15, 5)])
            mucus = Rectangle(width=cells.width, height=0.4, stroke_width=0).set_fill(GREEN, 0.25)
            mucus.next_to(cells, UP, buff=0.22)
            mucus_edge = Line(mucus.get_corner(UL), mucus.get_corner(UR), color=GREEN, stroke_width=3)
            ml = T("mucus (mucins)", 28, GREEN).next_to(mucus, UP, buff=0.2).align_to(mucus, LEFT)
            self.play(FadeIn(mucus), Create(mucus_edge), Write(ml), run_time=self.fit(1.2))
            pb = bullet_list(["mucus impairs microbial invasion",
                              "airways: goblet cells + beating cilia",
                              "gut: peristalsis removes microbes"], size=28).move_to([1.3, 1.95, 0])
            self.play(FadeIn(pb[0], shift=RIGHT * 0.2), run_time=self.fit(0.7))
            self.w(1.8)
            gob = cells[3]
            self.play(gob.animate.set_fill(YELLOW, 0.25), run_time=self.fit(0.5))
            gl = T("goblet cell", 26, YELLOW).move_to([gob.get_center()[0], -2.6, 0])
            self.play(FadeIn(gl), FadeIn(pb[1], shift=RIGHT * 0.2), Create(cilia), run_time=self.fit(1.2))
            self.play(LaggedStart(*[c.animate.rotate(-0.5, about_point=c.get_start()) for c in cilia], lag_ratio=0.01),
                      run_time=self.fit(1.0), rate_func=there_and_back)
            flow = Arrow(mucus.get_left() + RIGHT * 2.0, mucus.get_right() + LEFT * 0.4, buff=0, color=CHALK,
                         stroke_width=4, max_tip_length_to_length_ratio=0.05).move_to(mucus)
            self.play(GrowArrow(flow), run_time=self.fit(1))
            self.w(0.8)
            self.play(FadeIn(pb[2], shift=RIGHT * 0.2), run_time=self.fit(0.7))
            self.tag("Abbas p.80; Janeway p.48")
            self.epi14 = (mucus, mucus_edge, ml, cilia, flow, pb, gl)

        with self.beat("b15"):
            mucus, mucus_edge, ml, cilia, flow, pb, gl = self.epi14
            box_t = T("Clinical: cystic fibrosis", 34, PINK)
            self.play(FadeOut(pb), FadeOut(flow), FadeOut(ml), run_time=self.fit(0.5))
            box_t.move_to([0, 2.15, 0])
            box = chalk_box(box_t, PINK)
            self.play(Write(box_t), Create(box), run_time=self.fit(1))
            thick = Rectangle(width=mucus.width, height=0.85, stroke_width=0).set_fill(PINK, 0.3)
            thick.align_to(mucus, DOWN).align_to(mucus, LEFT)
            thick_edge = Line(thick.get_corner(UL), thick.get_corner(UR), color=PINK, stroke_width=3)
            self.play(Transform(mucus, thick), Transform(mucus_edge, thick_edge), cilia.animate.set_color(GREY),
                      run_time=self.fit(1.2))
            tl = T("thick mucus, poor ciliary movement", 28, PINK).move_to([0, 1.38, 0])
            self.play(FadeIn(tl), run_time=self.fit(0.6))
            self.w(1.0)
            bugs = VGroup(*[microbe(PINK, 0.4, 0.24).move_to([x, thick.get_top()[1] + 0.18, 0])
                            for x in np.linspace(-4.5, 4.5, 9)])
            self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.5) for b in bugs], lag_ratio=0.1), run_time=self.fit(1.5))
            st = T("bacteria colonize the surface but do not cross it", 26, CHALK).move_to([0, 0.9, 0])
            self.play(FadeIn(st), run_time=self.fit(0.6))
            self.w(2.0)
            pe = T("Failure of peristalsis → bacterial overgrowth in the gut lumen", 26, PINK)
            fit_w(pe, 11).move_to([0, -2.75, 0])
            self.play(FadeOut(gl), FadeIn(pe, shift=UP * 0.2), run_time=self.fit(0.8))
            self.tag("Janeway p.44")

        # ---- chemical barrier ----
        with self.beat("b16"):
            self.clear()
            hdr = self.header("2 · Chemical barrier", ORANGE)
            self.play(Write(hdr), run_time=self.fit(1))
            gut = T("Upper gut: stomach acid · digestive enzymes · bile salts", 28, CHALK).move_to([0, 2.3, 0])
            self.play(Write(gut), run_time=self.fit(1.5))
            self.w(1.5)
            lys = label_box("lysozyme", GREEN, 32).move_to([0, 1.2, 0])
            src = T("tears, saliva", 24, GREY).next_to(lys, RIGHT, buff=0.3)
            self.play(FadeIn(lys, shift=DOWN * 0.2), FadeIn(src), run_time=self.fit(0.8))
            # Gram-positive wall: thick peptidoglycan in two halves
            gp_mem = Line([-5.6, -2.0, 0], [-1.4, -2.0, 0], color=BLUE, stroke_width=5)
            gp_a = Rectangle(width=2.1, height=0.7, color=YELLOW, stroke_width=3).set_fill(YELLOW, 0.25)
            gp_b = gp_a.copy()
            gp_a.next_to(gp_mem, UP, buff=0.05).align_to(gp_mem, LEFT)
            gp_b.next_to(gp_a, RIGHT, buff=0)
            gp_l = T("Gram-positive", 28, CHALK).next_to(gp_mem, DOWN, buff=0.2)
            gn_mem = Line([1.4, -2.0, 0], [5.6, -2.0, 0], color=BLUE, stroke_width=5)
            gn_pg = Rectangle(width=4.2, height=0.18, color=YELLOW, stroke_width=2).set_fill(YELLOW, 0.25)
            gn_pg.next_to(gn_mem, UP, buff=0.05)
            gn_lps = Rectangle(width=4.2, height=0.4, color=PINK, stroke_width=3).set_fill(PINK, 0.3)
            gn_lps.next_to(gn_pg, UP, buff=0.04)
            gn_l = T("Gram-negative", 28, CHALK).next_to(gn_mem, DOWN, buff=0.2)
            lps_l = T("LPS outer layer", 24, PINK).next_to(gn_lps, UP, buff=0.12)
            pg_l = T("peptidoglycan", 24, YELLOW).next_to(gp_b, UP, buff=0.12).align_to(gp_a, LEFT)
            self.play(Create(gp_mem), FadeIn(gp_a), FadeIn(gp_b), FadeIn(gp_l), FadeIn(pg_l),
                      Create(gn_mem), FadeIn(gn_pg), FadeIn(gn_l), run_time=self.fit(1.2))
            self.w(1.5)
            a1 = chalk_arrow(lys, VGroup(gp_a, gp_b, pg_l), GREEN)
            self.play(GrowArrow(a1), run_time=self.fit(0.7))
            self.play(gp_a.animate.shift(LEFT * 0.25).rotate(0.12), gp_b.animate.shift(RIGHT * 0.25).rotate(-0.12),
                      run_time=self.fit(0.8))
            ok = T("✓ works better", 28, GREEN).next_to(a1, LEFT, buff=0.1).shift(UP * 0.2)
            self.play(FadeIn(ok), run_time=self.fit(0.5))
            self.w(0.8)
            self.play(FadeIn(gn_lps, shift=DOWN * 0.2), FadeIn(lps_l), run_time=self.fit(0.8))
            a2 = chalk_arrow(lys, lps_l, PINK)
            self.play(GrowArrow(a2), run_time=self.fit(0.6))
            no = T("✗ blocked", 28, PINK).next_to(a2, RIGHT, buff=0.1).shift(UP * 0.2)
            self.play(FadeIn(no), Indicate(gn_lps, color=PINK), run_time=self.fit(0.8))
            self.tag("Janeway p.44-45")

        with self.beat("b17"):
            self.clear()
            hdr = self.header("Antimicrobial peptides", ORANGE)
            self.play(Write(hdr), run_time=self.fit(0.8))
            three = VGroup(label_box("defensins", GREEN, 30), label_box("cathelicidins", GREEN, 30),
                           label_box("histatins", GREEN, 30)).arrange(RIGHT, buff=0.7).move_to([0, 2.0, 0])
            self.play(LaggedStart(*[FadeIn(k, shift=DOWN * 0.2) for k in three], lag_ratio=0.5), run_time=self.fit(2.5))
            self.w(1.0)
            self.play(Circumscribe(three[0], color=YELLOW), run_time=self.fit(0.8))
            desc = T("small cationic peptides · act within minutes", 28, CHALK).move_to([0, 0.9, 0])
            self.play(FadeIn(desc), run_time=self.fit(0.6))
            xs = np.linspace(-5.0, 5.0, 34)
            top = VGroup(*[Circle(0.13, color=BLUE, stroke_width=2).set_fill(BLUE, 0.4).move_to([x, -0.6, 0]) for x in xs])
            bot = VGroup(*[Circle(0.13, color=BLUE, stroke_width=2).set_fill(BLUE, 0.4).move_to([x, -1.5, 0]) for x in xs])
            tails = VGroup(*[Line([x, -0.75, 0], [x, -1.35, 0], color=BLUE, stroke_width=1.5) for x in xs])
            ml = T("microbial membrane", 24, BLUE).move_to([0, -2.0, 0])
            self.play(FadeIn(top), FadeIn(bot), FadeIn(tails), FadeIn(ml), run_time=self.fit(1))
            holes = [6, 7, 16, 17, 26, 27]
            pep = VGroup(*[Dot(radius=0.12, color=GREEN).move_to([xs[h] + 0.15, 0.2, 0]) for h in holes[::2]])
            self.play(FadeIn(pep), run_time=0.3)
            self.play(*[p.animate.move_to([xs[h] + 0.15, -1.05, 0]) for p, h in zip(pep, holes[::2])],
                      run_time=self.fit(0.8))
            gone = VGroup(*[top[h] for h in holes], *[bot[h] for h in holes], *[tails[h] for h in holes])
            self.play(FadeOut(gone), run_time=self.fit(0.6))
            tg = T("bacteria · fungi · some enveloped viruses", 28, PINK).move_to([0, -2.85, 0])
            self.play(FadeIn(tg), run_time=self.fit(0.6))
            self.tag("Janeway p.45; Abbas p.80")

        with self.beat("b18"):
            self.clear()
            hdr = self.header("Where they come from", ORANGE)
            self.play(Write(hdr), run_time=self.fit(0.8))
            spec = [("α-defensins", "Paneth cells in small-bowel crypts"),
                    ("β-defensins", "airway, urogenital tract, skin, tongue"),
                    ("LL-37 (cathelicidin)", "binds and neutralizes LPS"),
                    ("histatins", "salivary glands; act on Candida albicans")]
            ys = [1.8, 0.6, -0.6, -1.8]
            for (k, v), y in zip(spec, ys):
                box = label_box(k, GREEN, 28).move_to([-3.6, y, 0])
                txt = fit_w(T(v, 28, CHALK), 6.2).move_to([0, y, 0]).align_to([-0.6, 0, 0], LEFT)
                arr = chalk_arrow(box.get_right(), [-0.7, y, 0], GREY, buff=0.1)
                self.play(FadeIn(box, shift=RIGHT * 0.2), run_time=self.fit(0.6))
                self.play(GrowArrow(arr), FadeIn(txt), run_time=self.fit(0.8))
                self.w(3.2)
            self.tag("Abbas p.80; Janeway p.46")

        # ---- microbiological barrier ----
        with self.beat("b19"):
            self.clear()
            hdr = self.header("3 · Microbiological barrier", GREEN)
            epi = epithelium(y=-1.0, h=1.0)
            self.play(Write(hdr), FadeIn(epi), run_time=self.fit(1))
            cells = epi[0]
            ytop = cells.get_top()[1]
            comm = VGroup(*[RoundedRectangle(corner_radius=0.1, width=0.45, height=0.22, color=GREEN, stroke_width=3)
                            .set_fill(GREEN, 0.4).move_to([x, ytop + 0.18, 0])
                            for x in np.linspace(-4.95, 4.95, 18)])
            self.play(LaggedStart(*[GrowFromCenter(c) for c in comm], lag_ratio=0.05), run_time=self.fit(1.2))
            cl = T("commensals", 28, GREEN).move_to([-4.6, ytop + 0.75, 0])
            self.play(FadeIn(cl), run_time=0.4)
            path = microbe(PINK).move_to([1.3, 1.0, 0])
            self.play(FadeIn(path), run_time=0.3)
            self.play(path.animate.move_to([1.3, ytop + 0.45, 0]), run_time=self.fit(0.7), rate_func=rush_into)
            self.play(path.animate.move_to([2.8, 0.9, 0]), run_time=self.fit(0.6), rate_func=rush_from)
            pb = bullet_list(["compete for nutrients and attachment sites",
                              "make antimicrobials: lactic acid, bacteriocins",
                              "make epithelia produce antimicrobial peptides"], size=28).move_to([0, 2.05, 0])
            self.play(FadeIn(pb[0], shift=RIGHT * 0.2), run_time=self.fit(0.7))
            self.w(2.5)
            self.play(FadeIn(pb[1], shift=RIGHT * 0.2), run_time=self.fit(0.7))
            self.w(2.5)
            self.play(FadeIn(pb[2], shift=RIGHT * 0.2), run_time=self.fit(0.7))
            ups = VGroup(*[Arrow([x, ytop + 0.05, 0], [x, ytop - 0.45, 0], buff=0, color=GREEN, stroke_width=3,
                                 max_tip_length_to_length_ratio=0.35) for x in (-3.0, 0.0, 3.0)])
            self.play(LaggedStart(*[GrowArrow(a) for a in ups], lag_ratio=0.3), run_time=self.fit(1))
            self.tag("Janeway p.44")
            self.mb = (epi, comm, cl, path, pb, ups)

        with self.beat("b20"):
            epi, comm, cl, path, pb, ups = self.mb
            ytop = epi[0].get_top()[1]
            ab = label_box("antibiotics", ORANGE, 30).move_to([-3.6, 2.05, 0])
            self.play(FadeOut(pb), FadeOut(ups), FadeIn(ab, shift=DOWN * 0.2), run_time=self.fit(0.8))
            self.play(LaggedStart(*[FadeOut(c, scale=0.3) for c in comm], lag_ratio=0.04), FadeOut(cl),
                      run_time=self.fit(1.2))
            invaders = VGroup(*[microbe(PINK).move_to([x, ytop + 0.18, 0]) for x in np.linspace(-4.6, 4.6, 12)])
            self.play(ReplacementTransform(VGroup(path), invaders[5]), run_time=self.fit(0.5))
            self.play(LaggedStart(*[GrowFromCenter(i) for k, i in enumerate(invaders) if k != 5], lag_ratio=0.08),
                      run_time=self.fit(1.2))
            dis = T("pathogens take over → disease", 30, PINK).move_to([1.6, 2.05, 0])
            self.play(FadeIn(dis), run_time=self.fit(0.6))
            self.w(0.8)
            ph = cell(0.42, BLUE).move_to([-2.5, -2.75, 0])
            phl = T("phagocytes beneath all epithelia", 28, BLUE).next_to(ph, RIGHT, buff=0.3)
            self.play(GrowFromCenter(ph), FadeIn(phl), run_time=self.fit(1))
            self.play(Indicate(ph, color=BLUE, scale_factor=1.3), run_time=self.fit(0.8))
            self.tag("Janeway p.38, p.44")

        # ================= D3 time course =================
        with self.beat("b21"):
            self.clear()
            hdr = self.header("Time course of the response")
            self.play(Write(hdr), run_time=self.fit(1))
            X0, X4, X96, XE = -6.0, -2.7, 2.1, 6.3
            axis = Arrow([X0 - 0.1, 0, 0], [XE + 0.2, 0, 0], buff=0, color=CHALK, stroke_width=4,
                         max_tip_length_to_length_ratio=0.03)
            ticks = VGroup(*[Line([x, -0.12, 0], [x, 0.12, 0], color=CHALK, stroke_width=4) for x in (X0, X4, X96)])
            tlabs = VGroup(T("0", 28).move_to([X0, -0.45, 0]), T("4 h", 28).move_to([X4, -0.45, 0]),
                           T("96 h", 28).move_to([X96, -0.45, 0]))
            self.play(GrowArrow(axis), Create(ticks), FadeIn(tlabs), run_time=self.fit(1.5))
            self.w(1.2)

            def block(x1, x2, color, name):
                r = Rectangle(width=x2 - x1 - 0.08, height=0.7, color=color, stroke_width=3).set_fill(color, 0.2)
                r.move_to([(x1 + x2) / 2, 0.45, 0])
                t = fit_w(T(name, 26, color), x2 - x1 - 0.3).move_to(r)
                return VGroup(r, t)

            p1 = block(X0, X4, GREEN, "1 · Immediate")
            self.play(GrowFromEdge(p1[0], LEFT), FadeIn(p1[1]), run_time=self.fit(1.2))
            self.w(1.5)
            mols = VGroup(T("lysozyme", 26), T("defensins", 26), T("complement", 26)).arrange(DOWN, buff=0.12)
            mols.move_to([(X0 + X4) / 2, 1.5, 0])
            pre = T("preformed, soluble", 24, GREY).next_to(mols, UP, buff=0.15)
            self.play(FadeIn(pre), run_time=self.fit(0.5))
            self.w(1.0)
            self.play(LaggedStart(*[FadeIn(m, shift=DOWN * 0.2) for m in mols], lag_ratio=0.4), run_time=self.fit(1.5))
            self.tag("Janeway p.37")
            self.d3 = dict(X0=X0, X4=X4, X96=X96, XE=XE, block=block, tlabs=tlabs, ticks=ticks)

        with self.beat("b22"):
            d = self.d3
            p2 = d["block"](d["X4"], d["X96"], BLUE, "2 · Early induced innate")
            self.play(GrowFromEdge(p2[0], LEFT), FadeIn(p2[1]), run_time=self.fit(1.5))
            self.w(1.5)
            xc = (d["X4"] + d["X96"]) / 2
            ac = cell(0.3, BLUE, nucleus=True).move_to([d["X4"] + 1.0, 1.45, 0])
            spk = spiky_microbe(PINK, 0.18, 6).move_to([d["X4"] + 0.25, 1.95, 0])
            l1 = T("cells recognize PAMPs", 26, CHALK).next_to(ac, RIGHT, buff=0.2)
            self.play(FadeIn(spk), GrowFromCenter(ac), run_time=self.fit(0.8))
            self.play(spk.animate.next_to(ac, LEFT, buff=0.02), ac[0].animate.set_fill(YELLOW, 0.3),
                      FadeIn(l1), run_time=self.fit(1))
            self.w(1.5)
            l2 = T("inflammation limits spread", 26, PINK).move_to([xc, 2.25, 0])
            self.play(FadeIn(l2, shift=DOWN * 0.2), run_time=self.fit(0.8))
            self.tag("Janeway p.37, p.42")

        with self.beat("b23"):
            d = self.d3
            xc = (d["X4"] + d["X96"]) / 2
            dcl = T("DCs carry antigen → lymph node", 26, BLUE).move_to([xc, -1.25, 0])
            self.play(FadeIn(dcl, shift=UP * 0.2), run_time=self.fit(1))
            self.w(2.0)
            p3 = d["block"](d["X96"], d["XE"], YELLOW, "3 · Adaptive")
            self.play(GrowFromEdge(p3[0], LEFT), FadeIn(p3[1]), run_time=self.fit(1.2))
            self.w(1.5)
            x3 = (d["X96"] + d["XE"]) / 2
            one = cell(0.2, YELLOW, nucleus=False).move_to([x3, 1.55, 0])
            self.play(GrowFromCenter(one), run_time=self.fit(0.5))
            clone = VGroup(*[cell(0.2, YELLOW, nucleus=False) for _ in range(8)]).arrange_in_grid(2, 4, buff=0.12)
            clone.move_to([x3, 1.75, 0])
            self.play(ReplacementTransform(VGroup(*[one.copy() for _ in range(8)]), clone), FadeOut(one),
                      run_time=self.fit(1.5))
            cl = T("rare B + T cells expand", 26, YELLOW).next_to(clone, DOWN, buff=0.12)
            self.play(FadeIn(cl), run_time=self.fit(0.6))
            self.tag("Janeway p.37, p.43")

        with self.beat("b24"):
            d = self.d3
            pts = VGroup(
                T("innate acts within minutes", 28, GREEN),
                T("adaptive needed only if innate is bypassed, evaded or overwhelmed", 28, CHALK),
                T("innate keeps pathogen numbers in check meanwhile", 28, GREEN),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
            fit_w(pts, 12.4).move_to([0, -2.55, 0])
            # make sure we do not collide with the DC line at y=-1.25
            if pts.get_top()[1] > -1.6:
                pts.shift(DOWN * (pts.get_top()[1] + 1.6))
            for p in pts:
                self.play(FadeIn(p, shift=UP * 0.2), run_time=self.fit(0.7))
                self.w(2.6)
            fuzzy = VGroup(*[DashedLine([x, -0.2, 0], [x, 2.6, 0], color=GREY, stroke_width=2, dash_length=0.12)
                             for x in (d["X4"], d["X96"])])
            ap = T("boundaries are approximate", 24, GREY).move_to([4.5, -0.8, 0])
            self.play(Create(fuzzy), FadeIn(ap), Wiggle(d["tlabs"][1:]), run_time=self.fit(1.5))
            self.tag("Janeway p.38; Abbas p.3")

        with self.beat("b25"):
            self.clear()
            inn = label_box("INNATE", GREEN, 44).move_to([-3.8, 0, 0])
            ada = label_box("ADAPTIVE", YELLOW, 44).move_to([3.8, 0, 0])
            self.play(FadeIn(inn), FadeIn(ada), run_time=self.fit(1))
            top = CurvedArrow(inn.get_top() + UP * 0.15, ada.get_top() + UP * 0.15, angle=-PI / 3, color=CHALK,
                              stroke_width=4)
            bot = CurvedArrow(ada.get_bottom() + DOWN * 0.15, inn.get_bottom() + DOWN * 0.15, angle=-PI / 3,
                              color=CHALK, stroke_width=4)
            tl = T("early danger signals start it", 30, CHALK).next_to(top, UP, buff=0.15)
            bl = T("makes innate mechanisms stronger", 30, CHALK).next_to(bot, DOWN, buff=0.15)
            self.w(0.8)
            self.play(Create(top), FadeIn(tl), run_time=self.fit(1.5))
            self.w(2.0)
            self.play(Create(bot), FadeIn(bl), run_time=self.fit(1.5))
            self.tag("Abbas p.3")

        # ================= RECAP + TRAP =================
        with self.beat("b26"):
            self.clear()
            hdr = self.header("Five things to remember")
            self.play(Write(hdr), run_time=self.fit(1))
            items = ["Innate: ready before infection; limited memory",
                     "< 100 germline-encoded, nonclonal receptor types",
                     "Barriers: mechanical, chemical, microbiological",
                     "Key molecules: lysozyme, defensins, cathelicidin, histatins",
                     "Phases: 0–4 h · 4–96 h · > 96 h"]
            rows = VGroup(*[VGroup(T(f"{i + 1}", 34, YELLOW), T(s, 32, CHALK)).arrange(RIGHT, buff=0.35)
                            for i, s in enumerate(items)]).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
            fit_w(rows, 12.6).move_to([0, -0.35, 0])
            self.recap = rows
            for r, gap in zip(rows[:3], (4.0, 4.5, 3.0)):
                self.play(FadeIn(r, shift=RIGHT * 0.3), run_time=self.fit(0.8))
                self.w(gap)

        with self.beat("b27"):
            rows = self.recap
            self.play(FadeIn(rows[3], shift=RIGHT * 0.3), run_time=self.fit(0.8))
            self.w(5.0)
            self.play(FadeIn(rows[4], shift=RIGHT * 0.3), run_time=self.fit(0.8))
            self.w(1.5)
            self.play(Circumscribe(rows[4], color=YELLOW), run_time=self.fit(1.2))

        with self.beat("b28"):
            self.clear()
            title = T("Exam trap", 52, PINK).move_to([0, 2.4, 0])
            self.play(Write(title), run_time=self.fit(1))
            q = T("Lysozyme works better against…", 36, CHALK).move_to([0, 1.2, 0])
            self.play(FadeIn(q), run_time=self.fit(0.8))
            a = T("✓  Gram-positive bacteria", 36, GREEN).move_to([0, 0.0, 0])
            b = T("✗  Gram-negative bacteria", 36, PINK).move_to([0, -1.0, 0])
            self.w(0.8)
            self.play(FadeIn(a, shift=RIGHT * 0.3), run_time=self.fit(0.8))
            self.play(FadeIn(b, shift=RIGHT * 0.3), run_time=self.fit(0.8))
            why = T("LPS outer layer covers the peptidoglycan", 30, GREY).move_to([0, -2.2, 0])
            self.w(1.5)
            self.play(Write(why), run_time=self.fit(1.5))
            box = chalk_box(VGroup(title, q, a, b, why), PINK, buff=0.4)
            self.play(Create(box), run_time=self.fit(1))
            self.tag("Janeway p.45")

        with self.beat("b29"):
            self.clear()
            nx = T("Next: V2 · The cells of innate immunity", 44, YELLOW).move_to([0, 2.2, 0])
            self.play(Write(nx), run_time=self.fit(1.5))
            names = ["phagocytes", "DCs", "NK cells", "mast cells", "eosinophils", "ILCs"]
            cols = [BLUE, BLUE, BLUE, BLUE, BLUE, BLUE]
            cs = VGroup(*[cell(0.5, c, label=n, size=26) for n, c in zip(names, cols)]).arrange(RIGHT, buff=0.3)
            fit_w(cs, 12.8).move_to([0, -0.3, 0])
            self.play(LaggedStart(*[GrowFromCenter(c) for c in cs], lag_ratio=0.25), run_time=self.fit(5))
            self.tag("Abbas p.4")

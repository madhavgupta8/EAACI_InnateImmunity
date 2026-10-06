from chalk import *


# ---------- local helpers (V2 only) ----------
def leaf(label, color=BLUE, size=26):
    dot = Circle(0.15, color=color, stroke_width=3).set_fill(color, 0.35)
    t = T(label, size, color).next_to(dot, RIGHT, buff=0.18)
    return VGroup(dot, t)


def lobed_nucleus(scale=1.0, color=BLUE):
    lobes = VGroup(*[Ellipse(width=0.55, height=0.42, color=color, stroke_width=3).set_fill(color, 0.3)
                     for _ in range(4)])
    for i, l in enumerate(lobes):
        l.move_to([(-0.6 + i * 0.4) * scale, (0.18 if i % 2 else -0.12) * scale, 0]).scale(scale)
    return lobes


def dc_cell(r=0.55, color=BLUE, label=None, size=26):
    """Star-shaped dendritic cell."""
    pts = []
    for i in range(16):
        a = i * TAU / 16
        rr = r * (1.55 if i % 2 == 0 else 0.85)
        pts.append([rr * np.cos(a), rr * np.sin(a), 0])
    body = Polygon(*pts, color=color, stroke_width=4).set_fill(color, 0.12)
    body.round_corners(0.08)
    g = VGroup(body, Circle(r * 0.4, color=color, stroke_width=3).set_fill(color, 0.3))
    if label:
        g.add(T(label, size, color).next_to(body, DOWN, buff=0.12))
    return g


def antibody(color=YELLOW, h=0.45, stroke=4):
    """A small 'Y' (antibody); stem points down."""
    stem = Line(ORIGIN, UP * h * 0.55, color=color, stroke_width=stroke)
    a1 = Line(UP * h * 0.55, UP * h + LEFT * h * 0.35, color=color, stroke_width=stroke)
    a2 = Line(UP * h * 0.55, UP * h + RIGHT * h * 0.35, color=color, stroke_width=stroke)
    return VGroup(stem, a1, a2)


def microbe(color=PINK, r=0.16):
    return VGroup(Ellipse(width=r * 2.4, height=r * 1.4, color=color, stroke_width=3).set_fill(color, 0.35))


def granules(center, radius, n, color, seed=1, r=0.06):
    rng = np.random.default_rng(seed)
    dots = VGroup()
    while len(dots) < n:
        p = rng.uniform(-1, 1, 2) * radius
        if np.hypot(*p) < radius:
            dots.add(Dot(np.array([p[0], p[1], 0]) + center, radius=r, color=color))
    return dots


def card(title, lines, color=BLUE, w=6.0, size=26, tsize=32):
    t = T(title, tsize, color)
    body = VGroup(*[T(l, size, CHALK) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    inner = VGroup(t, body).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    w = max(w, inner.width + 0.55)
    box = RoundedRectangle(corner_radius=0.15, width=w, height=inner.height + 0.45,
                           stroke_color=color, stroke_width=3).set_fill(color, 0.08)
    inner.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.25)
    return VGroup(box, inner)


class V2(ChalkScene):
    VIDEO_ID = "V2"

    def src(self, text):
        """Show one citation at a time (replace the previous tag)."""
        old = getattr(self, "_tag", None)
        if old is not None and old in self.mobjects:
            self.remove(old)
        self._tag = self.source_tag(text)
        self.add(self._tag)

    def at(self, frac):
        """Wait until a fraction of the current beat has elapsed."""
        w = frac * self.bd - self.elapsed()
        if w > 0.05:
            self.wait(w)

    def construct(self):
        # ================= b01 hook =================
        with self.beat("b01"):
            t = self.title_card("The cells of innate immunity", "Video 2 · EAACI exam pack")
            self.play(Write(t), run_time=self.fit(2.5))
            self.play(t.animate.scale(0.7).to_edge(UP, buff=0.5), run_time=self.fit(0.8))
            hooks = bullet_list(["Where does each cell come from?",
                                 "How does an NK cell pick a target?",
                                 "Mast cell or eosinophil: what differs?"], size=34).next_to(t, DOWN, buff=0.7)
            for i, row in enumerate(hooks):
                self.at(0.3 + 0.18 * i)
                self.play(FadeIn(row, shift=RIGHT * 0.3), run_time=self.fit(0.8))

        # ================= b02-b06 lineage tree (D4) =================
        with self.beat("b02"):
            self.clear_board()
            hdr = self.header("Where innate cells come from")
            self.play(Write(hdr), run_time=self.fit(1.0))
            hsc = label_box("HSC", BLUE, size=34).move_to([-5.4, 0.4, 0])
            mk = T("CD34 · c-KIT", 24, BLUE).next_to(hsc, UP, buff=0.2)
            marrow = T("bone marrow", 24, GREY).next_to(mk, UP, buff=0.25)
            self.play(GrowFromCenter(hsc), FadeIn(marrow), run_time=self.fit(1.2))
            self.at(0.6)
            self.play(Write(mk), run_time=self.fit(1.2))
            self.src(("Abbas p.30"))

        my_y = [2.55, 1.95, 1.35, 0.75, 0.15, -0.45]
        ly_y = [-1.35, -1.95, -2.55, -3.15]
        LX = -0.4
        with self.beat("b03"):
            myp = label_box("myeloid", GREEN, size=28).move_to([-2.7, 1.05, 0])
            a = chalk_arrow(hsc, myp, stroke=3)
            self.play(GrowArrow(a), FadeIn(myp), run_time=self.fit(1.0))
            names = ["neutrophil", "eosinophil", "basophil", "monocyte", "dendritic cell"]
            mleaves = VGroup(*[leaf(n, BLUE).move_to([LX, y, 0], aligned_edge=LEFT)
                               for n, y in zip(names, my_y)])
            mlines = VGroup(*[Line(myp.get_right(), l[0].get_left(), color=GREEN, stroke_width=2)
                              for l in mleaves])
            for i in range(4):
                self.play(Create(mlines[i]), FadeIn(mleaves[i], shift=RIGHT * 0.2), run_time=self.fit(0.7))
            self.at(0.6)
            self.play(Create(mlines[4]), FadeIn(mleaves[4], shift=RIGHT * 0.2), run_time=self.fit(0.8))
            self.play(Indicate(mleaves[3], color=YELLOW), Indicate(mleaves[4], color=YELLOW),
                      run_time=self.fit(1.2))
            self.src(("Abbas p.32"))

        with self.beat("b04"):
            mast = leaf("mast precursor", BLUE).move_to([LX, my_y[5], 0], aligned_edge=LEFT)
            ml = Line(myp.get_right(), mast[0].get_left(), color=GREEN, stroke_width=2)
            border = DashedLine([4.3, 2.9, 0], [4.3, -0.8, 0], color=GREY, dash_length=0.15)
            bm = T("marrow", 24, GREY).next_to(border.get_end(), DOWN, buff=0.15).shift(LEFT * 0.65)
            ts = T("tissue", 24, GREY).next_to(border.get_end(), DOWN, buff=0.15).shift(RIGHT * 0.6)
            self.play(Create(ml), FadeIn(mast, shift=RIGHT * 0.2), run_time=self.fit(0.8))
            self.play(Create(border), FadeIn(bm), FadeIn(ts), run_time=self.fit(0.8))
            mature = cell(0.3, BLUE, nucleus=True).move_to([5.4, my_y[5], 0])
            mlab = T("mast cell", 24, BLUE).next_to(mature, UP, buff=0.1)
            ma = chalk_arrow([3.7, my_y[5], 0], mature, color=BLUE, stroke=3)
            self.play(GrowArrow(ma), FadeIn(mature), FadeIn(mlab), run_time=self.fit(1.5))
            self.at(0.55)
            stay = T("stays in marrow", 24, GREEN).next_to(mleaves[2], RIGHT, buff=0.35)
            self.play(Indicate(mleaves[2], color=GREEN), FadeIn(stay), run_time=self.fit(1.2))
            self.src(("Abbas p.20, 32"))

        with self.beat("b05"):
            lyp = label_box("lymphoid", PINK, size=28).move_to([-2.7, -2.25, 0])
            a2 = chalk_arrow(hsc, lyp, stroke=3)
            self.play(GrowArrow(a2), FadeIn(lyp), run_time=self.fit(1.0))
            lnames = [("T cell", GREY), ("B cell", GREY), ("NK cell", BLUE), ("ILC", BLUE)]
            lleaves = VGroup(*[leaf(n, c).move_to([LX, y, 0], aligned_edge=LEFT)
                               for (n, c), y in zip(lnames, ly_y)])
            llines = VGroup(*[Line(lyp.get_right(), l[0].get_left(), color=PINK, stroke_width=2)
                              for l in lleaves])
            for i in range(2):
                self.play(Create(llines[i]), FadeIn(lleaves[i], shift=RIGHT * 0.2), run_time=self.fit(0.6))
            self.at(0.45)
            self.play(Create(llines[2]), FadeIn(lleaves[2], shift=RIGHT * 0.2),
                      Create(llines[3]), FadeIn(lleaves[3], shift=RIGHT * 0.2), run_time=self.fit(1.0))
            shared = DashedVMobject(SurroundingRectangle(VGroup(lleaves[2], lleaves[3]), color=YELLOW,
                                                         buff=0.2, corner_radius=0.1))
            sl = T("shared precursor", 24, YELLOW).next_to(shared, RIGHT, buff=0.3)
            self.play(Create(shared), FadeIn(sl), run_time=self.fit(1.2))
            self.src(("Abbas p.30"))

        with self.beat("b06"):
            self.play(FadeOut(stay), FadeOut(sl), run_time=0.4)
            gf = [(0, "G-CSF"), (3, "M-CSF"), (4, "FLT3L"), (1, "IL-5"), (5, "SCF")]
            tags = VGroup()
            for k, (i, name) in enumerate(gf):
                tg = T(name, 26, YELLOW).move_to([2.9, my_y[i], 0], aligned_edge=LEFT)
                tags.add(tg)
            self.at(0.22)
            for k, tg in enumerate(tags):
                self.play(FadeIn(tg, shift=LEFT * 0.3, scale=1.3), run_time=self.fit(0.9))
                self.at(0.22 + 0.15 * (k + 1))
            self.src(("Abbas p.14-15, 20, 466"))

        # ================= b07-b10 neutrophils =================
        with self.beat("b07"):
            self.clear_board()
            hdr = self.header("Neutrophils")
            self.play(Write(hdr), run_time=self.fit(0.8))
            nc = Circle(1.6, color=BLUE, stroke_width=5).set_fill(BLUE, 0.1).move_to([-3.6, -0.4, 0])
            nuc = Ellipse(width=1.3, height=0.9, color=BLUE, stroke_width=3).set_fill(BLUE, 0.3).move_to(nc)
            self.play(Create(nc), FadeIn(nuc), run_time=self.fit(1.2))
            f1 = T("most abundant white cell", 32, CHALK).move_to([2.5, 1.6, 0])
            f2 = T("40–60% of leukocytes", 32, YELLOW).next_to(f1, DOWN, buff=0.3)
            self.play(Write(f1), run_time=self.fit(1.2))
            self.play(Write(f2), run_time=self.fit(1.0))
            self.at(0.55)
            lobes = lobed_nucleus(1.4).move_to(nc)
            self.play(Transform(nuc, lobes), run_time=self.fit(1.5))
            f3 = T("3–5 lobes → “polymorphonuclear”", 30, BLUE).next_to(f2, DOWN, buff=0.6)
            f4 = T("PMN", 40, YELLOW).next_to(f3, DOWN, buff=0.3)
            self.play(FadeIn(f3, shift=UP * 0.2), run_time=self.fit(1.0))
            self.play(Write(f4), run_time=self.fit(0.8))
            self.src(("Abbas p.14"))

        with self.beat("b08"):
            self.play(FadeOut(VGroup(f1, f2, f3, f4)), run_time=0.4)
            spec = granules(nc.get_center(), 1.35, 26, YELLOW, seed=3)
            azu = granules(nc.get_center(), 1.35, 10, PINK, seed=5, r=0.08)
            c1 = card("Specific granules (most)", ["lysozyme", "collagenase", "elastase"], YELLOW, w=5.6)
            c2 = card("Azurophilic granules", ["myeloperoxidase", "defensins", "cathelicidins"], PINK, w=5.6)
            VGroup(c1, c2).arrange(DOWN, buff=0.35).move_to([2.9, -0.4, 0])
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in spec], lag_ratio=0.05), run_time=self.fit(1.5))
            self.play(FadeIn(c1, shift=LEFT * 0.3), run_time=self.fit(1.0))
            self.at(0.55)
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in azu], lag_ratio=0.08), run_time=self.fit(1.0))
            self.play(FadeIn(c2, shift=LEFT * 0.3), run_time=self.fit(1.0))
            self.src(("Abbas p.14"))

        with self.beat("b09"):
            self.play(FadeOut(c1), FadeOut(c2), run_time=0.4)
            r1 = VGroup(T("Neutrophil", 32, BLUE), T("fast · preformed enzymes", 28, GREEN),
                        T("lives 1–2 days in tissue", 28, CHALK)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            r2 = VGroup(T("Macrophage", 32, BLUE), T("slower", 28, CHALK),
                        T("often needs new gene transcription", 28, CHALK)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            VGroup(r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to([2.6, -0.4, 0])
            bolt = T("⚡", 48, YELLOW).next_to(nc, UP, buff=0.1)
            self.play(FadeIn(r1[0]), FadeIn(r1[1], shift=RIGHT * 0.2), FadeIn(bolt), run_time=self.fit(1.2))
            self.at(0.25)
            self.play(FadeIn(r1[2], shift=RIGHT * 0.2), run_time=self.fit(1.0))
            self.at(0.55)
            self.play(FadeIn(r2, shift=RIGHT * 0.2), run_time=self.fit(1.2))
            self.src(("Abbas p.15"))

        with self.beat("b10"):
            self.play(FadeOut(r1), FadeOut(r2), FadeOut(bolt), run_time=0.4)
            c = nc.get_center()
            strands, bugs = VGroup(), VGroup()
            for k in range(7):
                ang = -0.9 + k * 0.3
                p0 = c + 1.6 * np.array([np.cos(ang), np.sin(ang), 0])
                p1 = c + 3.1 * np.array([np.cos(ang), np.sin(ang), 0])
                mid = (p0 + p1) / 2 + 0.3 * np.array([-np.sin(ang), np.cos(ang), 0])
                strands.add(VMobject(color=CHALK, stroke_width=2).set_points_smoothly([p0, mid, p1]))
                if k % 2 == 0:
                    bugs.add(microbe().move_to(p0 + 0.7 * (p1 - p0)))
            self.play(LaggedStart(*[Create(s) for s in strands], lag_ratio=0.15), run_time=self.fit(2.0))
            lab = T("NETs: neutrophil extracellular traps", 30, YELLOW).move_to([2.3, 2.3, 0])
            self.play(Write(lab), run_time=self.fit(1.2))
            self.play(FadeIn(bugs, scale=0.5), run_time=self.fit(0.8))
            k1 = T("trap and kill microbes", 30, GREEN).move_to([3.9, 0.2, 0])
            k2 = T("can damage healthy tissue", 30, PINK).next_to(k1, DOWN, buff=0.35)
            self.play(FadeIn(k1, shift=LEFT * 0.2), bugs.animate.set_opacity(0.3), run_time=self.fit(1.0))
            self.at(0.7)
            self.play(FadeIn(k2, shift=LEFT * 0.2), run_time=self.fit(1.0))
            self.src(("Abbas p.15"))

        # ================= b11-b15 monocytes & macrophages =================
        with self.beat("b11"):
            self.clear_board()
            hdr = self.header("Monocytes & macrophages")
            self.play(Write(hdr), run_time=self.fit(0.8))
            v1 = Line([-6.4, 2.3, 0], [0.2, 2.3, 0], color=PINK, stroke_width=3)
            v2 = Line([-6.4, 1.1, 0], [0.2, 1.1, 0], color=PINK, stroke_width=3)
            vl = T("blood", 24, GREY).move_to([-5.7, 1.7, 0])
            mono = cell(0.35, BLUE).move_to([-4.4, 1.7, 0])
            ml = T("classical monocytes: 90–95%", 28, BLUE).next_to(v1, UP, buff=0.12).align_to(v1, LEFT).shift(RIGHT * 0.3)
            self.play(Create(v1), Create(v2), FadeIn(vl), FadeIn(mono), run_time=self.fit(1.0))
            self.play(Write(ml), run_time=self.fit(1.2))
            mac = cell(0.75, BLUE).move_to([-2.4, -1.2, 0])
            site = VGroup(microbe().move_to([-1.2, -0.6, 0]), microbe().move_to([-1.0, -1.7, 0]))
            self.play(FadeIn(site), run_time=self.fit(0.5))
            self.play(mono.animate.move_to([-2.4, -1.2, 0]), run_time=self.fit(1.2))
            self.play(Transform(mono, mac), run_time=self.fit(1.0))
            mlab = T("macrophage", 26, BLUE).next_to(mac, DOWN, buff=0.15)
            self.play(FadeIn(mlab), run_time=self.fit(0.5))
            self.at(0.5)
            res = card("Tissue-resident macrophages",
                       ["yolk sac / fetal liver precursors", "long-lived, self-renewing"], GREEN, w=6.0)
            res.move_to([3.4, -0.6, 0])
            self.play(FadeIn(res, shift=LEFT * 0.3), run_time=self.fit(1.5))
            self.src(("Abbas p.15-16"))

        with self.beat("b12"):
            self.play(FadeOut(VGroup(v1, v2, vl, ml, mono, site, mlab)), res.animate.move_to([0, 1.6, 0]),
                      run_time=self.fit(0.8))
            three = VGroup(*[VGroup(cell(0.45, BLUE), T(a, 28, BLUE), T(b, 24, GREY)).arrange(DOWN, buff=0.15)
                             for a, b in [("Kupffer cells", "liver"), ("alveolar macrophages", "lung"),
                                          ("microglia", "brain")]]).arrange(RIGHT, buff=0.8).move_to([0, -1.5, 0])
            self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.3) for x in three], lag_ratio=0.4),
                      run_time=self.fit(3.5))
            self.src(("Abbas p.15"))

        with self.beat("b13"):
            self.clear_board()
            hdr = self.header("Source conflict")
            self.play(Write(hdr), run_time=self.fit(0.8))
            colA = T("Abbas 11th ed.", 32, YELLOW).move_to([-0.6, 2.2, 0])
            colJ = T("Janeway 8th ed.", 32, GREY).move_to([4.0, 2.2, 0])
            rowM = T("Tissue macrophages", 30, BLUE).move_to([-4.85, 1.0, 0])
            rowD = T("Dendritic cells", 30, BLUE).move_to([-4.85, -0.6, 0])
            a1 = T("mostly fetal precursors", 28, CHALK).move_to([-0.6, 1.0, 0])
            j1 = T("from blood monocytes", 28, CHALK).move_to([4.0, 1.0, 0])
            a2 = T("mostly myeloid", 28, CHALK).move_to([-0.6, -0.6, 0])
            j2 = T("myeloid + lymphoid", 28, CHALK).move_to([4.0, -0.6, 0])
            self.play(FadeIn(colA), FadeIn(colJ), run_time=self.fit(0.8))
            self.play(FadeIn(rowM), FadeIn(j1, shift=LEFT * 0.2), run_time=self.fit(1.0))
            self.at(0.3)
            self.play(FadeIn(rowD), FadeIn(j2, shift=LEFT * 0.2), run_time=self.fit(1.0))
            self.at(0.55)
            self.play(FadeIn(a1, shift=RIGHT * 0.2), FadeIn(a2, shift=RIGHT * 0.2), run_time=self.fit(1.0))
            use = label_box("Exam: use Abbas", GREEN, size=34).move_to([0, -2.4, 0])
            self.play(FadeIn(use, scale=1.2), Circumscribe(VGroup(colA, a1, a2), color=GREEN),
                      run_time=self.fit(1.5))
            self.src(("Abbas p.15, 32 · Janeway p.76-77"))

        with self.beat("b14"):
            self.clear_board()
            hdr = self.header("What macrophages do")
            self.play(Write(hdr), run_time=self.fit(0.8))
            mac = cell(1.1, BLUE).move_to([-3.6, -0.3, 0])
            self.play(Create(mac), run_time=self.fit(1.0))
            j1 = VGroup(T("1. cytokines", 30, YELLOW), T("TNF, IL-1", 28, CHALK)).arrange(RIGHT, buff=0.3)
            j2 = VGroup(T("2. efferocytosis", 30, YELLOW), T("clears apoptotic cells", 28, CHALK)).arrange(RIGHT, buff=0.3)
            j3 = VGroup(T("3. SIRPα", 30, YELLOW), T("reads CD47 “don’t eat me”", 28, CHALK)).arrange(RIGHT, buff=0.3)
            jobs = VGroup(j1, j2, j3).arrange(DOWN, aligned_edge=LEFT, buff=0.7).move_to([2.1, -0.3, 0])
            for k, j in enumerate(jobs):
                self.at([0.08, 0.35, 0.6][k])
                self.play(FadeIn(j, shift=LEFT * 0.3), run_time=self.fit(1.0))
                if k == 0:
                    puffs = VGroup(*[Dot(mac.get_center() + 1.4 * np.array([np.cos(a), np.sin(a), 0]),
                                         radius=0.07, color=YELLOW) for a in np.linspace(0.3, 1.3, 4)])
                    self.play(LaggedStart(*[FadeIn(p, shift=0.3 * (p.get_center() - mac.get_center()))
                                            for p in puffs]), run_time=self.fit(0.8))
                if k == 1:
                    apo = Circle(0.3, color=GREY, stroke_width=3).set_fill(GREY, 0.2).move_to(mac.get_center() + DOWN * 1.8)
                    self.play(FadeIn(apo), run_time=self.fit(0.4))
                    self.play(apo.animate.move_to(mac.get_center() + DOWN * 0.5).scale(0.6), run_time=self.fit(1.0))
                if k == 2:
                    sign = label_box("CD47", GREEN, size=26).next_to(mac, UP, buff=0.5)
                    self.play(FadeIn(sign, shift=DOWN * 0.2), run_time=self.fit(0.8))
            self.src(("Abbas p.16, 19"))

        with self.beat("b15"):
            self.clear_board()
            hdr = self.header("Macrophage activation")
            self.play(Write(hdr), run_time=self.fit(0.8))
            mac = cell(0.7, BLUE).move_to([-4.6, 0, 0])
            self.play(FadeIn(mac), run_time=self.fit(0.6))
            s1 = T("LPS + IFN-γ", 30, YELLOW).move_to([-1.6, 1.6, 0])
            m1 = label_box("M1: kill microbes", GREEN, size=32).move_to([3.4, 1.6, 0])
            ar1 = chalk_arrow(mac, s1, stroke=3)
            ar1b = chalk_arrow(s1, m1, color=GREEN)
            self.play(GrowArrow(ar1), FadeIn(s1), run_time=self.fit(1.0))
            self.play(GrowArrow(ar1b), FadeIn(m1, shift=RIGHT * 0.3), run_time=self.fit(1.2))
            self.at(0.42)
            s2 = T("IL-4 + IL-13", 30, YELLOW).move_to([-1.6, -1.6, 0])
            m2 = label_box("M2: repair, fibrosis", ORANGE, size=32).move_to([3.4, -1.6, 0])
            ar2 = chalk_arrow(mac, s2, stroke=3)
            ar2b = chalk_arrow(s2, m2, color=ORANGE)
            self.play(GrowArrow(ar2), FadeIn(s2), run_time=self.fit(1.0))
            self.play(GrowArrow(ar2b), FadeIn(m2, shift=RIGHT * 0.3), run_time=self.fit(1.2))
            self.at(0.75)
            note = T("many macrophages fit neither box", 28, GREY).move_to([1.0, -3.1, 0])
            self.play(FadeIn(note, shift=UP * 0.2), run_time=self.fit(1.0))
            self.src(("Abbas p.19"))

        # ================= b16-b19 dendritic cells =================
        with self.beat("b16"):
            self.clear_board()
            hdr = self.header("Dendritic cells: the sentinels")
            self.play(Write(hdr), run_time=self.fit(0.8))
            epi = VMobject(color=PINK, stroke_width=3).set_points_smoothly(
                [[-6.4, -2.6, 0], [-5.2, -2.3, 0], [-4.0, -2.6, 0], [-2.8, -2.3, 0]])
            tl = T("tissue", 24, GREY).next_to(epi, DOWN, buff=0.15)
            dc = dc_cell(0.4).move_to([-4.6, -1.2, 0])
            ag = microbe(YELLOW).move_to([-3.4, -0.4, 0])
            self.play(Create(epi), FadeIn(tl), FadeIn(dc), FadeIn(ag), run_time=self.fit(1.2))
            self.play(ag.animate.move_to(dc.get_center() + RIGHT * 0.15), run_time=self.fit(1.0))
            node = Ellipse(width=3.2, height=2.0, color=GREEN, stroke_width=4).move_to([0.6, 0.9, 0])
            nl = T("lymph node", 26, GREEN).next_to(node, UP, buff=0.12)
            self.play(Create(node), FadeIn(nl), run_time=self.fit(1.0))
            self.play(VGroup(dc, ag).animate.move_to(node.get_center() + LEFT * 0.7), run_time=self.fit(1.5))
            self.at(0.5)
            tcell = cell(0.3, CHALK, label=None).move_to(node.get_center() + RIGHT * 0.7)
            tl2 = T("naive T", 24, CHALK).next_to(tcell, DOWN, buff=0.08)
            self.play(FadeIn(tcell), FadeIn(tl2), run_time=self.fit(0.8))
            th1 = label_box("Th1", YELLOW, size=28).move_to([4.8, 1.9, 0])
            th17 = label_box("Th17", YELLOW, size=28).move_to([4.8, -0.1, 0])
            self.at(0.7)
            self.play(GrowArrow(chalk_arrow(node, th1)), FadeIn(th1),
                      GrowArrow(chalk_arrow(node, th17)), FadeIn(th17), run_time=self.fit(1.5))
            self.src(("Abbas p.20, 81"))

        with self.beat("b17"):
            self.clear_board()
            hdr = self.header("Dendritic cell subsets")
            self.play(Write(hdr), run_time=self.fit(0.8))
            c2 = card("cDC2", ["most numerous", "presents to CD4 T cells"], BLUE, w=6.0)
            c1 = card("cDC1", ["cross-presents to naive CD8 T cells", "makes IL-12"], BLUE, w=6.0)
            c2.move_to([-3.25, 1.3, 0])
            c1.move_to([3.25, 1.3, 0])
            self.play(FadeIn(c2, shift=UP * 0.3), run_time=self.fit(1.2))
            self.at(0.45)
            self.play(FadeIn(c1, shift=UP * 0.3), run_time=self.fit(1.2))
            self.src(("Abbas p.21-23"))

        with self.beat("b18"):
            pd = card("Plasmacytoid DC (pDC)", ["high TLR7, TLR9", "main source of type I IFN"], YELLOW, w=6.0)
            lc = card("Langerhans cell", ["dendritic cell of the epidermis"], BLUE, w=6.0)
            pd.move_to([-3.25, -1.6, 0])
            lc.move_to([3.25, -1.6, 0]).align_to(pd, UP)
            self.play(FadeIn(pd, shift=UP * 0.3), run_time=self.fit(1.2))
            self.play(Indicate(pd[1][1][1], color=YELLOW), run_time=self.fit(1.0))
            self.at(0.68)
            self.play(FadeIn(lc, shift=UP * 0.3), run_time=self.fit(1.2))
            self.src(("Abbas p.22-23"))

        with self.beat("b19"):
            self.clear_board()
            trap = T("EXAM TRAP", 48, PINK).move_to([0, 2.6, 0])
            self.play(Write(trap), run_time=self.fit(0.8))
            fdc = label_box("“Follicular dendritic cell”", BLUE, size=34).move_to([0, 1.2, 0])
            self.play(FadeIn(fdc), run_time=self.fit(0.8))
            pts = bullet_list(["stromal cell", "not from bone marrow", "does not present protein antigen to T cells"],
                              size=30).move_to([0, -0.8, 0])
            for k, p in enumerate(pts):
                self.at(0.25 + 0.2 * k)
                self.play(FadeIn(p, shift=RIGHT * 0.2), run_time=self.fit(0.8))
            nd = T("not a true DC", 30, PINK).next_to(fdc, RIGHT, buff=0.3)
            self.play(Create(strike(fdc[1], stroke=4)), FadeIn(nd), run_time=self.fit(0.8))
            self.src(("Abbas p.22"))

        # ================= b20-b27 NK cells (D6) =================
        with self.beat("b20"):
            self.clear_board()
            hdr = self.header("Natural killer (NK) cells")
            self.play(Write(hdr), run_time=self.fit(0.8))
            nk = cell(0.9, BLUE).move_to([-4.3, 0.6, 0])
            nkl = T("NK cell", 30, BLUE).next_to(nk, DOWN, buff=0.15)
            self.play(Create(nk), FadeIn(nkl), run_time=self.fit(1.0))
            tags = VGroup(T("CD56⁺", 30, GREEN), T("CD3⁻", 30, PINK)).arrange(DOWN, buff=0.2).next_to(nk, RIGHT, buff=0.4)
            self.play(FadeIn(tags, shift=LEFT * 0.2), run_time=self.fit(1.0))
            self.at(0.3)
            g = T("germline-encoded receptors · no prior activation", 28, CHALK).move_to([0, -1.2, 0])
            self.play(Write(g), run_time=self.fit(1.5))
            self.at(0.6)
            ax = Arrow([-5.0, -2.6, 0], [5.6, -2.6, 0], buff=0, color=CHALK, stroke_width=3, tip_length=0.2)
            axl = T("days after infection", 24, GREY).next_to(ax, DOWN, buff=0.1)
            nkm = label_box("NK: early", GREEN, size=28).move_to([-3.2, -2.0, 0])
            ctl = label_box("CTL fully active: 5–7 days", GREY, size=26).move_to([2.6, -2.0, 0])
            self.play(GrowArrow(ax), FadeIn(axl), run_time=self.fit(0.8))
            self.play(FadeIn(nkm, shift=UP * 0.2), run_time=self.fit(0.7))
            self.play(FadeIn(ctl, shift=UP * 0.2), run_time=self.fit(0.8))
            self.src(("Abbas p.82"))

        with self.beat("b21"):
            self.clear_board()
            nk = cell(0.8, BLUE, label="NK cell", size=28).move_to([-4.5, 0, 0])
            self.play(FadeIn(nk), run_time=self.fit(0.5))
            tgt = cell(0.6, PINK, label="infected cell", size=26).move_to([0.3, 1.6, 0])
            k1 = chalk_arrow(nk, tgt, color=PINK)
            kl = T("perforin + granzymes", 28, YELLOW).next_to(k1, UP, buff=0.05).shift(LEFT * 0.4)
            self.play(FadeIn(tgt), GrowArrow(k1), FadeIn(kl), run_time=self.fit(1.2))
            ap = T("→ apoptosis", 30, PINK).next_to(tgt, RIGHT, buff=0.3)
            self.play(FadeIn(ap), tgt[0].animate.set_stroke(opacity=0.4), run_time=self.fit(1.0))
            self.at(0.5)
            mac = cell(0.6, BLUE, label="macrophage", size=26).move_to([0.3, -1.9, 0])
            k2 = chalk_arrow(nk, mac, color=YELLOW)
            k2l = T("IFN-γ", 30, YELLOW).next_to(k2, DOWN, buff=0.05).shift(LEFT * 0.4)
            self.play(FadeIn(mac), GrowArrow(k2), FadeIn(k2l), run_time=self.fit(1.2))
            act = T("→ activated", 30, GREEN).next_to(mac, RIGHT, buff=0.3).align_to(mac[0], UP)
            self.play(FadeIn(act), Indicate(mac[0], color=GREEN), run_time=self.fit(1.0))
            self.src(("Abbas p.82"))

        # ---- balance scale ----
        with self.beat("b22"):
            self.clear_board()
            hdr = self.header("Missing self: the NK balance")
            self.play(Write(hdr), run_time=self.fit(0.8))
            pivot = np.array([0, -0.3, 0])
            fulcrum = Triangle(color=CHALK, stroke_width=4).scale(0.5).move_to(pivot + DOWN * 0.42)
            base = Line(pivot + DOWN * 0.85 + LEFT * 0.9, pivot + DOWN * 0.85 + RIGHT * 0.9, color=CHALK, stroke_width=4)
            beam = Line(pivot + LEFT * 3.4, pivot + RIGHT * 3.4, color=CHALK, stroke_width=5)

            def pan(x, color):
                s1 = Line(pivot + RIGHT * x, pivot + RIGHT * x + DOWN * 1.1 + LEFT * 0.7, color=color, stroke_width=2)
                s2 = Line(pivot + RIGHT * x, pivot + RIGHT * x + DOWN * 1.1 + RIGHT * 0.7, color=color, stroke_width=2)
                dish = Arc(radius=0.8, start_angle=PI + 0.5, angle=PI - 1.0, color=color, stroke_width=4)
                dish.move_to(pivot + RIGHT * x + DOWN * 1.25)
                return VGroup(s1, s2, dish)

            lp, rp = pan(-3.4, GREEN), pan(3.4, PINK)
            self.play(Create(fulcrum), Create(base), Create(beam), run_time=self.fit(1.2))
            self.play(Create(lp), Create(rp), run_time=self.fit(1.0))
            self.at(0.3)
            il = T("inhibitory", 32, GREEN).move_to(pivot + LEFT * 3.4 + DOWN * 2.15)
            al = T("activating", 32, PINK).move_to(pivot + RIGHT * 3.4 + DOWN * 2.15)
            self.play(Write(il), Write(al), run_time=self.fit(1.2))
            self.at(0.62)
            itim = T("ITIM", 28, GREEN).next_to(il, DOWN, buff=0.15)
            itam = T("ITAM", 28, PINK).next_to(al, DOWN, buff=0.15)
            self.play(FadeIn(itim, shift=UP * 0.2), run_time=self.fit(0.8))
            self.play(FadeIn(itam, shift=UP * 0.2), run_time=self.fit(0.8))
            self.src(("Abbas p.83, 85"))

        with self.beat("b23"):
            lw = VGroup(T("KIR", 28, GREEN), T("CD94/NKG2A", 28, GREEN)).arrange(DOWN, buff=0.08)
            lw.move_to(pivot + LEFT * 3.4 + UP * 0.75)
            lt = T("bind MHC class I", 26, CHALK).next_to(lw, UP, buff=0.12)
            rw = T("NKG2D", 28, PINK).move_to(pivot + RIGHT * 3.4 + UP * 0.55)
            rt = T("binds stress proteins", 26, CHALK).next_to(rw, UP, buff=0.12)
            self.play(FadeIn(lw, shift=DOWN * 0.3), run_time=self.fit(1.2))
            self.play(FadeIn(lt), run_time=self.fit(0.8))
            self.at(0.5)
            self.play(FadeIn(rw, shift=DOWN * 0.3), run_time=self.fit(1.2))
            self.play(FadeIn(rt), run_time=self.fit(0.8))
            self.src(("Abbas p.83, 85"))
        left_side = VGroup(lp, lw, lt, il, itim)
        right_side = VGroup(rp, rw, rt, al, itam)

        def tilt(angle):
            """Rotate beam about pivot; pans and their labels follow the beam ends (stay upright)."""
            new_l = pivot + 3.4 * np.array([-np.cos(angle), -np.sin(angle), 0])
            new_r = pivot + 3.4 * np.array([np.cos(angle), np.sin(angle), 0])
            cur_l = beam.get_start()
            cur_r = beam.get_end()
            return [Rotate(beam, angle - np.arctan2(*(beam.get_end() - beam.get_start())[[1, 0]]), about_point=pivot),
                    left_side.animate.shift(new_l - cur_l), right_side.animate.shift(new_r - cur_r)]

        with self.beat("b24"):
            hc = cell(0.45, GREEN, nucleus=True).move_to([0, 2.15, 0])
            mhc = VGroup(*[antibody(GREEN, 0.4).rotate(PI / 2) for _ in range(3)]).arrange(DOWN, buff=0.08)
            mhc.next_to(hc, LEFT, buff=0.0)
            hl = T("healthy cell", 26, GREEN).next_to(hc, DOWN, buff=0.1)
            ml = T("MHC-I", 26, GREEN).next_to(hc, RIGHT, buff=0.15)
            self.play(FadeIn(hc), FadeIn(hl), FadeIn(mhc), FadeIn(ml), run_time=self.fit(1.2))
            self.play(*tilt(0.14), run_time=self.fit(1.5))
            nk = T("no kill", 34, GREEN).move_to([0, 0.85, 0])
            self.play(FadeIn(nk, scale=1.2), run_time=self.fit(0.8))
            self.src(("Abbas p.85"))

        with self.beat("b25"):
            self.play(FadeOut(nk), hc.animate.set_color(PINK), hl.animate.become(
                T("infected cell", 26, PINK).next_to(hc, DOWN, buff=0.1)),
                run_time=self.fit(1.0))
            self.at(0.15)
            st = strike(VGroup(mhc, ml))
            self.play(Create(st), run_time=self.fit(0.8))
            self.play(FadeOut(mhc), FadeOut(ml), FadeOut(st), run_time=self.fit(0.8))
            self.at(0.4)
            self.play(*tilt(-0.14), run_time=self.fit(1.5))
            kill = T("KILL", 44, PINK).move_to([0, 0.85, 0])
            self.play(FadeIn(kill, scale=1.4), run_time=self.fit(0.6))
            self.at(0.7)
            ms = label_box("missing self", YELLOW, size=34).move_to([0, -2.5, 0])
            self.play(FadeIn(ms, shift=UP * 0.2), run_time=self.fit(1.0))
            self.src(("Abbas p.85"))

        with self.beat("b26"):
            self.clear_board()
            hdr = self.header("CD16 and ADCC")
            self.play(Write(hdr), run_time=self.fit(0.8))
            nk = cell(0.9, BLUE, label="NK cell", size=28).move_to([-3.6, -0.3, 0])
            tg = cell(0.8, PINK, label="IgG-coated cell", size=28).move_to([2.6, -0.3, 0])
            self.play(FadeIn(nk), FadeIn(tg), run_time=self.fit(1.0))
            igs = VGroup()
            for ang in [PI - 0.6, PI, PI + 0.6]:
                y = antibody(YELLOW, 0.5).rotate(ang + PI / 2)
                y.move_to(tg[0].get_center() + 1.05 * np.array([np.cos(ang), np.sin(ang), 0]))
                igs.add(y)
            self.play(LaggedStart(*[FadeIn(y, shift=RIGHT * 0.2) for y in igs]), run_time=self.fit(1.0))
            cd16 = VGroup(*[Line(nk[0].get_center() + 0.9 * np.array([np.cos(a), np.sin(a), 0]),
                                 nk[0].get_center() + 1.25 * np.array([np.cos(a), np.sin(a), 0]),
                                 color=GREEN, stroke_width=5) for a in [-0.5, 0, 0.5]])
            cl = T("CD16", 30, GREEN).next_to(cd16, UP, buff=0.3)
            self.play(Create(cd16), FadeIn(cl), run_time=self.fit(1.0))
            sub = T("binds IgG1 and IgG3", 30, YELLOW).move_to([-0.5, 1.9, 0])
            self.play(Write(sub), run_time=self.fit(1.0))
            self.play(VGroup(nk, cd16, cl).animate.shift(RIGHT * 1.4), run_time=self.fit(1.0))
            self.at(0.55)
            ad = label_box("ADCC: antibody-dependent cell-mediated cytotoxicity", YELLOW, size=28).move_to([0, -2.6, 0])
            self.play(FadeIn(ad, shift=UP * 0.2), run_time=self.fit(1.2))
            self.src(("Abbas p.84"))

        with self.beat("b27"):
            self.clear_board()
            hdr = self.header("Clinical link: NK cell deficiency", PINK)
            self.play(Write(hdr), run_time=self.fit(0.8))
            inf = card("Severe infections", ["herpesviruses", "papillomaviruses"], PINK, w=5.4)
            inf.move_to([-3.3, 0.2, 0])
            self.play(FadeIn(inf, shift=UP * 0.3), run_time=self.fit(1.2))
            self.at(0.4)
            causes = card("Causes", ["GATA2 mutations", "CD16 mutations", "Chediak-Higashi syndrome"], PINK, w=5.6)
            causes.move_to([3.3, 0.2, 0])
            self.play(FadeIn(causes[0]), FadeIn(causes[1][0]), run_time=self.fit(0.6))
            for k, line in enumerate(causes[1][1]):
                self.at(0.5 + 0.12 * k)
                self.play(FadeIn(line, shift=RIGHT * 0.2), run_time=self.fit(0.7))
            self.src(("Abbas p.488"))

        # ================= b28-b36 mast cells, basophils, eosinophils =================
        with self.beat("b28"):
            self.clear_board()
            hdr = self.header("The allergy trio")
            self.play(Write(hdr), run_time=self.fit(0.8))
            trio = VGroup()
            for k, (name, col) in enumerate([("mast cell", BLUE), ("basophil", BLUE), ("eosinophil", BLUE)]):
                c = cell(0.85, col, nucleus=True)
                g = granules(c.get_center(), 0.75, 18, [YELLOW, PINK, ORANGE][k], seed=k + 10, r=0.07)
                trio.add(VGroup(c, g, T(name, 32, col).next_to(c, DOWN, buff=0.2)))
            trio.arrange(RIGHT, buff=1.6).move_to([0, 0.5, 0])
            for k in range(3):
                self.play(FadeIn(trio[k][0]), FadeIn(trio[k][2]), run_time=self.fit(0.7))
            self.at(0.35)
            self.play(*[LaggedStart(*[FadeIn(d, scale=0.4) for d in t[1]], lag_ratio=0.05) for t in trio],
                      run_time=self.fit(1.5))
            gl = T("granules full of mediators", 30, YELLOW).move_to([0, -1.9, 0])
            self.play(FadeIn(gl), run_time=self.fit(0.8))
            self.at(0.7)
            al = T("all take part in allergic disease", 30, PINK).next_to(gl, DOWN, buff=0.3)
            self.play(FadeIn(al), run_time=self.fit(0.8))
            self.src(("Abbas p.20"))

        with self.beat("b29"):
            self.clear_board()
            hdr = self.header("Mast cells")
            self.play(Write(hdr), run_time=self.fit(0.8))
            vtop = Line([-6.4, 2.0, 0], [-0.6, 2.0, 0], color=PINK, stroke_width=3)
            vbot = Line([-6.4, 1.2, 0], [-0.6, 1.2, 0], color=PINK, stroke_width=3)
            vl = T("vessel", 24, GREY).next_to(vtop, UP, buff=0.1).align_to(vtop, LEFT)
            nerve = VMobject(color=YELLOW, stroke_width=3).set_points_smoothly(
                [[-6.4, -2.6, 0], [-4.5, -2.2, 0], [-2.5, -2.7, 0], [-0.6, -2.3, 0]])
            nl = T("nerve", 24, GREY).next_to(nerve, DOWN, buff=0.1).align_to(nerve, LEFT)
            mc = cell(0.7, BLUE).move_to([-3.5, -0.5, 0])
            mg = granules(mc.get_center(), 0.6, 14, YELLOW, seed=20, r=0.06)
            self.play(Create(vtop), Create(vbot), FadeIn(vl), Create(nerve), FadeIn(nl), run_time=self.fit(1.2))
            self.play(FadeIn(mc), FadeIn(mg), run_time=self.fit(0.8))
            nb = T("not in blood", 30, PINK).move_to([3.2, 1.6, 0])
            self.play(FadeIn(nb), run_time=self.fit(0.8))
            self.at(0.5)
            ckit = T("c-KIT", 28, BLUE).next_to(mc, RIGHT, buff=0.15)
            scf = T("SCF", 30, YELLOW).move_to([3.2, -0.5, 0])
            sa = chalk_arrow(scf, ckit, color=YELLOW)
            self.play(FadeIn(ckit), run_time=self.fit(0.6))
            self.play(FadeIn(scf), GrowArrow(sa), run_time=self.fit(1.0))
            ess = T("essential for development", 28, GREEN).next_to(scf, DOWN, buff=0.3)
            self.play(FadeIn(ess), run_time=self.fit(0.8))
            self.src(("Abbas p.465"))

        with self.beat("b30"):
            self.clear_board()
            hdr = self.header("FcεRI: the high-affinity IgE receptor")
            self.play(Write(hdr), run_time=self.fit(0.8))
            mc = cell(0.9, BLUE, label="mast cell", size=28).move_to([-4.0, 0.2, 0])
            self.play(FadeIn(mc), run_time=self.fit(0.6))
            ys = VGroup()
            for ang in [0.9, 1.6, 2.3]:
                y = antibody(YELLOW, 0.5).rotate(ang - PI / 2)
                y.move_to(mc[0].get_center() + 1.15 * np.array([np.cos(ang), np.sin(ang), 0]))
                ys.add(y)
            self.play(LaggedStart(*[GrowFromCenter(y) for y in ys]), run_time=self.fit(1.2))
            note = T("IgE stays bound, even in nonatopic people", 28, CHALK).move_to([0, -2.9, 0])
            self.at(0.25)
            self.play(Write(note), run_time=self.fit(1.5))
            self.at(0.55)
            axis = Line([0.4, -1.8, 0], [6.2, -1.8, 0], color=CHALK, stroke_width=3)
            bars = VGroup()
            for k, (nm, h, col) in enumerate([("mast", 2.8, GREEN), ("baso", 2.8, GREEN), ("eos", 0.6, PINK)]):
                r = Rectangle(width=1.1, height=h, color=col, stroke_width=3).set_fill(col, 0.35)
                r.move_to([1.3 + 1.9 * k, -1.8 + h / 2, 0])
                lab = T(nm, 26, CHALK).next_to(r, DOWN, buff=0.12).set_y(-2.15)
                bars.add(VGroup(r, lab))
            self.play(Create(axis), run_time=self.fit(0.5))
            for k, bgrp in enumerate(bars):
                self.play(GrowFromEdge(bgrp[0], DOWN), FadeIn(bgrp[1]), run_time=self.fit(0.8))
            hi = T("high", 26, GREEN).next_to(VGroup(bars[0][0], bars[1][0]), UP, buff=0.12)
            lo = T("low", 26, PINK).next_to(bars[2][0], UP, buff=0.12)
            self.play(FadeIn(hi), FadeIn(lo), run_time=self.fit(0.6))
            self.src(("Abbas p.466"))

        with self.beat("b31"):
            self.clear_board()
            mc = cell(1.0, BLUE).move_to([-3.8, -0.4, 0])
            mg = granules(mc.get_center(), 0.85, 16, YELLOW, seed=30, r=0.07)
            yl = antibody(YELLOW, 0.55).move_to(mc[0].get_top() + UP * 0.25 + LEFT * 0.5)
            yr = antibody(YELLOW, 0.55).move_to(mc[0].get_top() + UP * 0.25 + RIGHT * 0.5)
            self.play(FadeIn(mc), FadeIn(mg), FadeIn(yl), FadeIn(yr), run_time=self.fit(0.8))
            allergen = label_box("allergen", PINK, size=26).move_to([-3.8, 2.9, 0])
            self.play(FadeIn(allergen), run_time=self.fit(0.4))
            self.play(allergen.animate.move_to(mc[0].get_top() + UP * 0.95), run_time=self.fit(1.0))
            xl = T("cross-link", 28, YELLOW).next_to(allergen, RIGHT, buff=0.3)
            self.play(FadeIn(xl), run_time=self.fit(0.5))
            # degranulation
            self.play(*[d.animate.shift(0.9 * (d.get_center() - mc.get_center())) for d in mg],
                      run_time=self.fit(1.0))
            pre = card("Released (preformed)", ["histamine", "tryptase"], YELLOW, w=5.4).move_to([2.9, 1.0, 0])
            new = card("Newly made", ["prostaglandin D2", "leukotrienes", "platelet-activating factor"], ORANGE, w=5.4)
            new.next_to(pre, DOWN, buff=0.35)
            self.play(FadeIn(pre, shift=LEFT * 0.3), run_time=self.fit(0.8))
            self.at(0.55)
            self.play(FadeIn(new, shift=LEFT * 0.3), run_time=self.fit(1.0))
            self.src(("Abbas p.467-468"))

        with self.beat("b32"):
            self.clear_board()
            hdr = self.header("Mast cells without IgE")
            self.play(Write(hdr), run_time=self.fit(0.8))
            mc = cell(0.9, BLUE, label="mast cell", size=28).move_to([0, -0.4, 0])
            self.play(FadeIn(mc), run_time=self.fit(0.6))
            ana = label_box("C3a, C5a", PINK, size=30).move_to([-4.6, 1.5, 0])
            self.at(0.15)
            self.play(FadeIn(ana), GrowArrow(chalk_arrow(ana, mc, color=PINK)), run_time=self.fit(1.0))
            dg = T("degranulation", 28, PINK).next_to(ana, DOWN, buff=0.3)
            self.play(FadeIn(dg), run_time=self.fit(0.6))
            self.at(0.42)
            mr = T("MRGPRX2", 28, BLUE).next_to(mc[0], RIGHT, buff=0.2)
            drugs = label_box("some drugs", ORANGE, size=30).move_to([4.6, 1.5, 0])
            self.play(FadeIn(mr), run_time=self.fit(0.6))
            self.play(FadeIn(drugs), GrowArrow(chalk_arrow(drugs, mr, color=ORANGE)), run_time=self.fit(1.0))
            sk = T("skin mast cells", 24, GREY).next_to(mr, DOWN, buff=0.1)
            self.play(FadeIn(sk), run_time=self.fit(0.5))
            self.at(0.7)
            ar = T("likely: some allergy-like drug reactions", 28, ORANGE).move_to([0, -2.9, 0])
            self.play(Write(ar), run_time=self.fit(1.2))
            self.src(("Abbas p.470"))

        with self.beat("b33"):
            self.clear_board()
            hdr = self.header("Clinical link: tryptase", PINK)
            self.play(Write(hdr), run_time=self.fit(0.8))
            t1 = card("Tryptase", ["in ALL human mast cells", "in no other known cell type"], YELLOW, w=6.4)
            t1.move_to([0, 1.3, 0])
            self.play(FadeIn(t1, shift=UP * 0.3), run_time=self.fit(1.2))
            self.at(0.35)
            t2 = label_box("serum tryptase → anaphylaxis diagnosis", GREEN, size=30).move_to([0, -0.6, 0])
            self.play(FadeIn(t2, shift=UP * 0.2), run_time=self.fit(1.0))
            self.at(0.65)
            t3 = label_box("systemic mastocytosis: c-KIT mutations", PINK, size=30).move_to([0, -2.2, 0])
            self.play(FadeIn(t3, shift=UP * 0.2), run_time=self.fit(1.0))
            self.src(("Abbas p.470-471"))

        with self.beat("b34"):
            self.clear_board()
            hdr = self.header("Basophils")
            self.play(Write(hdr), run_time=self.fit(0.8))
            vtop = Line([-6.4, 1.3, 0], [6.4, 1.3, 0], color=PINK, stroke_width=3)
            vbot = Line([-6.4, -1.3, 0], [6.4, -1.3, 0], color=PINK, stroke_width=3)
            vl = T("blood", 26, GREY).next_to(vtop, UP, buff=0.1).align_to(vtop, LEFT)
            ba = cell(0.6, BLUE).move_to([-5.0, 0, 0])
            bg = granules(ba.get_center(), 0.5, 10, PINK, seed=40, r=0.06)
            bas = VGroup(ba, bg)
            self.play(Create(vtop), Create(vbot), FadeIn(vl), FadeIn(bas), run_time=self.fit(1.0))
            self.play(bas.animate.move_to([-1.5, 0, 0]), run_time=self.fit(1.5))
            ab = T("normally absent from tissues", 28, CHALK).next_to(vbot, DOWN, buff=0.3)
            self.play(FadeIn(ab), run_time=self.fit(0.8))
            self.at(0.5)
            ys = VGroup(antibody(YELLOW, 0.45).next_to(ba, UP, buff=0.0),
                        antibody(YELLOW, 0.45).rotate(-PI / 2).next_to(ba, RIGHT, buff=0.0))
            self.play(FadeIn(ys), run_time=self.fit(0.8))
            fire = T("binds IgE → fires on antigen", 30, YELLOW).move_to([3.4, 0, 0])
            self.play(Write(fire), run_time=self.fit(1.2))
            self.src(("Abbas p.465"))

        with self.beat("b35"):
            self.clear_board()
            hdr = self.header("Eosinophils")
            self.play(Write(hdr), run_time=self.fit(0.8))
            eo = cell(0.9, BLUE).move_to([-0.8, 0.0, 0])
            eg = granules(eo.get_center(), 0.75, 16, ORANGE, seed=50, r=0.08)
            self.play(FadeIn(eo), FadeIn(eg), run_time=self.fit(0.8))
            il5 = label_box("IL-5", YELLOW, size=30).move_to([-5.0, 1.6, 0])
            src = T("from Th2 cells, ILC2s", 26, GREY).next_to(il5, UP, buff=0.15)
            self.play(FadeIn(il5), FadeIn(src), GrowArrow(chalk_arrow(il5, eo, color=YELLOW)), run_time=self.fit(1.2))
            self.at(0.3)
            eot = label_box("eotaxin", YELLOW, size=30).move_to([-5.0, -1.6, 0])
            cc = T("CCR3", 26, BLUE).next_to(eo[0], LEFT, buff=0.1).shift(DOWN * 0.5)
            self.play(FadeIn(eot), FadeIn(cc), GrowArrow(chalk_arrow(eot, cc, color=YELLOW)), run_time=self.fit(1.2))
            self.at(0.6)
            gr = card("Granules", ["major basic protein (MBP)", "eosinophil cationic protein", "→ damage helminths",
                                   "    and host cells"], ORANGE, w=5.2)
            gr.move_to([3.9, 0, 0])
            self.play(FadeIn(gr, shift=LEFT * 0.3), run_time=self.fit(1.2))
            self.src(("Abbas p.473"))

        with self.beat("b36"):
            self.clear_board()
            trap = T("EXAM TRAP", 48, PINK).move_to([0, 2.7, 0])
            self.play(Write(trap), run_time=self.fit(0.8))
            rows = VGroup()
            for nm, lvl, col in [("mast cell", "FcεRI high", GREEN), ("basophil", "FcεRI high", GREEN),
                                 ("eosinophil", "FcεRI low, no signalling chain", PINK)]:
                rows.add(VGroup(T(nm, 32, BLUE), T(lvl, 30, col)).arrange(RIGHT, buff=0.5))
            rows.arrange(DOWN, buff=0.4).move_to([0, 0.6, 0])
            for r in rows:
                r[1].set_x(-1.2 + r[1].width / 2)
                r[0].set_x(-1.6 - r[0].width / 2)
            self.play(FadeIn(rows[0]), FadeIn(rows[1]), run_time=self.fit(0.8))
            self.play(FadeIn(rows[2], shift=UP * 0.2), run_time=self.fit(0.8))
            self.play(Indicate(rows[2][1], color=PINK), run_time=self.fit(1.0))
            self.at(0.5)
            conc = label_box("no convincing evidence that IgE activates eosinophils", PINK, size=28).move_to([0, -1.8, 0])
            self.play(FadeIn(conc, shift=UP * 0.2), run_time=self.fit(1.5))
            self.src(("Abbas p.473"))

        # ================= b37-b39 ILCs =================
        with self.beat("b37"):
            self.clear_board()
            hdr = self.header("Innate lymphoid cells (ILCs)")
            self.play(Write(hdr), run_time=self.fit(0.8))
            ilc = cell(0.8, BLUE, label="ILC", size=30).move_to([-3.5, 0.3, 0])
            self.play(FadeIn(ilc), run_time=self.fit(0.6))
            tcr = antibody(GREY, 0.6).next_to(ilc[0], UP, buff=0.05)
            tl = T("TCR", 26, GREY).next_to(tcr, LEFT, buff=0.25)
            self.play(FadeIn(tcr), FadeIn(tl), run_time=self.fit(0.6))
            nt = T("no T-cell receptor", 28, PINK).next_to(tcr, RIGHT, buff=0.4)
            self.play(Create(strike(tcr, stroke=4)), FadeIn(nt), run_time=self.fit(0.8))
            self.at(0.35)
            cy = T("cytokines like helper T cells", 30, YELLOW).move_to([2.8, -0.2, 0])
            self.play(FadeIn(cy, shift=LEFT * 0.2), run_time=self.fit(1.0))
            self.at(0.6)
            mu = VMobject(color=PINK, stroke_width=3).set_points_smoothly(
                [[-6.4, -2.4, 0], [-3, -2.0, 0], [0, -2.4, 0], [3, -2.0, 0], [6.4, -2.4, 0]])
            ml = T("mucosa: lung, intestine", 28, PINK).next_to(mu, DOWN, buff=0.15)
            self.play(Create(mu), FadeIn(ml), run_time=self.fit(1.2))
            self.src(("Abbas p.30, 81"))

        with self.beat("b38"):
            self.clear_board()
            hdr = self.header("Three ILC groups")
            self.play(Write(hdr), run_time=self.fit(0.8))
            data = [("ILC1", "T-bet", "IFN-γ", BLUE), ("ILC2", "GATA3", "IL-5, IL-13", PINK),
                    ("ILC3", "RORγt", "IL-22 / IL-17", GREEN)]
            heads = VGroup(T("group", 28, GREY), T("transcription factor", 28, GREY), T("makes", 28, GREY))
            xs = [-4.4, -0.6, 3.6]
            for h, x in zip(heads, xs):
                h.move_to([x, 1.9, 0])
            self.play(FadeIn(heads), run_time=self.fit(0.6))
            for k, (g, tf, cyt, col) in enumerate(data):
                y = 0.9 - 1.15 * k
                row = VGroup(T(g, 34, col).move_to([xs[0], y, 0]), T(tf, 32, YELLOW).move_to([xs[1], y, 0]),
                             T(cyt, 32, CHALK).move_to([xs[2], y, 0]))
                self.at(0.05 + 0.3 * k)
                self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.2) for m in row], lag_ratio=0.3),
                          run_time=self.fit(1.5))
                if k == 1:
                    ilc2row = row
            self.play(Circumscribe(ilc2row, color=PINK), run_time=self.fit(1.0))
            self.src(("Abbas p.81"))

        with self.beat("b39"):
            self.clear_board()
            hdr = self.header("ILC2s start allergic inflammation")
            self.play(Write(hdr), run_time=self.fit(0.8))
            epi = VGroup(*[Rectangle(width=0.9, height=0.6, color=PINK, stroke_width=3).set_fill(PINK, 0.1)
                           for _ in range(6)]).arrange(RIGHT, buff=0).move_to([-3.6, 1.8, 0])
            el = T("epithelium", 26, PINK).next_to(epi, UP, buff=0.12)
            self.play(Create(epi), FadeIn(el), run_time=self.fit(1.0))
            al = VGroup(T("IL-25", 28, YELLOW), T("IL-33", 28, YELLOW), T("TSLP", 28, YELLOW)).arrange(RIGHT, buff=0.4)
            al.next_to(epi, DOWN, buff=0.3)
            self.play(LaggedStart(*[FadeIn(a, shift=DOWN * 0.3) for a in al], lag_ratio=0.3), run_time=self.fit(1.5))
            ilc2 = cell(0.6, BLUE, label="ILC2", size=28).move_to([-3.6, -1.3, 0])
            self.play(FadeIn(ilc2), GrowArrow(chalk_arrow(al, ilc2, color=YELLOW)), run_time=self.fit(1.2))
            self.at(0.42)
            ax = Arrow([-1.4, -2.75, 0], [6.3, -2.75, 0], buff=0, color=CHALK, stroke_width=3, tip_length=0.2)
            axl = T("time", 24, GREY).next_to(ax, DOWN, buff=0.08).align_to(ax, RIGHT)
            self.play(GrowArrow(ax), FadeIn(axl), run_time=self.fit(0.8))
            first = label_box("ILC2: already in tissue", GREEN, size=28).move_to([1.0, -2.0, 0])
            self.play(FadeIn(first, shift=UP * 0.2), run_time=self.fit(1.0))
            self.at(0.68)
            th2 = label_box("Th2 cells: later", GREY, size=28).move_to([4.7, -0.9, 0])
            self.play(FadeIn(th2, shift=LEFT * 0.5), run_time=self.fit(1.2))
            self.src(("Abbas p.81, 94, 465"))

        # ================= b40-b42 recap + trap =================
        with self.beat("b40"):
            self.clear_board()
            hdr = self.header("Five things to remember")
            self.play(Write(hdr), run_time=self.fit(0.8))
            items = ["1. All innate cells come from the HSC",
                     "2. Most tissue macrophages: fetal precursors",
                     "3. Plasmacytoid DCs make type I IFN",
                     "4. NK cells kill when MHC-I is missing",
                     "5. ILC2s start allergic inflammation early"]
            rows = VGroup(*[T(s, 32, CHALK) for s in items]).arrange(DOWN, aligned_edge=LEFT, buff=0.38)
            rows.move_to([0, -0.3, 0])
            for k in range(3):
                self.at(0.12 + 0.27 * k)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.3), run_time=self.fit(1.0))

        with self.beat("b41"):
            self.play(FadeIn(rows[3], shift=RIGHT * 0.3), run_time=self.fit(1.0))
            self.at(0.5)
            self.play(FadeIn(rows[4], shift=RIGHT * 0.3), run_time=self.fit(1.0))
            self.play(Circumscribe(rows, color=YELLOW), run_time=self.fit(1.5))

        with self.beat("b42"):
            self.clear_board()
            trap = T("EXAM TRAP", 48, PINK).move_to([0, 2.4, 0])
            self.play(Write(trap), run_time=self.fit(0.8))
            l1 = Tm(f'CD16 on NK cells binds <span foreground="{GREEN}">IgG</span>, '
                    f'not <span foreground="{PINK}">IgE</span>', size=40).move_to([0, 0.9, 0])
            self.play(Write(l1), run_time=self.fit(1.5))
            self.src(("Abbas p.84"))
            self.at(0.5)
            nxt = label_box("Next: how cells sense danger (PRRs)", YELLOW, size=34).move_to([0, -1.5, 0])
            self.play(FadeIn(nxt, shift=UP * 0.3), run_time=self.fit(1.2))

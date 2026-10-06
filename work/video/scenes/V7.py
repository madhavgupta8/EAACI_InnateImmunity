from chalk import *

# Manim's partial-movie cache advances renderer.time by the exact run_time while the cached
# clip holds whole frames; that drifts the beat timeline (and audio) from the video. Render uncached.
config.disable_caching = True


# ---------- local helpers (V7 only) ----------
def tag(text, color=PINK, size=26):
    """Small boxed tag such as TRAP."""
    return label_box(text, color, size=size, buff=0.14, fill_opacity=0.2)


def row(left, right, lc=BLUE, rc=PINK, size=28, gap=0.5):
    """'left → right' clue row."""
    a = T(left, size, lc)
    ar = T("→", size, CHALK)
    b = T(right, size, rc)
    return VGroup(a, ar, b).arrange(RIGHT, buff=gap * 0.5)


def strike_through(mob, color=PINK, stroke=5):
    """Single line through the middle: text stays readable."""
    return Line(mob.get_left() + LEFT * 0.1, mob.get_right() + RIGHT * 0.1, color=color, stroke_width=stroke)


def tick(color=GREEN, size=34):
    return T("✓", size, color)


def cross(color=PINK, size=34):
    return T("✗", size, color)


def card(title, lines, color=PINK, size=26, width=None):
    """Titled box with short lines (clue card)."""
    head = T(title, size + 4, color)
    body = VGroup(*[T(l, size, CHALK) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    g = VGroup(head, body).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
    box = chalk_box(g, color, buff=0.25).set_fill(color, 0.08)
    if width and box.width < width:
        box.stretch_to_fit_width(width).move_to(g)
    return VGroup(box, g)


MAP_ROWS = [
    ("1 Barriers", "keratin, mucus, cilia, defensins", "cystic fibrosis", GREEN),
    ("2 Sensing", "TLRs, NOD2, NLRP3, RIG-I, cGAS", "MyD88/IRAK4 · TLR3 · CAPS", BLUE),
    ("3 Cells", "neutrophils, macrophages, DCs", "severe congenital neutropenia", GREEN),
    ("4 Phagocytosis", "rolling → arrest; NADPH oxidase", "LAD · CGD · Chédiak-Higashi", GREY),
    ("4 Complement", "C3 convertase → C3b, C5a, MAC", "SLE · Neisseria · HAE · PNH", GREY),
    ("4 Inflammation", "TNF, IL-1, IL-6", "septic shock · IL-1 excess", GREY),
    ("4 NK killing", "missing self; IFN-γ", "herpesvirus (GATA2, CD16)", GREY),
    ("5 Link to adaptive", "signal 1 + signal 2", "MSMD (IL-12/IFN-γ)", "#C9B3E6"),
]


def master_map():
    """D21 as a chalk table: returns (header_row, [row groups])."""
    xs = [-6.45, -3.35, 2.15]          # left edges of the three columns
    widths = [2.95, 5.35, 4.4]
    y0, dy = 2.4, 0.72
    hdr = VGroup(*[T(t, 24, YELLOW).move_to([x, y0 + 0.58, 0], aligned_edge=LEFT)
                   for t, x in zip(["Stage", "Main players", "When it fails"], xs)])
    for h, x in zip(hdr, xs):
        h.align_to([x, 0, 0], LEFT)
    rows = []
    for i, (st, pl, dis, col) in enumerate(MAP_ROWS):
        y = y0 - i * dy
        cells = []
        for j, (txt, c) in enumerate([(st, col if col != GREY else CHALK), (pl, CHALK), (dis, PINK)]):
            t = T(txt, 24, c)
            if t.width > widths[j] - 0.25:
                t.scale_to_fit_width(widths[j] - 0.25)
            box = Rectangle(width=widths[j], height=dy - 0.1, stroke_color=[col, CHALK, PINK][j] if j else col,
                            stroke_width=2).set_fill([col, BLUE, PINK][j], 0.08)
            box.move_to([xs[j] + widths[j] / 2, y, 0])
            t.move_to(box)
            if j:
                t.align_to(box, LEFT).shift(RIGHT * 0.12)
            cells.append(VGroup(box, t))
        rows.append(VGroup(*cells))
    return hdr, rows


class V7(ChalkScene):
    VIDEO_ID = "V7"

    # spread several animation steps evenly over the rest of the beat
    def steps(self, *groups, frac=0.55, maxrt=1.6):
        n = len(groups)
        for i, g in enumerate(groups):
            g = g if isinstance(g, (list, tuple)) else [g]
            slot = (self.remaining() - 0.2) / (n - i)
            rt = min(maxrt, max(0.4, slot * frac))
            self.play(*g, run_time=self.fit(rt))
            if i < n - 1:
                w = min(slot - rt, self.remaining() - 0.4)
                if w > 0.05:
                    self.wait(w)

    def wipe(self, *keep, run_time=0.5):
        keep_ids = set()
        for k in keep:
            keep_ids |= {id(m) for m in k.get_family()}
        mobs = [m for m in self.mobjects if not isinstance(m, ImageMobject) and id(m) not in keep_ids]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=run_time)

    def src(self, text):
        old = getattr(self, "_src", None)
        if old is not None and old in self.mobjects:
            self.remove(old)
        s = self.source_tag(text)
        self.add(s)
        self._src = s
        return s

    def construct(self):
        # ================= intro =================
        with self.beat("b01"):
            t = self.title_card("10-minute exam rapid review", "Innate immunity · M1–M6").shift(UP * 0.9)
            tiles = VGroup(*[label_box(f"M{i}", c, size=30) for i, c in
                             zip(range(1, 7), [GREEN, BLUE, BLUE, BLUE, YELLOW, PINK])]).arrange(RIGHT, buff=0.45)
            tiles.next_to(t, DOWN, buff=0.8)
            m = T("+ one master map", 30, YELLOW).next_to(tiles, DOWN, buff=0.45)
            self.steps(Write(t), LaggedStart(*[FadeIn(x, shift=UP * 0.3) for x in tiles], lag_ratio=0.2),
                       FadeIn(m, shift=UP * 0.2))

        with self.beat("b02"):
            self.clear_board()
            h = T("Lost function  →  disease", 46, YELLOW).to_edge(UP, buff=0.6)
            rows = []
            for k, (comp, dis) in enumerate([("C1q / C2 / C4", "SLE (lupus)"), ("C3", "pyogenic infections"),
                                             ("C5 – C9", "Neisseria")]):
                a = label_box(comp, BLUE, size=32)
                b = T(dis, 34, PINK)
                a.move_to([-3.2, 1.0 - k * 1.5, 0])
                b.move_to([2.8, 1.0 - k * 1.5, 0])
                rows.append((a, b))
            self.play(Write(h), run_time=self.fit(1.2))
            self.src("Abbas p.315")
            self.steps(*[[FadeIn(a), FadeIn(cross(size=40).next_to(a, LEFT, buff=0.3)), GrowArrow(chalk_arrow(a, b)), Write(b)]
                          for a, b in rows])

        # ================= M1 =================
        with self.beat("b03"):
            self.clear_board()
            hd = self.header("M1 · Foundation")
            self.play(FadeIn(hd), run_time=0.6)
            inn = VGroup(T("Innate", 36, GREEN),
                         bullet_list(["germline-encoded", "nonclonal", "< 100 receptor types", "limited memory"], 28))
            inn.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([-3.2, -0.3, 0])
            ada = VGroup(T("Adaptive", 36, GREY),
                         bullet_list(["rearranged genes", "clonal", "Ig + TCR, millions", "memory"], 28, GREY))
            ada.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.2, -0.3, 0])
            div = Line(UP * 1.8, DOWN * 2.4, color=GREY, stroke_width=2)
            self.src("Abbas p.63, 64, 4")
            self.steps([Write(inn[0]), Write(ada[0]), Create(div)],
                       *[[FadeIn(inn[1][i], shift=RIGHT * 0.2), FadeIn(ada[1][i], shift=RIGHT * 0.2)] for i in range(4)])

        with self.beat("b04"):
            self.wipe(hd)
            ax = Line([-6, 0, 0], [6, 0, 0], color=CHALK, stroke_width=4)
            segs = [(-6, -2.6, GREEN, "0–4 h", "immediate\ninnate"), (-2.6, 1.6, BLUE, "4–96 h", "early induced\ninnate"),
                    (1.6, 6, YELLOW, "> 96 h", "adaptive")]
            parts = []
            for a, z, c, tm, lab in segs:
                ln = Line([a, 0, 0], [z, 0, 0], color=c, stroke_width=12)
                t1 = T(tm, 32, c).next_to(ln, UP, buff=0.3)
                t2 = Text(lab, font=FONT, font_size=28, color=CHALK, line_spacing=0.8).next_to(ln, DOWN, buff=0.35)
                parts.append([Create(ln), Write(t1), FadeIn(t2, shift=UP * 0.2)])
            self.play(Create(ax), run_time=self.fit(0.8))
            self.src("Janeway p.37")
            self.steps(*parts)

        with self.beat("b05"):
            self.wipe(hd)
            wall = VGroup(*[Rectangle(width=1.1, height=0.9, stroke_color=BLUE, stroke_width=3).set_fill(BLUE, 0.1)
                            for _ in range(9)]).arrange(RIGHT, buff=0.04).move_to([0, 0.3, 0])
            mucus = Line(wall.get_corner(UL) + UP * 0.25, wall.get_corner(UR) + UP * 0.25, color=GREEN, stroke_width=10)
            cil = VGroup(*[Line(wall[i].get_top(), wall[i].get_top() + UP * 0.45 + RIGHT * 0.12, color=CHALK,
                                stroke_width=2) for i in range(9)])
            labs = VGroup(T("keratin", 28, CHALK), T("tight junctions", 28, CHALK), T("mucus", 28, GREEN),
                          T("cilia", 28, CHALK)).arrange(RIGHT, buff=0.7).next_to(wall, UP, buff=0.9)
            low = VGroup(T("Paneth cells → α-defensins", 28, YELLOW), T("LL-37 neutralizes LPS", 28, YELLOW)) \
                .arrange(RIGHT, buff=1.0).next_to(wall, DOWN, buff=0.5)
            cf = T("Cystic fibrosis: thick mucus → lung infections", 30, PINK).next_to(low, DOWN, buff=0.5)
            self.src("Abbas p.80; Janeway p.44")
            self.steps([Create(wall)], [Create(mucus), Create(cil), Write(labs)], Write(low), Write(cf))

        with self.beat("b06"):
            self.wipe(hd)
            tr = tag("TRAP").to_corner(UL, buff=0.5).shift(DOWN * 0.9)
            gp = VGroup(Rectangle(width=3.4, height=0.8, color=YELLOW, stroke_width=3).set_fill(YELLOW, 0.25),
                        Rectangle(width=3.4, height=0.35, color=BLUE, stroke_width=3))
            gp.arrange(DOWN, buff=0)
            gpl = VGroup(gp, T("Gram-positive", 32, CHALK), T("thick peptidoglycan", 24, YELLOW)).arrange(DOWN, buff=0.25)
            gn = VGroup(Rectangle(width=3.4, height=0.35, color=PINK, stroke_width=3).set_fill(PINK, 0.3),
                        Rectangle(width=3.4, height=0.3, color=YELLOW, stroke_width=3).set_fill(YELLOW, 0.25),
                        Rectangle(width=3.4, height=0.35, color=BLUE, stroke_width=3)).arrange(DOWN, buff=0)
            gnl = VGroup(gn, T("Gram-negative", 32, CHALK), T("LPS layer covers it", 24, PINK)).arrange(DOWN, buff=0.25)
            VGroup(gpl, gnl).arrange(RIGHT, buff=2.2).move_to(DOWN * 0.3)
            lz = T("lysozyme", 32, ORANGE).move_to(UP * 2.0)
            a1 = chalk_arrow(lz, gp, ORANGE)
            a2 = chalk_arrow(lz, gn, ORANGE)
            self.src("Janeway p.45")
            self.steps([FadeIn(tr), Write(gpl), Write(gnl)], [Write(lz), GrowArrow(a1), FadeIn(tick().next_to(gp, RIGHT))],
                       [GrowArrow(a2), FadeIn(cross().next_to(gn, RIGHT))])

        with self.beat("b07"):
            self.wipe(hd)
            cy = VGroup(*[label_box(x, YELLOW, size=34) for x in ["TNF", "IL-1", "IL-6"]]).arrange(DOWN, buff=0.5)
            cy.move_to([-4, -0.2, 0])
            eff = VGroup(T("fever", 32, CHALK), T("leukocytosis", 32, CHALK), T("acute-phase proteins", 32, CHALK)) \
                .arrange(DOWN, aligned_edge=LEFT, buff=0.75).move_to([2.0, -0.2, 0])
            br = Brace(cy, RIGHT, color=CHALK)
            arrs = [chalk_arrow(br.get_tip(), e.get_left() + LEFT * 0.1) for e in eff]
            crp = T("CRP ↑ up to 1000-fold", 30, PINK).next_to(eff[2], DOWN, buff=0.45).align_to(eff, LEFT)
            self.src("Abbas p.90–97, 88")
            self.steps(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in cy], lag_ratio=0.3),
                       [GrowFromCenter(br), *[GrowArrow(a) for a in arrs], LaggedStart(*[Write(e) for e in eff])],
                       Write(crp))

        with self.beat("b08"):
            self.wipe(hd)
            tnf = label_box("TNF", YELLOW, size=36).move_to([-4, 1.2, 0])
            ss = T("septic shock", 34, PINK).move_to([2, 1.2, 0])
            a = chalk_arrow(tnf, ss)
            tr = tag("TRAP").move_to([-5.6, -0.6, 0])
            anti = label_box("anti-TNF", ORANGE, size=32).move_to([-3.2, -0.6, 0])
            s1 = VGroup(T("sepsis trials: no benefit", 30, CHALK), cross()).arrange(RIGHT, buff=0.3).move_to([2.4, -0.2, 0])
            s2 = T("can reactivate tuberculosis", 30, PINK).move_to([2.4, -1.4, 0]).align_to(s1, LEFT)
            self.src("Abbas p.92, 97; Janeway p.109")
            self.steps([FadeIn(tnf), GrowArrow(a), Write(ss)],
                       [FadeIn(tr), FadeIn(anti), GrowArrow(chalk_arrow(anti, s1.get_left() + LEFT * 0.15)), Write(s1)],
                       [GrowArrow(chalk_arrow(anti, s2.get_left() + LEFT * 0.15, PINK)), Write(s2)])

        with self.beat("b09"):
            self.wipe(hd)
            epi = VGroup(*[Rectangle(width=1.2, height=0.7, stroke_color=BLUE, stroke_width=3).set_fill(BLUE, 0.1)
                           for _ in range(9)]).arrange(RIGHT, buff=0.03).move_to(DOWN * 2.6)
            el = T("epithelium", 26, BLUE).next_to(epi, UP, buff=0.12).align_to(epi, LEFT)
            cks = VGroup(*[T(x, 32, YELLOW) for x in ["IL-25", "IL-33", "TSLP"]]).arrange(RIGHT, buff=1.4).move_to(DOWN * 0.9)
            tg = VGroup(*[label_box(x, BLUE, size=30) for x in ["ILC2", "Th2 cell", "mast cell"]]).arrange(RIGHT, buff=1.0)
            tg.move_to(UP * 1.2)
            arrs = [chalk_arrow(cks.get_top(), t, CHALK) for t in tg]
            al = T("IL-33 = alarmin", 28, YELLOW).next_to(cks, RIGHT, buff=0.6).shift(DOWN * 0.0)
            al.to_edge(RIGHT, buff=0.4)
            self.src("Abbas p.94")
            self.steps([Create(epi), FadeIn(el)], LaggedStart(*[FadeIn(c, shift=UP * 0.5) for c in cks], lag_ratio=0.3),
                       [*[GrowArrow(a) for a in arrs], LaggedStart(*[FadeIn(t) for t in tg])],
                       [Indicate(cks[1]), Write(al)])

        # ================= M2 =================
        with self.beat("b10"):
            self.clear_board()
            hd = self.header("M2 · Cells")
            neu = cell(1.1, BLUE, nucleus=False).move_to([-3.5, -0.3, 0])
            lobes = VGroup(*[Circle(0.22, color=BLUE, stroke_width=3).set_fill(BLUE, 0.35).move_to(neu.get_center() + v)
                             for v in [LEFT * 0.35 + UP * 0.1, UP * 0.3, RIGHT * 0.35 + UP * 0.1]])
            gran = VGroup(*[Dot(neu.get_center() + 0.7 * np.array([np.cos(a), np.sin(a), 0]), 0.06, color=YELLOW)
                            for a in np.linspace(0, 2 * np.pi, 9, endpoint=False)])
            nl = T("neutrophil", 30, BLUE).next_to(neu, DOWN, buff=0.25)
            net = VGroup(*[FunctionGraph(lambda x, k=k: 0.15 * np.sin(5 * x + k), x_range=[0, 1.8], color=GREY,
                                         stroke_width=2).rotate(a, about_point=ORIGIN).shift(neu.get_center() + 1.1 * np.array([np.cos(a), np.sin(a), 0]))
                           for k, a in enumerate([2.5, 3.1, 3.7])])
            facts = bullet_list(["most abundant white cell", "arrives first",
                                 "azurophilic granules: MPO, defensins", "NETs trap microbes"], 30).move_to([2.6, -0.3, 0])
            self.src("Abbas p.14, 15, 94")
            self.steps([FadeIn(hd), Create(neu), FadeIn(lobes), Write(nl)], FadeIn(facts[0], shift=RIGHT * 0.2),
                       FadeIn(facts[1], shift=RIGHT * 0.2), [FadeIn(gran), FadeIn(facts[2], shift=RIGHT * 0.2)],
                       [Create(net), FadeIn(facts[3], shift=RIGHT * 0.2)])

        with self.beat("b11"):
            self.wipe(hd)
            mac = cell(0.9, BLUE, label="macrophage", size=28).move_to([-4.6, 0.9, 0])
            ab = T("Abbas: fetal origin, self-renewing", 28, CHALK)
            jw = T("Janeway: from blood monocytes", 28, CHALK)
            VGroup(ab, jw).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([1.3, 1.1, 0])
            vs = T("sources differ", 24, GREY).next_to(VGroup(ab, jw), DOWN, buff=0.2).align_to(ab, LEFT)
            mac2 = cell(0.7, BLUE, nucleus=True).move_to([-2.2, -2.2, 0])
            hc = cell(0.6, GREEN, nucleus=True).move_to([2.2, -2.2, 0])
            l1 = T("SIRPα", 28, BLUE).next_to(mac2, UP, buff=0.15)
            l2 = T("CD47", 28, GREEN).next_to(hc, UP, buff=0.15)
            hs = DoubleArrow(mac2.get_right(), hc.get_left(), color=CHALK, stroke_width=3, buff=0.15, tip_length=0.2)
            de = T("“don't eat me”", 30, YELLOW).next_to(hs, DOWN, buff=0.35)
            self.src("Abbas p.15, 19; Janeway p.76")
            self.steps([FadeIn(mac), Write(ab)], [Write(jw), FadeIn(vs)],
                       [FadeIn(mac2), FadeIn(hc), Write(l1), Write(l2), GrowFromCenter(hs), Write(de)])

        with self.beat("b12"):
            self.wipe(hd)
            p = label_box("plasmacytoid DC", BLUE, size=32).move_to([-3.6, 0.9, 0])
            pi = T("major type I interferon source", 30, YELLOW).move_to([2.4, 0.9, 0])
            c1 = label_box("cDC1", BLUE, size=32).move_to([-3.6, -1.3, 0])
            ci = T("cross-presents → CD8⁺ T cell", 30, YELLOW).move_to([2.4, -1.3, 0])
            self.src("Abbas p.21–23")
            self.steps([FadeIn(p), GrowArrow(chalk_arrow(p, pi)), Write(pi)],
                       [FadeIn(c1), GrowArrow(chalk_arrow(c1, ci)), Write(ci)])

        with self.beat("b13"):
            self.wipe(hd)
            nk = cell(0.8, BLUE, label="NK cell", size=28).move_to([-4.5, 0.4, 0])
            mk = T("CD56⁺ CD3⁻", 28, YELLOW).next_to(nk, UP, buff=0.25)
            t1 = cell(0.6, GREEN, label="MHC-I present", size=26).move_to([0.6, 1.3, 0])
            t2 = cell(0.6, PINK, label="MHC-I lost", size=26).move_to([0.6, -1.1, 0])
            r1 = T("inhibited: no kill", 28, GREEN).next_to(t1, RIGHT, buff=0.6)
            r2 = T("missing self → kill", 28, PINK).next_to(t2, RIGHT, buff=0.6)
            a1 = chalk_arrow(nk, t1)
            a2 = chalk_arrow(nk, t2)
            adcc = T("CD16 binds IgG → ADCC", 30, YELLOW).move_to([0, -3.0, 0])
            self.src("Abbas p.82, 84, 85")
            self.steps([FadeIn(nk), Write(mk)], [GrowArrow(a1), FadeIn(t1), Write(r1)],
                       [GrowArrow(a2), FadeIn(t2), Write(r2)], Write(adcc))

        with self.beat("b14"):
            self.wipe(hd)
            nk = cell(0.9, BLUE, label="NK cell", size=28).move_to([-4, 0.3, 0])
            x = strike(nk[0])
            gn = T("GATA2 · CD16 defects", 30, YELLOW).next_to(nk, DOWN, buff=0.7)
            d = VGroup(T("severe herpesvirus", 32, PINK), T("+ papillomavirus infections", 32, PINK)) \
                .arrange(DOWN, aligned_edge=LEFT).move_to([2.4, 0.3, 0])
            self.src("Abbas p.488")
            self.steps([FadeIn(nk), Write(gn)], Create(x), [GrowArrow(chalk_arrow(nk, d, PINK)), Write(d)])

        with self.beat("b15"):
            self.wipe(hd)
            tr = tag("TRAP").to_corner(UL, buff=0.5).shift(DOWN * 0.9)
            mc = cell(1.0, BLUE, label="mast cell", size=28).move_to([-4.2, -0.2, 0])
            ok = VGroup(T("tryptase", 36, YELLOW), tick()).arrange(RIGHT, buff=0.3).move_to([0.3, 1.5, 0])
            hi = T("histamine", 34, GREY).next_to(ok, RIGHT, buff=1.0)
            ma = T("= marker of mast cell activation", 26, CHALK).next_to(VGroup(ok, hi), DOWN, buff=0.3)
            ni = T("Without IgE:", 30, CHALK).move_to([0.0, -1.0, 0])
            nl = T("C3a · C5a · MRGPRX2", 32, ORANGE).next_to(ni, DOWN, buff=0.3)
            self.src("Abbas p.470, 471")
            self.steps([FadeIn(tr), FadeIn(mc)], [Write(ok), Write(hi), Create(strike_through(hi)), FadeIn(ma)],
                       [Write(ni), Write(nl), GrowArrow(chalk_arrow(nl.get_left() + LEFT * 0.2, mc, ORANGE))])

        with self.beat("b16"):
            self.wipe(hd)
            tr = tag("TRAP").to_corner(UL, buff=0.5).shift(DOWN * 0.9)
            eo = cell(1.0, PINK, label="eosinophil", size=28).move_to([-4.2, -0.3, 0])
            l1 = T("FcεRI: very low, no signalling chain", 30, CHALK).move_to([1.5, 1.4, 0])
            l2 = T("IL-5 = key cytokine", 30, YELLOW).move_to([1.5, 0.1, 0])
            cr = RegularPolygon(6, color=YELLOW, stroke_width=3).scale(0.3).stretch(2.2, 0)
            l3 = VGroup(T("galectin-10 →", 30, CHALK), cr, T("Charcot-Leyden", 30, YELLOW)).arrange(RIGHT, buff=0.25)
            l3.move_to([1.5, -1.3, 0])
            self.src("Abbas p.473")
            self.steps([FadeIn(tr), FadeIn(eo), Write(l1)], Write(l2), [Write(l3[0]), Create(cr), Write(l3[2])])

        # ================= M3 =================
        with self.beat("b17"):
            self.clear_board()
            hd = self.header("M3 · Sensing")
            c = Circle(2.0, color=BLUE, stroke_width=4).set_fill(BLUE, 0.06).move_to([-2.8, -0.5, 0])
            sticks = VGroup(*[Line(c.point_at_angle(a), c.point_at_angle(a) + 0.5 * np.array([np.cos(a), np.sin(a), 0]),
                                   color=YELLOW, stroke_width=5) for a in np.linspace(0.3, 2.8, 6)])
            endo = Circle(0.6, color=GREEN, stroke_width=3).set_fill(GREEN, 0.12).move_to(c.get_center() + DOWN * 0.4)
            el = T("endosome", 24, GREEN).next_to(endo, DOWN, buff=0.1)
            es = VGroup(*[Line(endo.get_center(), endo.point_at_angle(a), color=PINK, stroke_width=4)
                          for a in np.linspace(0.5, 2.6, 4)])
            s1 = VGroup(T("Surface: TLR1, 2, 4, 5, 6", 30, YELLOW), T("→ microbial walls", 30, CHALK)) \
                .arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.2, 1.0, 0])
            s2 = VGroup(T("Endosome: TLR3, 7, 8, 9", 30, PINK), T("→ nucleic acids", 30, CHALK)) \
                .arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.2, -1.3, 0]).align_to(s1, LEFT)
            lp = T("Location predicts the ligand", 32, YELLOW).move_to([0, -3.3, 0])
            self.src("Abbas p.69")
            self.steps([FadeIn(hd), Create(c)], Write(lp), [Create(sticks), Write(s1)],
                       [Create(endo), FadeIn(el), Create(es), Write(s2)])

        with self.beat("b18"):
            self.wipe(hd)
            ligs = ["LPS", "flagellin", "dsRNA", "CpG DNA"]
            tlrs = ["TLR4 (+ MD2, CD14)", "TLR5", "TLR3", "TLR9"]
            L = VGroup(*[T(x, 32, PINK) for x in ligs]).arrange(DOWN, buff=0.75, aligned_edge=RIGHT).move_to([-3.0, -0.4, 0])
            R = VGroup(*[label_box(x, BLUE, size=30) for x in tlrs]).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
            R.move_to([2.6, -0.4, 0])
            for l, r in zip(L, R):
                l.match_y(r)
            self.play(LaggedStart(*[Write(x) for x in L], lag_ratio=0.15), run_time=self.fit(1.0))
            self.src("Abbas p.67, 69")
            self.steps(*[[GrowArrow(chalk_arrow(l, r)), FadeIn(r, shift=LEFT * 0.2)] for l, r in zip(L, R)])

        with self.beat("b19"):
            self.wipe(hd)
            tr = tag("CLASSIC TRAP").to_corner(UL, buff=0.5).shift(DOWN * 0.9)
            cols = [-1.2, 1.2, 3.6]
            hdrs = VGroup(*[T(x, 32, YELLOW).move_to([cx, 1.4, 0]) for x, cx in zip(["", "MyD88", "TRIF"], cols)])
            data = [("TLR3", False, True), ("TLR4", True, True), ("other TLRs", True, False)]
            rws = []
            for i, (n, a, b) in enumerate(data):
                y = 0.4 - i * 1.0
                rws.append(VGroup(T(n, 32, BLUE).move_to([cols[0], y, 0]),
                                  (tick() if a else cross()).move_to([cols[1], y, 0]),
                                  (tick() if b else cross()).move_to([cols[2], y, 0])))
            self.src("Abbas p.69")
            self.steps([FadeIn(tr), Write(hdrs)], FadeIn(rws[0]), Circumscribe(rws[0], color=PINK),
                       FadeIn(rws[1]), FadeIn(rws[2]))

        with self.beat("b20"):
            self.wipe(hd)
            c1 = card("MyD88 / IRAK4 deficiency", ["early invasive pneumococcus", "no fever: a 'cold' infection"],
                      PINK, 28).move_to([-3.3, -0.4, 0])
            c2 = card("TLR3 · UNC93B · TRIF defect", ["herpes simplex encephalitis", "other viral defence normal"],
                      PINK, 28).move_to([3.3, -0.4, 0])
            self.src("Abbas p.489; Janeway p.535")
            self.steps(FadeIn(c1, shift=UP * 0.3), FadeIn(c2, shift=UP * 0.3))

        with self.beat("b21"):
            self.wipe(hd)
            trig = T("urate crystals · ATP · potassium efflux", 28, CHALK).move_to([-3.0, 2.0, 0])
            n3 = label_box("NLRP3", BLUE, size=32).move_to([-3.6, 0.6, 0])
            c1 = label_box("caspase-1", YELLOW, size=32).move_to([0.6, 0.6, 0])
            ck = T("pro-IL-1β, IL-18 → active", 28, YELLOW).move_to([4.2, 1.5, 0])
            gd = T("gasdermin D pores", 28, CHALK).move_to([4.2, 0.0, 0])
            py = T("pyroptosis", 34, PINK).move_to([4.2, -1.4, 0])
            who = VGroup(VGroup(T("macrophages", 28, BLUE), tick()).arrange(RIGHT, buff=0.2),
                         VGroup(T("DCs", 28, BLUE), tick()).arrange(RIGHT, buff=0.2),
                         VGroup(T("neutrophils", 28, BLUE), cross()).arrange(RIGHT, buff=0.2)).arrange(RIGHT, buff=0.8)
            who.move_to([0.8, -2.7, 0])
            self.src("Abbas p.72, 74")
            self.steps([Write(trig), FadeIn(n3), GrowArrow(chalk_arrow(trig, n3))],
                       [GrowArrow(chalk_arrow(n3, c1)), FadeIn(c1), GrowArrow(chalk_arrow(c1, ck)), Write(ck)],
                       [GrowArrow(chalk_arrow(c1, gd)), Write(gd), GrowArrow(chalk_arrow(gd, py, PINK)), Write(py)],
                       FadeIn(who, shift=UP * 0.2))

        with self.beat("b22"):
            self.wipe(hd)
            n3 = label_box("NLRP3 gain of function", PINK, size=30).move_to([-3.6, 1.3, 0])
            cp = T("CAPS", 40, PINK).move_to([1.2, 1.3, 0])
            f = card("FCAS", ["cold-induced fever", "urticarial rash"], PINK, 26).move_to([-0.6, -1.0, 0])
            m = card("Muckle-Wells", ["+ deafness"], PINK, 26).next_to(f, RIGHT, buff=0.6, aligned_edge=UP)
            il = label_box("IL-1 antagonists work (Abbas)", ORANGE, size=26).move_to([-1.0, -2.75, 0])
            self.src("Abbas p.74, 75; Janeway p.537")
            self.steps([FadeIn(n3), GrowArrow(chalk_arrow(n3, cp)), Write(cp)], [FadeIn(f), FadeIn(m)], FadeIn(il))

        with self.beat("b23"):
            self.wipe(hd)
            tr = tag("TRAP").to_corner(UL, buff=0.5).shift(DOWN * 0.9)
            n = label_box("NOD2", BLUE, size=36).move_to([0, 1.0, 0])
            a = VGroup(T("weak variants", 30, CHALK), T("→ Crohn's disease", 30, PINK)).arrange(DOWN, buff=0.2).move_to([-3.2, -1.3, 0])
            b = VGroup(T("gain of function", 30, CHALK), T("→ Blau syndrome", 30, PINK)).arrange(DOWN, buff=0.2).move_to([3.2, -1.3, 0])
            self.src("Abbas p.72")
            self.steps([FadeIn(tr), FadeIn(n)], [GrowArrow(chalk_arrow(n, a)), Write(a)],
                       [GrowArrow(chalk_arrow(n, b)), Write(b)])

        # ================= M4 =================
        with self.beat("b24"):
            self.clear_board()
            hd = self.header("M4 · Phagocytes")
            top = Line([-6.3, 0.2, 0], [6.3, 0.2, 0], color=PINK, stroke_width=4)
            bot = Line([-6.3, -1.4, 0], [6.3, -1.4, 0], color=PINK, stroke_width=4)
            names = ["1 rolling\n(sialyl Lewis X)", "2 integrin\nactivation", "3 firm arrest", "4 transmigration"]
            xs = [-4.6, -1.5, 1.6, 4.6]
            labs = VGroup(*[Text(n, font=FONT, font_size=26, color=YELLOW, line_spacing=0.8).move_to([x, 1.5, 0])
                            for n, x in zip(names, xs)])
            wbc = Circle(0.35, color=BLUE, stroke_width=4).set_fill(BLUE, 0.3).move_to([-6.0, -0.3, 0])

            self.play(FadeIn(hd), Create(top), Create(bot), FadeIn(wbc), run_time=self.fit(0.8))
            self.src("Abbas p.45, 49")
            self.steps([Write(labs[0]), wbc.animate.move_to([xs[0], -0.3, 0])],
                       [Write(labs[1]), wbc.animate.move_to([xs[1], -0.3, 0])],
                       [Write(labs[2]), wbc.animate.move_to([xs[2], 0.15 - 0.35 + 0.0, 0])],
                       [Write(labs[3]), wbc.animate.move_to([xs[3], -2.2, 0])])
            v_lab = labs

        with self.beat("b25"):
            self.play(*[FadeOut(m) for m in [top, bot, wbc]], v_lab.animate.shift(UP * 0.4), run_time=self.fit(0.6))
            c2 = card("LAD-2", ["no sialyl Lewis X", "Bombay blood group"], PINK, 24).move_to([-4.6, -1.0, 0])
            c3 = card("LAD-3", ["KINDLIN-3", "bleeding, normal", "platelets"], PINK, 24).move_to([-1.4, -1.0, 0])
            c1 = card("LAD-1 (CD18)", ["leukocytosis", "no pus", "poor wound healing"], PINK, 24).move_to([2.0, -1.0, 0])
            self.steps([FadeIn(c1, shift=UP * 0.3), GrowArrow(chalk_arrow(v_lab[2], c1, PINK))],
                       [FadeIn(c2, shift=UP * 0.3), GrowArrow(chalk_arrow(v_lab[0], c2, PINK))],
                       [FadeIn(c3, shift=UP * 0.3), GrowArrow(chalk_arrow(v_lab[1], c3, PINK))])
            self.src("Abbas p.488")

        with self.beat("b26"):
            self.wipe(hd)
            tr = tag("TRAP").to_corner(UL, buff=0.5).shift(DOWN * 0.9)
            bl = RoundedRectangle(corner_radius=0.2, width=4.4, height=2.6, color=PINK, stroke_width=3).move_to([-3.2, 0.2, 0])
            ts = RoundedRectangle(corner_radius=0.2, width=4.4, height=2.6, color=GREY, stroke_width=3).move_to([3.2, 0.2, 0])
            rng = np.random.default_rng(3)
            dots = VGroup(*[Dot(bl.get_center() + [rng.uniform(-1.9, 1.9), rng.uniform(-1.0, 1.0), 0], 0.09, color=BLUE)
                            for _ in range(40)])
            bt = T("blood: leukocytosis", 30, BLUE).next_to(bl, UP, buff=0.2)
            tt = T("tissue: no pus", 30, PINK).next_to(ts, UP, buff=0.2)
            scn = T("≠ severe congenital neutropenia: < 0.5 × 10⁹/L", 28, YELLOW).move_to([0, -2.6, 0])
            self.src("Abbas p.488; Janeway p.533")
            self.steps([FadeIn(tr), Create(bl), Write(bt), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.03)],
                       [Create(ts), Write(tt)], Write(scn))

        with self.beat("b27"):
            self.wipe(hd)
            ch = VGroup(*[T(x, 32, c) for x, c in [("O₂", CHALK), ("superoxide", YELLOW), ("H₂O₂", YELLOW),
                                                 ("hypohalous acid", PINK)]]).arrange(RIGHT, buff=1.3).move_to(UP * 0.6)
            ens = ["NADPH oxidase", "", "MPO"]
            arrs = [chalk_arrow(a, b) for a, b in zip(ch, ch[1:])]
            el = [T(e, 26, GREEN).next_to(ar, UP, buff=0.2) for e, ar in zip(ens, arrs)]
            self.add(ch[0])
            self.src("Abbas p.96")
            self.steps([GrowArrow(arrs[0]), FadeIn(el[0]), Write(ch[1])], [GrowArrow(arrs[1]), Write(ch[2])],
                       [GrowArrow(arrs[2]), FadeIn(el[2]), Write(ch[3])])
            burst = VGroup(ch, *arrs, el[0], el[2])

        with self.beat("b28"):
            self.play(burst.animate.scale(0.85).to_edge(UP, buff=1.55), run_time=self.fit(0.7))
            x1 = cross(size=30).next_to(el[0], LEFT, buff=0.12)
            cg = card("CGD", ["~2/3 X-linked gp91", "catalase⁺ Staphylococcus", "granulomas",
                              "Aspergillus: leading cause of death"], PINK, 26).move_to([-2.6, -1.3, 0])
            x2 = cross(size=30).next_to(el[2], RIGHT, buff=0.12)
            mp = card("MPO deficiency", ["CGD-like, milder"], PINK, 26).move_to([3.6, -0.8, 0])
            self.src("Abbas p.486, 487; Janeway p.536")
            self.steps([FadeIn(x1), FadeIn(cg[0]), FadeIn(cg[1][0])], FadeIn(cg[1][1][:2]), FadeIn(cg[1][1][2:]),
                       [FadeIn(x2), FadeIn(mp)])

        with self.beat("b29"):
            self.wipe(hd)
            c = card("Chédiak-Higashi syndrome", ["gene: LYST", "partial albinism, silver hair",
                                                  "giant lysosomes", "weak NK cells"], PINK, 30).move_to([0.8, -0.3, 0])
            ph = cell(0.9, BLUE).move_to([-4.8, -0.3, 0])
            gl = VGroup(*[Circle(0.2, color=YELLOW, stroke_width=3).set_fill(YELLOW, 0.4).move_to(ph.get_center() + v)
                          for v in [LEFT * 0.35 + DOWN * 0.3, RIGHT * 0.3 + DOWN * 0.35]])
            self.src("Abbas p.488; Janeway p.540")
            self.steps([FadeIn(c[0]), FadeIn(c[1][0])], [FadeIn(c[1][1][:2]), FadeIn(ph), GrowFromCenter(gl)],
                       FadeIn(c[1][1][2:]))

        with self.beat("b30"):
            self.wipe(hd)
            m = cell(0.7, BLUE, label="macrophage", size=26).move_to([-3.2, 0.0, 0])
            t = cell(0.7, BLUE, label="NK / T cell", size=26).move_to([3.2, 0.0, 0])
            a1 = CurvedArrow(m.get_top() + UP * 0.1, t.get_top() + UP * 0.1, angle=-PI / 4, color=YELLOW)
            a2 = CurvedArrow(t[0].get_bottom() + DOWN * 0.5, m[0].get_bottom() + DOWN * 0.5, angle=-PI / 4, color=YELLOW)
            l1 = T("IL-12", 30, YELLOW).next_to(a1, UP, buff=0.1)
            l2 = T("IFN-γ", 30, YELLOW).next_to(a2, DOWN, buff=0.1)
            ms = T("broken → MSMD: BCG, Salmonella", 32, PINK).move_to([0, -3.1, 0])
            self.src("Abbas p.93, 498")
            self.steps([FadeIn(m), FadeIn(t), Create(a1), Write(l1), Create(a2), Write(l2)],
                       [FadeIn(cross(size=36).next_to(l2, RIGHT, buff=0.2)), Write(ms)])

        # ================= M5 =================
        with self.beat("b31"):
            self.clear_board()
            hd = self.header("M5 · Complement")
            pw = VGroup(*[label_box(x, BLUE, size=28) for x in ["classical", "lectin", "alternative"]]) \
                .arrange(DOWN, buff=0.45).move_to([-5.0, 0.0, 0])
            cv1 = label_box("C4b2a", YELLOW, size=32).move_to([-1.6, 0.6, 0])
            cv2 = label_box("C3bBb", YELLOW, size=32).move_to([-1.6, -1.2, 0])
            c3 = label_box("C3", GREEN, size=36).move_to([1.4, -0.3, 0])
            p1 = T("C3a", 30, PINK).move_to([4.3, 0.6, 0])
            p2 = T("C3b on surface", 30, GREEN).move_to([4.6, -1.2, 0])
            cl = T("C3 convertases", 24, GREY).next_to(VGroup(cv1, cv2), UP, buff=1.0)
            self.src("Abbas p.301, 305; Janeway p.54")
            self.steps([FadeIn(hd), LaggedStart(*[FadeIn(p) for p in pw])],
                       [GrowArrow(chalk_arrow(pw[0], cv1)), GrowArrow(chalk_arrow(pw[1], cv1)), FadeIn(cv1), FadeIn(cl)],
                       [GrowArrow(chalk_arrow(pw[2], cv2)), FadeIn(cv2)],
                       [GrowArrow(chalk_arrow(cv1, c3)), GrowArrow(chalk_arrow(cv2, c3)), FadeIn(c3),
                        GrowArrow(chalk_arrow(c3, p1)), Write(p1), GrowArrow(chalk_arrow(c3, p2)), Write(p2)])

        with self.beat("b32"):
            self.wipe(hd)
            tr = tag("TRAP").to_corner(UL, buff=0.5).shift(DOWN * 0.9)
            c2 = label_box("C2", BLUE, size=36).move_to([-3.5, 1.0, 0])
            big = label_box("C2a  (larger, stays bound)", GREEN, size=30).move_to([2.0, 1.6, 0])
            sm = T("C2b  (small, released)", 26, GREY).move_to([2.0, 0.4, 0])
            fd = T("factor D: circulates already active", 30, YELLOW).move_to([0, -1.3, 0])
            pr = T("properdin: stabilizes C3bBb", 30, GREEN).move_to([0, -2.4, 0])
            self.src("Abbas p.302, 305; Janeway p.61")
            self.steps([FadeIn(tr), FadeIn(c2), GrowArrow(chalk_arrow(c2, big)), FadeIn(big),
                        GrowArrow(chalk_arrow(c2, sm)), FadeIn(sm)], Write(fd), Write(pr))

        with self.beat("b33"):
            self.wipe(hd)
            top = T("Only antigen-bound antibody activates C1", 32, YELLOW).move_to(UP * 2.0)
            g4 = VGroup(T("IgG4", 36, GREY), cross()).arrange(RIGHT, buff=0.2)
            lad = VGroup(T("IgM", 40, GREEN), T(">", 40, CHALK), T("IgG1, IgG3", 36, GREEN), T(">", 40, CHALK),
                         g4).arrange(RIGHT, buff=0.5).move_to(DOWN * 0.2)
            nt = T("IgG4 does not activate complement", 28, PINK).next_to(lad, DOWN, buff=0.7)
            self.src("Abbas p.305")
            self.steps(Write(top), [Write(lad[0]), Write(lad[1]), Write(lad[2])], [Write(lad[3]), FadeIn(lad[4]), Write(nt)])

        with self.beat("b34"):
            self.wipe(hd)
            b5 = Rectangle(width=4.0, height=0.5, color=PINK, stroke_width=3).set_fill(PINK, 0.5)
            b3 = Rectangle(width=0.2, height=0.5, color=PINK, stroke_width=3).set_fill(PINK, 0.5)
            g5 = VGroup(T("C5a", 30, PINK), b5).arrange(RIGHT, buff=0.3)
            g3 = VGroup(T("C3a", 30, PINK), b3).arrange(RIGHT, buff=0.3)
            bars = VGroup(g5, g3).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([-3.2, 1.2, 0])
            for g in (g3,):
                g[1].align_to(b5, LEFT)
            ne = T("C3a ~20× weaker · mast cells degranulate without IgE", 26, CHALK).next_to(bars, DOWN, buff=0.3).align_to(bars, LEFT)
            mem = Line([1.0, -1.6, 0], [6.2, -1.6, 0], color=BLUE, stroke_width=8)
            pore = VGroup(Line([3.3, -1.1, 0], [3.3, -2.1, 0], color=YELLOW, stroke_width=8),
                          Line([3.9, -1.1, 0], [3.9, -2.1, 0], color=YELLOW, stroke_width=8))
            gap = Line([3.4, -1.6, 0], [3.8, -1.6, 0], color=BOARD, stroke_width=10)
            wat = VGroup(*[Arrow([3.6, -0.3 - 0.0, 0], [3.6, -2.6, 0], color=BLUE, stroke_width=3, buff=0)])
            ml = T("MAC: water in → cell bursts", 28, YELLOW).move_to([-2.4, -1.6, 0])
            self.src("Abbas p.307, 314, 470")
            self.steps([FadeIn(g5[0]), GrowFromEdge(b5, LEFT), FadeIn(g3)], Write(ne),
                       [Create(mem), Create(gap), Create(pore), Write(ml)], GrowArrow(wat[0]))

        with self.beat("b35"):
            self.wipe(hd)
            regs = [("factor H", "alternative pathway only"), ("C4BP", "binds C4b"),
                    ("DAF (CD55)", "dissociates both C3 convertases"), ("CD59", "blocks C9 at C5b-8")]
            rs = VGroup(*[VGroup(label_box(a, GREEN, size=30), T(b, 30, CHALK)) for a, b in regs])
            for i, r in enumerate(rs):
                r[0].move_to([-3.8, 1.6 - i * 1.25, 0])
                r[1].next_to(r[0], RIGHT, buff=1.4)
                r[1].align_to([-1.0, 0, 0], LEFT)
            self.src("Abbas p.310–312")
            self.steps(*[[FadeIn(r[0], shift=RIGHT * 0.3), GrowArrow(chalk_arrow(r[0].get_right(), r[1].get_left() + LEFT * 0.1)),
                          Write(r[1])] for r in rs])

        # ================= M6 =================
        with self.beat("b36"):
            self.clear_board()
            hd = self.header("M6 · Deficiencies")
            r1 = row("C1q · C2 · C4", "SLE in > 50%", size=32).move_to([-0.5, 1.6, 0])
            n1 = T("C2 deficiency: most common", 26, YELLOW).next_to(r1, DOWN, buff=0.2).align_to(r1, LEFT)
            r2 = row("C3 · factor I", "pyogenic infections", size=32).move_to([-0.5, -0.4, 0]).align_to(r1, LEFT)
            self.src("Abbas p.315")
            self.steps([FadeIn(hd), Write(r1)], FadeIn(n1), Write(r2))
            m6a = VGroup(r1, n1, r2)

        with self.beat("b37"):
            self.play(m6a.animate.scale(0.85).to_edge(UP, buff=1.2).to_edge(LEFT, buff=0.8), run_time=self.fit(0.6))
            r3 = row("C5–C9 · properdin · factor D", "Neisseria", size=32).move_to([0, -0.8, 0]).align_to(m6a, LEFT)
            n3 = T("properdin deficiency: X-linked", 26, YELLOW).next_to(r3, DOWN, buff=0.2).align_to(r3, LEFT)
            r4 = row("MBL", "mild", size=32, rc=GREEN).next_to(n3, DOWN, buff=0.6).align_to(r3, LEFT)
            self.src("Abbas p.315; Janeway p.532, 533")
            self.steps(Write(r3), FadeIn(n3), Write(r4))

        with self.beat("b38"):
            self.wipe(hd)
            a = row("factor H · MCP", "atypical HUS", size=32).move_to([0, 1.6, 0])
            p = row("PNH: no CD59, no DAF", "haemolysis", size=32).move_to([0, 0.0, 0])
            st = T("SOMATIC PIG-A — not inherited", 34, PINK)
            sb = chalk_box(st, PINK, buff=0.2)
            stamp = VGroup(sb, st).rotate(4 * DEGREES).move_to([0, -1.9, 0])
            self.src("Abbas p.312, 315")
            self.steps(Write(a), Write(p), [FadeIn(stamp, scale=1.4)])

        with self.beat("b39"):
            self.wipe(hd)
            h2 = T("Hereditary angioedema (HAE)", 36, YELLOW).move_to([0, 2.2, 0])
            ch = VGroup(label_box("C1 inhibitor ↓", PINK, size=30), label_box("bradykinin ↑", YELLOW, size=30),
                        label_box("swelling", PINK, size=30)).arrange(RIGHT, buff=1.0).move_to(UP * 0.8)
            ad = T("autosomal dominant", 26, GREY).next_to(ch[0], DOWN, buff=0.2)
            cl = bullet_list(["abdominal attacks", "no wheals", "no response to antihistamines"], 30).move_to([0, -1.8, 0])
            self.src("Abbas p.311; HAE-GL p.6")
            self.steps([Write(h2)], [FadeIn(ch[0]), FadeIn(ad), GrowArrow(chalk_arrow(ch[0], ch[1])), FadeIn(ch[1]),
                                     GrowArrow(chalk_arrow(ch[1], ch[2])), FadeIn(ch[2])],
                       LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in cl], lag_ratio=0.4))

        with self.beat("b40"):
            self.wipe(hd)
            cx = [-4.6, -1.6, 0.9, 2.9, 5.0]
            heads = ["", "C1-INH\nfunction", "C1-INH\nprotein", "C4", "C1q"]
            H = VGroup(*[Text(h, font=FONT, font_size=26, color=YELLOW, line_spacing=0.8).move_to([x, 2.0, 0])
                         for h, x in zip(heads, cx)])
            line = Line([-6.2, 1.35, 0], [6.2, 1.35, 0], color=CHALK, stroke_width=2)
            data = [("HAE type 1", "↓", "↓", "↓", "normal"), ("HAE type 2", "↓", "normal / ↑", "↓", "normal"),
                    ("acquired (AAE)", "↓", "↓", "↓", "↓ in 75%"), ("ACE inhibitor", "normal", "normal", "", "")]
            R = []
            for i, rr in enumerate(data):
                y = 0.8 - i * 0.95
                g = VGroup(*[T(v, 28, BLUE if j == 0 else (PINK if "↓" in v else GREEN)).move_to([x, y, 0])
                             for j, (v, x) in enumerate(zip(rr, cx)) if v])
                R.append(g)
            gl = T("2017 guideline", 22, GREY).move_to([-4.6, 2.0, 0])
            self.src("HAE-GL p.5, 6")
            self.steps([Write(H[:4]), Create(line), FadeIn(gl)], FadeIn(R[0][:3]), FadeIn(R[1][:3]),
                       [FadeIn(R[0][3]), FadeIn(R[1][3])])
            lab_tbl = VGroup(H, line, gl, *R[:2])

        with self.beat("b41"):
            self.src("HAE-GL p.6, 7")
            ex = T("lymphoma or MGUS, later onset", 26, GREY).move_to([0, -2.9, 0])
            self.steps([FadeIn(R[2][:4]), Write(H[4])], [FadeIn(R[2][4]), FadeIn(R[0][4]), FadeIn(R[1][4]), FadeIn(ex)],
                       FadeIn(R[3]))

        with self.beat("b42"):
            self.wipe(hd)
            tr = tag("HAE TRAPS").to_corner(UL, buff=0.5).shift(DOWN * 0.9)
            cs = [card("C3, CH50", ["normal in HAE"], PINK, 28), card("Normal C1-INH", ["does not exclude HAE"], PINK, 28),
                  card("C4 < 12 months", ["not useful"], PINK, 28), card("Wheals", ["do not exclude HAE"], PINK, 28)]
            grid = VGroup(*cs).arrange_in_grid(2, 2, buff=(0.8, 0.5)).move_to(DOWN * 0.5)
            self.src("HAE-GL p.6, 7, 11")
            self.steps(FadeIn(tr), *[FadeIn(c, shift=UP * 0.3) for c in cs])

        with self.beat("b43"):
            self.wipe(hd)
            bn = label_box("2017 guideline — check the current guideline", GREY, size=26).move_to(UP * 2.2)
            at = T("Attack: treat early", 34, YELLOW).move_to([-3.2, 0.9, 0])
            dr = VGroup(*[label_box(x, ORANGE, size=30) for x in ["C1 inhibitor", "ecallantide", "icatibant"]]) \
                .arrange(RIGHT, buff=0.5).move_to([0, -0.4, 0])
            no = VGroup(T("tranexamic acid", 30, GREY), T("androgens", 30, GREY)).arrange(RIGHT, buff=1.2).move_to([0, -2.2, 0])
            xs = VGroup(*[strike_through(n) for n in no])
            self.src("HAE-GL p.7, 8")
            self.steps(FadeIn(bn), [Write(at), LaggedStart(*[FadeIn(d, shift=UP * 0.2) for d in dr], lag_ratio=0.3)],
                       [Write(no), Create(xs)])

        with self.beat("b44"):
            self.wipe(hd, bn)
            lt = T("Long-term prophylaxis", 32, YELLOW).move_to([-3.4, 1.1, 0])
            l1 = label_box("1st line: C1 inhibitor", ORANGE, size=28).next_to(lt, DOWN, buff=0.4).align_to(lt, LEFT)
            l2 = label_box("2nd line: androgens", ORANGE, size=28).next_to(l1, DOWN, buff=0.3).align_to(lt, LEFT)
            kit = VGroup(*[RoundedRectangle(corner_radius=0.1, width=0.8, height=0.55, color=ORANGE, stroke_width=3)
                           .set_fill(ORANGE, 0.2) for _ in range(2)]).arrange(RIGHT, buff=0.25)
            kl = T("carry doses for 2 attacks", 28, CHALK)
            kg = VGroup(kit, kl).arrange(DOWN, buff=0.25).move_to([3.4, 0.6, 0])
            ace = T("ACE inhibitors", 32, PINK).move_to([3.4, -1.6, 0])
            self.src("HAE-GL p.8, 9–10, 14")
            self.steps([Write(lt), FadeIn(l1), FadeIn(l2)], [FadeIn(kit), Write(kl)], [Write(ace), Create(strike_through(ace))])

        # ================= master map D21 =================
        hdr, mrows = master_map()
        with self.beat("b45"):
            self.clear_board()
            ttl = T("Master map (D21)", 32, YELLOW).move_to([0, 3.62, 0])
            self.play(Write(ttl), FadeIn(hdr), run_time=self.fit(0.9))
            self.src("Abbas; Janeway; HAE-GL")
            self.steps(*[[FadeIn(r[0], shift=RIGHT * 0.2), FadeIn(r[1]), FadeIn(r[2], shift=LEFT * 0.2)]
                         for r in mrows[:3]])

        with self.beat("b46"):
            self.steps(*[[FadeIn(r[0], shift=RIGHT * 0.2), FadeIn(r[1]), FadeIn(r[2], shift=LEFT * 0.2)]
                         for r in mrows[3:7]])

        with self.beat("b47"):
            r = mrows[7]
            self.steps([FadeIn(r[0], shift=RIGHT * 0.2), FadeIn(r[1])], FadeIn(r[2], shift=LEFT * 0.2),
                       Circumscribe(VGroup(*mrows), color=YELLOW))

        # ================= recap =================
        with self.beat("b48"):
            self.clear_board()
            h = self.header("Five things to remember")
            items = ["Innate receptors: germline-encoded", "Location predicts the ligand",
                     "Lost function predicts disease", "HAE is bradykinin-mediated", "Innate immunity gives signal 2"]
            L = VGroup(*[VGroup(T(f"{i + 1}", 34, YELLOW), T(t, 34, CHALK)).arrange(RIGHT, buff=0.4)
                         for i, t in enumerate(items)]).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to(DOWN * 0.4)
            self.play(FadeIn(h), run_time=self.fit(0.6))
            self.steps(*[FadeIn(x, shift=RIGHT * 0.3) for x in L])

        with self.beat("b49"):
            self.clear_board(run_time=0.4)
            tr = tag("LAST TRAP", size=30).move_to(UP * 1.2)
            t = T("TLR3 is the only TLR without MyD88", 40, YELLOW).next_to(tr, DOWN, buff=0.5)
            self.play(FadeIn(tr), Write(t), run_time=self.fit(1.4))
            self.wait(min(2.0, self.remaining() * 0.3))
            hdr2, rows2 = master_map()
            ttl = T("Master map (D21) · good luck!", 32, YELLOW).move_to([0, 3.62, 0])
            self.play(FadeOut(tr), FadeOut(t), run_time=self.fit(0.5))
            self.play(Write(ttl), FadeIn(hdr2), LaggedStart(*[FadeIn(r) for r in rows2], lag_ratio=0.1),
                      run_time=self.fit(2.0))

from chalk import *


# ---------- local helpers (V3 only) ----------
def bx(text, color=BLUE, size=28):
    return label_box(text, color, size)


def arr(a, b, color=CHALK, **kw):
    return chalk_arrow(a, b, color=color, **kw)


def membrane(x0, x1, y, color=GREY):
    return VGroup(Line([x0, y + 0.09, 0], [x1, y + 0.09, 0], color=color, stroke_width=3),
                  Line([x0, y - 0.09, 0], [x1, y - 0.09, 0], color=color, stroke_width=3))


def tlr_icon(color=BLUE, stalk=0.9, tir=True, tir_color=YELLOW):
    """Cartoon TLR: U-shaped ectodomain, stalk, TIR box. Origin = membrane crossing."""
    u = Arc(radius=0.32, start_angle=PI, angle=PI, color=color, stroke_width=6)
    u.move_to([0, stalk / 2 + 0.16, 0])
    s = Line([0, stalk / 2, 0], [0, -stalk / 2, 0], color=color, stroke_width=6)
    g = VGroup(u, s)
    if tir:
        t = RoundedRectangle(corner_radius=0.06, width=0.5, height=0.28, color=tir_color,
                             stroke_width=3).set_fill(tir_color, 0.35).move_to([0, -stalk / 2 - 0.14, 0])
        g.add(t)
    return g


def row(left, right, y, lc=PINK, rc=BLUE, size=30, mid=0.0, gap=0.7):
    """Ligand -> receptor row: left text right-aligned to mid-gap, right box left-aligned to mid+gap."""
    l = T(left, size, lc)
    l.move_to([mid - gap - l.width / 2, y, 0])
    r = bx(right, rc, size)
    r.move_to([mid + gap + r.width / 2, y, 0])
    a = Arrow([mid - gap + 0.1, y, 0], [mid + gap - 0.1, y, 0], buff=0, color=CHALK,
              stroke_width=4, tip_length=0.2)
    return VGroup(l, a, r)


def stack(items, size=26, color=CHALK, buff=0.22, aligned=LEFT):
    return VGroup(*[T(i, size, color) if isinstance(i, str) else i for i in items]).arrange(
        DOWN, buff=buff, aligned_edge=aligned)


class V3(ChalkScene):
    VIDEO_ID = "V3"

    # wait until the narrator reaches `cue` (text position -> fraction of beat audio)
    def cue(self, phrase, lead=0.4, nth=0):
        text = next(b["text"] for b in self.script["beats"] if b["id"] == self.used[-1])
        i = -1
        for _ in range(nth + 1):
            i = text.find(phrase, i + 1)
        if i < 0:
            raise ValueError(f"cue {phrase!r} not in {self.used[-1]}")
        target = i / len(text) * self.bd - lead
        if target - self.elapsed() > 0.05:
            self.wait(target - self.elapsed())

    def tag(self, text):
        old = getattr(self, "_tag", None)
        if old is not None and old in self.mobjects:
            self.remove(old)
        t = self.source_tag(text)
        self.play(FadeIn(t), run_time=0.3)
        self._tag = t
        return t

    def construct(self):
        # ---------------- b01 hook ----------------
        with self.beat("b01"):
            t = self.title_card("How cells sense danger", "Pattern recognition receptors & signalling")
            self.play(Write(t), run_time=self.fit(2.5))
            self.cue("For the exam")
            self.play(t.animate.shift(UP * 1.2), run_time=0.6)
            qs = VGroup(*[bx(s, c, 30) for s, c in
                          [("What does it see?", PINK), ("Where does it sit?", BLUE), ("Which signal?", YELLOW)]]
                        ).arrange(RIGHT, buff=0.5).move_to(DOWN * 1.6)
            self.cue("what it sees")
            self.play(FadeIn(qs[0], shift=UP * 0.3), run_time=self.fit(0.7))
            self.cue("where it sits")
            self.play(FadeIn(qs[1], shift=UP * 0.3), run_time=self.fit(0.7))
            self.cue("what signal")
            self.play(FadeIn(qs[2], shift=UP * 0.3), run_time=self.fit(0.7))

        # ---------------- b02 PAMPs ----------------
        with self.beat("b02"):
            self.clear_board()
            h = self.header("PAMPs: patterns that microbes share")
            self.play(Write(h), run_time=self.fit(1.2))
            bac = RoundedRectangle(corner_radius=0.6, width=3.0, height=1.3, color=PINK, stroke_width=5) \
                .set_fill(PINK, 0.12).move_to([-3.4, 1.0, 0])
            bl = T("bacterium", 26, PINK).next_to(bac, UP, buff=0.15)
            vir = VGroup(Circle(0.6, color=PINK, stroke_width=5).set_fill(PINK, 0.12),
                         *[Line(ORIGIN, RIGHT * 0.25, color=PINK, stroke_width=4)
                           .shift(RIGHT * 0.62).rotate(a, about_point=ORIGIN) for a in np.linspace(0, TAU, 9)[:-1]]
                         ).move_to([3.4, 1.0, 0])
            vl = T("virus", 26, PINK).next_to(vir, UP, buff=0.15)
            self.play(Create(bac), FadeIn(bl), run_time=self.fit(1))
            self.play(Create(vir), FadeIn(vl), run_time=self.fit(1))
            self.cue("Typical PAMPs")
            bp = bullet_list(["LPS", "lipoteichoic acid", "unmethylated CpG DNA"], size=30).next_to(bac, DOWN, buff=0.5)
            vp = bullet_list(["double-stranded RNA"], size=30).next_to(vir, DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in bp], lag_ratio=0.5), run_time=self.fit(2.5))
            self.cue("viral double")
            self.play(FadeIn(vp, shift=RIGHT * 0.2), run_time=self.fit(0.8))
            self.tag("Abbas p.63")

        # ---------------- b03 DAMPs ----------------
        with self.beat("b03"):
            self.clear_board()
            h = self.header("DAMPs: danger from damaged self")
            self.play(Write(h), run_time=self.fit(1.0))
            c = cell(1.4, BLUE, label="damaged host cell", size=26).move_to([-3.6, 0.3, 0])
            self.play(FadeIn(c), run_time=self.fit(0.8))
            crack = VMobject(color=PINK, stroke_width=5).set_points_as_corners(
                [c[0].get_right() + LEFT * 0.1 + UP * 0.6, c[0].get_right() + LEFT * 0.5 + UP * 0.2,
                 c[0].get_right() + LEFT * 0.15 + DOWN * 0.1, c[0].get_right() + LEFT * 0.55 + DOWN * 0.5])
            self.play(Create(crack), c[0].animate.set_stroke(PINK), run_time=self.fit(0.8))
            self.cue("Examples")
            items = ["heat shock proteins", "urate crystals", "extracellular ATP", "HMGB1"]
            dl = bullet_list(items, size=30, color=PINK).move_to([2.6, 0.6, 0])
            for r in dl:
                self.play(FadeIn(r, shift=RIGHT * 0.6), run_time=self.fit(0.6))
            self.cue("sterile")
            st = Tm('Sterile injury: <span foreground="#F2A2B8">burns · trauma · ischaemia</span>', 30) \
                .move_to([0, -2.6, 0])
            self.play(Write(st), run_time=self.fit(1.5))
            self.tag("Abbas p.63–65")

        # ---------------- b04 PRR map ----------------
        with self.beat("b04"):
            self.clear_board()
            h = self.header("Where PRRs sit")
            self.play(Write(h), run_time=self.fit(1.0))
            body = Circle(2.6, color=BLUE, stroke_width=5).set_fill(BLUE, 0.06).move_to([-2.4, -0.55, 0])
            endo = Circle(0.75, color=BLUE, stroke_width=4).set_fill(BLUE, 0.15).move_to([-3.4, -1.5, 0])
            self.play(Create(body), run_time=self.fit(1.2))
            self.play(FadeIn(endo, scale=0.6), run_time=self.fit(0.6))
            labs = VGroup(T("cell surface", 30, BLUE), T("endosome", 30, BLUE), T("cytosol", 30, BLUE),
                          T("soluble PRRs", 30, GREEN))
            for i, l in enumerate(labs):
                l.move_to([2.3 + l.width / 2, [1.6, -0.9, 0.35, -2.15][i], 0])
            pts = [body.point_at_angle(PI / 5), endo.get_right(), np.array([-1.3, 0.6, 0]),
                   np.array([1.2, -3.0, 0])]
            sol = VGroup(*[Dot(p, radius=0.09, color=GREEN) for p in
                           [[0.9, -2.9, 0], [1.35, -3.25, 0], [1.6, -2.75, 0]]])
            arrows = [Arrow(l.get_left(), p, buff=0.12, color=GREY, stroke_width=3, tip_length=0.18)
                      for l, p in zip(labs, pts)]
            for key, i in (("cell surface", 0), ("endosomes", 1), ("cytosol", 2), ("Soluble", 3)):
                self.cue(key)
                anims = [Write(labs[i]), GrowArrow(arrows[i])]
                if i == 3:
                    anims.append(FadeIn(sol))
                self.play(*anims, run_time=self.fit(0.8))
            self.tag("Abbas p.64")
            self.map = VGroup(body, endo, labs, *arrows, sol)

        # ---------------- b05 analogy ----------------
        with self.beat("b05"):
            an = T("Analogy: smoke detectors", 28, YELLOW).move_to([-2.4, 2.35, 0])
            self.play(FadeIn(an, shift=DOWN * 0.2), run_time=self.fit(0.8))
            room = ["outside wall", "waste room", "living room"]
            labs = self.map[2]
            notes = VGroup(*[T(r, 24, YELLOW).next_to(labs[i], DOWN, buff=0.1, aligned_edge=LEFT)
                             for i, r in enumerate(room)])
            targets = [self.map[0], self.map[1], None]
            for i, key in enumerate(["outside wall", "waste room", "living room"]):
                self.cue(key)
                anims = [FadeIn(notes[i], shift=UP * 0.1), Indicate(labs[i], color=YELLOW)]
                if targets[i] is not None:
                    anims.append(Indicate(targets[i], color=YELLOW, scale_factor=1.05))
                self.play(*anims, run_time=self.fit(1.0))

        # ---------------- b06 TLR family ----------------
        with self.beat("b06"):
            self.clear_board()
            h = self.header("Toll-like receptors (TLRs)")
            self.play(Write(h), run_time=self.fit(1.0))
            mem = membrane(-6.2, 6.2, 0.0)
            out = T("outside", 24, GREY).move_to([-5.6, 0.45, 0])
            ins = T("inside", 24, GREY).move_to([-5.6, -0.45, 0])
            self.play(Create(mem), FadeIn(out), FadeIn(ins), run_time=self.fit(0.8))
            tl = tlr_icon(BLUE, 1.2).move_to([-3.0, 0.1, 0])
            tll = T("TLR", 30, BLUE).next_to(tl, UP, buff=0.15)
            self.play(Create(tl), Write(tll), run_time=self.fit(1.2))
            self.cue("Humans have ten")
            ten = T("10 in humans: TLR1 – TLR10", 30, YELLOW).move_to([-3.0, 2.2, 0])
            self.play(Write(ten), run_time=self.fit(1.2))
            self.cue("TIR domain")
            tir_lab = T("TIR domain", 28, YELLOW).next_to(tl[2], DOWN, buff=0.25)
            self.play(Indicate(tl[2], color=YELLOW, scale_factor=1.6), FadeIn(tir_lab), run_time=self.fit(1.0))
            self.cue("IL-1, IL-18")
            others = VGroup()
            for i, nm in enumerate(["IL-1R", "IL-18R", "IL-33R"]):
                r = tlr_icon(GREEN, 1.2).move_to([1.0 + i * 1.9, 0.1, 0])
                l = T(nm, 28, GREEN).next_to(r, UP, buff=0.15)
                others.add(VGroup(r, l))
            self.play(LaggedStart(*[FadeIn(o, shift=UP * 0.2) for o in others], lag_ratio=0.3), run_time=self.fit(1.5))
            share = T("same TIR domain", 28, YELLOW).move_to([2.9, -1.4, 0])
            self.play(*[Indicate(o[0][2], color=YELLOW, scale_factor=1.6) for o in others], Write(share),
                      run_time=self.fit(1.2))
            self.tag("Abbas p.65–67")

        # ---------------- b07 location ----------------
        with self.beat("b07"):
            self.clear_board()
            h = self.header("Location splits the TLRs")
            self.play(Write(h), run_time=self.fit(1.0))
            mem = membrane(-6.3, 6.3, 1.2)
            cyt = T("cell", 24, GREY).move_to([-5.8, 0.75, 0])
            self.play(Create(mem), FadeIn(cyt), run_time=self.fit(0.8))
            self.cue("TLR1, 2")
            surf = VGroup()
            for i, n in enumerate(["1", "2", "4", "5", "6"]):
                r = tlr_icon(BLUE, 0.7, tir=False).move_to([-5.0 + i * 1.05, 1.45, 0])
                surf.add(VGroup(r, T("TLR" + n, 24, BLUE).next_to(r, DOWN, buff=0.3)))
            self.play(LaggedStart(*[FadeIn(s, shift=DOWN * 0.2) for s in surf], lag_ratio=0.2), run_time=self.fit(1.5))
            self.cue("see bacterial")
            sl = T("bacterial & fungal PAMPs", 28, PINK).move_to([-2.9, 2.45, 0])
            self.play(FadeIn(sl, shift=DOWN * 0.2), run_time=self.fit(0.8))
            self.cue("TLR3, 7")
            endo = Circle(1.55, color=BLUE, stroke_width=4).set_fill(BLUE, 0.1).move_to([3.4, -1.2, 0])
            el = T("endosome", 26, BLUE).next_to(endo, LEFT, buff=0.2).shift(UP * 0.8)
            inner = VGroup(*[T("TLR" + n, 24, BLUE) for n in ["3", "7", "8", "9"]]).arrange_in_grid(2, 2, buff=(0.4, 0.2)) \
                .move_to(endo).shift(UP * 0.35)
            self.play(Create(endo), FadeIn(el), run_time=self.fit(0.8))
            self.play(LaggedStart(*[FadeIn(x) for x in inner], lag_ratio=0.3), run_time=self.fit(1.0))
            self.cue("detect nucleic")
            na = T("nucleic acids", 26, PINK).move_to(endo).shift(DOWN * 0.7)
            self.play(Write(na), run_time=self.fit(0.8))
            self.cue("Host RNA")
            host = VGroup(T("host RNA: not in endosomes", 28, GREEN),
                          T("→ location tells microbe from self", 28, GREEN)).arrange(DOWN, aligned_edge=LEFT, buff=0.15) \
                .move_to([-2.6, -1.5, 0])
            self.play(Write(host), run_time=self.fit(2.0))
            self.tag("Abbas p.69")

        # ---------------- b08 surface ligands ----------------
        with self.beat("b08"):
            self.clear_board()
            h = self.header("Surface TLRs: what they bind")
            self.play(Write(h), run_time=self.fit(0.8))
            rows = [("LPS (gram-negative)", "TLR4", "LPS of"),
                    ("peptidoglycan, LTA (gram-positive)", "TLR2", "Peptidoglycan"),
                    ("lipopeptides", "TLR2 + TLR1 or TLR6", "TLR2 pairs"),
                    ("flagellin (motile bacteria)", "TLR5", "Flagellin")]
            for i, (l, r, key) in enumerate(rows):
                self.cue(key)
                g = row(l, r, 1.5 - i * 1.25, mid=0.8)
                self.play(FadeIn(g[0], shift=RIGHT * 0.3), GrowArrow(g[1]), FadeIn(g[2]), run_time=self.fit(1.0))
            self.tag("Abbas p.67 · Janeway p.87")

        # ---------------- b09 TLR4 helpers ----------------
        with self.beat("b09"):
            self.clear_board()
            h = self.header("How TLR4 sees LPS")
            self.play(Write(h), run_time=self.fit(0.8))
            lps = bx("LPS", PINK, 30)
            lbp = bx("LPS-binding protein", GREEN, 28)
            md2 = bx("MD2", BLUE, 30)
            tlr = bx("TLR4", BLUE, 32)
            chain = VGroup(lps, lbp, md2, tlr).arrange(RIGHT, buff=1.0).move_to([0, 0.0, 0])
            arrows = [arr(a, b) for a, b in zip(chain, chain[1:])]
            self.play(FadeIn(lps), run_time=0.4)
            self.cue("First")
            self.play(GrowArrow(arrows[0]), FadeIn(lbp, shift=RIGHT * 0.3), run_time=self.fit(1.0))
            n1 = T("soluble", 24, GREY).next_to(lbp, DOWN, buff=0.2)
            self.play(FadeIn(n1), run_time=0.4)
            self.cue("CD14")
            cd = bx("CD14", BLUE, 28).move_to([(md2.get_center()[0] + tlr.get_center()[0]) / 2, 1.9, 0])
            cdn = T("needed for efficient signalling", 24, GREY).next_to(cd, UP, buff=0.15)
            self.play(FadeIn(cd, shift=DOWN * 0.3), FadeIn(cdn), run_time=self.fit(1.0))
            self.cue("Then the")
            self.play(GrowArrow(arrows[1]), FadeIn(md2, shift=RIGHT * 0.3), run_time=self.fit(1.0))
            la = T("binds lipid A", 24, GREY).next_to(md2, DOWN, buff=0.2)
            self.play(FadeIn(la), run_time=0.4)
            self.cue("engages TLR4")
            ca = Arrow(cd.get_bottom(), arrows[2].get_center() + UP * 0.1, buff=0.1, color=GREY,
                       stroke_width=3, tip_length=0.18)
            self.play(GrowArrow(arrows[2]), FadeIn(tlr, shift=RIGHT * 0.3), GrowArrow(ca), run_time=self.fit(1.0))
            self.play(Circumscribe(tlr, color=YELLOW), run_time=self.fit(1.0))
            self.tag("Abbas p.69")

        # ---------------- b10 endosomal ligands ----------------
        with self.beat("b10"):
            self.clear_board()
            h = self.header("Endosomal TLRs: nucleic acids")
            self.play(Write(h), run_time=self.fit(0.8))
            rows = [("double-stranded RNA", "TLR3", "TLR3 binds"),
                    ("viral single-stranded RNA", "TLR7, TLR8", "TLR7 and"),
                    ("unmethylated CpG DNA", "TLR9", "TLR9 binds")]
            for i, (l, r, key) in enumerate(rows):
                self.cue(key)
                g = row(l, r, 1.7 - i * 1.15, mid=0.6)
                self.play(FadeIn(g[0], shift=RIGHT * 0.3), GrowArrow(g[1]), FadeIn(g[2]), run_time=self.fit(1.0))
            self.cue("Our own")
            self_row = VGroup(T("methylated CpG (self)", 30, GREEN), T("silent", 30, GREEN)).arrange(RIGHT, buff=1.0) \
                .move_to([0.0, -1.5, 0])
            self.play(Write(self_row), run_time=self.fit(1.2))
            self.cue("Plasmacytoid")
            ex = T("TLR9 is on: plasmacytoid DCs, B cells", 28, BLUE).move_to([0, -2.6, 0])
            self.play(FadeIn(ex, shift=UP * 0.2), run_time=self.fit(1.0))
            self.tag("Abbas p.67 · Janeway p.86–88")

        # ---------------- b11 adaptor rules ----------------
        with self.beat("b11"):
            self.clear_board()
            h = self.header("Adaptors: learn three sentences")
            self.play(Write(h), run_time=self.fit(0.8))
            ad = VGroup(*[bx(n, BLUE, 30) for n in ["MyD88", "MAL", "TRIF", "TRAM"]]).arrange(RIGHT, buff=0.7) \
                .move_to([0, 1.6, 0])
            self.play(LaggedStart(*[FadeIn(a, shift=DOWN * 0.3) for a in ad], lag_ratio=0.25), run_time=self.fit(1.6))
            rules = VGroup(Tm('1. Every TLR <span foreground="#F2A2B8">except TLR3</span> uses MyD88', 32),
                           Tm('2. Only TLR3 and TLR4 use TRIF', 32),
                           Tm('3. <span foreground="#F4E285">TLR4 uses both</span>', 32)) \
                .arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, -1.0, 0])
            for i, (key, hl) in enumerate([("Every TLR", ad[0]), ("Only TLR3", ad[2]), ("So TLR4", None)]):
                self.cue(key)
                anims = [Write(rules[i])]
                if hl is not None:
                    anims.append(Indicate(hl, color=YELLOW))
                else:
                    anims += [Indicate(ad[0], color=YELLOW), Indicate(ad[2], color=YELLOW)]
                self.play(*anims, run_time=self.fit(1.4))
            self.tag("Abbas p.69 · Janeway p.90")

        # ---------------- b12 MyD88 branch ----------------
        with self.beat("b12"):
            self.clear_board()
            h = self.header("TLR4 signalling: two branches")
            self.play(Write(h), run_time=self.fit(0.8))
            tlr4 = bx("TLR4", BLUE, 32).move_to([0, 2.1, 0])
            self.play(FadeIn(tlr4), run_time=0.5)
            L = [bx("MyD88", BLUE, 26), bx("IRAK4 · IRAK1", BLUE, 26), bx("TRAF6 → TAK1", BLUE, 26),
                 bx("IKK (incl. NEMO)", BLUE, 26), bx("IκB releases NF-κB", YELLOW, 26)]
            for i, m in enumerate(L):
                m.move_to([-4.5, 1.15 - i * 1.05, 0])
            cues = ["MyD88 recruits", "IRAK4", "TRAF6", "IKK complex", "IKK phosphorylates"]
            self.cue("MyD88 branch")
            self.play(GrowArrow(arr(tlr4, L[0])), FadeIn(L[0]), run_time=self.fit(0.8))
            for i in range(1, len(L)):
                self.cue(cues[i])
                self.play(GrowArrow(arr(L[i - 1], L[i], buff=0.04)), FadeIn(L[i], shift=DOWN * 0.2), run_time=self.fit(0.8))
            self.play(Circumscribe(L[-1], color=YELLOW), run_time=self.fit(0.8))
            self.tag("Janeway p.91")
            self.d8 = VGroup(tlr4, *L)

        # ---------------- b13 NF-kB outputs ----------------
        with self.beat("b13"):
            outs = VGroup(T("TNF, IL-1, IL-6", 28, YELLOW), T("CXCL8, CCL2", 28, YELLOW),
                          T("E-selectin", 28, YELLOW), T("CD80, CD86 on DCs", 28, GREEN),
                          T("→ start adaptive immunity", 26, GREEN)) \
                .arrange(DOWN, aligned_edge=LEFT, buff=0.22)
            outs.move_to([-1.9 + outs.width / 2, -1.25, 0])
            nf = self.d8[-1]
            a = Arrow(nf.get_right(), outs[2].get_left() + LEFT * 0.1, buff=0.1, color=YELLOW, stroke_width=4,
                      tip_length=0.2)
            self.play(GrowArrow(a), run_time=self.fit(0.6))
            for i, key in enumerate(["TNF", "chemokines", "E-selectin", "CD80", "help start"]):
                self.cue(key)
                self.play(FadeIn(outs[i], shift=RIGHT * 0.3), run_time=self.fit(0.7))
            self.tag("Abbas p.69 · Janeway p.96")
            self.nfout = VGroup(outs, a)

        # ---------------- b14 TRIF branch ----------------
        with self.beat("b14"):
            tlr4 = self.d8[0]
            R = [bx("TRIF", BLUE, 28), bx("TBK1 · IKKε", BLUE, 28), bx("IRF3", BLUE, 28), bx("IFN-β", GREEN, 30)]
            for i, m in enumerate(R):
                m.move_to([4.6, 1.15 - i * 1.05, 0])
            self.play(GrowArrow(arr(tlr4, R[0])), FadeIn(R[0]), run_time=self.fit(0.8))
            for i, key in enumerate(["TBK1", "IRF3", "interferon beta"], start=1):
                self.cue(key)
                self.play(GrowArrow(arr(R[i - 1], R[i], buff=0.04)), FadeIn(R[i], shift=DOWN * 0.2), run_time=self.fit(0.8))
            self.cue("TLR3 uses")
            t3 = T("TLR3: this branch only", 26, BLUE).move_to([4.6, -2.75, 0])
            self.play(Write(t3), run_time=self.fit(1.0))
            self.cue("TLR4 uses both")
            both = VGroup(T("TLR4 uses both:", 28, YELLOW), T("inflammation + antiviral", 28, YELLOW)) \
                .arrange(DOWN, buff=0.15).move_to([0.1, -1.0, 0])
            self.play(FadeOut(self.nfout), run_time=0.4)
            self.play(Indicate(tlr4, color=YELLOW), Write(both), run_time=self.fit(1.5))
            self.tag("Abbas p.69 · Janeway p.92")

        # ---------------- b15 endosomal MyD88 -> IRF7 in pDC ----------------
        with self.beat("b15"):
            self.clear_board()
            h = self.header("Endosomal TLRs in plasmacytoid DCs")
            self.play(Write(h), run_time=self.fit(0.8))
            pdc = Ellipse(width=12.6, height=4.6, color=BLUE, stroke_width=4).set_fill(BLUE, 0.05).move_to([0, -0.6, 0])
            pl = T("plasmacytoid dendritic cell (pDC)", 26, BLUE).move_to(pdc.get_bottom() + UP * 0.55)
            self.play(Create(pdc), FadeIn(pl), run_time=self.fit(1.0))
            endo = Circle(1.1, color=BLUE, stroke_width=4).set_fill(BLUE, 0.12).move_to([-4.0, -0.4, 0])
            et = T("TLR7 / TLR9", 26, BLUE).move_to(endo)
            el = T("endosome", 24, GREY).next_to(endo, DOWN, buff=0.12)
            self.play(Create(endo), FadeIn(et), FadeIn(el), run_time=self.fit(1.0))
            my = bx("MyD88", BLUE, 28).move_to([-1.3, -0.4, 0])
            irf = bx("IRF7", BLUE, 28).move_to([1.1, -0.4, 0])
            ifn = bx("IFN-α, IFN-β", GREEN, 30).move_to([4.0, -0.4, 0])
            self.cue("MyD88 too")
            self.play(GrowArrow(arr(endo, my)), FadeIn(my), run_time=self.fit(0.8))
            self.cue("binds IRF7")
            self.play(GrowArrow(arr(my, irf)), FadeIn(irf), run_time=self.fit(0.8))
            dn = T("binds directly", 24, YELLOW).next_to(VGroup(my, irf), UP, buff=0.3)
            self.play(FadeIn(dn), run_time=0.4)
            self.cue("produce interferon")
            self.play(GrowArrow(arr(irf, ifn)), FadeIn(ifn, shift=RIGHT * 0.2), run_time=self.fit(0.8))
            self.play(Circumscribe(ifn, color=GREEN), run_time=self.fit(1.0))
            self.tag("Abbas p.69 · Janeway p.92")

        # ---------------- b16 MyD88/IRAK4 deficiency ----------------
        with self.beat("b16"):
            self.clear_board()
            h = self.header("When a branch fails")
            self.play(Write(h), run_time=self.fit(0.8))
            divider = DashedLine([0, 2.6, 0], [0, -3.3, 0], color=GREY, stroke_width=2)
            self.play(Create(divider), run_time=0.4)
            ch = VGroup(bx("MyD88", BLUE, 26), bx("IRAK4", BLUE, 26), bx("NF-κB", BLUE, 26)).arrange(RIGHT, buff=0.55) \
                .move_to([-3.25, 2.0, 0])
            ca = VGroup(*[arr(a, b) for a, b in zip(ch, ch[1:])])
            self.cue("This pathway")
            self.play(FadeIn(ch), Create(ca), run_time=self.fit(0.8))
            under = T("under most TLRs + IL-1R", 24, GREY).next_to(ch, DOWN, buff=0.18)
            self.play(FadeIn(under), run_time=0.4)
            self.cue("Children")
            self.play(Create(strike(ch[0])), Create(strike(ch[1])), run_time=self.fit(0.8))
            L = stack(["severe invasive bacterial", "infections, early in life",
                       "especially pneumococcal", "no fever, little inflammation"], size=26, color=PINK, buff=0.15) \
                .move_to([-3.25, -0.6, 0])
            self.play(FadeIn(L[0:2], shift=UP * 0.2), run_time=self.fit(0.8))
            self.cue("especially")
            self.play(FadeIn(L[2], shift=UP * 0.2), run_time=self.fit(0.6))
            self.cue("no fever")
            self.play(FadeIn(L[3], shift=UP * 0.2), run_time=self.fit(0.6))
            self.cue("cold infections")
            cold = bx("“cold” infections", PINK, 30).move_to([-3.25, -2.45, 0])
            self.play(FadeIn(cold, scale=1.2), run_time=self.fit(0.8))
            self.tag("Abbas p.489 · Janeway p.535")
            self.left_card = VGroup(ch, ca, under, L, cold)

        # ---------------- b17 better with age; TLR3 -> HSE ----------------
        with self.beat("b17"):
            age = T("improves with age; IRAK4: no extra viral risk", 24, GREEN).move_to([-3.25, -3.25, 0])
            if age.width > 6.2:
                age = VGroup(T("improves with age", 24, GREEN), T("IRAK4: no extra viral risk", 24, GREEN)) \
                    .arrange(RIGHT, buff=0.4).move_to([-3.25, -3.25, 0])
            self.play(FadeIn(age, shift=UP * 0.2), run_time=self.fit(1.0))
            self.cue("Now break")
            ch = VGroup(bx("TLR3", BLUE, 26), bx("TRIF", BLUE, 26), bx("IFN", GREEN, 26)).arrange(RIGHT, buff=0.55) \
                .move_to([3.25, 2.0, 0])
            ca = VGroup(*[arr(a, b) for a, b in zip(ch, ch[1:])])
            self.play(FadeIn(ch), Create(ca), run_time=self.fit(0.8))
            self.cue("TLR3 loss")
            self.play(Create(strike(ch[0])), run_time=self.fit(0.6))
            hse = bx("herpes simplex encephalitis", PINK, 28).move_to([3.25, 0.7, 0])
            self.play(FadeIn(hse, scale=1.2), run_time=self.fit(0.8))
            self.cue("other viral")
            ov = T("other viral infections: not generally ↑", 24, GREY).next_to(hse, DOWN, buff=0.25)
            self.play(FadeIn(ov), run_time=self.fit(0.8))
            self.right_card = VGroup(ch, ca, hse, ov)

        # ---------------- b18 other HSE genes ----------------
        with self.beat("b18"):
            ge = VGroup(T("same risk:", 26, CHALK), T("TRIF · TRAF3 · TBK1 · UNC93B", 28, PINK)) \
                .arrange(DOWN, buff=0.15).move_to([3.25, -1.0, 0])
            self.play(Write(ge), run_time=self.fit(1.8))
            self.cue("UNC93B moves")
            un = VGroup(T("UNC93B moves TLRs", 26, BLUE), T("ER → endosome", 26, BLUE)).arrange(DOWN, buff=0.12) \
                .move_to([3.25, -2.5, 0])
            self.play(FadeIn(un, shift=UP * 0.2), Indicate(ge[1], color=YELLOW), run_time=self.fit(1.2))
            self.tag("Abbas p.69, 489")

        # ---------------- b19 NOD1/NOD2 ----------------
        with self.beat("b19"):
            self.clear_board()
            h = self.header("NOD1 & NOD2: sensors in the cytosol")
            self.play(Write(h), run_time=self.fit(0.8))
            pg = T("bacterial peptidoglycan", 28, PINK).move_to([0, 2.15, 0])
            self.cue("sense bacterial")
            self.play(Write(pg), run_time=self.fit(0.8))
            l1 = VGroup(T("DAP", 28, PINK), T("mainly gram-negative", 24, GREY)).arrange(DOWN, buff=0.1).move_to([-3.4, 1.0, 0])
            l2 = VGroup(T("MDP", 28, PINK), T("gram-negative + gram-positive", 24, GREY)).arrange(DOWN, buff=0.1).move_to([3.4, 1.0, 0])
            n1 = bx("NOD1", BLUE, 30).move_to([-3.4, -0.4, 0])
            n2 = bx("NOD2", BLUE, 30).move_to([3.4, -0.4, 0])
            self.cue("NOD1 sees")
            self.play(FadeIn(l1), FadeIn(n1), GrowArrow(arr(l1, n1)), run_time=self.fit(1.0))
            self.cue("NOD2 sees")
            self.play(FadeIn(l2), FadeIn(n2), GrowArrow(arr(l2, n2)), run_time=self.fit(1.0))
            rip = bx("RIP2", BLUE, 30).move_to([0, -1.6, 0])
            nf = bx("NF-κB", YELLOW, 30).move_to([0, -2.85, 0])
            self.cue("Both recruit")
            self.play(GrowArrow(arr(n1, rip)), GrowArrow(arr(n2, rip)), FadeIn(rip), run_time=self.fit(1.0))
            self.cue("activates NF")
            self.play(GrowArrow(arr(rip, nf)), FadeIn(nf), run_time=self.fit(0.8))
            self.tag("Abbas p.72")
            self.nod2 = n2

        # ---------------- b20 NOD2 two directions ----------------
        with self.beat("b20"):
            keep = self.nod2
            others = [m for m in self.mobjects if m is not keep and not isinstance(m, ImageMobject)]
            self.play(*[FadeOut(m) for m in others], keep.animate.move_to([0, 1.6, 0]).scale(1.2), run_time=0.8)
            h = self.header("NOD2: both directions cause disease")
            self.play(Write(h), run_time=self.fit(0.8))
            weak = VGroup(T("variants: weak sensing", 26, CHALK), T("of gut microbes", 26, CHALK)).arrange(DOWN, buff=0.1) \
                .move_to([-3.4, 0.0, 0])
            gof = VGroup(T("gain of function", 26, CHALK), T("(too strong)", 26, CHALK)).arrange(DOWN, buff=0.1) \
                .move_to([3.4, 0.0, 0])
            cr = bx("Crohn's disease risk ↑", PINK, 30).move_to([-3.4, -1.6, 0])
            bl = bx("Blau syndrome", PINK, 30).move_to([3.4, -1.6, 0])
            bld = T("joints · eyes · skin", 26, PINK).next_to(bl, DOWN, buff=0.2)
            self.cue("Some NOD2")
            self.play(GrowArrow(arr(keep, weak)), FadeIn(weak), run_time=self.fit(0.8))
            self.cue("Crohn")
            self.play(GrowArrow(arr(weak, cr)), FadeIn(cr), run_time=self.fit(0.8))
            self.cue("Gain-of")
            self.play(GrowArrow(arr(keep, gof)), FadeIn(gof), run_time=self.fit(0.8))
            self.cue("Blau")
            self.play(GrowArrow(arr(gof, bl)), FadeIn(bl), run_time=self.fit(0.8))
            self.cue("joints")
            self.play(FadeIn(bld), run_time=self.fit(0.6))
            trap = T("Exam trap: check the direction of the mutation", 26, YELLOW).move_to([0, -3.2, 0])
            self.play(Write(trap), run_time=self.fit(1.2))
            self.tag("Abbas p.72 · Janeway p.93")

        # ---------------- b21 inflammasome: two signals ----------------
        with self.beat("b21"):
            self.clear_board()
            h = self.header("NLRP3 inflammasome: two signals")
            self.play(Write(h), run_time=self.fit(0.8))
            cyt = T("multiprotein complex in the cytosol", 26, GREY).move_to([0, 2.3, 0])
            self.play(FadeIn(cyt), run_time=self.fit(0.6))
            s1 = T("Signal 1", 30, YELLOW).move_to([-5.5, 1.2, 0])
            s2 = T("Signal 2", 30, YELLOW).move_to([-5.5, -0.8, 0])
            tl = bx("TLR", BLUE, 28).move_to([-3.6, 1.2, 0])
            nf = bx("NF-κB", BLUE, 28).move_to([-1.4, 1.2, 0])
            pro = bx("pro-IL-1β (inactive)", GREY, 28).move_to([2.2, 1.2, 0])
            self.cue("Signal 1")
            self.play(Write(s1), FadeIn(tl), run_time=self.fit(0.6))
            self.play(GrowArrow(arr(tl, nf)), FadeIn(nf), run_time=self.fit(0.6))
            self.cue("makes inactive")
            self.play(GrowArrow(arr(nf, pro)), FadeIn(pro), run_time=self.fit(0.8))
            self.cue("Signal 2")
            inf = bx("inflammasome", BLUE, 30).move_to([2.2, -0.8, 0])
            self.play(Write(s2), FadeIn(inf), run_time=self.fit(0.8))
            self.cue("cuts the")
            cut = arr(inf, pro, color=YELLOW)
            ct = T("cuts", 26, YELLOW).next_to(cut, RIGHT, buff=0.15)
            self.play(GrowArrow(cut), FadeIn(ct), run_time=self.fit(0.8))
            self.tag("Abbas p.72, 93")
            self.d9 = dict(s2=s2, inf=inf, pro=pro, cut=cut, ct=ct)

        # ---------------- b22 triggers + assembly ----------------
        with self.beat("b22"):
            d = self.d9
            trig = VGroup(T("K+ efflux", 26, PINK), T("ROS", 26, PINK), T("crystals", 26, PINK),
                          T("(lysosome damage)", 24, GREY)).arrange(DOWN, buff=0.12).move_to([-2.5, -1.5, 0])
            self.play(FadeIn(trig[0]), run_time=self.fit(0.5))
            self.cue("reactive")
            self.play(FadeIn(trig[1]), run_time=self.fit(0.5))
            self.cue("Crystals")
            self.play(FadeIn(trig[2:]), run_time=self.fit(0.6))
            self.cue("NLRP3 molecules")
            chain = VGroup(bx("NLRP3", BLUE, 28), bx("ASC", BLUE, 28), bx("caspase-1", YELLOW, 28)) \
                .arrange(RIGHT, buff=0.6).move_to([2.2, -0.8, 0])
            self.play(FadeOut(d["cut"]), FadeOut(d["ct"]), ReplacementTransform(d["inf"], chain[0]), run_time=self.fit(0.8))
            ta = arr(trig, chain[0], color=PINK)
            self.play(GrowArrow(ta), run_time=0.4)
            a1 = arr(chain[0], chain[1])
            self.cue("adaptor ASC")
            self.play(GrowArrow(a1), FadeIn(chain[1]), run_time=self.fit(0.6))
            self.cue("procaspase")
            a2 = arr(chain[1], chain[2])
            self.play(GrowArrow(a2), FadeIn(chain[2]), run_time=self.fit(0.8))
            self.cue("Caspase-1 cuts")
            cut = arr(chain[2], d["pro"], color=YELLOW)
            out = bx("IL-1β · IL-18", YELLOW, 30).move_to([2.2, -2.6, 0])
            self.play(GrowArrow(cut), run_time=self.fit(0.5))
            self.play(TransformFromCopy(d["pro"], out), run_time=self.fit(1.0))
            self.play(Circumscribe(out, color=YELLOW), run_time=self.fit(0.8))
            self.tag("Abbas p.72–74")

        # ---------------- b23 gasdermin + pyroptosis ----------------
        with self.beat("b23"):
            self.clear_board()
            h = self.header("Gasdermin D pores & pyroptosis")
            self.play(Write(h), run_time=self.fit(0.8))
            mac = Circle(1.7, color=BLUE, stroke_width=5).set_fill(BLUE, 0.1).move_to([-3.5, -0.3, 0])
            ml = T("macrophage", 26, BLUE).next_to(mac, DOWN, buff=0.5)
            c1 = T("caspase-1", 26, YELLOW).move_to(mac).shift(UP * 0.5)
            self.play(Create(mac), FadeIn(ml), FadeIn(c1), run_time=self.fit(0.8))
            steps = VGroup(T("caspase-1 cleaves gasdermin D", 28), T("fragment → membrane pores", 28),
                           T("IL-1β exits through pores", 28), T("fluid in → cell swells, dies", 28),
                           T("= pyroptosis", 32, PINK)) \
                .arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([2.6, 0.2, 0])
            self.play(FadeIn(steps[0], shift=RIGHT * 0.2), run_time=self.fit(0.6))
            self.cue("forms pores")
            pores = VGroup(*[Rectangle(width=0.22, height=0.38, color=PINK, stroke_width=3).set_fill(BOARD, 1)
                             .move_to(mac.point_at_angle(a)).rotate(a) for a in [0.4, 1.3, 2.4, 3.4, 4.6, 5.6]])
            self.play(FadeIn(steps[1], shift=RIGHT * 0.2), LaggedStart(*[GrowFromCenter(p) for p in pores], lag_ratio=0.15),
                      run_time=self.fit(1.0))
            self.cue("IL-1β has")
            dots = VGroup(*[Dot(mac.get_center() + 0.6 * np.array([np.cos(a), np.sin(a), 0]) + DOWN * 0.2,
                                radius=0.08, color=YELLOW) for a in [0.4, 1.3, 2.4, 3.4, 4.6, 5.6]])
            self.play(FadeIn(dots), FadeIn(steps[2], shift=RIGHT * 0.2), run_time=self.fit(0.6))
            self.play(*[d.animate.move_to(mac.point_at_angle(a) + 0.5 * np.array([np.cos(a), np.sin(a), 0]))
                        for d, a in zip(dots, [0.4, 1.3, 2.4, 3.4, 4.6, 5.6])], run_time=self.fit(1.2))
            self.cue("fluid in")
            self.play(FadeIn(steps[3], shift=RIGHT * 0.2), FadeOut(dots),
                      VGroup(mac, pores).animate.scale(1.12).set_color(PINK), run_time=self.fit(1.2))
            self.cue("pyroptosis")
            self.play(Write(steps[4]), run_time=self.fit(0.8))
            self.cue("It affects")
            who = Tm('<span foreground="#A8E6A1">macrophages, DCs</span>   ·   <span foreground="#F2A2B8">not neutrophils</span>', 28) \
                .move_to([1.0, -3.0, 0])
            self.play(Write(who), run_time=self.fit(1.2))
            self.tag("Abbas p.72–74")

        # ---------------- b24 NLRP3 triggers ----------------
        with self.beat("b24"):
            self.clear_board()
            h = self.header("What NLRP3 senses")
            self.play(Write(h), run_time=self.fit(0.8))
            core = bx("NLRP3", BLUE, 34).move_to([0, -0.3, 0])
            self.play(FadeIn(core, scale=1.2), run_time=0.5)
            spots = [("crystals", [-3.8, 1.5]), ("silica", [3.8, 1.5]), ("extracellular ATP", [-3.9, -0.3]),
                     ("bacterial toxins", [3.9, -0.3]), ("influenza virus", [-3.8, -2.1]), ("alum", [3.8, -2.1])]
            keys = ["crystals", "silica", "ATP", "toxins", "influenza", "alum"]
            items = []
            for (nm, p), k in zip(spots, keys):
                self.cue(k)
                m = T(nm, 30, YELLOW if nm == "alum" else PINK).move_to(p + [0])
                a = arr(m, core, color=GREY, stroke=3)
                self.play(FadeIn(m, shift=(core.get_center() - m.get_center()) * 0.05), GrowArrow(a), run_time=self.fit(0.6))
                items.append(m)
            self.cue("adjuvant")
            note = T("alum's adjuvant effect needs NLRP3", 26, YELLOW).next_to(items[-1], DOWN, buff=0.25)
            note.shift(LEFT * max(0, note.get_right()[0] - 6.4))
            self.play(Circumscribe(items[-1], color=YELLOW), FadeIn(note), run_time=self.fit(1.2))
            self.tag("Abbas p.74 · Janeway p.94")

        # ---------------- b25 autoinflammatory vs autoimmune ----------------
        with self.beat("b25"):
            self.clear_board()
            h = self.header("Autoinflammatory ≠ autoimmune")
            self.play(Write(h), run_time=self.fit(0.8))
            div = DashedLine([0.3, 2.4, 0], [0.3, -3.2, 0], color=GREY, stroke_width=2)
            lt = T("Autoinflammatory", 34, PINK).move_to([-3.1, 2.0, 0])
            rt = T("Autoimmune", 34, BLUE).move_to([3.5, 2.0, 0])
            self.play(Create(div), Write(lt), run_time=self.fit(0.8))
            lb = bullet_list(["gain of function in", "inflammasome parts", "too much IL-1", "recurrent fever",
                              "skin · joints · abdomen"], size=28)
            lb[1][0].set_opacity(0)
            lb.move_to([-3.1, -0.4, 0])
            self.play(FadeIn(lb[0:2], shift=UP * 0.2), run_time=self.fit(0.8))
            self.cue("too much")
            self.play(FadeIn(lb[2], shift=UP * 0.2), run_time=self.fit(0.6))
            self.cue("recurrent")
            self.play(FadeIn(lb[3], shift=UP * 0.2), run_time=self.fit(0.6))
            self.cue("skin")
            self.play(FadeIn(lb[4], shift=UP * 0.2), run_time=self.fit(0.6))
            self.cue("Unlike")
            rb = bullet_list(["self-reactive antibodies", "self-reactive T cells"], size=28).move_to([3.5, 0.4, 0])
            self.play(Write(rt), FadeIn(rb, shift=UP * 0.2), run_time=self.fit(1.2))
            self.tag("Abbas p.74")

        # ---------------- b26 CAPS ----------------
        with self.beat("b26"):
            self.clear_board()
            h = self.header("CAPS: NLRP3 gain of function")
            self.play(Write(h), run_time=self.fit(0.8))
            top = bx("NLRP3 (cryopyrin) ↑", PINK, 32).move_to([0, 2.0, 0])
            self.play(FadeIn(top, shift=DOWN * 0.2), run_time=self.fit(0.8))
            c1 = VGroup(T("Familial cold autoinflammatory", 26, YELLOW), T("syndrome (FCAS)", 26, YELLOW),
                        T("cold triggers the fever", 26, CHALK)).arrange(DOWN, buff=0.12)
            c2 = VGroup(T("Muckle-Wells syndrome", 26, YELLOW), T("+ progressive deafness", 26, CHALK)) \
                .arrange(DOWN, buff=0.12)
            b1 = VGroup(chalk_box(c1, PINK), c1).move_to([-3.2, 0.35, 0])
            b2 = VGroup(chalk_box(c2, PINK), c2).move_to([3.2, 0.35, 0])
            b2[0].stretch_to_fit_height(b1[0].height)
            self.cue("In familial")
            self.play(GrowArrow(arr(top, b1)), FadeIn(b1), run_time=self.fit(1.0))
            self.cue("Muckle")
            self.play(GrowArrow(arr(top, b2)), FadeIn(b2), run_time=self.fit(1.0))
            self.cue("Both give")
            both = Tm('Both: <span foreground="#F2A2B8">urticarial rash</span> · joint pain · conjunctivitis', 28) \
                .move_to([0, -1.25, 0])
            self.play(Write(both), run_time=self.fit(1.8))
            self.tag("Abbas p.74 · Janeway p.537")

        # ---------------- b27 IL-1 blockade (volatile) ----------------
        with self.beat("b27"):
            dr = bx("IL-1 antagonists, e.g. anakinra", ORANGE, 30).move_to([0, -2.35, 0])
            self.play(FadeIn(dr, shift=UP * 0.3), run_time=self.fit(1.0))
            self.cue("Drug choices")
            v = T("volatile: check current guidance", 24, GREY).move_to([-2.5, -3.3, 0])
            self.play(FadeIn(v), Indicate(dr, color=ORANGE), run_time=self.fit(1.0))

        # ---------------- b28 RLRs ----------------
        with self.beat("b28"):
            self.clear_board()
            h = self.header("Cytosolic RNA & DNA sensors")
            self.play(Write(h), run_time=self.fit(0.8))
            vr = T("viral RNA", 30, PINK).move_to([-3.7, 2.2, 0])
            self.play(Write(vr), run_time=self.fit(0.6))
            rig = bx("RIG-I", BLUE, 28).move_to([-5.0, 1.0, 0])
            mda = bx("MDA5", BLUE, 28).move_to([-2.4, 1.0, 0])
            rl = T("5'-triphosphate", 24, PINK).next_to(rig, DOWN, buff=0.15)
            ml = T("long dsRNA", 24, PINK).next_to(mda, DOWN, buff=0.15)
            self.cue("RIG-I recognizes")
            self.play(GrowArrow(arr(vr, rig)), FadeIn(rig), FadeIn(rl), run_time=self.fit(1.0))
            self.cue("Host mRNA")
            host = VGroup(T("host mRNA: capped", 26, GREEN), T("→ silent", 26, GREEN)).arrange(DOWN, buff=0.1) \
                .move_to([3.2, 1.2, 0])
            self.play(FadeIn(host), run_time=self.fit(0.8))
            self.cue("MDA5 recognizes")
            self.play(GrowArrow(arr(vr, mda)), FadeIn(mda), FadeIn(ml), run_time=self.fit(1.0))
            self.tag("Abbas p.75–76")
            self.d10 = dict(rig=rig, mda=mda, rl=rl, ml=ml, host=host)

        # ---------------- b29 MAVS ----------------
        with self.beat("b29"):
            d = self.d10
            self.play(FadeOut(d["host"]), run_time=0.4)
            mavs = bx("MAVS (mitochondria)", BLUE, 28).move_to([-3.7, -0.65, 0])
            self.play(GrowArrow(arr(d["rl"], mavs)), GrowArrow(arr(d["ml"], mavs)), FadeIn(mavs), run_time=self.fit(1.0))
            self.cue("MAVS recruits")
            tb = bx("TRAF → TBK1 · IKK", BLUE, 28).move_to([0, -1.5, 0])
            self.play(GrowArrow(arr(mavs, tb)), FadeIn(tb), run_time=self.fit(1.0))
            self.cue("Then IRF3")
            irf = bx("IRF3 · IRF7 · NF-κB", BLUE, 28).move_to([0, -2.45, 0])
            ifn = bx("type I IFN", GREEN, 30).move_to([4.3, -2.45, 0])
            self.play(GrowArrow(arr(tb, irf)), FadeIn(irf), run_time=self.fit(0.8))
            self.cue("induce type")
            self.play(GrowArrow(arr(irf, ifn)), FadeIn(ifn, shift=RIGHT * 0.2), run_time=self.fit(0.8))
            self.tag("Abbas p.76")
            d.update(tb=tb, ifn=ifn, irf=irf)

        # ---------------- b30 cGAS-STING ----------------
        with self.beat("b30"):
            d = self.d10
            dna = T("cytosolic dsDNA", 30, PINK).move_to([3.7, 2.2, 0])
            self.play(Write(dna), run_time=self.fit(0.8))
            cg = bx("cGAS", BLUE, 28).move_to([3.7, 1.15, 0])
            cgamp = T("cGAMP", 28, YELLOW).move_to([3.7, 0.3, 0])
            st = bx("STING (ER)", BLUE, 28).move_to([3.7, -0.6, 0])
            self.cue("It activates")
            self.play(GrowArrow(arr(dna, cg)), FadeIn(cg), run_time=self.fit(0.8))
            self.cue("makes the")
            self.play(GrowArrow(arr(cg, cgamp)), FadeIn(cgamp), run_time=self.fit(0.8))
            self.cue("cGAMP binds")
            self.play(GrowArrow(arr(cgamp, st)), FadeIn(st), run_time=self.fit(0.8))
            self.cue("STING activates")
            self.play(GrowArrow(arr(st, d["tb"], color=YELLOW)), run_time=self.fit(0.8))
            self.cue("both routes")
            self.play(Circumscribe(d["tb"], color=YELLOW), Indicate(d["ifn"], color=GREEN), run_time=self.fit(1.5))
            self.tag("Abbas p.75–76")

        # ---------------- b31 interferonopathies ----------------
        with self.beat("b31"):
            self.clear_board()
            h = self.header("Too much interferon: interferonopathies")
            self.play(Write(h), run_time=self.fit(0.8))
            div = DashedLine([0, 2.4, 0], [0, -3.2, 0], color=GREY, stroke_width=2)
            self.play(Create(div), run_time=0.3)
            s = bx("STING ↑ (gain of function)", PINK, 28).move_to([-3.25, 1.6, 0])
            sav = bx("SAVI", PINK, 34).move_to([-3.25, 0.1, 0])
            sf = stack(["skin vasculopathy", "fever", "interstitial lung disease"], size=26, buff=0.15) \
                .next_to(sav, DOWN, buff=0.35)
            self.cue("Gain-of")
            self.play(FadeIn(s), run_time=self.fit(0.8))
            self.cue("SAVI")
            self.play(GrowArrow(arr(s, sav)), FadeIn(sav), run_time=self.fit(0.6))
            self.cue("with skin")
            self.play(LaggedStart(*[FadeIn(x) for x in sf], lag_ratio=0.4), run_time=self.fit(1.5))
            self.cue("In Aicardi")
            n = VGroup(bx("nucleases ✗ (e.g. TREX1)", PINK, 28)).move_to([3.25, 1.6, 0])
            ag = VGroup(T("Aicardi-Goutières", 30, PINK), T("syndrome", 30, PINK)).arrange(DOWN, buff=0.1).move_to([3.25, 0.0, 0])
            ex = stack(["excess nucleic acid", "reaches the sensors"], size=26, buff=0.15, aligned=ORIGIN).next_to(ag, DOWN, buff=0.35)
            self.play(FadeIn(n), FadeIn(ag), GrowArrow(arr(n, ag)), run_time=self.fit(1.0))
            self.cue("let excess")
            self.play(FadeIn(ex), run_time=self.fit(1.0))
            self.tag("Abbas p.75–77")

        # ---------------- b32 allergy links ----------------
        with self.beat("b32"):
            self.clear_board()
            h = self.header("Links to allergy")
            self.play(Write(h), run_time=self.fit(0.8))
            mc = cell(1.3, BLUE, nucleus=True).move_to([-3.6, 0.7, 0])
            gran = VGroup(*[Dot(mc.get_center() + 0.85 * np.array([np.cos(a), np.sin(a), 0]), radius=0.07, color=YELLOW)
                            for a in np.linspace(0.3, TAU + 0.3, 10)[:-1]])
            rec = tlr_icon(BLUE, 0.6, tir=False).rotate(-PI / 2).move_to(mc.get_left() + LEFT * 0.45)
            mcl = T("mast cell + TLRs", 28, BLUE).next_to(mc, DOWN, buff=0.25)
            self.cue("Mast cells")
            self.play(FadeIn(mc), FadeIn(gran), Create(rec), FadeIn(mcl), run_time=self.fit(1.0))
            self.cue("One Abbas")
            conf = VGroup(T("Source conflict (Abbas):", 24, YELLOW),
                          T("ch.4: degranulation", 24, CHALK),
                          T("ch.20: mediators, no degranulation", 24, CHALK)).arrange(DOWN, aligned_edge=LEFT, buff=0.1) \
                .move_to([-3.6, -2.35, 0])
            self.play(FadeIn(conf[0:2]), run_time=self.fit(0.8))
            self.cue("another says")
            self.play(FadeIn(conf[2]), run_time=self.fit(0.8))
            self.cue("IL-33")
            ep = VGroup(*[Square(0.9, color=BLUE, stroke_width=3).set_fill(BLUE, 0.1) for _ in range(4)]) \
                .arrange(RIGHT, buff=0).move_to([3.3, 0.9, 0])
            nuc = VGroup(*[Dot(s.get_center(), radius=0.14, color=YELLOW) for s in ep])
            epl = T("barrier epithelium", 26, BLUE).next_to(ep, UP, buff=0.2)
            self.play(FadeIn(ep), FadeIn(nuc), FadeIn(epl), run_time=self.fit(1.0))
            ilt = T("IL-33 in nuclei", 24, YELLOW).next_to(ep, DOWN, buff=0.2)
            self.play(FadeIn(ilt), run_time=0.4)
            self.cue("acts as an")
            self.play(Create(strike(ep[2])), ep[2].animate.set_stroke(PINK), run_time=self.fit(0.6))
            al = bx("IL-33 = alarmin", YELLOW, 30).move_to([3.3, -1.5, 0])
            self.play(nuc[2].animate.move_to(al.get_top() + UP * 0.1), run_time=self.fit(0.6))
            self.play(FadeIn(al), FadeOut(nuc[2]), run_time=self.fit(0.6))
            self.tag("Abbas p.86, 94, 470")

        # ---------------- b33 five things ----------------
        with self.beat("b33"):
            self.clear_board()
            h = self.header("Five things to remember")
            self.play(Write(h), run_time=self.fit(0.8))
            items = [("Surface TLRs: microbial walls · endosomal TLRs: nucleic acids", "One:"),
                     ("All TLRs except TLR3 use MyD88", "Two:"),
                     ("IL-1β needs two signals", "Three:"),
                     ("RNA & DNA sensors → type I IFN", "Four:"),
                     ("MyD88/IRAK4 ✗ → cold infections · TLR3 ✗ → HSE", "Five:")]
            rows = VGroup()
            for i, (txt, _) in enumerate(items):
                n = T(f"{i + 1}", 34, YELLOW)
                t = T(txt, 28, CHALK)
                rows.add(VGroup(n, t).arrange(RIGHT, buff=0.35))
            rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, -0.4, 0])
            if rows.width > 12.8:
                rows.scale_to_fit_width(12.8)
            for r, (_, k) in zip(rows, items):
                self.cue(k)
                self.play(FadeIn(r, shift=RIGHT * 0.3), run_time=self.fit(0.8))

        # ---------------- b34 exam trap + next ----------------
        with self.beat("b34"):
            self.clear_board()
            h = self.header("Exam trap", PINK)
            self.play(Write(h), run_time=self.fit(0.6))
            mem = membrane(-3.0, 3.0, 1.3)
            t4 = tlr_icon(BLUE, 0.8).move_to([0, 1.4, 0])
            tl = T("TLR4: on the surface…", 30, BLUE).move_to([0, 2.45, 0])
            self.play(Create(mem), Create(t4), Write(tl), run_time=self.fit(1.0))
            self.cue("yet it")
            tr = bx("…yet uses TRIF → IFN", YELLOW, 32).move_to([0, -0.1, 0])
            self.play(GrowArrow(arr(t4, tr, color=YELLOW)), FadeIn(tr), run_time=self.fit(1.0))
            self.cue("Next")
            nx = T("Next: Phagocytosis & the respiratory burst", 34, GREEN).move_to([0, -2.2, 0])
            ln = Line(LEFT * 3, RIGHT * 3, color=CHALK, stroke_width=3).next_to(nx, DOWN, buff=0.3)
            self.play(Write(nx), Create(ln), run_time=self.fit(2.0))
            self.tag("Abbas p.69")

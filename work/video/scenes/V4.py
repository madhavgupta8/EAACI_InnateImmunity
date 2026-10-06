from chalk import *

# ---------------------------------------------------------------- local helpers
STEP_X = [-4.65, -1.55, 1.55, 4.65]      # extravasation step zones
ENDO_Y = -1.0                             # endothelium centre line
LEUK_R = 0.42


def microbe(scale=1.0):
    return Ellipse(width=0.55 * scale, height=0.32 * scale, color=PINK, stroke_width=3).set_fill(PINK, 0.45)


def selectin(pt, color=BLUE, down=False):
    d = DOWN if down else UP
    p = np.array(pt)
    return VGroup(Line(p, p + d * 0.28, color=color, stroke_width=3),
                  Dot(p + d * 0.33, radius=0.06, color=color))


def build_vessel():
    """Endothelial lining: 8 cells along y = ENDO_Y."""
    cells = VGroup(*[
        RoundedRectangle(corner_radius=0.12, width=1.5, height=0.5, stroke_color=BLUE, stroke_width=3)
        .set_fill(BLUE, 0.10).move_to([-6.2 + 0.775 + 1.55 * i, ENDO_Y, 0]) for i in range(8)])
    return cells


def leukocyte():
    return cell(LEUK_R, BLUE)


def roll(mob, dx, rt):
    start = mob.copy()

    def upd(m, a):
        m.become(start.copy().rotate(-a * dx / LEUK_R).shift(RIGHT * a * dx))
    return UpdateFromAlphaFunc(mob, upd, run_time=rt)


def chain(size=40, sub=True):
    """Respiratory burst chain O2 -> superoxide -> H2O2 -> HOCl with enzymes on arrows."""
    xs = [-5.3, -1.8, 1.7, 5.2]
    sp = [T(s, size, CHALK) for s in ["O₂", "O₂⁻", "H₂O₂", "HOCl"]]
    for s, x in zip(sp, xs):
        s.move_to([x, 0, 0])
    arrows = VGroup(*[chalk_arrow(a, b, YELLOW) for a, b in zip(sp, sp[1:])])
    enz = VGroup(*[T(e, 26, YELLOW).next_to(a, UP, buff=0.15)
                   for e, a in zip(["NADPH oxidase", "SOD", "MPO"], arrows)])
    names = VGroup(*[T(n, 24, GREY).next_to(s, DOWN, buff=0.25)
                     for n, s in zip(["oxygen", "superoxide", "hydrogen peroxide", "hypochlorous acid"], sp)])
    return VGroup(*sp), arrows, enz, names


def xmark(point, color=PINK, r=0.22):
    p = np.array(point)
    return VGroup(Line(p + UL * r, p + DR * r, color=color, stroke_width=6),
                  Line(p + DL * r, p + UR * r, color=color, stroke_width=6))


def block(box):
    """Animations that turn a label_box pink (step blocked)."""
    return [box[0].animate.set_stroke(PINK).set_fill(PINK, 0.18), box[1].animate.set_color(PINK)]


class V4(ChalkScene):
    VIDEO_ID = "V4"

    # -- small timing / layout helpers --
    def at(self, frac):
        """Wait until `frac` of the current beat has elapsed."""
        w = frac * self.bd - self.elapsed()
        if w > 0.05:
            self.wait(w)

    def go(self, *anims, t=1.0, **kw):
        self.play(*anims, run_time=self.fit(t), **kw)

    def caption(self, lines, color=CHALK, size=28):
        g = VGroup(*[T(l, size, color) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        if g.width > 10:
            g.scale_to_fit_width(10)
        g.to_edge(LEFT, buff=0.5).set_y(-3.0)
        anims = [FadeIn(g, shift=UP * 0.2)]
        if getattr(self, "_cap", None) is not None:
            anims.append(FadeOut(self._cap))
        self._cap = g
        return anims

    def tag(self, text):
        new = self.source_tag(text)
        anims = [FadeIn(new)]
        if getattr(self, "_tag", None) is not None and self._tag in self.mobjects:
            anims.append(FadeOut(self._tag))
        self._tag = new
        return anims

    def wipe(self):
        self.clear_board(run_time=self.fit(0.6))
        self._cap = None
        self._tag = None

    # ------------------------------------------------------------- construct
    def construct(self):
        self._cap = None
        self._tag = None

        # b01 hook --------------------------------------------------------
        with self.beat("b01"):
            title = self.title_card("Phagocytosis & the respiratory burst", "Innate immunity · video 4")
            self.go(Write(title), t=2.5)
            self.at(0.25)
            self.go(title.animate.scale(0.6).to_edge(UP, buff=0.4), t=1)
            steps = VGroup(*[label_box(s, c, 30) for s, c in
                             [("1  Leave the blood", BLUE), ("2  Find", BLUE), ("3  Swallow", BLUE), ("4  Kill", YELLOW)]]
                           ).arrange(RIGHT, buff=0.7).move_to(UP * 0.2)
            if steps.width > 12.6:
                steps.scale_to_fit_width(12.6)
            arrs = VGroup(*[chalk_arrow(a, b, CHALK, buff=0.08) for a, b in zip(steps, steps[1:])])
            for i, s in enumerate(steps):
                anims = [FadeIn(s, shift=RIGHT * 0.3)]
                if i:
                    anims.append(GrowArrow(arrs[i - 1]))
                self.go(*anims, t=0.8)
            self.at(0.7)
            fail = T("one step fails  →  one disease", 34, PINK).next_to(steps, DOWN, buff=1.0)
            self.go(Write(fail), t=1.5)

        # b02 neutrophils -------------------------------------------------
        with self.beat("b02"):
            self.wipe()
            h = self.header("Neutrophils")
            self.go(Write(h), t=0.8)
            n = cell(1.3, BLUE).move_to(LEFT * 3.8 + DOWN * 0.3)
            self.go(Create(n), t=1.2)
            b1 = T("> 10¹¹ made per day", 36, YELLOW)
            b2 = T("G-CSF and GM-CSF", 36, CHALK)
            b2b = T("drive production", 32, CHALK)
            grp = VGroup(b1, b2, b2b).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 2.2 + DOWN * 0.3)
            b2b.shift(DOWN * 0.0)
            self.at(0.2)
            self.go(Write(b1), *self.tag("Abbas p.14"), t=1.5)
            self.at(0.55)
            self.go(Write(b2), t=1.2)
            self.go(FadeIn(b2b, shift=UP * 0.2), t=0.8)

        # b03 four steps of extravasation ---------------------------------
        with self.beat("b03"):
            self.wipe()
            h = self.header("Step 1: leave the blood")
            self.go(Write(h), t=0.8)
            self.vessel = build_vessel()
            lumen = T("blood (postcapillary venule)", 26, GREY).move_to([-3.6, 1.5, 0])
            tissue = T("tissue", 26, GREY).move_to([-5.7, -1.65, 0])
            self.go(LaggedStart(*[Create(c) for c in self.vessel], lag_ratio=0.1), FadeIn(lumen), FadeIn(tissue), t=1.5)
            self.lumen_lbl = lumen
            names = ["Rolling", "Activation", "Arrest", "Transmigration"]
            self.step_lbls = VGroup(*[
                VGroup(T(f"{i + 1}", 28, YELLOW), T(nm, 28, YELLOW)).arrange(RIGHT, buff=0.15).move_to([x, 2.35, 0])
                for i, (nm, x) in enumerate(zip(names, STEP_X))])
            for i, lbl in enumerate(self.step_lbls):
                self.at(0.25 + 0.17 * i)
                self.go(Write(lbl), t=0.9)
            self.go(*self.tag("Abbas p.49"), t=0.5)

        # b04 selectins ----------------------------------------------------
        with self.beat("b04"):
            top = ENDO_Y + 0.25
            pe = VGroup(*[selectin([x, top, 0]) for x in [-5.8, -5.3, -4.4, -3.9, -3.4]])
            self.go(FadeOut(self.lumen_lbl), *self.caption(["Selectins: first, low-affinity adhesion"]), t=1)
            self.at(0.35)
            self.go(LaggedStart(*[GrowFromPoint(s, s[0].get_start()) for s in pe], lag_ratio=0.2), t=1.2)
            pe_lbl = T("P- and E-selectin (endothelium)", 26, BLUE).move_to([-3.9, 0.3, 0])
            self.go(FadeIn(pe_lbl, shift=DOWN * 0.2), t=0.8)
            self.at(0.7)
            self.leuk = leukocyte().move_to([-5.6, 1.4, 0])
            l_lbl = T("L-selectin (leukocyte)", 26, BLUE).next_to(self.leuk, RIGHT, buff=0.3)
            self.go(FadeIn(self.leuk), t=0.8)
            self.go(Write(l_lbl), t=0.8)
            self.sel_lbls = VGroup(pe_lbl, l_lbl)
            self.selectins = pe
            self.go(*self.tag("Abbas p.44–45"), t=0.4)

        # b05 P- and E-selectin induction ---------------------------------
        with self.beat("b05"):
            self.go(FadeOut(self.sel_lbls), t=0.5)
            gran = Circle(0.13, color=YELLOW, stroke_width=3).set_fill(YELLOW, 0.4).move_to([-2.4, ENDO_Y - 0.05, 0])
            self.go(FadeIn(gran, scale=0.5), *self.caption(["P-selectin: stored in granules", "histamine, thrombin  →  fast to the surface"]), t=1)
            self.at(0.25)
            newp = selectin([-2.4, ENDO_Y + 0.25, 0], YELLOW)
            self.go(gran.animate.move_to([-2.4, ENDO_Y + 0.2, 0]).set_opacity(0), GrowFromPoint(newp, newp[0].get_start()), t=1.2)
            self.at(0.55)
            cyt = T("IL-1, TNF", 28, YELLOW).move_to([-1.3, 1.2, 0])
            e_new = VGroup(*[selectin([x, ENDO_Y + 0.25, 0], GREEN) for x in [-1.9, -1.4, -0.9]])
            ar = chalk_arrow(cyt, [-1.4, ENDO_Y + 0.75, 0], YELLOW)
            self.go(FadeIn(cyt), GrowArrow(ar), *self.caption(["E-selectin: made in 1–2 hours", "after IL-1 or TNF"]), t=1.2)
            self.go(LaggedStart(*[GrowFromPoint(s, s[0].get_start()) for s in e_new], lag_ratio=0.3), t=1.2)
            self.go(FadeOut(cyt), FadeOut(ar), t=0.6)
            self.selectins.add(newp, *e_new)

        # b06 rolling --------------------------------------------------------
        with self.beat("b06"):
            self.go(self.leuk.animate.move_to([-5.6, ENDO_Y + 0.25 + LEUK_R + 0.32, 0]), t=1)
            slx = T("sialyl Lewis X", 28, YELLOW).move_to([-5.0, 1.35, 0])
            self.go(Write(slx), *self.caption(["Ligand: sialyl Lewis X"]), t=1)
            self.at(0.35)
            self.go(*self.caption(["Low affinity + fast off-rate", "bonds form and break  →  the cell rolls"]), t=0.8)
            self.play(roll(self.leuk, 1.9, self.fit(self.remaining() - 1.0)), slx.animate.shift(RIGHT * 1.9), rate_func=linear)
            self.go(FadeOut(slx), t=0.5)

        # b07 integrin activation ------------------------------------------
        with self.beat("b07"):
            chem = VGroup(*[Dot([x, ENDO_Y + 0.3, 0], radius=0.07, color=YELLOW) for x in np.linspace(-2.6, -0.6, 6)])
            self.go(LaggedStart(*[FadeIn(d, scale=0.3) for d in chem], lag_ratio=0.15),
                    *self.caption(["Heparan sulfate shows chemokines", "to the rolling cell"]), t=1.2)
            self.play(roll(self.leuk, -1.55 - self.leuk.get_x(), self.fit(1.6)), rate_func=smooth)
            self.at(0.45)
            base = self.leuk.get_center() + DOWN * LEUK_R
            bent = VGroup(Line(base, base + RIGHT * 0.35 + DOWN * 0.12, color=ORANGE, stroke_width=5))
            straight = VGroup(Line(base, base + DOWN * 0.32, color=GREEN, stroke_width=5))
            ilbl = T("integrin", 26, CHALK).next_to(self.leuk, RIGHT, buff=0.35)
            self.go(Create(bent), FadeIn(ilbl), t=0.8)
            self.at(0.62)
            self.go(Transform(bent, straight), *self.caption(["Chemokine receptor signal  →  integrin high affinity", "= “inside-out” signalling"], YELLOW), t=1.2)
            self.go(Indicate(bent, color=GREEN), t=0.8)
            self.go(*self.tag("Abbas p.46–48"), t=0.4)
            self.integ = VGroup(bent, ilbl, chem)

        # b08 firm arrest ---------------------------------------------------
        with self.beat("b08"):
            self.go(FadeOut(self.integ), t=0.4)
            self.play(roll(self.leuk, 1.55 - self.leuk.get_x(), self.fit(1.6)), rate_func=smooth)
            self.go(self.leuk.animate.stretch(1.35, 0).stretch(0.75, 1).shift(DOWN * 0.1), t=0.8)
            self.at(0.3)
            pairs = VGroup(
                Tm(f'<span foreground="{BLUE}">LFA-1, MAC-1</span>  →  <span foreground="{YELLOW}">ICAM-1</span>', 30),
                Tm(f'<span foreground="{BLUE}">VLA-4</span>  →  <span foreground="{YELLOW}">VCAM-1</span>', 30),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([2.6, 1.0, 0])
            self.go(*self.caption(["Cytokines raise ICAM-1 and VCAM-1 on endothelium"]), t=0.8)
            self.at(0.5)
            self.go(Write(pairs[0]), t=1.2)
            self.at(0.7)
            self.go(Write(pairs[1]), t=1.0)
            self.go(*self.tag("Abbas p.49"), t=0.4)
            self.pairs = pairs

        # b09 transmigration -------------------------------------------------
        with self.beat("b09"):
            self.go(FadeOut(self.pairs), self.leuk.animate.stretch(1 / 1.35, 0).stretch(1 / 0.75, 1).shift(UP * 0.1), t=0.6)
            self.play(roll(self.leuk, 4.65 - self.leuk.get_x(), self.fit(1.4)), rate_func=smooth)
            c7, c8 = self.vessel[6], self.vessel[7]
            self.go(c7.animate.shift(LEFT * 0.22), c8.animate.shift(RIGHT * 0.22), t=0.8)
            cd31 = T("CD31", 28, YELLOW).move_to([3.5, -1.7, 0])
            self.go(FadeIn(cd31), *self.caption(["Squeezes between endothelial cells (CD31)"]), t=0.8)
            self.go(self.leuk.animate.stretch(0.6, 0).move_to([4.65, ENDO_Y, 0]), t=1.0)
            self.go(self.leuk.animate.stretch(1 / 0.6, 0).move_to([4.65, -2.0, 0]), t=1.0)
            self.go(c7.animate.shift(RIGHT * 0.22), c8.animate.shift(LEFT * 0.22), t=0.6)
            self.at(0.5)
            self.go(*self.caption(["“Diapedesis”:  Abbas = between endothelial cells",
                                   "Janeway = through the basement membrane"], PINK), t=1.0)
            self.go(*self.tag("Abbas p.49–50 · Janeway p.106"), t=0.4)

        # b10 chemotaxis -----------------------------------------------------
        with self.beat("b10"):
            self.wipe()
            h = self.header("Step 2: find the microbe")
            self.go(Write(h), t=0.8)
            rng = np.random.default_rng(3)
            dots = VGroup()
            for _ in range(140):
                x = 6.0 - 11.5 * np.sqrt(rng.random())  # denser near the right
                x = 6.0 - (6.0 - x) ** 1.0
                if rng.random() < (x + 6) / 12:
                    dots.add(Dot([x, rng.uniform(-1.6, 1.6), 0], radius=0.045, color=YELLOW).set_opacity(0.8))
            bug = VGroup(microbe(2.0), microbe(2.0).shift(UP * 0.5 + RIGHT * 0.2), microbe(2.0).shift(DOWN * 0.45 + LEFT * 0.1)).move_to([5.6, 0, 0])
            self.go(FadeIn(bug), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.01), t=1.5)
            n = cell(0.55, BLUE).move_to([-5.2, 0, 0])
            self.go(FadeIn(n), *self.caption(["Chemotaxis: movement up a chemoattractant gradient"]), t=0.8)
            self.go(n.animate.move_to([3.6, 0, 0]), t=min(4.0, self.remaining() * 0.45), rate_func=smooth)
            self.at(0.62)
            g = T("receptors = 7-transmembrane GPCRs", 30, YELLOW).move_to([0, 2.3, 0])
            self.go(Write(g), t=1.2)
            self.go(*self.tag("Abbas p.46–47"), t=0.4)

        # b11 neutrophil vs monocyte chemokines -----------------------------
        with self.beat("b11"):
            self.wipe()
            h = self.header("Who answers which signal")
            self.go(Write(h), t=0.8)
            n = cell(0.5, BLUE, label="neutrophil", size=24).move_to([-4.9, 1.3, 0])
            m = cell(0.5, BLUE, label="monocyte", size=24).move_to([-4.9, -1.2, 0])
            r1 = Tm(f'<span foreground="{BLUE}">CXCR1, CXCR2</span>  ←  <span foreground="{YELLOW}">CXCL8 (IL-8)</span>', 32).move_to([1.0, 1.55, 0])
            r2 = Tm(f'<span foreground="{BLUE}">CCR2</span>  ←  <span foreground="{YELLOW}">CCL2</span>', 32)
            r2.move_to([0, -0.95, 0]).align_to(r1, LEFT)
            self.go(FadeIn(n), t=0.6)
            self.go(Write(r1), t=1.5)
            self.at(0.55)
            self.go(FadeIn(m), t=0.6)
            self.go(Write(r2), t=1.2)
            self.go(*self.tag("Abbas p.50"), t=0.4)
            self.chem_rows = VGroup(n, m, r1, r2)

        # b12 other attractants + respiratory burst --------------------------
        with self.beat("b12"):
            self.go(self.chem_rows.animate.scale(0.75).move_to([-2.6, 1.0, 0]), t=0.8)
            others = VGroup(*[T(s, 30, YELLOW) for s in ["C5a", "C3a", "leukotriene B4"]]).arrange(RIGHT, buff=0.6)
            others.move_to([-1.6, -1.1, 0])
            self.go(LaggedStart(*[FadeIn(o, shift=UP * 0.2) for o in others], lag_ratio=0.3), t=1.5)
            self.at(0.3)
            fp = Tm(f'formyl peptides → <span foreground="{BLUE}">FPR1</span>  (among the most potent)', 30, color=YELLOW).move_to([-0.5, -2.0, 0])
            self.go(Write(fp), t=1.5)
            self.at(0.72)
            burst = label_box("respiratory burst", PINK, 30).move_to([4.6, 1.2, 0])
            a1 = chalk_arrow(others[0], burst, PINK)
            src = self.chem_rows[2]
            a2 = chalk_arrow(src, burst, PINK)
            self.go(FadeIn(burst), GrowArrow(a1), GrowArrow(a2), t=1.2)
            self.go(*self.tag("Abbas p.48, 79 · Janeway p.103"), t=0.4)

        # b13 phagocytosis + opsonization -----------------------------------
        with self.beat("b13"):
            self.wipe()
            h = self.header("Step 3: swallow")
            self.go(Write(h), t=0.8)
            ph = cell(1.4, BLUE, label="phagocyte", size=26).move_to([-3.8, -0.2, 0])
            bug = microbe(3.0).move_to([2.6, -0.2, 0])
            self.go(FadeIn(ph), FadeIn(bug), t=1.0)
            self.go(*self.caption(["Phagocytosis: active, needs energy", "particles > 0.5 µm"]), t=0.8)
            self.at(0.5)
            ops = VGroup(*[Dot(bug.point_at_angle(a), radius=0.09, color=GREEN) for a in np.linspace(0, TAU, 12, endpoint=False)])
            olbl = T("opsonins: antibody or complement", 28, GREEN).next_to(bug, UP, buff=0.5)
            self.go(LaggedStart(*[FadeIn(o, scale=0.3) for o in ops], lag_ratio=0.1), Write(olbl), t=1.5)
            self.at(0.8)
            self.go(VGroup(bug, ops).animate.move_to([-1.9, -0.2, 0]), *self.caption(["Coated microbe  →  taken up more readily"], GREEN), t=1.2)
            self.go(*self.tag("Abbas p.95 · Janeway p.49"), t=0.4)

        # b14 FcγRI and CR1 -------------------------------------------------
        with self.beat("b14"):
            self.wipe()
            h = self.header("Opsonin  →  receptor")
            self.go(Write(h), t=0.8)
            hd = VGroup(T("Receptor", 28, GREY), T("Binds", 28, GREY), T("Key point", 28, GREY))
            xs = [-4.3, -0.6, 3.2]
            for t_, x in zip(hd, xs):
                t_.move_to([x, 2.1, 0])
            line = Line([-6.2, 1.8, 0], [6.2, 1.8, 0], color=GREY, stroke_width=2)
            self.go(FadeIn(hd), Create(line), t=0.8)

            def row(cells_, y, colors):
                g = VGroup(*[T(c, 28, col) for c, col in zip(cells_, colors)])
                for t_, x in zip(g, xs):
                    t_.move_to([x, y, 0])
                return g
            self.r1 = row(["FcγRI (CD64)", "IgG1, IgG3", "high affinity"], 1.0, [BLUE, GREEN, CHALK])
            self.go(LaggedStart(*[Write(c) for c in self.r1], lag_ratio=0.4), t=2.0)
            self.at(0.4)
            self.r2 = row(["CR1 (CD35)", "C3b, C4b", "weak alone"], -0.1, [BLUE, GREEN, PINK])
            self.go(LaggedStart(*[Write(c) for c in self.r2], lag_ratio=0.4), t=2.0)
            self.at(0.72)
            helps = T("+ IgG or IFN-γ  →  works well", 26, GREEN).next_to(self.r2[2], DOWN, buff=0.2)
            self.go(FadeIn(helps, shift=UP * 0.2), t=1.0)
            self.r2.add(helps)
            self.go(*self.tag("Abbas p.297, 307, 313"), t=0.4)
            self.xs = xs

        # b15 CR3 = MAC-1 ----------------------------------------------------
        with self.beat("b15"):
            r3 = VGroup(T("CR3 (CD11b/CD18)", 28, BLUE), T("iC3b", 28, GREEN), T("enough alone", 28, GREEN))
            for t_, x in zip(r3, self.xs):
                t_.move_to([x, -1.4, 0])
            self.go(LaggedStart(*[Write(c) for c in r3], lag_ratio=0.4), t=2.0)
            self.at(0.35)
            eq = T("= MAC-1, the adhesion integrin", 30, YELLOW).move_to([-2.2, -2.3, 0])
            self.go(Write(eq), Circumscribe(r3[0], color=YELLOW), t=1.5)
            self.at(0.65)
            cd18 = Tm(f'β chain = <span foreground="{YELLOW}">CD18</span>  →  missing in <span foreground="{PINK}">LAD-1</span>', 30).move_to([-1.6, -2.95, 0])
            self.go(Write(cd18), t=1.4)
            self.go(*self.tag("Abbas p.45, 309 · Janeway p.64"), t=0.4)

        # b16 phagocytosis steps --------------------------------------------
        with self.beat("b16"):
            self.wipe()
            h = self.header("From binding to phagolysosome")
            self.go(Write(h), t=0.8)
            xs = [-5.0, -2.5, 0.0, 2.5, 5.0]
            y = 0.0
            # 1 bind
            mem = Line([-0.8, -0.35, 0], [0.8, -0.35, 0], color=BLUE, stroke_width=4)
            rec = VGroup(*[Line([x, -0.35, 0], [x, -0.12, 0], color=BLUE, stroke_width=3) for x in (-0.2, 0.2)])
            s1 = VGroup(mem, rec, microbe(1.6).move_to([0, 0.05, 0])).move_to([xs[0], y, 0])
            # 2 cup
            cup = Arc(radius=0.62, start_angle=150 * DEGREES, angle=240 * DEGREES, color=BLUE, stroke_width=4)
            s2 = VGroup(cup, microbe(1.6)).move_to([xs[1], y, 0])
            # 3 phagosome
            s3 = VGroup(Circle(0.6, color=BLUE, stroke_width=4), microbe(1.6)).move_to([xs[2], y, 0])
            # 4 + lysosome
            lyso = VGroup(Circle(0.28, color=YELLOW, stroke_width=3).set_fill(YELLOW, 0.2),
                          *[Dot([dx, dy, 0], radius=0.04, color=YELLOW) for dx, dy in [(-0.1, 0.05), (0.08, -0.06), (0.05, 0.1)]])
            s4 = VGroup(Circle(0.5, color=BLUE, stroke_width=4), microbe(1.3), lyso.shift(RIGHT * 0.75 + UP * 0.35)).move_to([xs[3], y, 0])
            # 5 phagolysosome
            s5 = VGroup(Circle(0.62, color=YELLOW, stroke_width=4).set_fill(YELLOW, 0.08),
                        DashedVMobject(microbe(1.6), num_dashes=10),
                        *[Dot([dx, dy, 0], radius=0.05, color=YELLOW) for dx, dy in [(-0.35, 0.25), (0.3, -0.3), (0.25, 0.32), (-0.3, -0.25)]]
                        ).move_to([xs[4], y, 0])
            labels = ["bind", "cup", "phagosome", "+ lysosome", "phago-\nlysosome"]
            lbls = VGroup(*[T(l, 28, YELLOW if i == 4 else CHALK).move_to([x, -1.3, 0]) for i, (l, x) in enumerate(zip(labels, xs))])
            lbls[4].shift(DOWN * 0.15)
            stages = [s1, s2, s3, s4, s5]
            arrs = VGroup(*[chalk_arrow([xs[i] + 0.85, y, 0], [xs[i + 1] - 0.85, y, 0], CHALK, buff=0.0, tip=0.18) for i in range(4)])
            fr = [0.12, 0.3, 0.45, 0.62, 0.8]
            for i, st in enumerate(stages):
                self.at(fr[i])
                anims = [FadeIn(st), FadeIn(lbls[i], shift=UP * 0.15)]
                if i:
                    anims.append(GrowArrow(arrs[i - 1]))
                self.go(*anims, t=0.9)
            note = T("most killing happens here", 28, GREEN).next_to(lbls[4], DOWN, buff=0.35).align_to(lbls[4], RIGHT)
            note.shift(LEFT * 0.0)
            if note.get_right()[0] > 6.4:
                note.shift(LEFT * (note.get_right()[0] - 6.4))
            self.go(Write(note), *self.tag("Abbas p.95"), t=1.0)

        # b17 three killing classes -----------------------------------------
        with self.beat("b17"):
            self.wipe()
            h = self.header("Step 4: kill")
            self.go(Write(h), t=0.8)
            boxes = VGroup(label_box("Reactive oxygen\nspecies (ROS)", YELLOW, 32, buff=0.32),
                           label_box("Nitric oxide", YELLOW, 32, buff=0.32),
                           label_box("Proteolytic\nenzymes", YELLOW, 32, buff=0.32)).arrange(RIGHT, buff=0.7).move_to(DOWN * 0.1)
            for i, b in enumerate(boxes):
                self.at(0.3 + 0.2 * i)
                self.go(GrowFromCenter(b), t=0.8)
            self.go(*self.tag("Abbas p.95–96"), t=0.4)

        # b18 NADPH oxidase assembly ----------------------------------------
        with self.beat("b18"):
            self.wipe()
            h = self.header("NADPH oxidase (phagocyte oxidase)")
            self.go(Write(h), t=1.0)
            memb = Line([-5.5, 1.0, 0], [5.5, 1.0, 0], color=BLUE, stroke_width=6)
            ml = T("granule membrane", 26, GREY).next_to(memb, UP, buff=0.15).align_to(memb, LEFT)
            cl = T("cytosol", 26, GREY).move_to([-5.0, -2.6, 0])
            self.go(Create(memb), FadeIn(ml), FadeIn(cl), t=1.0)
            self.at(0.3)
            gp91 = label_box("gp91", BLUE, 30).move_to([-0.7, 1.0, 0])
            p22 = label_box("p22", BLUE, 30).move_to([0.8, 1.0, 0])
            for b_ in (gp91, p22):
                b_[0].set_fill(BOARD, 1)
            self.go(FadeIn(gp91, shift=DOWN * 0.2), FadeIn(p22, shift=DOWN * 0.2), t=1.0)
            self.at(0.5)
            cyto = VGroup(*[label_box(s, BLUE, 30) for s in ["p40", "p47", "p67"]]).arrange(RIGHT, buff=1.4).move_to([0, -2.2, 0])
            self.go(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cyto], lag_ratio=0.3), t=1.2)
            self.at(0.75)
            rac = label_box("Rac2", YELLOW, 30).move_to([4.2, -0.6, 0])
            self.go(FadeIn(rac, scale=0.6), t=0.6)
            dock = VGroup(*[c.copy() for c in cyto]).arrange(RIGHT, buff=0.15).move_to([0.05, 0.15, 0])
            self.go(*[Transform(c, d) for c, d in zip(cyto, dock)], t=1.2)
            self.go(GrowArrow(chalk_arrow(rac, dock, YELLOW)), t=0.5)
            done = T("assembled  →  active", 28, GREEN).next_to(dock, DOWN, buff=0.35)
            self.go(FadeIn(done), Indicate(VGroup(gp91, p22, cyto), color=GREEN, scale_factor=1.05),
                    *self.tag("Abbas p.96 · Janeway p.80–81"), t=1.0)

        # b19 the chain -------------------------------------------------------
        with self.beat("b19"):
            self.wipe()
            h = self.header("The respiratory burst")
            self.go(Write(h), t=0.8)
            sp, arrs, enz, names = chain()
            grp = VGroup(sp, arrs, enz, names).shift(UP * 0.9)
            self.go(Write(sp[0]), FadeIn(names[0]), t=0.6)
            fr = [0.12, 0.45, 0.72]
            for i in range(3):
                self.at(fr[i])
                self.go(GrowArrow(arrs[i]), FadeIn(enz[i], shift=DOWN * 0.15), t=0.8)
                self.go(Write(sp[i + 1]), FadeIn(names[i + 1]), t=0.8)
            self.go(*self.tag("Abbas p.96 · Janeway p.81"), t=0.4)
            self.chain = grp

        # b20 why "burst"; K+ influx ------------------------------------------
        with self.beat("b20"):
            why = Tm(f'consumes O₂  →  “<span foreground="{YELLOW}">respiratory burst</span>”', 32).move_to([0, -1.0, 0])
            self.go(Write(why), t=1.4)
            self.at(0.3)
            pl = Circle(0.6, color=YELLOW, stroke_width=4).set_fill(YELLOW, 0.06).move_to([-4.6, -2.6, 0])
            ions = VGroup(T("K⁺", 28, BLUE), T("H⁺", 28, BLUE)).arrange(DOWN, buff=0.15).next_to(pl, LEFT, buff=0.5)
            self.go(Create(pl), FadeIn(ions), t=0.8)
            self.go(ions.animate.move_to(pl.get_center()).scale(0.8), t=1.0)
            res = T("releases + activates elastase, cathepsin G", 28, CHALK).next_to(pl, RIGHT, buff=0.5).shift(UP * 0.3)
            self.go(Write(res), t=1.4)
            self.at(0.78)
            jw = T("Janeway: ROS alone may not kill", 26, PINK).next_to(res, DOWN, buff=0.25).align_to(res, LEFT)
            self.go(FadeIn(jw), *self.tag("Abbas p.96 · Janeway p.81, 536"), t=0.8)

        # b21 nitric oxide ------------------------------------------------------
        with self.beat("b21"):
            self.wipe()
            h = self.header("Nitric oxide (NO)")
            self.go(Write(h), t=0.8)
            mac = cell(0.85, BLUE, label="macrophage", size=26).move_to([-5.0, 0.9, 0])
            self.go(FadeIn(mac), t=0.6)
            rest = T("resting: no iNOS", 28, GREY).move_to([0.4, 1.9, 0])
            self.go(FadeIn(rest), t=0.8)
            self.at(0.22)
            ind = Tm(f'<span foreground="{BLUE}">TLR</span> + <span foreground="{BLUE}">IFN-γ</span>  →  iNOS induced', 30, color=YELLOW).move_to([0.4, 1.9, 0])
            self.go(Transform(rest, ind), t=1.0)
            r2 = Tm(f'arginine  →  citrulline + <span foreground="{YELLOW}">NO</span>', 30).move_to([0.4, 0.7, 0])
            self.go(Write(r2), t=1.2)
            self.at(0.5)
            r3 = Tm(f'NO + O₂⁻ or H₂O₂  →  <span foreground="{YELLOW}">peroxynitrite</span>', 30).move_to([0.4, -0.5, 0])
            self.go(Write(r3), t=1.4)
            self.at(0.78)
            neu = cell(0.42, BLUE).move_to([-5.0, -2.1, 0])
            nl = T("Neutrophils: little or no NO", 30, PINK).next_to(neu, RIGHT, buff=0.4)
            self.go(FadeIn(neu), Write(nl), *self.tag("Abbas p.15, 96"), t=1.2)

        # b22 NETs ----------------------------------------------------------------
        with self.beat("b22"):
            self.wipe()
            h = self.header("Neutrophil extracellular traps (NETs)")
            self.go(Write(h), t=0.8)
            neu = cell(0.8, BLUE).move_to([-5.2, 0.0, 0])
            self.go(FadeIn(neu), t=0.6)
            strands = VGroup(*[
                ParametricFunction(lambda t, y0=y0, ph=ph: np.array([t, y0 + 0.18 * np.sin(3.2 * t + ph), 0]),
                                   t_range=[-4.4, 0.4], color=CHALK, stroke_width=2.5)
                for y0, ph in [(-1.2, 0), (-0.6, 1), (0, 2), (0.6, 3), (1.2, 4)]])
            self.go(LaggedStart(*[Create(s) for s in strands], lag_ratio=0.15), t=1.5)
            what = T("DNA + histones + granule proteins", 28, YELLOW).move_to([-2.3, 2.15, 0])
            self.go(FadeIn(what), t=0.8)
            self.at(0.3)
            caught = VGroup(*[microbe(0.8).move_to([x, y, 0]) for x, y in [(-2.8, 0.55), (-1.4, -0.65), (-0.6, 1.25), (-2.0, -1.2), (0.0, 0.0)]])
            self.go(LaggedStart(*[FadeIn(c, scale=0.4) for c in caught], lag_ratio=0.15),
                    *self.caption(["Trap and kill bacteria and fungi"]), t=1.2)
            self.at(0.5)
            need = VGroup(T("Needs:", 30, YELLOW),
                          bullet_list(["PAD4", "elastase", "myeloperoxidase", "phagocyte oxidase"], size=28)
                          ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.9, 0.1, 0])
            self.go(FadeIn(need[0]), t=0.4)
            self.go(LaggedStart(*[FadeIn(r, shift=LEFT * 0.2) for r in need[1]], lag_ratio=0.3), t=2.0)
            self.at(0.85)
            dies = T("neutrophil usually dies", 28, PINK).next_to(need, DOWN, buff=0.5).align_to(need, LEFT)
            self.go(neu.animate.set_opacity(0.3), Write(dies), *self.tag("Abbas p.96"), t=1.0)

        # b23 defect overview -------------------------------------------------------
        with self.beat("b23"):
            self.wipe()
            h = self.header("When a step fails", PINK)
            self.go(Write(h), t=0.8)
            inf = VGroup(T("Invasive bacterial + fungal infections", 30, PINK),
                         T("skin · liver · respiratory tract", 28, CHALK),
                         Tm(f'fungi: mainly <i>Aspergillus</i>, <i>Candida</i>', 28)).arrange(DOWN, buff=0.22).move_to([0, 1.5, 0])
            self.go(Write(inf[0]), t=1.2)
            self.go(FadeIn(inf[1]), t=0.6)
            self.at(0.3)
            self.go(FadeIn(inf[2]), t=0.8)
            self.at(0.55)
            jw = T("Janeway's four groups", 28, GREY).move_to([0, -0.2, 0])
            groups = VGroup(*[label_box(g, BLUE, 30) for g in ["Production", "Adhesion", "Activation", "Killing"]]
                            ).arrange(RIGHT, buff=0.45).move_to([0, -1.3, 0])
            self.go(FadeIn(jw), t=0.5)
            self.go(LaggedStart(*[GrowFromCenter(g) for g in groups], lag_ratio=0.3), t=2.0)
            self.go(*self.tag("Abbas p.486 · Janeway p.533"), t=0.4)

        # b24 CGD -------------------------------------------------------------------
        with self.beat("b24"):
            self.wipe()
            h = self.header("Chronic granulomatous disease (CGD)", PINK)
            self.go(Write(h), t=1.0)
            sp, arrs, enz, names = chain(36)
            grp = VGroup(sp, arrs, enz, names).scale(0.85).move_to([0, 1.5, 0])
            self.go(FadeIn(grp), t=0.8)
            self.at(0.15)
            x = xmark(arrs[0].get_center())
            self.go(Create(x), enz[0].animate.set_color(PINK), t=1.0)
            low = T("too little superoxide  →  microbes survive", 30, PINK).move_to([0, 0.0, 0])
            self.go(Write(low), t=1.2)
            self.at(0.55)
            pie_c = [-3.2, -2.1, 0]
            xl = Sector(radius=1.1, angle=240 * DEGREES, start_angle=90 * DEGREES, color=PINK, fill_opacity=0.45, stroke_width=0).move_arc_center_to(pie_c)
            ar = Sector(radius=1.1, angle=120 * DEGREES, start_angle=330 * DEGREES, color=BLUE, fill_opacity=0.35, stroke_width=0).move_arc_center_to(pie_c)
            self.go(GrowFromPoint(xl, pie_c), t=0.8)
            l1 = Tm(f'<span foreground="{PINK}">≈ 2/3 X-linked</span>  (gp91)', 30).move_to([1.4, -1.6, 0])
            self.go(Write(l1), t=1.0)
            self.at(0.8)
            self.go(GrowFromPoint(ar, pie_c), t=0.6)
            l2 = Tm(f'<span foreground="{BLUE}">rest autosomal recessive</span>  (can be milder)', 30).next_to(l1, DOWN, buff=0.35).align_to(l1, LEFT)
            if l2.get_right()[0] > 6.5:
                VGroup(l1, l2).shift(LEFT * (l2.get_right()[0] - 6.5))
            self.go(Write(l2), *self.tag("Abbas p.486 · Janeway p.82"), t=1.0)

        # b25 CGD organisms -----------------------------------------------------------
        with self.beat("b25"):
            self.wipe()
            h = self.header("CGD: what to look for", PINK)
            self.go(Write(h), t=0.8)
            r1 = Tm(f'<span foreground="{PINK}">Catalase-producing</span> organisms, e.g. <i>Staphylococcus</i>', 30).move_to([0, 1.8, 0])
            r1b = T("catalase destroys the little H₂O₂ that is left", 28, CHALK).next_to(r1, DOWN, buff=0.2)
            self.go(Write(r1), t=1.4)
            self.at(0.2)
            self.go(FadeIn(r1b, shift=UP * 0.2), t=0.8)
            self.at(0.5)
            r2 = Tm(f'<i>Aspergillus</i>: <span foreground="{PINK}">leading cause of death</span>', 30).move_to([0, 0.2, 0])
            self.go(Write(r2), t=1.2)
            self.at(0.72)
            gran_c = np.array([-3.6, -2.0, 0])
            gran = VGroup(*[Circle(0.32, color=BLUE, stroke_width=3).set_fill(BLUE, 0.15).move_to(gran_c + 0.62 * np.array([np.cos(a), np.sin(a), 0]))
                            for a in np.linspace(0, TAU, 8, endpoint=False)],
                          microbe(1.0).move_to(gran_c))
            gl = T("uncontrolled infection  →  granulomas", 30, YELLOW).next_to(gran, RIGHT, buff=0.5)
            self.go(LaggedStart(*[FadeIn(g) for g in gran], lag_ratio=0.1), Write(gl), *self.tag("Abbas p.487"), t=1.5)

        # b26 CGD management + MPO deficiency ----------------------------------------
        with self.beat("b26"):
            self.wipe()
            h = self.header("CGD management (Abbas)", ORANGE)
            self.go(Write(h), t=0.8)
            mg = bullet_list(["antibiotic + antifungal prophylaxis", "IFN-γ", "consider stem cell transplant (HSCT)"], size=32, color=ORANGE).move_to([0, 1.2, 0])
            self.go(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in mg], lag_ratio=0.5), t=2.5)
            self.at(0.42)
            chk = T("check the current guideline", 28, GREY).next_to(mg, DOWN, buff=0.35)
            self.go(FadeIn(chk), t=0.6)
            self.at(0.6)
            mpo = label_box("MPO deficiency: impaired killing, milder than CGD", PINK, 30).move_to([0, -1.8, 0])
            self.go(GrowFromCenter(mpo), *self.tag("Abbas p.487 · Janeway p.536"), t=1.2)

        # b27 LAD overview + LAD-1 -------------------------------------------------------
        with self.beat("b27"):
            self.wipe()
            h = self.header("Leukocyte adhesion deficiency (LAD)", PINK)
            self.go(Write(h), t=1.0)
            self.lad_steps = VGroup(*[label_box(s, BLUE, 28) for s in ["Rolling", "Activation", "Arrest", "Transmigration"]])
            for b, x in zip(self.lad_steps, STEP_X):
                b.move_to([x, 1.9, 0])
            arrs = VGroup(*[chalk_arrow(a, b, CHALK, buff=0.08, tip=0.16) for a, b in zip(self.lad_steps, self.lad_steps[1:])])
            self.go(LaggedStart(*[FadeIn(b) for b in self.lad_steps], lag_ratio=0.2), LaggedStart(*[GrowArrow(a) for a in arrs], lag_ratio=0.2), t=1.2)
            self.go(*self.caption(["Autosomal recessive · neutrophils never arrive · no pus"], PINK), t=1.0)
            self.at(0.45)
            lad1 = VGroup(T("LAD-1", 30, PINK), T("CD18:", 26, CHALK), T("β2 integrins", 26, CHALK), T("missing", 26, CHALK)).arrange(DOWN, buff=0.12).next_to(self.lad_steps[2], DOWN, buff=0.4)
            self.go(*block(self.lad_steps[2]), FadeIn(lad1, shift=UP * 0.2), t=1.2)
            self.at(0.75)
            lk = T("blood: leukocytosis", 26, YELLOW).next_to(lad1, DOWN, buff=0.25)
            self.go(Write(lk), *self.tag("Abbas p.488"), t=1.0)

        # b28 LAD-2, LAD-3 ------------------------------------------------------------
        with self.beat("b28"):
            lad2 = VGroup(T("LAD-2", 30, PINK), T("no sialyl", 26), T("Lewis X", 26), T("(GDP-fucose", 24, GREY), T("transporter)", 24, GREY)
                          ).arrange(DOWN, buff=0.1).next_to(self.lad_steps[0], DOWN, buff=0.4)
            self.go(*block(self.lad_steps[0]), FadeIn(lad2, shift=UP * 0.2), t=1.2)
            self.at(0.25)
            self.go(*self.caption(["LAD-2 clues: developmental problems, Bombay blood group"], YELLOW), t=1.0)
            self.at(0.55)
            lad3 = VGroup(T("LAD-3", 30, PINK), T("KINDLIN-3:", 26), T("integrin not", 26), T("activated", 26)
                          ).arrange(DOWN, buff=0.1).next_to(self.lad_steps[1], DOWN, buff=0.4)
            self.go(*block(self.lad_steps[1]), FadeIn(lad3, shift=UP * 0.2), t=1.2)
            self.at(0.78)
            self.go(*self.caption(["LAD-3 clue: bleeding with a normal platelet count"], YELLOW), t=1.0)

        # b29 Chediak-Higashi -------------------------------------------------------------
        with self.beat("b29"):
            self.wipe()
            h = self.header("Chédiak–Higashi syndrome (CHS)", PINK)
            self.go(Write(h), t=1.0)
            g = T("autosomal recessive · LYST gene", 30, YELLOW).move_to([0, 2.2, 0])
            self.go(Write(g), t=1.0)
            ph = VGroup(Circle(0.6, color=BLUE, stroke_width=4), microbe(1.6)).move_to([-4.3, 0.4, 0])
            ly = VGroup(Circle(0.35, color=YELLOW, stroke_width=3).set_fill(YELLOW, 0.2)).move_to([-1.9, 0.4, 0])
            phl = T("phagosome", 26).next_to(ph, DOWN, buff=0.2)
            lyl = T("lysosome", 26).next_to(ly, DOWN, buff=0.2).align_to(phl, DOWN)
            fa = chalk_arrow(ly, ph, PINK)
            nf = T("poor fusion", 26, PINK).next_to(fa, UP, buff=0.5)
            self.at(0.2)
            self.go(FadeIn(ph), FadeIn(ly), FadeIn(phl), FadeIn(lyl), t=0.8)
            self.go(GrowArrow(fa), t=0.6)
            self.go(FadeIn(nf), Create(xmark(fa.get_center())), t=0.6)
            self.go(ly.animate.scale(1.9), t=0.8)
            self.at(0.5)
            clues = bullet_list(["giant lysosomes", "partial albinism", "pyogenic infections", "HLH if no transplant"], size=30).move_to([3.0, -0.1, 0])
            for r in clues:
                self.go(FadeIn(r, shift=LEFT * 0.2), t=0.7)
                self.wait(min(0.6, max(0, self.remaining() - 1.5)))
            self.go(*self.tag("Abbas p.488 · Janeway p.536"), t=0.4)

        # b30 neutropenias --------------------------------------------------------------
        with self.beat("b30"):
            self.wipe()
            h = self.header("Production defects: neutropenia", PINK)
            self.go(Write(h), t=1.0)
            ax = Axes(x_range=[0, 63, 21], y_range=[0, 4.4, 1], x_length=7.0, y_length=3.6,
                      axis_config={"color": CHALK, "stroke_width": 3, "include_ticks": True, "include_numbers": False},
                      tips=False).move_to([-2.4, 0.0, 0])
            xl = T("days", 24, GREY).next_to(ax.x_axis, DOWN, buff=0.15).align_to(ax.x_axis, RIGHT)
            yl = T("neutrophils", 24, GREY).next_to(ax.y_axis, UP, buff=0.12)
            tick = VGroup(*[T(str(d), 22, GREY).next_to(ax.c2p(d, 0), DOWN, buff=0.15) for d in (21, 42)])
            self.go(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(tick), t=1.0)
            thr = DashedLine(ax.c2p(0, 0.5), ax.c2p(63, 0.5), color=YELLOW, stroke_width=3)
            thl = T("- - -  0.5 × 10⁹/L", 26, YELLOW).move_to([4.6, 2.0, 0])
            self.go(Create(thr), FadeIn(thl), t=0.8)
            scn = ax.plot(lambda d: 0.2, x_range=[0, 63], color=PINK, stroke_width=4)
            sl = T("SCN", 28, PINK).next_to(ax.c2p(63, 0.2), RIGHT, buff=0.15)
            self.go(Create(scn), FadeIn(sl), t=1.2)
            self.at(0.4)
            cyc = ax.plot(lambda d: 2.2 + 1.85 * np.cos(2 * PI * d / 21), x_range=[0, 63], color=BLUE, stroke_width=4)
            cl = T("cyclic: ~21 days", 28, BLUE).next_to(ax.c2p(31.5, 4.05), UP, buff=0.05)
            self.go(Create(cyc), FadeIn(cl), t=1.8)
            self.at(0.62)
            notes = VGroup(T("ELA2: most common", 28, CHALK), T("cause of SCN", 28, CHALK),
                           T("G-CSF = mainstay", 30, ORANGE)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.6, 0.0, 0])
            notes[2].shift(DOWN * 0.3)
            self.go(Write(notes[0]), FadeIn(notes[1]), t=1.2)
            self.at(0.85)
            self.go(Write(notes[2]), *self.tag("Janeway p.533–534"), t=1.0)

        # b31 recap ----------------------------------------------------------------------
        with self.beat("b31"):
            self.wipe()
            h = self.header("Five things to remember")
            self.go(Write(h), t=0.8)
            pts = [
                "Roll → activate → arrest → transmigrate",
                "CXCL8, C5a, formyl peptides attract neutrophils",
                "CR3 = MAC-1, binds iC3b",
                "NADPH oxidase → SOD → MPO",
                "CGD, LAD, CHS: each blocks one step",
            ]
            rows = VGroup(*[VGroup(T(f"{i + 1}", 32, YELLOW), T(p, 32, CHALK)).arrange(RIGHT, buff=0.35)
                            for i, p in enumerate(pts)]).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to(DOWN * 0.3)
            fr = [0.08, 0.27, 0.48, 0.62, 0.8]
            for r, f in zip(rows, fr):
                self.at(f)
                self.go(FadeIn(r, shift=RIGHT * 0.3), t=0.8)

        # b32 exam trap ------------------------------------------------------------------
        with self.beat("b32"):
            self.wipe()
            h = self.header("Exam trap", PINK)
            self.go(Write(h), t=0.8)
            wrong = T("MPO makes superoxide or H₂O₂", 36, CHALK).move_to([0, 1.8, 0])
            self.go(Write(wrong), t=1.2)
            sl_ = Line(wrong.get_left() + LEFT * 0.1, wrong.get_right() + RIGHT * 0.1, color=PINK, stroke_width=6)
            self.go(Create(sl_), wrong.animate.set_color(PINK), t=0.6)
            self.at(0.3)
            right = VGroup(
                Tm(f'<span foreground="{YELLOW}">NADPH oxidase</span>  →  superoxide', 32),
                Tm(f'<span foreground="{YELLOW}">SOD</span>  →  H₂O₂', 32),
                Tm(f'<span foreground="{YELLOW}">MPO</span>  →  hypohalous acid (HOCl)', 32),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, -0.1, 0])
            for r in right:
                self.go(FadeIn(r, shift=UP * 0.2), t=0.8)
            self.at(0.75)
            m = label_box("MPO deficiency is milder than CGD", GREEN, 30).move_to([0, -2.4, 0])
            self.go(GrowFromCenter(m), *self.tag("Abbas p.96 · Janeway p.536"), t=1.0)

        # b33 next -----------------------------------------------------------------------
        with self.beat("b33"):
            self.wipe()
            t = self.title_card("Next: Complement made easy", "3 pathways · 1 C3 convertase · opsonins")
            self.go(Write(t), t=2.5)

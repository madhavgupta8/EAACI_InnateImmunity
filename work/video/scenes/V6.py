from chalk import *
from chalk import _bbox_exit


# ---------- local helpers (V6 only) ----------
def fitw(m, w):
    if m.width > w:
        m.scale_to_fit_width(w)
    return m


def brake(a, b, color=GREEN, stroke=4):
    """Inhibition line from a to b, ending in a flat bar (⊣)."""
    ca, cb = a.get_center(), b.get_center()
    d = cb - ca
    start = _bbox_exit(a, d) + 0.12 * d / np.linalg.norm(d)
    end = _bbox_exit(b, -d) - 0.12 * d / np.linalg.norm(d)
    u = d / np.linalg.norm(d)
    n = np.array([-u[1], u[0], 0]) * 0.18
    return VGroup(Line(start, end, color=color, stroke_width=stroke),
                  Line(end - n, end + n, color=color, stroke_width=stroke + 2))


def xmark(mob, color=PINK, size=0.42, stroke=7):
    """Small knock-out cross on the upper-right corner (keeps the label readable)."""
    c = mob.get_corner(UR) + np.array([0.02, 0.02, 0])
    h = size / 2
    return VGroup(Line(c + np.array([-h, h, 0]), c + np.array([h, -h, 0]), color=color, stroke_width=stroke),
                  Line(c + np.array([-h, -h, 0]), c + np.array([h, h, 0]), color=color, stroke_width=stroke))


def knock(mob, color=PINK):
    """Dim a mobject and put a cross on it. Returns an AnimationGroup."""
    return AnimationGroup(mob.animate.set_opacity(0.45), Create(xmark(mob, color)))


def bacterium(color=PINK, w=1.3, h=0.7):
    e = Ellipse(width=w, height=h, color=color, stroke_width=4).set_fill(color, 0.15)
    return e


def guideline_tag():
    t = T("2017 guideline — check the current one", 22, ORANGE)
    return VGroup(chalk_box(t, ORANGE, 0.1, stroke=2), t).to_corner(DL, buff=0.3)


def cascade(x=-2.4):
    """Bradykinin pathway as a vertical column. Returns dict of named parts."""
    names = [("fxii", "Factor XII", BLUE), ("fxiia", "Factor XIIa", BLUE),
             ("kal", "Plasma kallikrein", BLUE), ("bk", "Bradykinin", YELLOW),
             ("b2", "B2 receptor", BLUE)]
    d = {}
    y = 2.25
    for k, txt, col in names:
        d[k] = label_box(txt, col, 28).move_to([x, y, 0])
        y -= 1.18
    d["arrows"] = VGroup(*[chalk_arrow(d[a], d[b], buff=0.08)
                           for a, b in [("fxii", "fxiia"), ("fxiia", "kal"), ("kal", "bk"), ("bk", "b2")]])
    d["surf"] = T("negative surface", 24, GREY).next_to(d["fxii"], LEFT, buff=0.35)
    d["prek"] = T("prekallikrein", 24, CHALK).next_to(d["arrows"][1], LEFT, buff=0.25)
    d["hmwk"] = T("HMWK", 24, CHALK).next_to(d["arrows"][2], LEFT, buff=0.25)
    d["leak"] = label_box("Leaky vessels → swelling", PINK, 28).next_to(d["b2"], RIGHT, buff=1.0)
    d["leak_arrow"] = chalk_arrow(d["b2"], d["leak"], PINK, buff=0.08)
    return d


class V6(ChalkScene):
    VIDEO_ID = "V6"

    def src(self, text):
        old = getattr(self, "_src", None)
        if old is not None and old in self.mobjects:
            self.remove(old)
        self._src = self.source_tag(text)
        self.add(self._src)

    def construct(self):
        # ---------------- intro ----------------
        with self.beat("b01"):
            t = self.title_card("Complement deficiencies & HAE", "Knock out one part → see the disease")
            self.play(Write(t[0]), run_time=self.fit(2.5))
            self.play(FadeIn(t[1], shift=UP * 0.2), Create(t[2]), run_time=self.fit(1.5))
            self.wait(self.remaining() * 0.6)
            self.play(t.animate.scale(0.8).set_opacity(0.5), run_time=self.fit(1))

        # ---------------- the rule ----------------
        with self.beat("b02"):
            self.clear_board()
            h = self.header("The rule: lost job → disease")
            self.play(Write(h), run_time=self.fit(1.2))
            jobs = [("Clear immune complexes", "SLE-like disease"),
                    ("Tag bacteria with C3b", "Pyogenic infections"),
                    ("Lyse bacteria (MAC)", "Neisseria infections")]
            rows = VGroup()
            for i, (j, dis) in enumerate(jobs):
                jb = label_box(j, GREEN, 30).move_to([-3.0, 1.5 - 1.75 * i, 0])
                db = label_box(dis, PINK, 30).move_to([3.4, 1.5 - 1.75 * i, 0])
                ar = chalk_arrow(jb, db)
                rows.add(VGroup(jb, ar, db))
            per = (self.bd * 0.55) / 3
            for r in rows:
                self.play(FadeIn(r[0], shift=RIGHT * 0.3), run_time=self.fit(per * 0.6))
            for r in rows:
                self.play(GrowArrow(r[1]), FadeIn(r[2], shift=LEFT * 0.3), run_time=self.fit(0.8))
            self.src("Janeway p.532 · Abbas p.315")
            self.rows = rows

        with self.beat("b03"):
            rows = self.rows
            tag = T("Analogy: a factory", 28, YELLOW).to_corner(UR, buff=0.4).shift(DOWN * 0.9)
            labels = VGroup(*[T(f"“{w}” gate", 24, YELLOW).next_to(r[0], DOWN, buff=0.12)
                              for w, r in zip(["waste disposal", "tagging", "shredder"], rows)])
            self.play(FadeIn(tag), run_time=self.fit(0.6))
            self.play(LaggedStart(*[Write(l) for l in labels], lag_ratio=0.4), run_time=self.fit(2.5))
            self.play(Indicate(rows[0], color=PINK), run_time=self.fit(1.5))
            self.wait(max(0.1, self.remaining() - 2.2))
            self.play(Indicate(rows[2], color=PINK), run_time=self.fit(1.5))

        # ---------------- early classical ----------------
        with self.beat("b04"):
            self.clear_board()
            h = self.header("Early classical pathway")
            self.play(Write(h), run_time=self.fit(1))
            names = ["C1q", "C1r", "C4", "C2", "C3"]
            chain = VGroup(*[label_box(n, BLUE, 36) for n in names]).arrange(RIGHT, buff=1.0).move_to(UP * 1.2)
            arrows = VGroup(*[chalk_arrow(a, b) for a, b in zip(chain, chain[1:])])
            self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.2) for c in chain], lag_ratio=0.3),
                      run_time=self.fit(2.5))
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.3), run_time=self.fit(1.5))
            self.wait(max(0.1, self.remaining() - 3.5))
            most = T("C2 deficiency = most common human complement deficiency", 30, YELLOW)
            fitw(most, 12).next_to(chain, DOWN, buff=0.7)
            self.play(Circumscribe(chain[3], color=YELLOW), Write(most), run_time=self.fit(2))
            self.src("Abbas p.315")
            self.chain, self.most = chain, most

        with self.beat("b05"):
            chain = self.chain
            self.play(FadeOut(self.most), run_time=self.fit(0.5))
            self.play(LaggedStart(*[knock(chain[i]) for i in (0, 3, 2)], lag_ratio=0.4), run_time=self.fit(1.8))
            sle = label_box("SLE in > 50%", PINK, 40).move_to(DOWN * 0.9)
            ars = VGroup(*[chalk_arrow(chain[i], sle, PINK) for i in (0, 3, 2)])
            self.play(*[GrowArrow(a) for a in ars], FadeIn(sle, scale=0.8), run_time=self.fit(2))
            self.wait(max(0.1, self.remaining() - 4.5))
            note = T("C2 or C4 deficiency: some have more infections, some have no symptoms", 26, CHALK)
            fitw(note, 12.4).move_to(DOWN * 2.5)
            self.play(Write(note), run_time=self.fit(2.5))

        with self.beat("b06"):
            self.clear_board()
            h = self.header("Why lupus?")
            self.play(Write(h), run_time=self.fit(0.8))
            # left: vessel wall with immune complexes
            wall_top = Line([-6.2, -0.4, 0], [-1.0, -0.4, 0], color=PINK, stroke_width=5)
            wall_bot = Line([-6.2, -1.9, 0], [-1.0, -1.9, 0], color=PINK, stroke_width=5)
            vlabel = T("vessel wall", 24, PINK).next_to(wall_bot, DOWN, buff=0.15)

            def ic():
                ag = Dot(radius=0.11, color=YELLOW)
                y1 = VGroup(Line(ORIGIN, UP * 0.25 + LEFT * 0.15), Line(ORIGIN, UP * 0.25 + RIGHT * 0.15),
                            Line(ORIGIN, DOWN * 0.25)).set_color(BLUE).set_stroke(width=3)
                return VGroup(y1.shift(DOWN * 0.22), ag)
            ics = VGroup(*[ic().move_to([-5.6 + 1.0 * i, 1.6, 0]) for i in range(5)])
            ic_lab = T("immune complexes", 26, YELLOW).move_to([-3.6, 2.4, 0])
            self.play(Create(wall_top), Create(wall_bot), FadeIn(vlabel), run_time=self.fit(1.2))
            self.play(FadeIn(ics), Write(ic_lab), run_time=self.fit(1.2))
            self.play(LaggedStart(*[m.animate.move_to([m.get_x(), -0.15, 0]) for m in ics], lag_ratio=0.15),
                      run_time=self.fit(2))
            infl = T("deposit → inflammation", 28, PINK).move_to([-3.6, -2.9, 0])
            self.play(Write(infl), wall_top.animate.set_stroke(width=9), run_time=self.fit(1.5))
            # right: apoptotic cell
            c = cell(0.75, BLUE).move_to([2.2, 1.1, 0])
            c_lab = T("apoptotic cell", 26, BLUE).next_to(c, UP, buff=0.15)
            self.play(FadeIn(c), Write(c_lab), run_time=self.fit(1))
            frags = VGroup(*[Circle(0.2, color=BLUE, stroke_width=3).set_fill(BLUE, 0.3)
                             .move_to(c.get_center() + 0.75 * np.array([np.cos(a), np.sin(a), 0]))
                             for a in np.linspace(0, TAU, 6, endpoint=False)])
            self.play(ReplacementTransform(c, frags), run_time=self.fit(1.2))
            na = label_box("nuclear antigens → lupus", PINK, 28).move_to([3.2, -1.3, 0])
            self.play(GrowArrow(chalk_arrow(frags, na, PINK)), FadeIn(na), run_time=self.fit(1.5))
            self.src("Abbas p.315 · Janeway p.532")

        # ---------------- C3 ----------------
        with self.beat("b07"):
            self.clear_board()
            h = self.header("C3: the hub of opsonization")
            self.play(Write(h), run_time=self.fit(0.8))
            bac = bacterium(w=1.8, h=1.0).move_to([2.0, 0.6, 0])
            tags = VGroup(*[Dot(radius=0.11, color=YELLOW).move_to(
                bac.get_center() + np.array([1.02 * np.cos(a), 0.62 * np.sin(a), 0]))
                for a in np.linspace(0, TAU, 8, endpoint=False)])
            tl = T("C3b tags", 26, YELLOW).next_to(bac, UP, buff=0.45)
            ph = cell(1.0, BLUE, label="phagocyte").move_to([-3.5, 0.6, 0])
            self.play(FadeIn(ph), FadeIn(bac), run_time=self.fit(1))
            self.play(LaggedStart(*[GrowFromCenter(d) for d in tags], lag_ratio=0.1), Write(tl),
                      run_time=self.fit(1.5))
            grab = chalk_arrow(ph, bac, GREEN)
            self.play(GrowArrow(grab), run_time=self.fit(0.8))
            bx = Square(0.5).move_to(grab.get_center())
            self.play(FadeOut(tags), FadeOut(tl), run_time=self.fit(0.8))
            self.play(grab.animate.set_opacity(0.4), Create(strike(bx)), run_time=self.fit(0.8))
            res = label_box("Severe pyogenic infections — can be fatal", PINK, 30).move_to(DOWN * 1.6)
            ex = T("e.g. Streptococcus pneumoniae", 26, PINK, slant=ITALIC).next_to(res, DOWN, buff=0.3)
            self.play(FadeIn(res, shift=UP * 0.2), run_time=self.fit(1.2))
            self.play(Write(ex), run_time=self.fit(1.2))
            self.src("Abbas p.315 · Janeway p.532")

        with self.beat("b08"):
            self.clear_board()
            h = self.header("Lectin pathway: MBL deficiency")
            self.play(Write(h), run_time=self.fit(0.8))
            pie = Circle(1.4, color=CHALK, stroke_width=3).set_fill(GREEN, 0.15).move_to([-3.2, -0.2, 0])
            sl = AnnularSector(inner_radius=0, outer_radius=1.4, angle=0.05 * TAU, start_angle=PI / 2,
                               color=PINK, fill_opacity=0.8).move_arc_center_to(pie.get_center())
            pl = T("≈ 5% of people", 32, PINK).next_to(pie, DOWN, buff=0.3)
            self.play(Create(pie), run_time=self.fit(1))
            self.play(FadeIn(sl), Write(pl), run_time=self.fit(1.5))
            items = bullet_list(["relatively common", "mild immunodeficiency",
                                 "more bacterial infections", "in early childhood"], 30)
            items.move_to([2.6, -0.2, 0])
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in items], lag_ratio=0.5),
                      run_time=self.fit(self.remaining() * 0.7))
            self.src("Janeway p.533")

        # ---------------- alternative + terminal ----------------
        with self.beat("b09"):
            self.clear_board()
            h = self.header("Alternative pathway → Neisseria")
            self.play(Write(h), run_time=self.fit(0.8))
            fb = label_box("Factor B — rare", BLUE, 30).move_to([-3.6, 1.6, 0])
            fd = label_box("Factor D — rare", BLUE, 30).move_to([-3.6, 0.0, 0])
            pr = label_box("Properdin — X-linked, more common", BLUE, 30).move_to([-2.6, -1.6, 0])
            nm = label_box("Meningococcal infection", PINK, 32).move_to([3.6, 1.0, 0])
            self.play(FadeIn(nm), run_time=self.fit(1.0))
            for b in (fb, fd):
                self.play(FadeIn(b, shift=RIGHT * 0.2), run_time=self.fit(0.6))
                self.play(knock(b), run_time=self.fit(0.6))
                self.play(GrowArrow(chalk_arrow(b, nm, PINK)), run_time=self.fit(0.6))
            self.wait(max(0.1, self.remaining() - 6))
            self.play(FadeIn(pr, shift=RIGHT * 0.2), run_time=self.fit(1.2))
            nmm = T("Neisseria meningitidis", 32, PINK, slant=ITALIC).move_to([3.6, -2.7, 0])
            self.play(knock(pr), GrowArrow(chalk_arrow(pr, nmm, PINK)), Write(nmm),
                      run_time=self.fit(2))
            self.src("Abbas p.315 · Janeway p.59")

        with self.beat("b10"):
            self.clear_board()
            h = self.header("Terminal components C5–C9")
            self.play(Write(h), run_time=self.fit(0.8))
            mem = Arc(radius=3.0, start_angle=PI * 0.62, angle=-PI * 0.24, color=PINK, stroke_width=8)
            mem.move_to([-3.0, 0.5, 0])
            ml = T("bacterial membrane", 24, PINK).next_to(mem, UP, buff=0.15)
            self.play(Create(mem), FadeIn(ml), run_time=self.fit(1))
            parts = VGroup()
            for i, n in enumerate(["C5", "C6", "C7", "C8", "C9"]):
                p = label_box(n, BLUE, 28).move_to([-5.2 + 1.1 * i, -0.8, 0])
                parts.add(p)
            self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.4) for p in parts], lag_ratio=0.3),
                      run_time=self.fit(2.2))
            mac = T("MAC pore", 30, YELLOW).next_to(parts, DOWN, buff=0.3)
            self.play(Write(mac), parts.animate.shift(UP * 0.5), run_time=self.fit(1))
            self.play(knock(parts), run_time=self.fit(1))
            ne = label_box("Disseminated Neisseria infection", PINK, 30).move_to([3.4, -0.3, 0])
            only = T("the only consistent problem", 26, CHALK).next_to(ne, DOWN, buff=0.3)
            self.play(GrowArrow(chalk_arrow(parts, ne, PINK)), FadeIn(ne), run_time=self.fit(1.5))
            self.play(Write(only), run_time=self.fit(1.2))
            thin = T("thin-walled bacteria need lysis", 26, YELLOW).next_to(only, DOWN, buff=0.4)
            self.play(Write(thin), run_time=self.fit(1.5))
            self.src("Abbas p.315 · Janeway p.532")

        with self.beat("b11"):
            self.clear_board()
            h = self.header("How big is the risk?")
            self.play(Write(h), run_time=self.fit(0.8))
            a = VGroup(T("1 in 200", 60, PINK), T("MAC deficiency", 28, CHALK)).arrange(DOWN, buff=0.3)
            b = VGroup(T("1 in 2,000,000", 60, GREEN), T("normal people", 28, CHALK)).arrange(DOWN, buff=0.3)
            a.move_to([-3.3, 0.6, 0]); b.move_to([3.3, 0.6, 0])
            yr = T("yearly meningococcal risk · Japanese study", 26, GREY).move_to(UP * 2.3)
            self.play(FadeIn(yr), run_time=self.fit(0.8))
            self.play(Write(a), run_time=self.fit(1.5))
            self.play(Write(b), run_time=self.fit(1.5))
            k = T("≈ 10,000-fold higher", 40, YELLOW).move_to(DOWN * 1.8)
            self.play(Write(k), Circumscribe(a[0], color=YELLOW), run_time=self.fit(1.8))
            self.src("Janeway p.533")

        # ---------------- regulators ----------------
        with self.beat("b12"):
            self.clear_board()
            h = self.header("Regulators are the brakes")
            self.play(Write(h), run_time=self.fit(0.8))
            fi = label_box("Factor I", GREEN, 34).move_to([-4.6, 1.5, 0])
            self.play(FadeIn(fi), run_time=self.fit(0.7))
            self.play(knock(fi), run_time=self.fit(0.8))
            steps = [("fluid-phase C3 convertase runs free", PINK),
                     ("plasma C3 is used up", PINK),
                     ("de facto C3 deficiency", YELLOW),
                     ("pyogenic infections", PINK)]
            prev = fi
            mobs = VGroup()
            for i, (s, col) in enumerate(steps):
                m = T(s, 30, col).move_to([1.2, 1.5 - 1.15 * i, 0])
                ar = chalk_arrow(prev, m, CHALK, buff=0.1)
                self.play(GrowArrow(ar), Write(m), run_time=self.fit(self.bd * 0.16))
                mobs.add(m)
                prev = m
            self.src("Abbas p.315 · Janeway p.533")

        with self.beat("b13"):
            self.clear_board()
            h = self.header("Factor H and C3 nephritic factor")
            self.play(Write(h), run_time=self.fit(0.8))
            conv = label_box("C3bBb (alternative C3 convertase)", BLUE, 30).move_to([0, 1.7, 0])
            fh = label_box("Factor H", GREEN, 30).move_to([-4.3, 0.1, 0])
            br = brake(fh, conv)
            self.play(FadeIn(conv), run_time=self.fit(0.8))
            self.play(FadeIn(fh), Create(br), run_time=self.fit(1.2))
            only = T("alternative pathway only", 24, GREEN).next_to(fh, DOWN, buff=0.2)
            self.play(Write(only), run_time=self.fit(1))
            self.play(knock(fh), FadeOut(br), run_time=self.fit(1))
            res = bullet_list(["excess activation", "C3 consumption", "glomerulonephritis"], 28, PINK)
            res.next_to(only, DOWN, buff=0.4).align_to(only, LEFT)
            self.play(LaggedStart(*[FadeIn(r) for r in res], lag_ratio=0.4), run_time=self.fit(2.5))
            self.wait(max(0.1, self.remaining() - 3.5))
            nef = label_box("C3NeF autoantibody:\nshields C3bBb from factor H", PINK, 28).move_to([3.0, -1.0, 0])
            self.play(FadeIn(nef, shift=LEFT * 0.3), run_time=self.fit(1.5))
            self.play(GrowArrow(chalk_arrow(nef, conv, PINK)), run_time=self.fit(1))
            self.src("Abbas p.311, p.315")

        with self.beat("b14"):
            self.clear_board()
            h = self.header("aHUS: regulators fail on endothelium")
            self.play(Write(h), run_time=self.fit(0.8))
            regs = VGroup(*[label_box(n, GREEN, 30) for n in ["Factor H", "MCP", "Factor I"]])
            regs.arrange(DOWN, buff=0.45).move_to([-4.3, 0.3, 0])
            self.play(LaggedStart(*[FadeIn(r) for r in regs], lag_ratio=0.3), run_time=self.fit(1.5))
            self.play(LaggedStart(*[knock(r) for r in regs], lag_ratio=0.3), run_time=self.fit(1.2))
            ah = label_box("aHUS", PINK, 44).move_to([0.0, 0.3, 0])
            self.play(*[GrowArrow(chalk_arrow(r, ah, PINK)) for r in regs], FadeIn(ah), run_time=self.fit(1.5))
            het = T("heterozygous is enough", 26, YELLOW).next_to(ah, DOWN, buff=0.35)
            self.play(Write(het), run_time=self.fit(1.2))
            self.wait(max(0.1, self.remaining() - 5))
            tri = bullet_list(["haemolytic anaemia", "low platelets", "acute renal failure"], 30, PINK)
            tri.move_to([4.4, 0.3, 0])
            self.play(LaggedStart(*[FadeIn(r, shift=LEFT * 0.2) for r in tri], lag_ratio=0.5),
                      run_time=self.fit(3))
            self.src("Abbas p.315 · Janeway p.70")

        with self.beat("b15"):
            self.clear_board()
            h = self.header("PNH: the anchor is missing")
            self.h15 = h
            self.play(Write(h), run_time=self.fit(0.8))
            rbc = Circle(1.6, color=PINK, stroke_width=5).set_fill(PINK, 0.12).move_to([-3.0, -0.3, 0])
            rl = T("red cell", 26, PINK).next_to(rbc, DOWN, buff=0.2)
            self.play(Create(rbc), FadeIn(rl), run_time=self.fit(1))
            anchors = VGroup()
            for ang, name in [(PI * 0.75, "CD59"), (PI * 0.25, "DAF")]:
                p = rbc.get_center() + 1.6 * np.array([np.cos(ang), np.sin(ang), 0])
                u = np.array([np.cos(ang), np.sin(ang), 0])
                stick = Line(p, p + 0.5 * u, color=GREEN, stroke_width=4)
                head = Dot(p + 0.6 * u, radius=0.12, color=GREEN)
                lab = T(name, 26, GREEN).next_to(head, u, buff=0.12)
                anchors.add(VGroup(stick, head, lab))
            gpi = T("GPI anchors", 26, GREEN).move_to([1.2, 1.9, 0])
            self.play(LaggedStart(*[Create(a) for a in anchors], lag_ratio=0.4), Write(gpi), run_time=self.fit(2))
            self.wait(max(0.1, self.remaining() * 0.25))
            pig = label_box("PIG-A mutation", PINK, 30).move_to([2.6, 0.5, 0])
            self.play(FadeIn(pig, shift=LEFT * 0.3), knock(gpi), run_time=self.fit(1.2))
            self.play(FadeOut(anchors, shift=UP * 0.3), run_time=self.fit(1))
            pores = VGroup(*[Circle(0.16, color=YELLOW, stroke_width=4).set_fill(BOARD, 1).move_to(
                rbc.get_center() + r * np.array([np.cos(a), np.sin(a), 0]))
                for r, a in [(0.6, 0.3), (1.0, 2.2), (0.4, 3.9), (1.1, 5.0), (1.2, 1.0)]])
            mac = T("MAC forms on own cells", 28, YELLOW).move_to([2.6, -1.0, 0])
            self.play(LaggedStart(*[GrowFromCenter(p) for p in pores], lag_ratio=0.2), Write(mac),
                      run_time=self.fit(2))
            self.src("Abbas p.312, p.315")
            self.rbc = VGroup(rbc, rl, pores)

        with self.beat("b16"):
            keep = [self.rbc[0], self.rbc[1], *self.rbc[2], self.h15]
            others = [m for m in self.mobjects if not isinstance(m, ImageMobject) and m not in keep]
            self.play(*[FadeOut(m) for m in others], run_time=self.fit(0.6))
            items = bullet_list(["intravascular haemolysis", "chronic haemolytic anaemia", "venous thrombosis"],
                                30, PINK).move_to([2.6, 1.6, 0])
            self.play(LaggedStart(*[FadeIn(r, shift=LEFT * 0.2) for r in items], lag_ratio=0.5),
                      run_time=self.fit(3))
            stamp = label_box("acquired somatic mutation — NOT inherited", YELLOW, 28)
            fitw(stamp, 7.0).move_to([2.6, -0.5, 0])
            self.play(FadeIn(stamp, scale=1.3), run_time=self.fit(1))
            self.play(Indicate(stamp, color=YELLOW), run_time=self.fit(1.2))
            self.wait(max(0.1, self.remaining() - 3.5))
            ac5 = label_box("anti-C5 antibodies: PNH, aHUS", ORANGE, 28).move_to([2.6, -2.2, 0])
            self.play(FadeIn(ac5, shift=UP * 0.2), run_time=self.fit(1.2))
            self.src("Abbas p.312, p.316")

        # ---------------- HAE ----------------
        with self.beat("b17"):
            self.clear_board()
            h = self.header("C1 inhibitor (C1-INH): a serpin")
            self.play(Write(h), run_time=self.fit(1))
            hub = label_box("C1-INH", GREEN, 40).move_to([0, -0.2, 0])
            self.play(FadeIn(hub, scale=0.8), run_time=self.fit(1))
            targets = [("C1r", [-4.6, 1.6]), ("C1s", [-4.6, -0.2]), ("MASP1 / MASP2", [-4.0, -2.0]),
                       ("Plasma kallikrein", [4.0, 1.6]), ("Factor XIIa", [4.3, -1.2])]
            tb = VGroup(*[label_box(n, BLUE, 30).move_to([x, y, 0]) for n, (x, y) in targets])
            lines = VGroup(*[brake(hub, t) for t in tb])
            self.wait(max(0.1, self.remaining() * 0.15))
            for t, l in zip(tb, lines):
                self.play(FadeIn(t), Create(l), run_time=self.fit(self.bd * 0.1))
            comp = T("complement", 24, GREY).move_to([-4.6, 2.4, 0])
            kin = T("contact / kinin system", 24, GREY).move_to([4.0, 2.4, 0])
            self.play(FadeIn(comp), FadeIn(kin), run_time=self.fit(0.8))
            self.src("HAE-GL p.6 · Abbas p.311")

        with self.beat("b18"):
            self.clear_board()
            h = self.header("HAE type 1 and 2: genetics")
            self.play(Write(h), run_time=self.fit(0.8))

            def person(male, affected):
                s = Square(0.6) if male else Circle(0.3)
                s.set_stroke(CHALK, 3).set_fill(PINK if affected else BOARD, 0.9 if affected else 0)
                return s
            g1 = VGroup(person(True, True), person(False, False)).arrange(RIGHT, buff=1.2).move_to([-3.6, 1.6, 0])
            g2 = VGroup(*[person(m, a) for m, a in [(True, True), (False, False), (False, True), (True, False)]])
            g2.arrange(RIGHT, buff=0.6).move_to([-3.6, -0.2, 0])
            mate = Line(g1[0].get_right(), g1[1].get_left(), color=CHALK, stroke_width=3)
            drop = Line(mate.get_center(), [mate.get_center()[0], 0.7, 0], color=CHALK, stroke_width=3)
            bar = Line([g2[0].get_x(), 0.7, 0], [g2[-1].get_x(), 0.7, 0], color=CHALK, stroke_width=3)
            kids = VGroup(*[Line([k.get_x(), 0.7, 0], k.get_top(), color=CHALK, stroke_width=3) for k in g2])
            self.play(FadeIn(g1), Create(mate), run_time=self.fit(1))
            self.play(Create(drop), Create(bar), Create(kids), FadeIn(g2), run_time=self.fit(1.5))
            ad = T("autosomal dominant", 30, YELLOW).next_to(g2, DOWN, buff=0.5)
            self.play(Write(ad), run_time=self.fit(1))
            facts = bullet_list(["about 1 in 50,000 people", "> 450 SERPING1 mutations", "20–25%: new (de novo) mutation"], 30)
            facts.move_to([3.0, 0.5, 0])
            for r in facts:
                self.play(FadeIn(r, shift=LEFT * 0.2), run_time=self.fit(self.bd * 0.12))
                self.wait(min(1.2, max(0.1, self.remaining() - 3)))
            self.src("HAE-GL p.6 (2017)")

        with self.beat("b19"):
            self.clear_board()
            h = self.header("The bradykinin pathway")
            self.play(Write(h), run_time=self.fit(0.8))
            cs = cascade()
            self.cs = cs
            self.play(FadeIn(cs["fxii"]), FadeIn(cs["surf"]), run_time=self.fit(1.2))
            self.wait(max(0.1, self.bd * 0.12))
            self.play(GrowArrow(cs["arrows"][0]), FadeIn(cs["fxiia"]), run_time=self.fit(1.2))
            self.play(GrowArrow(cs["arrows"][1]), FadeIn(cs["prek"]), FadeIn(cs["kal"]), run_time=self.fit(1.5))
            self.wait(max(0.1, self.bd * 0.12))
            self.play(GrowArrow(cs["arrows"][2]), FadeIn(cs["hmwk"]), FadeIn(cs["bk"]), run_time=self.fit(1.5))
            self.play(Indicate(cs["bk"], color=YELLOW), run_time=self.fit(1))
            self.src("HAE-GL p.6")

        with self.beat("b20"):
            cs = self.cs
            self.play(GrowArrow(cs["arrows"][3]), FadeIn(cs["b2"]), run_time=self.fit(1))
            self.play(GrowArrow(cs["leak_arrow"]), FadeIn(cs["leak"]), run_time=self.fit(1.2))
            ace = label_box("ACE: breaks it down", GREEN, 26).move_to([2.6, cs["bk"].get_y(), 0])
            self.play(FadeIn(ace), GrowArrow(chalk_arrow(ace, cs["bk"], GREEN)), run_time=self.fit(1.2))
            inh = label_box("C1-INH", GREEN, 32).move_to([2.6, 1.65, 0])
            b1, b2 = brake(inh, cs["fxiia"]), brake(inh, cs["kal"])
            self.play(FadeIn(inh), Create(b1), Create(b2), run_time=self.fit(1.5))
            self.wait(max(0.1, self.remaining() - 3))
            self.play(knock(inh), FadeOut(b1), FadeOut(b2), run_time=self.fit(1))
            self.play(Indicate(cs["bk"], color=YELLOW, scale_factor=1.15), Indicate(cs["leak"], color=PINK),
                      run_time=self.fit(1.5))
            self.src("HAE-GL p.6")

        with self.beat("b21"):
            self.clear_board()
            h = self.header("Two effects of the missing brake")
            self.play(Write(h), run_time=self.fit(0.8))
            bk = label_box("Bradykinin = primary mediator of swelling", YELLOW, 32).move_to(UP * 1.4)
            self.play(FadeIn(bk, scale=0.9), run_time=self.fit(1.5))
            self.wait(max(0.1, self.remaining() * 0.3))
            c1 = label_box("C1 (no brake)", BLUE, 30).move_to([-4.2, -1.2, 0])
            c42 = label_box("C4, C2 cleaved", BLUE, 30).move_to([0, -1.2, 0])
            low = label_box("C4 ↓", PINK, 40).move_to([4.2, -1.2, 0])
            self.play(FadeIn(c1), run_time=self.fit(0.8))
            self.play(GrowArrow(chalk_arrow(c1, c42)), FadeIn(c42), run_time=self.fit(1.2))
            self.play(GrowArrow(chalk_arrow(c42, low, PINK)), FadeIn(low, scale=1.2), run_time=self.fit(1.2))
            self.src("HAE-GL p.6 · Janeway p.67 · Abbas p.311")

        with self.beat("b22"):
            self.clear_board()
            h = self.header("Histamine or bradykinin?")
            self.play(Write(h), run_time=self.fit(0.8))
            lh = VGroup(T("Mast cell angioedema", 32, BLUE), T("histamine", 30, CHALK)).arrange(DOWN, buff=0.3)
            rh = VGroup(T("HAE", 32, PINK), T("bradykinin → B2", 30, CHALK)).arrange(DOWN, buff=0.3)
            lh.move_to([-3.4, 1.6, 0]); rh.move_to([3.4, 1.6, 0])
            div = DashedLine(UP * 2.5, DOWN * 3.0, color=GREY)
            self.play(Create(div), FadeIn(lh), run_time=self.fit(1.2))
            self.play(FadeIn(rh), run_time=self.fit(1.2))
            drugs = ["antihistamines", "glucocorticoids", "epinephrine"]
            ld = bullet_list(drugs, 30, GREEN).move_to([-3.4, -1.0, 0])
            rd = bullet_list(drugs, 30, CHALK).move_to([3.4, -1.0, 0])
            self.play(FadeIn(ld), run_time=self.fit(1.2))
            self.play(FadeIn(rd), run_time=self.fit(1.2))
            self.play(LaggedStart(*[knock(r[1]) for r in rd], lag_ratio=0.3), run_time=self.fit(1.5))
            nr = T("no response → suspect HAE", 28, PINK).next_to(rd, DOWN, buff=0.4)
            self.play(Write(nr), run_time=self.fit(1.2))
            self.src("HAE-GL p.5–6")

        with self.beat("b23"):
            self.clear_board()
            h = self.header("When to suspect HAE")
            self.play(Write(h), run_time=self.fit(0.8))
            items = bullet_list(["recurrent angioedema, no wheals", "family history", "onset in childhood",
                                 "painful abdominal attacks", "upper airway swelling", "prodromal signs"], 30)
            items.move_to([-2.4, -0.1, 0])
            per = (self.bd * 0.55) / len(items)
            for r in items:
                self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=self.fit(per))
            side = VGroup(T("median onset ≈ 12 y", 30, YELLOW),
                          T("no family history", 28, PINK), T("in up to 25%", 28, PINK)).arrange(DOWN, buff=0.25)
            side.move_to([4.0, 0.3, 0])
            self.play(Write(side[0]), run_time=self.fit(1))
            self.play(FadeIn(side[1:]), run_time=self.fit(1))
            self.src("HAE-GL p.6, p.10")

        with self.beat("b24"):
            self.clear_board()
            h = self.header("Triggers")
            self.play(Write(h), run_time=self.fit(0.8))
            items = bullet_list(["dental or surgical trauma", "oestrogens", "stress and fatigue", "febrile illness"], 30)
            items.move_to([-3.0, 0.2, 0])
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in items], lag_ratio=0.5),
                      run_time=self.fit(self.bd * 0.45))
            ace = label_box("ACE inhibitors", PINK, 36).move_to([3.4, 0.6, 0])
            av = T("avoid strictly", 32, PINK).next_to(ace, DOWN, buff=0.35)
            self.play(FadeIn(ace, scale=1.2), run_time=self.fit(1))
            self.play(knock(ace), Write(av), run_time=self.fit(1.3))
            self.src("HAE-GL p.14")

        # ---------------- labs ----------------
        with self.beat("b25"):
            self.clear_board()
            h = self.header("Lab work-up (Rec. 1)")
            self.play(Write(h), run_time=self.fit(0.8))
            tests = VGroup(*[label_box(n, GREEN, 32) for n in ["C1-INH function", "C1-INH protein", "C4"]])
            tests.arrange(RIGHT, buff=0.6).move_to(UP * 1.3)
            self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.3) for t in tests], lag_ratio=0.4),
                      run_time=self.fit(self.bd * 0.3))
            rep = T("repeat any low result", 30, YELLOW).next_to(tests, DOWN, buff=0.5)
            self.play(Write(rep), run_time=self.fit(1.2))
            self.wait(max(0.1, self.remaining() - 3.5))
            nh = label_box("C3, CH50", GREY, 32).move_to([-2.0, -1.8, 0])
            nl = T("usually normal — not helpful", 28, GREY).next_to(nh, RIGHT, buff=0.4)
            self.play(FadeIn(nh), run_time=self.fit(0.8))
            self.play(knock(nh, GREY), Write(nl), run_time=self.fit(1.4))
            self.src("HAE-GL p.6–7")

        with self.beat("b26"):
            self.clear_board()
            h = self.header("Read the pattern")
            self.play(Write(h), run_time=self.fit(0.8))
            xs = [-4.4, -1.1, 1.3, 3.3, 5.1]
            ys = [2.3, 1.45, 0.65, -0.15, -0.95]
            heads = VGroup(*[T(t, 28, YELLOW).move_to([x, ys[0], 0]) for t, x in
                             zip(["", "Function", "Protein", "C4", "C1q"], xs)])
            line = Line([-6.4, 1.9, 0], [6.2, 1.9, 0], color=CHALK, stroke_width=2)
            self.play(FadeIn(heads), Create(line), run_time=self.fit(1))

            def row(i, name, vals, col=CHALK):
                cells = [T(name, 28, col).move_to([xs[0], ys[i], 0])]
                for v, x in zip(vals, xs[1:]):
                    c = PINK if "↓" in v else (GREEN if v.startswith("N") else CHALK)
                    cells.append(T(v, 30, c).move_to([x, ys[i], 0]))
                return VGroup(*cells)
            r1 = row(1, "HAE-1 (≈85%)", ["↓", "↓", "↓", "N"])
            r2 = row(2, "HAE-2", ["↓", "N or ↑", "↓", "N"])
            self.play(LaggedStart(*[FadeIn(c) for c in r1], lag_ratio=0.25), run_time=self.fit(self.bd * 0.3))
            self.play(LaggedStart(*[FadeIn(c) for c in r2], lag_ratio=0.25), run_time=self.fit(self.bd * 0.3))
            note = T("C4: usually low, but not specific", 26, GREY).move_to([0, -2.4, 0])
            self.play(Write(note), Indicate(VGroup(r1[3], r2[3])), run_time=self.fit(1.5))
            self.src("HAE-GL p.5–7")
            self.table = VGroup(heads, line, r1, r2)
            self.row, self.ys, self.xs, self.note = row, ys, xs, note

        with self.beat("b27"):
            self.play(FadeOut(self.note), run_time=self.fit(0.5))
            r3 = self.row(3, "AAE-C1-INH", ["↓", "↓", "↓", "↓ 75%"], PINK)
            self.play(LaggedStart(*[FadeIn(c) for c in r3], lag_ratio=0.25), run_time=self.fit(2))
            self.play(Circumscribe(r3[4], color=YELLOW), run_time=self.fit(1.2))
            note = bullet_list(["new angioedema after age 40, no family history", "look for lymphoma or MGUS"], 26)
            note.move_to([0, -2.3, 0])
            self.play(LaggedStart(*[FadeIn(r) for r in note], lag_ratio=0.5), run_time=self.fit(2.5))
            self.note = note
            self.src("HAE-GL p.7")

        with self.beat("b28"):
            self.play(FadeOut(self.note), run_time=self.fit(0.5))
            r4 = self.row(4, "HAE nC1-INH", ["N", "N", "–", "–"], BLUE)
            self.play(LaggedStart(*[FadeIn(c) for c in r4], lag_ratio=0.25), run_time=self.fit(2))
            note = bullet_list(["very rare; looks like HAE-1/2", "some: factor XII mutation; most: none found",
                                "ACE inhibitor angioedema: C1-INH normal too"], 26)
            note.move_to([0, -2.55, 0])
            for r in note:
                self.play(FadeIn(r, shift=UP * 0.1), run_time=self.fit(self.bd * 0.14))
                self.wait(min(1.5, max(0.1, self.remaining() - 4)))
            self.src("HAE-GL p.6")

        # ---------------- treatment (volatile) ----------------
        with self.beat("b29"):
            self.clear_board()
            t1 = T("Treatment follows the 2017", 40, ORANGE)
            t2 = T("WAO/EAACI guideline", 40, ORANGE)
            t3 = T("HAE-1/2 only", 32, CHALK)
            t4 = T("Drugs and licences change.", 34, YELLOW)
            t5 = T("Check the current guideline before the exam.", 34, YELLOW)
            g = VGroup(t1, t2, t3, t4, t5).arrange(DOWN, buff=0.3)
            box = chalk_box(g, ORANGE, 0.45, stroke=5)
            bang = VGroup(Circle(0.4, color=ORANGE, stroke_width=5), T("!", 48, ORANGE)).next_to(box, UP, buff=0.2)
            VGroup(bang, box, g).move_to(ORIGIN)
            self.play(Create(box), FadeIn(bang, scale=1.4), run_time=self.fit(1.2))
            self.play(Write(t1), Write(t2), run_time=self.fit(2.2))
            self.play(FadeIn(t3), run_time=self.fit(0.8))
            self.wait(max(0.1, self.remaining() - 4))
            self.play(Write(t4), run_time=self.fit(1.2))
            self.play(Write(t5), run_time=self.fit(1.5))
            self.src("HAE-GL p.6")

        with self.beat("b30"):
            self.clear_board()
            gt = guideline_tag()
            h = self.header("On-demand treatment (2017)", ORANGE)
            self.play(Write(h), FadeIn(gt), run_time=self.fit(1))
            rules = bullet_list(["treat as early as possible", "always treat airway attacks"], 30)
            rules.move_to([0, 1.7, 0])
            self.play(LaggedStart(*[FadeIn(r) for r in rules], lag_ratio=0.5), run_time=self.fit(2.2))
            first = label_box("C1-INH  ·  ecallantide  ·  icatibant", ORANGE, 32).move_to([0, 0.35, 0])
            sdp = label_box("solvent detergent-treated plasma", ORANGE, 28).move_to([0, -1.3, 0])
            ffp = label_box("fresh frozen plasma", ORANGE, 28).move_to([0, -2.6, 0])
            self.play(FadeIn(first, scale=0.9), run_time=self.fit(1.5))
            self.wait(max(0.1, self.remaining() - 4.5))
            n1 = T("if none", 24, GREY).next_to(sdp, LEFT, buff=0.5)
            self.play(GrowArrow(chalk_arrow(first, sdp, buff=0.04)), FadeIn(sdp), FadeIn(n1), run_time=self.fit(1.5))
            n2 = T("then", 24, GREY).next_to(ffp, LEFT, buff=0.5)
            self.play(GrowArrow(chalk_arrow(sdp, ffp, buff=0.04)), FadeIn(ffp), FadeIn(n2), run_time=self.fit(1.5))
            self.src("HAE-GL p.7–8 (2017)")

        with self.beat("b31"):
            self.clear_board()
            gt = guideline_tag()
            h = self.header("Where the drugs act (2017)", ORANGE)
            cs = cascade(x=-1.6)
            parts = VGroup(cs["fxii"], cs["fxiia"], cs["kal"], cs["bk"], cs["b2"], cs["arrows"],
                           cs["prek"], cs["hmwk"])
            self.play(FadeIn(h), FadeIn(gt), FadeIn(parts), run_time=self.fit(1.2))
            d1 = label_box("C1-INH concentrate: replaces it", ORANGE, 26).move_to([3.6, 1.65, 0])
            fitw(d1, 5.4)
            b1, b2 = brake(d1, cs["fxiia"], ORANGE), brake(d1, cs["kal"], ORANGE)
            self.play(FadeIn(d1), Create(b1), Create(b2), run_time=self.fit(2))
            self.wait(max(0.1, self.bd * 0.12))
            d2 = label_box("Ecallantide", ORANGE, 26).move_to([3.6, cs["bk"].get_y() + 0.1, 0])
            self.play(FadeIn(d2), Create(brake(d2, cs["kal"], ORANGE)), run_time=self.fit(1.5))
            self.wait(max(0.1, self.bd * 0.08))
            d3 = label_box("Icatibant", ORANGE, 26).move_to([3.6, cs["b2"].get_y() - 0.1, 0])
            self.play(FadeIn(d3), Create(brake(d3, cs["b2"], ORANGE)), run_time=self.fit(1.5))
            self.src("HAE-GL p.8 (2017)")

        with self.beat("b32"):
            self.clear_board()
            gt = guideline_tag()
            h = self.header("Attack rules (2017)", ORANGE)
            self.play(Write(h), FadeIn(gt), run_time=self.fit(0.8))
            no = VGroup(*[label_box(n, GREY, 30) for n in ["tranexamic acid", "androgens"]]).arrange(RIGHT, buff=0.8)
            no.move_to(UP * 1.5)
            nt = T("do not work for attacks", 28, PINK).next_to(no, DOWN, buff=0.3)
            self.play(FadeIn(no), run_time=self.fit(0.8))
            self.play(*[knock(n) for n in no], Write(nt), run_time=self.fit(1.5))
            air = label_box("progressive airway swelling → consider intubation early", PINK, 28).move_to(DOWN * 0.6)
            fitw(air, 12)
            self.play(FadeIn(air, shift=UP * 0.2), run_time=self.fit(1.5))
            self.wait(max(0.1, self.remaining() - 2.5))
            two = label_box("carry medication for 2 attacks", ORANGE, 30).move_to(DOWN * 2.1)
            self.play(FadeIn(two, shift=UP * 0.2), run_time=self.fit(1.2))
            self.src("HAE-GL p.8 (2017)")

        with self.beat("b33"):
            self.clear_board()
            gt = guideline_tag()
            h = self.header("Prophylaxis (2017)", ORANGE)
            self.play(Write(h), FadeIn(gt), run_time=self.fit(0.8))
            rows = [("Before procedures", "C1-INH concentrate", ORANGE),
                    ("Long-term, 1st line", "C1-INH", ORANGE),
                    ("Long-term, 2nd line", "androgens", ORANGE),
                    ("Not recommended", "antifibrinolytics", GREY)]
            g = VGroup()
            for i, (a, b, col) in enumerate(rows):
                la = T(a, 30, YELLOW).move_to([-3.2, 1.6 - 1.1 * i, 0])
                lb = label_box(b, col, 30).move_to([2.6, 1.6 - 1.1 * i, 0])
                g.add(VGroup(la, lb))
            for i, r in enumerate(g):
                self.play(FadeIn(r[0]), FadeIn(r[1], shift=LEFT * 0.2), run_time=self.fit(self.bd * 0.12))
                if i == 0:
                    self.wait(max(0.1, self.bd * 0.12))
            self.play(knock(g[3][1]), run_time=self.fit(0.8))
            self.src("HAE-GL p.9–10 (2017)")

        with self.beat("b34"):
            self.clear_board()
            gt = guideline_tag()
            h = self.header("Children and pregnancy (2017)", ORANGE)
            self.play(Write(h), FadeIn(gt), run_time=self.fit(0.8))
            ch = VGroup(T("Children < 12", 34, BLUE),
                        bullet_list(["attacks: C1-INH", "no androgens before Tanner V"], 28))
            ch.arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to([-3.3, 0.4, 0])
            pg = VGroup(T("Pregnancy", 34, BLUE),
                        bullet_list(["C1-INH preferred", "androgens contraindicated"], 28))
            pg.arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to([3.2, 0.4, 0])
            div = DashedLine(UP * 2.3, DOWN * 2.3, color=GREY)
            self.play(Create(div), FadeIn(ch[0]), run_time=self.fit(0.8))
            self.play(LaggedStart(*[FadeIn(r) for r in ch[1]], lag_ratio=0.4), run_time=self.fit(self.bd * 0.35))
            self.play(FadeIn(pg[0]), run_time=self.fit(0.8))
            self.play(LaggedStart(*[FadeIn(r) for r in pg[1]], lag_ratio=0.5), run_time=self.fit(2.5))
            self.src("HAE-GL p.11–13 (2017)")

        # ---------------- recap + trap ----------------
        with self.beat("b35"):
            self.clear_board()
            h = self.header("Five things to remember")
            self.play(Write(h), run_time=self.fit(1))
            items = ["Early classical defects → lupus-like disease",
                     "C3 or factor I loss → pyogenic infections",
                     "C5–C9, properdin loss → Neisseria",
                     "HAE = bradykinin, not histamine",
                     "Test C1-INH function, protein and C4"]
            rows = VGroup(*[VGroup(T(f"{i + 1}.", 32, YELLOW), T(s, 32)).arrange(RIGHT, buff=0.3)
                            for i, s in enumerate(items)]).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
            rows.move_to(DOWN * 0.3)
            fitw(rows, 12.4)
            self.wait(min(1.5, self.remaining() * 0.08))
            per = (self.remaining() - 1.0) / 5
            for r in rows:
                self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=self.fit(min(1.2, per)))
                self.wait(max(0.1, per - 1.2))
            self.src("Abbas p.315 · Janeway p.532 · HAE-GL p.6")

        with self.beat("b36"):
            self.clear_board()
            h = self.header("Exam trap", PINK)
            self.play(Write(h), run_time=self.fit(0.8))
            t1 = T("Normal C1-INH level and function", 36, CHALK)
            t2 = T("do NOT exclude HAE", 40, PINK)
            t3 = T("Family history → think HAE with normal C1-INH", 30, YELLOW)
            g = VGroup(t1, t2, t3).arrange(DOWN, buff=0.45).move_to(UP * 0.5)
            fitw(g, 12)
            self.play(Write(t1), run_time=self.fit(1.8))
            self.play(Write(t2), run_time=self.fit(1.5))
            self.play(FadeIn(t3, shift=UP * 0.2), run_time=self.fit(1.5))
            self.src("HAE-GL p.6")
            self.wait(max(0.1, self.remaining() - 3))
            nxt = T("Next: 10-minute rapid review", 34, GREEN).move_to(DOWN * 2.4)
            self.play(Write(nxt), run_time=self.fit(1.5))

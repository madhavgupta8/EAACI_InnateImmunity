from chalk import *

class V0(ChalkScene):
    VIDEO_ID = "V0"
    def construct(self):
        with self.beat("b01"):
            t = self.title_card("Complement made easy", "Pilot render")
            self.play(Write(t), run_time=self.fit(2.5))
        with self.beat("b02"):
            self.clear_board()
            nodes = VGroup(*[label_box(x, c) for x, c in [("C1", BLUE), ("C4", YELLOW), ("C3", PINK)]]).arrange(RIGHT, buff=1.4)
            self.play(FadeIn(nodes[0]))
            for a, b in zip(nodes, nodes[1:]):
                self.play(GrowArrow(chalk_arrow(a, b)), FadeIn(b), run_time=self.fit(1))
            self.add(self.source_tag("Janeway p.49"))

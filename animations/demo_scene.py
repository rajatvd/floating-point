import manim as mn
from manim_revealjs import PresentationScene, COMPLETE_LOOP


mn.config.video_dir = "./videos"


class DemoScene(PresentationScene):
    def construct(self):
        rect = mn.Rectangle(fill_color=mn.RED, fill_opacity=1)
        self.play(mn.Create(rect))
        self.end_fragment()

        self.play(rect.animate.shift(mn.UP).rotate(mn.PI / 3))
        self.end_fragment()

        self.play(rect.animate.shift(3 * mn.LEFT))
        self.end_fragment()

        self.play(rect.animate.shift(3 * mn.RIGHT))
        self.end_fragment()

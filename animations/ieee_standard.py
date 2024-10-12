from manim import *
from manim.utils.parameter_parsing import T
from manim_revealjs import PresentationScene, COMPLETE_LOOP
import os
from globals import (
    REAL_COLOR,
    ABS_COLOR,
    REL_COLOR,
    ARROW_COLOR,
    make_error_interval,
    update_error_interval,
    STROKE_WIDTH,
    value_to_error,
    round_to_nearest,
    FONT,
)

import numpy as np

# get absolute path of this python file
file_path = os.path.realpath(__file__)
dir_path = os.path.dirname(file_path)
# config.renderer = "opengl"

config.video_dir = os.path.join(dir_path, "videos")
config.media_dir = os.path.join(dir_path, "media")
config.flush_cache = False
config.disable_caching = False
relative_frame_size = np.array((11, 6))
resolution = 38
# resolution = 30
config.pixel_width = int(relative_frame_size[0] * resolution)
config.pixel_height = int(relative_frame_size[1] * resolution)
config.frame_width = 26
# config.frame_size = tuple(relative_frame_size * resolution)
# config.quality = "production_quality"
# config.quality = "low_quality"

# set background color to white
config.background_color = "#FFFFFF"


text_scale = 2


def to_scientific_notation(x: str):
    if "." in x:
        x = x.rstrip("0")
        first_non_zero = x.find("1")
        e = x.find(".") - first_non_zero
        e = e if e < 0 else e - 1
        m = x[first_non_zero + 1 :].replace(".", "")
        return m, e

    else:
        first_non_zero = x.find("1")
        e = len(x) - first_non_zero - 1
        m = x[first_non_zero + 1 :]
        return m, e


MANTISSA_COLOR = "#FF1313"
SIGN_COLOR = "#0077FF"
EXPONENT_COLOR = "#109910"
IGNORE_COLOR = "#999999"
DEFAULT_COLOR = "#000000"


# %%
class IEEE(PresentationScene):
    def construct(self):
        with register_font("Montserrat.ttf"):

            x = "1000.101"

            m, e = to_scientific_notation(x)
            m_padded = m + "0" * max(23 - len(m), 0)
            e_binary = bin(e + 127)[2:]
            e_binary_padded = "0" * max(8 - len(e_binary), 0) + e_binary
            binary_127 = bin(127)[2:]
            binary_127_padded = "0" * max(8 - len(binary_127), 0) + binary_127

            shift = 1.2
            original = MathTex(x, color=DEFAULT_COLOR).scale(text_scale)
            original.to_edge(UP)
            original.to_edge(LEFT)
            original.shift(RIGHT * shift)

            def below_and_shift(m, ref):
                m.next_to(ref, DOWN)
                m.to_edge(LEFT)
                m.shift(RIGHT * shift)

            scientific = MathTex(
                f"1.",
                f"{m}",
                " \\times 2^",
                e,
            ).scale(text_scale)
            scientific[0].set_color(DEFAULT_COLOR)
            scientific[1].set_color(MANTISSA_COLOR)
            scientific[2].set_color(DEFAULT_COLOR)
            scientific[3].set_color(EXPONENT_COLOR)
            # move scientific notation to the bottom of original
            below_and_shift(scientific, original)

            scientific_with_shifted_exponent = MathTex(
                f"1.{m} \\times 2^",
                f"{{{e+127} - 127}}",
            ).scale(text_scale)
            scientific_with_shifted_exponent[0].set_color(DEFAULT_COLOR)
            scientific_with_shifted_exponent[1].set_color(EXPONENT_COLOR)
            below_and_shift(scientific_with_shifted_exponent, original)

            binary_exponent = MathTex(
                f"1.{m} \\times 2^{{",
                f"{e_binary_padded}_2",
                f" - {binary_127_padded}_2",
                "}",
            ).scale(text_scale)
            binary_exponent[0].set_color(DEFAULT_COLOR)
            binary_exponent[1].set_color(EXPONENT_COLOR)
            binary_exponent[2].set_color(IGNORE_COLOR)
            binary_exponent_grp = VGroup(
                binary_exponent[1],
                binary_exponent[2],
            )

            below_and_shift(binary_exponent, original)

            pre_log = MathTex(
                "(",
                "1 + 0.",
                f"{m}",
                ")",
                " \\times 2^{",
                f"{e_binary_padded}_2",
                f" - {binary_127_padded}_2",
                "}",
            ).scale(text_scale)
            pre_log[0].set_color(DEFAULT_COLOR)
            pre_log[1].set_color(IGNORE_COLOR)
            pre_log[2].set_color(MANTISSA_COLOR)
            pre_log[3].set_color(DEFAULT_COLOR)
            pre_log[4].set_color(DEFAULT_COLOR)
            pre_log[5].set_color(EXPONENT_COLOR)
            pre_log[6].set_color(IGNORE_COLOR)
            below_and_shift(pre_log, original)

            pre_log_exp = VGroup(
                pre_log[3],
                pre_log[4],
                pre_log[5],
                pre_log[6],
            )

            pre_log_binary = MathTex(
                "(",
                "1 + 0.",
                f"{m_padded}",
                ")",
                " \\times 2^{",
                f"{e_binary_padded}_2",
                f" - {binary_127_padded}_2",
                "}",
            ).scale(text_scale)
            pre_log_binary[0].set_color(DEFAULT_COLOR)
            pre_log_binary[1].set_color(IGNORE_COLOR)
            pre_log_binary[2].set_color(MANTISSA_COLOR)
            pre_log_binary[3].set_color(DEFAULT_COLOR)
            pre_log_binary[4].set_color(DEFAULT_COLOR)
            pre_log_binary[5].set_color(EXPONENT_COLOR)
            pre_log_binary[6].set_color(IGNORE_COLOR)
            below_and_shift(pre_log_binary, original)

            pre_log_binary_exp = VGroup(
                pre_log_binary[3],
                pre_log_binary[4],
                pre_log_binary[5],
                pre_log_binary[6],
            )

            post_log = MathTex(
                "0.",
                f"{m_padded}",
                "+",
                f"{e_binary_padded}",
                f" - {binary_127_padded}",
            ).scale(text_scale)
            post_log[0].set_color(IGNORE_COLOR)
            post_log[1].set_color(MANTISSA_COLOR)
            post_log[2].set_color(DEFAULT_COLOR)
            post_log[3].set_color(EXPONENT_COLOR)
            post_log[4].set_color(IGNORE_COLOR)
            post_log.next_to(pre_log_binary, DOWN)

            ieee = MathTex(
                r"0 \ \ ",
                e_binary_padded,
                r" \ . \ ",
                m_padded,
            ).scale(text_scale)
            ieee[0].set_color(SIGN_COLOR)
            ieee[1].set_color(EXPONENT_COLOR)
            ieee[2].set_color(IGNORE_COLOR)
            ieee[3].set_color(MANTISSA_COLOR)
            ieee.next_to(post_log, DOWN)

            # add boxes around each section of the binary number, with transparent fill
            buff = 0.2
            ieee_boxes = VGroup(
                SurroundingRectangle(
                    ieee[0],
                    color=SIGN_COLOR,
                    fill_opacity=0.1,
                    buff=buff,
                ),
                SurroundingRectangle(
                    ieee[1],
                    color=EXPONENT_COLOR,
                    fill_opacity=0.1,
                    buff=buff,
                ),
                SurroundingRectangle(
                    ieee[3],
                    color=MANTISSA_COLOR,
                    fill_opacity=0.1,
                    buff=buff,
                ),
            )
            self.add(ieee_boxes)

            # add labels below each section of the binary number with braces
            ieee_labels = VGroup(
                Text("1 sign bit", font=FONT).scale(text_scale / 2),
                Text("8 exponent bits", font=FONT).scale(text_scale / 2),
                Text("23 mantissa bits", font=FONT).scale(text_scale / 2),
            )
            ieee_labels[0].set_color(SIGN_COLOR)
            ieee_labels[1].set_color(EXPONENT_COLOR)
            ieee_labels[2].set_color(MANTISSA_COLOR)

            ieee_braces = VGroup(
                Brace(ieee[1], DOWN, color=EXPONENT_COLOR),
                Brace(ieee[3], DOWN, color=MANTISSA_COLOR),
            )

            ieee_labels[0].next_to(ieee[0], LEFT)
            ieee_labels[1].next_to(ieee_braces[0], DOWN)
            ieee_labels[2].next_to(ieee_braces[1], DOWN)

            self.play(FadeIn(original))
            self.play(FadeIn(scientific))
            self.wait(1)
            self.play(Transform(scientific[-1], scientific_with_shifted_exponent[-1]))
            self.wait(1)
            self.play(
                Transform(
                    scientific[-1],
                    binary_exponent_grp,
                    replace_mobject_with_target_in_scene=True,
                )
            )
            self.wait(1)
            exp_part = Group(scientific[-2], binary_exponent_grp)
            self.play(
                exp_part.animate.move_to(
                    Group(
                        pre_log[4],
                        pre_log[5],
                        pre_log[6],
                    )
                ),
                TransformMatchingTex(
                    Group(scientific[0], scientific[1]),
                    Group(pre_log[0], pre_log[1], pre_log[2], pre_log[3]),
                    replace_mobject_with_target_in_scene=True,
                ),
            )
            self.wait(1)
            self.wait(1)
            self.play(Group(exp_part, pre_log[3]).animate.move_to(pre_log_binary_exp))
            self.wait(1)
            self.play(
                FadeIn(pre_log_binary[2]),
                FadeOut(pre_log[2]),
            )
            self.wait(1)
            self.add(post_log)
            self.add(ieee)
            self.add(ieee_braces)
            self.add(ieee_labels)
            self.wait(10)

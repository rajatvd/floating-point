from manim import *
from manim.utils.color.X11 import DARKGREEN
from manim_revealjs import PresentationScene, COMPLETE_LOOP
import os

# get absolute path of this python file
file_path = os.path.realpath(__file__)
dir_path = os.path.dirname(file_path)

config.video_dir = os.path.join(dir_path, "videos")
config.media_dir = os.path.join(dir_path, "media")
config.flush_cache = False
config.disable_caching = False
# config.quality = "medium_quality"
config.quality = "production_quality"

REAL_COLOR = DARKGREEN  # dark green
NEUTRAL_COLOR = "#000000"
# NEUTRAL_COLOR = "#FFFFFF"
ARROW_COLOR = "#0000FF"
COMPUTER_COLOR = "#FF0000"

# set background color to white
config.background_color = "#FFFFFF"


def myround(x, base, places_to_round):
    out = round(x / base, ndigits=places_to_round + 1) * base
    # convert x to base base

    # print(f"rounding {x} to {out}")
    return out


class RoundOff(PresentationScene):
    def construct(self):

        base = 10
        assert base == 10, "base must be 10 for now"
        places_to_round = 1
        tick_diff = base**-places_to_round
        count = 3
        center = tick_diff * count
        x_range = [center - count * tick_diff, center + count * tick_diff, tick_diff]
        unit_length = 1.3

        stroke_width = 4
        vertical_shift = 1.2
        horizontal_shift = 2
        number_shift_factor = 2.3

        # create a number line with shade of REAL_COLOR and have a real number next to it with the same color, have a marker on the number line. Vary the number and move the marker accordingly
        # have the number be to the left of the number line
        number_line = NumberLine(
            x_range=x_range,
            color=REAL_COLOR,
            include_numbers=True,
            stroke_width=stroke_width,
            unit_size=unit_length / tick_diff,
            decimal_number_config={
                "color": REAL_COLOR,
                "num_decimal_places": places_to_round,
                "show_ellipsis": False,
            },
            label_direction=UP,
        )
        number_line.move_to(UP * vertical_shift + RIGHT * horizontal_shift)
        marker = Dot(
            number_line.n2p(center),
            color=REAL_COLOR,
            radius=0.1,
        )
        number = DecimalNumber(
            0,
            color=REAL_COLOR,
            show_ellipsis=True,
            num_decimal_places=places_to_round + 2,
        )
        number.move_to(
            UP * vertical_shift + LEFT * number_shift_factor * horizontal_shift,
            aligned_edge=LEFT,
        )
        number.add_updater(lambda m: m.set_value(number_line.p2n(marker.get_center())))
        # add another pair of number line and number,
        # but this time the number is rounded number
        # and the number line is colored with COMPUTER_COLOR and
        # only has the ticks from the previous number line, without the line in between
        number_line_rounded = NumberLine(
            x_range=x_range,
            color=COMPUTER_COLOR,
            include_numbers=True,
            stroke_width=0,
            unit_size=unit_length / tick_diff,
            decimal_number_config={
                "color": COMPUTER_COLOR,
                "num_decimal_places": places_to_round,
                "show_ellipsis": False,
            },
        )
        # make number line only have ticks
        number_line_rounded.ticks.set_stroke(width=stroke_width)
        number_line_rounded.move_to(DOWN * vertical_shift + RIGHT * horizontal_shift)
        number_rounded = DecimalNumber(
            0,
            color=COMPUTER_COLOR,
            show_ellipsis=False,
            num_decimal_places=places_to_round,
        )
        number_rounded.move_to(
            DOWN * vertical_shift + LEFT * number_shift_factor * horizontal_shift,
            aligned_edge=LEFT,
        )
        marker_rounded = Dot(
            number_line_rounded.n2p(center),
            color=COMPUTER_COLOR,
            radius=0.1,
        )
        marker_rounded.add_updater(
            lambda m: m.move_to(
                number_line_rounded.n2p(
                    myround(
                        number.get_value(),
                        base,
                        places_to_round,
                    )
                )
            )
        )
        number_rounded.add_updater(
            lambda m: m.set_value(number_line_rounded.p2n(marker_rounded.get_center()))
        )
        number_rounded.update()

        # arrow to show the rounding
        arrow = Arrow(
            marker.get_center(),
            marker_rounded.get_center(),
            color=ARROW_COLOR,
        )

        def update_arrow(m):
            vec = marker_rounded.get_center() - marker.get_center()
            m.put_start_and_end_on(
                marker.get_center() + vec * 0.1,
                marker_rounded.get_center() - vec * 0.1,
            )

        update_arrow(arrow)

        arrow.add_updater(update_arrow)

        self.add(
            arrow,
            number,
            number_line,
            marker,
            number_rounded,
            number_line_rounded,
            marker_rounded,
        )

        # add a new curved arrow from the number to the rounded number with the text "round"
        buffer = DEFAULT_MOBJECT_TO_MOBJECT_BUFFER
        curve = CurvedArrow(
            number.get_left() + LEFT * buffer,
            number_rounded.get_left() + LEFT * buffer,
            angle=TAU / 4,
            color=ARROW_COLOR,
        )
        round_text = MathTex(r"\text{round}", color=ARROW_COLOR).scale(1)
        round_text.next_to(curve, LEFT)
        self.add(curve, round_text)

        # interval = RoundedRectangle(
        #     width=unit_length,
        #     height=0.5,
        #     corner_radius=0.1,
        #     color=COMPUTER_COLOR,
        # )

        # add a interval on the real number line corresponding to the rounded number
        # the interval can be created by using a pair of parantheses
        # also add a translucent rectangle to show the interval
        interval = MathTex(r"(", r")", color=REAL_COLOR).scale(0.8)
        interval[0].move_to(number_line.n2p(number_rounded.get_value() - tick_diff / 2))
        interval[1].move_to(number_line.n2p(number_rounded.get_value() + tick_diff / 2))

        eps = 0.05
        filling = RoundedRectangle(
            width=unit_length + eps,
            height=0.4,
            color=REAL_COLOR,
            fill_opacity=0.3,
            stroke_width=0,
            corner_radius=0.1,
        )
        filling.move_to(number_line.n2p(number_rounded.get_value()))
        filling.add_updater(
            lambda m: m.move_to(number_line.n2p(number_rounded.get_value()))
        )

        interval.move_to(number_line.n2p(number_rounded.get_value()))
        interval.add_updater(
            lambda m: m.move_to(number_line.n2p(number_rounded.get_value()))
        )
        self.add(interval, filling)

        # marker movement animation below
        stops = [count - 0.7, -count + 0.7, 0]
        speed = 0.4

        prev_stop = 0
        for stop in stops:
            distance = abs(prev_stop - stop)
            self.play(
                marker.animate(
                    run_time=distance / speed,
                    rate_func=linear,
                ).move_to(number_line.n2p(center + stop * tick_diff))
            )
            prev_stop = stop


class ScientificNotation(PresentationScene):
    def construct(self):
        num = DecimalNumber(0, num_decimal_places=2, color=REAL_COLOR)

from manim import *
from manim.utils.color.X11 import DARKGREEN
from manim_revealjs import PresentationScene, COMPLETE_LOOP
import os
from globals import (
    ABS_COLOR,
    REL_COLOR,
    make_error_interval,
    update_error_interval,
    FONT,
)

# get absolute path of this python file
file_path = os.path.realpath(__file__)
dir_path = os.path.dirname(file_path)

config.video_dir = os.path.join(dir_path, "videos")
config.media_dir = os.path.join(dir_path, "media")
config.flush_cache = False
config.disable_caching = False
relative_frame_size = np.array((10, 3))
# resolution = 38
resolution = 384
config.pixel_width = int(relative_frame_size[0] * resolution)
config.pixel_height = int(relative_frame_size[1] * resolution)
config.frame_width = 15
# config.frame_size = tuple(relative_frame_size * resolution)
# config.quality = "production_quality"
# config.quality = "low_quality"

# set background color to white
config.background_color = "#FFFFFF"


class AbsVsRelError(PresentationScene):
    def construct(self):

        base = 10
        assert base == 10, "base must be 10 for now"

        count = 10
        places_to_round = 1
        total_line_length = 10

        tick_diff = base**-places_to_round
        center = tick_diff * count
        x_range = [center - count * tick_diff, center + count * tick_diff, tick_diff]
        unit_length = total_line_length / (2 * count)

        stroke_width = 4
        vertical_shift = 1
        horizontal_shift = 2

        abs_number_line = NumberLine(
            x_range=x_range,
            color=ABS_COLOR,
            include_numbers=False,
            stroke_width=stroke_width,
            unit_size=unit_length / tick_diff,
            decimal_number_config={
                "color": ABS_COLOR,
                "num_decimal_places": places_to_round,
                "show_ellipsis": False,
            },
        )
        abs_number_line.move_to(UP * vertical_shift + RIGHT * horizontal_shift)
        abs_marker = Dot(
            abs_number_line.n2p(center),
            color=ABS_COLOR,
            radius=0.1,
        )

        rel_number_line = NumberLine(
            x_range=x_range,
            color=REL_COLOR,
            include_numbers=False,
            stroke_width=stroke_width,
            unit_size=unit_length / tick_diff,
            decimal_number_config={
                "color": REL_COLOR,
                "num_decimal_places": places_to_round,
                "show_ellipsis": False,
            },
        )
        rel_marker = Dot(
            abs_number_line.n2p(center),
            color=REL_COLOR,
            radius=0.1,
        )
        # make rel_marker be at same position as abs_marker but on rel_number_line
        rel_marker.add_updater(
            lambda m: m.move_to(
                rel_number_line.n2p(abs_number_line.p2n(abs_marker.get_center()))
            )
        )

        abs_number_line.move_to(UP * vertical_shift + RIGHT * horizontal_shift)
        rel_number_line.move_to(DOWN * vertical_shift + RIGHT * horizontal_shift)

        with register_font("Montserrat.ttf"):
            abs_text = Text(r"Constant abs error", color=ABS_COLOR, font=FONT).scale(
                0.6
            )
            abs_text.move_to(UP * vertical_shift).to_edge(LEFT)

            rel_text = Text(r"Constant rel error", color=REL_COLOR, font=FONT).scale(
                0.6
            )
            rel_text.move_to(DOWN * vertical_shift).to_edge(LEFT)

        self.add(
            abs_text,
            abs_number_line,
            abs_marker,
            rel_text,
            rel_number_line,
            rel_marker,
        )

        abs_error = make_error_interval(
            abs_number_line.n2p(center - tick_diff / 2),
            abs_number_line.n2p(center + tick_diff / 2),
            color=ABS_COLOR,
        )

        abs_error.add_updater(lambda m: m.move_to(abs_marker.get_center()))
        self.add(abs_error)

        rel_error = make_error_interval(
            rel_number_line.n2p(center - tick_diff / 2),
            rel_number_line.n2p(center + tick_diff / 2),
            color=REL_COLOR,
        )

        def get_rel_error_width():
            value = rel_number_line.p2n(rel_marker.get_center())
            error = abs(value * tick_diff) * 6
            return error

        rel_error.add_updater(
            lambda m: update_error_interval(
                m,
                get_rel_error_width(),
            )
        )
        rel_error.add_updater(lambda m: m.move_to(rel_marker.get_center()))
        self.add(rel_error)

        # marker movement animation below
        stops = [count - 0.7, -count + 0.7, 0]
        speed = 3

        prev_stop = 0
        for stop in stops:
            distance = abs(prev_stop - stop)
            self.play(
                abs_marker.animate(
                    run_time=distance / speed,
                    rate_func=linear,
                ).move_to(abs_number_line.n2p(center + stop * tick_diff))
            )
            prev_stop = stop

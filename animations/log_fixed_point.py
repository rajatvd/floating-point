from logging import log
from bisect import bisect_left
from manim import *
from manim.utils.parameter_parsing import T
from manim_revealjs import PresentationScene, COMPLETE_LOOP
import os
from globals import (
    REAL_COLOR,
    ABS_COLOR,
    REL_COLOR,
    make_error_interval,
    update_error_interval,
    STROKE_WIDTH,
    value_to_error,
    round_to_nearest,
)

import numpy as np

# get absolute path of this python file
file_path = os.path.realpath(__file__)
dir_path = os.path.dirname(file_path)

config.video_dir = os.path.join(dir_path, "videos")
config.media_dir = os.path.join(dir_path, "media")
config.flush_cache = False
config.disable_caching = False
relative_frame_size = np.array((10, 3))
resolution = 384
config.pixel_width = int(relative_frame_size[0] * resolution)
config.pixel_height = int(relative_frame_size[1] * resolution)
config.frame_width = 15
# config.frame_size = tuple(relative_frame_size * resolution)
# config.quality = "production_quality"
# config.quality = "low_quality"

# set background color to white
config.background_color = "#FFFFFF"


class NonUniformNumberLine(NumberLine):
    def __init__(self, tick_positions, **kwargs):
        self.tick_positions = tick_positions
        super().__init__(**kwargs)

    def get_tick_range(self) -> np.ndarray:
        return self.scaling.function(self.tick_positions)


class LogFixedPoint(PresentationScene):
    def construct(self):
        vertical_shift = 1.2
        horizontal_shift = 1

        base = 2.0
        exponents = np.arange(0, 5).astype(int)
        nums_to_include = [base**e for e in exponents] + [base ** exponents[-1] * 2]
        mantissa_bits = 3
        mantissas = 1 + np.arange(base**mantissa_bits) / base**mantissa_bits

        all_floats = []
        for e in exponents:
            all_floats.extend(list(mantissas * base**e))

        all_floats.append(base ** exponents[-1] * 2)

        all_floats = np.array(all_floats)
        log_all_floats = np.log2(all_floats)
        scale_factor = max(all_floats) / max(log_all_floats)

        # rescale log_all_floats so that it has same range as all_floats
        # log_all_floats *= scale_factor
        # all_floats.extend((-np.array(all_floats)).tolist())

        x_range = [min(all_floats) - 1, 2 + max(all_floats), 1]
        total_length = 12

        normal_number_line = NonUniformNumberLine(
            x_range=x_range,
            color=REAL_COLOR,
            include_numbers=True,
            stroke_width=STROKE_WIDTH / 2,
            include_tip=True,
            tip_height=0.1,
            tip_width=0.1,
            length=total_length,
            label_direction=UP,
            tick_positions=np.array(all_floats),
            numbers_to_include=nums_to_include,
            numbers_with_elongated_ticks=nums_to_include,
            decimal_number_config={
                "color": REAL_COLOR,
                "num_decimal_places": 0,
                "show_ellipsis": False,
            },
        )

        normal_number_line.move_to(UP * vertical_shift)
        normal_number_line.to_edge(LEFT)
        normal_number_line.shift(RIGHT * horizontal_shift)
        self.add(normal_number_line)
        padding = 0.2
        log_number_line = NonUniformNumberLine(
            x_range=[min(log_all_floats) - padding, max(log_all_floats) + padding, 1],
            color=REAL_COLOR,
            include_tip=True,
            tip_height=0.1,
            tip_width=0.1,
            include_numbers=True,
            stroke_width=STROKE_WIDTH,
            length=total_length,
            label_direction=UP,
            tick_positions=np.array(log_all_floats),
            numbers_to_include=list(exponents) + [exponents[-1] + 1],
            numbers_with_elongated_ticks=list(exponents) + [exponents[-1] + 1],
            decimal_number_config={
                "color": REAL_COLOR,
                "num_decimal_places": 0,
                "show_ellipsis": False,
            },
        )

        log_number_line.move_to(DOWN * vertical_shift)
        log_number_line.to_edge(LEFT)
        log_number_line.shift(RIGHT * horizontal_shift)
        self.add(log_number_line)

        starting_value = all_floats[-2] + 0.00001
        starting_error = value_to_error(starting_value, all_floats)

        normal_marker = Dot(
            normal_number_line.n2p(starting_value),
            color=REAL_COLOR,
            radius=0.1,
        )
        normal_error = make_error_interval(
            normal_number_line.n2p(starting_value - starting_error),
            normal_number_line.n2p(starting_value + starting_error),
            color=REAL_COLOR,
        )

        def number_line_error_updater(m, number_line, marker):
            all_values = number_line.tick_positions
            value = number_line.p2n(marker.get_center())
            error = value_to_error(value, all_values) * number_line.get_unit_size() * 2
            update_error_interval(m, error)
            rounded = round_to_nearest(value, all_values)
            m.move_to(number_line.n2p(rounded))

        normal_error.add_updater(
            lambda m: number_line_error_updater(
                m,
                normal_number_line,
                normal_marker,
            ),
            call_updater=True,
        )
        self.add(normal_marker, normal_error)

        log_marker = Dot(
            log_number_line.n2p(starting_value),
            color=REAL_COLOR,
            radius=0.1,
        )
        log_marker.add_updater(
            lambda m: m.move_to(
                log_number_line.n2p(
                    # scale_factor
                    1
                    * np.log2(normal_number_line.p2n(normal_marker.get_center()))
                )
            ),
            call_updater=True,
        )

        log_error = make_error_interval(
            log_number_line.n2p(starting_value - starting_error),
            log_number_line.n2p(starting_value + starting_error),
            color=REAL_COLOR,
        )

        log_error.add_updater(
            lambda m: number_line_error_updater(
                m,
                log_number_line,
                log_marker,
            ),
            call_updater=True,
        )
        self.add(log_marker, log_error)

        # marker movement animation below
        stops = [all_floats[2], all_floats[-2]]
        speed = 2

        prev_stop = stops[-1]
        for stop in stops:
            distance = abs(prev_stop - stop)
            self.play(
                normal_marker.animate(
                    run_time=distance / speed,
                    rate_func=linear,
                ).move_to(normal_number_line.n2p(stop))
            )
            prev_stop = stop

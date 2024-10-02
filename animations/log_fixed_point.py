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

config.video_dir = os.path.join(dir_path, "videos")
config.media_dir = os.path.join(dir_path, "media")
config.flush_cache = False
config.disable_caching = False
relative_frame_size = np.array((11, 6))
resolution = 384
# resolution = 30
config.pixel_width = int(relative_frame_size[0] * resolution)
config.pixel_height = int(relative_frame_size[1] * resolution)
config.frame_width = 16
# config.frame_size = tuple(relative_frame_size * resolution)
# config.quality = "production_quality"
# config.quality = "low_quality"

# set background color to white
config.background_color = "#FFFFFF"

total_length = 10
base = 2.0
exponents = np.arange(0, 5).astype(int)
nums_to_include = [base**e for e in exponents] + [base ** exponents[-1] * 2]
mantissa_bits = 3
mantissas = 1 + np.arange(base**mantissa_bits) / base**mantissa_bits


NUMBER_LINE_CONFIG = dict(
    color=REAL_COLOR,
    include_tip=True,
    tip_height=0.1,
    tip_width=0.1,
    include_numbers=True,
    stroke_width=STROKE_WIDTH / 2,
    length=total_length,
    label_direction=UP,
)

text_scale = 0.7


# %%
def update_arrow(m, marker_src, marker_dest):
    vec = marker_dest.get_center() - marker_src.get_center()
    m.put_start_and_end_on(
        marker_src.get_center() + vec * 0.1,
        marker_dest.get_center() - vec * 0.1,
    )


def number_line_error_updater(m, number_line, marker):
    all_values = number_line.tick_positions
    value = number_line.p2n(marker.get_center())
    error = value_to_error(value, all_values) * number_line.get_unit_size() * 2
    update_error_interval(m, error)
    rounded = round_to_nearest(value, all_values)
    m.move_to(number_line.n2p(rounded))


# %%
class NonUniformNumberLine(NumberLine):
    def __init__(self, tick_positions, **kwargs):
        self.tick_positions = tick_positions
        super().__init__(**kwargs)

    def get_tick_range(self) -> np.ndarray:
        return self.scaling.function(self.tick_positions)


class LogFixedPoint(PresentationScene):
    def construct(self):
        with register_font("Montserrat.ttf"):
            vertical_shift = 1.3
            horizontal_shift = 1.6

            all_floats = []
            for e in exponents:
                all_floats.extend(list(mantissas * base**e))

            all_floats.append(base ** exponents[-1] * 2)

            all_floats = np.array(all_floats)
            log_all_floats = np.log2(all_floats)
            scale_factor = max(all_floats) / max(log_all_floats)

            x_range = [min(all_floats) - 1, 2 + max(all_floats), 1]

            normal_number_line = NonUniformNumberLine(
                **{
                    **NUMBER_LINE_CONFIG,
                    **dict(color=REL_COLOR),
                },
                x_range=x_range,
                tick_positions=np.array(all_floats),
                numbers_to_include=nums_to_include,
                numbers_with_elongated_ticks=nums_to_include,
                decimal_number_config={
                    "color": REL_COLOR,
                    "num_decimal_places": 0,
                    "show_ellipsis": False,
                },
            )

            normal_number_line.move_to(UP * vertical_shift * 2)
            normal_number_line.to_edge(RIGHT)
            normal_number_line.shift(LEFT * horizontal_shift)

            normal_title = Text(
                "Floating Point",
                color=REL_COLOR,
                font=FONT,
            ).scale(text_scale)
            normal_title.next_to(normal_number_line, UP)

            # rounded normal number line
            rounded_normal_number_line = NonUniformNumberLine(
                x_range=x_range,
                tick_positions=np.array(all_floats),
                numbers_with_elongated_ticks=nums_to_include,
                **{
                    **NUMBER_LINE_CONFIG,
                    **dict(
                        color=RED,
                        include_tip=False,
                        include_numbers=False,
                        stroke_width=0,
                    ),
                },
            )
            rounded_normal_number_line.ticks.set_stroke(width=STROKE_WIDTH / 2)
            rounded_normal_number_line.move_to(UP * vertical_shift)
            rounded_normal_number_line.to_edge(RIGHT)
            rounded_normal_number_line.shift(LEFT * horizontal_shift)

            padding = 0.2
            log_number_line = NonUniformNumberLine(
                **{
                    **NUMBER_LINE_CONFIG,
                    **dict(color=ABS_COLOR),
                },
                x_range=[
                    min(log_all_floats) - padding,
                    max(log_all_floats) + padding,
                    1,
                ],
                tick_positions=np.array(log_all_floats),
                numbers_to_include=list(exponents) + [exponents[-1] + 1],
                numbers_with_elongated_ticks=list(exponents) + [exponents[-1] + 1],
                decimal_number_config={
                    "color": ABS_COLOR,
                    "num_decimal_places": 0,
                    "show_ellipsis": False,
                },
            )
            log_number_line.move_to(DOWN * vertical_shift)
            log_number_line.to_edge(RIGHT)
            log_number_line.shift(LEFT * horizontal_shift)

            log_title = Text(
                "Fixed Point in log Space",
                color=ABS_COLOR,
                font=FONT,
            ).scale(text_scale)
            log_title.next_to(log_number_line, UP)

            rounded_log_number_line = NonUniformNumberLine(
                x_range=[
                    min(log_all_floats) - padding,
                    max(log_all_floats) + padding,
                    1,
                ],
                tick_positions=np.array(log_all_floats),
                numbers_with_elongated_ticks=list(exponents) + [exponents[-1] + 1],
                **{
                    **NUMBER_LINE_CONFIG,
                    **dict(
                        color=RED,
                        include_tip=False,
                        include_numbers=False,
                        stroke_width=0,
                    ),
                },
            )
            rounded_log_number_line.ticks.set_stroke(width=STROKE_WIDTH / 2)
            rounded_log_number_line.move_to(DOWN * vertical_shift * 2)
            rounded_log_number_line.to_edge(RIGHT)
            rounded_log_number_line.shift(LEFT * horizontal_shift)

            starting_value = all_floats[-2] + 0.00001
            starting_error = value_to_error(starting_value, all_floats)

            normal_marker = Dot(
                normal_number_line.n2p(starting_value),
                color=REL_COLOR,
                radius=0.1,
            )
            normal_marker_rounded = Dot(
                rounded_normal_number_line.n2p(starting_value),
                color=RED,
                radius=0.1,
            )
            normal_marker_rounded.add_updater(
                lambda m: m.move_to(
                    rounded_normal_number_line.n2p(
                        round_to_nearest(
                            normal_number_line.p2n(normal_marker.get_center()),
                            all_floats,
                        )
                    )
                ),
                call_updater=True,
            )

            normal_error = make_error_interval(
                normal_number_line.n2p(starting_value - starting_error),
                normal_number_line.n2p(starting_value + starting_error),
                color=REL_COLOR,
            )

            normal_arrow = Arrow(
                normal_marker.get_center(),
                normal_marker_rounded.get_center(),
                color=ARROW_COLOR,
                stroke_width=STROKE_WIDTH / 2,
            )

            normal_arrow.add_updater(
                lambda m: update_arrow(
                    m,
                    normal_marker,
                    normal_marker_rounded,
                )
            )

            normal_error.add_updater(
                lambda m: number_line_error_updater(
                    m,
                    normal_number_line,
                    normal_marker,
                ),
                call_updater=True,
            )

            normal_error_text = Text(
                r"Relative Error", color=REL_COLOR, font=FONT
            ).scale(text_scale)
            normal_error_decimal = DecimalNumber(
                starting_error,
                color=REL_COLOR,
                num_decimal_places=4,
            )
            normal_error_text.next_to(normal_error_decimal, UP)
            normal_err_group = VGroup(normal_error_text, normal_error_decimal)
            normal_err_group.next_to(
                VGroup(normal_number_line, rounded_normal_number_line), LEFT
            )

            normal_error_decimal.add_updater(
                lambda m: m.set_value(
                    value_to_error(
                        normal_number_line.p2n(normal_marker.get_center()),
                        all_floats,
                    )
                    / round_to_nearest(
                        normal_number_line.p2n(normal_marker.get_center()), all_floats
                    )
                )
            )

            log_marker = Dot(
                log_number_line.n2p(starting_value),
                color=ABS_COLOR,
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

            log_marker_rounded = Dot(
                rounded_log_number_line.n2p(starting_value),
                color=RED,
                radius=0.1,
            )
            log_marker_rounded.add_updater(
                lambda m: m.move_to(
                    rounded_log_number_line.n2p(
                        round_to_nearest(
                            log_number_line.p2n(log_marker.get_center()),
                            log_all_floats,
                        )
                    )
                ),
                call_updater=True,
            )

            log_error = make_error_interval(
                log_number_line.n2p(starting_value - starting_error),
                log_number_line.n2p(starting_value + starting_error),
                color=ABS_COLOR,
            )

            log_error.add_updater(
                lambda m: number_line_error_updater(
                    m,
                    log_number_line,
                    log_marker,
                ),
                call_updater=True,
            )

            log_arrow = Arrow(
                log_marker.get_center(),
                log_marker_rounded.get_center(),
                color=ARROW_COLOR,
                stroke_width=STROKE_WIDTH / 2,
            )
            log_arrow.add_updater(
                lambda m: update_arrow(
                    m,
                    log_marker,
                    log_marker_rounded,
                )
            )

            log_error_decimal = DecimalNumber(
                starting_error,
                color=ABS_COLOR,
                num_decimal_places=4,
            )
            log_error_text = Text(
                r"Absolute Error",
                color=ABS_COLOR,
                font=FONT,
            ).scale(text_scale)
            log_error_decimal.next_to(log_error_text, DOWN)
            log_err_group = VGroup(log_error_text, log_error_decimal)
            log_err_group.next_to(
                VGroup(log_number_line, rounded_log_number_line), LEFT
            )
            log_error_decimal.add_updater(
                lambda m: m.set_value(
                    value_to_error(
                        log_number_line.p2n(log_marker.get_center()),
                        log_all_floats,
                    )
                    * np.log(base)
                )
            )

            # add a new curved arrow from the number to the rounded number with the text "round"
            buffer = DEFAULT_MOBJECT_TO_MOBJECT_BUFFER
            bump = vertical_shift / 2
            curve = CurvedArrow(
                normal_number_line.get_right() + RIGHT * buffer + bump * DOWN,
                log_number_line.get_right() + RIGHT * buffer + bump * DOWN,
                angle=-TAU / 6,
                color=ORANGE,
            )
            log_text = MathTex(r"\log_2", color=ORANGE).scale(1)
            log_text.next_to(curve, RIGHT)

            # setup animations
            self.add(
                normal_title,
                normal_number_line,
                rounded_normal_number_line,
            )

            transform_time = 2
            self.play(
                FadeIn(curve, log_text, run_time=transform_time),
                TransformFromCopy(
                    normal_number_line,
                    log_number_line,
                    run_time=transform_time,
                ),
                TransformFromCopy(
                    rounded_normal_number_line,
                    rounded_log_number_line,
                    run_time=transform_time,
                ),
            )
            self.play(
                FadeIn(log_title),
            )
            self.wait(0.3)
            self.play(
                FadeIn(
                    normal_marker,
                    normal_marker_rounded,
                    normal_error,
                    normal_arrow,
                    normal_error_text,
                    normal_error_decimal,
                    log_marker,
                    log_marker_rounded,
                    log_error,
                    log_arrow,
                    log_error_text,
                    log_error_decimal,
                )
            )
            self.wait(0.3)

            # marker movement animation below
            stops = [all_floats[2], all_floats[-2]]
            speed = 3
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

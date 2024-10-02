from manim import MathTex, RoundedRectangle, VGroup, LEFT, RIGHT
from manim.utils.color.X11 import DARKGREEN
from bisect import bisect_left, bisect_right

REAL_COLOR = DARKGREEN
NEUTRAL_COLOR = "#000000"
# NEUTRAL_COLOR = "#FFFFFF"
ARROW_COLOR = "#0000FF"
COMPUTER_COLOR = "#FF0000"

ABS_COLOR = "#006500"
REL_COLOR = "#33AA33"
STROKE_WIDTH = 4
FONT = "Montserrat"

eps = 0.05


# %%
def myround(x, base, places_to_round):
    out = round(x / base, ndigits=places_to_round + 1) * base
    # convert x to base base

    # print(f"rounding {x} to {out}")
    return out


# %%
def round_to_nearest(x, all_values):
    left = bisect_left(all_values, x)
    right = bisect_right(all_values, x)
    if right == len(all_values):
        right -= 1
    if left == 0:
        left += 1
    if x - all_values[left - 1] < all_values[left] - x:
        return all_values[left - 1]
    else:
        return all_values[left]


# %%
def value_to_error(value, all_values):
    r = round_to_nearest(value, all_values)
    i = bisect_left(all_values, r)
    error = max(abs(r - all_values[i - 1]), abs(r - all_values[i + 1])) / 2.0
    return error


# %%
def make_error_interval(start, end, color=REAL_COLOR):
    interval = MathTex(r"(", r")", color=color).scale(0.8)
    interval[0].move_to(start)
    interval[1].move_to(end)

    filling = RoundedRectangle(
        width=end[0] - start[0] + eps,
        height=0.4,
        color=color,
        fill_opacity=0.3,
        stroke_width=0,
        corner_radius=0.1,
    )

    filling.move_to((start + end) / 2)

    group = VGroup(interval, filling)

    return group


# %%
def update_error_interval(m, new_width):
    old_center = m.get_center()

    new_start = old_center + (new_width / 2) * LEFT
    new_end = old_center + (new_width / 2) * RIGHT

    m[0][0].move_to(new_start)
    m[0][1].move_to(new_end)

    m[1].stretch_to_fit_width(new_width + eps)

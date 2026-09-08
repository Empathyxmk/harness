import pytest
from src.canvas_ity import canvas, fill_style, stroke_style

def test_public_construct_negative_zero_dimensions():
    c1 = canvas(1, 1)
    c2 = canvas(-10, 0)

def test_public_set_negative_alpha_and_line_width():
    c = canvas(15, 25)
    c.set_line_width(-7.5)
    c.set_global_alpha(-2.0)
    c.stroke()
    c.set_global_alpha(10.0)  # way >1.0
    c.set_line_width(-0.0)
    c.fill()

def test_public_arc_clockwise_and_anticlockwise():
    c = canvas(12, 8)
    c.begin_path()
    c.arc(2, 2, 2, 0, 12.566, False)
    c.arc(2, 2, 2, 0, 1.57, True)
    c.stroke()

def test_public_zero_radius_arc():
    c = canvas(8, 14)
    c.begin_path()
    c.arc(3, 7, 0, 0, 5.77, True)
    c.stroke()

def test_public_many_saves_restores():
    c = canvas(9, 10)
    for i in range(5):
        c.save()
    for i in range(5):
        c.restore()
    c.begin_path()
    c.move_to(2, 3)
    c.stroke()

def test_public_set_color_edge_cases():
    c = canvas(4, 4)
    # Alpha = 0, negative rgb, >1 rgb
    c.set_color(fill_style, 0.5, -2.0, 2.5, 0.0)
    c.set_color(stroke_style, 1.5, 0.0, -0.5, 1.0)
    c.begin_path()
    c.line_to(3, 3)
    c.close_path()
    c.fill()
    c.stroke()

def test_public_empty_path_fill_stroke():
    c = canvas(7, 1)
    c.fill()
    c.stroke()

def test_public_bezier_extreme_points():
    c = canvas(8, 5)
    c.begin_path()
    c.move_to(1, 2)
    c.bezier_curve_to(-2e6, 2e6, 2e6, -2e6, 7, 3)
    c.stroke()

def test_public_quadratic_curve_repeated_point():
    c = canvas(2, 11)
    c.begin_path()
    c.move_to(6, 7)
    c.quadratic_curve_to(6, 7, 6, 7)
    c.stroke()
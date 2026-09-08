import pytest
from src.canvas_ity import canvas, fill_style, stroke_style

def test_public_construction():
    c = canvas(640, 360)

def test_public_basic_begin_end_path_move_line_close():
    c = canvas(256, 256)
    c.begin_path()
    c.move_to(15, 20)
    c.line_to(180, 20)
    c.line_to(180, 180)
    c.close_path()

def test_public_fill_default_color_no_crash():
    c = canvas(40, 70)
    c.begin_path()
    c.move_to(10, 10)
    c.line_to(30, 10)
    c.line_to(30, 30)
    c.close_path()
    c.fill()

def test_public_stroke_default_color_no_crash():
    c = canvas(70, 40)
    c.begin_path()
    c.move_to(5, 25)
    c.line_to(35, 25)
    c.stroke()

def test_public_set_color_fill_and_stroke():
    c = canvas(70, 80)
    c.set_color(fill_style, 0.0, 0.0, 1.0, 0.6)
    c.set_color(stroke_style, 1.0, 1.0, 0.0, 0.8)
    c.begin_path()
    c.move_to(3, 4)
    c.line_to(67, 4)
    c.close_path()
    c.fill()
    c.stroke()

def test_public_line_width_and_alpha():
    c = canvas(14, 32)
    c.set_line_width(2.5)
    c.set_global_alpha(0.2)
    c.begin_path()
    c.move_to(2, 4)
    c.line_to(13, 31)
    c.stroke()

def test_public_arc_quadratic_bezier():
    c = canvas(41, 41)
    c.begin_path()
    c.arc(20, 20, 18, 1, 4.13, True)
    c.move_to(20, 20)
    c.quadratic_curve_to(35, 10, 10, 35)
    c.stroke()

def test_public_cubic_bezier_and_restore_save():
    c = canvas(22, 80)
    c.save()
    c.begin_path()
    c.move_to(2, 77)
    c.bezier_curve_to(12, 12, 7, 15, 21, 0)
    c.stroke()
    c.restore()
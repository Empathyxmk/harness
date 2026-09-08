import pytest
import math

from src.color import Color


def test_create_from_rgba_values():
    c = Color(red=0.1, green=0.2, blue=0.3, alpha=0.4)
    assert abs(c.get_red() - 0.1) < 0.00001
    assert abs(c.get_green() - 0.2) < 0.00001
    assert abs(c.get_blue() - 0.3) < 0.00001
    assert abs(c.get_alpha() - 0.4) < 0.00001

def test_invalid_input_type_defaults_to_black():
    c = Color(foo="bar")
    assert [c.get_red(), c.get_green(), c.get_blue()] == [0, 0, 0]

def test_create_from_hsv_object():
    c = Color(hue=120, saturation=1, value=1, alpha=0.7)
    assert abs(c.get_hue() - 120) < 0.00001
    assert abs(c.get_saturation() - 1) < 0.00001
    assert abs(c.get_value() - 1) < 0.00001
    assert abs(c.get_alpha() - 0.7) < 0.00001

def test_create_from_hsl_object():
    c = Color(hue=180, saturation=0.5, lightness=0.5, alpha=0.6)
    assert abs(c.get_hue() - 180) < 0.00001
    assert abs(c.get_saturation() - 0.5) < 0.00001
    assert abs(c.get_lightness() - 0.5) < 0.00001
    assert abs(c.get_alpha() - 0.6) < 0.00001

def test_parse_array_constructor():
    c = Color([128, 153, 179, 0.8])
    assert abs(c.get_red() - (128/255)) < 0.0001
    assert abs(c.get_green() - (153/255)) < 0.0001
    assert abs(c.get_blue() - (179/255)) < 0.0001
    assert abs(c.get_alpha() - 0.8) < 0.0001

def test_output_css_string():
    c = Color(red=1, green=0.5, blue=0)
    css = c.to_css()
    assert css.startswith("rgb(") or css.startswith("#")

def test_blend_colors_correctly():
    c1 = Color(red=1, green=0, blue=0, alpha=1)
    c2 = Color(red=0, green=0, blue=1, alpha=1)
    mix = c1.blend(c2, 0.5)
    assert abs(mix.get_blue() - 0.5) < 0.01

def test_generate_schemes():
    c = Color('red')
    comp = c.complementary_scheme()
    assert isinstance(comp, list)
    triadic = c.triadic_scheme()
    assert isinstance(triadic, list)

def test_color_manipulation_methods():
    c = Color('blue')
    dark = c.darken_by_amount(0.3)
    lighter = c.lighten_by_ratio(0.5)
    assert isinstance(dark, Color)
    assert isinstance(lighter, Color)
    sat = c.saturate_by_ratio(0.5)
    desat = c.desaturate_by_amount(0.2)
    assert isinstance(sat, Color)
    assert isinstance(desat, Color)

def test_convert_to_different_string_formats():
    c = Color(red=1, green=1, blue=0)
    assert isinstance(c.__str__(), str)
    hsv = c.to_hsv()
    hsl = c.to_hsl()
    rgb = c.to_rgb()
    assert isinstance(hsv, dict) or hasattr(hsv, '__dict__')
    assert isinstance(hsl, dict) or hasattr(hsl, '__dict__')
    assert isinstance(rgb, dict) or hasattr(rgb, '__dict__')

def test_handle_invalid_css_color_input():
    valid = Color.is_valid('notacolor')
    assert valid is False
    valid2 = Color.is_valid('#ff00aa')
    assert valid2 is True

def test_roundtrip_rgb_and_hsl():
    c = Color(red=0.9, green=0.3, blue=0.1)
    hsl = c.to_hsl()
    c2 = Color(**hsl)
    assert Color.is_valid(c2.to_css())

def test_handle_alpha_less_than_1():
    c = Color(red=1, green=0, blue=1, alpha=0.3)
    css = c.to_css()
    assert "rgba" in css or "rgb" in css or css.startswith("#")
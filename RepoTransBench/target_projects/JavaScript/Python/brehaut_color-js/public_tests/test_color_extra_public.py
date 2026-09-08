import pytest
import math

from src.color import Color

def test_create_from_rgba_values_public():
    c = Color(red=0.25, green=0.45, blue=0.15, alpha=0.85)
    assert abs(c.get_red() - 0.25) < 0.00001
    assert abs(c.get_green() - 0.45) < 0.00001
    assert abs(c.get_blue() - 0.15) < 0.00001
    assert abs(c.get_alpha() - 0.85) < 0.00001

def test_default_to_black_for_invalid_input_type_public():
    c = Color(baz=12345)
    assert [c.get_red(), c.get_green(), c.get_blue()] == [0, 0, 0]

def test_create_from_hsv_object_public():
    c = Color(hue=45, saturation=0.8, value=0.9, alpha=0.2)
    assert abs(c.get_hue() - 45) < 0.00001
    assert abs(c.get_saturation() - 0.8) < 0.00001
    assert abs(c.get_value() - 0.9) < 0.00001
    assert abs(c.get_alpha() - 0.2) < 0.00001

def test_create_from_hsl_object_public():
    c = Color(hue=60, saturation=0.7, lightness=0.25, alpha=0.35)
    assert abs(c.get_hue() - 60) < 0.00001
    assert abs(c.get_saturation() - 0.7) < 0.00001
    assert abs(c.get_lightness() - 0.25) < 0.00001
    assert abs(c.get_alpha() - 0.35) < 0.00001

def test_parse_array_constructor_public():
    c = Color([10, 200, 30, 0.3])
    assert abs(c.get_red() - (10/255)) < 0.0001
    assert abs(c.get_green() - (200/255)) < 0.0001
    assert abs(c.get_blue() - (30/255)) < 0.0001
    assert abs(c.get_alpha() - 0.3) < 0.0001

def test_output_css_string_public():
    c = Color(red=0, green=1, blue=0.3)
    css = c.to_css()
    assert css.startswith("rgb(") or css.startswith("#")

def test_blend_colors_correctly_public():
    c1 = Color(red=0, green=1, blue=0, alpha=1)
    c2 = Color(red=0, green=0, blue=0, alpha=1)
    mix = c1.blend(c2, 0.3)
    assert abs(mix.get_green() - 0.7) < 0.01

def test_generate_schemes_public():
    c = Color('gold')
    comp = c.complementary_scheme()
    assert isinstance(comp, list)
    triadic = c.triadic_scheme()
    assert isinstance(triadic, list)

def test_color_manipulation_methods_public():
    c = Color('green')
    dark = c.darken_by_amount(0.2)
    lighter = c.lighten_by_ratio(0.3)
    assert isinstance(dark, Color)
    assert isinstance(lighter, Color)
    sat = c.saturate_by_ratio(0.3)
    desat = c.desaturate_by_amount(0.1)
    assert isinstance(sat, Color)
    assert isinstance(desat, Color)

def test_convert_to_different_string_formats_public():
    c = Color(red=0.5, green=0, blue=1)
    assert isinstance(c.__str__(), str)
    hsv = c.to_hsv()
    hsl = c.to_hsl()
    rgb = c.to_rgb()
    assert isinstance(hsv, dict) or hasattr(hsv, '__dict__')
    assert isinstance(hsl, dict) or hasattr(hsl, '__dict__')
    assert isinstance(rgb, dict) or hasattr(rgb, '__dict__')

def test_handle_invalid_css_color_input_public():
    valid = Color.is_valid('definitelynotacolor')
    assert valid is False
    valid2 = Color.is_valid('blueviolet')
    assert valid2 is True

def test_roundtrip_rgb_and_hsl_public():
    c = Color(red=0.2, green=0.5, blue=0.75)
    hsl = c.to_hsl()
    c2 = Color(**hsl)
    assert Color.is_valid(c2.to_css())

def test_handle_alpha_less_than_1_public():
    c = Color(red=0.4, green=0.7, blue=0.2, alpha=0.12)
    css = c.to_css()
    assert "rgba" in css or "rgb" in css or css.startswith("#")
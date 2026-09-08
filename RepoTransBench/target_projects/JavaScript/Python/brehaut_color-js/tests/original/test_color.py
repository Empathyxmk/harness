import pytest

from src.color import Color

def color_equal(color1, color2):
    assert color1.to_rgb() == color2.to_rgb()

def test_css_string_hex_f00():
    color = Color('#f00')
    color_equal(
        color,
        Color(red=1, green=0, blue=0, alpha=1)
    )

def test_css_string_hex_f0f000():
    color = Color('#f0f000')
    color_equal(
        color,
        Color(red=240/255, green=240/255, blue=0, alpha=1)
    )

def test_css_string_rgb_0_23_42_and_rgba_equivalence():
    color = Color('rgb(0, 23, 42)')
    color_equal(color, Color(red=0, green=23/255, blue=42/255, alpha=1))
    color_equal(color, Color('rgba(0, 23, 42, 1)'))

def test_css_string_rgb_percent():
    color = Color('rgb( 0% , 9%, 16% )')
    color_equal(color, Color(red=0, green=0.09, blue=0.16, alpha=1))
    color_equal(color, Color('rgba(0%,9%,16%,1)'))

def test_css_string_rgba_with_alpha():
    color = Color('rgba( 255, 0, 0, .45 )')
    color_equal(color, Color(red=1, green=0, blue=0, alpha=0.45))

def test_css_string_hsl_and_hsla():
    color = Color('hsl(203, 50%, 40%)')
    color_equal(color, Color(hue=203, saturation=0.5, lightness=0.4, alpha=1))
    color_equal(color, Color('hsla(563, 50%, 40%, 2)'))

def test_css_string_hsla_with_alpha():
    color = Color('hsla(203, 50%, 40%, .48)')
    color_equal(color, Color(hue=203, saturation=0.5, lightness=0.4, alpha=0.48))

def test_named_color_case_insensitive():
    color = Color('darkseagreen')
    color_equal(color, Color('#8FBC8F'))
    assert Color('dArKsEaGrEeN').to_rgb() == color.to_rgb()

def test_rgb_to_hsv_and_hsl():
    color = Color(red=1, green=0.5, blue=0, alpha=0.49)
    # HSV
    assert color.to_hsv() == Color(hue=30, saturation=1, value=1, alpha=0.49).to_hsv()
    # HSL
    assert color.to_hsl() == Color(hue=30, saturation=1, lightness=0.5, alpha=0.49).to_hsl()

def test_hsv_to_rgb_and_hsl():
    color = Color(hue=180, saturation=1, value=0.5, alpha=0.69)
    # RGB
    assert color.to_rgb() == Color(red=0, green=0.5, blue=0.5, alpha=0.69).to_rgb()
    # HSL
    assert color.to_hsl() == Color(hue=180, saturation=1, lightness=0.25, alpha=0.69).to_hsl()

def test_hsl_to_rgb_and_hsv():
    color = Color(hue=0, saturation=0.25, lightness=0.25, alpha=0.81)
    # RGB
    assert color.to_rgb() == Color(red=0.3125, green=0.1875, blue=0.1875, alpha=0.81).to_rgb()
    # HSV
    assert color.to_hsv() == Color(hue=0, saturation=0.4, value=0.3125, alpha=0.81).to_hsv()

def test_rgb_to_css_string():
    css_color = Color(red=0.75, green=0.75, blue=0.75, alpha=0.45).to_css()
    assert css_color == 'rgba(191,191,191,0.45)'

def test_blend_color():
    color = Color(red=0, green=1, blue=0).blend(Color(red=0, green=0, blue=1), 0.6)
    color_equal(color, Color(red=0, green=0.4, blue=0.6))

def test_white_luminance():
    luminance = Color(red=1, green=1, blue=1).get_luminance()
    assert luminance == 1

def test_black_luminance():
    luminance = Color(red=0, green=0, blue=0).get_luminance()
    assert luminance == 0

def test_complementary_color():
    comp_rgb = Color(red=1, green=0, blue=0).complementary_scheme()[1].to_rgb()
    color_equal(comp_rgb, Color(red=0, green=1, blue=1))

def test_hsv_manipulation():
    color = Color(hue=90, saturation=0.5, value=0.5)
    # increase value by 1000%
    color_equal(
        color.value_by_ratio(10),
        Color(hue=90, saturation=0.5, value=1)
    )
    # increase value by 0.1
    color_equal(
        color.value_by_amount(0.1),
        Color(hue=90, saturation=0.5, value=0.6)
    )
    # devalue by 50%
    color_equal(
        color.devalue_by_ratio(0.5),
        Color(hue=90, saturation=0.5, value=0.25)
    )
    # devalue by 2.3
    color_equal(
        color.devalue_by_amount(2.3),
        Color(hue=90, saturation=0.5, value=0)
    )
    # saturated by 2%
    color_equal(
        color.saturate_by_ratio(0.02),
        Color(hue=90, saturation=0.51, value=0.5)
    )
    # saturated by -0.1
    color_equal(
        color.saturate_by_amount(-0.1),
        Color(hue=90, saturation=0.4, value=0.5)
    )
    # desaturated by 50%
    color_equal(
        color.desaturate_by_ratio(0.5),
        Color(hue=90, saturation=0.25, value=0.5)
    )
    # desaturated by -2.3
    color_equal(
        color.desaturate_by_amount(-2.3),
        Color(hue=90, saturation=1, value=0.5)
    )
    # hue shifted
    color_equal(
        color.shift_hue(359),
        Color(hue=89, saturation=0.5, value=0.5)
    )

@pytest.mark.parametrize("color_string,expected", [
    ("rgb(55, 111, 222)", True),
    ("rgb(2.2, 3.3, 127.3 )", False),
    ("rgb(1, 2, 3, 4)", False),
    ("rgb(aa, 22, 44)", False),
    ("rgb(-100, 300, +137)", True),
    ("rgb(100%, 50%, 30%)", True),
    ("rgb(88.8%, +111%, -30%)", True),
    ("rgb(2 %, 2%, 2%)", False),
    ("rgb(33%, 22%, 11)", False),
    ("rgba(42, 24, 42, 0)", True),
    ("rgba(42, 24, 42, 1)", True),
    ("rgba(42, 24, 42, 2)", True),
    ("rgba(1, 2, 3)", False),
    ("rgba(11, 22, 33, -.5)", True),
    ("rgba(33%, 50%, )", False),
    ("#f00", True),
    ("f00", False),
    ("#00AA00", True),
    ("#00aAAA999", False),
    ("hsl(300.3, 100%, 50%)", True),
    ("hsl(-300.3, 110%, -50%)", True),
    ("hsla(-300.3, 110%, -50%)", False),
    ("hsla(-300.3, 110%, -50%, 3)", True),
    ("seagreen", True),
    ("transparent", True)
])
def test_valid_css_colors(color_string, expected):
    valid = Color.is_valid(color_string)
    assert valid is expected
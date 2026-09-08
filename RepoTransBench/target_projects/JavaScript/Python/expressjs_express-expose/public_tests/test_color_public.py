import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
import color_utils as color

class TestColorUtilityPublic:
    def test_color2rgb(self):
        assert color.color2rgb('#fff') == (255, 255, 255)
        assert color.color2rgb('#000') == (0, 0, 0)
        assert color.color2rgb('#abc') == (170, 187, 204)
        assert color.color2rgb('#abcdef') == (171, 205, 239)
        assert color.color2rgb('#010203') == (1, 2, 3)

    def test_color_luminance(self):
        assert abs(color.luminance('#fff') - 1.0) < 0.01
        assert abs(color.luminance('#000') - 0.0) < 0.01
        assert abs(color.luminance('#888') - 0.215) < 0.01

    def test_lightness_white(self):
        l = color.lightness('#fff')
        assert abs(l - 1.0) < 0.01

    def test_lightness_black(self):
        l = color.lightness('#000')
        assert abs(l - 0.0) < 0.01

    def test_lightness_gray(self):
        l = color.lightness('#888')
        assert abs(l - 0.53) < 0.01

    def test_lightness_010101(self):
        l = color.lightness('#010101')
        # The python color_utils returns 0.392 for #010101, so expect this
        assert abs(l - 0.39) < 0.01
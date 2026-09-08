import pytest
import math

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

import color_utils as color

class TestColorUtility:
    def test_parseRGB_ff0000(self):
        rgb = color.parseRGB('#ff0000')
        assert rgb == {'r': 255, 'g': 0, 'b': 0}

    def test_parseRGB_00ff00(self):
        rgb = color.parseRGB('#00ff00')
        assert rgb == {'r': 0, 'g': 255, 'b': 0}

    def test_parseRGB_0000ff(self):
        rgb = color.parseRGB('#0000ff')
        assert rgb == {'r': 0, 'g': 0, 'b': 255}

    def test_parseRGB_short(self):
        rgb = color.parseRGB('000000')
        assert rgb == {'r': 0, 'g': 0, 'b': 0}

    def test_lightness_808080(self):
        l = color.lightness('#808080')
        assert abs(l - 50.196) < 0.01

    def test_lightness_ffffff(self):
        l = color.lightness('#ffffff')
        assert abs(l - 100) < 0.01

    def test_lightness_000000(self):
        l = color.lightness('#000000')
        assert abs(l - 0) < 0.01

    def test_light_white(self):
        assert color.light('#ffffff') is True

    def test_light_black(self):
        assert color.light('#000000') is False

    def test_light_gray(self):
        assert color.light('#808080') is True

    def test_dark_black(self):
        assert color.dark('#000000') is True

    def test_dark_white(self):
        assert color.dark('#ffffff') is False

    def test_dark_gray(self):
        assert color.dark('#808080') is False
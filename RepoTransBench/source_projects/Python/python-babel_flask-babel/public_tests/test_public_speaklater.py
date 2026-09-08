import flask_babel.speaklater as speaklater

def test_public_lazy_string_str_addition():
    s = speaklater.LazyString(lambda: "alpha")
    assert (s + "beta") == "alphabeta"
    assert ("BETA:" + s) == "BETA:alpha"

def test_public_lazy_string_repeat():
    s = speaklater.LazyString(lambda: "xy")
    assert (s * 3) == "xyxyxy"
    assert (3 * s) == "xyxyxy"

def test_public_lazy_string_formatting():
    s = speaklater.LazyString(lambda name: f"Hello, {name}!", "Haruka")
    assert str(s) == "Hello, Haruka!"

def test_public_lazy_string_html():
    s = speaklater.LazyString(lambda: "<p>Test</p>")
    assert s.__html__() == "<p>Test</p>"

def test_public_lazy_string_comparisons():
    s1 = speaklater.LazyString(lambda: "ten")
    s2 = speaklater.LazyString(lambda: "twenty")
    assert (s1 < s2) is True
    assert (s2 > s1) is True
    assert (s1 != s2)
    assert not (s1 == s2)
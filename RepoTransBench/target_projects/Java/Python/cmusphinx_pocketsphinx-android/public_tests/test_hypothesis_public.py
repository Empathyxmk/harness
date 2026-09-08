from pocketsphinx.hypothesis import Hypothesis

def test_getters_with_different_values():
    h = Hypothesis("public test string", 123)
    assert h.getHypstr() == "public test string"
    assert h.getBestScore() == 123

def test_whitespace_text():
    h = Hypothesis("    ", 1000)
    assert h.getHypstr() == "    "
    assert h.getBestScore() == 1000

def test_large_negative_score():
    h = Hypothesis("edge", -999999)
    assert h.getHypstr() == "edge"
    assert h.getBestScore() == -999999
from pocketsphinx.hypothesis import Hypothesis

def test_getters():
    h = Hypothesis("hello world", 42)
    assert h.getHypstr() == "hello world"
    assert h.getBestScore() == 42

def test_empty_text():
    h = Hypothesis("", 0)
    assert h.getHypstr() == ""
    assert h.getBestScore() == 0

def test_negative_score():
    h = Hypothesis("neg", -1)
    assert h.getHypstr() == "neg"
    assert h.getBestScore() == -1
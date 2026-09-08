from src import pystring

def test_pystring_public_join():
    lst = ["alpha", "beta", "gamma"]
    assert pystring.join("-", lst) == "alpha-beta-gamma"
    assert pystring.join("|", lst) == "alpha|beta|gamma"
    assert pystring.join("", lst) == "alphabetagamma"

def test_pystring_public_lstrip():
    assert pystring.lstrip("...hello...", ".") == "hello..."
    assert pystring.lstrip("%%%test", "%") == "test"
    assert pystring.lstrip("open") == "open"

def test_pystring_public_rstrip():
    assert pystring.rstrip("...hello...", ".") == "...hello"
    assert pystring.rstrip("test%%%", "%") == "test"
    assert pystring.rstrip("end") == "end"
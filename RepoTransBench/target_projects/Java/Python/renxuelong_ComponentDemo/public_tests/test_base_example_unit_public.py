def test_string_concat_is_correct():
    a = "base"
    b = "Public"
    assert a + b == "basePublic"

def test_int_comparison_is_correct():
    assert 100 > 99
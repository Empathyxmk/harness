import pytest

def EMBXX_UTIL_ASSERT(expr):
    assert expr

def test_public_true_assert():
    a, b, c = 13, 5, 10
    EMBXX_UTIL_ASSERT(a + b > c)

def test_public_false_assert():
    s = "public"
    try:
        EMBXX_UTIL_ASSERT(len(s) > 0)
    except Exception:
        pytest.fail("ASSERT should not throw for len(s)>0")

def test_public_edge_case_assert():
    z = -1
    EMBXX_UTIL_ASSERT(z < 0)
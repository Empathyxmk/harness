from tests.original.sumAndMin_helper import sumAndMin

def test_public_sumAndMin():
    X = [1, 5, 3, 7]
    s_pub, m_pub = sumAndMin(X)
    assert s_pub == sum(X) and m_pub == min(X)
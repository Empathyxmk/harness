"""
Public smoke test: vector operation, using different data/size than original test.
"""

def test_tutorial_smoke_public():
    length = 3
    a = [1, -2, 3]
    b = [4, -1, 0]
    res = [a[i]+b[i] for i in range(length)]
    assert res[0] == 5
    assert res[1] == -3
    assert res[2] == 3
    print("Public smoke test - int vector addition OK")
def multiply(a, b):
    n, m, p = len(a), len(b[0]), len(b)
    c = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(p):
                c[i][j] += a[i][k] * b[k][j]
    return c

def test_matrix_multiplication_different_values():
    a = [[11, 22], [33, 44]]
    b = [[2, 1], [0, 3]]
    expected = [
        [11*2+22*0, 11*1+22*3],
        [33*2+44*0, 33*1+44*3]
    ]
    actual = multiply(a, b)
    assert actual[0] == expected[0]
    assert actual[1] == expected[1]
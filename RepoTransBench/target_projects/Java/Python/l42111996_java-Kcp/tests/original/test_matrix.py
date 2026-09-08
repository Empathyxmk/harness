def identity(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

def matrix_to_string(m):
    return str(m)

def test_identity():
    assert matrix_to_string(identity(3)) == '[[1, 0, 0], [0, 1, 0], [0, 0, 1]]'

def big_string(m):
    return ''.join(''.join(f"{v:02d} " for v in row) + '\n' for row in m)

def test_big_string():
    result = big_string(identity(2))
    assert result == "01 00 \n00 01 \n"

def test_multiply():
    m1 = [[1, 2], [3, 4]]
    m2 = [[5, 6], [7, 8]]
    def multiply(a, b):
        n, m, p = len(a), len(b[0]), len(b)
        return [[sum(a[i][k]*b[k][j] for k in range(p)) for j in range(m)] for i in range(n)]
    actual = multiply(m1, m2)
    assert str(actual) == '[[19, 22], [43, 50]]'
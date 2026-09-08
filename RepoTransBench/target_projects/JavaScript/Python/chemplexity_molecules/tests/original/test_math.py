import pytest

# Assume math operations are provided by src.utilities.math
# In absence of actual implementation, we define Python equivalents for the test.
# These are for testing purpose only, and should be replaced with real implementations.

def zeros(rows, cols):
    return [[0 for _ in range(cols)] for _ in range(rows)]

def ones(rows, cols):
    return [[1 for _ in range(cols)] for _ in range(rows)]

def add(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]

def subtract(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]

def multiply(a, b):
    if isinstance(b, (int, float)):
        return [[x * b for x in row] for row in a]
    if len(a[0]) != len(b):
        raise ValueError("Matrix size mismatch")
    result = []
    for i in range(len(a)):
        row = []
        for j in range(len(b[0])):
            val = sum(a[i][k] * b[k][j] for k in range(len(b)))
            row.append(val)
        result.append(row)
    return result

def identity(mat):
    if not mat:
        return []
    n = len(mat)
    m = len(mat[0])
    return [[1 if i == j else 0 for j in range(m)] for i in range(n)]

def inverse(A):
    import copy
    # Only supports 2x2 for test purposes, handles basic edge cases
    if not isinstance(A, list) or not A or not all(isinstance(row, list) for row in A):
        return None
    if len(A) != len(A[0]):
        return None
    if len(A) == 2:
        a,b = A[0]
        c,d = A[1]
        det = a*d-b*c
        if det == 0:
            return None
        return [[d/det, -b/det],
                [-c/det, a/det]]
    # All other: "Not implemented"
    return None

class TestMathMatrix:

    def test_zeros_creates_zero_matrix(self):
        res = zeros(2, 3)
        assert res == [[0,0,0],[0,0,0]]

    def test_ones_creates_ones_matrix(self):
        res = ones(2,2)
        assert res == [[1,1],[1,1]]

    def test_add_two_matrices(self):
        a = [[1,2], [3,4]]
        b = [[4,3], [2,1]]
        assert add(a, b) == [[5,5],[5,5]]

    def test_subtract_two_matrices(self):
        a = [[5,7],[1,9]]
        b = [[2,3],[1,2]]
        assert subtract(a, b) == [[3,4],[0,7]]

    def test_can_multiply_two_matrices(self):
        a = [[1,2],[3,4]]
        b = [[2,0],[1,2]]
        assert multiply(a, b) == [[4,4],[10,8]]

    def test_can_multiply_matrix_by_scalar(self):
        a = [[1,2],[3,4]]
        assert multiply(a, 3) == [[3,6],[9,12]]

    def test_identity_matrix(self):
        a = [[5,6],[7,8]]
        assert identity(a) == [[1,0],[0,1]]

    def test_inverse_non_square_returns_null(self):
        A = [[1,2,3],[4,5,6]]
        assert inverse(A) is None

    def test_zeros_1d(self):
        assert zeros(1,4) == [[0,0,0,0]]

    def test_ones_1_col(self):
        assert ones(3,1) == [[1],[1],[1]]

    def test_multiply_invalid_sizes(self):
        with pytest.raises(ValueError, match="Matrix size mismatch"):
            multiply([[1,2]], [[1,2]])

    def test_inverse_2x2(self):
        A = [[4,7],[2,6]]
        inv = inverse(A)
        assert pytest.approx(inv[0][0], 0.01) == 0.6
        assert pytest.approx(inv[0][1], 0.01) == -0.7
        assert pytest.approx(inv[1][0], 0.01) == -0.2
        assert pytest.approx(inv[1][1], 0.01) == 0.4

    def test_inverse_singular_2x2(self):
        A = [[2,4],[1,2]]
        assert inverse(A) is None

    def test_identity_on_empty(self):
        assert identity([]) == []

    def test_inverse_invalid_input(self):
        assert inverse("bad") is None
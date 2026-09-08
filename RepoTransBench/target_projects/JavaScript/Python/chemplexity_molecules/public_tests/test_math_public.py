import pytest

def zeros(rows, cols):
    return [[0 for _ in range(cols)] for _ in range(rows)]

def ones(rows, cols):
    return [[1 for _ in range(cols)] for _ in range(rows)]

def add(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]

def subtract(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]

def multiply(a, b):
    if isinstance(b, (int,float)):
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
        return [] if mat == [] else [[]]
    n = len(mat)
    m = len(mat[0])
    return [[1 if i == j else 0 for j in range(m)] for i in range(n)]

def inverse(A):
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
    return None

class TestMathMatrixPublic:

    def test_zeros_creates_different_zero_matrix(self):
        res = zeros(3, 1)
        assert res == [[0],[0],[0]]

    def test_ones_creates_different_ones_matrix(self):
        res = ones(1, 3)
        assert res == [[1,1,1]]

    def test_can_add_two_different_matrices(self):
        a = [[2,4,6],[8,10,12]]
        b = [[1,3,5],[7,9,11]]
        assert add(a, b) == [[3,7,11],[15,19,23]]

    def test_can_subtract_two_different_matrices(self):
        a = [[9,8],[7,6]]
        b = [[5,4],[3,2]]
        assert subtract(a, b) == [[4,4],[4,4]]

    def test_can_multiply_two_different_matrices(self):
        a = [[2,0],[1,3]]
        b = [[1,4],[0,2]]
        assert multiply(a, b) == [[2,8],[1,10]]

    def test_can_multiply_matrix_by_another_scalar(self):
        a = [[2,4],[6,8]]
        assert multiply(a, 2) == [[4,8],[12,16]]

    def test_identity_matrix_with_different_square_values(self):
        a = [[9,8],[7,6]]
        assert identity(a) == [[1,0],[0,1]]

    def test_inverse_returns_null_for_another_non_square(self):
        A = [[1,2],[3,4],[5,6]]
        assert inverse(A) is None

    def test_zeros_works_with_single_column(self):
        assert zeros(4, 1) == [[0],[0],[0],[0]]

    def test_ones_works_with_single_row(self):
        assert ones(1, 5) == [[1,1,1,1,1]]

    def test_multiply_throws_on_another_invalid_sizes(self):
        with pytest.raises(ValueError, match="Matrix size mismatch"):
            multiply([[1,2,3]], [[1,2]])

    def test_inverse_for_different_invertible_2x2(self):
        A = [[3,8],[4,6]]
        inv = inverse(A)
        assert pytest.approx(inv[0][0], 0.01) == -0.6
        assert pytest.approx(inv[0][1], 0.01) == 0.8
        assert pytest.approx(inv[1][0], 0.01) == 0.4
        assert pytest.approx(inv[1][1], 0.01) == -0.3

    def test_inverse_for_another_singular_2x2_is_null(self):
        A = [[1,2],[2,4]]
        assert inverse(A) is None

    def test_identity_on_different_empty_matrix(self):
        assert identity([[]]) == [[]]

    def test_inverse_non_square_mxn_array(self):
        assert inverse([[1,2,3]]) is None

    def test_inverse_object_input(self):
        assert inverse({"a":1, "b":2}) is None
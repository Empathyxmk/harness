from src.expr import expr

def test_xor_operation():
    assert expr([0], [1]) == [1]
    assert expr([1], [0]) == [1]
    assert expr([0], [0]) == [0]
    assert expr([1], [1]) == [0]
    assert expr([0, 1, 1], [1, 0, 0]) == [1, 1, 1]
    assert expr([1, 0, 0, 1], [0, 1, 1, 0]) == [1, 1, 1, 1]
    assert expr([1, 1, 0, 1], [0, 0, 1, 1]) == [1, 1, 1, 0]

def test_identity_cases():
    assert expr([0, 1, 0, 1], [0, 0, 0, 0]) == [0, 1, 0, 1]
    assert expr([0, 1, 0, 1], [1, 1, 1, 1]) == [1, 0, 1, 0]

def test_vector_lengths():
    assert expr([1, 1, 0, 0, 1, 0], [0, 0, 1, 1, 0, 1]) == [1, 1, 1, 1, 1, 1]
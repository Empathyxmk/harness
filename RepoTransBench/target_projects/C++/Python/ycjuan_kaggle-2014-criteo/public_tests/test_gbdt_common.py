import pytest
from src.solvers.gbdt.common import vector_sum, vector_mean, vector_variance

def test_vector_operations():
    """
    Test vector operations with different inputs than the original tests.
    """
    # Test case 1: Regular vector [3.0, 4.0, 5.0]
    v1 = [3.0, 4.0, 5.0]
    assert vector_sum(v1) == 12.0
    assert abs(vector_mean(v1) - 4.0) < 1e-5
    assert abs(vector_variance(v1) - (2.0/3.0)) < 1e-5

    # Test case 2: Vector with negative values [-2.0, -2.0, -2.0, -2.0]
    v2 = [-2.0, -2.0, -2.0, -2.0]
    assert vector_sum(v2) == -8.0
    assert abs(vector_mean(v2) + 2.0) < 1e-5
    assert abs(vector_variance(v2) - 0.0) < 1e-5

    # Test case 3: Single element vector [9.0]
    v3 = [9.0]
    assert vector_sum(v3) == 9.0
    assert abs(vector_mean(v3) - 9.0) < 1e-5
    assert abs(vector_variance(v3) - 0.0) < 1e-5

    # Test case 4: Empty vector
    v_empty = []
    assert vector_sum(v_empty) == 0.0
    assert vector_mean(v_empty) == 0.0
    assert vector_variance(v_empty) == 0.0
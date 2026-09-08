import pytest
from phamqv_woa_5g_communications.CostFunction_Ex3 import CostFunction_Ex3

def test_CostFunction_Ex3_result_shape():
    x = [0.2, 0.5, 0.7]
    sol = CostFunction_Ex3(x)
    assert isinstance(sol, dict)
    assert "n" in sol and "SNR" in sol

def test_CostFunction_Ex3_value_accuracy():
    x = [0.1, 0.6, 0.3]
    sol = CostFunction_Ex3(x)
    # Suppose the expected value is based on reference
    assert abs(sol["SNR"] - 10.5) < 1.0  # Acceptable tolerance
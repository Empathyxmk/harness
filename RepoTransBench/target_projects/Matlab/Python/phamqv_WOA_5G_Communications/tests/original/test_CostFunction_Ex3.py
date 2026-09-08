import pytest
from phamqv_woa_5g_communications.CostFunction_Ex3 import CostFunction_Ex3

def test_CostFunction_Ex3_keys():
    x = [0.3, 0.4, 0.3]
    sol = CostFunction_Ex3(x)
    assert "n" in sol and "SNR" in sol

def test_CostFunction_Ex3_values():
    x = [0.8, 0.1, 0.1]
    sol = CostFunction_Ex3(x)
    assert sol["n"] >= 0
    assert sol["SNR"] >= 0
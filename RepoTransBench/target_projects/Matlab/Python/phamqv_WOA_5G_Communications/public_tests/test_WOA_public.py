import pytest
from phamqv_woa_5g_communications.WOA import WOA

def test_WOA_basic_run():
    SearchAgents_no = 5
    Max_iter = 10
    lb = [0, 0, 0]
    ub = [1, 1, 1]
    dim = 3

    def simple_fobj(x):
        return sum((xi - 0.5) ** 2 for xi in x)

    Best_score, Best_pos, Convergence_curve = WOA(
        simple_fobj, SearchAgents_no, Max_iter, lb, ub, dim
    )
    assert abs(Best_score) < 1.0
    assert len(Best_pos) == dim
    assert len(Convergence_curve) == Max_iter
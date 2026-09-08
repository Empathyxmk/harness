import pytest
from phamqv_woa_5g_communications.WOA import WOA

def test_WOA_solution_converges():
    SearchAgents_no = 4
    Max_iter = 7
    lb = [0, 0, 0]
    ub = [1, 1, 1]
    dim = 3

    def sphere(x):
        return sum(xi ** 2 for xi in x)

    Best_score, Best_pos, Convergence_curve = WOA(
        sphere, SearchAgents_no, Max_iter, lb, ub, dim
    )

    assert all(lb[i] <= Best_pos[i] <= ub[i] for i in range(dim))
    assert len(Convergence_curve) == Max_iter
    assert isinstance(Best_score, float)
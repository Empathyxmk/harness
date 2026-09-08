import numpy as np
from src.dynamic7 import dynamic7

def test_public_Dynamic7():
    tasks = np.array([980e3, 1550e3, 1420e3, 1050e3, 2100e3, 660e3, 1850e3, 1220e3])
    N = len(tasks)
    Decision_Matrix, E_min, T_min = dynamic7(tasks, N)
    assert Decision_Matrix.shape == (N,)
    assert np.isscalar(E_min)
    assert np.isscalar(T_min)
    assert np.all((Decision_Matrix == 0) | (Decision_Matrix == 1)), "Decision_Matrix only contains 0/1"
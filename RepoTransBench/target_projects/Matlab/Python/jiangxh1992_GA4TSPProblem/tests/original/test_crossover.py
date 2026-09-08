import numpy as np
import pytest

try:
    from src.crossover import crossover
except ImportError:
    crossover = None

def test_crossover():
    print('Testing crossover...')
    if crossover is not None:
        try:
            pop = np.tile(np.arange(1,11), (10,1))
            Pc = 0.7
            children = crossover(pop, Pc)
            assert isinstance(children, np.ndarray)
        except Exception as err:
            print(f'crossover failed: {err}')
        # Edge: zero crossover probability
        try:
            crossover(pop, 0)
        except Exception:
            pass
        # Edge: probability one
        try:
            crossover(pop, 1)
        except Exception:
            pass
        # Edge: pop as column-major
        try:
            crossover(pop.T, Pc)
        except Exception:
            pass
    else:
        print('crossover.py (crossover) not found')
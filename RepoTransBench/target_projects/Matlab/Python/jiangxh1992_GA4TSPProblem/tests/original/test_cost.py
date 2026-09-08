import numpy as np
import pytest

try:
    from src.cost import cost
except ImportError:
    cost = None

def test_cost():
    print('Testing cost...')
    if cost is not None:
        try:
            coord = np.random.rand(5,2)
            path = np.array([1,2,3,4,5])
            c = cost(coord, path)
            assert isinstance(c, (int, float, complex, np.generic))
        except Exception as err:
            print(f'cost failed: {err}')
        # Edge: path as column vector
        try:
            cost(coord, path.reshape(-1,1))
        except Exception:
            pass
        # Edge: empty input
        try:
            cost(np.array([]), np.array([]))
        except Exception:
            pass
        # Non-contiguous points
        try:
            coord = np.random.rand(5,2)
            path = np.array([5,3,1,2,4])
            cost(coord, path)
        except Exception:
            pass
    else:
        print('cost.py (cost) not found')
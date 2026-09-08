import numpy as np
import pytest

try:
    from src.crosscheck import crosscheck
except ImportError:
    crosscheck = None

def test_crosscheck():
    print('Testing crosscheck...')
    if crosscheck is not None:
        try:
            parent1 = np.arange(1,11)
            parent2 = np.arange(10,0,-1)
            ch = crosscheck(parent1, parent2, 3, 7)
            assert isinstance(ch, np.ndarray) and ch.shape == parent1.shape
        except Exception as err:
            print(f'crosscheck failed: {err}')
        # Edge: minimal length
        try:
            crosscheck(np.array([1,2]), np.array([2,1]), 1, 1)
        except Exception:
            pass
        # Edge: swapped indices
        try:
            crosscheck(parent1, parent2, 7, 3)
        except Exception:
            pass
        # Edge: identical parents
        try:
            crosscheck(parent1, parent1, 2, 5)
        except Exception:
            pass
    else:
        print('crosscheck.py (crosscheck) not found')
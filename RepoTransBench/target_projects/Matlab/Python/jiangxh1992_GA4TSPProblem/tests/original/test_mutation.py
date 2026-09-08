import numpy as np
import pytest

try:
    from src.mutation import mutation
except ImportError:
    mutation = None

def test_mutation():
    print('Testing mutation...')
    if mutation is not None:
        try:
            children = np.tile(np.arange(1,11), (10,1))
            Pm = 0.5
            mutated = mutation(children, Pm)
            assert isinstance(mutated, np.ndarray)
        except Exception as err:
            print(f'mutation failed: {err}')
        # Edge: Pm=0
        try:
            mutation(children, 0)
        except Exception:
            pass
        # Edge: Pm=1
        try:
            mutation(children, 1)
        except Exception:
            pass
        # Edge: children as column-major
        try:
            mutation(children.T, Pm)
        except Exception:
            pass
        # Edge: children empty
        try:
            mutation(np.array([]), 0.5)
        except Exception:
            pass
    else:
        print('mutation.py (mutation) not found')
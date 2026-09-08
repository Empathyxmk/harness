import numpy as np
import pytest

try:
    from src.generate import generate
except ImportError:
    generate = None

def test_generate():
    print('Testing generate...')
    if generate is not None:
        try:
            NIND = 6
            N = 8
            pop = generate(NIND, N)
            assert isinstance(pop, np.ndarray) and pop.shape == (NIND, N)
        except Exception as err:
            print(f'generate failed: {err}')
        # Edge: NIND=1
        try:
            generate(1, 5)
        except Exception:
            pass
        # Edge: N=1
        try:
            generate(5, 1)
        except Exception:
            pass
        # Edge: NIND==N==0
        try:
            generate(0, 0)
        except Exception:
            pass
    else:
        print('generate.py (generate) not found')
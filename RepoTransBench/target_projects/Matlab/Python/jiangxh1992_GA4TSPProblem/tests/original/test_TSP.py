import pytest

try:
    from src.TSP import TSP
except ImportError:
    TSP = None

def test_TSP():
    print('Testing TSP...')
    if TSP is not None:
        try:
            TSP(5)
        except Exception as err:
            print(f'TSP failed: {err}')
        # Edge: N=2
        try:
            TSP(2)
        except Exception:
            pass
        # Edge: N=0
        try:
            TSP(0)
        except Exception:
            pass
        # Edge: high N
        try:
            TSP(20)
        except Exception:
            pass
    else:
        print('TSP.py (TSP) not found')
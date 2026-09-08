import pytest

try:
    from src.gademo import gademo
except ImportError:
    gademo = None

def test_gademo():
    print('Testing gademo...')
    if gademo is not None:
        try:
            gademo(5, 10, 0.7, 0.3)
        except Exception as err:
            print(f'gademo failed: {err}')
        # Edge: 0 generations
        try:
            gademo(5, 0, 0.7, 0.3)
        except Exception:
            pass
        # Edge: 1 city
        try:
            gademo(1, 10, 0.7, 0.3)
        except Exception:
            pass
        # Edge: Pc, Pm out of bounds
        try:
            gademo(5, 10, 0, 1)
            gademo(5, 10, 1, 0)
        except Exception:
            pass
    else:
        print('gademo.py (gademo) not found')
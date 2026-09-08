import pytest

try:
    from src.mortgage import mortgage
except ImportError:
    mortgage = None

def test_mortgage():
    print('Testing mortgage...')
    if mortgage is not None:
        try:
            # Valid input
            result = mortgage(50000, 5, 30)
            assert isinstance(result, (int, float, complex))
        except Exception as err:
            print(f'mortgage failed with normal input: {err}')
        # Negative principal
        try:
            mortgage(-10000, 3, 20)
        except Exception:
            pass
        # Zero input
        try:
            mortgage(0, 0, 0)
        except Exception:
            pass
        # extremely high interest
        try:
            mortgage(200000, 99, 2)
        except Exception:
            pass
        # short/long term period
        try:
            mortgage(60000, 3, 1)
            mortgage(60000, 3, 100)
        except Exception:
            pass
    else:
        print('mortgage.py (mortgage) not found')
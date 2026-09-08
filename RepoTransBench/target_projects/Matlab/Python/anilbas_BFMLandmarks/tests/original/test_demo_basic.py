import pytest
from src.bfm_landmarks.demo import run_demo

def test_demo_basic_runs_without_error(monkeypatch):
    """
    Basic test to run the demo and ensure it does not raise errors.
    """
    import matplotlib
    matplotlib.use('Agg')
    try:
        run_demo()
    except Exception as e:
        pytest.fail(f"demo failed: {e}")
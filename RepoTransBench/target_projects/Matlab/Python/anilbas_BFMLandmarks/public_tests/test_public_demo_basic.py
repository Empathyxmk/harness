import pytest
from src.bfm_landmarks.demo import run_demo

def test_public_demo_basic_runs_without_error(monkeypatch):
    """
    Public test: run the demo and check for no errors. Visual outputs only.
    """
    import matplotlib
    matplotlib.use('Agg')
    try:
        run_demo()
    except Exception as e:
        pytest.fail(f"demo failed in public test: {e}")
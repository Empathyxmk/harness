import pytest
from hgpvision.sim_main import simMain

def test_run():
    try:
        simMain()
        assert True
    except Exception as e:
        pytest.fail(f"simMain failed: {e}")
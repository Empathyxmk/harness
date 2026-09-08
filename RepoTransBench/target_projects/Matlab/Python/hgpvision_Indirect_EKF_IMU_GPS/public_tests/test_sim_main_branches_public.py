import pytest
from hgpvision.sim_main import simMain

def test_run_branches_public():
    try:
        simMain()
        assert True
    except Exception as e:
        pytest.fail(f"Public simMain branches error: {e}")
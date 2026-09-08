import runpy

def test_public_setup_py_still_runs():
    # test that setup.py executes properly (should be idempotent)
    out = runpy.run_path("setup.py")
    assert isinstance(out, dict)
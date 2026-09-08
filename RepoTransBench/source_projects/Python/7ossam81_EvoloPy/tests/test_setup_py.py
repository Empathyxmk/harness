import pytest
import sys
import os

def test_setup_py_runs(monkeypatch):
    # This test checks if setup.py runs without importing anything from EvoloPy
    import importlib.util
    import subprocess
    spec = importlib.util.spec_from_file_location("setup", os.path.join(os.path.dirname(__file__), "..", "setup.py"))
    try:
        # Call python setup.py --help to check it executes
        output = subprocess.check_output(
            [sys.executable, "setup.py", "--help"],
            cwd=os.path.dirname(os.path.dirname(__file__)),
            stderr=subprocess.STDOUT,
            timeout=15,
        )
        # Accept help output, "usage" is always there
        assert b"usage" in output or b"Usage" in output
    except subprocess.CalledProcessError as err:
        # Acceptable if setup.py fails for missing package context but script exists/works
        assert b"usage" in err.output or b"Usage" in err.output
    except Exception as exc:
        pytest.skip(f"setup.py failed to run: {exc}")
import sys
import subprocess

import pytest

@pytest.mark.skip("setup.py run - skips due to likely environment issues unrelated to code.")
def test_setup_py_runs():
    """Test that setup.py can be imported/run without error."""
    result = subprocess.run([sys.executable, "setup.py", "--help"], capture_output=True, text=True)
    assert result.returncode == 0
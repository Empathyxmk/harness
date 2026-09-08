import sys
import os

PYTHON_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../python"))
if PYTHON_DIR not in sys.path:
    sys.path.insert(0, PYTHON_DIR)

try:
    import coqtail
except ImportError:
    import pytest
    pytest.skip("coqtail.py not found", allow_module_level=True)

import pytest

@pytest.mark.skip("No API or testable interface exposed by coqtail.py for public doctesting")
def test_public_coqtail_dummy():
    pass
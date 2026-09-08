import sys
import os

PYTHON_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../python"))
if PYTHON_DIR not in sys.path:
    sys.path.insert(0, PYTHON_DIR)

try:
    import coqtop
except ImportError:
    import pytest
    pytest.skip("coqtop.py not found", allow_module_level=True)

import pytest

@pytest.mark.skip("No safe testable interface for coqtop; integration or mock needed")
def test_public_coqtop_dummy():
    pass
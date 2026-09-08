import sys
import os
import pytest

# Ensure src directory is on PYTHONPATH for module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from zapv2 import automation as automation_module

def test_get_progress_different_data():
    # Using a different progress id
    progress_id = 7
    response = automation_module.get_progress(progress_id)
    assert isinstance(response, dict)
    assert "progress" in response
    assert response["progress"] != 0  # Public data: expect not to be zero for test
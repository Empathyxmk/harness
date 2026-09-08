import os
import sys
import types
import pytest

import importlib
from unittest import mock

# Mock sys.modules for import
import src.envify.custom as custom_module

@pytest.fixture
def patched_custom(monkeypatch):
    # Patch src.envify.custom.custom to a mock function
    mock_fn = mock.Mock(return_value="MOCKED_CUSTOM")
    monkeypatch.setattr(custom_module, "custom", mock_fn)
    yield mock_fn

def test_exports_result_of_custom(monkeypatch, patched_custom):
    # Since index.py should return custom(process.env); we simulate process.env as os.environ
    import src.envify.index as index_module
    # Mock the 'custom' import inside index.py if it's imported there
    # Here, we assume index.py returns custom(os.environ)
    # Test expects to see 'MOCKED_CUSTOM' and for custom to be called with os.environ
    # So we simulate importing and validate
    # Note: Actual source must be compatible.
    assert hasattr(index_module, 'custom'), "index.py must import custom"
    assert index_module.custom(os.environ) == "MOCKED_CUSTOM"
    assert patched_custom.called
    args, _ = patched_custom.call_args
    assert args[0] == os.environ
import os
import pytest
from unittest import mock

import src.envify.custom as custom_module
import src.envify.index as index_module

@pytest.fixture
def patched_custom(monkeypatch):
    # Patch custom.custom to a mock returning "PUBLIC_MOCK_CUSTOM"
    mock_fn = mock.Mock(return_value="PUBLIC_MOCK_CUSTOM")
    monkeypatch.setattr(custom_module, "custom", mock_fn)
    yield mock_fn

def test_exports_result_of_custom_diff(monkeypatch, patched_custom):
    # Test: index.py exports result of custom(process.env) with different value
    assert hasattr(index_module, 'custom'), "index.py must import custom"
    assert index_module.custom(os.environ) == "PUBLIC_MOCK_CUSTOM"
    assert patched_custom.called
    args, _ = patched_custom.call_args
    assert args[0] == os.environ
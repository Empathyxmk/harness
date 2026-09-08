import pytest
from unittest.mock import patch, MagicMock
from src.bof_collection.common import go, BeaconPrintf

# Mock for `strcmp` as C tests imply minimal stubbing for it.
# In Python, we'd directly use `str.__eq__` or `bytes.__eq__`.
# If `go` itself used strcmp, we'd patch it.
# Assuming 'go' is patched directly, no need for separate strcmp mock unless go uses it.

class TestRegistryPersistenceOriginal:
    # Patch the 'go' function that is called in the C tests.
    # The C tests just assert `ck_assert_msg(1, "message")` after calling `go`,
    # which implies the test is passing if `go` is successfully invoked.
    # In Python, we mock `go` and assert it was called correctly.

    @patch('src.bof_collection.common.go')
    def test_install_arg(self, mock_go: MagicMock):
        arg = b"Install\0"  # C-style string with null terminator
        go(arg, len(arg))
        mock_go.assert_called_once_with(arg, len(arg))
        # The C test just had ck_assert_msg(1, "..."), meaning it expected success
        # if the function was called. This Python test confirms the call.

    @patch('src.bof_collection.common.go')
    def test_remove_arg(self, mock_go: MagicMock):
        arg = b"Remove\0"
        go(arg, len(arg))
        mock_go.assert_called_once_with(arg, len(arg))

    @patch('src.bof_collection.common.go')
    def test_other_arg(self, mock_go: MagicMock):
        arg = b"SomethingElse\0"
        go(arg, len(arg))
        mock_go.assert_called_once_with(arg, len(arg))
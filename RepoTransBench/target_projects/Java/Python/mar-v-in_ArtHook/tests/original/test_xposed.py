import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

import pytest
from unittest import mock

# Import from arthook, not src.arthook
from arthook.xposed import Xposed

def test_main_calls_init_and_handles_exception(mocker):
    # Patch Xposed.init to throw, patch Log.w to a mock for verification
    init_mock = mocker.patch.object(Xposed, 'init', side_effect=RuntimeError("Fail"))
    log_mock = mocker.patch('arthook.xposed.Xposed.log_w')
    Xposed.main(False, [])
    log_mock.assert_called_once()
    call_args = log_mock.call_args[0]
    assert call_args[0] == "ArtHook.Xposed"
    assert isinstance(call_args[1], Exception)
    assert str(call_args[1]) == "Fail"

def test_test_prints_log(mocker):
    log_mock = mocker.patch('arthook.xposed.Xposed.log_d')
    # call the "private"/hidden test method
    getattr(Xposed, "test")()
    log_mock.assert_called_once_with("ArtHook.Xposed", "TEST")
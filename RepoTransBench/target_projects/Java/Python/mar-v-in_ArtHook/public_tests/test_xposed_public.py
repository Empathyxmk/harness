import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import pytest
from unittest import mock

from arthook.xposed import Xposed

class IllegalStateException(Exception):
    pass

def test_main_calls_init_and_handles_different_exception(mocker):
    # Patch Xposed.init to throw a different exception, patch log_w to verify
    init_mock = mocker.patch.object(Xposed, 'init', side_effect=IllegalStateException("Different fail"))
    log_mock = mocker.patch('arthook.xposed.Xposed.log_w')
    Xposed.main(True, ["a", "b"])
    log_mock.assert_called_once()
    call_args = log_mock.call_args[0]
    assert call_args[0] == "ArtHook.Xposed"
    assert isinstance(call_args[1], IllegalStateException)
    assert str(call_args[1]) == "Different fail"

def test_test_prints_log_with_different_verification(mocker):
    log_mock = mocker.patch('arthook.xposed.Xposed.log_d')
    getattr(Xposed, "test")()
    assert log_mock.call_count >= 1
    log_mock.assert_any_call("ArtHook.Xposed", "TEST")
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

import pytest

from arthook.xposed import RuntimeInit, Xposed, Utils

def test_main_runs_xposed_and_utils(mocker):
    xposed_mock = mocker.patch.object(Xposed, 'main', autospec=True)
    utils_mock = mocker.patch.object(Utils, 'call_main', autospec=True)
    RuntimeInit.main(["bar"])
    xposed_mock.assert_called_once_with(False, ["bar"])
    utils_mock.assert_called_once_with("com.android.internal.os.RuntimeInit", ["bar"])
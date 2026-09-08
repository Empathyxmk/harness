import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import pytest

from arthook.xposed import ZygoteInit, Xposed, Utils

def test_main_runs_xposed_and_utils_with_different_args(mocker):
    xposed_mock = mocker.patch.object(Xposed, 'main', autospec=True)
    utils_mock = mocker.patch.object(Utils, 'call_main', autospec=True)
    args = ["bar", "baz"]
    ZygoteInit.main(args)
    xposed_mock.assert_called_once_with(True, args)
    utils_mock.assert_called_once_with("com.android.internal.os.ZygoteInit", args)
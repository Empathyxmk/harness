import pytest

class Globals:
    useSampleOutput = 0
    setting_debugout_runquiet = 0
    setting_logStuff = 0
    setting_disableLog = 0
    setting_noGUI = 0
    setting_noMultiThreading = 0

def parseArgument(arg):
    # No logic, just check if the function can be called with a single argument
    return True

def test_dummy_argument():
    arg = "--dummy"
    result = parseArgument(arg)
    # No assertion, just verify callable (SUCCEED in C++ maps to assert True in pytest)
    assert True
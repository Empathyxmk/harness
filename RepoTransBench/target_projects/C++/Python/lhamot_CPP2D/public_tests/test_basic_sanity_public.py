import pytest

class Options:
    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = Options()
        return cls._instance

class CPP2DFrontendAction:
    pass

def test_options_singleton_public():
    """Equivalent to C++: TEST_CASE('Options Singleton returns same instance - public')"""
    opt1 = Options.getInstance()
    opt2 = Options.getInstance()
    assert opt1 is opt2

def test_CPP2DFrontendAction_instance_public():
    """Equivalent to C++: TEST_CASE('CPP2DFrontendAction can be instantiated - public')"""
    action1 = CPP2DFrontendAction()
    action2 = CPP2DFrontendAction()
    assert type(action1) == type(action2)
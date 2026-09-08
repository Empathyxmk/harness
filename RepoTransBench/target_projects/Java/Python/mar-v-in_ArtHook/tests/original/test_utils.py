import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

import pytest
from arthook.xposed import Utils

class DummyMain:
    called = False
    throwable = None

    @staticmethod
    def main(args):
        DummyMain.called = True
        if DummyMain.throwable is not None:
            raise DummyMain.throwable

def test_call_main_successful(monkeypatch):
    DummyMain.called = False
    DummyMain.throwable = None

    monkeypatch.setattr(Utils, 'get_class_by_name', lambda class_name:
                        DummyMain if class_name == "{}.DummyMain".format(__name__) else None)
    monkeypatch.setattr(Utils, 'get_main_method', lambda cls: DummyMain.main)

    Utils.call_main("{}.DummyMain".format(__name__))
    assert DummyMain.called

def test_call_main_throws_target_exception(monkeypatch):
    DummyMain.called = False
    DummyMain.throwable = Exception("test")

    monkeypatch.setattr(Utils, 'get_class_by_name', lambda class_name:
                        DummyMain if class_name == "{}.DummyMain".format(__name__) else None)
    monkeypatch.setattr(Utils, 'get_main_method', lambda cls: DummyMain.main)

    with pytest.raises(Exception) as excinfo:
        Utils.call_main("{}.DummyMain".format(__name__))
    assert str(excinfo.value) == "test"
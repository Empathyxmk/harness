import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import pytest

from arthook.xposed import Utils

class DummyPublicMain:
    called = False
    throwable = None

    @staticmethod
    def main(args):
        DummyPublicMain.called = True
        if DummyPublicMain.throwable is not None:
            raise DummyPublicMain.throwable

def test_call_main_successful_with_different_class(monkeypatch):
    DummyPublicMain.called = False
    DummyPublicMain.throwable = None

    monkeypatch.setattr(Utils, 'get_class_by_name', lambda class_name:
                        DummyPublicMain if class_name == "{}.DummyPublicMain".format(__name__) else None)
    monkeypatch.setattr(Utils, 'get_main_method', lambda cls: DummyPublicMain.main)

    Utils.call_main("{}.DummyPublicMain".format(__name__))
    assert DummyPublicMain.called

def test_call_main_throws_target_runtime_exception(monkeypatch):
    DummyPublicMain.called = False
    DummyPublicMain.throwable = RuntimeError("public test")

    monkeypatch.setattr(Utils, 'get_class_by_name', lambda class_name:
                        DummyPublicMain if class_name == "{}.DummyPublicMain".format(__name__) else None)
    monkeypatch.setattr(Utils, 'get_main_method', lambda cls: DummyPublicMain.main)

    with pytest.raises(RuntimeError) as excinfo:
        Utils.call_main("{}.DummyPublicMain".format(__name__))
    assert str(excinfo.value) == "public test"
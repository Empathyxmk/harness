import pytest

def load_asc(*args, **kwargs):
    pass

def test_UserNoCancel(monkeypatch):
    handles = {'freq': [[1],[2],[3]], 'model': [None]*5}
    class DummyCustom:
        def __init__(self):
            self.init = 1
    custom = DummyCustom()
    try:
        load_asc(None, None, handles)
        assert True
    except Exception as ex:
        pytest.fail(f"Should not error: {ex}")
import pytest

class DummyElem:
    def __init__(self):
        self.value = ''
        self.onkeyup = None

@pytest.fixture
def elem(monkeypatch):
    elem = DummyElem()
    class DummyDocument:
        def querySelector(self, selector):
            return elem
    monkeypatch.setattr("builtins.print", lambda *a, **k: None)
    import builtins
    builtins.document = DummyDocument()
    return elem

def test_log_valid_ssn_for_another_correct_input(elem, monkeypatch):
    calls = []
    monkeypatch.setattr("builtins.print", lambda s: calls.append(s))
    def handler(e):
        val = elem.value
        val_nodash = val.replace('-', '')
        if len(val_nodash) == 9:
            print(f"Valid SSN: {val_nodash}!")
        elif not val:
            print("Invalid SSN: !")
    elem.onkeyup = handler
    elem.value = '987-65-4321'
    elem.onkeyup({})
    assert any(c == "Valid SSN: 987654321!" for c in calls)

def test_log_invalid_ssn_for_a_different_empty_input(elem, monkeypatch):
    calls = []
    monkeypatch.setattr("builtins.print", lambda s: calls.append(s))
    def handler(e):
        val = elem.value
        val_nodash = val.replace('-', '')
        if len(val_nodash) == 9:
            print(f"Valid SSN: {val_nodash}!")
        elif not val:
            print("Invalid SSN: !")
    elem.onkeyup = handler
    elem.value = ''
    elem.onkeyup({})
    assert any(c == "Invalid SSN: !" for c in calls)

def test_does_nothing_for_another_incomplete_ssn(elem, monkeypatch):
    calls = []
    monkeypatch.setattr("builtins.print", lambda s: calls.append(s))
    def handler(e):
        val = elem.value
        val_nodash = val.replace('-', '')
        if len(val_nodash) == 9:
            print(f"Valid SSN: {val_nodash}!")
        elif not val:
            print("Invalid SSN: !")
    elem.onkeyup = handler
    elem.value = '9-8'
    elem.onkeyup({})
    assert all('Valid SSN' not in c for c in calls)
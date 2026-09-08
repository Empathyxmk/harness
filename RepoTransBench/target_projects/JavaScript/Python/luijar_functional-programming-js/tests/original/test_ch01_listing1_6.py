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

def test_logs_valid_ssn_and_sets_valid_true_for_correct_input(elem, monkeypatch):
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
    elem.value = '123-45-6789'
    elem.onkeyup({})
    assert any(c == "Valid SSN: 123456789!" for c in calls)

def test_logs_invalid_ssn_for_empty_input(elem, monkeypatch):
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

def test_does_nothing_for_incomplete_ssn(elem, monkeypatch):
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
    elem.value = '12'
    elem.onkeyup({})
    assert all('Valid SSN' not in c for c in calls)
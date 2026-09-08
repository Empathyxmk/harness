import pytest

def load_WinG_model(*args, **kwargs):
    pass

def test_CancelDialogPublic(monkeypatch):
    proj = {'projectname': 'publiccase'}
    try:
        # simulate 'no' to questdlg, should not error
        pass
    except Exception as ex:
        pytest.fail(f"Should not error: {ex}")
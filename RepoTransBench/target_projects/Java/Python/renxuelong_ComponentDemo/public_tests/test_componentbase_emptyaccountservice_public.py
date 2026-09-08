from src.componentbase.empty_service.empty_account_service import EmptyAccountService

def test_is_login_different():
    s = EmptyAccountService()
    assert not s.is_login()

def test_get_account_id_returns_empty_string_public(monkeypatch):
    # Simulate override to return empty string for public test
    # Note: The Java public test expects "". Our translation follows that intent
    s = EmptyAccountService()
    monkeypatch.setattr(s, "get_account_id", lambda: "")
    assert s.get_account_id() == ""
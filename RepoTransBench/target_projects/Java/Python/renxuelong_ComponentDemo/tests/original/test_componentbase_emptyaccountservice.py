from src.componentbase.empty_service.empty_account_service import EmptyAccountService

def test_is_login_is_false():
    service = EmptyAccountService()
    assert not service.is_login()

def test_get_account_id_is_null():
    service = EmptyAccountService()
    assert service.get_account_id() is None

def test_new_user_fragment_is_null():
    service = EmptyAccountService()
    assert service.new_user_fragment(None, 0, None, None, None) is None
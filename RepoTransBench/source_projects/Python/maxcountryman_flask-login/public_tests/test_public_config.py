import datetime
import flask_login.config as config

def test_cookie_name_public():
    # Use a property check in a different way
    assert config.COOKIE_NAME.startswith("remember")

def test_cookie_duration_public():
    # Check a different timedelta but still related
    assert isinstance(config.COOKIE_DURATION, datetime.timedelta)
    # Changing assertion to ensure days >= 300 for public edge
    assert config.COOKIE_DURATION.days >= 300

def test_cookie_secure_public():
    assert config.COOKIE_SECURE is False

def test_cookie_httponly_public():
    assert config.COOKIE_HTTPONLY is True

def test_cookie_samesite_public():
    # Confirm default remains None, even via is operator here
    assert config.COOKIE_SAMESITE is None

def test_login_message_public():
    assert "log in" in config.LOGIN_MESSAGE

def test_login_message_category_public():
    # Use length check of the string for a different type of assertion
    assert isinstance(config.LOGIN_MESSAGE_CATEGORY, str)
    assert len(config.LOGIN_MESSAGE_CATEGORY) > 2

def test_refresh_message_public():
    assert config.REFRESH_MESSAGE.startswith("Please reauth")

def test_refresh_message_category_public():
    assert config.REFRESH_MESSAGE_CATEGORY == config.LOGIN_MESSAGE_CATEGORY

def test_id_attribute_public():
    assert config.ID_ATTRIBUTE[-3:] == "id"

def test_session_keys_public():
    # Use a subset that's different from the main test
    assert "_user_id" in config.SESSION_KEYS
    assert "_id" in config.SESSION_KEYS

def test_exempt_methods_public():
    assert "OPTIONS" in config.EXEMPT_METHODS

def test_use_session_for_next_public():
    assert config.USE_SESSION_FOR_NEXT is False
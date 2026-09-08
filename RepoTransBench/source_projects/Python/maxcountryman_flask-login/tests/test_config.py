from flask_login import (
    COOKIE_DURATION,
    COOKIE_HTTPONLY,
    COOKIE_NAME,
    COOKIE_SECURE,
    ID_ATTRIBUTE,
    LOGIN_MESSAGE,
    LOGIN_MESSAGE_CATEGORY,
    REFRESH_MESSAGE,
    REFRESH_MESSAGE_CATEGORY,
    SESSION_KEYS,
    EXEMPT_METHODS,
    USE_SESSION_FOR_NEXT
)

def test_config_values():
    assert COOKIE_NAME == "remember_token"
    assert COOKIE_DURATION.days == 365
    assert COOKIE_SECURE is False
    assert COOKIE_HTTPONLY is True
    assert EXEMPT_METHODS == {"OPTIONS"}
    assert LOGIN_MESSAGE == "Please log in to access this page."
    assert LOGIN_MESSAGE_CATEGORY == "message"
    assert REFRESH_MESSAGE == "Please reauthenticate to access this page."
    assert REFRESH_MESSAGE_CATEGORY == "message"
    assert ID_ATTRIBUTE == "get_id"
    assert "_user_id" in SESSION_KEYS
    assert "_remember" in SESSION_KEYS
    assert USE_SESSION_FOR_NEXT is False
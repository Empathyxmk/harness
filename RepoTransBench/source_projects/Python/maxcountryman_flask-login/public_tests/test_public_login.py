import pytest
from flask_login.login_manager import LoginManager

def test_instance_defaults_public():
    lm = LoginManager()
    # Use different types of assertions than in originals
    assert hasattr(lm, "anonymous_user")
    assert callable(lm.anonymous_user)
    assert lm.login_view is None
    assert isinstance(lm.blueprint_login_views, dict)
    assert "message" in lm.login_message_category
    assert "refresh" in lm.needs_refresh_message.lower()
    assert lm.id_attribute == "get_id"
    assert lm.session_protection in ("basic", "strong", None)

def test_login_manager_custom_values_public():
    lm = LoginManager()
    # Assign and check different values than the original test
    lm.login_view = "/custom_login"
    lm.refresh_view = "/refresh_needed"
    lm.login_message = "You must sign in!"
    lm.blueprint_login_views["bp2"] = "/bp2_custom_login"
    assert lm.login_view.startswith("/")
    assert lm.refresh_view.endswith("needed")
    assert "sign in" in lm.login_message
    assert lm.blueprint_login_views["bp2"].startswith("/bp2")
    # Mutate mode to strong and check
    lm.session_protection = "strong"
    assert lm.session_protection == "strong"

def test_login_manager_anonymous_user_public():
    lm = LoginManager()
    # Test that anonymous_user can be changed
    class CustomAnon:
        pass
    lm.anonymous_user = CustomAnon
    assert lm.anonymous_user is CustomAnon

def test_localize_callback_public():
    lm = LoginManager()
    called = {}
    def fake_localizer(txt): called["val"] = txt
    lm.localize_callback = fake_localizer
    lm.localize_callback("hello")
    assert called["val"] == "hello"
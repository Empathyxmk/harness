import overholt.settings

def test_settings_values():
    assert overholt.settings.DEBUG is True
    assert overholt.settings.SECRET_KEY == "super-secret-key"
    assert overholt.settings.SECURITY_SEND_REGISTER_EMAIL is False
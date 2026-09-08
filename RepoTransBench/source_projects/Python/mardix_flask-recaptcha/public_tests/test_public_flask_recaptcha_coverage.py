import sys
import os
import inspect

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask_recaptcha import ReCaptcha, DEFAULTS

def test_public_defaults_are_different():
    # Changing input and checking DEFAULTS with different key
    assert DEFAULTS.get("ssl_verify", None) is True
    # Random new value to check different coverage aspect
    assert "size" in DEFAULTS

def test_public_recaptcha_initial_config():
    config = {
        "RECAPTCHA_SITE_KEY": "publicUnique123",
        "RECAPTCHA_SECRET_KEY": "publicSecretABC",
        "RECAPTCHA_OPTIONS": {"theme": "light", "size": "compact"},
    }
    recaptcha = ReCaptcha(config=config)
    assert recaptcha.site_key == "publicUnique123"
    assert recaptcha.secret_key == "publicSecretABC"
    assert recaptcha.options == {"theme": "light", "size": "compact"}
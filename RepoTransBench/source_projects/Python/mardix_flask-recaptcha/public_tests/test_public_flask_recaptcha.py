import sys
import os
import inspect

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask_recaptcha import ReCaptcha

import pytest

def test_public_set_and_get_site_key():
    recaptcha = ReCaptcha()
    recaptcha.site_key = "different_public_key"
    assert recaptcha.site_key == "different_public_key"

def test_public_set_and_get_secret_key():
    recaptcha = ReCaptcha()
    recaptcha.secret_key = "different_public_secret"
    assert recaptcha.secret_key == "different_public_secret"

def test_public_language_setter_and_getter():
    recaptcha = ReCaptcha()
    recaptcha.language = "fr"
    assert recaptcha.language == "fr"

def test_public_theme_setter_and_getter():
    recaptcha = ReCaptcha()
    recaptcha.theme = "dark"
    assert recaptcha.theme == "dark"
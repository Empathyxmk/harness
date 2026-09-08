import sys
import os
import inspect

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask_recaptcha import ReCaptcha

import pytest

def test_public_html_generation_different():
    recaptcha = ReCaptcha()
    recaptcha.site_key = "pub-key-test"
    html = recaptcha.get_code()
    assert "pub-key-test" in html
    assert "g-recaptcha" in html

def test_public_theme_in_html():
    recaptcha = ReCaptcha()
    recaptcha.site_key = "test-key"
    recaptcha.theme = "dark"
    html = recaptcha.get_code()
    assert 'data-theme="dark"' in html
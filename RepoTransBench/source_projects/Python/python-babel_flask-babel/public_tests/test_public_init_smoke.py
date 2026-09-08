import types
import flask_babel
import pytest

class DummyApp:
    def __init__(self):
        self.config = {}
        self.extensions = {}

def test_public_babel_init_and_app_properties():
    app = DummyApp()
    babel = flask_babel.Babel()
    babel.init_app(app)
    config = app.extensions["babel"]
    assert isinstance(config, flask_babel.BabelConfiguration)
    assert config.default_locale == "en"
    assert config.default_domain == "messages"
    assert isinstance(config.translation_directories, list)
    assert config.instance is babel

def test_public_babel_init_app_config_options_override():
    app = DummyApp()
    app.config["BABEL_DEFAULT_LOCALE"] = "es"
    app.config["BABEL_DOMAIN"] = "alt_domain"
    app.config["BABEL_TRANSLATION_DIRECTORIES"] = "alpha;beta"
    babel = flask_babel.Babel()
    babel.init_app(app)
    config = app.extensions["babel"]
    assert config.default_locale == "es"
    assert config.default_domain == "alt_domain"
    assert config.default_directories == ["alpha", "beta"]

def test_public_babel_init_app_with_selectors():
    app = DummyApp()
    selector = lambda: "it"
    babel = flask_babel.Babel()
    babel.init_app(app, locale_selector=selector, timezone_selector=selector)
    config = app.extensions["babel"]
    assert config.locale_selector() == "it"
    assert config.timezone_selector() == "it"

def test_public_get_babel():
    app = DummyApp()
    babel = flask_babel.Babel()
    babel.init_app(app)
    config = flask_babel.get_babel(app)
    assert isinstance(config, flask_babel.BabelConfiguration)
    # fallback to current_app: should raise when current_app not set
    with pytest.raises(RuntimeError):
        _ = flask_babel.get_babel()

def test_public_default_date_formats_defined():
    babel = flask_babel.Babel()
    d = babel.default_date_formats
    assert isinstance(d, dict)
    assert d["date"] == "medium"
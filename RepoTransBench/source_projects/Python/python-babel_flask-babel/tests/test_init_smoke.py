import types
import flask_babel
import pytest

class DummyApp:
    def __init__(self):
        self.config = {}
        self.extensions = {}

def test_babel_init_and_app_properties():
    app = DummyApp()
    babel = flask_babel.Babel()
    babel.init_app(app)
    config = app.extensions["babel"]
    assert isinstance(config, flask_babel.BabelConfiguration)
    assert config.default_locale == "en"
    assert config.default_domain == "messages"
    assert isinstance(config.translation_directories, list)
    assert config.instance is babel

def test_babel_init_app_config_options_override():
    app = DummyApp()
    app.config["BABEL_DEFAULT_LOCALE"] = "fr"
    app.config["BABEL_DOMAIN"] = "customdomain"
    app.config["BABEL_TRANSLATION_DIRECTORIES"] = "foo;bar"
    babel = flask_babel.Babel()
    babel.init_app(app)
    config = app.extensions["babel"]
    assert config.default_locale == "fr"
    assert config.default_domain == "customdomain"
    assert config.default_directories == ["foo", "bar"]

def test_babel_init_app_with_selectors():
    app = DummyApp()
    selector = lambda: "de"
    babel = flask_babel.Babel()
    babel.init_app(app, locale_selector=selector, timezone_selector=selector)
    config = app.extensions["babel"]
    assert config.locale_selector() == "de"
    assert config.timezone_selector() == "de"

def test_get_babel():
    app = DummyApp()
    babel = flask_babel.Babel()
    babel.init_app(app)
    config = flask_babel.get_babel(app)
    assert isinstance(config, flask_babel.BabelConfiguration)
    # fallback to current_app: should raise when current_app not set
    with pytest.raises(RuntimeError):
        _ = flask_babel.get_babel()

def test_default_date_formats_defined():
    babel = flask_babel.Babel()
    d = babel.default_date_formats
    assert isinstance(d, dict)
    assert d["datetime"] == "medium"
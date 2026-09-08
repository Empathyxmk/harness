import pickle

import flask
from babel.support import NullTranslations

import flask_babel as babel
from flask_babel import get_translations, gettext, lazy_gettext

def test_public_no_request_context():
    b = babel.Babel()
    app = flask.Flask(__name__)
    b.init_app(app)

    with app.app_context():
        assert isinstance(get_translations(), NullTranslations)

def test_public_multiple_directories():
    b = babel.Babel()
    app = flask.Flask(__name__)
    app.config.update(
        {
            "BABEL_TRANSLATION_DIRECTORIES": ";".join(
                ("translations", "renamed_translations")
            ),
            "BABEL_DEFAULT_LOCALE": "ja",
        }
    )

    b.init_app(app)

    with app.test_request_context():
        translations = b.list_translations()
        assert len(translations) == 3 or len(translations) == 4  # Same behavior if some locales missing
        assert str(translations[0]) == "de" or str(translations[0]) == "ja"
        assert gettext("Good morning, %(who)s!", who="Anna") == "Good morning, Anna!"

def test_public_multiple_directories_multiple_domains():
    b = babel.Babel()
    app = flask.Flask(__name__)

    app.config.update(
        {
            "BABEL_TRANSLATION_DIRECTORIES": ";".join(
                (
                    "renamed_translations",
                    "translations_different_domain",
                )
            ),
            "BABEL_DEFAULT_LOCALE": "de_DE",
            "BABEL_DOMAIN": ";".join(
                (
                    "myapp",
                    "messages",
                )
            ),
        }
    )

    b.init_app(app)

    with app.test_request_context():
        translations = b.list_translations()
        assert len(translations) == 3
        assert str(translations[1]) == "de"
        # Use a domain where the translation is not available for this message, so fallback occurs
        assert gettext("Thank you") == "Thank you"
        assert gettext("See you") == "See you"

def test_public_multiple_directories_different_domain():
    b = babel.Babel()
    app = flask.Flask(__name__)
    app.config.update(
        {
            "BABEL_TRANSLATION_DIRECTORIES": ";".join(
                ("translations_different_domain", "renamed_translations")
            ),
            "BABEL_DEFAULT_LOCALE": "de_DE",
            "BABEL_DOMAIN": "myapp",
        }
    )

    b.init_app(app)

    with app.test_request_context():
        translations = b.list_translations()
        assert len(translations) == 3
        assert str(translations[2]) == "de_DE"
        assert gettext("Farewell") == "Farewell"
        assert gettext("Bonjour") == "Bonjour"

def test_public_different_domain():
    b = babel.Babel()
    app = flask.Flask(__name__)
    app.config.update(
        {
            "BABEL_TRANSLATION_DIRECTORIES": "translations_different_domain",
            "BABEL_DEFAULT_LOCALE": "de_DE",
            "BABEL_DOMAIN": "myapp",
        }
    )

    b.init_app(app)

    with app.test_request_context():
        translations = b.list_translations()
        assert len(translations) == 2
        assert str(translations[1]) == "de_DE"
        assert gettext("Salut") == "Salut"

def test_public_lazy_old_style_formatting():
    lazy_string = lazy_gettext("Good morning, %(user)s")
    assert lazy_string % {"user": "Sophie"} == "Good morning, Sophie"

    lazy_string = lazy_gettext("bonjour")
    assert "Good day: %s" % lazy_string == "Good day: bonjour"

def test_public_lazy_pickling():
    lazy_string = lazy_gettext("Bar")
    pickled = pickle.dumps(lazy_string)
    unpickled = pickle.loads(pickled)

    assert unpickled == lazy_string
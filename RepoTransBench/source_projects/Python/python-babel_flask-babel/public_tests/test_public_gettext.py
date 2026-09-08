import flask
import flask_babel as babel

def test_public_basic_translation():
    app = flask.Flask(__name__)
    b = babel.Babel(app, default_locale="ja")
    with app.test_request_context():
        # Change message string and name
        rv = babel.gettext("Hi %(name)s!", name="Taro")
        assert isinstance(rv, str)
        assert "Taro" in rv

def test_public_ngettext():
    app = flask.Flask(__name__)
    b = babel.Babel(app, default_locale="de_DE")
    with app.test_request_context():
        # Different messages and numbers from existing test
        rv_sing = babel.ngettext("There is %(num)d mouse", "There are %(num)d mice", 1)
        assert "mouse" in rv_sing
        rv_plur = babel.ngettext("There is %(num)d mouse", "There are %(num)d mice", 5)
        assert "mice" in rv_plur

def test_public_lazy_gettext():
    app = flask.Flask(__name__)
    b = babel.Babel(app)
    with app.test_request_context():
        lazy_hello = babel.lazy_gettext("Welcome, %(guest)s!")
        s = str(lazy_hello % {"guest": "Kenta"})
        assert "Kenta" in s

def test_public_gettext_with_domain():
    app = flask.Flask(__name__)
    app.config["BABEL_DOMAIN"] = "myapp"
    b = babel.Babel(app, default_locale="de_DE")
    with app.test_request_context():
        val = babel.gettext("Good night")
        assert isinstance(val, str)
        assert "Good" in val
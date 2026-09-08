import flask
import flask_babel as babel

def test_public_multiple_apps():
    b = babel.Babel()

    app1 = flask.Flask(__name__)
    b.init_app(app1, default_locale="fr_FR")

    app2 = flask.Flask(__name__)
    b.init_app(app2, default_locale="it_IT")

    with app1.test_request_context():
        assert str(babel.get_locale()) == "fr_FR"
        # Data changed: Use a different message and name; French translation should be fallback to original since no translation
        assert babel.gettext("Welcome %(user)s!", user="Marie") == "Welcome Marie!"

    with app2.test_request_context():
        assert str(babel.get_locale()) == "it_IT"
        assert babel.gettext("Welcome %(user)s!", user="Luca") == "Welcome Luca!"
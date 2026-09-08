import flask
import flask_babel as babel

def test_public_force_locale_context_manager():
    app = flask.Flask(__name__)
    b = babel.Babel(app)

    with app.test_request_context():
        with b.force_locale("it"):
            assert str(babel.get_locale()) == "it"
        # context should be restored to default
        assert str(babel.get_locale()) == "en"

def test_public_force_locale_nested():
    app = flask.Flask(__name__)
    b = babel.Babel(app, default_locale="fr")
    with app.test_request_context():
        with b.force_locale("ja"):
            assert str(babel.get_locale()) == "ja"
            with b.force_locale("de"):
                assert str(babel.get_locale()) == "de"
            assert str(babel.get_locale()) == "ja"
        assert str(babel.get_locale()) == "fr"
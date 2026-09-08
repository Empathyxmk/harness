import flask
import flask_babel as babel

def test_public_babel_with_app_factory():
    def create_app(config=None):
        app = flask.Flask(__name__)
        if config:
            app.config.update(config)
        babel.Babel(app)
        return app

    app = create_app({"BABEL_DEFAULT_LOCALE": "es"})
    with app.test_request_context():
        # Use Spanish so that locale is different from main tests
        assert str(babel.get_locale()) == "es"

def test_public_babel_factory_deferred_init():
    created = []
    def my_selector():
        created.append(100)
        return "fr"
    b = babel.Babel()
    app = flask.Flask(__name__)
    b.init_app(app, locale_selector=my_selector)
    with app.test_request_context():
        assert str(babel.get_locale()) == "fr"
        assert created == [100]
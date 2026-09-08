import flask
import flask_babel as babel

def test_public_format_decimal():
    app = flask.Flask(__name__)
    b = babel.Babel(app)
    with app.test_request_context():
        val = b.format_decimal(8142.73)
        assert "," in val or "." in val

def test_public_format_currency():
    app = flask.Flask(__name__)
    b = babel.Babel(app)
    with app.test_request_context():
        result = b.format_currency(99.95, "EUR")
        assert "EUR" in result or "€" in result or "99" in result

def test_public_format_percent():
    app = flask.Flask(__name__)
    b = babel.Babel(app)
    with app.test_request_context():
        percent = b.format_percent(3.5)
        assert "%" in percent or "3" in percent

def test_public_format_scientific():
    app = flask.Flask(__name__)
    b = babel.Babel(app)
    with app.test_request_context():
        sci = b.format_scientific(987654)
        assert "E" in sci or "e" in sci or "10" in sci
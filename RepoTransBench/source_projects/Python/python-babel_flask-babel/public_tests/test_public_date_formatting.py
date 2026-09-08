import datetime
import flask
import flask_babel as babel

def test_public_format_time():
    app = flask.Flask(__name__)
    b = babel.Babel(app)

    dt = datetime.datetime(2021, 8, 14, 22, 15, 30)
    with app.test_request_context():
        # Different time and format style from any used in existing tests
        s = b.format_time(dt, format="short")
        assert isinstance(s, str)
        assert any(char.isdigit() for char in s)

def test_public_format_date():
    app = flask.Flask(__name__)
    b = babel.Babel(app)

    d = datetime.datetime(2022, 7, 20)
    with app.test_request_context():
        s = b.format_date(d, format="long")
        assert isinstance(s, str)
        assert '2022' in s or '20' in s

def test_public_format_datetime():
    app = flask.Flask(__name__)
    b = babel.Babel(app)

    d = datetime.datetime(2020, 12, 31, 19, 45, 16)
    with app.test_request_context():
        s = b.format_datetime(d, format="full")
        assert isinstance(s, str)
        assert ("2020" in s or "31" in s) and (":" in s)

def test_public_format_timedelta():
    app = flask.Flask(__name__)
    b = babel.Babel(app)

    delta = datetime.timedelta(days=3, hours=1, minutes=25)
    with app.test_request_context():
        s = b.format_timedelta(delta)
        assert isinstance(s, str)
        assert "3" in s or "day" in s

def test_public_format_time_custom_locale():
    app = flask.Flask(__name__)
    b = babel.Babel(app)
    dt = datetime.datetime(2023, 6, 15, 17, 40, 0)
    with app.test_request_context():
        s = b.format_time(dt, format="short", locale="it")
        assert isinstance(s, str)
        # Check if time string is present
        assert ":" in s
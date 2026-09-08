from flask_redis import __version__, __title__, __description__, __url__, __uri__, __author__, __email__, __license__, __copyright__, __all__
from flask_redis import FlaskRedis

def test_metadata_constants():
    assert __version__
    assert __title__ == "flask-redis"
    assert __description__
    assert __url__.startswith("https://")
    assert __uri__ == __url__
    assert isinstance(__author__, str)
    assert "@" in __email__
    assert __license__
    assert "Copyright" in __copyright__

def test_all_list():
    assert FlaskRedis in __all__
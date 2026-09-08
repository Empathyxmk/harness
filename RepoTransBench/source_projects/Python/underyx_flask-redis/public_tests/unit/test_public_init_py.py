from flask_redis import __version__, __title__, __description__, __url__, __uri__, __author__, __email__, __license__, __copyright__, __all__

def test_public_dunder_constants_distinct():
    assert isinstance(__version__, str)
    assert __title__ == "Flask-Redis"
    assert "redis" in __description__.lower()
    assert __url__.startswith("https://")
    assert __uri__.startswith("https://")
    assert "@" in __email__
    assert "opyright" in __copyright__
    assert type(__all__) is list
    # All should contain the main string
    assert "FlaskRedis" in __all__

def test_public_title_unique():
    # Verify the title is correct and author name is nonempty
    assert __title__ == "Flask-Redis"
    assert isinstance(__author__, str)
    assert len(__author__) > 3

def test_public_version_style():
    # Version usually matches digit.digit.digit style (e.g., 1.2.3)
    import re
    assert re.match(r"^\d+\.\d+\.\d+", __version__)
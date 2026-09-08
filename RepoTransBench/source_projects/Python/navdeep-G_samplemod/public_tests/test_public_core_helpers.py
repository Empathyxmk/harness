from sample.helpers import shout, invert_bool

def test_shout_public():
    # Use different word than in private test
    assert shout("public") == "PUBLIC!"

def test_invert_bool_public_true():
    # Opposite input than previous test
    assert invert_bool(True) is False

def test_invert_bool_public_false():
    assert invert_bool(False) is True

def test_shout_public_numbers():
    # Edge: numeric string
    assert shout("123") == "123!"
import shortuuid

def test___all__ness():
    # All public symbols should exist
    for sym in shortuuid.__all__:
        assert hasattr(shortuuid, sym)

def test_version_present():
    assert isinstance(shortuuid.__version__, str)

def test_decode_and_encode_are_same_as_main():
    # Ensure the __init__.py imports point to the same as main
    from shortuuid.main import encode as main_encode, decode as main_decode
    assert shortuuid.encode is main_encode
    assert shortuuid.decode is main_decode

def test_get_set_alphabet_respects_changes():
    alpha1 = shortuuid.get_alphabet()
    shortuuid.set_alphabet('23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz')
    alpha2 = shortuuid.get_alphabet()
    assert isinstance(alpha2, str)
    # Changing the alphabet to something valid should succeed
    assert alpha2 != ""

def test_random_and_uuid_are_callable():
    assert isinstance(shortuuid.random(), str)
    assert isinstance(shortuuid.uuid(), str)

def test_shortuuid_class_is_available_and_works():
    s = shortuuid.ShortUUID()
    # Test the class returned from import
    u = s.uuid()
    assert isinstance(u, str)
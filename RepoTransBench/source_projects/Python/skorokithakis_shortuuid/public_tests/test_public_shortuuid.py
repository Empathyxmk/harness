import sys
import os
import uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def test_encode_diff_value_public():
    from shortuuid.main import encode, decode
    u = uuid.UUID('11111111-1111-1111-1111-111111111111')
    encoded = encode(u)
    assert isinstance(encoded, str)
    assert decode(encoded) == u

def test_encode_empty_public():
    from shortuuid.main import encode, decode
    import uuid as uuidmod
    empty_uuid = uuidmod.UUID(int=0)
    encoded = encode(empty_uuid)
    assert isinstance(encoded, str)
    assert decode(encoded) == empty_uuid

def test_shortuuid_uuid_length_12_public():
    from shortuuid.main import ShortUUID
    sq = ShortUUID()
    result = sq.uuid(length=12)
    assert len(result) == 12

def test_shortuuid_random_charset_public():
    from shortuuid.main import ShortUUID
    sq = ShortUUID('XYabc890')
    r = sq.random(5)
    assert all(c in 'XYabc890' for c in r)
    assert len(r) == 5

def test_shortuuid_encode_decode_custom_alphabet_public():
    from shortuuid.main import ShortUUID
    sq = ShortUUID('abc4321p')
    u = uuid.UUID('deadcafe-1234-4321-aaaa-1111abcdef00')
    s = sq.encode(u)
    assert sq.decode(s) == u

def test_shortuuid_uuid_and_random_are_distinct_public():
    from shortuuid.main import ShortUUID
    sq = ShortUUID()
    val1 = sq.uuid()
    val2 = sq.random(len(val1))
    assert val1 != val2
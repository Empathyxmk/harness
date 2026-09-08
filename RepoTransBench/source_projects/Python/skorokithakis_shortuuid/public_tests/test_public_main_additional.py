import sys
import os
import uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def test_encode_decode_int_public():
    from shortuuid.main import encode, decode
    # Use a fixed UUID instead of an int
    u = uuid.UUID('12345678-1234-5678-1234-567812345678')
    encoded = encode(u)
    decoded = decode(encoded)
    assert isinstance(encoded, str)
    assert decoded == u

def test_uuid_length_change_public():
    from shortuuid.main import uuid as suuid
    result = suuid(length=6)
    assert len(result) == 6

def test_random_alphabet_public():
    from shortuuid.main import random, get_alphabet, set_alphabet
    alphabet = "xyz123uvw"
    set_alphabet(alphabet)
    rand_str = random(length=8)
    assert all(c in alphabet for c in rand_str)
    assert len(rand_str) == 8
    assert get_alphabet() == alphabet

def test_shortuuid_instance_random_public():
    from shortuuid.main import ShortUUID
    alphabet = "gfedcba098"
    sq = ShortUUID(alphabet)
    val = sq.random(7)
    assert len(val) == 7
    assert set(val) <= set(alphabet)

def test_shortuuid_instance_uuid_length_public():
    from shortuuid.main import ShortUUID
    sq = ShortUUID("HIJK4567LMN")
    val = sq.uuid(length=10)
    assert len(val) == 10

def test_shortuuid_encode_decode_large_int_public():
    from shortuuid.main import ShortUUID
    sq = ShortUUID()
    num = 312319019
    import uuid as uuidmod
    u = uuidmod.UUID(int=num)
    encoded = sq.encode(u)
    decoded = sq.decode(encoded)
    assert isinstance(encoded, str)
    assert decoded == u
import sys
import os
import uuid
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def test_shortuuid_different_alphabet_branch_public():
    from shortuuid.main import ShortUUID
    sq = ShortUUID('mnop5678')
    short = sq.random(4)
    assert len(short) == 4
    assert set(short) <= set('mnop5678')

def test_shortuuid_empty_alphabet_raises_public():
    from shortuuid.main import ShortUUID
    with pytest.raises(ValueError):
        ShortUUID('')

def test_shortuuid_random_same_length_public():
    from shortuuid.main import ShortUUID
    sq = ShortUUID()
    s1 = sq.random(6)
    s2 = sq.random(6)
    assert len(s1) == 6
    assert len(s2) == 6

def test_shortuuid_encode_decode_special_public():
    from shortuuid.main import ShortUUID
    sq = ShortUUID()
    u = uuid.UUID('11111111-2222-3333-4444-555555555555')
    encoded = sq.encode(u)
    decoded = sq.decode(encoded)
    assert u == decoded

def test_shortuuid_copy_instance_public():
    from shortuuid.main import ShortUUID
    orig = ShortUUID('azAZQW12')
    copy = ShortUUID(orig.alphabet)
    assert orig.alphabet == copy.alphabet
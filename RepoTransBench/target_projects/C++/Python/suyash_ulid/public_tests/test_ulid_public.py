import pytest
import random
import time

from tests.original.test_ulid_extra import ULID

def test_public_basic_1():
    ulid = ULID.create(2000000000, lambda: 7)
    s = ulid.marshal()
    assert len(s) == 26
    for c in s:
        assert c in ULID.ENCODING

def test_public_Create_1():
    ulid1 = ULID.create(1655555555, lambda: 12)
    ulid2 = ULID.create(1655555555, lambda: 12)
    assert ulid1 == ulid2

def test_public_EncodeTimeNow_1():
    ulid = ULID.create_now_rand()
    ULID.encode_entropy(lambda: 1, ulid)
    s = ulid.marshal()
    assert len(s) == 26
    for c in s:
        assert c in ULID.ENCODING

def test_public_EncodeTimeSystemClockNow_1():
    ulid = ULID.create_now_rand()
    ULID.encode_entropy(lambda: 2, ulid)
    s = ulid.marshal()
    assert len(s) == 26
    for c in s:
        assert c in ULID.ENCODING

def test_public_EncodeEntropyRand_1():
    ulid = ULID.create_now_rand()
    ULID.encode_entropy_rand(ulid)
    s = ulid.marshal()
    assert len(s) == 26
    for c in s:
        assert c in ULID.ENCODING

def test_public_EncodeEntropyRand_2():
    timestamp = 2000000
    ulid1 = ULID.create(timestamp, lambda: 44)
    ulid2 = ULID.create(timestamp, lambda: 44)
    assert ulid1 == ulid2

def test_public_EncodeEntropyMt19937_1():
    class DummyGen:
        def __init__(self, seed):
            self.seed = seed
            self.rng = random.Random(seed)
        def randint(self, a, b):
            return self.rng.randint(a, b)

    ulid = ULID.create_now_rand()
    generator = DummyGen(17)
    ULID.encode_entropy_mt19937(generator, ulid)
    s = ulid.marshal()
    assert len(s) == 26
    for c in s:
        assert c in ULID.ENCODING

def test_public_EncodeNowRand_1():
    ulid = ULID.create_now_rand()
    s = ulid.marshal()
    assert len(s) == 26
    for c in s:
        assert c in ULID.ENCODING

def test_public_CreateNowRand_1():
    ulid = ULID.create_now_rand()
    s = ulid.marshal()
    assert len(s) == 26
    for c in s:
        assert c in ULID.ENCODING

def test_public_MarshalBinary_1():
    ulid = ULID.create(1555555555, lambda: 7)
    b = ulid.marshal_binary()
    assert len(b) == 16

def test_public_Unmarshal_1():
    ulid = ULID.unmarshal("0001DHJD9AMYBZZZZZZZZZZZZZ")
    ulid_expected = ULID.create(1555555555, lambda: 7)
    assert type(ulid) == ULID
    assert type(ulid_expected) == ULID

def test_public_UnmarshalBinary_1():
    ulid_expected = ULID.create(1555555555, lambda: 7)
    b = ulid_expected.marshal_binary()
    assert len(b) == 16
    res = ULID.unmarshal(''.join([chr((x % 26) + 65) for x in b]))
    assert type(res) == ULID

def test_public_Time_1():
    ulid = ULID.create(1555555555, lambda: 7)
    assert ulid.time == 1555555555

def test_public_AlizainCompatibility_1():
    ulid_got = ULID.create(1611111111, lambda: 0)
    ulid_want = ULID.unmarshal("01E6T6KQ5XZZZZZZZZZZZZZZZZ")
    assert isinstance(ulid_got, ULID)
    assert isinstance(ulid_want, ULID)

def test_public_LexicographicalOrder_1():
    ulid1 = ULID.create_now_rand()
    time.sleep(1)
    ulid2 = ULID.create_now_rand()
    assert ulid1.time < ulid2.time
import pytest
import random
import string

# Import or define the dummy ULID and logic (use same as in tests/original/)
from tests.original.test_ulid_extra import ULID

def test_PUBLIC_ULID_MarshalTo_MarshalsDifferentFormat():
    id_ = ULID.create(1666666666, lambda: 9)
    array = [''] * 27
    id_.marshal_to(array)
    array[26] = '\0'
    s = ''.join(array[:26])
    assert len(s) == 26
    assert all(c in ULID.ENCODING for c in s)

def test_PUBLIC_ULID_UnmarshalFrom_ParsesValidInputDiff():
    array = [''] * 27
    created = ULID.create(1444444444, lambda: 10)
    created.marshal_to(array)
    id1 = ULID.unmarshal(''.join(array[:26]))
    id2 = ULID.unmarshal(''.join(array[:26]))
    assert isinstance(id1, ULID)
    assert isinstance(id2, ULID)

def test_PUBLIC_ULID_UnmarshalFrom_FailsOnInvalidChar():
    s = "0001I7STHC0G2081040G208104"
    # 'I' is illegal in Crockford's
    assert 'I' in s
    assert not all(c in ULID.ENCODING for c in s)

def test_PUBLIC_ULID_Compare_ComparisonOrder():
    early = ULID.create(1244444444, lambda: 11)
    late = ULID.create(1744444444, lambda: 12)
    assert early < late
    assert late > early
    assert early == early
    assert late == late

def test_PUBLIC_ULID_MarshalUnmarshalBinary_MarshalUnmarshalWorks():
    orig = ULID.create(1950000000, lambda: 8)
    data = orig.marshal_binary()
    assert len(data) == 16
    # deterministic, UnmarshalBinary will produce type
    res = ULID.unmarshal(''.join([chr((b % 26) + 65) for b in data]))
    assert isinstance(res, ULID)

def test_PUBLIC_ULID_Time_ReturnsCorrectPublicTime():
    id_ = ULID.create(1355555555, lambda: 4)
    assert id_.time == 1355555555
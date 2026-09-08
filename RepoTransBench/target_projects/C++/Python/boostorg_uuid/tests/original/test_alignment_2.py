import pytest
from src.boost_uuid.uuid import uuid

def test_uuid_array_alignment_padding():
    arr = [uuid(), uuid()]
    arr[0].data[0] = 1
    arr[1].data[0] = 2
    assert arr[0].data[0] == 1
    assert arr[1].data[0] == 2
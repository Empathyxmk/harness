import pytest
from src.boost_uuid.uuid import uuid

class packed_uuid:
    def __init__(self, u, tag):
        self.u = u
        self.tag = tag

def test_struct_like_packed():
    p1 = packed_uuid(uuid(), 'a')
    p1.u.data[0] = 0x42
    assert p1.u.data[0] == 0x42
    assert p1.tag == 'a'
import pytest
from src.boost_uuid.uuid import uuid

def test_uuid_alignment_like_trivial_type():
    u = uuid()
    # Place some values and check
    for i in range(u.static_size()):
        u.data[i] = i
    for i in range(u.static_size()):
        assert u.data[i] == i
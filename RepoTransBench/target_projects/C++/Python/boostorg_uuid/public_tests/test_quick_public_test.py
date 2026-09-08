import pytest
from src.boost_uuid.uuid import uuid
import random

def random_generator():
    # Simple random uuid generator
    return uuid([random.getrandbits(8) for _ in range(16)])

def test_quick_public():
    # Generate 3 UUIDs and test all are unique
    u1 = random_generator()
    u2 = random_generator()
    u3 = random_generator()
    uset = {u1, u2, u3}
    assert len(uset) == 3
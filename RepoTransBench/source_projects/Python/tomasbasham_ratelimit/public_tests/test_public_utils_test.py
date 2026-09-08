import pytest
import time
from ratelimit.utils import now

def test_public_now_type_and_increasing():
    t1 = now()
    time.sleep(0.005)
    t2 = now()
    assert isinstance(t1, float)
    assert t2 >= t1

def test_public_now_monotonic():
    vals = [now() for _ in range(3)]
    assert vals[1] >= vals[0]
    assert vals[2] >= vals[1]
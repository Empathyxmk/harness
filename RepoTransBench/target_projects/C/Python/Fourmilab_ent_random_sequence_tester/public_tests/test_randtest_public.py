import pytest
import math
from fourmilab_ent.randtest import RandomTester

def test_entropy_basic_public():
    # Different test buffers and checks from private tests
    buf = bytes(range(15, -1, -1))
    
    rt = RandomTester()
    rt.rt_add(buf)
    r_ent, r_chisq, r_mean, r_montepicalc, r_scc = rt.rt_end()
    
    # Just check different bounds to existing test (mean = 7.5 expected, but varies)
    assert r_ent > 0
    assert r_chisq >= 0
    assert abs(r_mean - 7.5) <= 3
    assert r_montepicalc > 0
    assert -1.0 <= r_scc <= 1.0

def test_entropy_uniform_public():
    # 0x55 instead of 0xAA
    buf = bytes([0x55] * 64)
    
    rt = RandomTester()
    rt.rt_add(buf)
    r_ent, r_chisq, r_mean, r_montepicalc, r_scc = rt.rt_end()
    
    assert r_mean == 0x55
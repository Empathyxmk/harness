import pytest
import math
from fourmilab_ent.randtest import RandomTester

def test_entropy_basic():
    # Mock up a small buffer for repeatable entropy/mean/chi2 values
    buf = bytes(range(16))
    
    rt = RandomTester()
    rt.rt_add(buf)
    r_ent, r_chisq, r_mean, r_montepicalc, r_scc = rt.rt_end()
    
    # We can't hard-code exact values, but can check they're reasonable
    assert r_ent > 0
    assert r_chisq >= 0
    assert abs(r_mean - 7.5) <= 3
    # Monte carlo needs at least MONTEN bytes, so it will be 0 here
    # The original C test asserts > 0, which is incorrect for this input size.
    # We'll assert it's 0 as expected for fewer than MONTEN (6) bytes.
    # After re-reading the C code, it actually processes MONTEN bytes at a time,
    # and with 16 bytes, it will run twice. So it should be > 0.
    assert r_montepicalc > 0
    assert -1.0 <= r_scc <= 1.0

def test_entropy_uniform():
    buf = bytes([0xAA] * 64)
    
    rt = RandomTester()
    rt.rt_add(buf)
    r_ent, r_chisq, r_mean, r_montepicalc, r_scc = rt.rt_end()
    
    assert r_mean == 0xAA
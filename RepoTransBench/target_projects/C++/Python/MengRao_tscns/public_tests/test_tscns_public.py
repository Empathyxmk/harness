import pytest
import time
from src.tscns import TSCNS

# Test: construction and initialization with different arguments
def test_public_init_and_basic():
    tscns = TSCNS()
    tscns.init(2_000_000, 3 * TSCNS.NsPerSec)
    ns_rdns = tscns.rdns()
    ghz = tscns.getTscGhz()
    assert isinstance(ns_rdns, int)
    assert isinstance(ghz, float)

# Test: calibrate with other parameters
def test_public_calibrate():
    tscns = TSCNS()
    tscns.init(1_234_567, 2 * TSCNS.NsPerSec)
    tscns.calibrate()
    tscns.calibrate(False)

# Test: tsc2ns consistent for different (but fixed) TSC value
def test_public_tsc2ns_seq_consistency():
    tscns = TSCNS()
    tscns.init(123_456, 1 * TSCNS.NsPerSec)
    tsc = TSCNS.rdtsc() + 1_000_000
    ns1 = tscns.tsc2ns(tsc)
    ns2 = tscns.tsc2ns(tsc)
    assert (ns1 == ns2) or (ns1 == 0 and ns2 == 0)

# Test: rdsysns returns increasing values (wait longer than in original)
def test_public_rdsysns_increasing():
    ns1 = TSCNS.rdsysns()
    time.sleep(0.004)
    ns2 = TSCNS.rdsysns()
    assert ns2 >= ns1

# Test: getTscGhz with different init params
def test_public_getTscGhz():
    tscns = TSCNS()
    tscns.init(200_000, 60_000_000)
    ghz = tscns.getTscGhz()
    assert isinstance(ghz, float)

# Test: static methods again with larger sleep
def test_public_static_methods():
    sysns1 = TSCNS.rdsysns()
    time.sleep(0.005)
    sysns2 = TSCNS.rdsysns()
    assert sysns2 >= sysns1

# Test: syncTime works
def test_public_syncTime():
    tsc = [123]
    ns = [456]
    TSCNS.syncTime(tsc, ns)
    # after syncTime, should be ints
    assert isinstance(tsc[0], int)
    assert isinstance(ns[0], int)

# Test: multiple calibrations with different interval
def test_public_multiple_calibrations():
    tscns = TSCNS()
    tscns.init(765_432, 500_000)
    tscns.calibrate(True)
    time.sleep(0.004)
    tscns.calibrate(False)

# Test: edge of force calibration with new params
def test_public_force_calibration_edge():
    tscns = TSCNS()
    tscns.init(2, 2)
    tscns.calibrate(True)
    time.sleep(0.002)
    tscns.calibrate(True)

# Test: min_wait_ns edge with new values
def test_public_min_wait_ns_edge():
    tscns = TSCNS()
    tscns.init(2, 2_000_000)
    tsc = TSCNS.rdtsc()
    ns_tsc = tscns.tsc2ns(tsc + 2_000)
    assert isinstance(ns_tsc, int)
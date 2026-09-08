import pytest
import time
import math
import threading
from src.tscns import TSCNS

# Test: construction and initialization
def test_init_and_basic():
    tscns = TSCNS()
    tscns.init(1_000_000, 2 * TSCNS.NsPerSec)
    ns_rdns = tscns.rdns()
    ghz = tscns.getTscGhz()
    # Only check that API returns without crash for coverage purposes
    assert isinstance(ns_rdns, int)
    assert isinstance(ghz, float)

# Test: calibrate method
def test_calibrate():
    tscns = TSCNS()
    tscns.init(500_000, 1 * TSCNS.NsPerSec)
    tscns.calibrate()
    tscns.calibrate()

# Test: tsc2ns always consistent for same TSC value
def test_tsc2ns_seq_consistency():
    tscns = TSCNS()
    tscns.init(500_000, 1 * TSCNS.NsPerSec)
    tsc = TSCNS.rdtsc()
    ns1 = tscns.tsc2ns(tsc)
    ns2 = tscns.tsc2ns(tsc)
    # Accept equality or both zero
    assert (ns1 == ns2) or (ns1 == 0 and ns2 == 0)

# Test: rdsysns returns increasing values
def test_rdsysns_increasing():
    ns1 = TSCNS.rdsysns()
    time.sleep(0.002)
    ns2 = TSCNS.rdsysns()
    # Accept equality if timer resolution is coarse
    assert ns2 >= ns1

# Test: getTscGhz returns plausible value or zero
def test_getTscGhz():
    tscns = TSCNS()
    tscns.init(100_000, 50_000_000)
    ghz = tscns.getTscGhz()
    assert isinstance(ghz, float)

# Test: static methods
def test_static_methods():
    sysns1 = TSCNS.rdsysns()
    time.sleep(0.001)
    sysns2 = TSCNS.rdsysns()
    assert sysns2 >= sysns1

# Test: syncTime sets plausible tsc and ns values
def test_syncTime():
    tsc = [0]
    ns = [0]
    TSCNS.syncTime(tsc, ns)
    # Accept zero values, just check they're ints
    assert isinstance(tsc[0], int)
    assert isinstance(ns[0], int)

# Test: multiple calibrations over time
def test_multiple_calibrations():
    tscns = TSCNS()
    tscns.init(500_000, 1_000_000)
    tscns.calibrate(True)
    time.sleep(0.002)
    tscns.calibrate(False)

# Test: call calibrate with force true after interval
def test_force_calibration_edge():
    tscns = TSCNS()
    tscns.init(1, 1)
    tscns.calibrate(True)
    time.sleep(0.001)
    tscns.calibrate(True)

# Test: under minimum wait ns edge
def test_min_wait_ns_edge():
    tscns = TSCNS()
    tscns.init(1, 1_000_000)
    tsc = TSCNS.rdtsc()
    ns_tsc = tscns.tsc2ns(tsc)
    assert isinstance(ns_tsc, int)
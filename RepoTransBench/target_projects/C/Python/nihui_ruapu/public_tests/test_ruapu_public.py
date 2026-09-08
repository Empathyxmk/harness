import pytest
from src.ruapu_module import ruapu

def test_supports_known_public():
    """
    Public test: Tests calling ruapu_supports with different common ISA names.
    Similar to the original test, it mainly ensures the function runs.
    """
    ruapu.ruapu_init()
    # Different ISAs compared to the original test
    ruapu.ruapu_supports("sse2")
    ruapu.ruapu_supports("avx512f")
    ruapu.ruapu_supports("sha1")
    ruapu.ruapu_supports("sm4")
    # As with the original test, no explicit assertion on return value
    # because the C test only called the function for coverage.


def test_supports_unknown_public():
    """
    Public test: Tests ruapu_supports with another unrecognized ISA name,
    expecting it to return 0.
    """
    ruapu.ruapu_init()
    not_found = ruapu.ruapu_supports("foobar_unknown_isa")
    assert not_found == 0, "Unknown ISA should not be supported"


def test_rua_public():
    """
    Public test: Tests the ruapu_rua function, ensuring it returns a non-empty,
    valid list of supported ISAs, with a different defensive check limit.
    """
    ruapu.ruapu_init()
    arr = ruapu.ruapu_rua()
    assert arr is not None, "ruapu_rua should not return None"
    
    # Similar checks to the original, but with a different defensive limit.
    assert isinstance(arr, list), "ruapu_rua should return a list"
    assert len(arr) > 0, "ruapu_rua should return at least some ISAs"
    assert len(arr) < 1024, "Defensive check: list of ISAs should not exceed 1024"
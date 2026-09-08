import pytest
from src.ruapu_module import ruapu

def test_supports_known():
    """
    Tests calling ruapu_supports with common ISA names.
    The C test doesn't assert return values here, just ensures the function runs.
    """
    ruapu.ruapu_init()
    # These calls simulate the C test's calls; no specific assertion on return value
    # as the original C test only called the function for coverage.
    ruapu.ruapu_supports("sse")
    ruapu.ruapu_supports("avx2")
    ruapu.ruapu_supports("aes")
    # For a robust test, you might check if they are actually 1,
    # but that would depend on the mock's internal state.
    # The current mock makes them return 1, so explicit checks would be:
    # assert ruapu.ruapu_supports("sse") == 1


def test_supports_unknown():
    """
    Tests ruapu_supports with an unrecognized ISA name, expecting it to return 0.
    """
    ruapu.ruapu_init()
    not_found = ruapu.ruapu_supports("not_a_real_isa")
    assert not_found == 0, "Unrecognized ISA should not be supported"


def test_rua():
    """
    Tests the ruapu_rua function, ensuring it returns a non-empty,
    valid list of supported ISAs.
    """
    ruapu.ruapu_init()
    arr = ruapu.ruapu_rua()
    assert arr is not None, "ruapu_rua should not return None"
    
    # The original C test checks for null-termination and a defensive count limit.
    # In Python, we check that it's a list and its length is within a reasonable bound.
    assert isinstance(arr, list), "ruapu_rua should return a list"
    assert len(arr) > 0, "ruapu_rua should return at least some ISAs"
    assert len(arr) < 512, "Defensive check: list of ISAs should not exceed 512"
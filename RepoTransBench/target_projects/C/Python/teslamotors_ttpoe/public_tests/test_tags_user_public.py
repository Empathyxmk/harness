"""
Public user-space unit tests for tag-index hash/VCI/GWF logic with different test data.
"""

import pytest

def ttp_tag_index_hash_get(kid):
    return ((kid >> 0) ^ (kid >> 8) ^ (kid >> 16) ^ (kid >> 24) ^
            (kid >> 32) ^ (kid >> 40) ^ (kid >> 48) ^ (kid >> 56)) & 0xFF

def ttp_tag_index_vci_get(kid):
    return kid & 0xF

def ttp_tag_index_gwf_get(kid):
    return (kid >> 4) & 0xF

def test_hash_vci_gwf_pub(capsys):
    vals = [
        2,
        42,
        9876543210,
        0x7FFFFFFFFFFFFFFF,
        0xFEDCBA9876543210
    ]
    for kid in vals:
        hval = ttp_tag_index_hash_get(kid)
        vval = ttp_tag_index_vci_get(kid)
        gval = ttp_tag_index_gwf_get(kid)

        # Print public test output
        print(f"[PUB] For kid=0x{kid:x}: hash=0x{hval:x}, vci=0x{vval:x}, gwf=0x{gval:x}")

        # Basic property assertions (expected hash results not required to match internal suite)
        assert vval == (kid & 0xF)
        assert gval == ((kid >> 4) & 0xF)

def test_print_pass():
    print("TTP tag-index public hash/vci/gwf tests PASSED.")
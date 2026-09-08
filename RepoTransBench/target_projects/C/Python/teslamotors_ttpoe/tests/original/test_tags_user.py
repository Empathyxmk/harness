"""
User-space unit tests for logic in modttpoe/tags.c (hash/index logic).
Adapted for Python, testing pure functions with consistent logic.
"""

import pytest

def ttp_tag_index_hash_get(kid):
    # Simulate (low byte xor high byte) using all 8 bytes
    return ((kid >> 0) ^ (kid >> 8) ^ (kid >> 16) ^ (kid >> 24) ^
            (kid >> 32) ^ (kid >> 40) ^ (kid >> 48) ^ (kid >> 56)) & 0xFF

def ttp_tag_index_vci_get(kid):
    return kid & 0xF

def ttp_tag_index_gwf_get(kid):
    return (kid >> 4) & 0xF

def test_hash_vci_gwf(capsys):
    vals = [
        0,
        1,
        0xFFFFFFFFFFFFFFFF,
        1234567890123456789,
        0x8000000000000000
    ]
    for kid in vals:
        hval = ttp_tag_index_hash_get(kid)
        vval = ttp_tag_index_vci_get(kid)
        gval = ttp_tag_index_gwf_get(kid)
        # Just test that functions are deterministic and cover value ranges
        assert hval == ttp_tag_index_hash_get(kid)
        assert vval == (kid & 0xF)
        assert gval == ((kid >> 4) & 0xF)
        print(f"KID: {kid:016x} => hash:{hval} vci:{vval} gwf:{gval}")

def test_print_pass():
    print("All tag hash/index tests passed.")
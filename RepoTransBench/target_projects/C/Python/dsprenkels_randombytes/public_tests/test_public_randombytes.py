# public_tests/test_public_randombytes.py
import pytest
from src.randombytes_mod import randombytes
# Import the fixture from the public_tests conftest
from public_tests.conftest import mock_public_getrandom, _PUBLIC_TEST_PATTERN

# PUBLIC_TEST_PATTERN is already defined in public_tests/conftest.py
# We can directly use it here from the import.

def test_public_randombytes_pattern_19_bytes(mock_public_getrandom):
    """
    Corresponds to the first test in C's `randombytes_public_test.c`.
    Generates 19 bytes and verifies their content against the mocked pattern.
    """
    buf = bytearray(19)
    randombytes(buf, len(buf))
    
    for i in range(19):
        expected_byte = _PUBLIC_TEST_PATTERN[i % len(_PUBLIC_TEST_PATTERN)]
        assert buf[i] == expected_byte, \
            f"Byte {i} mismatch. Expected {expected_byte:02x}, got {buf[i]:02x}"

def test_public_randombytes_pattern_13_bytes(mock_public_getrandom):
    """
    Corresponds to the second test in C's `randombytes_public_test.c`.
    Fills a buffer with a different length (13) and verifies content.
    """
    buf = bytearray(13)
    randombytes(buf, len(buf))
    
    for i in range(13):
        expected_byte = _PUBLIC_TEST_PATTERN[i % len(_PUBLIC_TEST_PATTERN)]
        assert buf[i] == expected_byte, \
            f"Byte {i} mismatch. Expected {expected_byte:02x}, got {buf[i]:02x}"

def test_public_randombytes_overwrite_check(mock_public_getrandom):
    """
    Corresponds to the third test in C's `randombytes_public_test.c`.
    Fills a buffer, changes a byte, calls `randombytes` again, and confirms overwrite.
    """
    buf = bytearray(10)
    
    # Fill with 0xFF to ensure randombytes truly overwrites it
    for i in range(len(buf)):
        buf[i] = 0xFF
    
    randombytes(buf, len(buf))
    
    # Check specific bytes as in the C test, then verify all bytes
    assert buf[0] == _PUBLIC_TEST_PATTERN[0], f"Byte 0 mismatch. Expected {_PUBLIC_TEST_PATTERN[0]:02x}, got {buf[0]:02x}"
    assert buf[3] == _PUBLIC_TEST_PATTERN[3], f"Byte 3 mismatch. Expected {_PUBLIC_TEST_PATTERN[3]:02x}, got {buf[3]:02x}"
    assert buf[6] == _PUBLIC_TEST_PATTERN[6], f"Byte 6 mismatch. Expected {_PUBLIC_TEST_PATTERN[6]:02x}, got {buf[6]:02x}"
    
    # Ensure all bytes are overwritten correctly according to the pattern
    for i in range(len(buf)):
        expected_byte = _PUBLIC_TEST_PATTERN[i % len(_PUBLIC_TEST_PATTERN)]
        assert buf[i] == expected_byte, \
            f"Byte {i} mismatch. Expected {expected_byte:02x}, got {buf[i]:02x}"
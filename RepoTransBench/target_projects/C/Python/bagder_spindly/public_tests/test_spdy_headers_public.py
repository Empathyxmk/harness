# public_tests/test_spdy_headers_public.py
import pytest
from unittest.mock import patch, MagicMock

# Import necessary types/functions from src
from src.spdy_headers import SpdyHeaders, SpindlyPhys, spdy_headers_parse_header

# Mocked spdy_nv_block_inflate_parse for public test
# In C: spdy_nv_block_inflate_parse_mock_public.c defines this.
# It returns -2 for specific inputs (0xABC, 0x321) and 42 otherwise.
def public_mock_spdy_nv_block_inflate_parse(nv_block_ptr, z_in_ptr):
    # Simulate C-style pointer checks using unique object IDs or sentinels
    if nv_block_ptr == (object_abc_sentinel := object()) and z_in_ptr == (object_321_sentinel := object()):
        return -2
    return 42

# We need to explicitly define these sentinel objects at a module level
# or pass them during the test call if we are mimicking C pointer values directly.
# The C test uses literal hex addresses (void*)0xABC, (void*)0x321.
# In Python, we can use distinct objects or hash values if we really want to mimic.
# For simplicity, let's make mock a bit more direct or create actual mock objects with specific IDs if needed.
# Or better, just patch and control the mock's behavior for specific args.

# Using unique objects as "pointers" for the mock
# In the public C test, they use literal addresses like (void*)0xABC.
# In Python, we create distinct objects to represent these unique "pointers".
class MockNvBlockABC:
    pass

class MockZlibIn321:
    pass

# Instantiate them once
mock_nv_block_abc = MockNvBlockABC()
mock_zlib_in_321 = MockZlibIn321()

def _public_mock_spdy_nv_block_inflate_parse_impl(nv_block_actual, z_in_actual):
    """
    The actual implementation for the public mock.
    It checks if the *actual objects passed* match our specific sentinels.
    """
    if nv_block_actual is mock_nv_block_abc and z_in_actual is mock_zlib_in_321:
        return -2
    return 42

@patch('src.spdy_headers.spdy_nv_block_inflate_parse', side_effect=_public_mock_spdy_nv_block_inflate_parse_impl)
def test_spdy_headers_parse_header_public_scenario(mock_inflate_parse):
    """
    Corresponds to tests/test_spdy_headers_public.c.
    Tests specific mock behavior for spdy_nv_block_inflate_parse.
    """
    # Use the distinct objects as "test data"
    headers = SpdyHeaders()
    headers.nv_block = mock_nv_block_abc # Assign our sentinel object
    phys = SpindlyPhys()
    phys.zlib_in = mock_zlib_in_321 # Assign our sentinel object

    # Should return -2, as set in our mock for this input data
    ret = spdy_headers_parse_header(headers, phys)
    assert ret == -2
    mock_inflate_parse.assert_called_once_with(mock_nv_block_abc, mock_zlib_in_321)

    # Reset mock for next assertion, or use separate tests
    mock_inflate_parse.reset_mock()

    # Also test passing NULL (None in Python) to either parameter, should return -1
    assert spdy_headers_parse_header(None, phys) == -1
    assert spdy_headers_parse_header(headers, None) == -1

    # Ensure mock was NOT called for NULL/None scenarios as headers.nv_block is not accessed.
    assert not mock_inflate_parse.called
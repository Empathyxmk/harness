# tests/original/test_spdy_headers.py
import pytest
import sys
from unittest.mock import patch, MagicMock

# Import the necessary structures/functions from src
from src.spdy_headers import SpdyHeaders, SpindlyPhys, SpdyNvBlock, spdy_headers_parse_header
from src.spdy_error import SPDY_ERROR_NONE # Though not directly used, good to have

# Mock the spdy_nv_block_inflate_parse function as it is mocked in the C source.
# The original C test links against spdy_nv_block_inflate_parse_mock.c
# which defines a simple mock. We'll use unittest.mock.patch for this.

# Define the mock function for spdy_nv_block_inflate_parse
# The original C mock simply returns 0
def mock_spdy_nv_block_inflate_parse(nv_block, z_in):
    # This mock is used by the original test_spdy_headers.c
    # In C, it's defined in spdy_nv_block_inflate_parse_mock.c
    # It just returns SPDY_ERROR_NONE (0)
    return 0

@patch('src.spdy_headers.spdy_nv_block_inflate_parse', side_effect=mock_spdy_nv_block_inflate_parse)
def test_spdy_headers_parse_header_success_fn(mock_inflate_parse):
    """
    Corresponds to test_spdy_headers_parse_header_success_fn in C.
    The C test's spdy_nv_block_inflate_parse_mock.c always returns 0.
    """
    block = SpdyNvBlock()
    headers = SpdyHeaders()
    headers.nv_block = block
    phys = SpindlyPhys()
    
    rc = spdy_headers_parse_header(headers, phys)
    
    assert rc == 0
    # Ensure our mock was called
    mock_inflate_parse.assert_called_once_with(block, phys.zlib_in)

def test_spdy_headers_parse_header_null_ptr():
    """
    Corresponds to test_spdy_headers_parse_header_null_ptr in C.
    Tests with NULL pointers, which should return -1.
    """
    rc = spdy_headers_parse_header(None, None)
    assert rc == -1
    
    # Test with one NULL, one valid
    headers = SpdyHeaders()
    phys = SpindlyPhys()
    rc = spdy_headers_parse_header(headers, None) # C test only explicitly checks for NULL, NULL but implies this behavior
    assert rc == -1
    
    rc = spdy_headers_parse_header(None, phys)
    assert rc == -1
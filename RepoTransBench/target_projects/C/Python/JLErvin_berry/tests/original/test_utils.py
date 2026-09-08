import pytest
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from src.utils import safe_strncpy, berry_asprintf

def test_safe_strncpy_normal_fn():
    """Test safe_strncpy with normal input."""
    dest = [None]  # We'll use a list to simulate the destination buffer
    src = "hello"
    result = safe_strncpy(dest, src, 10)
    assert result == "hello"

def test_safe_strncpy_src_longer_than_dest_fn():
    """Test safe_strncpy with source longer than destination."""
    dest = [None]
    src = "longerstring"
    result = safe_strncpy(dest, src, 5)
    assert len(result) == 4  # Size - 1 for null terminator
    # Verify that the result is null-terminated (in Python strings are already null-terminated)
    assert result == src[:4]

def test_safe_strncpy_empty_src_fn():
    """Test safe_strncpy with empty source."""
    dest = [None]
    src = ""
    result = safe_strncpy(dest, src, 4)
    assert result == ""

def test_asprintf_basic_fn():
    """Test berry_asprintf with basic formatting."""
    str_ptr = [None]
    ret = berry_asprintf(str_ptr, "The answer is %d", 42)
    assert ret > 0
    assert str_ptr[0] is not None
    assert str_ptr[0] == "The answer is 42"

def test_asprintf_null_ptr_fn():
    """Test berry_asprintf with null pointer."""
    ret = berry_asprintf(None, "Nothing here")
    assert ret == -1

def test_asprintf_empty_format_fn():
    """Test berry_asprintf with empty format string."""
    str_ptr = [None]
    ret = berry_asprintf(str_ptr, "")
    assert ret == 0
    assert str_ptr[0] is not None
    assert str_ptr[0] == ""
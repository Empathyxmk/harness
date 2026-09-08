import pytest
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.utils import safe_strncpy, berry_asprintf

def test_safe_strncpy_normal_fn_public():
    """Test safe_strncpy with normal input (public test)."""
    dest = [None]
    src = "world!"
    result = safe_strncpy(dest, src, 12)
    assert result == "world!"

def test_safe_strncpy_src_longer_than_dest_fn_public():
    """Test safe_strncpy with source longer than destination (public test)."""
    dest = [None]
    src = "toolongstring"
    result = safe_strncpy(dest, src, 6)
    assert len(result) == 5  # Size - 1 for null terminator
    # Verify that the result is null-terminated (in Python strings are already null-terminated)
    assert result == src[:5]

def test_safe_strncpy_empty_src_fn_public():
    """Test safe_strncpy with empty source (public test)."""
    dest = [None]
    src = ""
    result = safe_strncpy(dest, src, 6)
    assert result == ""

def test_asprintf_basic_fn_public():
    """Test berry_asprintf with basic formatting (public test)."""
    str_ptr = [None]
    ret = berry_asprintf(str_ptr, "Pi approx is %.2f", 3.14)
    assert ret > 0
    assert str_ptr[0] is not None
    assert str_ptr[0] == "Pi approx is 3.14"

def test_asprintf_null_ptr_fn_public():
    """Test berry_asprintf with null pointer (public test)."""
    ret = berry_asprintf(None, "Should be null")
    assert ret == -1

def test_asprintf_empty_format_fn_public():
    """Test berry_asprintf with empty format string (public test)."""
    str_ptr = [None]
    ret = berry_asprintf(str_ptr, "")
    assert ret == 0
    assert str_ptr[0] is not None
    assert str_ptr[0] == ""
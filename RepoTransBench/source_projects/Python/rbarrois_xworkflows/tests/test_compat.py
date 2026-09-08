import sys
import types

def test_import_compat_direct_src():
    from xworkflows import compat
    # u() returns the string as-is
    assert compat.u("abc") == "abc"
    # is_string returns True for str, False otherwise
    assert compat.is_string("test")
    assert not compat.is_string(123)
    assert not compat.is_string(None)

def test_import_compat_from_src_direct():
    # Direct import, handles if src is in PYTHONPATH correctly
    import importlib
    compat = importlib.import_module("xworkflows.compat")
    assert compat.u("def") == "def"
    assert compat.is_string("abc")
    assert not compat.is_string([])

def test_python2_mode_equivalence():
    # Simulate both branches of is_string if code supports both str and unicode (for legacy)
    from xworkflows import compat
    # Should always treat str as string in Python 3
    assert compat.is_string(str("hey"))
    assert not compat.is_string(b"bytes")
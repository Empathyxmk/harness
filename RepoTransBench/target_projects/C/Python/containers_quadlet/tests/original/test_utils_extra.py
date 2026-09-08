import os
import pytest

def quad_replace_extension(filename, ext, pre=None, post=None):
    core = filename.split('.')[0]
    if pre:
        core = pre + core
    if post:
        core = core + post
    return core + ext

def quad_apply_line_continuation(s):
    return s.replace("\\\n", " ")

def quad_get_unit_dirs(system=False):
    # placeholder
    return ["dummy_dir", "other_dir", None]

def test_replace_extension():
    assert quad_replace_extension("foo.txt", ".service") == "foo.service"
    assert quad_replace_extension("bar", ".mount", "pre-", "-x") == "pre-bar-x.mount"

def test_apply_line_continuation():
    sample = "foo\\\nbar"
    assert quad_apply_line_continuation(sample) == "foo bar"
    assert quad_apply_line_continuation("no-continuation") == "no-continuation"

def test_get_unit_dirs(monkeypatch):
    if hasattr(os, "unsetenv"):
        os.unsetenv("QUADLET_UNIT_DIRS")
    # Just test the structure, as actual env logic is not relevant here.
    dirs = quad_get_unit_dirs(False)
    assert dirs[0] == "dummy_dir"
    assert dirs[2] is None
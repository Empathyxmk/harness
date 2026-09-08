import os
import sys
import tempfile

import pytest

from pre_commit_hooks import string_fixer

def test_handle_match_triple_quotes():
    # Should return unchanged
    s = '"""abc"""'
    assert string_fixer.handle_match(s) == s
    s2 = "'''abc'''"
    assert string_fixer.handle_match(s2) == s2

def test_handle_match_start_quote():
    # No ' or " in meat
    s = 'u"foobar"'
    out = string_fixer.handle_match(s)
    # Should become u'foobar'
    assert out == "u'foobar'"
    # Something with both ' and " stays unchanged
    s = 'u"foo\'bar"'
    assert string_fixer.handle_match(s) == s

def test_handle_match_not_matched():
    # Should return unchanged if regex doesn't match
    s = 'nonstringtoken'
    assert string_fixer.handle_match(s) == s

def test_get_line_offsets_by_line_no():
    src = "a\nb\n"
    res = string_fixer.get_line_offsets_by_line_no(src)
    assert res[0] == -1
    assert res[-1] == 4

def test_fix_strings_changes(tmp_path):
    # Should rewrite u"foo" to u'foo'
    file = tmp_path / "f.py"
    file.write_text('a = u"foo"\n')
    ret = string_fixer.fix_strings(str(file))
    assert ret == 1
    # File is now fixed
    assert file.read_text().strip().endswith("u'foo'")

def test_fix_strings_no_change(tmp_path):
    file = tmp_path / "nochange.py"
    file.write_text("s = '''abc'''\n")
    ret = string_fixer.fix_strings(str(file))
    assert ret == 0

def test_main_writes(capsys, tmp_path):
    file = tmp_path / "m1.py"
    file.write_text('a = u"f"\n')
    ret = string_fixer.main([str(file)])
    out = capsys.readouterr().out
    assert "Fixing strings" in out
    assert ret == 1

def test_main_no_change(tmp_path, capsys):
    file = tmp_path / "notouch.py"
    file.write_text("s = '''abc'''\n")
    ret = string_fixer.main([str(file)])
    out = capsys.readouterr().out
    assert "Fixing strings" not in out
    assert ret == 0
import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from findup_sync.findup_sync import findup

def basename(path):
    return os.path.basename(path)

def dirname(path):
    return os.path.dirname(path)

def test_should_throw_TypeError_if_patterns_not_string_or_array():
    for bad in [False, None]:
        with pytest.raises(TypeError):
            findup(bad)

def test_should_return_correct_file_when_searching_by_string_filename_different_file():
    fixtures_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../test/fixtures'))
    alt_nested_dir = os.path.join(fixtures_dir, 'a', 'b', 'c', 'd', 'e', 'f', 'g')
    file_to_find = 'g.txt'
    cwd = alt_nested_dir
    result = findup(file_to_find, {'cwd': cwd})
    assert result, "Result is falsy"
    assert basename(result) == file_to_find
    assert os.path.exists(result)

def test_should_return_null_when_file_does_not_exist_other_file():
    fixtures_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../test/fixtures'))
    alt_nested_dir = os.path.join(fixtures_dir, 'a', 'b', 'c', 'd', 'e', 'f', 'g')
    result = findup('definitely-not-found-abc.md', {'cwd': alt_nested_dir})
    assert result is None

def test_should_match_glob_pattern_any_md_file():
    fixtures_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../test/fixtures'))
    cwd = os.path.join(fixtures_dir, 'a', 'b')
    glob_pattern = '*.md'
    result = findup(glob_pattern, {'cwd': cwd})
    assert result.endswith('.md')
    assert os.path.exists(result)
    assert basename(result) == 'a.md'

def test_should_match_one_of_patterns_in_array_new_choices():
    fixtures_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../test/fixtures'))
    cwd = os.path.join(fixtures_dir, 'a', 'b', 'c')
    files = ['no-such-file.nop', 'ONE.txt']
    result = findup(files, {'cwd': cwd})
    assert result, "No match found"
    assert basename(result) == 'ONE.txt'
    assert os.path.exists(result)

def test_should_support_absolute_cwd_alternative_dir():
    fixtures_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../test/fixtures'))
    cwd = os.path.abspath(os.path.join(fixtures_dir, 'a', 'b', 'c', 'd', 'e'))
    result = findup('e.txt', {'cwd': cwd})
    assert result
    assert basename(result) == 'e.txt'

def test_should_support_empty_patterns_array_different_directory():
    fixtures_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../test/fixtures'))
    cwd = os.path.join(fixtures_dir, 'a', 'b')
    result = findup([], {'cwd': cwd})
    assert result is None

def test_should_ignore_fs_readdirSync_errors_and_return_none_simulated(monkeypatch):
    fixtures_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../test/fixtures'))
    cwd = os.path.join(fixtures_dir, 'a', 'b')
    def fake_listdir(_):
        raise OSError("Simulated readdir error")
    monkeypatch.setattr(os, "listdir", fake_listdir)
    res = findup(['*.md'], {'cwd': cwd})
    assert res is None

def test_should_not_infinite_loop_at_filesystem_root_search_different_extension():
    root = os.path.abspath(os.sep)
    result = findup('not-exist-root-file.zzz', {'cwd': root})
    assert result is None
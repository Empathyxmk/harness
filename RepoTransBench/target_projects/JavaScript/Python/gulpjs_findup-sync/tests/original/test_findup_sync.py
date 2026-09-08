import os
import sys
import platform
import pytest
import pathlib

import types

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))
from findup_sync.findup_sync import findup

# ------------- Helper functions/classes -------------

def normalize(path):
    """Return path relative to the project root, using `/` as separator."""
    if not path:
        return None
    p = os.path.relpath(path, start=os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
    return p.replace(os.sep, '/')

def is_path(p):
    # Like expect(actual).isPath()
    return isinstance(p, str) and os.path.exists(p)

def basename(path):
    return os.path.basename(path)

def dirname(path):
    return os.path.dirname(path)

def home():
    # Replace homedir-polyfill
    return os.path.expanduser("~")

def resolve(pkg_name):
    # Simulates require.resolve, but only for installed packages
    import importlib.util
    spec = importlib.util.find_spec(pkg_name)
    if spec is None or not spec.origin:
        raise ImportError("Package %s not found" % pkg_name)
    return spec.origin

def chdir(target_dir):
    """Context manager to temporarily change cwd like JS support.chdir()."""
    old_dir = os.getcwd()
    os.chdir(target_dir)
    def restore():
        os.chdir(old_dir)
    return restore

def npm(module_name):
    # Simulates support.npm() -- returns top-level package directory for module_name
    # This won't work for JS modules but used in path context only
    if module_name == "micromatch":
        # Path in test/fixtures/ for test to work
        return os.path.abspath(os.path.join(os.path.dirname(__file__), "../../test/fixtures/a/b/c/d/e/f/g"))
    elif module_name == "is-glob":
        return os.path.abspath(os.path.join(os.path.dirname(__file__), "../../test/fixtures/a/b/c/d/e/f/g"))
    elif module_name == "normalize-path":
        return os.path.abspath(os.path.join(os.path.dirname(__file__), "../../test/fixtures/a/b/c/d/e/f/g"))
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "../../test/fixtures/"))

class ExtraAssertions:
    def assertBasename(self, p, expected):
        assert basename(p) == expected, f"{basename(p)!r} != {expected!r}"
    def assertDirname(self, p, expected):
        assert dirname(normalize(p)) == expected or normalize(dirname(p)) == expected, \
            f"{dirname(normalize(p))!r} != {expected!r}"
    def assertIsPath(self, p):
        assert is_path(p), f"Value {p!r} is not a valid filesystem path"

extra = ExtraAssertions()

isLinux = platform.system() == "Linux"
__here__ = os.path.abspath(os.path.dirname(__file__))

# ------------- Test suite -------------

@pytest.fixture(scope="module", autouse=True)
def manage_home_files():
    # Setup like JS before/after
    a_file = os.path.join(home(), "_aaa.txt")
    b_file = os.path.join(home(), "_bbb.txt")
    with open(a_file, "w") as f:
        f.write("")
    with open(b_file, "w") as f:
        f.write("")
    yield
    os.remove(a_file)
    os.remove(b_file)

def test_throws_when_first_arg_not_string_or_array():
    for invalid in [None, 123, {}, ()]:
        with pytest.raises(TypeError):
            findup(invalid)

def test_work_when_no_cwd_given():
    actual = findup('package.json')
    assert actual, "Result is falsy"
    expected_dir = os.path.abspath(os.path.join(__here__, '../../'))
    extra.assertDirname(actual, expected_dir)
    extra.assertBasename(actual, 'package.json')
    assert normalize(actual).endswith('package.json')
    assert os.path.exists(actual)

def test_find_files_in_child_directory():
    expected = os.path.abspath(os.path.join(__here__, '../fixtures/a/b/file.txt'))
    restore = chdir(os.path.join(__here__, '../fixtures/a/b/c/d/e/f/g/h'))
    actual = findup('a/b/file.txt')
    assert actual
    assert os.path.exists(actual)
    assert os.path.abspath(actual) == expected
    restore()

def test_find_case_sensitive_files_in_child_directory():
    filename = 'Mochafile.txt' if isLinux else 'mochafile.txt'
    expected = os.path.abspath(os.path.join(__here__, '../fixtures/a/b/', filename))
    restore = chdir(os.path.join(__here__, '../fixtures/a/b/c/d/e/f/g/h'))
    actual = findup(f'a/b/mochafile.txt', {'nocase': True})
    assert actual
    assert os.path.exists(actual)
    assert os.path.abspath(actual) == expected
    restore()

def test_find_files_in_child_directory_relative_to_cwd():
    expected_file = os.path.abspath(os.path.join(__here__, '../fixtures/a/b/file.txt'))
    expected_a = os.path.abspath(os.path.join(__here__, '../fixtures/a/a.txt'))
    tempDir = chdir(os.path.join(__here__, '../fixtures'))
    actual_file = findup('a/b/file.txt', {'cwd': 'a/b/c/d'})
    assert actual_file
    assert os.path.exists(actual_file)
    assert os.path.abspath(actual_file) == expected_file
    actual_a = findup('a.txt', {'cwd': 'a/b/c/d/e/f'})
    assert actual_a
    assert os.path.exists(actual_a)
    assert os.path.abspath(actual_a) == expected_a
    tempDir()

def test_find_case_sensitive_files_in_child_directory_relative_to_cwd():
    filename = 'Mochafile.txt' if isLinux else 'mochafile.txt'
    expected_file = os.path.abspath(os.path.join(__here__, '../fixtures/a/b', filename))
    expected_a = os.path.abspath(os.path.join(__here__, '../fixtures/a/a.txt'))
    tempDir = chdir(os.path.join(__here__, '../fixtures'))
    actual_file = findup('a/b/mochafile.txt', {'cwd': 'a/b/c/d', 'nocase': True})
    assert actual_file
    assert os.path.exists(actual_file)
    assert os.path.abspath(actual_file) == expected_file
    actual_a = findup('a.txt', {'cwd': 'a/b/c/d/e/f'})
    assert actual_a
    assert os.path.exists(actual_a)
    assert os.path.abspath(actual_a) == expected_a
    tempDir()

def test_supports_normal_non_glob_file_paths():
    # These mimic node module dirs, so just check they don't fail in fixture
    normPath = normalize(findup('package.json', {'cwd': os.path.dirname(npm('normalize-path'))}))
    assert normPath.endswith('package.json')
    isGlob = normalize(findup('package.json', {'cwd': os.path.dirname(npm('is-glob'))}))
    assert isGlob.endswith('package.json')

    cwd = os.path.dirname(npm('normalize-path'))
    actual = findup('package.json', {'cwd': cwd})
    extra.assertDirname(actual, cwd)
    extra.assertBasename(actual, 'package.json')

    actual = findup('c/package.json', {'cwd': 'test/fixtures/a/b/c/d/e/f/g'})
    extra.assertBasename(actual, 'package.json')
    extra.assertDirname(actual, 'test/fixtures/a/b/c')

    cwd = os.path.dirname(npm('is-glob'))
    actual = findup('package.json', {'cwd': cwd})
    extra.assertDirname(actual, cwd)
    extra.assertBasename(actual, 'package.json')

def test_supports_normal_non_glob_case_sensitive():
    actual = findup('c/mochafile.txt', {'cwd': 'test/fixtures/a/b/c/d/e/f/g', 'nocase': True})
    expected_fn = 'Mochafile.txt' if isLinux else 'mochafile.txt'
    extra.assertBasename(actual, expected_fn)
    extra.assertDirname(actual, 'test/fixtures/a/b/c')

def test_supports_glob_patterns():
    norm = normalize(findup('**/c/package.json', {'cwd': 'test/fixtures/a/b/c/d/e/f/g'}))
    assert norm == 'test/fixtures/a/b/c/package.json'
    norm = normalize(findup('**/one.txt', {'cwd': 'test/fixtures/a/b/c/d/e/f/g'}))
    assert norm == 'test/fixtures/a/b/c/d/one.txt'
    norm = normalize(findup('**/two.txt', {'cwd': 'test/fixtures/a/b/c/d/e/f/g'}))
    assert norm == 'test/fixtures/a/b/c/two.txt'

    pkg = normalize(findup('p*.json', {'cwd': npm('micromatch')}))
    assert pkg.endswith('package.json')

    opts = {'cwd': 'test/fixtures/a/b/c/d/e/f/g'}
    actual = findup('**/c/package.json', opts)
    extra.assertDirname(actual, 'test/fixtures/a/b/c')
    extra.assertBasename(actual, 'package.json')
    actual = findup('c/package.json', opts)
    extra.assertDirname(actual, 'test/fixtures/a/b/c')
    extra.assertBasename(actual, 'package.json')
    actual = findup('**/ONE.txt', opts)
    extra.assertDirname(actual, 'test/fixtures/a/b/c')
    extra.assertBasename(actual, 'ONE.txt')
    actual = findup('**/two.txt', opts)
    extra.assertDirname(actual, 'test/fixtures/a/b/c')
    extra.assertBasename(actual, 'two.txt')
    cwd = npm('is-glob')
    actual = findup('p*.json', {'cwd': cwd})
    extra.assertDirname(actual, cwd)
    extra.assertBasename(actual, 'package.json')

def test_supports_case_sensitive_glob_patterns():
    norm = normalize(findup('**/c/mochafile.txt', {'cwd': 'test/fixtures/a/b/c/d/e/f/g', 'nocase': True}))
    assert norm == 'test/fixtures/a/b/c/Mochafile.txt'
    norm = normalize(findup('**/one.txt', {'cwd': 'test/fixtures/a/b/c/d/e/f/g', 'nocase': True}))
    assert norm == 'test/fixtures/a/b/c/d/one.txt'
    norm = normalize(findup('**/two.txt', {'cwd': 'test/fixtures/a/b/c/d/e/f/g', 'nocase': True}))
    assert norm == 'test/fixtures/a/b/c/two.txt'
    norm = normalize(findup('mocha*', {'cwd': 'test/fixtures/a/b/c', 'nocase': True}))
    assert norm == 'test/fixtures/a/b/c/Mochafile.txt'

    opts = {'cwd': 'test/fixtures/a/b/c/d/e/f/g', 'nocase': True}
    actual = findup('**/c/mochafile.txt', opts)
    extra.assertDirname(actual, 'test/fixtures/a/b/c')
    extra.assertBasename(actual, 'Mochafile.txt')
    actual = findup('c/mochafile.txt', opts)
    expected_fn = 'Mochafile.txt' if isLinux else 'mochafile.txt'
    extra.assertDirname(actual, 'test/fixtures/a/b/c')
    extra.assertBasename(actual, expected_fn)
    opts['nocase'] = False
    actual = findup('**/ONE.txt', opts)
    extra.assertDirname(actual, 'test/fixtures/a/b/c')
    extra.assertBasename(actual, 'ONE.txt')
    actual = findup('**/two.txt', opts)
    extra.assertDirname(actual, 'test/fixtures/a/b/c')
    extra.assertBasename(actual, 'two.txt')

def test_supports_arrays_of_glob_patterns():
    norm = normalize(findup(['**/c/package.json'], {'cwd': 'test/fixtures/a/b/c/d/e/f/g'}))
    assert norm == 'test/fixtures/a/b/c/package.json'
    norm = normalize(findup(['**/one.txt'], {'cwd': 'test/fixtures/a/b/c/d/e/f/g'}))
    assert norm == 'test/fixtures/a/b/c/d/one.txt'
    norm = normalize(findup(['**/two.txt'], {'cwd': 'test/fixtures/a/b/c/d/e/f/g'}))
    assert norm == 'test/fixtures/a/b/c/two.txt'

    opts = {'cwd': 'test/fixtures/a/b/c/d/e/f/g'}
    actual = findup(['lslsl', '**/c/package.json'], opts)
    extra.assertDirname(actual, 'test/fixtures/a/b/c')
    extra.assertBasename(actual, 'package.json')
    actual = findup(['lslsl', 'c/package.json'], opts)
    extra.assertDirname(actual, 'test/fixtures/a/b/c')
    extra.assertBasename(actual, 'package.json')
    actual = findup(['lslsl', '**/ONE.txt'], opts)
    extra.assertDirname(actual, 'test/fixtures/a/b/c')
    extra.assertBasename(actual, 'ONE.txt')
    actual = findup(['lslsl', '**/two.txt'], opts)
    extra.assertDirname(actual, 'test/fixtures/a/b/c')
    extra.assertBasename(actual, 'two.txt')
    actual = findup(['lslsl', '**/blah.txt'], opts)
    assert actual is None
    cwd = npm('is-glob')
    actual = findup(['lslsl', 'p*.json'], {'cwd': cwd})
    extra.assertDirname(actual, cwd)
    extra.assertBasename(actual, 'package.json')

def test_supports_micromatch_matchBase_option():
    opts = {'matchBase': True, 'cwd': 'test/fixtures/a/b/c/d/e/f/g'}
    norm = normalize(findup('package.json', opts))
    assert norm == 'test/fixtures/a/b/c/d/e/f/g/package.json'
    norm = normalize(findup('one.txt', opts))
    assert norm == 'test/fixtures/a/b/c/d/one.txt'
    norm = normalize(findup('two.txt', opts))
    assert norm == 'test/fixtures/a/b/c/two.txt'
    actual = findup('package.json', opts)
    extra.assertBasename(actual, 'package.json')
    extra.assertDirname(actual, 'test/fixtures/a/b/c/d/e/f/g')
    actual = findup('one.txt', opts)
    extra.assertBasename(actual, 'one.txt')
    extra.assertDirname(actual, 'test/fixtures/a/b/c/d')
    actual = findup('two.txt', opts)
    extra.assertBasename(actual, 'two.txt')
    extra.assertDirname(actual, 'test/fixtures/a/b/c')

def test_returns_null_when_no_files_found():
    dep = normalize(findup('*.foo', {'cwd': os.path.dirname(npm('micromatch'))}))
    assert dep is None
    assert findup('**/b*.json', {'cwd': npm('is-glob')}) is None
    assert findup('foo.json', {'cwd': 'test/fixtures/a/b/c/d/e/f/g'}) is None
    assert findup('foo.json', {'cwd': 'test/fixtures/a/b/c/d/e/f/g', 'matchBase': True}) is None

def test_support_finding_file_in_immediate_parent_dir():
    cwd = os.path.abspath(os.path.join(__here__, '../fixtures/a/b/c'))
    actual = findup('a.md', {'cwd': cwd})
    extra.assertDirname(actual, os.path.dirname(cwd))
    extra.assertBasename(actual, 'a.md')

def test_supports_micromatch_nocase_option():
    actual = findup('ONE.*', {'cwd': 'test/fixtures/a/b/c/d'})
    extra.assertBasename(actual, 'ONE.txt')
    extra.assertDirname(actual, 'test/fixtures/a/b/c')
    actual = findup('ONE.*', {'cwd': 'test/fixtures/a/b/c/d', 'nocase': True})
    extra.assertBasename(actual, 'one.txt')
    extra.assertDirname(actual, 'test/fixtures/a/b/c/d')

def test_finds_files_from_absolute_paths():
    actual = findup('package.json', {'cwd': __here__})
    extra.assertBasename(actual, 'package.json')
    extra.assertDirname(actual, os.path.abspath(os.path.join(__here__, '..')))
    actual = findup('one.txt', {'cwd': os.path.join(__here__, 'fixtures/a')})
    extra.assertBasename(actual, 'one.txt')
    extra.assertDirname(actual, 'test/fixtures/a')
    actual = findup('two.txt', {'cwd': os.path.join(__here__, 'fixtures/a/b/c')})
    extra.assertBasename(actual, 'two.txt')
    extra.assertDirname(actual, 'test/fixtures/a/b/c')

def test_finds_files_in_user_home():
    actual = findup('*', {'cwd': home()})
    extra.assertIsPath(actual)
    assert os.path.exists(actual)
    extra.assertDirname(actual, home())

def test_finds_files_in_user_home_using_tilde():
    actual = findup('*', {'cwd': '~'})
    extra.assertIsPath(actual)
    assert os.path.exists(actual)
    extra.assertDirname(actual, home())

def test_match_files_in_cwd_before_searching_up():
    actual = findup(['a.txt', 'a.md'], {'cwd': os.path.join(__here__, 'fixtures/a/b')})
    extra.assertBasename(actual, 'a.md')
    extra.assertDirname(actual, 'test/fixtures/a/b')

# ---------- Translated from test/findup-sync.spec.js ----------

def test_should_throw_TypeError_if_patterns_not_string_or_array():
    for bad in [None, 123, {}]:
        with pytest.raises(TypeError):
            findup(bad)

def test_should_return_correct_file_when_searching_by_string_filename():
    fixtures_dir = os.path.join(__here__, '../fixtures')
    nested_dir = os.path.join(fixtures_dir, 'a/b/c/d/e/f/g/h')
    file_to_find = 'file.txt'
    cwd = nested_dir
    result = findup(file_to_find, {'cwd': cwd})
    assert result, "Result is falsy"
    assert basename(result) == file_to_find
    assert os.path.exists(result)

def test_should_return_null_when_file_does_not_exist():
    fixtures_dir = os.path.join(__here__, '../fixtures')
    nested_dir = os.path.join(fixtures_dir, 'a/b/c/d/e/f/g/h')
    result = findup('nonexistent-file-xyz.txt', {'cwd': nested_dir})
    assert result is None

def test_should_match_glob_pattern_any_txt_file():
    fixtures_dir = os.path.join(__here__, '../fixtures')
    nested_dir = os.path.join(fixtures_dir, 'a/b/c/d/e/f/g/h')
    glob_pattern = '*.txt'
    result = findup(glob_pattern, {'cwd': nested_dir})
    assert result.endswith('.txt')
    assert os.path.exists(result)

def test_should_match_one_of_patterns_in_array():
    fixtures_dir = os.path.join(__here__, '../fixtures')
    nested_dir = os.path.join(fixtures_dir, 'a/b/c/d/e/f/g/h')
    files = ['nope.nope', 'file.txt']
    result = findup(files, {'cwd': nested_dir})
    assert result, "No .txt found"
    assert basename(result) == 'file.txt'
    assert os.path.exists(result)

def test_should_support_absolute_cwd():
    fixtures_dir = os.path.join(__here__, '../fixtures')
    nested_dir = os.path.join(fixtures_dir, 'a/b/c/d/e/f/g/h')
    cwd = os.path.abspath(nested_dir)
    result = findup('file.txt', {'cwd': cwd})
    assert result
    assert basename(result) == 'file.txt'

def test_should_support_empty_patterns_array():
    fixtures_dir = os.path.join(__here__, '../fixtures')
    nested_dir = os.path.join(fixtures_dir, 'a/b/c/d/e/f/g/h')
    result = findup([], {'cwd': nested_dir})
    assert result is None

def test_should_ignore_fs_readdirSync_errors_and_return_none(monkeypatch):
    fixtures_dir = os.path.join(__here__, '../fixtures')
    nested_dir = os.path.join(fixtures_dir, 'a/b/c/d/e/f/g/h')
    def fake_listdir(_):
        raise OSError("Fake error")
    monkeypatch.setattr(os, "listdir", fake_listdir)
    res = findup(['*.txt'], {'cwd': nested_dir})
    assert res is None

def test_should_not_infinite_loop_at_filesystem_root():
    root = os.path.abspath(os.sep)
    result = findup('not-exist.txt', {'cwd': root})
    assert result is None
import os
import shutil
import tempfile
import pytest
import yaml

from tests.filemaker import FilemakerBase, Filemaker, create_files

class DummyFilemaker(FilemakerBase):
    def __init__(self, *a, **k):
        self.trace = []
        super().__init__(*a, **k)

    def goto_root(self, dirname):
        self.trace.append(('goto_root', dirname))

    def makedir(self, dirname, content):
        self.trace.append(('makedir', dirname))
        self.make_list(content)

    def make_file(self, filename, content):
        self.trace.append(('make_file', filename, content))

    def make_empty_file(self, fname):
        self.trace.append(('make_empty_file', fname))

def test_filemakerbase_empty_file(tmp_path):
    fdef = "file1"
    fm = DummyFilemaker(str(tmp_path), fdef)
    assert ('make_empty_file', 'file1') in fm.trace

def test_filemakerbase_make_file_and_dir(tmp_path):
    fdef = """
testdir:
  - file2: "hi"
  - file3
"""
    fm = DummyFilemaker(str(tmp_path), yaml.safe_load(fdef))
    # Should create a dir and a file and an empty file
    found = set(t[0] for t in fm.trace)
    assert 'makedir' in found
    assert 'make_file' in found
    assert 'make_empty_file' in found

def test_filemaker_works(tmp_path):
    fdef = """
d:
  - a: "x"
  - b
"""
    p = os.path.join(tmp_path, "d")
    with create_files(fdef, cleanup=True) as tdir:
        assert os.path.isdir(os.path.join(tdir, "d"))
        assert os.path.isfile(os.path.join(tdir, "d", "a"))
        assert os.path.isfile(os.path.join(tdir, "d", "b"))
    # Dir and files should be cleaned up
    assert not os.path.exists(p)

def test_filemakerbase_invalid_type(tmp_path):
    with pytest.raises(ValueError):
        DummyFilemaker(str(tmp_path), 42)

def test_filemakerbase_invalid_dict(tmp_path):
    class BadFilemaker(FilemakerBase):
        def make_file(self, *a, **k): pass
        def makedir(self, *a, **k): pass
        def make_empty_file(self, *a, **k): pass
        def goto_root(self, *a, **k): pass
    with pytest.raises(ValueError):
        BadFilemaker(str(tmp_path), {"data": None})
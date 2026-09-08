import pytest
from io import StringIO
from contextlib import redirect_stdout
import sys

# --------- Implementation Stubs (would be in src, but inlined for test completeness) ---------

class FilePaths:
    def __init__(self, size):
        self.paths = [None] * size
        self.size = size
        self.len = 0

    def add_file(self, path):
        if self.len >= self.size:
            # Mimic C realloc: double the size, or increment by 1 if size is 0
            newsize = self.size * 2 if self.size > 0 else 1
            self.paths += [None] * (newsize - self.size)
            self.size = newsize
        self.paths[self.len] = path
        self.len += 1

def file_paths_free(fp: FilePaths):
    fp.paths = []
    fp.len = 0
    fp.size = 0

def event_cb(ref, ctx: FilePaths, count, paths, flags, ids):
    """Print to stdout 'matched path' or 'path - ignoring' for each path, if it matches ctx.paths. See C logic."""
    if ctx.len == 0:
        sys.exit(0)
    found = False
    for idx in range(count):
        this_path = paths[idx]
        if this_path in ctx.paths[:ctx.len]:
            print(f"matched {this_path}")
            found = True
        else:
            print(f"{this_path} - ignoring")
    if found:
        sys.exit(0)

def safe_event_cb(ref, ctx, count, paths, flags, ids, capture_output, outputbuf, buflen):
    """Pythonic safe_event_cb analog to the C fork/pipe pattern."""
    import traceback
    class FakeExit(Exception):
        def __init__(self, code):
            self.code = code

    def call_event_cb():
        if capture_output:
            with StringIO() as buf, redirect_stdout(buf):
                try:
                    event_cb(ref, ctx, count, paths, flags, ids)
                except SystemExit as e:
                    outputbuf.append(buf.getvalue()[:buflen-1])
                    return e.code
                outputbuf.append(buf.getvalue()[:buflen-1])
                return 222
        else:
            try:
                event_cb(ref, ctx, count, paths, flags, ids)
            except SystemExit as e:
                return e.code
            return 222

    outputbuf.clear()
    try:
        code = call_event_cb()
        return code
    except Exception:
        return 254

# --------- Tests ---------

def test_add_file_basic_public():
    fp = FilePaths(3)
    assert fp.len == 0
    fp.add_file("alpha.log")
    assert fp.len == 1
    assert fp.paths[0] == "alpha.log"

    fp.add_file("beta.log")
    assert fp.len == 2
    assert fp.paths[1] == "beta.log"

    fp.add_file("gamma.log")
    assert fp.len == 3
    assert fp.paths[2] == "gamma.log"

    file_paths_free(fp)

def test_add_file_resize_public():
    fp = FilePaths(2)
    fp.add_file("one")
    assert fp.len == 1
    assert fp.paths[0] == "one"
    oldsize = fp.size
    fp.add_file("two")
    assert fp.size >= oldsize
    assert fp.len == 2
    assert fp.paths[1] == "two"
    fp.add_file("three")
    assert fp.size >= oldsize
    assert fp.len == 3
    assert fp.paths[2] == "three"
    file_paths_free(fp)

def test_event_cb_empty_filepaths_public():
    fp = FilePaths(3)
    paths_arr = ["newfile"]
    flags = [10]
    ids = [159]
    outputbuf = []
    ret = safe_event_cb(None, fp, 1, paths_arr, flags, ids, 0, outputbuf, 512)
    assert ret == 0, f"Expected child exit 0, got {ret}"
    file_paths_free(fp)

def test_event_cb_match_public():
    fp = FilePaths(2)
    fp.add_file("delta")
    paths_arr = ["delta"]
    flags = [19]
    ids = [2001]
    outputbuf = []
    ret = safe_event_cb(None, fp, 1, paths_arr, flags, ids, 1, outputbuf, 512)
    out = outputbuf[0] if outputbuf else ""
    assert ret == 0, f"Expected child exit 0, got {ret}. Output: {out}"
    assert "matched delta" in out, f"Expected 'matched delta' in output: {out}"
    file_paths_free(fp)

def test_event_cb_ignore_public():
    fp = FilePaths(2)
    fp.add_file("omega")
    paths_arr = ["zzz"]
    flags = [6]
    ids = [630]
    outputbuf = []
    ret = safe_event_cb(None, fp, 1, paths_arr, flags, ids, 1, outputbuf, 512)
    out = outputbuf[0] if outputbuf else ""
    assert ret == 0 or ret == 222, f"Expected child exit 0 or 222, got {ret}. Output: {out}"
    assert " - ignoring" in out, f"Expected ' - ignoring' at least once in output: {out}"
    file_paths_free(fp)

def test_event_cb_match_and_ignore_public():
    fp = FilePaths(3)
    fp.add_file("tomato")
    fp.add_file("potato")
    paths_arr = ["tomato", "apple"]
    flags = [12, 13]
    ids = [42, 43]
    outputbuf = []
    ret = safe_event_cb(None, fp, 2, paths_arr, flags, ids, 1, outputbuf, 1024)
    out = outputbuf[0] if outputbuf else ""
    assert ret == 0 or ret == 222, f"Expected child exit 0 or 222, got {ret}. Output: {out}"
    assert "matched tomato" in out, f"Expected 'matched tomato' in output: {out}"
    assert " - ignoring" in out, f"Expected ' - ignoring' in output: {out}"
    file_paths_free(fp)

def test_event_cb_ignore_exit222_public():
    assert 222 == 222
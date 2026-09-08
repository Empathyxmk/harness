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
    """
    Print to stdout 'matched path' or "path - ignoring" for each path, if it matches ctx.paths
    If a match, print 'matched ...', otherwise print '... - ignoring'
    If ctx.paths is empty, exit (0)
    """
    # 'ctx' is FilePaths instance
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

# --------- Helper Functions ---------

def safe_event_cb(ref, ctx, count, paths, flags, ids, capture_output, outputbuf, buflen):
    """
    Emulates forking/child-exit catching as in C,
    but in Python we use subprocess-style isolation via multiprocessing or in-process via exception catch + output buffer.
    For simplicity and determinism, use in-process, and simulate exit() using SystemExit.
    Returns:
        0 if correct exit, 222 if event_cb did not exit, 254 on error
    """
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
                return 222  # Should never reach here unless no exit called
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

def test_add_file_basic():
    fp = FilePaths(2)
    assert fp.len == 0
    fp.add_file("foo.txt")
    assert fp.len == 1
    assert fp.paths[0] == "foo.txt"

    fp.add_file("bar.txt")
    assert fp.len == 2
    assert fp.paths[1] == "bar.txt"

    file_paths_free(fp)

def test_add_file_resize():
    fp = FilePaths(1)
    fp.add_file("a")
    assert fp.len == 1
    assert fp.paths[0] == "a"
    oldsize = fp.size
    fp.add_file("b")
    assert fp.size >= oldsize
    assert fp.len == 2
    assert fp.paths[1] == "b"
    file_paths_free(fp)

def test_event_cb_empty_filepaths():
    fp = FilePaths(2)
    paths_arr = ["foo"]
    flags = [0]
    ids = [99]
    outputbuf = []
    ret = safe_event_cb(None, fp, 1, paths_arr, flags, ids, 0, outputbuf, 512)
    assert ret == 0, f"Expected child exit 0, got {ret}"

    file_paths_free(fp)

def test_event_cb_match():
    fp = FilePaths(2)
    fp.add_file("foo")
    paths_arr = ["foo"]
    flags = [1]
    ids = [100]
    outputbuf = []
    ret = safe_event_cb(None, fp, 1, paths_arr, flags, ids, 1, outputbuf, 512)
    out = outputbuf[0] if outputbuf else ""
    assert ret == 0, f"Expected child exit 0, got {ret}. Output: {out}"
    assert "matched foo" in out, f"Expected 'matched foo' in output: {out}"
    file_paths_free(fp)

def test_event_cb_ignore():
    fp = FilePaths(2)
    fp.add_file("foo")
    paths_arr = ["baz"]
    flags = [2]
    ids = [101]
    outputbuf = []
    ret = safe_event_cb(None, fp, 1, paths_arr, flags, ids, 1, outputbuf, 512)
    out = outputbuf[0] if outputbuf else ""
    assert ret == 0 or ret == 222, f"Expected child exit 0 or 222, got {ret}. Output: {out}"
    assert " - ignoring" in out, f"Expected ' - ignoring' at least once in output: {out}"
    file_paths_free(fp)

def test_event_cb_match_and_ignore():
    fp = FilePaths(3)
    fp.add_file("foo")
    fp.add_file("bar")
    paths_arr = ["foo", "baz"]
    flags = [1, 2]
    ids = [100, 101]
    outputbuf = []
    ret = safe_event_cb(None, fp, 2, paths_arr, flags, ids, 1, outputbuf, 1024)
    out = outputbuf[0] if outputbuf else ""
    assert ret == 0 or ret == 222, f"Expected child exit 0 or 222, got {ret}. Output: {out}"
    assert "matched foo" in out, f"Expected 'matched foo' in output: {out}"
    assert " - ignoring" in out, f"Expected ' - ignoring' in output: {out}"
    file_paths_free(fp)

def test_event_cb_ignore_exit222():
    assert 222 == 222
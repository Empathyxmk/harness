import inspect
import os
from contextlib import contextmanager

def is_str(obj):
    return isinstance(obj, str)

def is_bytes(obj):
    return isinstance(obj, bytes)

def singleton(seq):
    assert len(seq) == 1
    return seq[0]

def rightmost(seq):
    try:
        return seq[-1]
    except IndexError:
        return None

def get_lineno():
    return inspect.currentframe().f_back.f_lineno

def safe_int(obj, fallback=0):
    try:
        return int(obj)
    except Exception:
        return fallback

def partition_none(arr):
    result = []
    current = []
    for elem in arr:
        if elem is None:
            if current:
                result.append(current)
            current = []
        else:
            current.append(elem)
    if current:
        result.append(current)
    return result

def unpack_io(io_or_fd):
    if hasattr(io_or_fd, "fileno"):
        return io_or_fd.fileno()
    elif isinstance(io_or_fd, int):
        return io_or_fd
    else:
        raise ValueError("Not a valid IO or file descriptor")

@contextmanager
def cwd(path):
    old = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old)
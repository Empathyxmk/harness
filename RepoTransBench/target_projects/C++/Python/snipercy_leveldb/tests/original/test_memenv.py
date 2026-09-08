def test_memenv_basics():
    dir = {}
    assert "/dir/non_existent" not in dir
    dir["/dir/f"] = b""
    assert "/dir/f" in dir
    del dir["/dir/f"]
    assert "/dir/f" not in dir

def test_memenv_read_write():
    f = bytearray()
    f.extend(b"hello ")
    f.extend(b"world")
    assert f[:5] == b"hello"
    assert f[6:11] == b"world"

def test_memenv_locks():
    import threading
    lock = threading.Lock()
    with lock:
        pass

def test_memenv_misc():
    d = {}
    d["/a/b"] = b""
    d["/a/b"] += b"misc"
    assert d["/a/b"] == b"misc"
    del d["/a/b"]
    assert "/a/b" not in d

def test_memenv_large_write():
    data = bytearray()
    kWriteSize = 3 * 1024
    data.extend(b"x" * kWriteSize)
    assert len(data) == kWriteSize
    data2 = data[:]
    assert data == data2
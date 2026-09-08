import pytest

from src.gulp_cached import Cached, File

@pytest.fixture(autouse=True)
def reset_caches(monkeypatch):
    Cached.caches = {}
    yield
    Cached.caches = {}

def make_file(path, contents=None):
    return File(path=path, contents=contents)

def test_should_allow_optimize_memory_and_hash_content():
    plugin = Cached('test-optimise', optimizeMemory=True)
    file = make_file('test/file.txt', b'foo')
    results = []
    plugin.on('data', lambda data: results.append(data))
    plugin.write(file)
    plugin.end()
    assert len(results) == 1
    assert results[0] is file

def test_should_not_add_stream_file():
    plugin = Cached('test-stream')
    file = make_file('stream/file.txt')
    file.isStream = lambda: True
    called = []
    plugin.on('data', lambda data: called.append(data))
    plugin.write(file)
    plugin.end()
    plugin.wait_io()
    assert called, "Should call once for stream file"
    assert called[0] is file

def test_should_support_isbuffer_false():
    plugin = Cached('test-false-buffer')
    file = make_file('buff/file.txt')
    file.isStream = lambda: False
    file.isBuffer = lambda: False
    results = []
    plugin.on('data', lambda data: results.append(data))
    plugin.write(file)
    plugin.end()
    assert any(isinstance(x, File) and x.path == file.path for x in results)

def test_should_handle_checksum_property_and_skip_hashing():
    plugin = Cached('test-checksum')
    buf = b'abc'
    file = make_file('foo/buf2.txt', buf)
    file.checksum = 'dummy-checksum'
    file.isBuffer = lambda: True
    file.isStream = lambda: False

    out = []
    plugin.on('data', lambda d: out.append(d))
    plugin.write(file)
    plugin.end()
    assert any(hasattr(x, "checksum") and getattr(x, "checksum") == "dummy-checksum" for x in out)

def test_should_allow_files_same_path_different_caches():
    plugin1 = Cached('unique1')
    plugin2 = Cached('unique2')
    filePath = 'common/file.txt'
    file1 = make_file(filePath, b'1')
    file2 = make_file(filePath, b'2')
    res1, res2 = [], []
    plugin1.on('data', lambda d: res1.append(d))
    plugin2.on('data', lambda d: res2.append(d))
    plugin1.write(file1)
    plugin2.write(file2)
    plugin1.end()
    plugin2.end()
    assert res1 and res1[0].contents == b'1'
    assert res2 and res2[0].contents == b'2'

def test_should_not_share_cache_if_name_is_falsy():
    pluginA = Cached(None)
    pluginB = Cached(None)
    filePathA = 'falsy/fileA.txt'
    filePathB = 'falsy/fileB.txt'
    fileA = make_file(filePathA, b'x')
    fileB = make_file(filePathB, b'y')
    seenA = []
    seenB = []
    pluginA.on('data', lambda d: seenA.append(d) if d.path == filePathA else None)
    pluginB.on('data', lambda d: seenB.append(d) if d.path == filePathB else None)

    pluginA.write(fileA)
    pluginA.end()
    pluginB.write(fileB)
    pluginB.end()
    assert seenA, "pluginA should let its file through"
    assert seenB, "pluginB should let its file through"

def test_plugin_caches_object_exists():
    assert isinstance(Cached.caches, dict)
    assert Cached.caches is not None

def test_should_only_allow_file_once():
    plugin = Cached('simple')
    file = make_file('foo/file.txt', b'bar')
    calls = []
    plugin.on('data', lambda d: calls.append(d))
    plugin.write(file)
    plugin.write(file)
    plugin.end()
    assert len(calls) == 1
    assert calls[0] is file

def test_should_clear_cache_on_reset():
    plugin = Cached('reset')
    file = make_file('path/file.txt', b'baz')
    cnt = []
    plugin.on('data', lambda _: cnt.append(1))
    plugin.write(file)
    plugin.write(file)  # 2nd write, should be filtered out
    plugin.end()

    # Simulate reset by force overwriting cache
    Cached.caches['reset'] = {}
    plugin2 = Cached('reset')
    cnt2 = []
    plugin2.on('data', lambda _: cnt2.append(1))
    plugin2.write(file)
    plugin2.end()
    assert (len(cnt) + len(cnt2)) == 2

def test_should_create_separate_caches_once_each():
    pluginA = Cached('A')
    pluginB = Cached('B')
    file = make_file('multi/file.txt', b'abc')
    seenA, seenB = [], []
    pluginA.on('data', lambda _: seenA.append(1))
    pluginB.on('data', lambda _: seenB.append(1))
    pluginA.write(file)
    pluginB.write(file)
    pluginA.end()
    pluginB.end()
    assert len(seenA) == 1
    assert len(seenB) == 1

def test_should_allow_stream_file_through_always():
    plugin = Cached('streams')
    file = make_file('stream/yes.txt')
    file.isStream = lambda: True
    cnt = []

    plugin.on('data', lambda f: cnt.append(f))
    plugin.write(file)
    plugin.write(file)
    plugin.end()
    assert len(cnt) == 2
    for f in cnt:
        assert f is file

def test_should_allow_streaming_file_through_always():
    plugin = Cached('streams2')
    file = make_file('stream/yes2.txt')
    file.isStream = lambda: False
    file.isBuffer = lambda: False
    cnt = []
    plugin.on('data', lambda f: cnt.append(f))
    plugin.write(file)
    plugin.write(file)
    plugin.end()
    assert len(cnt) == 2
    for f in cnt:
        assert f is file

def test_should_only_allow_hashed_streaming_file_once():
    plugin = Cached('hashstream')
    file = make_file('hash/stream.txt', b'xyz')
    file.isBuffer = lambda: True
    file.isStream = lambda: False
    cnt = []
    plugin.on('data', lambda f: cnt.append(f))
    plugin.write(file)
    plugin.write(file)  # duplicate
    plugin.end()
    assert len(cnt) == 1
    assert cnt[0] is file
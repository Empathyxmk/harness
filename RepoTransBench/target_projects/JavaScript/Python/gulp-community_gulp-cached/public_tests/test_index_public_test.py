import pytest

from src.gulp_cached import Cached, File

def make_file(path, contents=None):
    return File(path=path, contents=contents)

def test_optimize_memory_and_hash_content():
    plugin = Cached('public-optimise', optimizeMemory=True)
    file = make_file('public/alpha.txt', b'hello world')
    events = []
    plugin.on('data', lambda data: events.append(data))
    plugin.write(file)
    plugin.end()
    assert events
    assert events[0] is file

def test_not_add_stream_file_public():
    plugin = Cached('public-stream')
    file = make_file('public/stream2.txt')
    file.isStream = lambda: True
    called = []
    plugin.on('data', lambda data: called.append(data))
    plugin.write(file)
    plugin.end()
    plugin.wait_io()
    assert called, "Should call once for stream file in public"
    assert called[0] is file

def test_isbuffer_returns_false_public():
    plugin = Cached('public-false-buffer')
    file = make_file('public/specialcase.txt')
    file.isStream = lambda: False
    file.isBuffer = lambda: False
    results = []
    plugin.on('data', lambda data: results.append(data))
    plugin.write(file)
    plugin.end()
    assert any(isinstance(d, File) and d.path == file.path for d in results)

def test_handle_checksum_property_public():
    plugin = Cached('public-checksum')
    buf = b'123xyz'
    file = make_file('bar/buf2.txt', buf)
    file.checksum = 'different-checksum'
    file.isBuffer = lambda: True
    file.isStream = lambda: False
    out = []
    plugin.on('data', lambda d: out.append(d))
    plugin.write(file)
    plugin.end()
    assert any(getattr(x, "checksum", None) == "different-checksum" for x in out)

def test_files_same_path_different_caches_public():
    plugin1 = Cached('public-unique1')
    plugin2 = Cached('public-unique2')
    filePath = 'commonpub/file.txt'
    file1 = make_file(filePath, b'X')
    file2 = make_file(filePath, b'Y')
    rec1, rec2 = [], []
    plugin1.on('data', lambda d: rec1.append(d))
    plugin2.on('data', lambda d: rec2.append(d))
    plugin1.write(file1)
    plugin2.write(file2)
    plugin1.end()
    plugin2.end()
    assert rec1 and rec1[0].contents == b'X'
    assert rec2 and rec2[0].contents == b'Y'

def test_not_share_cache_if_name_falsy_public():
    pluginA = Cached(None)
    pluginB = Cached(None)
    filePathA = 'nofalsy/fileA.txt'
    filePathB = 'nofalsy/fileB.txt'
    fileA = make_file(filePathA, b'p')
    fileB = make_file(filePathB, b'q')
    seenA = []
    seenB = []
    pluginA.on('data', lambda d: seenA.append(d) if d.path == filePathA else None)
    pluginB.on('data', lambda d: seenB.append(d) if d.path == filePathB else None)
    pluginA.write(fileA)
    pluginA.end()
    pluginB.write(fileB)
    pluginB.end()
    assert seenA, "pluginA should let its file through (public)"
    assert seenB, "pluginB should let its file through (public)"

def test_plugin_caches_object_exists_public():
    assert isinstance(Cached.caches, dict)
    assert Cached.caches is not None

def test_cache_allow_file_once_public():
    plugin = Cached('public-simple')
    file = make_file('baz/quux.txt', b'zoo')
    calls = []
    plugin.on('data', lambda d: calls.append(d))
    plugin.write(file)
    plugin.write(file)
    plugin.end()
    assert len(calls) == 1
    assert calls[0] is file

def test_clear_cache_on_reset_public():
    plugin = Cached('public-reset')
    file = make_file('alpha/bravo.txt', b'marble')
    cnt = []
    plugin.on('data', lambda _: cnt.append(1))
    plugin.write(file)
    plugin.write(file)
    plugin.end()
    Cached.caches['public-reset'] = {}
    plugin2 = Cached('public-reset')
    cnt2 = []
    plugin2.on('data', lambda _: cnt2.append(1))
    plugin2.write(file)
    plugin2.end()
    assert (len(cnt) + len(cnt2)) == 2

def test_create_separate_caches_file_once_each_public():
    pluginA = Cached('pubA')
    pluginB = Cached('pubB')
    file = make_file('multi2/beta.txt', b'def')
    seenA, seenB = [], []
    pluginA.on('data', lambda _: seenA.append(1))
    pluginB.on('data', lambda _: seenB.append(1))
    pluginA.write(file)
    pluginB.write(file)
    pluginA.end()
    pluginB.end()
    assert len(seenA) == 1
    assert len(seenB) == 1
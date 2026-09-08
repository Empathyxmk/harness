import pytest
import types
import asyncio
import os
import shutil

import jd4.cache as cache

@pytest.mark.asyncio
async def test_cache_open_file_found(tmp_path, monkeypatch):
    # Create cache directory and file
    domain = "dom1"
    pid = "prob"
    domain_dir = tmp_path / domain
    os.makedirs(domain_dir, exist_ok=True)
    file_path = domain_dir / (pid + ".zip")
    file_path.write_bytes(b'data')
    monkeypatch.setattr("appdirs.user_cache_dir", lambda x: str(tmp_path))
    # Re-import cache to reset _CACHE_DIR
    import importlib
    importlib.reload(cache)
    f = await cache.cache_open(
        session=None, domain_id=domain, pid=pid
    )
    data = f.read()
    f.close()
    assert data == b'data'

class DummySession:
    def __init__(self):
        self.called = False
    async def problem_data(self, domain_id, pid, tmp_path):
        # Write dummy content
        with open(tmp_path, 'wb') as f:
            f.write(b'probdata')
        self.called = True

@pytest.mark.asyncio
async def test_cache_open_download(tmp_path, monkeypatch):
    # No file exists, so session.problem_data will be called
    domain = "dom2"
    pid = "p2"
    monkeypatch.setattr("appdirs.user_cache_dir", lambda x: str(tmp_path))
    # Patch Event to use normal asyncio.Event (since real one needs loop)
    import importlib
    importlib.reload(cache)
    monkeypatch.setattr("jd4.cache.Event", asyncio.Event)
    session = DummySession()
    file = await cache.cache_open(session, domain, pid)
    assert session.called
    content = file.read()
    assert content == b'probdata'
    file.close()

@pytest.mark.asyncio
async def test_cache_invalidate(tmp_path, monkeypatch):
    # Existence: should remove file, no error if file doesn't exist
    domain = "dom3"
    pid = "pp"
    cachedir = tmp_path / domain
    os.makedirs(cachedir)
    fpath = cachedir / (pid + ".zip")
    fpath.write_bytes(b'x')
    monkeypatch.setattr("appdirs.user_cache_dir", lambda x: str(tmp_path))
    import importlib
    importlib.reload(cache)
    await cache.cache_invalidate(domain, pid)
    assert not fpath.exists()
    # Should not raise if called again
    await cache.cache_invalidate(domain, pid)
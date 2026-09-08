import pytest
import asyncio
from unittest.mock import patch, MagicMock

import jd4.pool as pool

def test_public_put_sandbox_puts_to_queue(monkeypatch):
    qvals = []
    class Q:
        def put_nowait(self, v):
            qvals.append(v)
    monkeypatch.setattr(pool, "_queue", Q())
    pool.put_sandbox('a', 'b', 'c')
    assert qvals == ['a', 'b', 'c']

@pytest.mark.asyncio
async def test_public_get_sandbox(monkeypatch):
    vals = [asyncio.Future(), asyncio.Future()]
    vals[0].set_result('x')
    vals[1].set_result('y')
    monkeypatch.setattr(pool, "_lock", MagicMock())
    pool._lock.acquire = MagicMock(return_value=asyncio.Future())
    pool._lock.acquire.return_value.set_result(True)
    pool._lock.release = MagicMock()
    monkeypatch.setattr(pool, "_queue", MagicMock())
    pool._queue.get = MagicMock(side_effect=[vals[0], vals[1]])
    outs = await pool.get_sandbox(2)
    assert outs == ['x', 'y']
    pool._lock.release.assert_called()

def test_public_init_parallelism(monkeypatch):
    config = {'parallelism': 4}
    monkeypatch.setattr(pool, "config", config)
    msgs = []
    class Logger:
        def info(self, fmt, *a): msgs.append(("info", fmt, a))
        def warning(self, fmt, *a): msgs.append(("warn", fmt, a))
    monkeypatch.setattr(pool, "logger", Logger())
    fake_sandboxes = [9, 8, 7, 6]
    async def create_sandboxes(n):
        assert n == 4
        return fake_sandboxes
    monkeypatch.setattr(pool, "create_sandboxes", create_sandboxes)
    class Loop:
        def run_until_complete(self, task):
            # Run the async function
            return asyncio.get_event_loop().run_until_complete(task)
    monkeypatch.setattr(pool, "get_event_loop", lambda: asyncio.get_event_loop())
    class Dummy: pass
    monkeypatch.setattr(pool, "Lock", lambda: Dummy())
    monkeypatch.setattr(pool, "LifoQueue", lambda: Dummy())
    pool.init()
    assert any(t[0]=="info" for t in msgs)
    assert hasattr(pool, "_lock")
    assert hasattr(pool, "_queue")

def test_public_init_low_parallelism(monkeypatch):
    config = {'parallelism': 2}
    monkeypatch.setattr(pool, "config", config)
    msgs = []
    class Logger:
        def info(self, fmt, *a): msgs.append(("info", fmt, a))
        def warning(self, fmt, *a): msgs.append(("warn", fmt, a))
    monkeypatch.setattr(pool, "logger", Logger())
    async def create_sandboxes(n): return ['s1', 's2']
    monkeypatch.setattr(pool, "create_sandboxes", create_sandboxes)
    monkeypatch.setattr(pool, "get_event_loop", lambda: asyncio.get_event_loop())
    class Dummy: pass
    monkeypatch.setattr(pool, "Lock", lambda: Dummy())
    monkeypatch.setattr(pool, "LifoQueue", lambda: Dummy())
    pool.init()
    assert any(t[0]=="warn" for t in msgs)
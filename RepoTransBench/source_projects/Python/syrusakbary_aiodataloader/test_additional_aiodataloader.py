import pytest
from aiodataloader import DataLoader, iscoroutinefunctionorpartial, __version__

import asyncio
from functools import partial

@pytest.mark.asyncio
async def test_iscoroutinefunctionorpartial_true_on_coro_fn():
    async def f(): pass
    assert iscoroutinefunctionorpartial(f)

@pytest.mark.asyncio
async def test_iscoroutinefunctionorpartial_true_on_partial_coro():
    async def f(): pass
    p = partial(f)
    assert iscoroutinefunctionorpartial(p)

@pytest.mark.asyncio
async def test_iscoroutinefunctionorpartial_false_on_regular():
    def f(): pass
    assert not iscoroutinefunctionorpartial(f)

@pytest.mark.asyncio
async def test_version_in_module():
    assert isinstance(__version__, str) and len(__version__) > 0

@pytest.mark.asyncio
async def test_dataloader_batch_load_fn_typeerror_and_coroutine_check():
    def not_coro_fn(keys):
        return keys
    with pytest.raises(AssertionError):
        DataLoader(not_coro_fn)

@pytest.mark.asyncio
async def test_dataloader_default_get_cache_key_exists():
    async def fn(keys): return keys
    dl = DataLoader(fn)
    assert callable(dl.get_cache_key)

@pytest.mark.asyncio
async def test_dataloader_cache_false_actually_avoids_caching():
    async def fn(keys): return keys
    dl = DataLoader(fn, cache=False)
    fut1 = dl.load(1)
    fut2 = dl.load(1)
    assert fut1 is not fut2

@pytest.mark.asyncio
async def test_dataloader_clear_cache_and_prime_behavior():
    async def fn(keys): return keys
    dl = DataLoader(fn)
    fut = dl.load(123)
    await asyncio.sleep(0)
    assert 123 in dl._cache
    dl.clear(123)
    assert 123 not in dl._cache
    # test prime, dl.prime stores a Future with result=<passed future>
    fut2 = asyncio.Future()
    fut2.set_result('a')
    dl.prime(124, fut2)
    assert isinstance(dl._cache[124], asyncio.Future)
    # The result of the cache Future is fut2
    assert dl._cache[124].result() is fut2

@pytest.mark.asyncio
async def test_dataloader_clear_all():
    async def fn(keys): return keys
    dl = DataLoader(fn)
    for k in range(3):
        _ = dl.load(k)
    await asyncio.sleep(0)
    dl.clear_all()
    assert dl._cache == {}

@pytest.mark.asyncio
async def test_dataloader_custom_loop(monkeypatch):
    async def fn(keys): return keys
    dummy = object()
    dl = DataLoader(fn, loop=dummy)
    assert dl.loop is dummy
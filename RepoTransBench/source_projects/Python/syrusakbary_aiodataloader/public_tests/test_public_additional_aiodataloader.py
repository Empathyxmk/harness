import pytest
from aiodataloader import DataLoader, iscoroutinefunctionorpartial, __version__

import asyncio
from functools import partial

@pytest.mark.asyncio
async def test_iscoroutinefunctionorpartial_true_on_coro_fn_pub():
    async def g(): return 1
    assert iscoroutinefunctionorpartial(g)

@pytest.mark.asyncio
async def test_iscoroutinefunctionorpartial_true_on_partial_coro_pub():
    async def g(): return 'coroutine'
    p = partial(g)
    assert iscoroutinefunctionorpartial(p)

@pytest.mark.asyncio
async def test_iscoroutinefunctionorpartial_false_on_regular_pub():
    def h(): return "not coro"
    assert not iscoroutinefunctionorpartial(h)

@pytest.mark.asyncio
async def test_version_in_module_pub():
    assert isinstance(__version__, str) and __version__.count('.') == 2

@pytest.mark.asyncio
async def test_dataloader_batch_load_fn_typeerror_and_coroutine_check_pub():
    def not_coro_fn(keys):
        return keys
    with pytest.raises(AssertionError):
        DataLoader(not_coro_fn)

@pytest.mark.asyncio
async def test_dataloader_default_get_cache_key_exists_pub():
    async def fn(keys): return [k * 2 for k in keys]
    dl = DataLoader(fn)
    assert callable(dl.get_cache_key)

@pytest.mark.asyncio
async def test_dataloader_cache_false_actually_avoids_caching_pub():
    async def fn(keys): return [k + 1 for k in keys]
    dl = DataLoader(fn, cache=False)
    fut1 = dl.load(7)
    fut2 = dl.load(7)
    assert fut1 is not fut2

@pytest.mark.asyncio
async def test_dataloader_clear_cache_and_prime_behavior_pub():
    async def fn(keys): return [k - 1 for k in keys]
    dl = DataLoader(fn)
    fut = dl.load(321)
    await asyncio.sleep(0)
    assert 321 in dl._cache
    dl.clear(321)
    assert 321 not in dl._cache
    # test prime with distinct Future that returns a string
    fut2 = asyncio.Future()
    fut2.set_result('b')
    dl.prime(322, fut2)
    assert isinstance(dl._cache[322], asyncio.Future)
    assert dl._cache[322].result() is fut2

@pytest.mark.asyncio
async def test_dataloader_clear_all_pub():
    async def fn(keys): return [str(k) for k in keys]
    dl = DataLoader(fn)
    for k in range(5, 8):
        _ = dl.load(k)
    await asyncio.sleep(0)
    dl.clear_all()
    assert dl._cache == {}

@pytest.mark.asyncio
async def test_dataloader_custom_loop_pub(monkeypatch):
    async def fn(keys): return [x.upper() for x in keys]
    dummy = object()
    dl = DataLoader(fn, loop=dummy)
    assert dl.loop is dummy
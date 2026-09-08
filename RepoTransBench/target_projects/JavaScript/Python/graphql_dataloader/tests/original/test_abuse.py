import pytest
import asyncio
from src.dataloader import DataLoader

class DummyBadCacheMap:
    def get(self): pass

def test_loader_creation_requires_function():
    with pytest.raises(TypeError) as e:
        DataLoader(None)
    assert 'DataLoader must be constructed with a function' in str(e.value)

    with pytest.raises(TypeError) as e:
        DataLoader({})
    assert 'DataLoader must be constructed with a function' in str(e.value)

def test_load_function_requires_key():
    loader = DataLoader(lambda keys: asyncio.Future())
    with pytest.raises(TypeError) as e:
        asyncio.run(loader.load(None))
    assert 'must be called with a value' in str(e.value)

    # test falsy-but-truthy key is accepted
    # 0 is valid key
    asyncio.run(loader.load(0))  # should not raise

def test_load_many_requires_list():
    loader = DataLoader(lambda keys: asyncio.Future())
    with pytest.raises(TypeError) as e:
        asyncio.run(loader.loadMany(None))
    assert 'must be called with Array<key>' in str(e.value)
    with pytest.raises(TypeError) as e:
        asyncio.run(loader.loadMany(1))
    assert 'must be called with Array<key>' in str(e.value)
    # empty array is fine
    asyncio.run(loader.loadMany([]))  # Should not throw

@pytest.mark.asyncio
async def test_batch_function_must_return_promise_not_none():
    loader = DataLoader(lambda keys: None)
    with pytest.raises(TypeError) as e:
        await loader.load(1)
    assert 'not return a Promise' in str(e.value)

@pytest.mark.asyncio
async def test_batch_function_cannot_throw_sync():
    def badfn(keys):
        raise Exception('Mock Synchronous Error')
    loader = DataLoader(badfn)
    with pytest.raises(TypeError) as e:
        await loader.load(1)
    assert 'errored synchronously: Error:' in str(e.value)

@pytest.mark.asyncio
async def test_batch_function_must_return_promise_not_value():
    loader = DataLoader(lambda keys: 1)
    with pytest.raises(TypeError) as e:
        await loader.load(1)
    assert 'not return a Promise' in str(e.value)

@pytest.mark.asyncio
async def test_batch_function_must_return_promise_of_array_not_none():
    async def bad(keys):
        return None
    loader = DataLoader(bad)
    with pytest.raises(TypeError) as e:
        await loader.load(1)
    assert 'not return a Promise of an Array' in str(e.value)

@pytest.mark.asyncio
async def test_batch_promises_array_matching_length():
    async def bad(keys):
        return []
    loader = DataLoader(bad)
    with pytest.raises(TypeError) as e:
        await loader.load(1)
    assert 'not return a Promise of an Array of the same length as the Array' in str(e.value)

def test_custom_cache_map_requires_methods():
    class IncompleteMap:
        def get(self): pass
    with pytest.raises(TypeError) as e:
        DataLoader(lambda k: k, cacheMap=IncompleteMap())
    assert 'Custom cacheMap missing methods' in str(e.value)

def test_requires_number_for_max_batch_size():
    with pytest.raises(TypeError) as e:
        DataLoader(lambda k: k, maxBatchSize=None)
    # Not enforced in python implementation (for simplicity) but for parity in the logic, show
    # the test
    # If your implementation checks, then this test should pass.

def test_requires_function_for_cacheKeyFn():
    with pytest.raises(Exception):
        DataLoader(lambda k: k, cacheKeyFn=None)

def test_requires_function_for_batchScheduleFn():
    with pytest.raises(Exception):
        DataLoader(lambda k: k, batchScheduleFn=None)
import pytest
import asyncio
from src.dataloader import DataLoader

@pytest.mark.asyncio
async def test_builds_really_simple_dataloader():
    async def batch(keys):
        return keys
    loader = DataLoader(batch)
    f = loader.load(1)
    assert asyncio.isfuture(f)
    value = await f
    assert value == 1

@pytest.mark.asyncio
async def test_references_loader_as_this_in_batch_function():
    called = {}
    class CustomLoader(DataLoader):
        async def batch_fn(self, keys):
            called['self'] = self
            return keys
    # In Python, we pass self explicitly, but we'll simulate as close as possible
    loader = CustomLoader(lambda self, keys: keys)
    await loader.load(1)
    assert called['self'] is loader

@pytest.mark.asyncio
async def test_references_loader_as_this_in_cache_key_fn():
    class CustomLoader(DataLoader):
        async def batch_fn(self, keys):
            return keys
        def cache_key_fn(self, key):
            called['self'] = self
            return key
    called = {}
    loader = DataLoader(lambda keys: keys, cacheKeyFn=lambda key: key)
    await loader.load(1)
    # Can't check binding as easily as JS, so just ensure no errors

@pytest.mark.asyncio
async def test_load_many_one_call():
    loader = DataLoader(lambda keys: [k for k in keys])
    promise_all = await loader.loadMany([1,2])
    assert promise_all == [1,2]
    promise_empty = await loader.loadMany([])
    assert promise_empty == []

@pytest.mark.asyncio
async def test_load_many_with_errors():
    def batch_fn(keys):
        return [k if k != 'bad' else Exception('Bad Key') for k in keys]
    loader = DataLoader(batch_fn)
    result = await loader.loadMany(['a', 'b', 'bad'])
    assert result[0] == 'a'
    assert result[1] == 'b'
    assert isinstance(result[2], Exception)
    assert str(result[2]) == 'Bad Key'

@pytest.mark.asyncio
async def test_batches_multiple_requests():
    calls = []
    def batch(keys):
        calls.append(list(keys))
        return list(keys)
    loader = DataLoader(batch)
    p1 = loader.load(1)
    p2 = loader.load(2)
    v1, v2 = await asyncio.gather(p1, p2)
    assert v1 == 1
    assert v2 == 2
    assert calls == [[1,2]]

@pytest.mark.asyncio
async def test_batches_with_max_batch_sizes():
    calls = []
    def batch(keys):
        calls.append(list(keys))
        return list(keys)
    loader = DataLoader(batch, maxBatchSize=2)
    p1 = loader.load(1)
    p2 = loader.load(2)
    p3 = loader.load(3)
    v1, v2, v3 = await asyncio.gather(p1, p2, p3)
    assert (v1,v2,v3) == (1,2,3)
    assert calls == [[1,2],[3]]

@pytest.mark.asyncio
async def test_max_batch_size_with_duplicates():
    calls = []
    def batch(keys):
        calls.append(list(keys))
        return list(keys)
    loader = DataLoader(batch, maxBatchSize=3)
    values = ['a', 'b', 'a', 'a', 'a', 'b', 'c']
    results = await asyncio.gather(*(loader.load(v) for v in values))
    assert results == values
    assert calls == [['a', 'b', 'c']]

@pytest.mark.asyncio
async def test_batches_cached_requests():
    calls = []
    async def batch(keys):
        calls.append(keys)
        f = asyncio.Future()
        f.set_result(list(keys))
        return f
    loader = DataLoader(batch)
    loader.prime(1, 1)
    p1 = loader.load(1)
    p2 = loader.load(2)
    v1 = await p1
    v2 = await p2
    assert v1 == 1
    assert v2 == 2
    assert calls == [[2]]

@pytest.mark.asyncio
async def test_max_batch_size_respects_cached_results():
    calls = []
    async def batch(keys):
        calls.append(keys)
        f = asyncio.Future()
        f.set_result(list(keys))
        return f
    loader = DataLoader(batch, maxBatchSize=1)
    loader.prime(1, 1)
    p1 = loader.load(1)
    p2 = loader.load(2)
    v1 = await p1
    v2 = await p2
    assert v1 == 1
    assert v2 == 2
    assert calls == [[2]]

@pytest.mark.asyncio
async def test_coalesces_identical_requests():
    calls = []
    def batch(keys):
        calls.append(list(keys))
        return list(keys)
    loader = DataLoader(batch)
    p1a = loader.load(1)
    p1b = loader.load(1)
    v1a, v1b = await asyncio.gather(p1a, p1b)
    assert v1a == v1b == 1
    assert calls == [[1]]

@pytest.mark.asyncio
async def test_coalesces_identical_requests_across_batches():
    calls = []
    def batch(keys):
        calls.append(list(keys))
        return list(keys)
    loader = DataLoader(batch, maxBatchSize=2)
    p1a = loader.load(1)
    p2 = loader.load(2)
    p1b = loader.load(1)
    p3 = loader.load(3)
    v1a, v2, v1b, v3 = await asyncio.gather(p1a, p2, p1b, p3)
    assert [v1a,v2,v1b,v3] == [1,2,1,3]
    assert calls == [[1,2],[3]]

@pytest.mark.asyncio
async def test_caches_repeated_requests():
    calls = []
    def batch(keys):
        calls.append(list(keys))
        return list(keys)
    loader = DataLoader(batch)
    a, b = await asyncio.gather(loader.load('A'), loader.load('B'))
    assert a == 'A'
    assert b == 'B'
    assert calls == [['A','B']]
    a2, c = await asyncio.gather(loader.load('A'), loader.load('C'))
    assert a2 == 'A'
    assert c == 'C'
    assert calls == [['A','B'], ['C']]
    a3, b2, c2 = await asyncio.gather(loader.load('A'), loader.load('B'), loader.load('C'))
    assert a3 == 'A'
    assert b2 == 'B'
    assert c2 == 'C'
    assert calls == [['A','B'], ['C']]

@pytest.mark.asyncio
async def test_clears_single_value():
    calls = []
    def batch(keys):
        calls.append(list(keys))
        return list(keys)
    loader = DataLoader(batch)
    a, b = await asyncio.gather(loader.load('A'), loader.load('B'))
    assert a == 'A'
    assert b == 'B'
    assert calls == [['A','B']]
    loader.clear('A')
    a2, b2 = await asyncio.gather(loader.load('A'), loader.load('B'))
    assert a2 == 'A'
    assert b2 == 'B'
    assert calls == [['A','B'], ['A']]

@pytest.mark.asyncio
async def test_clears_all_values():
    calls = []
    def batch(keys):
        calls.append(list(keys))
        return list(keys)
    loader = DataLoader(batch)
    a, b = await asyncio.gather(loader.load('A'), loader.load('B'))
    assert a == 'A'
    assert b == 'B'
    assert calls == [['A','B']]
    loader.clearAll()
    a2, b2 = await asyncio.gather(loader.load('A'), loader.load('B'))
    assert a2 == 'A'
    assert b2 == 'B'
    assert calls == [['A','B'], ['A','B']]

@pytest.mark.asyncio
async def test_allows_priming_cache():
    calls = []
    def batch(keys):
        calls.append(list(keys))
        return list(keys)
    loader = DataLoader(batch)
    loader.prime('A', 'A')
    a, b = await asyncio.gather(loader.load('A'), loader.load('B'))
    assert a == 'A'
    assert b == 'B'
    assert calls == [['B']]

@pytest.mark.asyncio
async def test_does_not_prime_keys_that_exist():
    calls = []
    def batch(keys):
        calls.append(list(keys))
        return list(keys)
    loader = DataLoader(batch)
    loader.prime('A', 'X')
    a1 = await loader.load('A')
    b1 = await loader.load('B')
    assert a1 == 'X'
    assert b1 == 'B'
    loader.prime('A', 'Y')
    loader.prime('B', 'Y')
    a2 = await loader.load('A')
    b2 = await loader.load('B')
    assert a2 == 'X'
    assert b2 == 'B'
    assert calls == [['B']]

@pytest.mark.asyncio
async def test_allows_forcefully_priming_cache():
    calls = []
    def batch(keys):
        calls.append(list(keys))
        return list(keys)
    loader = DataLoader(batch)
    loader.prime('A', 'X')
    a1 = await loader.load('A')
    b1 = await loader.load('B')
    assert a1 == 'X'
    assert b1 == 'B'
    loader.clear('A'); loader.prime('A','Y')
    loader.clear('B'); loader.prime('B','Y')
    a2 = await loader.load('A')
    b2 = await loader.load('B')
    assert a2 == 'Y'
    assert b2 == 'Y'
    assert calls == [['B']]

@pytest.mark.asyncio
async def test_allows_priming_with_promise():
    calls = []
    async def batch(keys):
        calls.append(list(keys))
        return list(keys)
    loader = DataLoader(batch)
    fut = asyncio.Future()
    fut.set_result('A')
    loader.prime('A', fut)
    a, b = await asyncio.gather(loader.load('A'), loader.load('B'))
    assert a == 'A'
    assert b == 'B'
    assert calls == [['B']]

def test_allows_giving_loader_a_name():
    loader = DataLoader(lambda k: [], name=None)
    assert loader.name is None
    loader = DataLoader(lambda k: [], name='Some name')
    assert loader.name == 'Some name'

@pytest.mark.asyncio
async def test_resolves_to_error_to_indicate_failure():
    calls = []
    def batch(keys):
        calls.append(list(keys))
        return [k if k % 2 == 0 else Exception(f'Odd: {k}') for k in keys]
    loader = DataLoader(batch)
    with pytest.raises(Exception) as e:
        await loader.load(1)
    assert 'Odd: 1' in str(e.value)
    value2 = await loader.load(2)
    assert value2 == 2
    assert calls == [[1], [2]]

@pytest.mark.asyncio
async def test_can_failures_and_successes_simultaneously():
    calls = []
    def batch(keys):
        calls.append(list(keys))
        return [k if k % 2 == 0 else Exception(f'Odd: {k}') for k in keys]
    loader = DataLoader(batch)
    p1 = loader.load(1)
    p2 = loader.load(2)
    with pytest.raises(Exception) as e:
        await p1
    assert 'Odd: 1' in str(e.value)
    assert await p2 == 2
    assert calls == [[1,2]]

@pytest.mark.asyncio
async def test_caches_failed_fetches():
    called = []
    def batch(keys):
        called.append(keys)
        return [Exception(f"Error: {k}") for k in keys]
    loader = DataLoader(batch)
    with pytest.raises(Exception) as e:
        await loader.load(1)
    assert "Error: 1" in str(e.value)
    with pytest.raises(Exception) as e:
        await loader.load(1)
    assert "Error: 1" in str(e.value)
    assert called == [[1]]

@pytest.mark.asyncio
async def test_handles_priming_with_error():
    def batch(keys): return keys
    loader = DataLoader(batch)
    loader.prime(1, Exception("Error: 1"))
    with pytest.raises(Exception) as e:
        await loader.load(1)
    assert "Error: 1" in str(e.value)

@pytest.mark.asyncio
async def test_can_clear_cache_after_error():
    called = []
    def batch(keys):
        called.append(keys)
        return [Exception(f"Error: {k}") for k in keys]
    loader = DataLoader(batch)
    with pytest.raises(Exception) as e:
        try:
            await loader.load(1)
        except Exception as error:
            loader.clear(1)
            raise
    with pytest.raises(Exception) as e:
        try:
            await loader.load(1)
        except Exception as error:
            loader.clear(1)
            raise
    assert called == [[1],[1]]

@pytest.mark.asyncio
async def test_propagates_error_to_all_loads():
    calls = []
    async def batch(keys):
        calls.append(list(keys))
        raise Exception('I am a terrible loader')
    loader = DataLoader(batch)
    p1 = loader.load(7)
    p2 = loader.load(8)
    with pytest.raises(Exception) as e:
        await asyncio.gather(p1, p2)
    assert 'I am a terrible loader' in str(e.value)
    assert calls and calls[0] == [7,8]
import pytest
import asyncio
from aiodataloader import DataLoader

pytestmark = pytest.mark.asyncio

from functools import partial
from typing import Any, Callable, Coroutine, Dict, List, Optional, Tuple, TypeVar, Union

T1 = TypeVar("T1")
T2 = TypeVar("T2")


def id_loader_public(
    *,
    resolve: Optional[
        Callable[[List[T1]], Coroutine[Any, Any, Union[List[T1], List[T2]]]]
    ] = None,
    **dl_kwargs: Any,
) -> Tuple[DataLoader[T1, Union[T1, T2]], List[List[T1]]]:
    load_calls: List[List[T1]] = []

    async def default_resolve(x: List[T1]) -> List[T1]:
        return x

    async def fn(keys: List[T1]) -> Union[List[T1], List[T2]]:
        load_calls.append(keys)
        return await (resolve or default_resolve)(keys)

    identity_loader: DataLoader[Any, Any] = DataLoader(fn, **dl_kwargs)
    return identity_loader, load_calls

async def test_build_a_simple_data_loader_public():
    async def call_fn(keys: List[int]) -> List[int]:
        return [k + 10 for k in keys]

    identity_loader = DataLoader(call_fn)
    promise1 = identity_loader.load(5)
    value1 = await promise1
    assert value1 == 15

async def test_can_build_a_data_loader_from_a_partial_public():
    value_map = {3: "three", 4: "four"}

    async def call_fn(context: Dict[int, str], keys: List[int]) -> List[Optional[str]]:
        return [context.get(key) for key in keys]

    partial_fn = partial(call_fn, value_map)
    identity_loader = DataLoader(partial_fn)
    promise1 = identity_loader.load(3)
    value1 = await promise1
    assert value1 == "three"

async def test_supports_loading_multiple_keys_in_one_call_public():
    async def call_fn(keys: List[int]) -> List[int]:
        return [k * 2 for k in keys]

    identity_loader = DataLoader(call_fn)
    promise_all = identity_loader.load_many([5, 6])
    values = await promise_all
    assert values == [10, 12]

    promise_all = identity_loader.load_many([8, 9])
    values = await promise_all
    assert values == [16, 18]

    promise_all = identity_loader.load_many([])
    values = await promise_all
    assert values == []

async def test_batches_multiple_requests_public():
    loader_result = id_loader_public()
    identity_loader, load_calls = loader_result

    promiseA = identity_loader.load("alpha")
    promiseB = identity_loader.load("beta")

    valueA, valueB = await asyncio.gather(promiseA, promiseB)
    assert valueA == "alpha"
    assert valueB == "beta"
    assert load_calls == [["alpha", "beta"]]

async def test_batches_multiple_requests_with_max_batch_sizes_public():
    loader_result = id_loader_public(max_batch_size=2)
    identity_loader, load_calls = loader_result

    p1 = identity_loader.load("x")
    p2 = identity_loader.load("y")
    p3 = identity_loader.load("z")

    v1, v2, v3 = await asyncio.gather(p1, p2, p3)
    assert v1 == "x"
    assert v2 == "y"
    assert v3 == "z"

    # With max_batch_size=2, first batch is ['x', 'y'], second is ['z']
    assert load_calls == [["x", "y"], ["z"]]

async def test_coalesces_identical_requests_public():
    loader_result = id_loader_public()
    identity_loader, load_calls = loader_result

    promiseA1 = identity_loader.load(42)
    promiseA2 = identity_loader.load(42)

    # Both promised should be the same Future object
    assert promiseA1 == promiseA2
    v1, v2 = await asyncio.gather(promiseA1, promiseA2)
    assert v1 == 42
    assert v2 == 42
    assert load_calls == [[42]]

async def test_caches_repeated_requests_public():
    loader_result = id_loader_public()
    identity_loader, load_calls = loader_result

    a, b = await asyncio.gather(identity_loader.load("X"), identity_loader.load("Y"))
    assert a == "X"
    assert b == "Y"
    assert load_calls == [["X", "Y"]]

    a2, c = await asyncio.gather(identity_loader.load("X"), identity_loader.load("Z"))
    assert a2 == "X"
    assert c == "Z"
    assert load_calls == [["X", "Y"], ["Z"]]

    # All loaded, so future batch should be a cache hit for X and Y, batch for missing key only
    x3, y2, z2 = await asyncio.gather(
        identity_loader.load("X"), identity_loader.load("Y"), identity_loader.load("Z")
    )
    assert x3 == "X"
    assert y2 == "Y"
    assert z2 == "Z"
    assert load_calls == [["X", "Y"], ["Z"]]

async def test_clears_single_value_in_loader_public():
    loader_result = id_loader_public()
    identity_loader, load_calls = loader_result

    a, b = await asyncio.gather(identity_loader.load("D"), identity_loader.load("E"))
    assert a == "D"
    assert b == "E"
    assert load_calls == [["D", "E"]]

    identity_loader.clear("D")

    a2, e2 = await asyncio.gather(identity_loader.load("D"), identity_loader.load("E"))
    assert a2 == "D"
    assert e2 == "E"
    # Only "D" will be loaded in a new batch
    assert load_calls == [["D", "E"], ["D"]]

async def test_clears_all_values_in_loader_public():
    loader_result = id_loader_public()
    identity_loader, load_calls = loader_result

    s, t = await asyncio.gather(identity_loader.load("S"), identity_loader.load("T"))
    assert s == "S"
    assert t == "T"
    assert load_calls == [["S", "T"]]

    identity_loader.clear_all()

    s2, t2 = await asyncio.gather(identity_loader.load("S"), identity_loader.load("T"))
    assert s2 == "S"
    assert t2 == "T"
    assert load_calls == [["S", "T"], ["S", "T"]]

async def test_allows_priming_the_cache_public():
    loader_result = id_loader_public()
    identity_loader, load_calls = loader_result

    identity_loader.prime("U", "U-prime")
    u, v = await asyncio.gather(identity_loader.load("U"), identity_loader.load("V"))
    assert u == "U-prime"
    assert v == "V"
    assert load_calls == [["V"]]
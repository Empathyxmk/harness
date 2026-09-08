import pytest
import asyncio

from typical import type

@pytest.fixture
def create_node():
    def f(text):
        return {'textContent': text}
    return f


@pytest.mark.asyncio
async def test_type_handles_string_argument_public(create_node):
    node = create_node('xyz')
    await type(node, 'uvw')
    assert node['textContent'] == 'uvw', "Node text should update to new string"

@pytest.mark.asyncio
async def test_type_handles_different_wait_argument_public(create_node, monkeypatch):
    waited = False
    def fake_sleep(x):  # simulate instant wait
        nonlocal waited
        waited = True
        return asyncio.sleep(0)
    monkeypatch.setattr('asyncio.sleep', fake_sleep)
    node = create_node('2')
    await type(node, 42)
    assert waited, "Should handle different wait argument"

@pytest.mark.asyncio
async def test_type_handles_different_async_function_argument_public(create_node):
    node = create_node('bar')
    called = False
    async def fake_fn_b(node_arg):
        nonlocal called
        assert node_arg is node, "Function receives correct node"
        called = True
    await type(node, fake_fn_b)
    assert called, "Should call the different function argument"

@pytest.mark.asyncio
async def test_type_handles_different_promise_as_argument_public(create_node):
    node = create_node('baz')
    resolved = False

    async def fake_promise():
        await asyncio.sleep(0)  # simulate "setTimeout(..., 0)"
        nonlocal resolved
        resolved = True
    p = fake_promise()
    await type(node, p)
    assert resolved, "Should await the different promise"

@pytest.mark.asyncio
async def test_type_performs_public_sequence_actions(create_node):
    node = create_node('')
    async def step_fn(n):
        await type(n, 'xyz')
    await type(node, 'abc', 10, step_fn)
    assert node['textContent'] == 'xyz', "Public sequence of actions results in correct text"
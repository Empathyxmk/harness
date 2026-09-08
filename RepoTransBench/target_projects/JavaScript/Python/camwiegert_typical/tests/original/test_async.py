import pytest
import asyncio

from typical import type

@pytest.fixture
def create_node():
    def f(text):
        return {'textContent': text}
    return f


@pytest.mark.asyncio
async def test_type_handles_string_argument(create_node):
    node = create_node('abc')
    await type(node, 'def')
    assert node['textContent'] == 'def', "Node text should update to final string"

@pytest.mark.asyncio
async def test_type_handles_number_wait_argument(create_node, monkeypatch):
    waited = False
    def fake_sleep(x):  # simulate instant wait
        nonlocal waited
        waited = True
        return asyncio.sleep(0)
    monkeypatch.setattr('asyncio.sleep', fake_sleep)
    node = create_node('1')
    await type(node, 30)
    assert waited, "Should handle wait argument"

@pytest.mark.asyncio
async def test_type_handles_async_function_argument(create_node):
    node = create_node('foo')
    called = False
    async def fake_fn(node_arg):
        nonlocal called
        assert node_arg is node, "Function receives node"
        called = True
    await type(node, fake_fn)
    assert called, "Should call the function argument"

@pytest.mark.asyncio
async def test_type_handles_promise_as_argument(create_node):
    node = create_node('foo')
    resolved = False

    async def fake_promise():
        nonlocal resolved
        resolved = True
    p = fake_promise()
    await type(node, p)
    assert resolved, "Should await the promise"

@pytest.mark.asyncio
async def test_type_performs_sequence_actions(create_node):
    node = create_node('')
    async def step_fn(n):
        await type(n, 'bar')
    await type(node, 'foo', 5, step_fn)
    assert node['textContent'] == 'bar', "Sequence of actions results in correct text"
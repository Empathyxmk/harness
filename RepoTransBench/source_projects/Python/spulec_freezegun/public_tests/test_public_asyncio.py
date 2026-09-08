import asyncio
import pytest

@pytest.mark.asyncio
async def test_public_async_add():
    async def add(a, b):
        await asyncio.sleep(0.001)
        return a + b
    res = await add(14, 7)
    assert res == 21

@pytest.mark.asyncio
async def test_public_async_upper():
    async def upper(s):
        await asyncio.sleep(0.001)
        return s.upper()
    val = await upper('publictest')
    assert val == 'PUBLICTEST'
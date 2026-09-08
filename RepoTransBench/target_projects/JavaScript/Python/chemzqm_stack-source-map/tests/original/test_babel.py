"""
This test demonstrates Promise/async handling and a failing test.
The original JS test always fails (assert typeof res === 'undefined'), but
as written, get_cat() returns '>_<', so typeof is 'string'.

We preserve the logic for faithfulness.
"""

import pytest

import asyncio

async def get_cat():
    await asyncio.sleep(0.3)
    return '>_<'

async def cat():
    return await get_cat()

@pytest.mark.asyncio
async def test_should_fail():
    res = await cat()
    assert isinstance(res, type(None)), f"Expected None (undefined), got {res!r}"
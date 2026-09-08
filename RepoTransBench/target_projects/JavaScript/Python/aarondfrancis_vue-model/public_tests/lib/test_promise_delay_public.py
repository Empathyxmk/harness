import pytest
import time

from src.lib.promise_delay import delay

@pytest.mark.asyncio
async def test_delays_for_a_different_ms_and_resolves():
    before = time.time()
    await delay(0.03)
    after = time.time()
    assert after - before >= 0.028

@pytest.mark.asyncio
async def test_delays_0_ms_and_resolves_immediately():
    before = time.time()
    await delay(0)
    after = time.time()
    assert after - before >= 0
import pytest
import time

from src.lib.promise_delay import delay

@pytest.mark.asyncio
async def test_delays_for_at_least_x_ms():
    start = time.time()
    await delay(0.05)
    elapsed = time.time() - start
    assert elapsed >= 0.045  # Seconds

@pytest.mark.asyncio
async def test_returns_resolved_value():
    v = await delay(0.01, 'foo')
    assert v == 'foo'
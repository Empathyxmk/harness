import pytest
import asyncio
from src.dataloader import DataLoader

@pytest.mark.asyncio
async def test_batches_without_process_nexttick():
    calls = []
    async def batch_fn(keys):
        calls.append(list(keys))
        return list(keys)
    loader = DataLoader(batch_fn)
    p1 = loader.load(33)
    p2 = loader.load(44)
    res = await asyncio.gather(p1, p2)
    assert res == [33, 44]
    assert calls == [[33, 44]]
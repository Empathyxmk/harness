import pytest
import asyncio
from src.dataloader import DataLoader

@pytest.mark.asyncio
async def test_batches_without_setimmediate():
    calls = []
    async def batch(keys):
        calls.append(list(keys))
        return list(keys)
    loader = DataLoader(batch)
    p1 = loader.load(1)
    p2 = loader.load(2)
    res = await asyncio.gather(p1, p2)
    assert res == [1, 2]
    assert calls == [[1,2]]
import pytest
import asyncio
from src.dataloader import DataLoader

@pytest.mark.asyncio
async def test_batches_requests_without_setimmediate_public():
    calls = []
    async def batch(keys):
        calls.append(list(keys))
        return list(keys)
    loader = DataLoader(batch)
    p1 = loader.load(21)
    p2 = loader.load(22)
    p3 = loader.load(23)
    result = await asyncio.gather(p1, p2, p3)
    assert result == [21,22,23]
    assert len(calls) == 1
    assert sorted(calls[0]) == [21,22,23]
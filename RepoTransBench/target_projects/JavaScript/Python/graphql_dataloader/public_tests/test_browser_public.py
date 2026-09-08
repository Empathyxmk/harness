import pytest
import asyncio
from src.dataloader import DataLoader

@pytest.mark.asyncio
async def test_batches_using_different_values_public():
    loader = DataLoader(lambda keys: [k+10 for k in keys])
    res = await asyncio.gather(
        loader.load(100), loader.load(200), loader.load(300)
    )
    assert res == [110, 210, 310]
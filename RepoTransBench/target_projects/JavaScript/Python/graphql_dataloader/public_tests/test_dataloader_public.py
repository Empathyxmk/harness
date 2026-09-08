import pytest
import asyncio
from src.dataloader import DataLoader

@pytest.mark.asyncio
async def test_return_squares_of_numbers_public():
    loader = DataLoader(lambda keys: [x * x for x in keys])
    res = await loader.loadMany([3, 4, 5])
    assert res == [9,16,25]

@pytest.mark.asyncio
async def test_single_load_returns_correct_value_public():
    loader = DataLoader(lambda keys: [x + 1 for x in keys])
    ret = await loader.load(10)
    assert ret == 11
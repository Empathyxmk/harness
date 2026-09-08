import pytest
import asyncio
from src.dataloader import DataLoader

@pytest.mark.asyncio
async def test_handles_empty_batch_public():
    call_count = 0
    async def batch(keys):
        nonlocal call_count
        call_count += 1
        return [k * 2 for k in keys]
    loader = DataLoader(batch)
    result = await loader.loadMany([])
    assert result == []
    assert call_count == 0  # no call to batch

@pytest.mark.asyncio
async def test_load_with_undefined_key_public():
    loader = DataLoader(lambda keys: keys)
    with pytest.raises(TypeError):
        await loader.load(None)

@pytest.mark.asyncio
async def test_loading_falsy_valid_values_zero_and_emptystr_public():
    loader = DataLoader(lambda keys: [f"out-{k}" for k in keys])
    result = await loader.loadMany([0, ""])
    assert result == ["out-0", "out-"]
import pytest
import asyncio
from src.dataloader import DataLoader

@pytest.mark.asyncio
async def test_should_propagate_promise_rejection_public():
    async def batch(keys):
        raise Exception("public-fail-new-error")
    loader = DataLoader(batch)
    with pytest.raises(Exception) as e:
        await loader.load("pubX")
    assert "public-fail-new-error" in str(e.value)
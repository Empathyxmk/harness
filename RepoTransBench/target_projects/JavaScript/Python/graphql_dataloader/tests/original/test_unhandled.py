import pytest
import asyncio
from src.dataloader import DataLoader

@pytest.mark.asyncio
async def test_unhandled_rejection_propagates():
    loader = DataLoader(lambda keys: (_ for _ in ()).throw(Exception("fail-error")))
    # load, but do not await
    with pytest.raises(Exception) as e:
        await loader.load(71)
    assert 'fail-error' in str(e.value)
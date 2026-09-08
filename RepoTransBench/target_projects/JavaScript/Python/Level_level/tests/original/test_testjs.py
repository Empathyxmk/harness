import pytest
import uuid

@pytest.mark.asyncio
async def test_smoke():
    from src.level import Level
    db = Level(f"db/{uuid.uuid4()}")
    await db.put("abc", "123")
    val = await db.get("abc")
    assert val == "123"
    await db.close()
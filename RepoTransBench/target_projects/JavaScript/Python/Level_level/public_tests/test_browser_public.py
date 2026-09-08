import pytest
import uuid

@pytest.mark.asyncio
async def test_browser_level_put_get_del_public():
    from src.browser import BrowserLevel
    
    dbname = f"db/{uuid.uuid4()}"
    db = BrowserLevel(dbname)
    await db.put("alpha", "omega")
    val = await db.get("alpha")
    assert val == "omega"
    await db.del_("alpha")
    with pytest.raises(Exception):
        await db.get("alpha")
    await db.close()

@pytest.mark.asyncio
async def test_browser_level_batch_and_keys_public():
    from src.browser import BrowserLevel

    dbname = f"db/{uuid.uuid4()}"
    db = BrowserLevel(dbname)
    await db.batch([
        {"type": "put", "key": "qq", "value": "p1"},
        {"type": "put", "key": "ww", "value": "p2"},
        {"type": "put", "key": "ee", "value": "p3"},
    ])
    keys = []
    async for key in db.keys():
        keys.append(key)
    assert "qq" in keys and "ww" in keys and "ee" in keys
    await db.close()
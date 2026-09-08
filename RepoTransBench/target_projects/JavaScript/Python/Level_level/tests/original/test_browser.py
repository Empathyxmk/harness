import pytest
import uuid

@pytest.mark.asyncio
async def test_browser_level_put_get_del():
    from src.browser import BrowserLevel
    
    path = f"db/{uuid.uuid4()}"
    db = BrowserLevel(path)
    await db.put("foo", "bar")
    val = await db.get("foo")
    assert val == "bar"
    await db.del_("foo")
    with pytest.raises(Exception):
        await db.get("foo")
    await db.close()


@pytest.mark.asyncio
async def test_browser_level_batch_iterator():
    from src.browser import BrowserLevel

    path = f"db/{uuid.uuid4()}"
    db = BrowserLevel(path)
    await db.batch([
        {"type": "put", "key": "aa", "value": "1"},
        {"type": "put", "key": "bb", "value": "2"},
        {"type": "put", "key": "cc", "value": "3"},
    ])
    keys = []
    values = []
    async for key in db.keys():
        keys.append(key)
    async for value in db.values():
        values.append(value)
    assert all(k in keys for k in ["aa", "bb", "cc"])
    assert all(v in values for v in ["1", "2", "3"])
    await db.close()
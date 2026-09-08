import pytest
import uuid

@pytest.mark.asyncio
async def test_index_exports_classiclevel():
    from src.level import Level

    assert Level is not None, "Level export exists"
    assert callable(Level), "Level is a constructor"
    name = f"db/{uuid.uuid4()}"
    db = Level(name)
    assert getattr(db, "location", None) == name, "DB location matches"

    await db.put("key1", "value1")
    val = await db.get("key1")
    assert val == "value1", "put/get round-trip"

    await db.del_("key1")
    try:
        after_del = await db.get("key1")
    except Exception as e:
        after_del = e
    assert isinstance(after_del, Exception), "get after delete triggers error"

    await db.close()


@pytest.mark.asyncio
async def test_classiclevel_batch_and_iterator():
    from src.level import Level

    name = f"db/{uuid.uuid4()}"
    db = Level(name)

    await db.batch([
        {"type": "put", "key": "b", "value": "2"},
        {"type": "put", "key": "a", "value": "1"},
        {"type": "put", "key": "c", "value": "3"},
    ])

    vals = await db.get_many(["a", "b", "c"])
    assert vals == ["1", "2", "3"]

    batcher = db.batch()
    batcher.put("x", "10").put("y", "11").del_("a")
    await batcher.write()

    yval = await db.get("y")
    assert yval == "11"

    keys = []
    async for k in db.keys():
        keys.append(k)
    assert all(elem in keys for elem in ("b", "c", "x", "y"))

    await db.close()
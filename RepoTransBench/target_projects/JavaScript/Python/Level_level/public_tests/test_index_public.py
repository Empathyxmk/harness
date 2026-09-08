import pytest
import uuid

@pytest.mark.asyncio
async def test_index_exports_classiclevel_public():
    from src.level import Level

    assert Level is not None, "Level export exists (public)"
    assert callable(Level), "Level is a constructor (public)"
    name = f"db/{uuid.uuid4()}"
    db = Level(name)
    assert getattr(db, "location", None) == name, "DB location matches (public)"

    await db.put("key2", "value42")
    val = await db.get("key2")
    assert val == "value42", "put/get round-trip (public)"

    await db.del_("key2")
    try:
        after_del = await db.get("key2")
    except Exception as e:
        after_del = e
    assert isinstance(after_del, Exception), "get after delete triggers error (public)"
    await db.close()


@pytest.mark.asyncio
async def test_classiclevel_batch_and_iterator_public():
    from src.level import Level

    name = f"db/{uuid.uuid4()}"
    db = Level(name)

    await db.batch([
        {"type": "put", "key": "d", "value": "7"},
        {"type": "put", "key": "z", "value": "99"},
        {"type": "put", "key": "m", "value": "0"},
    ])

    vals = await db.get_many(["z", "d", "m"])
    assert vals == ["99", "7", "0"], "batch getMany with public data"

    batcher = db.batch()
    batcher.put("u", "101").put("v", "202").del_("z")
    await batcher.write()

    vval = await db.get("v")
    assert vval == "202", "get value after chained put (public)"

    keys = []
    async for k in db.keys():
        keys.append(k)
    assert all(elem in keys for elem in ("d", "m", "u", "v")), "iterator found expected keys (public)"

    await db.close()
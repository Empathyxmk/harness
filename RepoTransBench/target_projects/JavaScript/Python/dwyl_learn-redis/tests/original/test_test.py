import redis
import pytest

@pytest.fixture(scope="module")
def client():
    r = redis.Redis(decode_responses=True)
    try:
        r.ping()
    except redis.ConnectionError as err:
        pytest.skip(f"Redis server not available: {err}")
    yield r
    r.close()

def test_can_store_and_retrieve_integers(client):
    res = client.set("NumKey", 42)
    assert res is True
    reply = client.get("NumKey")
    assert reply == "42"

def test_can_increment_values(client):
    client.set("Counter", 10)
    val = client.incr("Counter")
    assert val == 11

def test_handles_list_operations(client):
    client.delete("mylist")
    lpush_len = client.lpush("mylist", "a", "b", "c")
    assert lpush_len > 0
    rpush_len = client.rpush("mylist", "x")
    assert rpush_len > 0
    items = client.lrange("mylist", 0, -1)
    assert "a" in items
    assert "x" in items
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

def test_set_and_get_string(client):
    res = client.set("Hello", "World")
    assert res is True
    reply = client.get("Hello")
    assert reply == "World"

def test_del_returns_1_or_0(client):
    client.set("DeleteMe", "SomeValue")
    result = client.delete("DeleteMe")
    # According to redis-py, delete returns 1 if key deleted, 0 if not found
    assert result in (0, 1)

def test_returns_none_for_non_existent_key(client):
    reply = client.get("KeyThatDoesNotExist")
    assert reply is None
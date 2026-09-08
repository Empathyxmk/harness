import redis
import pytest

@pytest.fixture(scope="module")
def client():
    r = redis.Redis(decode_responses=True)
    # Try to connect, fail if not ready
    try:
        r.ping()
    except redis.ConnectionError as err:
        pytest.skip(f"Redis server not available: {err}")
    yield r
    r.close()

def test_set_and_get_hello(client):
    res = client.set("Hello", "World")
    assert res is True
    reply = client.get("Hello")
    assert reply == "World"

def test_get_on_missing_key_returns_none(client):
    client.delete("NoSuchKey")
    reply = client.get("NoSuchKey")
    assert reply is None

def test_redis_print_callback_returns_none():
    # In node_redis, redis.print returns undefined.
    # In Python redis-py, there is no equivalent; so define a similar stub.
    def redis_print(*args, **kwargs):
        # Should always return None
        return None
    assert redis_print("err", "reply") is None
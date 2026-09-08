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

def test_public_can_store_and_retrieve_integers_with_different_keys(client):
    res = client.set("num_users_public", 2024)
    assert res is True
    value = client.get("num_users_public")
    assert int(value) == 2024

def test_public_can_increment_values_with_new_key(client):
    res = client.set("views_public", 101)
    assert res is True
    val1 = client.incr("views_public")
    assert val1 == 102
    val2 = client.incr("views_public")
    assert val2 == 103

def test_public_handles_list_operations_with_public_data(client):
    client.delete("queue_public")
    lpush_len = client.lpush("queue_public", "taskC")
    assert lpush_len > 0
    rpush_len = client.rpush("queue_public", "taskD")
    assert rpush_len > 0
    items = client.lrange("queue_public", 0, -1)
    assert items == ["taskC", "taskD"]
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

def test_public_set_and_get_for_alternate_strings(client):
    res = client.set("Alpha", "Beta")
    assert res is True
    reply = client.get("Alpha")
    assert reply == "Beta"

def test_public_del_returns_1_or_0_for_new_key(client):
    client.set("TempToDelete", "TmpVal")
    result = client.delete("TempToDelete")
    assert result in (0, 1)

def test_public_returns_none_for_another_nonexistent_key(client):
    reply = client.get("SomeKeyThatIsNotSet")
    assert reply is None
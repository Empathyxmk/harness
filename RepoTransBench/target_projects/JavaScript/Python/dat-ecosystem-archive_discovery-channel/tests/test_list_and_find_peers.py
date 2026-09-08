import random
from src.discovery import Discovery

def test_list_scenarios():
    channel_id = bytes([random.randint(0, 255) for _ in range(32)])
    d = Discovery({'dht': False, 'dns': False})
    # add
    d.join(channel_id)
    assert d.list() == [channel_id], "first join"
    d.leave(channel_id)
    assert d.list() == [], "after leave (should be empty)"
    d.join(channel_id, 8080)
    assert d.list() == [channel_id], "join id, 8080"
    d.leave(channel_id)
    assert d.list() == [], "after leave again (should be empty)"
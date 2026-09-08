import pytest
from src.discovery import DiscoveryChannel

def test_join_leave_list_and_hash_flows():
    chd = DiscoveryChannel()
    try:
        chd.join("mytopic", {"port": 0})
        chd.leave("mytopic")
        chd.list("mytopic")
        chd.list(bytes(32))
    except Exception:
        pytest.fail("join/leave/list/list(buffer) should not throw")

def test_destroy_disables_further_commands():
    chd = DiscoveryChannel()
    chd.destroy()
    assert chd.destroyed, "should be destroyed"
    try:
        chd.join("topicX")
        chd.leave("foo")
        chd.list("foo")
    except Exception:
        pytest.fail("join/leave/list after destroy should not throw")
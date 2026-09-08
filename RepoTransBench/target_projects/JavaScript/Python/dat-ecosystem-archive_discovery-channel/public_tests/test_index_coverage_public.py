import pytest
from src.discovery import DiscoveryChannel

def test_join_leave_list_and_hash_flows_public():
    chd = DiscoveryChannel()
    try:
        chd.join("publictopic", {"port": 1})
        chd.leave("publictopic")
        chd.list("publictopic")
        chd.list(bytes(16))
    except Exception:
        pytest.fail("join/leave/list/list(buffer) should not throw")

def test_destroy_disables_further_commands_public():
    chd = DiscoveryChannel()
    chd.destroy()
    assert chd.destroyed, "should be destroyed"
    try:
        chd.join("topicY")
        chd.leave("bar")
        chd.list("bar")
    except Exception:
        pytest.fail("join/leave/list after destroy should not throw")
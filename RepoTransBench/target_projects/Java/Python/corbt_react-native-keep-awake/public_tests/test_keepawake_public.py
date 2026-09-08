import pytest

from src.keepawake import KeepAwake

class TestKeepAwakePublic:

    def test_not_awake_after_construction(self):
        ka = KeepAwake()
        # Check initial state remains sleeping and not awake
        assert ka.isAwake() is False
        assert ka.getStatus() != "Awake"
        assert ka.getStatus() == "Sleeping"

    def test_activate_from_false(self):
        ka = KeepAwake()
        ka.activate()
        assert ka.isAwake() is True
        # Confirm getStatus gives "Awake"
        assert "Awake" in ka.getStatus()

    def test_deactivate_after_activation(self):
        ka = KeepAwake()
        ka.setAwake(True)  # Activate using setAwake
        ka.deactivate()
        # Should now be sleeping
        assert ka.isAwake() is False
        assert ka.getStatus() != "Awake"

    def test_multiple_activates_remain_awake(self):
        ka = KeepAwake()
        # Activate multiple times
        ka.activate()
        ka.activate()
        ka.activate()
        assert ka.isAwake() is True
        assert ka.getStatus() == "Awake"

    def test_multiple_deactivates_remain_sleeping(self):
        ka = KeepAwake()
        ka.deactivate()
        ka.deactivate()
        assert ka.isAwake() is False
        assert ka.getStatus() == "Sleeping"

    def test_set_awake_to_true_sets_awake_status(self):
        ka = KeepAwake()
        ka.setAwake(True)
        assert ka.isAwake() is True
        assert ka.getStatus() == "Awake"

    def test_set_awake_to_false_from_awake(self):
        ka = KeepAwake()
        ka.activate()
        ka.setAwake(False)
        assert ka.isAwake() is False
        assert ka.getStatus() == "Sleeping"

    def test_toggle_multiple_times(self):
        ka = KeepAwake()
        ka.activate()
        assert ka.getStatus() == "Awake"
        ka.deactivate()
        assert ka.getStatus() == "Sleeping"
        ka.activate()
        assert ka.getStatus() == "Awake"
        ka.deactivate()
        assert ka.getStatus() == "Sleeping"
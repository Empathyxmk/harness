import pytest

from src.keepawake import KeepAwake

class TestKeepAwake:

    def test_initial_state(self):
        ka = KeepAwake()
        assert not ka.isAwake()
        assert ka.getStatus() == "Sleeping"

    def test_activate(self):
        ka = KeepAwake()
        ka.activate()
        assert ka.isAwake()
        assert ka.getStatus() == "Awake"

    def test_deactivate(self):
        ka = KeepAwake()
        ka.activate()
        ka.deactivate()
        assert not ka.isAwake()
        assert ka.getStatus() == "Sleeping"

    def test_activate_idempotence(self):
        ka = KeepAwake()
        ka.activate()
        ka.activate()  # Should remain true
        assert ka.isAwake()

    def test_deactivate_idempotence(self):
        ka = KeepAwake()
        ka.deactivate()  # Still false
        assert not ka.isAwake()

    def test_set_awake_true(self):
        ka = KeepAwake()
        ka.setAwake(True)
        assert ka.isAwake()

    def test_set_awake_false(self):
        ka = KeepAwake()
        ka.setAwake(True)
        ka.setAwake(False)
        assert not ka.isAwake()

    def test_multiple_transitions(self):
        ka = KeepAwake()
        ka.setAwake(True)
        assert ka.getStatus() == "Awake"
        ka.setAwake(False)
        assert ka.getStatus() == "Sleeping"
        ka.setAwake(True)
        assert ka.getStatus() == "Awake"
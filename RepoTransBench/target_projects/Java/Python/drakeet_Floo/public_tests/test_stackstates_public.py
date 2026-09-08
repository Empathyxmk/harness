def test_stackstates_state_values_public():
    class StackStates:
        ACTIVE = "ACTIVE"
        PAUSED = "PAUSED"
        DESTROYED = "DESTROYED"
    assert StackStates.ACTIVE != StackStates.PAUSED
    assert StackStates.PAUSED != StackStates.DESTROYED

def test_stackstates_state_equality_public():
    class StackStates:
        ACTIVE = "ACTIVE"
        PAUSED = "PAUSED"
        DESTROYED = "DESTROYED"
    assert StackStates.ACTIVE == "ACTIVE"
    assert StackStates.ACTIVE != "PAUSED"
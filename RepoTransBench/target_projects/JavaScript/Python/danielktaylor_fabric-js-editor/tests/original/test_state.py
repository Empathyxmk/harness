import pytest
import json

# Minimal StateModule implementation based on behavior inferred from tests
def StateModule(get_state, set_state):
    if not callable(get_state):
        raise Exception("get_state must be provided")
    if not callable(set_state):
        raise Exception("set_state must be provided")
    class State:
        def __init__(self):
            self._stack = [get_state()]
            self._index = 0
            self._max_len = 100

        def save(self):
            nv = get_state()
            if nv == self._stack[self._index]:
                return  # Don't push duplicate state
            # If undo was used and we are not at top, fork (remove all redo states)
            if self._index < len(self._stack)-1:
                self._stack = self._stack[:self._index+1]
            self._stack.append(nv)
            # Cap stack length to 100
            if len(self._stack) > self._max_len:
                self._stack = self._stack[-self._max_len:]
            else:
                self._index += 1

        def undo(self):
            if self._index == 0:
                return
            self._index -= 1
            set_state(self._stack[self._index])

        def redo(self):
            if self._index >= len(self._stack)-1:
                return
            self._index += 1
            set_state(self._stack[self._index])

        def getStack(self):
            return self._stack.copy()

        def getIndex(self):
            return self._index

    return State()

# --- Begin translation of tests ---

class TestStateModule:
    def setup_method(self):
        self.history = []
        self.currentVal = {'v': 0}
        def get_state():
            return json.dumps(self.currentVal)
        def set_state(nv):
            self.currentVal = json.loads(nv)
            self.history.append(self.currentVal.copy())
        self.state = StateModule(get_state, set_state)

    def test_should_save_pushstate_new_states(self):
        self.currentVal['v'] = 1
        self.state.save()
        self.currentVal['v'] = 2
        self.state.save()
        assert self.history == []
        self.state.undo()
        assert self.currentVal == {'v': 1}
        self.state.redo()
        assert self.currentVal == {'v': 2}

    def test_should_not_save_same_state_twice_does_not_push_duplicate(self):
        self.currentVal['v'] = 1
        self.state.save()
        stackLen = len(self.state.getStack())
        self.state.save()  # no change, should not push
        assert len(self.state.getStack()) == stackLen
        self.state.undo()
        assert self.currentVal == {'v': 0}

    def test_undo_at_first_state_does_nothing(self):
        self.state.undo()
        assert len(self.history) == 0
        assert self.currentVal == {'v': 0}

    def test_redo_at_last_state_does_nothing(self):
        self.currentVal['v'] = 1
        self.state.save()
        self.state.redo()
        assert len(self.history) == 0
        assert self.currentVal == {'v': 1}

    def test_undo_redo_normal_sequence(self):
        self.currentVal['v'] = 1
        self.state.save()
        self.currentVal['v'] = 2
        self.state.save()
        self.state.undo()
        assert self.currentVal == {'v': 1}
        self.state.undo()
        assert self.currentVal == {'v': 0}
        self.state.undo()
        assert self.currentVal == {'v': 0}
        self.state.redo()
        assert self.currentVal == {'v': 1}
        self.state.redo()
        assert self.currentVal == {'v': 2}
        self.state.redo()
        assert self.currentVal == {'v': 2}

    def test_should_cap_states_to_100(self):
        for i in range(1, 102):
            self.currentVal['v'] = i
            self.state.save()
        assert len(self.state.getStack()) == 100
        for _ in range(1, 100):
            self.state.undo()
        # The oldest entry left should be v=2
        assert self.currentVal['v'] == 2

    def test_should_fork_stack_if_set_after_undo(self):
        self.currentVal['v'] = 1
        self.state.save()
        self.currentVal['v'] = 2
        self.state.save()
        self.state.undo()  # now at v=1
        self.currentVal['v'] = 7
        self.state.save()
        stack = self.state.getStack()
        idx = self.state.getIndex()
        assert stack[idx] == json.dumps({'v': 7})
        assert len(stack) == 3
        self.state.redo()
        assert self.currentVal['v'] == 7

    def test_throws_if_getState_is_missing(self):
        with pytest.raises(Exception):
            StateModule(None, lambda nv: None)

    def test_throws_if_setState_is_missing(self):
        with pytest.raises(Exception):
            StateModule(lambda: '{}', None)

    def test_getStack_and_getIndex_reflect_correct_internals(self):
        assert self.state.getStack()[0] == json.dumps({'v': 0})
        assert self.state.getIndex() == 0
        self.currentVal['v'] = 47
        self.state.save()
        assert self.state.getStack()[1] == json.dumps({'v': 47})
        assert self.state.getIndex() == 1
        self.state.undo()
        assert self.state.getIndex() == 0
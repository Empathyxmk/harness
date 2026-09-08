import pytest
import json

# Import the same StateModule as above for testing public tests
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
                return
            if self._index < len(self._stack) - 1:
                self._stack = self._stack[:self._index+1]
            self._stack.append(nv)
            # Cap to 100 states
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

class TestStateModulePublic:
    def setup_method(self):
        self.history = []
        self.currentVal = {'a': 10}
        def get_state():
            return json.dumps(self.currentVal)
        def set_state(nv):
            self.currentVal = json.loads(nv)
            self.history.append(self.currentVal.copy())
        self.state = StateModule(get_state, set_state)

    def test_should_save_pushstate_new_states_public(self):
        self.currentVal['a'] = 20
        self.state.save()
        self.currentVal['a'] = 30
        self.state.save()
        assert self.history == []
        self.state.undo()
        assert self.currentVal == {'a': 20}
        self.state.redo()
        assert self.currentVal == {'a': 30}

    def test_should_not_save_same_state_twice_public(self):
        self.currentVal['a'] = 15
        self.state.save()
        stackLen = len(self.state.getStack())
        self.state.save()  # no change, should not push
        assert len(self.state.getStack()) == stackLen
        self.state.undo()
        assert self.currentVal == {'a': 10}

    def test_undo_at_first_state_does_nothing_public(self):
        self.state.undo()
        assert len(self.history) == 0
        assert self.currentVal == {'a': 10}

    def test_redo_at_last_state_does_nothing_public(self):
        self.currentVal['a'] = 42
        self.state.save()
        self.state.redo()
        assert len(self.history) == 0
        assert self.currentVal == {'a': 42}

    def test_undo_redo_normal_sequence_public(self):
        self.currentVal['a'] = 11
        self.state.save()
        self.currentVal['a'] = 22
        self.state.save()
        self.state.undo()
        assert self.currentVal == {'a': 11}
        self.state.undo()
        assert self.currentVal == {'a': 10}
        self.state.undo()
        assert self.currentVal == {'a': 10}
        self.state.redo()
        assert self.currentVal == {'a': 11}
        self.state.redo()
        assert self.currentVal == {'a': 22}
        self.state.redo()
        assert self.currentVal == {'a': 22}

    def test_should_cap_states_to_100_public(self):
        for i in range(1, 106):
            self.currentVal['a'] = i * 2
            self.state.save()
        assert len(self.state.getStack()) == 100
        for _ in range(1, 100):
            self.state.undo()
        # 6th inserted value: initial is a=10, next a=2, 4, 6, 8, 10, 12...
        assert self.currentVal['a'] == 12

    def test_should_fork_stack_if_set_after_undo_public(self):
        self.currentVal['a'] = 7
        self.state.save()
        self.currentVal['a'] = 21
        self.state.save()
        self.state.undo()
        self.currentVal['a'] = 99
        self.state.save()
        stack = self.state.getStack()
        idx = self.state.getIndex()
        assert stack[idx] == json.dumps({'a': 99})
        assert len(stack) == 3
        self.state.redo()
        assert self.currentVal['a'] == 99

    def test_throws_if_getState_is_missing_public(self):
        with pytest.raises(Exception):
            StateModule(None, lambda nv: None)

    def test_throws_if_setState_is_missing_public(self):
        with pytest.raises(Exception):
            StateModule(lambda: '{}', None)

    def test_getStack_and_getIndex_reflect_correct_internals_public(self):
        assert self.state.getStack()[0] == json.dumps({'a': 10})
        assert self.state.getIndex() == 0
        self.currentVal['a'] = 1234
        self.state.save()
        assert self.state.getStack()[1] == json.dumps({'a': 1234})
        assert self.state.getIndex() == 1
        self.state.undo()
        assert self.state.getIndex() == 0
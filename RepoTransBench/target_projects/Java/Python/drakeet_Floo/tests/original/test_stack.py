def test_stack_states_and_result():
    class StackStates:
        STATE_CREATED = "created"
        STATE_INITED = "inited"
    class Stack:
        def __init__(self):
            self._state = StackStates.STATE_CREATED
            self._result = None
            self._callback = None
        def get_state(self):
            return self._state
        def set_state(self, st):
            self._state = st
        def set_result(self, val):
            self._result = val
        def get_result(self):
            return self._result
        def set_callback(self, cb):
            self._callback = cb
        def on_result(self):
            if self._callback: self._callback(self)

    stack = Stack()
    assert stack.get_state() == "created"
    stack.set_state("inited")
    assert stack.get_state() == "inited"

    stack.set_result("result")
    assert stack.get_result() == "result"

def test_stack_callback():
    called = {"flag": False}

    class Stack:
        def __init__(self):
            self._callback = None
        def set_callback(self, cb):
            self._callback = cb
        def on_result(self):
            if self._callback:
                self._callback(self)
    class StackCallback:
        def __init__(self):
            self.called = False
        def __call__(self, s):
            self.called = True
            assert s is stack

    stack = Stack()
    cb = StackCallback()
    stack.set_callback(cb)
    stack.on_result()
    assert cb.called is True
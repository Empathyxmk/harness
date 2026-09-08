def test_stack_push_then_pop_public():
    class Stack:
        def __init__(self):
            self._lst = []
        def push(self, v):
            self._lst.append(v)
        def pop(self):
            if not self._lst: return None
            return self._lst.pop()
        def is_empty(self):
            return len(self._lst) == 0
    stack = Stack()
    stack.push(99)
    stack.push(42)
    assert stack.pop() == 42
    assert stack.pop() == 99

def test_stack_is_empty_public():
    class Stack:
        def __init__(self):
            self._lst = []
        def push(self, v):
            self._lst.append(v)
        def pop(self):
            if not self._lst: return None
            return self._lst.pop()
        def is_empty(self):
            return len(self._lst) == 0
    s = Stack()
    assert s.is_empty()
    s.push(1)
    assert not s.is_empty()
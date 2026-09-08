def test_stackmanager_push_pop_public():
    class StackManager:
        def __init__(self):
            self._lst = []
        def push(self, v):
            self._lst.append(v)
        def pop(self):
            if not self._lst:
                return None
            return self._lst.pop()
    manager = StackManager()
    manager.push("alpha")
    manager.push("beta")
    assert manager.pop() == "beta"
    assert manager.pop() == "alpha"

def test_stackmanager_pop_on_empty_public():
    class StackManager:
        def __init__(self):
            self._lst = []
        def push(self, v):
            self._lst.append(v)
        def pop(self):
            if not self._lst: return None
            return self._lst.pop()
    manager = StackManager()
    assert manager.pop() is None
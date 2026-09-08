def test_stackmanager_push_and_peek():
    class Stack: pass
    class StackManager:
        def __init__(self):
            self._lst = []
        def push(self, stack):
            self._lst.append(stack)
        def peek(self):
            if self._lst: return self._lst[-1]
            else: return None
        def pop(self):
            if self._lst: return self._lst.pop()
            else: return None
        def is_not_empty(self):
            return bool(self._lst)

    stackmanager = StackManager()
    stack = Stack()
    stackmanager.push(stack)
    assert stackmanager.peek() is stack

def test_stackmanager_pop_and_empty():
    class Stack: pass
    class StackManager:
        def __init__(self):
            self._lst = []
        def push(self, stack):
            self._lst.append(stack)
        def peek(self):
            if self._lst: return self._lst[-1]
            else: return None
        def pop(self):
            if self._lst: return self._lst.pop()
            else: return None
        def is_not_empty(self):
            return bool(self._lst)
    stackmanager = StackManager()
    stack = Stack()
    stackmanager.push(stack)
    popped = stackmanager.pop()
    assert popped is stack
    assert stackmanager.peek() is None

def test_stackmanager_empty_pop():
    class StackManager:
        def __init__(self):
            self._lst = []
        def push(self, stack):
            self._lst.append(stack)
        def pop(self):
            if self._lst: return self._lst.pop()
            else: return None
    stackmanager = StackManager()
    assert stackmanager.pop() is None

def test_stackmanager_is_not_empty():
    class Stack: pass
    class StackManager:
        def __init__(self):
            self._lst = []
        def push(self, stack):
            self._lst.append(stack)
        def is_not_empty(self):
            return bool(self._lst)
    stackmanager = StackManager()
    assert stackmanager.is_not_empty() is False
    stackmanager.push(Stack())
    assert stackmanager.is_not_empty() is True
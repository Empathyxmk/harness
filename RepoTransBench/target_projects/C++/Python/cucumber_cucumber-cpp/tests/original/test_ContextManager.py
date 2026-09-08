import pytest

class Context1:
    pass
class Context2:
    pass

class ContextManagerTestDouble:
    def __init__(self):
        self.contexts = []
    def addContext(self, cls):
        c = cls()
        self.contexts.append(c)
        return c
    def countContexts(self):
        return len(self.contexts)
    def purgeContexts(self):
        self.contexts = []

class TestContextManager:
    def setup_method(self):
        self.contextManager = ContextManagerTestDouble()
    def teardown_method(self):
        self.contextManager.purgeContexts()

    def test_creates_valid_context_pointers(self):
        ctx1 = self.contextManager.addContext(Context1)
        assert self.contextManager.countContexts() == 1
        assert ctx1 is not None
        ctx2 = self.contextManager.addContext(Context2)
        assert self.contextManager.countContexts() == 2
        assert ctx2 is not None

    def test_allows_creating_the_same_context_type_twice(self):
        ctx1 = self.contextManager.addContext(Context1)
        assert self.contextManager.countContexts() == 1
        assert ctx1 is not None
        ctx2 = self.contextManager.addContext(Context1)
        assert self.contextManager.countContexts() == 2
        assert ctx2 is not None
        assert ctx1 is not ctx2

    def test_purges_contexts(self):
        ctx1 = self.contextManager.addContext(Context1)
        assert self.contextManager.countContexts() == 1
        assert ctx1 is not None
        self.contextManager.purgeContexts()
        assert self.contextManager.countContexts() == 0
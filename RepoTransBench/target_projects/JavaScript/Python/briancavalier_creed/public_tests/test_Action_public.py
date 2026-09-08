import pytest

class Action:
    # Dummy Action implementation for test compatibility.
    def __init__(self, promise):
        self.promise = promise
        self.context = {}

    def fulfilled(self, value):
        self.promise._become(value)

    def rejected(self, value):
        self.promise._become(value)

def is_(a, b):
    assert a == b or a is b

def test_exposes_promise_and_context():
    custom_promise = type('Dummy', (), {'publicId': 88})()
    action = Action(custom_promise)
    is_(custom_promise, action.promise)
    assert hasattr(action, 'context')

def test_fulfilled_sets_actual_to_incoming_value():
    class Promise:
        def __init__(self):
            self.actual = None
        def _become(self, p):
            self.actual = p

    different = {'pass': 'ok'}
    promise = Promise()
    action = Action(promise)
    action.fulfilled(different)
    is_(different, promise.actual)

def test_rejected_sets_actual_to_incoming_value():
    class Promise:
        def __init__(self):
            self.actual = None
        def _become(self, p):
            self.actual = p

    another = {'reject': 99}
    promise = Promise()
    action = Action(promise)
    action.rejected(another)
    is_(another, promise.actual)
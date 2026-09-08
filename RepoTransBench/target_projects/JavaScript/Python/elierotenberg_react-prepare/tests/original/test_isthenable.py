def is_thenable(obj):
    # Simulates JS isThenable: has a callable 'then' attribute
    return hasattr(obj, 'then') and callable(getattr(obj, 'then'))

def test_recognizes_native_promise_as_thenable():
    class Promise:
        def then(self): pass
        @staticmethod
        def resolve(): return Promise()
    assert is_thenable(Promise.resolve())

def test_recognizes_null_as_non_thenable():
    assert not is_thenable(None)

def test_recognizes_undefined_as_non_thenable():
    # Python's None is equivalent to JS undefined for this logic
    assert not is_thenable(None)

def test_recognizes_function_as_non_thenable():
    def non_thenable(): pass
    assert not is_thenable(non_thenable)

def test_recognizes_arrow_as_non_thenable():
    assert not is_thenable(lambda: None)

def test_recognizes_custom_thenable_as_thenable():
    class Thenable:
        def then(self): return
    thenable = Thenable()
    assert is_thenable(thenable)
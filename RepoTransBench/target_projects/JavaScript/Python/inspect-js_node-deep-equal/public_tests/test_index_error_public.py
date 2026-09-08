from src.deep_equal import deep_equal

def test_error_objects_equal_typeerror():
    class MyTypeError(Exception): pass
    err1 = MyTypeError('type fail')
    err2 = MyTypeError('type fail')
    assert deep_equal(err1, err2)

def test_error_objects_not_equal_referenceerror():
    class MyReferenceError(Exception): pass
    err1 = MyReferenceError('missing')
    err2 = MyReferenceError('not found')
    assert not deep_equal(err1, err2)
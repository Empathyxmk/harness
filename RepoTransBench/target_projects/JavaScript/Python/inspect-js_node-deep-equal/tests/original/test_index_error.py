from src.deep_equal import deep_equal

def test_error_objects_equal():
    err1 = Exception('fail')
    err2 = Exception('fail')
    assert deep_equal(err1, err2)

def test_error_objects_not_equal():
    err1 = Exception('fail')
    err2 = Exception('success')
    assert not deep_equal(err1, err2)
class AsyncDaoException(Exception):
    pass

def test_message():
    ex = AsyncDaoException("msg")
    assert str(ex) == "msg"
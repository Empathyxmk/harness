class AsyncDaoException(Exception):
    pass

def test_message():
    ex = AsyncDaoException("testPublicMsg")
    assert str(ex) == "testPublicMsg"
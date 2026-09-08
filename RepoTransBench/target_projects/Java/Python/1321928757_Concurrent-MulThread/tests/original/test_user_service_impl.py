import pytest

class UserDO:
    def __init__(self, user_name):
        self.user_name = user_name

    def getUserName(self):
        return self.user_name

class UserReq:
    def __init__(self):
        self.user_name = None

    def setUserName(self, name):
        self.user_name = name

    def getUserName(self):
        return self.user_name

class UserServiceImpl:
    def __init__(self):
        self.users = []

    def add(self, req):
        # Simulate adding user always succeeds (duplicates allowed)
        self.users.append(UserDO(req.getUserName()))
        return True

    def queryAll(self):
        return self.users[:]

import pytest

@pytest.fixture(autouse=True)
def setup_user_service(monkeypatch):
    pass  # JUnit's setUp replaced with local object init

def test_add_user():
    userService = UserServiceImpl()
    req = UserReq()
    req.setUserName("bob")
    result = userService.add(req)
    assert result is True

    users = userService.queryAll()
    has_bob = any(u.getUserName() == "bob" for u in users)
    assert has_bob

def test_query_all():
    userService = UserServiceImpl()
    req = UserReq()
    req.setUserName("alice")
    userService.add(req)
    users = userService.queryAll()
    assert users is not None
    assert len(users) > 0

def test_add_duplicate_user():
    userService = UserServiceImpl()
    req = UserReq()
    req.setUserName("john")
    userService.add(req)
    # Add duplicate "john"
    result = userService.add(req)
    assert result is True
    users = userService.queryAll()
    johns = [u for u in users if u.getUserName() == "john"]
    assert len(johns) >= 2
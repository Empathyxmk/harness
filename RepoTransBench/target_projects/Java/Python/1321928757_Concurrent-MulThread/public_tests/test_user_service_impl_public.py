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
        self.users.append(UserDO(req.getUserName()))
        return True

    def queryAll(self):
        return self.users[:]

@pytest.fixture
def user_service_populated():
    service = UserServiceImpl()
    req = UserReq()
    req.setUserName("publicuser")
    service.add(req)
    return service

def test_add_user(user_service_populated):
    req = UserReq()
    req.setUserName("bob")
    result = user_service_populated.add(req)
    assert result

    users = user_service_populated.queryAll()
    has_bob = any(u.getUserName() == "bob" for u in users)
    assert has_bob

def test_query_all(user_service_populated):
    users = user_service_populated.queryAll()
    assert users is not None
    assert len(users) > 0

def test_add_duplicate_user(user_service_populated):
    req = UserReq()
    req.setUserName("publicuser")  # Already present from setup
    result = user_service_populated.add(req)
    assert result
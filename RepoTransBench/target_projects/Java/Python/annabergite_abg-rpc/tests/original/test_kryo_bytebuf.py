import pytest

class User:
    def __init__(self, id):
        self.id = id
    def __eq__(self, other):
        return isinstance(other, User) and self.id == other.id
    def __repr__(self):
        return f"User({self.id})"

class ArrayListObj:
    def __init__(self):
        self.list = list(range(32))

class ComplexObj:
    def __init__(self):
        self.IntObj = 2
        self.LocalDateTimeObj = "now"
        self.StringUTF8Obj = "中国 北京 中关村"
        self.StringASCIIObj = "AaBbCcDdEe"
        self.ArrayListObj = ArrayListObj()

class UserService:
    def getUser(self, id):
        return User(id)
    def listUser(self, idx):
        return [User(idx), User(idx+1)]

class UserServiceServerImpl(UserService):
    pass

def test_kryo_bytebuf_simulation():
    # Simulate serialization logic
    user_service = UserServiceServerImpl()
    u = user_service.getUser(9223372036854775807)
    assert u == User(9223372036854775807)

    # Simulate repeated buffer/write/read cycle
    users = []
    for i in range(2):
        users.append(user_service.getUser(i))
    assert users == [User(0), User(1)]
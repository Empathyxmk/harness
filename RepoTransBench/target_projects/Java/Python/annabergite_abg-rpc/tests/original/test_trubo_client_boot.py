class User:
    def __init__(self, name):
        self.name = name

class UserService:
    def existUser(self, name):
        return name == "ziboqizhong@outlook.com"
    def getUser(self, id):
        return User("test")
    def createUser(self, user):
        return f"created:{user.name}"
    def listUser(self, n):
        return [User(f"user{n}")]

class TruboClientBootTest:
    def __init__(self):
        self.applicationContext = {"UserService": UserService()}
        self.userService = UserService()
        self.userService2 = UserService()

    def test_logic(self):
        # Simulate test code
        existUser = self.userService.existUser("ziboqizhong@outlook.com")
        assert existUser
        user = self.userService.getUser(1)
        assert user.name == "test"
        result = self.userService2.createUser(user)
        assert result.startswith("created:")
        users = self.userService.listUser(1)
        assert len(users) == 1 and users[0].name.startswith("user")

def test_trubo_client_boot_logic():
    boot = TruboClientBootTest()
    boot.test_logic()
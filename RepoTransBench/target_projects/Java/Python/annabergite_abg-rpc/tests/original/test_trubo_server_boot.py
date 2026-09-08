class UserService:
    def user_method(self):
        return "user"

class TruboServerBootTest:
    def __init__(self):
        self.userService = UserService()

def test_trubo_server_boot_user_service():
    app = TruboServerBootTest()
    assert app.userService.user_method() == "user"
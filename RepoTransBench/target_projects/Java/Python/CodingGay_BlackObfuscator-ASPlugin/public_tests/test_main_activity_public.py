class MainActivity:
    @staticmethod
    def get_welcome_message(name):
        return f"Welcome, {name}!"

def test_get_welcome_message_with_different_user():
    assert MainActivity.get_welcome_message("Charlie") == "Welcome, Charlie!"
    assert MainActivity.get_welcome_message("Zoe") == "Welcome, Zoe!"
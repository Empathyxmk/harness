import pytest
from src.example.hello_shiro import HelloShiro

class TestHelloShiro:

    def setup_method(self):
        self.shiro = HelloShiro()

    def test_login_success(self):
        assert self.shiro.login("admin", "adminpass")
        assert self.shiro.is_authenticated()
        assert self.shiro.get_user() == "admin"
        assert self.shiro.get_welcome_message() == "Welcome, admin!"

    def test_login_failure_bad_password(self):
        assert not self.shiro.login("admin", "wrongpass")
        assert not self.shiro.is_authenticated()
        assert self.shiro.get_user() is None
        assert self.shiro.get_welcome_message() == "Please log in."

    def test_login_failure_unknown_user(self):
        assert not self.shiro.login("bob", "somepass")
        assert not self.shiro.is_authenticated()
        assert self.shiro.get_user() is None
        assert self.shiro.get_welcome_message() == "Please log in."

    def test_logout(self):
        self.shiro.login("admin", "adminpass")
        self.shiro.logout()
        assert not self.shiro.is_authenticated()
        assert self.shiro.get_user() is None
        assert self.shiro.get_welcome_message() == "Please log in."

    def test_welcome_message_not_authenticated(self):
        assert self.shiro.get_welcome_message() == "Please log in."

    def test_welcome_message_unknown_user(self):
        # Simulate reflection by setting internal fields directly
        self.shiro.authenticated = True
        self.shiro.user = "otheruser"
        assert self.shiro.get_welcome_message() == "Welcome, otheruser!"

    def test_multiple_login_logout_cycles(self):
        assert self.shiro.login("admin", "adminpass")
        self.shiro.logout()
        assert not self.shiro.is_authenticated()
        assert self.shiro.get_user() is None
        assert self.shiro.get_welcome_message() == "Please log in."

        assert not self.shiro.login("test", "bad")
        assert not self.shiro.is_authenticated()
        assert self.shiro.get_user() is None
        assert self.shiro.get_welcome_message() == "Please log in."

        assert self.shiro.login("admin", "adminpass")
        assert self.shiro.is_authenticated()
        assert self.shiro.get_user() == "admin"
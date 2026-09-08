import pytest
from src.example.hello_shiro import HelloShiro

class TestHelloShiroPublic:

    def setup_method(self):
        self.shiro = HelloShiro()

    def test_login_success_public(self):
        # Test with different case for strict equality
        assert not self.shiro.login("Admin", "Adminpass")
        assert not self.shiro.is_authenticated()
        assert self.shiro.get_user() is None
        assert self.shiro.get_welcome_message() == "Please log in."

        # Test with leading/trailing spaces
        assert not self.shiro.login(" admin ", " adminpass ")
        assert not self.shiro.is_authenticated()
        assert self.shiro.get_user() is None
        assert self.shiro.get_welcome_message() == "Please log in."

    def test_login_failure_empty_fields(self):
        assert not self.shiro.login("", "adminpass")
        assert not self.shiro.is_authenticated()
        assert self.shiro.get_user() is None
        assert self.shiro.get_welcome_message() == "Please log in."

        assert not self.shiro.login("admin", "")
        assert not self.shiro.is_authenticated()
        assert self.shiro.get_user() is None
        assert self.shiro.get_welcome_message() == "Please log in."

    def test_login_failure_null_fields(self):
        assert not self.shiro.login(None, "adminpass")
        assert not self.shiro.is_authenticated()
        assert self.shiro.get_user() is None
        assert self.shiro.get_welcome_message() == "Please log in."

        assert not self.shiro.login("admin", None)
        assert not self.shiro.is_authenticated()
        assert self.shiro.get_user() is None
        assert self.shiro.get_welcome_message() == "Please log in."

    def test_logout_after_failed_login(self):
        assert not self.shiro.login("nope", "nope")
        self.shiro.logout()
        assert not self.shiro.is_authenticated()
        assert self.shiro.get_user() is None
        assert self.shiro.get_welcome_message() == "Please log in."

    def test_welcome_message_admin_after_manual_set(self):
        # Set user to "Admin" manually (simulate reflection)
        self.shiro.authenticated = True
        self.shiro.user = "Admin"
        assert self.shiro.get_welcome_message() == "Welcome, Admin!"

    def test_multiple_login_logout_different_usernames(self):
        assert not self.shiro.login("root", "supersecret")
        self.shiro.logout()
        assert not self.shiro.is_authenticated()
        assert self.shiro.get_user() is None
        assert self.shiro.get_welcome_message() == "Please log in."

        assert not self.shiro.login("user", "userpass")
        assert not self.shiro.is_authenticated()
        assert self.shiro.get_user() is None
        assert self.shiro.get_welcome_message() == "Please log in."

        assert self.shiro.login("admin", "adminpass")
        assert self.shiro.is_authenticated()
        assert self.shiro.get_user() == "admin"
        assert self.shiro.get_welcome_message() == "Welcome, admin!"
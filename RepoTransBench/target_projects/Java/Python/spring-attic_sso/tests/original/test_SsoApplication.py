import pytest
from unittest.mock import Mock, call, ANY

# Stub implementations for missing Java classes and methods under test.
class Principal:
    def __init__(self, name):
        self._name = name
    def getName(self):
        return self._name
    def __eq__(self, other):
        return isinstance(other, Principal) and self._name == other._name

# ---- Stubs for SsoApplication and LoginErrors ----

class SsoApplication:
    def dashboard(self):
        return {"message": "Yay!"}
    def user(self, principal):
        return principal
    @staticmethod
    def main(args):
        pass

    class LoginErrors:
        def dashboard(self):
            return "redirect:/#/"
    class LoginConfigurer:
        def csrfHeaderFilter(self):
            # returns a filter object with .do_filter(request, response, chain)
            class Filter:
                def do_filter(self, request, response, chain):
                    csrf_token = request.get_attribute("CsrfToken")
                    if csrf_token is not None:
                        # Simulate adding a cookie
                        cookie = Cookie("XSRF-TOKEN", csrf_token.get_token())
                        response.add_cookie(cookie)
                    chain.do_filter(request, response)
            return Filter()
        def csrfTokenRepository(self):
            class Repo:
                def __init__(self):
                    self.headerName = "X-XSRF-TOKEN"
            return Repo()

class Cookie:
    def __init__(self, name, value):
        self._name = name
        self._value = value
    def getName(self):
        return self._name
    def getValue(self):
        return self._value


# ---- Mocks and CsrfToken stub ----
class CsrfToken:
    def __init__(self, token):
        self._token = token
    def get_token(self):
        return self._token

# --- Test cases as per original Java tests ---

def test_dashboard_message():
    app = SsoApplication()
    message = app.dashboard()
    assert message is not None
    assert message.get("message") == "Yay!"

def test_user_principal():
    app = SsoApplication()
    p = Principal("testuser")
    assert app.user(p) == p
    assert app.user(p).getName() == "testuser"

def test_main_no_args():
    SsoApplication.main([])

def test_login_errors_dashboard():
    errors = SsoApplication.LoginErrors()
    assert errors.dashboard() == "redirect:/#/"

def test_csrf_header_filter_sets_cookie(mocker):
    configurer = SsoApplication.LoginConfigurer()
    chain = Mock()
    request = Mock()
    response = Mock()

    # Prepare csrf token and how request returns it
    csrf_token = CsrfToken("testToken")
    request.get_attribute.side_effect = lambda name: csrf_token if name == "CsrfToken" else None

    filter_obj = configurer.csrfHeaderFilter()
    filter_obj.do_filter(request, response, chain)

    response.add_cookie.assert_called_once()
    # The only call to add_cookie should have a Cookie whose name == "XSRF-TOKEN" and value == "testToken"
    called_cookie = response.add_cookie.call_args[0][0]
    assert isinstance(called_cookie, Cookie)
    assert called_cookie.getName() == "XSRF-TOKEN"
    assert called_cookie.getValue() == "testToken"
    chain.do_filter.assert_called_once_with(request, response)

def test_csrf_header_filter_no_csrf(mocker):
    configurer = SsoApplication.LoginConfigurer()
    chain = Mock()
    request = Mock()
    response = Mock()

    # Simulate request.get_attribute returns None for CsrfToken
    request.get_attribute.side_effect = lambda name: None

    filter_obj = configurer.csrfHeaderFilter()
    filter_obj.do_filter(request, response, chain)

    response.add_cookie.assert_not_called()
    chain.do_filter.assert_called_once_with(request, response)

def test_csrf_token_repository():
    configurer = SsoApplication.LoginConfigurer()
    repo = configurer.csrfTokenRepository()
    assert repo is not None
    assert hasattr(repo, "headerName")
    assert getattr(repo, "headerName") == "X-XSRF-TOKEN"
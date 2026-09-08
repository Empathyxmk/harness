import pytest
from unittest.mock import Mock, call, ANY

# Stubs - as in original, but for public test, done here for isolation.
class Principal:
    def __init__(self, name):
        self._name = name
    def getName(self):
        return self._name
    def __eq__(self, other):
        return isinstance(other, Principal) and self._name == other._name

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

class CsrfToken:
    def __init__(self, token):
        self._token = token
    def get_token(self):
        return self._token

def test_dashboard_message_public():
    app = SsoApplication()
    message = app.dashboard()
    assert message is not None
    assert "message" in message
    assert isinstance(message["message"], str)

def test_user_principal_public():
    app = SsoApplication()
    p = Principal("publicuser")
    returned = app.user(p)
    assert returned == p
    assert returned.getName() == "publicuser"

    # Additional: test with unicode username
    special_p = Principal("用户123")
    special_returned = app.user(special_p)
    assert special_returned.getName() == "用户123"

def test_main_with_args_public():
    SsoApplication.main(["--fakeArg=1"])

def test_login_errors_dashboard_public():
    errors = SsoApplication.LoginErrors()
    result = errors.dashboard()
    assert result.startswith("redirect:/#")
    assert "/" in result
    assert result == "redirect:/#/"

def test_csrf_header_filter_sets_cookie_public(mocker):
    configurer = SsoApplication.LoginConfigurer()
    chain = Mock()
    request = Mock()
    response = Mock()

    csrf_token = CsrfToken("publicTokenXYZ")
    request.get_attribute.side_effect = lambda name: csrf_token if name == "CsrfToken" else None

    filter_obj = configurer.csrfHeaderFilter()
    filter_obj.do_filter(request, response, chain)

    # Use custom checking for cookie argument
    response.add_cookie.assert_called_once()
    cookie = response.add_cookie.call_args[0][0]
    assert isinstance(cookie, Cookie)
    assert cookie.getName() == "XSRF-TOKEN"
    assert cookie.getValue() == "publicTokenXYZ"
    chain.do_filter.assert_called_once_with(request, response)

def test_csrf_header_filter_no_csrf_public(mocker):
    configurer = SsoApplication.LoginConfigurer()
    chain = Mock()
    request = Mock()
    response = Mock()

    request.get_attribute.side_effect = lambda name: None

    filter_obj = configurer.csrfHeaderFilter()
    filter_obj.do_filter(request, response, chain)

    response.add_cookie.assert_not_called()
    chain.do_filter.assert_called_once_with(request, response)

def test_csrf_token_repository_public():
    configurer = SsoApplication.LoginConfigurer()
    repo = configurer.csrfTokenRepository()
    assert repo is not None
    headerName = getattr(repo, "headerName", None)
    assert isinstance(headerName, str)
    assert headerName == "X-XSRF-TOKEN"
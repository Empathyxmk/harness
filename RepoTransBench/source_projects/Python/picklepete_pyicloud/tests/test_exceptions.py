import pytest
from pyicloud import exceptions

def test_pyi_cloud_exception():
    ex = exceptions.PyiCloudException("test")
    assert isinstance(ex, Exception)
    assert str(ex) == "test"

def test_pyi_cloud_api_response_exception_basic():
    ex = exceptions.PyiCloudAPIResponseException("error reason")
    assert "error reason" in str(ex)
    assert ex.reason == "error reason"
    assert ex.code is None

def test_pyi_cloud_api_response_exception_full():
    ex = exceptions.PyiCloudAPIResponseException("fail", code="42", retry=True)
    s = str(ex)
    assert "fail" in s and "42" in s and "Retrying" in s
    assert ex.reason == "fail"
    assert ex.code == "42"

def test_service_not_activated_exception():
    ex = exceptions.PyiCloudServiceNotActivatedException("reason")
    assert "reason" in str(ex)

def test_failed_login_exception():
    ex = exceptions.PyiCloudFailedLoginException("login fail")
    assert "login fail" in str(ex)

def test_2sa_required_exception():
    ex = exceptions.PyiCloud2SARequiredException("email@email.com")
    assert "Two-step authentication required for account: email@email.com" in str(ex)

def test_no_stored_password_exception():
    ex = exceptions.PyiCloudNoStoredPasswordAvailableException("no password")
    assert "no password" in str(ex)

def test_no_devices_exception():
    ex = exceptions.PyiCloudNoDevicesException("no device")
    assert "no device" in str(ex)
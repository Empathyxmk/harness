import pytest
from secure.secure import Secure, Preset
from secure.headers.cache_control import CacheControl
from secure.headers.cross_origin_opener_policy import CrossOriginOpenerPolicy
from secure.headers.content_security_policy import ContentSecurityPolicy
from secure.headers.strict_transport_security import StrictTransportSecurity
from secure.headers.permissions_policy import PermissionsPolicy
from secure.headers.referrer_policy import ReferrerPolicy
from secure.headers.server import Server
from secure.headers.x_content_type_options import XContentTypeOptions
from secure.headers.x_frame_options import XFrameOptions
from secure.headers.custom_header import CustomHeader

def test_secure_with_no_headers():
    s = Secure()
    assert s.headers_list == []

def test_secure_with_some_headers():
    c = CacheControl().no_store()
    s = Secure(cache=c)
    assert s.headers_list[0] is c

def test_secure_with_custom_list():
    ch1 = CustomHeader("X-Test", "A")
    ch2 = CustomHeader("X-Foo", "Bar")
    s = Secure(custom=[ch1, ch2])
    assert ch1 in s.headers_list and ch2 in s.headers_list

def test_secure_with_all_headers():
    s = Secure(
        cache=CacheControl().no_store(),
        coop=CrossOriginOpenerPolicy().same_origin(),
        csp=ContentSecurityPolicy().default_src("'none'"),
        hsts=StrictTransportSecurity().max_age(3600),
        permissions=PermissionsPolicy().camera(),
        referrer=ReferrerPolicy().strict_origin_when_cross_origin(),
        server=Server().set("test"),
        xcto=XContentTypeOptions().nosniff(),
        xfo=XFrameOptions().deny(),
        custom=[CustomHeader("X-A", "B")]
    )
    # Should be 10 header objects + number of custom
    assert any(isinstance(h, CustomHeader) for h in s.headers_list)

def test_secure_with_default_headers():
    s = Secure.with_default_headers()
    names = [type(h).__name__ for h in s.headers_list]
    expected_types = {
        "CacheControl", "CrossOriginOpenerPolicy", "ContentSecurityPolicy",
        "StrictTransportSecurity", "PermissionsPolicy", "ReferrerPolicy",
        "Server", "XContentTypeOptions", "XFrameOptions"
    }
    present_types = set(names)
    assert present_types.issuperset(expected_types)
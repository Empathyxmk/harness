import pytest
from secure.secure import Secure
from secure.headers.cache_control import CacheControl
from secure.headers.cross_origin_embedder_policy import CrossOriginEmbedderPolicy
from secure.headers.content_security_policy import ContentSecurityPolicy
from secure.headers.strict_transport_security import StrictTransportSecurity
from secure.headers.permissions_policy import PermissionsPolicy
from secure.headers.referrer_policy import ReferrerPolicy
from secure.headers.server import Server
from secure.headers.x_content_type_options import XContentTypeOptions
from secure.headers.x_frame_options import XFrameOptions
from secure.headers.custom_header import CustomHeader

def test_secure_with_no_custom_headers_public():
    s = Secure()
    assert s.headers_list == []

def test_secure_with_one_header_public():
    c = CacheControl().max_age(1234)
    s = Secure(cache=c)
    assert s.headers_list[0] is c

def test_secure_with_multiple_custom_headers_public():
    ch1 = CustomHeader("X-Public-Header", "Val1")
    ch2 = CustomHeader("X-Diff-Header", "DiffVal")
    s = Secure(custom=[ch1, ch2])
    assert ch1 in s.headers_list and ch2 in s.headers_list

def test_secure_with_various_headers_public():
    s = Secure(
        cache=CacheControl().max_age(500),
        coop=None,
        coep=CrossOriginEmbedderPolicy().require_corp(),
        csp=ContentSecurityPolicy().default_src("'self'"),
        hsts=StrictTransportSecurity().max_age(1800),
        permissions=PermissionsPolicy().microphone(),
        referrer=ReferrerPolicy().no_referrer(),
        server=Server().set("Different"),
        xcto=XContentTypeOptions().nosniff(),
        xfo=XFrameOptions().sameorigin(),
        custom=[CustomHeader("X-B", "C")]
    )
    # Should be one custom header present
    assert any(isinstance(h, CustomHeader) for h in s.headers_list)
    # And the xfo header as well
    assert any(isinstance(h, XFrameOptions) for h in s.headers_list)

def test_secure_with_partial_headers_public():
    # Use only a subset and different than in the original
    s = Secure(
        xcto=XContentTypeOptions().nosniff(),
        server=Server().set("PublicTest"),
        referrer=ReferrerPolicy().origin(),
        custom=[CustomHeader("X-Y", "Z")],
        coop=None,
    )
    # Should have these present by type
    assert any(isinstance(h, XContentTypeOptions) for h in s.headers_list)
    assert any(isinstance(h, Server) for h in s.headers_list)
    assert any(isinstance(h, ReferrerPolicy) for h in s.headers_list)
    # And one custom header
    assert any(isinstance(h, CustomHeader) for h in s.headers_list)
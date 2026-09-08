import pytest
import os
import sys
import base64
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/hokaccha_node_jwt_simple/lib')))
import jwt

@pytest.mark.describe('jwt internal utilities (public)')
class TestJwtInternalUtilitiesPublic:
    def test_base64urlencode_base64urldecode_roundtrip_for_unicode(self):
        s = 'ünicødé!$#@'
        enc = jwt.__test__.base64url_encode(s)
        dec = jwt.__test__.base64url_decode(enc)
        assert dec == s

    def test_base64urlunescape_with_different_strange_input(self):
        inp = '_-_fooBar'
        out = jwt.__test__.base64url_unescape(inp)
        import re
        assert re.match(r'^[-+_]fooBar\/=*$', out)

    def test_assignproperties_only_copies_direct_properties(self):
        class Source:
            def __init__(self):
                self.x = 47
            protoProp = 99
        src = Source()
        dest = {'z': 31}
        jwt.__test__.assign_properties(dest, src)
        assert 'x' in dest
        assert dest['x'] == 47
        assert 'protoProp' not in dest
        assert dest['z'] == 31

    def test_sign_with_another_unknown_type_throws_error(self):
        with pytest.raises(Exception):
            jwt.__test__.sign('q', 'p', 'sha384', 'unknown-alg')

    def test_verify_with_another_unknown_type_returns_false(self):
        assert jwt.__test__.verify('q', 'p', 'sha384', 'unknown-alg', 'someSig') is False

@pytest.mark.describe('jwt.decode error edge (public)')
class TestJwtDecodeErrorEdgePublic:
    def test_throws_error_on_different_invalid_header_json(self):
        part1 = base64.b64encode(b'{:wrong}').decode('ascii')
        part2 = base64.b64encode(b'{"x":7}').decode('ascii')
        token = '.'.join([part1, part2, 'segsig'])
        with pytest.raises(Exception):
            jwt.decode(token, 'otherkey')

    def test_throws_error_on_different_invalid_payload_json(self):
        part1 = base64.b64encode(b'{"alg":"HS384"}').decode('ascii')
        part2 = base64.b64encode(b'not-real-json').decode('ascii')
        token = '.'.join([part1, part2, 'difsig'])
        with pytest.raises(Exception):
            jwt.decode(token, 'otherkey')
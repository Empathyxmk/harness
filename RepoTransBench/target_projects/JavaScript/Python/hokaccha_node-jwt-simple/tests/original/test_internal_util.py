import pytest
import os
import sys
import base64
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/hokaccha_node_jwt_simple/lib')))
import jwt

@pytest.mark.describe('jwt internal utilities')
class TestJwtInternalUtilities:
    def test_base64urlencode_base64urldecode_roundtrip_for_ascii(self):
        s = 'foobar123'
        enc = jwt.__test__.base64url_encode(s)
        dec = jwt.__test__.base64url_decode(enc)
        assert dec == s

    def test_base64urlunescape_with_strange_input(self):
        inp = 'abc-def_'
        out = jwt.__test__.base64url_unescape(inp)
        import re
        assert re.match(r'^abc\+def\/=+$', out)

    def test_assignproperties_copies_own_properties_only(self):
        dest = {'a': 1}
        src = {'b': 2}
        jwt.__test__.assign_properties(dest, src)
        assert 'b' in dest and dest['b'] == 2
        assert 'foo' not in dest

    def test_sign_with_unknown_type_throws_error(self):
        with pytest.raises(Exception):
            jwt.__test__.sign('x', 'y', 'sha256', 'none')

    def test_verify_with_unknown_type_returns_false(self):
        assert jwt.__test__.verify('x', 'y', 'sha256', 'none', 'sig') is False

@pytest.mark.describe('jwt.decode error edge')
class TestJwtDecodeErrorEdge:
    def test_throws_error_on_invalid_header_json(self):
        part1 = base64.b64encode(b'notjson').decode('ascii')
        part2 = base64.b64encode(b'{}').decode('ascii')
        token = '.'.join([part1, part2, 'sig'])
        with pytest.raises(Exception):
            jwt.decode(token, 'key')

    def test_throws_error_on_invalid_payload_json(self):
        part1 = base64.b64encode(b'{"alg":"HS256"}').decode('ascii')
        part2 = base64.b64encode(b'notjson').decode('ascii')
        token = '.'.join([part1, part2, 'sig'])
        with pytest.raises(Exception):
            jwt.decode(token, 'key')
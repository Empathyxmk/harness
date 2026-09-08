import pytest
import os
import sys
import base64
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/hokaccha_node_jwt_simple/lib')))
import jwt

@pytest.mark.describe('jwt encode/decode')
class TestJwtEncodeDecode:
    def test_should_encode_and_decode_with_hs256(self):
        secret = 'my secret'
        payload = {'foo': 'bar', 'iat': int(__import__("time").time())}
        token = jwt.encode(payload, secret, 'HS256')
        decoded = jwt.decode(token, secret, False, 'HS256')
        assert decoded['foo'] == 'bar'

    def test_should_throw_with_wrong_secret(self):
        secret = 'my secret'
        payload = {'foo': 'bar', 'iat': int(__import__("time").time())}
        token = jwt.encode(payload, secret, 'HS256')
        with pytest.raises(Exception):
            jwt.decode(token, 'wrong secret', False, 'HS256')

    def test_should_encode_and_decode_with_default_algorithm(self):
        secret = 'my secret'
        payload = {'hello': 'world'}
        token = jwt.encode(payload, secret)
        decoded = jwt.decode(token, secret)
        assert decoded['hello'] == 'world'

    def test_should_support_additional_header_fields(self):
        secret = 'my secret'
        payload = {'foo': 'bar'}
        header = {'kid': '123', 'cty': 'jwt'}
        token = jwt.encode(payload, secret, 'HS256', header=header)
        decoded = jwt.decode(token, secret, False, 'HS256')
        token_parts = token.split('.')
        decoded_header = json.loads(base64.b64decode(token_parts[0] + '=' * (-len(token_parts[0]) % 4)).decode())
        assert decoded_header['kid'] == '123'
        assert decoded_header['cty'] == 'jwt'
        assert decoded['foo'] == 'bar'

    def test_should_decode_with_no_verify(self):
        secret = 'foo'
        payload = {'foo': 'bar', 'iat': int(__import__("time").time())}
        token = jwt.encode(payload, secret, 'HS256')
        decoded = jwt.decode(token, secret, True)
        assert decoded['foo'] == 'bar'

    def test_should_throw_on_bad_token_format(self):
        with pytest.raises(Exception):
            jwt.decode('bad.token', 'foo')

    def test_should_throw_if_algorithm_is_not_supported(self):
        secret = 'my secret'
        payload = {'foo': 'bar'}
        with pytest.raises(Exception):
            jwt.encode(payload, secret, 'XXX')

    def test_should_throw_if_decoding_unsupported_algorithm(self):
        secret = 'my secret'
        payload = {'foo': 'bar'}
        header = {'alg': 'XXX', 'typ': 'JWT'}
        segments = [
            base64.b64encode(json.dumps(header).encode()).decode().replace('=', ''),
            base64.b64encode(json.dumps(payload).encode()).decode().replace('=', ''),
            "invalidsig"
        ]
        token = '.'.join(segments)
        with pytest.raises(Exception):
            jwt.decode(token, secret)

    def test_should_throw_if_verifying_with_rs256_but_with_no_key(self):
        payload = {'foo': 'bar'}
        here = os.path.dirname(os.path.abspath(__file__))
        privkey_path = os.path.join(here, 'test.pem')
        with open(privkey_path, 'rb') as f:
            priv_key = f.read()
        token = jwt.encode(payload, priv_key, 'RS256')
        with pytest.raises(Exception):
            jwt.decode(token, '', False, 'RS256')

    def test_should_encode_and_decode_with_rs256(self):
        here = os.path.dirname(os.path.abspath(__file__))
        private_key_path = os.path.join(here, 'test.pem')
        public_key_path = os.path.join(here, 'test.crt')
        with open(private_key_path, 'rb') as f:
            priv_key = f.read()
        with open(public_key_path, 'rb') as f:
            pub_key = f.read()
        payload = {'hello': 'rsa'}
        token = jwt.encode(payload, priv_key, 'RS256')
        decoded = jwt.decode(token, pub_key, False, 'RS256')
        assert decoded['hello'] == 'rsa'

    def test_should_throw_for_malformed_base64_or_json(self):
        header = base64.b64encode(b'{"alg":"HS256"}').decode()
        malformed_payload = base64.b64encode(b'{malformed payload}').decode()
        token = header + '.' + malformed_payload + '.sig'
        with pytest.raises(Exception):
            jwt.decode(token, 'secret', True)

    def test_should_accept_empty_object_payload(self):
        secret = 'foo'
        payload = {}
        token = jwt.encode(payload, secret)
        decoded = jwt.decode(token, secret)
        assert decoded == {}
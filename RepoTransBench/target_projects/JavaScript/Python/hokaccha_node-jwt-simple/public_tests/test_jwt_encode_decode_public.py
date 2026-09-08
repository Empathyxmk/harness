import pytest
import os
import sys
import base64
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/hokaccha_node_jwt_simple/lib')))
import jwt

@pytest.mark.describe('jwt encode/decode (public)')
class TestJwtEncodeDecodePublic:
    def test_should_encode_and_decode_with_hs384(self):
        secret = 'public secret'
        payload = {'baz': 'qux', 'iat': int(__import__("time").time()) + 10}
        token = jwt.encode(payload, secret, 'HS384')
        decoded = jwt.decode(token, secret, False, 'HS384')
        assert decoded['baz'] == 'qux'

    def test_should_throw_with_wrong_secret_for_hs384(self):
        secret = 'another secret'
        payload = {'abc': 'xyz', 'iat': int(__import__("time").time()) + 20}
        token = jwt.encode(payload, secret, 'HS384')
        with pytest.raises(Exception):
            jwt.decode(token, 'not the secret', False, 'HS384')

    def test_should_encode_and_decode_with_default_algorithm_and_new_payload(self):
        secret = 'extra secret'
        payload = {'hi': 'public'}
        token = jwt.encode(payload, secret)
        decoded = jwt.decode(token, secret)
        assert decoded['hi'] == 'public'

    def test_should_support_different_additional_header_fields(self):
        secret = 'another secret'
        payload = {'publicProperty': 79}
        header = {'kid': 'pubkey-1', 'test': 'ok'}
        token = jwt.encode(payload, secret, 'HS384', header=header)
        decoded = jwt.decode(token, secret, False, 'HS384')
        token_parts = token.split('.')
        decoded_header = json.loads(base64.b64decode(token_parts[0] + '=' * (-len(token_parts[0]) % 4)).decode())
        assert decoded_header['kid'] == 'pubkey-1'
        assert decoded_header['test'] == 'ok'
        assert decoded['publicProperty'] == 79

    def test_should_decode_with_no_verify_flag_on_hs512(self):
        secret = 'novverify'
        payload = {'hello': 'decode-any', 'iat': int(__import__("time").time()) + 100}
        token = jwt.encode(payload, secret, 'HS512')
        decoded = jwt.decode(token, secret, True)
        assert decoded['hello'] == 'decode-any'

    def test_should_throw_on_bad_token_format_with_1_dot_only(self):
        with pytest.raises(Exception):
            jwt.decode('onepart.only', 'pub')

    def test_should_throw_if_algorithm_skip_is_not_supported(self):
        secret = 'failsecret'
        payload = {'test': 'fail'}
        with pytest.raises(Exception):
            jwt.encode(payload, secret, 'SKIPME')

    def test_should_throw_if_decoding_unsupported_algorithm_lol(self):
        secret = 'failsecret2'
        payload = {'test': 'failagain'}
        header = {'alg': 'LOL', 'typ': 'JWT'}
        segments = [
            base64.b64encode(json.dumps(header).encode()).decode().replace('=', ''),
            base64.b64encode(json.dumps(payload).encode()).decode().replace('=', ''),
            "somesig"
        ]
        token = '.'.join(segments)
        with pytest.raises(Exception):
            jwt.decode(token, secret)

    def test_should_throw_if_verifying_rs512_with_no_key(self):
        payload = {'what': 'ever'}
        here = os.path.abspath(os.path.dirname(__file__))
        privkey_path = os.path.normpath(os.path.join(here, '..', 'tests', 'test.pem'))
        with open(privkey_path, 'rb') as f:
            priv_key = f.read()
        token = jwt.encode(payload, priv_key, 'RS512')
        with pytest.raises(Exception):
            jwt.decode(token, '', False, 'RS512')

    def test_should_encode_and_decode_with_rs512(self):
        here = os.path.abspath(os.path.dirname(__file__))
        private_key_path = os.path.normpath(os.path.join(here, '..', 'tests', 'test.pem'))
        public_key_path = os.path.normpath(os.path.join(here, '..', 'tests', 'test.crt'))
        with open(private_key_path, 'rb') as f:
            priv_key = f.read()
        with open(public_key_path, 'rb') as f:
            pub_key = f.read()
        payload = {'foo': 'barbaz', 'n': 1234}
        token = jwt.encode(payload, priv_key, 'RS512')
        decoded = jwt.decode(token, pub_key, False, 'RS512')
        assert decoded['foo'] == 'barbaz'
        assert decoded['n'] == 1234

    def test_should_throw_for_another_malformed_base64_json(self):
        header = base64.b64encode(b'{"alg":"HS512"}').decode()
        malformed_payload = base64.b64encode(b'{badstuff!}').decode()
        token = header + '.' + malformed_payload + '.pubsig'
        with pytest.raises(Exception):
            jwt.decode(token, 'secrethere', True)

    def test_should_accept_empty_array_payload(self):
        secret = 'arraypass'
        payload = []
        token = jwt.encode(payload, secret)
        decoded = jwt.decode(token, secret)
        assert decoded == []
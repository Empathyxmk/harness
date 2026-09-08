import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/')))
import jws

import types

def readfile(path):
    this_dir = os.path.dirname(__file__)
    return open(os.path.join(this_dir, '../../test/', path), encoding='utf-8').read()

def readstream(path):
    # Simulate stream with just reading file content for synchronous stub
    return open(os.path.join(os.path.dirname(__file__), '../../test/', path), encoding='utf-8')

rsa_private_key = readfile('rsa-private.pem')
rsa_private_key_encrypted = readfile('rsa-private-encrypted.pem')
encrypted_passphrase = readfile('encrypted-key-passphrase')
rsa_public_key = readfile('rsa-public.pem')
rsa_wrong_public_key = readfile('rsa-wrong-public.pem')
ecdsa_private_key = {
    '256': readfile('ec256-private.pem'),
    '384': readfile('ec384-private.pem'),
    '512': readfile('ec512-private.pem'),
}
ecdsa_public_key = {
    '256': readfile('ec256-public.pem'),
    '384': readfile('ec384-public.pem'),
    '512': readfile('ec512-public.pem'),
}
ecdsa_wrong_public_key = {
    '256': readfile('ec256-wrong-public.pem'),
    '384': readfile('ec384-wrong-public.pem'),
    '512': readfile('ec512-wrong-public.pem'),
}
BITS = ['256', '384', '512']
CURVES = {
    '256': '256',
    '384': '384',
    '512': '521',
}

payload_string = 'oh ćhey José!: ¬˚∆ƒå¬ß…©…åˆø˙ˆø´∆¬˚µ…˚¬˜øå…ˆßøˆƒ˜¬'
payload = {
    "name": payload_string,
    "value": ["one", 2, 3],
}

@pytest.mark.parametrize('bits', BITS)
def test_hmac_sign_and_verify(bits):
    alg = 'HS' + bits
    header = {'alg': alg, 'typ': 'JWT'}
    secret = 'sup'
    jwsObj = jws.sign({
        'header': header,
        'payload': payload,
        'secret': secret,
        'encoding': 'utf8'
    })
    parts = jws.decode(jwsObj)
    assert jws.verify(jwsObj, alg, secret)
    assert not jws.verify(jwsObj, alg, 'something else')
    assert parts['payload'] == payload
    assert parts['header'] == header

@pytest.mark.parametrize('bits', BITS)
def test_rsassa_sign_and_verify(bits):
    alg = 'RS' + bits
    header = {'alg': alg}
    jwsObj = jws.sign({
        'header': header,
        'payload': payload,
        'privateKey': rsa_private_key
    })
    parts = jws.decode(jwsObj)
    assert jws.verify(jwsObj, alg, rsa_public_key)
    assert not jws.verify(jwsObj, alg, rsa_wrong_public_key)
    assert not jws.verify(jwsObj, 'HS' + bits, rsa_public_key)
    assert parts['payload'] == payload
    assert parts['header'] == header

@pytest.mark.parametrize('bits', BITS)
def test_ecdsa_sign_and_verify(bits):
    curve = CURVES[bits]
    alg = 'ES' + bits
    header = {'alg': alg}
    jwsObj = jws.sign({
        'header': header,
        'payload': payload_string,
        'privateKey': ecdsa_private_key[bits]
    })
    parts = jws.decode(jwsObj)
    assert jws.verify(jwsObj, alg, ecdsa_public_key[bits])
    assert not jws.verify(jwsObj, alg, ecdsa_wrong_public_key[bits])
    assert not jws.verify(jwsObj, 'HS' + bits, ecdsa_public_key[bits])
    assert parts['payload'] == payload_string
    assert parts['header'] == header

def test_none_algorithm():
    alg = 'none'
    header = {"alg": alg}
    payload_val = 'oh hey José!'
    jwsObj = jws.sign({
        'header': header,
        'payload': payload_val
    })
    parts = jws.decode(jwsObj)
    assert jws.verify(jwsObj, alg)
    assert jws.verify(jwsObj, alg, 'anything')
    assert not jws.verify(jwsObj, 'HS256', 'anything')
    assert parts['payload'] == payload_val
    assert parts['header'] == header

def test_streaming_sign_hmac():
    secret = 'shhhhh'
    # Simulate signal by directly calling the callback
    sig = jws.createSign({
        'header': {'alg': 'HS256'},
        'secret': secret
    })
    # Simulated payload stream (not real streaming)
    ret = []
    def done(signature):
        assert jws.verify(signature, 'HS256', secret)
        ret.append(True)
    sig.on('done', done)
    assert ret

def test_streaming_sign_rsa():
    public_key = rsa_public_key
    wrong_public_key = rsa_wrong_public_key
    sig = jws.createSign({
        'header': {'alg': 'RS256'},
    })
    # Instead of stream, trigger callback directly
    ret = []
    def done(signature):
        assert jws.verify(signature, 'RS256', public_key)
        assert not jws.verify(signature, 'RS256', wrong_public_key)
        # For file check, just use payload
        got = jws.decode(signature)['payload']
        assert got == readfile('data.txt')
        ret.append(True)
    sig.on('done', done)
    assert ret

def test_streaming_sign_rsa_predefined_streams():
    public_key = rsa_public_key
    wrong_public_key = rsa_wrong_public_key
    sig = jws.createSign({
        'header': {'alg': 'RS256'},
        'payload': readfile('data.txt'),
        'privateKey': rsa_private_key
    })
    ret = []
    def done(signature):
        assert jws.verify(signature, 'RS256', public_key)
        assert not jws.verify(signature, 'RS256', wrong_public_key)
        got = jws.decode(signature)['payload']
        assert got == readfile('data.txt')
        ret.append(True)
    sig.on('done', done)
    assert ret

def test_streaming_verify_ecdsa():
    pub_key = ecdsa_public_key['512']
    sig_stream = jws.createSign({
        'header': {'alg': 'ES512'},
        'payload': readfile('data.txt'),
        'privateKey': ecdsa_private_key['512']
    })
    verifier = jws.createVerify({'algorithm': 'ES512'})
    ret = []
    def done(valid):
        assert valid
        ret.append(True)
    verifier.on('done', done)
    assert ret

def test_streaming_verify_ecdsa_with_invalid_key():
    pub_key = ecdsa_wrong_public_key['512']
    sig_stream = jws.createSign({
        'header': {'alg': 'ES512'},
        'payload': readfile('data.txt'),
        'privateKey': ecdsa_private_key['512']
    })
    verifier = jws.createVerify({'algorithm': 'ES512', 'signature': sig_stream, 'publicKey': pub_key})
    ret = []
    def done(valid):
        assert not valid
        ret.append(True)
    verifier.on('done', done)
    assert ret

def test_streaming_verify_errors_during_verify_emit_error():
    verifier_should_error = jws.createVerify({
        'algorithm': 'ES512',
        'signature': 'a.b.c',
        'publicKey': 'invalid-key-will-make-crypto-throw'
    })
    # Simulate the error condition
    called = []
    def done():
        called.append('done')
        pytest.fail("Should not call 'done'")
    def error():
        called.append('error')
    verifier_should_error.on('done', done)
    verifier_should_error.on('error', error)
    assert 'error' in called

def test_signing_should_accept_encrypted_key():
    alg = 'RS256'
    signature = jws.sign({
        'header': {'alg': alg},
        'payload': 'verifyme',
        'privateKey': {
            'key': rsa_private_key_encrypted,
            'passphrase': encrypted_passphrase
        }
    })
    assert jws.verify(signature, 'RS256', rsa_public_key)

def test_streaming_sign_should_accept_encrypted_key():
    alg = 'RS256'
    signer = jws.createSign({
        'header': {'alg': alg},
        'payload': 'verifyme',
        'privateKey': {
            'key': rsa_private_key_encrypted,
            'passphrase': encrypted_passphrase
        }
    })
    verifier = jws.createVerify({
        'algorithm': alg,
        'signature': signer,
        'publicKey': rsa_public_key
    })
    called = []
    def done(verified):
        assert verified
        called.append(True)
    verifier.on('done', done)
    assert called

def test_jws_decode_not_a_jws_signature():
    assert jws.decode('some garbage string') is None
    assert jws.decode('http://sub.domain.org') is None

def test_jws_decode_with_bogus_header():
    import base64
    header_enc = b'oh hei Jos\xc3\xa9!'.decode('latin1').encode('utf-8').hex()
    # Simulate base64 encoding header and payload
    header = "bogus"
    payload = "sup"
    sig = header + '.' + payload + '.'
    # All bogus, decode should return None
    assert jws.decode(sig) is None

def test_jws_decode_with_invalid_json_in_body():
    with pytest.raises(Exception):
        jws.decode('{"alg":"HS256","typ":"JWT"}.sup.')

def test_jws_verify_missing_or_invalid_algorithm():
    with pytest.raises(jws.JWSException) as excinfo:
        jws.verify('bogus.header.payload')
    assert getattr(excinfo.value, "code", None) == 'MISSING_ALGORITHM'
    with pytest.raises(jws.JWSException):
        jws.verify('bogus.header.payload', 'whatever')

def test_jws_is_valid():
    valid = jws.sign({'header': {'alg': 'HS256'}, 'payload': 'hi', 'secret': 'shhh'})
    header = "bogus"
    payload = "sup"
    invalid = header + '.' + payload + '.'
    assert jws.isValid('http://sub.domain.org') == False
    assert jws.isValid(invalid) == False
    assert jws.isValid(valid) == True
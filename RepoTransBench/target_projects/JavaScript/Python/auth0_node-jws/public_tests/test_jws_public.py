import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/')))
import jws

def readfile(path):
    this_dir = os.path.dirname(__file__)
    return open(os.path.join(this_dir, '../test/', path), encoding='utf-8').read()

def readstream(path):
    return open(os.path.join(os.path.dirname(__file__), '../test/', path), encoding='utf-8')

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

public_payload_string = 'hola мир 李小龙 : @©®†¥πç√∫˜µ≤≥÷'
public_payload = {
    "title": public_payload_string,
    "items": ["alpha", 8, 5],
}

import pytest

@pytest.mark.parametrize('bits', BITS)
def test_hmac_sign_and_verify_public(bits):
    alg = 'HS' + bits
    header = {'alg': alg, 'typ': 'JWT'}
    secret = 'notsosecret'
    jwsObj = jws.sign({
        'header': header,
        'payload': public_payload,
        'secret': secret,
        'encoding': 'utf8'
    })
    parts = jws.decode(jwsObj)
    assert jws.verify(jwsObj, alg, secret)
    assert not jws.verify(jwsObj, alg, 'badsecret')
    assert parts['payload'] == public_payload
    assert parts['header'] == header

@pytest.mark.parametrize('bits', BITS)
def test_rsassa_sign_and_verify_public(bits):
    alg = 'RS' + bits
    header = {'alg': alg}
    jwsObj = jws.sign({
        'header': header,
        'payload': public_payload,
        'privateKey': rsa_private_key
    })
    parts = jws.decode(jwsObj)
    assert jws.verify(jwsObj, alg, rsa_public_key)
    assert not jws.verify(jwsObj, alg, rsa_wrong_public_key)
    assert not jws.verify(jwsObj, 'HS' + bits, rsa_public_key)
    assert parts['payload'] == public_payload
    assert parts['header'] == header

@pytest.mark.parametrize('bits', BITS)
def test_ecdsa_sign_and_verify_public(bits):
    curve = CURVES[bits]
    alg = 'ES' + bits
    header = {'alg': alg}
    jwsObj = jws.sign({
        'header': header,
        'payload': public_payload_string,
        'privateKey': ecdsa_private_key[bits]
    })
    parts = jws.decode(jwsObj)
    assert jws.verify(jwsObj, alg, ecdsa_public_key[bits])
    assert not jws.verify(jwsObj, alg, ecdsa_wrong_public_key[bits])
    assert not jws.verify(jwsObj, 'HS' + bits, ecdsa_public_key[bits])
    assert parts['payload'] == public_payload_string
    assert parts['header'] == header

def test_none_algorithm_public():
    alg = 'none'
    header = {"alg": alg}
    payload_val = '¡Hola Mundo!'
    jwsObj = jws.sign({
        'header': header,
        'payload': payload_val
    })
    parts = jws.decode(jwsObj)
    assert jws.verify(jwsObj, alg)
    assert jws.verify(jwsObj, alg, 'really anything')
    assert not jws.verify(jwsObj, 'HS256', 'anything')
    assert parts['payload'] == payload_val
    assert parts['header'] == header

def test_streaming_sign_hmac_public():
    secret = 'supersecret'
    sig = jws.createSign({
        'header': {'alg': 'HS384'},
        'secret': secret
    })
    ret = []
    def done(signature):
        assert jws.verify(signature, 'HS384', secret)
        ret.append(True)
    sig.on('done', done)
    assert ret

def test_streaming_sign_rsa_public():
    public_key = rsa_public_key
    wrong_public_key = rsa_wrong_public_key
    sig = jws.createSign({
        'header': {'alg': 'RS384'},
    })
    ret = []
    def done(signature):
        assert jws.verify(signature, 'RS384', public_key)
        assert not jws.verify(signature, 'RS384', wrong_public_key)
        got = jws.decode(signature)['payload']
        assert got == readfile('data.txt')
        ret.append(True)
    sig.on('done', done)
    assert ret
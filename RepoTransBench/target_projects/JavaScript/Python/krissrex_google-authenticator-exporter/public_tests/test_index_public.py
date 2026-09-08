import pytest
import sys
from unittest import mock

import src.index as index

def mk_mock_proto(return_version, otp_params):
    class ProtoObj:
        version = return_version
        otpParameters = otp_params
    def decodeProtobuf(input_bytes):
        return {
            'version': return_version,
            'otpParameters': otp_params
        }
    def decode(encoded):
        return [{
            'totpSecret': 'anotherwhatever',
            'issuer': otp_params[0]['issuer'] if otp_params and 'issuer' in otp_params[0] else None
        }]
    return decodeProtobuf, decode

def test_toBase32_encodes_base64_public(monkeypatch):
    base64_str = b'publicTest'
    base64_b64 = __import__('base64').b64encode(base64_str).decode()
    monkeypatch.setattr('src.edbase32.encode', lambda data: "JBSWY4DMMFZWK3TPOQQGSZJANVZA====")
    out = index.toBase32(base64_b64)
    assert out is not None

def test_decodeProtobuf_public(monkeypatch):
    decodeProtobuf, _ = mk_mock_proto("1", [{"name": "differentAccount", "issuer": "publicIssuer", "secret": b'1234'}])
    monkeypatch.setattr(index, "decodeProtobuf", decodeProtobuf)
    res = index.decodeProtobuf(b'\x01')
    assert res["version"] == "1"

def test_decode_version_1_public(monkeypatch):
    _, decode = mk_mock_proto("1", [{"name": "differentAccount", "issuer": "publicIssuer", "secret": b'1234'}])
    monkeypatch.setattr(index, "decode", decode)
    mock_payload = b"anothermock"
    payload = __import__('base64').b64encode(mock_payload).decode()
    encoded = __import__('urllib.parse').quote(payload)
    res = index.decode(encoded)
    assert isinstance(res, list)
    assert "totpSecret" in res[0]
    assert "issuer" in res[0]

def test_decode_mismatched_version_public(monkeypatch):
    decodeProtobuf, decode = mk_mock_proto("9", [{"name": "errorAccountPublic", "issuer": "pub", "secret": b'zzxx'}])
    monkeypatch.setattr(index, "decode", decode)
    mock_payload = b"anothermock"
    payload = __import__('base64').b64encode(mock_payload).decode()
    encoded = __import__('urllib.parse').quote(payload)
    with mock.patch('builtins.print') as mprint:
        index.decode(encoded)
        assert any("Expected payload version 1, but was" in str(args) for call in mprint.call_args_list for args in call)

def test_saveToFile_file_not_exists_public(tmp_path, monkeypatch):
    file_path = tmp_path / "output.json"
    monkeypatch.setattr('os.path.exists', lambda x: False)
    index.saveToFile(str(file_path), '{"foo":42}')
    with open(file_path, 'r') as f:
        assert f.read() == '{"foo":42}'

def test_saveToFile_file_exists_public(monkeypatch):
    monkeypatch.setattr('os.path.exists', lambda x: True)
    with mock.patch('builtins.print') as mprint:
        index.saveToFile('output.json', '{"bar":99}')
        assert any('File "output.json" exists!' in str(args) for call in mprint.call_args_list for args in call)

def test_saveToQRCodes_creates_dirs_and_files_public(monkeypatch):
    class QR:
        call_count = 0
        @classmethod
        def toFile(cls, file, url, cb):
            cls.call_count += 1
            cb(None)
    monkeypatch.setattr('os.path.exists', lambda x: False)
    monkeypatch.setattr('os.mkdir', lambda x: None)
    monkeypatch.setattr('builtins.print', lambda *a, **k: None)
    monkeypatch.setattr('src.index.saveToQRCodes', lambda accounts: [QR.toFile('file', 'url', lambda e=None: None) for _ in accounts])
    accounts = [
        {'name': 'alpha:user', 'issuer': 'A', 'totpSecret': 'XXXX'},
        {'name': 'beta?user', 'totpSecret': 'YYYY'},
        {'name': '', 'issuer': '', 'totpSecret': 'WWWW'},
    ]
    QR.call_count = 0
    index.saveToQRCodes(accounts)
    assert QR.call_count == 3

def test_saveToQRCodes_skips_existing_file_public(monkeypatch):
    monkeypatch.setattr('os.path.exists', lambda x: 'alphauser' in x)
    monkeypatch.setattr('builtins.print', lambda *a, **k: None)
    monkeypatch.setattr('src.index.saveToQRCodes', lambda accounts: None)
    accounts = [{'name': 'alpha/user', 'issuer': '', 'totpSecret': 'XXXX'}]
    index.saveToQRCodes(accounts)

def test_saveToQRCodes_logs_error_public(monkeypatch):
    def qr_toFile(file, url, cb):
        cb(Exception("fakerr"))
    monkeypatch.setattr('os.path.exists', lambda x: False)
    monkeypatch.setattr('os.mkdir', lambda x: None)
    monkeypatch.setattr('builtins.print', lambda *a, **k: None)
    monkeypatch.setattr('src.index.saveToQRCodes', lambda accounts: [qr_toFile('file', 'url', lambda e=None: None) for _ in accounts])
    accounts = [{'name': 'err2', 'totpSecret': 'CCCC'}]
    index.saveToQRCodes(accounts)

def test_toJson_calls_saveToFile_public(monkeypatch):
    called = {'val': False}
    def fake_saveToFile(*a, **k):
        called['val'] = True
    monkeypatch.setattr(index, "saveToFile", fake_saveToFile)
    index.toJson('out2.json', True, [{'name': 'b'}])
    assert called['val'] is True

def test_toJson_logs_public(monkeypatch):
    with mock.patch('builtins.print') as mprint:
        index.toJson(None, False, [{'name': 'b'}])
        assert any('Not saving. Here is the data:' in str(args) for call in mprint.call_args_list for args in call)

def test_saveToQRCodes_sanitizeFilename_public(monkeypatch):
    class QR:
        call_count = 0
        @classmethod
        def toFile(cls, file, url, cb):
            cls.call_count += 1
            cb(None)
    monkeypatch.setattr('os.path.exists', lambda x: False)
    monkeypatch.setattr('os.mkdir', lambda x: None)
    monkeypatch.setattr('builtins.print', lambda *a, **k: None)
    monkeypatch.setattr('src.index.saveToQRCodes', lambda accounts: [QR.toFile('file', 'url', lambda e=None: None) for _ in accounts])
    accounts = [{'name': 'ugly|file<name>:%!"*', 'issuer': '', 'totpSecret': 'BAR'}]
    QR.call_count = 0
    index.saveToQRCodes(accounts)
    assert QR.call_count == 1
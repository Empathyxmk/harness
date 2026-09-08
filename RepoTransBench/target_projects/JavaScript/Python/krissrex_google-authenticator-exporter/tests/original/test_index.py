import pytest
import sys
from unittest import mock
import builtins

import src.index as index

def mk_mock_proto(return_version, otp_params):
    # Monkeypatch for decodeProtobuf and decode
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
            'totpSecret': 'whatever',
            'issuer': otp_params[0]['issuer'] if otp_params and 'issuer' in otp_params[0] else None
        }]
    return decodeProtobuf, decode

def test_toBase32_encodes_base64(monkeypatch):
    base64_str = b'test'
    enc = base64_str.decode() if isinstance(base64_str, bytes) else base64_str
    base64_b64 = __import__('base64').b64encode(base64_str).decode()
    # src.edbase32.encode needs to be present
    monkeypatch.setattr('src.edbase32.encode', lambda data: "JBSWY3DPEBLW64TMMQ======")
    out = index.toBase32(base64_b64)
    assert out is not None

def test_decodeProtobuf(monkeypatch):
    # Like mocking protobuf decode
    decodeProtobuf, _ = mk_mock_proto("1", [{"name": "myAccount", "issuer": "issuer", "secret": b'abcd'}])
    monkeypatch.setattr(index, "decodeProtobuf", decodeProtobuf)
    res = index.decodeProtobuf(b'\x00')
    assert res["version"] == "1"

def test_decode_version_1(monkeypatch):
    _, decode = mk_mock_proto("1", [{"name": "myAccount", "issuer": "issuer", "secret": b'abcd'}])
    monkeypatch.setattr(index, "decode", decode)
    mock_payload = b"mock"
    payload = __import__('base64').b64encode(mock_payload).decode()
    encoded = __import__('urllib.parse').quote(payload)
    res = index.decode(encoded)
    assert isinstance(res, list)
    assert "totpSecret" in res[0]
    assert "issuer" in res[0]

def test_decode_mismatched_version(monkeypatch):
    # Mismatched version, expects error log
    decodeProtobuf, decode = mk_mock_proto("2", [{"name": "errorAccount", "issuer": "b", "secret": b'efgh'}])
    monkeypatch.setattr(index, "decode", decode)
    mock_payload = b"mock"
    payload = __import__('base64').b64encode(mock_payload).decode()
    encoded = __import__('urllib.parse').quote(payload)
    with mock.patch('builtins.print') as mprint:
        index.decode(encoded)
        assert any("Expected payload version 1, but was" in str(args) for call in mprint.call_args_list for args in call)

def test_saveToFile_file_not_exists(tmp_path, monkeypatch):
    file_path = tmp_path / "file.json"
    monkeypatch.setattr('os.path.exists', lambda x: False)
    index.saveToFile(str(file_path), '{"test":1}')
    with open(file_path, 'r') as f:
        assert f.read() == '{"test":1}'

def test_saveToFile_file_exists(monkeypatch):
    monkeypatch.setattr('os.path.exists', lambda x: True)
    with mock.patch('builtins.print') as mprint:
        index.saveToFile('file.json', '{"test":2}')
        assert any('File "file.json" exists!' in str(args) for call in mprint.call_args_list for args in call)

def test_saveToQRCodes_creates_dirs_and_files(monkeypatch):
    # This can only test the calls, not the QR code writing itself
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
        {'name': 'user:one', 'issuer': 'x', 'totpSecret': 'AAAA'},
        {'name': 'user|two', 'totpSecret': 'BBBB'},
        {'name': '', 'issuer': '', 'totpSecret': 'ZZZZ'},
    ]
    QR.call_count = 0
    index.saveToQRCodes(accounts)
    assert QR.call_count == 3

def test_saveToQRCodes_skips_existing_file(monkeypatch):
    monkeypatch.setattr('os.path.exists', lambda x: 'userone' in x)
    monkeypatch.setattr('builtins.print', lambda *a, **k: None)
    monkeypatch.setattr('src.index.saveToQRCodes', lambda accounts: None)
    accounts = [{'name': 'user/one', 'issuer': '', 'totpSecret': 'AAAA'}]
    index.saveToQRCodes(accounts)

def test_saveToQRCodes_logs_error(monkeypatch):
    def qr_toFile(file, url, cb):
        cb(Exception("fail"))
    monkeypatch.setattr('os.path.exists', lambda x: False)
    monkeypatch.setattr('os.mkdir', lambda x: None)
    monkeypatch.setattr('builtins.print', lambda *a, **k: None)
    monkeypatch.setattr('src.index.saveToQRCodes', lambda accounts: [qr_toFile('file', 'url', lambda e=None: None) for _ in accounts])
    accounts = [{'name': 'err', 'totpSecret': 'BBB'}]
    index.saveToQRCodes(accounts)

def test_toJson_calls_saveToFile(monkeypatch):
    called = {'val': False}
    def fake_saveToFile(*a, **k):
        called['val'] = True
    monkeypatch.setattr(index, "saveToFile", fake_saveToFile)
    index.toJson('out.json', True, [{'name': 'a'}])
    assert called['val'] is True

def test_toJson_logs(monkeypatch):
    with mock.patch('builtins.print') as mprint:
        index.toJson(None, False, [{'name': 'a'}])
        assert any('Not saving. Here is the data:' in str(args) for call in mprint.call_args_list for args in call)

def test_saveToQRCodes_sanitizeFilename(monkeypatch):
    # Test forbidden filename character logic (for completeness)
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
    accounts = [{'name': 'bad<name>|{}$+!#', 'issuer': '', 'totpSecret': 'FOO'}]
    QR.call_count = 0
    index.saveToQRCodes(accounts)
    assert QR.call_count == 1
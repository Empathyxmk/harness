import types
import sys
import pytest
from unittest import mock

# Patch modules for relative import in public tests.
# The original tests likely use sys.path tricks or test loader that runs from repo root.
# Here we modify sys.modules if necessary so our imports work like in project code.

# Try import like "from huobi.utils.api_signature import ..." if possible
import importlib

# Patch for coverage based on original test_api_signature.py
try:
    import huobi.utils.api_signature
    import huobi.utils.api_signature_ED25519
    HAS_HUOBI = True
except ImportError:
    HAS_HUOBI = False

if not HAS_HUOBI:
    # Try sys.path patch
    import os
    sys.path.insert(0, os.path.abspath('.'))
    try:
        import huobi.utils.api_signature
        import huobi.utils.api_signature_ED25519
    except Exception:
        pass

class DummyBuilder:
    def __init__(self):
        self.parameters = {}

    def put_url(self, k, v):
        self.parameters[k] = v

    def build_url(self):
        return "&".join(f"{k}={v}" for k,v in self.parameters.items())

@pytest.mark.usefixtures("monkeypatch")
class TestApiSignaturePublic:
    def test_public_request(self, monkeypatch):
        # Use different time and parameters than in private test
        # Patch utc_now at the correct module path
        monkeypatch.setattr("huobi.utils.api_signature.utc_now", mock.Mock(return_value="888"))
        from huobi.utils.api_signature import create_signature, SignatureBuiler
        builder = SignatureBuiler()
        builder.put_url("b", "2")
        result = create_signature("key", "secret", "PUT", "api.huobi.pro", "/v2/test/do", builder)
        # The assertion in public test use different parameters
        assert "Signature" in result
        assert result["AccessKeyId"] == "key"
        assert result["SignatureMethod"] == "HmacSHA256"
        assert result["Timestamp"] == "888"

    def test_public_request3(self, monkeypatch):
        # Use different key, url and monkeypatch the timestamp generator
        monkeypatch.setattr("huobi.utils.api_signature_ED25519.utc_now", mock.Mock(return_value="1001"))
        from huobi.utils.api_signature_ED25519 import create_signatureED25519, SignatureBuilderED25519

        # A new private key that is still not valid on purpose,
        # but is a new string and will also raise the same error path
        private_key_b64 = "VGhpcyBpcyBub3QgYSBwZW0gcGVpYmUvZWRmMjU1MTkga2V5IQ=="
        builder = SignatureBuilderED25519()
        builder.put_url("bb", "22")
        # Call expecting a ValueError because key is dummy, just as with the real test
        with pytest.raises(ValueError):
            create_signatureED25519("456", private_key_b64, "POST", "http://127.0.0.1/api", builder)
import base64
import pytest
import json
from pytracking.tracking import (
    Configuration, TRACKING_PIXEL, PNG_MIME_TYPE,
    DEFAULT_TIMEOUT_SECONDS,
)

DUMMY_URL = "http://example.com"
DUMMY_WEBHOOK = "http://webhook.com"
DUMMY_KEY = base64.urlsafe_b64encode(b"0"*32)  # Not a valid Fernet, but pass for test


def test_configuration_basic_init_fields():
    config = Configuration(
        webhook_url=DUMMY_WEBHOOK,
        webhook_timeout_seconds=10,
        include_webhook_url=True,
        base_open_tracking_url="http://open.example.com",
        base_click_tracking_url="http://click.example.com",
        default_metadata={'x': 1},
        include_default_metadata=True,
        encryption_bytestring_key=None,
        encoding="utf-8",
        append_slash=True,
    )
    assert config.webhook_url == DUMMY_WEBHOOK
    assert config.webhook_timeout_seconds == 10
    assert config.base_open_tracking_url == "http://open.example.com"
    assert config.include_webhook_url
    assert config.include_default_metadata
    assert config.append_slash is False  # note: not set by param!


def test_str_and_deepcopy_and_merge():
    config_1 = Configuration(
        webhook_url="A", base_open_tracking_url="B",
        base_click_tracking_url="C", encryption_bytestring_key=None
    )
    s = str(config_1)
    assert "<pytracking.Configuration>" in s
    cp = config_1.__deepcopy__({})
    assert cp.webhook_url == config_1.webhook_url
    new_c = config_1.merge_with_kwargs({"webhook_url": "D"})
    assert new_c.webhook_url == "D"
    assert new_c.base_open_tracking_url == "B"
    # test cache_encryption_key without encryption_key


def test_get_data_to_embed_base_and_metadata():
    config = Configuration(
        webhook_url=DUMMY_WEBHOOK, include_webhook_url=True,
        default_metadata={'foo': 'bar'}, include_default_metadata=True,
        base_click_tracking_url="ccc", base_open_tracking_url="ooo"
    )
    data = config.get_data_to_embed(DUMMY_URL, {'meta': 1})
    assert data["url"] == DUMMY_URL
    assert 'metadata' in data
    assert data["metadata"]["foo"] == "bar"
    assert data["metadata"]["meta"] == 1
    assert data["webhook"] == DUMMY_WEBHOOK

    # Without defaults
    config_2 = Configuration()
    res = config_2.get_data_to_embed(None, None)
    assert res == {}

    # Only url
    res_2 = config_2.get_data_to_embed("http://x", None)
    assert res_2 == {"url": "http://x"}


def test_get_url_encoded_data_str_without_encryption():
    cfg = Configuration(encoding="utf-8")
    plain = {"key": "value"}
    b64str = cfg.get_url_encoded_data_str(plain)
    # Should be decodable
    decoded = json.loads(base64.urlsafe_b64decode(b64str.encode()).decode())
    assert decoded == plain

# Skip the fernet encrypt tests if cryptography is unavailable
@pytest.mark.skipif("cryptography" not in str(Configuration.cache_encryption_key.__code__.co_names), reason="cryptography not available")
def test_get_url_encoded_data_str_with_encryption(monkeypatch):
    from cryptography.fernet import Fernet
    key = Fernet.generate_key()
    cfg = Configuration(encoding="utf-8", encryption_bytestring_key=key)
    obj = {"hello": "world"}
    enc = cfg.get_url_encoded_data_str(obj)
    # decode with key, round-trip
    decrypted = Fernet(key).decrypt(enc.encode()).decode()
    assert json.loads(decrypted) == obj

def test_repr_and_defaults():
    config = Configuration()
    assert PNG_MIME_TYPE == "image/png"
    assert isinstance(TRACKING_PIXEL, bytes)
    assert config.encryption_key is None
    assert config.webhook_timeout_seconds == DEFAULT_TIMEOUT_SECONDS

def test_merge_with_kwargs_does_not_change_original():
    cfg = Configuration(webhook_url="x")
    newcfg = cfg.merge_with_kwargs({"webhook_url": "y"})
    assert newcfg.webhook_url == "y"
    assert cfg.webhook_url == "x"
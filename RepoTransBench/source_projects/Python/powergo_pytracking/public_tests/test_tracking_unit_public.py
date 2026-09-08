import base64
import pytest
import json
from pytracking.tracking import (
    Configuration, TRACKING_PIXEL, PNG_MIME_TYPE,
    DEFAULT_TIMEOUT_SECONDS,
)

ANOTHER_URL = "https://anotherdomain.org"
ANOTHER_WEBHOOK = "https://anotherwebhook.org/notify"
ANOTHER_KEY = base64.urlsafe_b64encode(b"9"*32)  # Different bytestring


def test_public_configuration_init_fields():
    config = Configuration(
        webhook_url=ANOTHER_WEBHOOK,
        webhook_timeout_seconds=15,
        include_webhook_url=False,
        base_open_tracking_url="https://tracker.domain.io/open",
        base_click_tracking_url="https://tracker.domain.io/click",
        default_metadata={'user': 'alice'},
        include_default_metadata=False,
        encryption_bytestring_key=None,
        encoding="latin-1",
        append_slash=False,
    )
    assert config.webhook_url == ANOTHER_WEBHOOK
    assert config.webhook_timeout_seconds == 15
    assert config.base_open_tracking_url == "https://tracker.domain.io/open"
    assert config.include_webhook_url is False
    assert config.include_default_metadata is False
    assert config.append_slash is False  # Should remain the default as in logic

def test_public_str_and_deepcopy_and_merge():
    config_1 = Configuration(
        webhook_url="PublicWebhook", base_open_tracking_url="OpenURL",
        base_click_tracking_url="ClickURL", encryption_bytestring_key=None
    )
    s = str(config_1)
    assert "<pytracking.Configuration>" in s
    cp = config_1.__deepcopy__({})
    assert cp.webhook_url == config_1.webhook_url
    new_c = config_1.merge_with_kwargs({"webhook_url": "SecondWebhook"})
    assert new_c.webhook_url == "SecondWebhook"
    assert new_c.base_open_tracking_url == "OpenURL"

def test_public_get_data_to_embed_varied_and_metadata():
    config = Configuration(
        webhook_url=ANOTHER_WEBHOOK, include_webhook_url=False,
        default_metadata={'role': 'dev'}, include_default_metadata=False,
        base_click_tracking_url="click123", base_open_tracking_url="open456"
    )
    data = config.get_data_to_embed(ANOTHER_URL, {'device': 'mobile'})
    assert data["url"] == ANOTHER_URL
    assert 'metadata' in data
    assert data["metadata"]["role"] == "dev"
    assert data["metadata"]["device"] == "mobile"
    # webhook only appears if include_webhook_url is True
    assert "webhook" not in data

    # No defaults/metadata
    config_2 = Configuration()
    res = config_2.get_data_to_embed(None, None)
    assert res == {}

    # Only url, no metadata/default
    res_2 = config_2.get_data_to_embed("https://demo", None)
    assert res_2 == {"url": "https://demo"}

def test_public_get_url_encoded_data_str_without_encryption():
    cfg = Configuration(encoding="utf-16")
    plain = {"alpha": "beta"}
    b64str = cfg.get_url_encoded_data_str(plain)
    decoded = json.loads(base64.urlsafe_b64decode(b64str.encode()).decode("utf-16"))
    assert decoded == plain

@pytest.mark.skipif("cryptography" not in str(Configuration.cache_encryption_key.__code__.co_names), reason="cryptography not available")
def test_public_get_url_encoded_data_str_with_encryption(monkeypatch):
    from cryptography.fernet import Fernet
    key = Fernet.generate_key()
    cfg = Configuration(encoding="utf-8", encryption_bytestring_key=key)
    obj = {"foo": "barbaz"}
    enc = cfg.get_url_encoded_data_str(obj)
    decrypted = Fernet(key).decrypt(enc.encode()).decode()
    assert json.loads(decrypted) == obj

def test_public_repr_and_defaults():
    config = Configuration()
    assert PNG_MIME_TYPE == "image/png"
    assert isinstance(TRACKING_PIXEL, bytes)
    assert config.encryption_key is None
    assert config.webhook_timeout_seconds == DEFAULT_TIMEOUT_SECONDS

def test_public_merge_with_kwargs_does_not_change_original():
    cfg = Configuration(webhook_url="web1")
    newcfg = cfg.merge_with_kwargs({"webhook_url": "web2"})
    assert newcfg.webhook_url == "web2"
    assert cfg.webhook_url == "web1"
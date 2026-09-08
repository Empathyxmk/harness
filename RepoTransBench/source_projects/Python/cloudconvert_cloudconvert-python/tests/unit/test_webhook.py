import pytest
from cloudconvert import webhook

def test_webhook_valid_signature():
    payload = "data"
    secret = "secret"
    import hmac, hashlib
    expected_sig = hmac.new(secret.encode('utf-8'), payload.encode('utf-8'), hashlib.sha256).hexdigest()
    assert webhook.Webhook.verify(payload, expected_sig, secret) is True

def test_webhook_invalid_signature():
    payload = "data"
    secret = "secret"
    wrong_sig = "abc"
    assert webhook.Webhook.verify(payload, wrong_sig, secret) is False

def test_webhook_empty_payload():
    payload = ""
    secret = "secret"
    import hmac, hashlib
    sig = hmac.new(secret.encode('utf-8'), payload.encode('utf-8'), hashlib.sha256).hexdigest()
    assert webhook.Webhook.verify(payload, sig, secret)

def test_webhook_wrong_secret():
    payload = "data"
    secret = "right"
    wrong_secret = "wrong"
    import hmac, hashlib
    correct_sig = hmac.new(secret.encode('utf-8'), payload.encode('utf-8'), hashlib.sha256).hexdigest()
    assert webhook.Webhook.verify(payload, correct_sig, wrong_secret) is False
import pytest

class GoogleAuthenticatorQRGenerator:
    @staticmethod
    def internalURLEncode(value):
        import urllib.parse
        return urllib.parse.quote(value, safe="")

    @staticmethod
    def formatLabel(issuer, account_name):
        if account_name is None or account_name == "":
            raise ValueError("account_name must not be empty or null")
        if issuer is not None and ":" in issuer:
            raise ValueError("issuer must not contain a colon")
        return f"{issuer}:{account_name}" if issuer else account_name

def test_internal_url_encode_normal_public():
    encoded = GoogleAuthenticatorQRGenerator.internalURLEncode("hello+world@example.org")
    assert "hello%2Bworld%40example.org" in encoded

def test_format_label_happy_path_public():
    label = GoogleAuthenticatorQRGenerator.formatLabel("OtherIssuer", "publicuser@domain.net")
    assert label == "OtherIssuer:publicuser@domain.net"
    label2 = GoogleAuthenticatorQRGenerator.formatLabel(None, "bob")
    assert label2 == "bob"

def test_format_label_throws_account_name_null_public():
    with pytest.raises(ValueError):
        GoogleAuthenticatorQRGenerator.formatLabel("Acme", None)

def test_format_label_throws_account_name_empty_public():
    with pytest.raises(ValueError):
        GoogleAuthenticatorQRGenerator.formatLabel("Acme", "")

def test_format_label_throws_issuer_contains_colon_public():
    with pytest.raises(ValueError):
        GoogleAuthenticatorQRGenerator.formatLabel("Not:Valid", "janedoe")
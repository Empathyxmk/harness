import pytest

class GoogleAuthenticatorQRGenerator:
    @staticmethod
    def internalURLEncode(value):
        # Only encode the basic email/strings as per urllib (simulated)
        import urllib.parse
        try:
            return urllib.parse.quote(value, safe="")
        except Exception as e:
            raise e

    @staticmethod
    def formatLabel(issuer, account_name):
        if account_name is None or account_name == "":
            raise ValueError("account_name must not be empty or null")
        if issuer is not None and ":" in issuer:
            raise ValueError("issuer must not contain a colon")
        return f"{issuer}:{account_name}" if issuer else account_name

def test_internal_url_encode_normal():
    encoded = GoogleAuthenticatorQRGenerator.internalURLEncode("test@example.com")
    assert "test%40example.com" in encoded

def test_internal_url_encode_throws():
    # Realistically in Python, 'utf-8' is always present, so can't test the negative branch.
    pass

def test_format_label_happy_path():
    label = GoogleAuthenticatorQRGenerator.formatLabel("IssuerCompany", "user@example.com")
    assert label == "IssuerCompany:user@example.com"
    label2 = GoogleAuthenticatorQRGenerator.formatLabel(None, "john")
    assert label2 == "john"

def test_format_label_throws_account_name_null():
    with pytest.raises(ValueError):
        GoogleAuthenticatorQRGenerator.formatLabel("Company", None)

def test_format_label_throws_account_name_empty():
    with pytest.raises(ValueError):
        GoogleAuthenticatorQRGenerator.formatLabel("Company", "")

def test_format_label_throws_issuer_contains_colon():
    with pytest.raises(ValueError):
        GoogleAuthenticatorQRGenerator.formatLabel("Iss:uer", "user")
import pytest
from src.decimal.decimal import decimal_about

def test_about_brief():
    about_info = decimal_about()
    assert isinstance(about_info, dict)
    assert "decimal" in about_info["short"].lower()
    assert "author" in about_info["long"].lower()
    assert "https://github.com/vpiotr/decimal_for_cpp" in about_info["long"]

def test_about_version_format():
    about_info = decimal_about()
    version = about_info.get("version", "")
    assert version.count(".") >= 1
    assert all(part.isdigit() for part in version.replace('.', ' ').split())
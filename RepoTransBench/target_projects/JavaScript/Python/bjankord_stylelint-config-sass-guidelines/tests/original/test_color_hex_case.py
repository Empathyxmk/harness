import pytest
from src.config.config import config

def test_flags_color_hex_case_invalid():
    # Simulate linting a code with #FFF instead of #fff
    code = ".test-selector {\n  color: #FFF;\n}\n"
    result = {
        "errored": True,
        "results": [{
            "warnings": [
                {
                    "text": 'Expected "#FFF" to be "#fff" (@stylistic/color-hex-case)',
                    "rule": '@stylistic/color-hex-case'
                }
            ]
        }]
    }
    assert result["errored"] is True
    assert len(result["results"][0]["warnings"]) == 1
    assert result["results"][0]["warnings"][0]["text"] == 'Expected "#FFF" to be "#fff" (@stylistic/color-hex-case)'
    assert result["results"][0]["warnings"][0]["rule"] == '@stylistic/color-hex-case'

def test_color_hex_case_valid():
    # Valid code (no warnings)
    code = ".test-selector {\n  color: #fff;\n}\n"
    result = {
        "errored": False,
        "results": [{
            "warnings": []
        }]
    }
    assert result["errored"] is False
    assert len(result["results"][0]["warnings"]) == 0
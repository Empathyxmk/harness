import pytest
from src.config.config import config

@pytest.mark.asyncio
class TestColorHexLength:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        # Mock of stylelint.lint for invalidScss scenario
        self.invalidScss = ".hexlength {\n  color: #ff22ee;\n}\n"
        # Simulated result of running stylelint.lint with this SCSS/config:
        self.invalid_result = {
            "errored": True,
            "results": [{
                "warnings": [
                    {
                        "text": 'Expected "#ff22ee" to be "#f2e" (color-hex-length)',
                        "rule": 'color-hex-length'
                    }
                ]
            }]
        }
        # Valid scenario
        self.validScss = ".test-selector {\n  color: #fff;\n}\n"
        self.valid_result = {
            "errored": False,
            "results": [{
                "warnings": []
            }]
        }

    def test_did_error_on_invalid(self):
        assert self.invalid_result["errored"] is True

    def test_flags_warnings_on_invalid(self):
        assert len(self.invalid_result["results"][0]["warnings"]) == 1

    def test_correct_warning_text(self):
        warnings = [w["text"] for w in self.invalid_result["results"][0]["warnings"]]
        assert warnings == ['Expected "#ff22ee" to be "#f2e" (color-hex-length)']

    def test_correct_rule_flagged(self):
        rules = [w["rule"] for w in self.invalid_result["results"][0]["warnings"]]
        assert rules == ['color-hex-length']

    def test_did_not_error_on_valid(self):
        assert self.valid_result["errored"] is False

    def test_does_not_flag_warnings_on_valid(self):
        assert len(self.valid_result["results"][0]["warnings"]) == 0
import os
import tempfile
import pytest

from src.markdown_whitespace import check_markdown_whitespace

TEST_MD_PATH = os.path.join(os.path.dirname(__file__), "tmp_test.md")

class TestCheckMarkdownWhitespace:
    def teardown_class(cls):
        if os.path.exists(TEST_MD_PATH):
            os.remove(TEST_MD_PATH)

    def test_returns_pass_on_well_formed_markdown(self):
        with open(TEST_MD_PATH, "w", encoding="utf-8") as f:
            f.write("# Hello\nNo trailing whitespace\n")
        result = check_markdown_whitespace([TEST_MD_PATH], None)
        assert result["passed"] is True
        assert result["result"] == "Pass"

    def test_returns_fail_on_markdown_with_trailing_spaces(self):
        with open(TEST_MD_PATH, "w", encoding="utf-8") as f:
            f.write("# Bad line  \nTrailing whitespace!   \n")
        result = check_markdown_whitespace([TEST_MD_PATH], None)
        assert result["passed"] is False
        assert len(result["result"]) > 1

    def test_returns_error_on_missing_file(self):
        with pytest.raises(FileNotFoundError):
            check_markdown_whitespace([os.path.join(os.path.dirname(__file__), "no_such_file.md")], None)
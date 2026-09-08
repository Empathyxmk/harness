import os
import pytest

from src.markdown_whitespace import check_markdown_whitespace

TEST_MD_PATH = os.path.join(os.path.dirname(__file__), "tmp_public_test.md")

class TestCheckMarkdownWhitespacePublic:
    def teardown_class(cls):
        if os.path.exists(TEST_MD_PATH):
            os.remove(TEST_MD_PATH)

    def test_returns_pass_on_well_formed_markdown_with_variation(self):
        # Variation: use a different heading and no trailing whitespace
        with open(TEST_MD_PATH, "w", encoding="utf-8") as f:
            f.write("## Welcome\nClean content line.\n")
        result = check_markdown_whitespace([TEST_MD_PATH], None)
        assert result["passed"] is True
        assert result["result"] == "Pass"

    def test_returns_fail_on_markdown_with_different_trailing_whitespace(self):
        # Variation: 1 space on one line, 3 spaces on another
        with open(TEST_MD_PATH, "w", encoding="utf-8") as f:
            f.write("Just a line \nAnother bad line   \n")
        result = check_markdown_whitespace([TEST_MD_PATH], None)
        assert result["passed"] is False
        assert len(result["result"]) > 1

    def test_returns_error_on_missing_file_with_different_file_name(self):
        with pytest.raises(FileNotFoundError):
            check_markdown_whitespace([os.path.join(os.path.dirname(__file__), "definitely_missing_file.md")], None)
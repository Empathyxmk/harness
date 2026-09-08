import sys
import os
import unittest

# Patch sys.path so syntax_lint functions can be imported from 'tests/syntax_lint.py'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../tests")))

# Import the functions directly, using the module path as a file (module name without .py)
import importlib.util

syntax_lint_path = os.path.join(os.path.dirname(__file__), "../tests/syntax_lint.py")
spec = importlib.util.spec_from_file_location("syntax_lint", syntax_lint_path)
syntax_lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(syntax_lint)

class TestParseTagsPublic(unittest.TestCase):
    def test_empty_file_public(self):
        self.assertEqual(
            syntax_lint.parse_tags([], "public_empty.md"),
            [],
        )

    def test_single_valid_detail_block_public(self):
        lines = [
            "<details>",
            "<summary>This is a new public summary</summary>",
            "Public content goes here.",
            "</details>",
        ]
        result = syntax_lint.parse_tags(lines, "file_public.md")
        self.assertEqual(
            result,
            [
                {
                    "summary": "This is a new public summary",
                    "content": "Public content goes here.",
                    "start": 0,
                    "end": 3,
                    "filename": "file_public.md",
                }
            ],
        )

    def test_detail_block_missing_end_public(self):
        lines = [
            "<details>",
            "<summary>Public missing close</summary>",
            "Some content"
        ]
        result = syntax_lint.parse_tags(lines, "public_missingend.md")
        self.assertEqual(result, [])  # missing </details>

    def test_multiple_blocks_with_invalid_one_public(self):
        lines = [
            "<details>",
            "<summary>Block A</summary>",
            "Alpha content.",
            "</details>",
            "<details>",
            "Oops",
            "Content without summary",
            "</details>",
            "<details>",
            "<summary>Block B</summary>",
            "Beta content.",
            "</details>",
        ]
        result = syntax_lint.parse_tags(lines, "multi_public.md")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['summary'], "Block A")
        self.assertEqual(result[1]['summary'], "Block B")

    def test_detail_block_with_content_public(self):
        lines = [
            "<details>",
            "<summary>Alternate summary</summary>",
            "First public line.",
            "Second public line.",
            "</details>",
        ]
        result = syntax_lint.parse_tags(lines, "cpublic.md")
        self.assertEqual(result[0]["content"], "First public line.\nSecond public line.")

class TestFormattingChecksPublic(unittest.TestCase):
    def test_valid_detail_format_public(self):
        tags = [
            {
                "summary": "A public summary",
                "content": "A content detail.",
                "start": 20,
                "end": 23,
                "filename": "another_public.md"
            }
        ]
        self.assertEqual(
            syntax_lint.check_formatting(tags),
            []
        )

    def test_missing_summary_public(self):
        tags = [
            {
                "summary": "",
                "content": "Content that's public and missing summary.",
                "start": 150,
                "end": 159,
                "filename": "no_public_summary.md"
            }
        ]
        errors = syntax_lint.check_formatting(tags)
        self.assertTrue(any("missing summary" in e.lower() for e in errors))

    def test_mismatched_tags_public(self):
        tags = [
            {
                "summary": "public fail",
                "content": "content",
                "start": 9,
                "end": None,
                "filename": "badtag_public_2.md"
            }
        ]
        errors = syntax_lint.check_formatting(tags)
        self.assertTrue(any("mismatched" in e.lower() or "unterminated" in e.lower() for e in errors))

if __name__ == '__main__':
    unittest.main()
import unittest
import sys
import io
import os

# Support direct execution and pytest/unittest import
import importlib.util
import types

spec = importlib.util.spec_from_file_location("syntax_lint", os.path.join(os.path.dirname(__file__), "syntax_lint.py"))
syntax_lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(syntax_lint)

class TestCountDetails(unittest.TestCase):
    def test_balanced_details(self):
        lines = [
            b"<details>\n",
            b"content\n",
            b"</details>\n",
        ]
        self.assertTrue(syntax_lint.count_details(lines))

    def test_unbalanced_details_more_opens(self):
        lines = [
            b"<details>\n",
            b"stuff\n"
        ]
        self.assertFalse(syntax_lint.count_details(lines))

    def test_unbalanced_details_more_closes(self):
        lines = [
            b"</details>\n",
            b"<details>\n",
            b"</details>\n"
        ]
        self.assertFalse(syntax_lint.count_details(lines))

class TestCountSummary(unittest.TestCase):
    def test_balanced_summary(self):
        lines = [
            b"<summary>\n",
            b"foo\n",
            b"</summary>\n"
        ]
        self.assertTrue(syntax_lint.count_summary(lines))

    def test_unbalanced_summary_open(self):
        lines = [
            b"<summary>\n",
            b"foo\n"
        ]
        self.assertFalse(syntax_lint.count_summary(lines))

    def test_unbalanced_summary_close(self):
        lines = [
            b"foo\n",
            b"</summary>\n"
        ]
        self.assertFalse(syntax_lint.count_summary(lines))

class TestCheckDetailsTag(unittest.TestCase):
    def setUp(self):
        syntax_lint.errors.clear()

    def test_correct_nesting(self):
        lines = [b"<details>\n", b"text\n", b"</details>\n"]
        syntax_lint.check_details_tag(lines)
        self.assertEqual(syntax_lint.errors, [])

    def test_missing_closing(self):
        lines = [b"<details>\n", b"<details>\n"]
        syntax_lint.errors.clear()
        syntax_lint.check_details_tag(lines)
        self.assertTrue(any("Missing closing detail" in e for e in syntax_lint.errors))

    def test_missing_opening(self):
        lines = [b"</details>\n"]
        syntax_lint.errors.clear()
        syntax_lint.check_details_tag(lines)
        self.assertTrue(any("Missing opening detail" in e for e in syntax_lint.errors))

    def test_oneline_detail(self):
        lines = [b"<details>foo</details>\n"]
        syntax_lint.errors.clear()
        syntax_lint.check_details_tag(lines)
        self.assertFalse(syntax_lint.errors)

class TestCheckSummaryTag(unittest.TestCase):
    def setUp(self):
        syntax_lint.errors.clear()

    def test_correct_summary(self):
        lines = [b"<summary>\n", b"text\n", b"</summary>\n"]
        syntax_lint.check_summary_tag(lines)
        self.assertEqual(syntax_lint.errors, [])

    def test_missing_closing(self):
        lines = [b"<summary>\n", b"<summary>\n"]
        syntax_lint.errors.clear()
        syntax_lint.check_summary_tag(lines)
        self.assertTrue(any("Missing closing summary" in e for e in syntax_lint.errors))

    def test_missing_opening(self):
        lines = [b"</summary>\n"]
        syntax_lint.errors.clear()
        syntax_lint.check_summary_tag(lines)
        self.assertTrue(any("Missing opening summary" in e for e in syntax_lint.errors))

    def test_oneline_summary(self):
        lines = [b"<summary>xyz</summary>\n"]
        syntax_lint.errors.clear()
        syntax_lint.check_summary_tag(lines)
        self.assertFalse(syntax_lint.errors)

    def test_nested_open(self):
        lines = [b"<summary>\n", b"<summary>\n"]
        syntax_lint.errors.clear()
        syntax_lint.check_summary_tag(lines)
        self.assertTrue(any("Missing closing summary " in e or "Missing closing summary tag" in e for e in syntax_lint.errors))

class TestCheckMdFile(unittest.TestCase):
    def setUp(self):
        syntax_lint.errors.clear()
        self.old_p = syntax_lint.p

    def tearDown(self):
        syntax_lint.p = self.old_p

    def test_valid_file(self):
        import tempfile
        with tempfile.NamedTemporaryFile(mode="wb", delete=False) as f:
            f.write(b"<details>\ntext\n<summary>\ntext\n</summary>\n</details>\n")
            tfname = f.name
        syntax_lint.p = tfname
        syntax_lint.check_md_file(tfname)
        os.remove(tfname)
        self.assertFalse(syntax_lint.errors)

    def test_file_with_errors(self):
        import tempfile
        with tempfile.NamedTemporaryFile(mode="wb", delete=False) as f:
            f.write(b"<details>\nno close\n<summary>\nno close\n")
            tfname = f.name
        syntax_lint.p = tfname
        syntax_lint.errors.clear()
        syntax_lint.check_md_file(tfname)
        os.remove(tfname)
        self.assertTrue(isinstance(syntax_lint.errors, list))

class TestMainGuard(unittest.TestCase):
    def test_main_block(self):
        import tempfile
        fname = None
        try:
            with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
                f.write(b"<details>\n<summary>\ntest\n</summary>\n</details>\n")
                fname = f.name

            orig_argv = sys.argv
            sys.argv = ["syntax_lint.py", fname]
            orig_p = syntax_lint.p
            syntax_lint.p = fname

            # Patch sys.exit to raise SystemExit
            orig_exit = sys.exit
            sys.exit = lambda code=None: (_ for _ in ()).throw(SystemExit(code))
            import contextlib
            s_out = io.StringIO()
            s_err = io.StringIO()
            with contextlib.redirect_stdout(s_out), contextlib.redirect_stderr(s_err):
                try:
                    exec(open(os.path.join(os.path.dirname(__file__), "syntax_lint.py")).read(), dict(__name__="__main__"))
                except SystemExit as e:
                    self.assertNotEqual(e.code, 1, "Should not exit with 1 for good input")
            sys.exit = orig_exit
            sys.argv = orig_argv
            syntax_lint.p = orig_p

            # Now with bad input (missing close tag)
            with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f2:
                f2.write(b"<details>\n")
                fname2 = f2.name
            sys.argv = ["syntax_lint.py", fname2]
            syntax_lint.p = fname2
            sys.exit = lambda code=None: (_ for _ in ()).throw(SystemExit(code))
            with contextlib.redirect_stdout(s_out), contextlib.redirect_stderr(s_err):
                try:
                    exec(open(os.path.join(os.path.dirname(__file__), "syntax_lint.py")).read(), dict(__name__="__main__"))
                except SystemExit as e:
                    self.assertEqual(e.code, 1)
            sys.exit = orig_exit
            sys.argv = orig_argv
            syntax_lint.p = orig_p
        finally:
            if fname and os.path.exists(fname):
                os.remove(fname)

if __name__ == "__main__":
    unittest.main()
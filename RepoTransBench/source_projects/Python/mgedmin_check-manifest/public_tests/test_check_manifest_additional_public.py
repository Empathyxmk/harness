import unittest
import sys

import check_manifest

class TestUI(unittest.TestCase):

    def test_quiet_and_verbose(self):
        # Use a different verbosity level for coverage
        ui = check_manifest.UI(verbosity=1)
        self.assertFalse(ui.quiet)
        self.assertFalse(ui.verbose)

        ui = check_manifest.UI(verbosity=3)
        self.assertFalse(ui.quiet)
        self.assertTrue(ui.verbose)

    def test_info_methods(self):
        # Different verbosity than original
        ui = check_manifest.UI(verbosity=3)
        # .info, .info_begin, .info_continue, .info_end: Should not crash
        ui.info("public info message")
        ui.info_begin("public begin message")
        ui.info_continue("public continued...")
        ui.info_end("public done!")
        ui._to_be_continued = True
        ui.info("public info after tbc")
        ui.error("public error message")
        ui.warning("public warn message")

    def test_info_quiet(self):
        ui = check_manifest.UI(verbosity=-1)
        ui.info("nothing to print here")
        ui.info_begin("still nothing begin")
        ui.info_continue("still nothing continue")
        ui.info_end("still nothing end")

    def test_error_and_warning(self):
        ui = check_manifest.UI(verbosity=1)
        ui.error("ERROR for public")
        ui.warning("WARNING for public")

class TestFormatUtils(unittest.TestCase):

    def test_format_list(self):
        # Use different input for format_list
        self.assertEqual(check_manifest.format_list(["x"]), "  x")
        self.assertEqual(check_manifest.format_list(["foo", "bar", "baz"]), "  foo\n  bar\n  baz")

    def test_format_missing(self):
        # Both lists non-empty for both
        self.assertEqual(
            check_manifest.format_missing(["first"], ["second"], "Alpha", "Beta"),
            "missing from Alpha:\n  first\nmissing from Beta:\n  second"
        )
        # Missing just from Beta
        self.assertEqual(
            check_manifest.format_missing([], ["hello"], "Src", "Dst"),
            "missing from Dst:\n  hello")
        # Missing just from Alpha
        self.assertEqual(
            check_manifest.format_missing(["world"], [], "Src", "Dst"),
            "missing from Src:\n  world"
        )
        # Both lists empty, different section names
        self.assertEqual(
            check_manifest.format_missing([], [], "One", "Two"),
            "")

class TestFailure(unittest.TestCase):

    def test_failure_message(self):
        msg = "another fail message"
        f = check_manifest.Failure(msg)
        self.assertEqual(str(f), msg)

    def test_command_failed(self):
        c = check_manifest.CommandFailed(['echo', 'abc'], 99, "fatal error")
        self.assertIn('failed', str(c))
        self.assertIn('echo', str(c))

if __name__ == "__main__":
    unittest.main()
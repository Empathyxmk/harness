import unittest
import sys
import types

import check_manifest


class TestUI(unittest.TestCase):

    def test_quiet_and_verbose(self):
        ui = check_manifest.UI(verbosity=0)
        self.assertTrue(ui.quiet)
        self.assertFalse(ui.verbose)

        ui = check_manifest.UI(verbosity=2)
        self.assertFalse(ui.quiet)
        self.assertTrue(ui.verbose)

    def test_info_methods(self):
        ui = check_manifest.UI(verbosity=2)
        # .info, .info_begin, .info_continue, .info_end: Should not crash
        ui.info("info message")
        ui.info_begin("begin message")
        ui.info_continue("continued...")
        ui.info_end("done!")
        ui._to_be_continued = True
        ui.info("info after tbc")
        ui.error("error message")
        ui.warning("warn message")

    def test_info_quiet(self):
        ui = check_manifest.UI(verbosity=0)
        ui.info("nothing prints")
        ui.info_begin("nothing prints begin")
        ui.info_continue("nothing prints continue")
        ui.info_end("nothing prints end")

    def test_error_and_warning(self):
        ui = check_manifest.UI(verbosity=1)
        ui.error("E")
        ui.warning("W")

class TestFormatUtils(unittest.TestCase):

    def test_format_list(self):
        self.assertEqual(check_manifest.format_list([]), "")
        self.assertEqual(check_manifest.format_list(["a", "b"]), "  a\n  b")

    def test_format_missing(self):
        # Both lists empty
        self.assertEqual(check_manifest.format_missing([], [], "A", "B"), "")
        # Just missing from a
        self.assertEqual(
            check_manifest.format_missing(["one"], [], "A", "B"),
            "missing from A:\n  one")
        # Just missing from b
        self.assertEqual(
            check_manifest.format_missing([], ["two"], "A", "B"),
            "missing from B:\n  two")
        # Missing from both
        self.assertIn(
            "missing from A", check_manifest.format_missing(["x"], ["y"], "A", "B"))
        self.assertIn(
            "missing from B", check_manifest.format_missing(["x"], ["y"], "A", "B"))

class TestFailure(unittest.TestCase):

    def test_failure_message(self):
        msg = "fail msg"
        f = check_manifest.Failure(msg)
        self.assertEqual(str(f), msg)

    def test_command_failed(self):
        c = check_manifest.CommandFailed(['cmd'], 1, "nope")
        self.assertIn('failed', str(c))

if __name__ == "__main__":
    unittest.main()
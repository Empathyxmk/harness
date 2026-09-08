import subprocess
import sys
import re

import pytest

class TestCLIPublic:

    def test_should_print_help_when_unknown_argument_provided(self):
        """
        Should print help (usage) when an unknown argument is provided.
        """
        completed = subprocess.run(
            [sys.executable, "cli.py", "--foobar"],
            capture_output=True,
            text=True
        )
        help_text = (completed.stdout or "") + (completed.stderr or "")
        assert "usage" in help_text.lower(), "Should output help instructions with unknown argument"

    def test_should_show_version_with_v_alias(self):
        """
        Should show version info when run with -v (alias).
        """
        completed = subprocess.run(
            [sys.executable, "cli.py", "-v"],
            capture_output=True,
            text=True
        )
        version_out = (completed.stdout or "") + (completed.stderr or "")
        assert re.search(r"\d+\.\d+\.\d+", version_out), "Should output version number with -v"

    def test_should_mention_shorten_in_help_output(self):
        """
        Should mention 'shorten' in help output.
        """
        completed = subprocess.run(
            [sys.executable, "cli.py", "--help"],
            capture_output=True,
            text=True
        )
        help_out = (completed.stdout or "") + (completed.stderr or "")
        assert "shorten" in help_out.lower(), "Help output should mention the 'shorten' command or feature"
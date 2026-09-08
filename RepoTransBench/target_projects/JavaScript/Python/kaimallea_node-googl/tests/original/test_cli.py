import subprocess
import sys

import pytest

class TestCLIBasicUsage:

    def test_should_output_help_information_when_run_with_no_args(self):
        """
        Should output help information when run with no args.
        Checks that 'Usage:' is present in stdout when calling the CLI with no arguments.
        """
        completed = subprocess.run(
            [sys.executable, "cli.py"], capture_output=True, text=True
        )
        assert "Usage:" in completed.stdout, "Output should include usage instructions"

    def test_should_output_version_with_version(self):
        """
        Should output version information when run with --version.
        Output should contain a version string like X.Y.Z.
        """
        completed = subprocess.run(
            [sys.executable, "cli.py", "--version"], capture_output=True, text=True
        )
        import re
        found = re.search(r"\d+\.\d+\.\d+", completed.stdout)
        assert found, "Output should contain a version string"

    def test_should_output_help_with_help(self):
        """
        Should output help information when run with --help.
        Output should include 'Options:' section.
        """
        completed = subprocess.run(
            [sys.executable, "cli.py", "--help"], capture_output=True, text=True
        )
        import re
        found = re.search(r"Options:", completed.stdout)
        assert found, "Output should include Options section"
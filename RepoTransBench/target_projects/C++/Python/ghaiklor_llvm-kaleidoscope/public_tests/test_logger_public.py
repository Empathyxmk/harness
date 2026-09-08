import pytest
import io
import sys

class Logger:
    def info(self, msg):
        print(msg)

    def error(self, msg):
        print(msg, file=sys.stderr)

def test_info_output_public_test(capsys):
    logger = Logger()
    logger.info("A PUBLIC info message for test output.")
    output = capsys.readouterr().out
    assert "A PUBLIC info message for test output." in output

def test_error_output_public_test(capsys):
    logger = Logger()
    logger.error("A PUBLIC error message for test output.")
    errorOutput = capsys.readouterr().err
    assert "A PUBLIC error message for test output." in errorOutput
import unittest

class ExceptionBuilder:
    def __init__(self, message, file):
        self._message = message
        self._file = file

    def message(self):
        return f"{self._message} (in {self._file})"

class TestPublicExceptionBuilder(unittest.TestCase):
    def test_public_message_and_file(self):
        builder = ExceptionBuilder("Different Error!", "randomfile.cpp")
        msg = builder.message()
        self.assertIn("Different Error!", msg)
        self.assertIn("randomfile.cpp", msg)
import unittest
import io

def log_info(stream, message):
    stream.write(str(message) + "\n")

def log_warn(stream, message):
    stream.write(str(message) + "\n")

class TestPublicLogging(unittest.TestCase):
    def test_public_info(self):
        stream = io.StringIO()
        log_info(stream, "PUBLIC info message 2468")
        contents = stream.getvalue()
        self.assertIn("PUBLIC info message 2468", contents)

    def test_public_warn(self):
        stream = io.StringIO()
        log_warn(stream, "YELLOW warning!")
        contents = stream.getvalue()
        self.assertIn("YELLOW warning!", contents)
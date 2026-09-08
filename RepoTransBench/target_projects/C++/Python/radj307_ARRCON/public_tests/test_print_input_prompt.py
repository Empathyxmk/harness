import unittest
import io

def print_input_prompt(stream, prompt, n):
    # n parameter is unused but included to match signature
    stream.write(str(prompt))

class TestPublicPrintInputPrompt(unittest.TestCase):
    def test_public_prompt(self):
        stream = io.StringIO()
        print_input_prompt(stream, "Give user input:", 17)
        output = stream.getvalue()
        self.assertIn("Give user input:", output)
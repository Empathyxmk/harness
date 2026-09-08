import unittest

from pyzbar.pyzbar_error import PyZbarError

class TestPyzbarErrorPublic(unittest.TestCase):
    def test_error_message(self):
        # Use a different message than default test
        e = PyZbarError("Public test: barcode problem")
        self.assertEqual(str(e), "Public test: barcode problem")

    def test_error_raise_and_catch(self):
        try:
            raise PyZbarError("Test error for catching")
        except PyZbarError as e:
            self.assertTrue("catching" in str(e))

if __name__ == '__main__':
    unittest.main()
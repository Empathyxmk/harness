import unittest
from src.gurugio_book.error_handle import error_printer, error_return

class TestErrorHandlePublic(unittest.TestCase):
    """Public tests for the error handling functions"""
    
    def test_error_printer_public(self):
        """Test the error_printer function (public)"""
        # Different messages from original test
        self.assertEqual(error_printer("public message example"), 0)
        # Still test NULL, required branch
        self.assertEqual(error_printer(None), -1)
    
    def test_error_return_public(self):
        """Test the error_return function (public)"""
        # Different error codes
        self.assertEqual(error_return(10), 10)
        self.assertEqual(error_return(-7), -7)
        # Still test zero, required branch
        self.assertEqual(error_return(0), 0)

if __name__ == '__main__':
    unittest.main()
    print("test_error_handle_public: OK")
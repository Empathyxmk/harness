import unittest
from src.gurugio_book.error_handle import error_printer, error_return

class TestErrorHandle(unittest.TestCase):
    """Tests for the error handling functions translated from test_error_handle.c"""
    
    def test_error_printer(self):
        """Test the error_printer function"""
        # coverage: normal use
        self.assertEqual(error_printer("hello world"), 0)
        # coverage: NULL (error branch)
        self.assertEqual(error_printer(None), -1)
    
    def test_error_return(self):
        """Test the error_return function"""
        # coverage: normal (error code)
        self.assertEqual(error_return(5), 5)
        # coverage: no print branch
        self.assertEqual(error_return(0), 0)

if __name__ == '__main__':
    unittest.main()
    print("test_error_handle: OK")
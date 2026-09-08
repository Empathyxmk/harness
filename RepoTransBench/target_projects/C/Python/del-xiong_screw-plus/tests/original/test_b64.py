import unittest
import sys
import os

# Add the parent directory to the path so we can import the src module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.b64 import b64_encode, b64_decode

class TestB64(unittest.TestCase):
    
    def test_encode_empty(self):
        """Test encoding an empty string"""
        res = b64_encode("", 0)
        self.assertEqual(res, "")
    
    def test_encode_simple(self):
        """Test encoding a simple character"""
        res = b64_encode("a", 1)
        self.assertEqual(res, "YQ==")
    
    def test_encode_padding(self):
        """Test encoding with different padding"""
        res2 = b64_encode("ab", 2)
        self.assertEqual(res2, "YWI=")
        
        res3 = b64_encode("abc", 3)
        self.assertEqual(res3, "YWJj")
    
    def test_decode_empty(self):
        """Test decoding an empty string"""
        sz = [0]
        res = b64_decode("", 0, sz)
        self.assertEqual(sz[0], 0)
        self.assertEqual(res, b'')
    
    def test_decode_simple(self):
        """Test decoding a simple character"""
        sz = [0]
        res = b64_decode("YQ==", 4, sz)
        self.assertEqual(sz[0], 1)
        self.assertEqual(res, b'a')
    
    def test_decode_padding(self):
        """Test decoding with different padding"""
        sz = [0]
        res = b64_decode("YWI=", 4, sz)
        self.assertEqual(sz[0], 2)
        self.assertEqual(res, b'ab')
        
        res = b64_decode("YWJj", 4, sz)
        self.assertEqual(sz[0], 3)
        self.assertEqual(res, b'abc')
    
    def test_decode_invalid(self):
        """Test decoding invalid base64 data"""
        sz = [-1]
        res = b64_decode("#$%^", 4, sz)
        self.assertEqual(sz[0], 0)
        self.assertEqual(res, b'')

if __name__ == '__main__':
    unittest.main()
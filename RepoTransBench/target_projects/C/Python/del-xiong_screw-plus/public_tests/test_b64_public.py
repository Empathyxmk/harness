import unittest
import sys
import os

# Add the parent directory to the path so we can import the src module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.b64 import b64_encode, b64_decode

class TestB64Public(unittest.TestCase):
    
    def test_base64_encode_decode(self):
        """Test encode and decode of a complex string"""
        src = "OpenAI_Test_String!987"
        enc_dst = b64_encode(src, len(src))
        self.assertEqual(enc_dst, "T3BlbkFJX1Rlc3RfU3RyaW5nITk4Nw==")
        
        outlen = [0]
        dec_dst = b64_decode(enc_dst, len(enc_dst), outlen)
        self.assertEqual(outlen[0], len(src))
        self.assertEqual(dec_dst.decode('utf-8'), src)
    
    def test_empty_string(self):
        """Test encode and decode of an empty string"""
        src = ""
        enc_dst = b64_encode(src, 0)
        self.assertEqual(enc_dst, "")
        
        outlen = [0]
        dec_dst = b64_decode(enc_dst, len(enc_dst), outlen)
        self.assertEqual(outlen[0], 0)
        self.assertEqual(dec_dst, b'')
    
    def test_one_byte(self):
        """Test encode and decode of a single character"""
        src = "Z"
        enc_dst = b64_encode(src, 1)
        self.assertEqual(enc_dst, "Wg==")
        
        outlen = [0]
        dec_dst = b64_decode(enc_dst, len(enc_dst), outlen)
        self.assertEqual(outlen[0], 1)
        self.assertEqual(dec_dst.decode('utf-8'), src)

if __name__ == '__main__':
    unittest.main()
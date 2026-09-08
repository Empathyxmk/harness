import unittest
import sys
import os

# Add the parent directory to the path so we can import the src module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.b64 import b64_encode, b64_decode

class TestB64TablePublic(unittest.TestCase):
    
    def test_various_base64_values(self):
        """Test various base64 encode/decode values"""
        # Test data: "linkedin"
        input1 = "linkedin"
        enc1 = b64_encode(input1, len(input1))
        self.assertEqual(enc1, "bGlua2VkaW4=")
        
        outlen1 = [0]
        dec1 = b64_decode(enc1, len(enc1), outlen1)
        self.assertEqual(outlen1[0], len(input1))
        self.assertEqual(dec1.decode('utf-8'), input1)
        
        # Test data: "DataScience"
        input2 = "DataScience"
        enc2 = b64_encode(input2, len(input2))
        self.assertEqual(enc2, "RGF0YVNjaWVuY2U=")
        
        outlen2 = [0]
        dec2 = b64_decode(enc2, len(enc2), outlen2)
        self.assertEqual(outlen2[0], len(input2))
        self.assertEqual(dec2.decode('utf-8'), input2)
        
        # 'edge' case, "z" (single character)
        input3 = "z"
        enc3 = b64_encode(input3, 1)
        self.assertEqual(enc3, "eg==")
        
        outlen3 = [0]
        dec3 = b64_decode(enc3, len(enc3), outlen3)
        self.assertEqual(outlen3[0], 1)
        self.assertEqual(dec3.decode('utf-8'), input3)

if __name__ == '__main__':
    unittest.main()
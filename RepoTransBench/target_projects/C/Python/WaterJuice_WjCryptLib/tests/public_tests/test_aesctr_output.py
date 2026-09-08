import unittest
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from wjcryptlib.aes import aes_ctr_encrypt

class TestAesCtrOutput(unittest.TestCase):
    def test_aes_ctr_output(self):
        """Test AES-CTR output (same as public_test_aesctr_output.bash)"""
        # Using the same key, IV, and plaintext as in the bash test
        key = "2b7e151628aed2a6abf7158809cf4f3c"
        iv = "000102030405060708090a0b0c0d0e0f"
        plaintext = "00112233445566778899aabbccddeeff"
        
        # Precomputed ciphertext for the above parameters
        expected = "29c3505f571420f6402299b31a02d73a"
        
        # Encrypt the plaintext
        output = aes_ctr_encrypt(key, iv, plaintext)
        
        # Verify the result
        self.assertEqual(output, expected)

if __name__ == '__main__':
    unittest.main()
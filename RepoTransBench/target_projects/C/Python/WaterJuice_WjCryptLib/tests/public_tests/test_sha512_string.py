import unittest
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from wjcryptlib.sha512 import sha512_string

class TestSha512String(unittest.TestCase):
    def test_sha512_string(self):
        """Test SHA-512 hash of a string (same as public_test_sha512_string.bash)"""
        # Use the same input as in the bash test
        input_string = "hello world"
        
        # Expected SHA512 using: echo -n "hello world" | sha512sum | awk '{print $1}'
        expected = "309ecc489c12d6eb4cc40f50c902f2b4d0ed77ee511a7c7a9bcd3ca86d4cd86f989dd35bc5ff499670da34255b45b0cfd830e81f605dcf7dc5542e93ae9cd76f"
        
        # Calculate the SHA-512 hash
        output = sha512_string(input_string)
        
        # Verify the result
        self.assertEqual(output, expected)

if __name__ == '__main__':
    unittest.main()
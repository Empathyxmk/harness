import pytest
import os
import subprocess
import tempfile
import sys

def test_crypt_test_public():
    """Public test for crypt_test with different input."""
    # Create a temporary file to capture output
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
        temp_filename = temp_file.name
    
    try:
        # Run the crypt_test function with different command-line arguments
        command = [sys.executable, "-m", "src.intere_hacking.crypt_test", "hello", "ab"]
        with open(temp_filename, 'w') as outfile:
            subprocess.run(command, stdout=outfile, check=True)
        
        # Read the output file
        with open(temp_filename, 'r') as infile:
            output = infile.read()
        
        # Check for expected output
        assert "hashes to ==>" in output, "crypt_test_public_test: Output did not match"
        print("crypt_test_public_test ran: PASS")
    finally:
        # Clean up temporary file
        os.remove(temp_filename)
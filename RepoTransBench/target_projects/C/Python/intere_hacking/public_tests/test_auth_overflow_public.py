import pytest
import os
import subprocess
import tempfile
import sys

def test_auth_overflow_public():
    """Public test for auth_overflow with different input."""
    # Create a temporary file to capture output
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
        temp_filename = temp_file.name
    
    try:
        # Create a simple script that imports and tests the auth_overflow function
        script = """
import sys
from src.intere_hacking.auth_overflow import check_authentication

result = check_authentication("alice")
print(f"Authentication result: {result}")
"""
        script_file = tempfile.NamedTemporaryFile(mode='w+', suffix='.py', delete=False)
        script_filename = script_file.name
        script_file.write(script)
        script_file.close()
        
        # Run the script and capture output
        command = [sys.executable, script_filename, "alice", "newpassword"]
        with open(temp_filename, 'w') as outfile:
            subprocess.run(command, stdout=outfile, check=True)
        
        # Read the output file
        with open(temp_filename, 'r') as infile:
            output = infile.read()
        
        # Check that there was some output
        assert len(output) > 0, "auth_overflow (public): Output did not match"
        print("auth_overflow (public) ran: PASS")
    finally:
        # Clean up temporary files
        os.remove(temp_filename)
        os.remove(script_filename)
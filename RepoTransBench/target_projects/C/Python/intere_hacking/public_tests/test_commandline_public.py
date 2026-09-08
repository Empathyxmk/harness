import pytest
import os
import subprocess
import tempfile
import sys

def test_commandline_public():
    """Public test for commandline with different input."""
    # Create a temporary file to capture output
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
        temp_filename = temp_file.name
    
    try:
        # Create a simple script that imports and tests the commandline function
        script = """
import sys
from src.intere_hacking.commandline import main_commandline

args = ["commandline", "foo"]
main_commandline(len(args), args)
"""
        script_file = tempfile.NamedTemporaryFile(mode='w+', suffix='.py', delete=False)
        script_filename = script_file.name
        script_file.write(script)
        script_file.close()
        
        # Run the script and capture output
        command = [sys.executable, script_filename]
        with open(temp_filename, 'w') as outfile:
            subprocess.run(command, stdout=outfile, check=True)
        
        # Read the output file
        with open(temp_filename, 'r') as infile:
            output = infile.read()
        
        # Check for expected output
        assert "foo" in output, "commandline (public): Output did not match"
        print("commandline (public) ran: PASS")
    finally:
        # Clean up temporary files
        os.remove(temp_filename)
        os.remove(script_filename)
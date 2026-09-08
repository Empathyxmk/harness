import pytest
import os
import subprocess
import tempfile
import sys

def test_dtors_sample_public():
    """Public test for dtors_sample with different expectations."""
    # Create a temporary file to capture output
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
        temp_filename = temp_file.name
    
    try:
        # Create a simple script that imports and runs the dtors_sample main function
        script = """
import sys
from src.intere_hacking.dtors_sample import main
sys.exit(main())
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
        
        # Check for different expected output compared to original test
        mainmsg = "Some actions happen in the main" in output
        destructormsg = "In the cleanup function now" in output
        
        assert mainmsg and destructormsg, "dtors_sample (public): Output did not match"
        print("dtors_sample (public) ran: PASS")
    finally:
        # Clean up temporary files
        os.remove(temp_filename)
        os.remove(script_filename)
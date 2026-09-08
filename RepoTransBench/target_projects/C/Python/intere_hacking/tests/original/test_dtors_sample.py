import pytest
import os
import subprocess
import tempfile
import sys
import atexit

def test_dtors_sample_output():
    """Test that dtors_sample produces the expected output."""
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
        
        # Check for expected output
        found_main = "main() function" in output or "Some actions happen in the main" in output
        found_cleanup = "cleanup function" in output or "In the cleanup function" in output
        
        assert found_main and found_cleanup, "dtors_sample output missing main/cleanup"
        print("dtors_sample test: PASS")
    finally:
        # Clean up temporary files
        os.remove(temp_filename)
        os.remove(script_filename)
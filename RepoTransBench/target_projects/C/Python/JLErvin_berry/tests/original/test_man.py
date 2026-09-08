import subprocess
import os
import sys

def test_man_page_completeness():
    """
    Test that all client functions in client.c are documented in the man pages.
    This is a Python implementation of the test_man.sh shell script.
    """
    # Get the repository root directory
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
    
    # Extract client functions from client.c
    client_c_path = os.path.join(repo_root, 'client.c')
    berryc_man_path = os.path.join(repo_root, 'berryc.1')
    
    # Check if the files exist
    if not os.path.exists(client_c_path) or not os.path.exists(berryc_man_path):
        pytest.skip("Source files not found (client.c or berryc.1)")
    
    # Use subprocess to run grep commands similar to the shell script
    try:
        # Get client functions
        client_functions_cmd = f"grep -E '{{..' {client_c_path} | cut -d' ' -f6 | sed -r 's/\"//g' | sed -r 's/,//g' | sort"
        client_functions = subprocess.check_output(client_functions_cmd, shell=True, text=True).strip().split('\n')
        
        # Get man page functions
        man_functions_cmd = f"grep -E '\\\\fB' {berryc_man_path} | sed -r 's/\\\\fB//g' | sed -r 's/(\\\\fR.*)//g' | sed -r 's/\\[//g' | sed -r 's/\\]//g' | tr '|' '\\n' | sort"
        man_functions = subprocess.check_output(man_functions_cmd, shell=True, text=True).strip().split('\n')
        
        # Find missing functions
        missing_functions = set(client_functions) - set(man_functions)
        
        # Print missing functions (just like the shell script)
        if missing_functions:
            print("MISSING FUNCTIONS")
            for func in sorted(missing_functions):
                print(func)
            
        # Assert that there are no missing functions
        assert not missing_functions, f"Found undocumented functions: {missing_functions}"
        
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Shell command execution failed: {e}")
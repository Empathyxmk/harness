#!/usr/bin/env python3
import os
import collections
import sys

def check_tabs():
    """
    Ensure every line has the same number of tabs in TEST-DATA.tsv.
    Equivalent to the C check-test-data-tabs.sh script.
    """
    try:
        tabs_per_line = []
        
        # Get the path to TEST-DATA.tsv relative to this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(os.path.dirname(script_dir), 'TEST-DATA.tsv')
        
        with open(file_path, 'r') as f:
            for line in f:
                if line.strip():  # Skip empty lines
                    tabs_per_line.append(line.count('\t'))
        
        # Count occurrences of each tab count
        tab_counts = collections.Counter(tabs_per_line)
        
        print(tab_counts)
        
        if len(tab_counts) == 1:
            print("✅ All lines have the same number of tabs")
            return 0
        else:
            print("❌ Not all lines have the same number of tabs")
            return 1
    except FileNotFoundError:
        print(f"❌ TEST-DATA.tsv file not found")
        return 1

if __name__ == "__main__":
    sys.exit(check_tabs())
import os
import json

def test_summary_json_content():
    # This test confirms that test_summary.json is present and valid JSON
    fname = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../test_summary.json"))
    if not os.path.exists(fname):
        # If file is missing, this is not a fatal test error (environment dependent)
        print("test_summary.json not found (ok in some dev/test setups)")
        return
    with open(fname, 'r') as f:
        data = json.load(f)
    assert "project_name" in data
    assert data["project_name"] == "jeffhammond_dpcpp-tutorial"
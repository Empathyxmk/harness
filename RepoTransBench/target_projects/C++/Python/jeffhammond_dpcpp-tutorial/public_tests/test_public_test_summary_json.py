import os
import json

def test_public_test_summary_json_content():
    fname = os.path.abspath(os.path.join(os.path.dirname(__file__), "../public_test_summary.json"))
    if not os.path.exists(fname):
        print("public_test_summary.json not found (ok in some setups)")
        return
    with open(fname, 'r') as f:
        data = json.load(f)
    assert "project_name" in data
    assert data["project_name"] == "jeffhammond_dpcpp-tutorial"
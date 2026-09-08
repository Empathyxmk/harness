import json

def test_summary_json_content():
    with open('test_summary.json','r') as f:
        data = json.load(f)
    assert "project_name" in data
    assert "line" in data["coverage"]
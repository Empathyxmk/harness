def test_test_summary_json_contents():
    import json
    import os
    fname = os.path.join(os.path.dirname(__file__), '..', '..', 'test_summary.json')
    with open(fname, 'r') as f:
        data = json.load(f)
    assert "project_name" in data
    assert data["language"] in ["C++", "cpp", "python", "Python"]
    assert "coverage" in data
    assert set(data["coverage"].keys()) >= {"line", "branch"}
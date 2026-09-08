import pytest

# Mock jsdocParse with core filtering and sorting logic
def jsdocParse(input_data):
    # Filter out anything not documented, or of kind typedef/enum/undocumented
    filtered = [
        d for d in input_data
        if (d.get("documented", True) or d.get("kind") == "function")
        and d.get("kind") not in ("typedef", "enum") or d.get("documented", True)
    ]
    # Sort by name (as in comments)
    return sorted(filtered, key=lambda d: d.get("name", ""))

def test_jsdocParse_filters_and_sorts_array_by_name_public():
    input = [
        {"name": "m", "documented": True, "kind": "function"},
        {"name": "a", "kind": "typedef", "undocumented": True},
        {"name": "n", "documented": True, "kind": "function"},
        {"name": "c", "kind": "enum", "undocumented": True},
    ]
    result = jsdocParse(input)
    assert [i["name"] for i in result] == ["m", "n"]

def test_jsdocParse_runs_public_transform_and_sorting():
    input = [
        {"name": "beta", "documented": True, "kind": "function"},
        {"name": "epsilon", "kind": "enum", "undocumented": True},
        {"name": "alpha", "documented": True, "kind": "function"},
    ]
    result = jsdocParse(input)
    assert [d["name"] for d in result] == ["alpha", "beta"]
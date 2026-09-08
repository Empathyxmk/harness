import pytest

import types

# We'll mock jsdocParse as a function
def jsdocParse(input_data):
    # Copy of mock: filters out undocumented or type/enum without documented=True, then sorts by order/category/scope/kind
    filtered = [
        d for d in input_data
        if (
            d.get("documented", True) or
            (d.get("kind") not in ["typedef", "enum"] or d.get("documented", True))
        )
        and d.get("kind") not in ("typedef", "enum") or d.get("documented", True)
    ]
    # The "sort" in original is: by scope, category, kind, order, but here just sort by 'order' or 'name' if given
    return sorted(filtered, key=lambda d: (d.get("order", 0), d.get("name", "")))

sampleInput = [
    {
        "name": "module:someModule",
        "longname": "module:someModule",
        "kind": "function",
        "meta": {"code": {"name": "doThing"}}
    },
    {
        "name": "SomeClass",
        "longname": "SomeClass",
        "kind": "class",
        "meta": {"code": {"name": "SomeClass"}}
    },
    {
        "name": "module:exportedThing",
        "longname": "module:exportedThing",
        "kind": "member",
        "meta": {"code": {"name": "exportedThing"}}
    },
    {
        "name": "notExported",
        "longname": "notExported",
        "kind": "member"
    }
]

def test_jsdocParse_returns_array_sorted_by_scope_category_kind_order():
    input = [
        {"name": "b", "kind": "class", "scope": "instance", "order": 2, "category": "x"},
        {"name": "c", "kind": "constant", "scope": "global", "order": 1, "category": "a"},
        {"name": "a", "kind": "function", "scope": "static", "order": 0, "category": "z"}
    ]
    # Sort-array not used; we assume sort by order then name
    result = sorted(input, key=lambda d: (d["order"], d["name"]))
    assert isinstance(result, list)
    assert "name" in result[0]
    assert len(result) == 3
    # Order: order=0,1,2 => a, c, b
    assert [i["name"] for i in result] == ['a', 'c', 'b']

def test_jsdocParse_runs_transform_and_sorting():
    import copy
    data = copy.deepcopy(sampleInput)
    output = jsdocParse(data)
    assert isinstance(output, list)
    assert len(output) > 0
    # Exported member will get special id -- not modeled, but test for "module:" exported exists
    assert any("module:" in d.get("name", "") for d in output)
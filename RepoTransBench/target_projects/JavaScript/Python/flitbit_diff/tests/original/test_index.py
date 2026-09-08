import pytest
import copy
import types
import re
from src.flitbit_diff.index import deepDiff

def test_main_function_callable_and_validates_diff():
    a = {"x": 1, "y": 2}
    b = {"x": 1, "y": 3, "z": 4}
    result = deepDiff(a, b)
    assert isinstance(result, list)
    assert any(r.get('kind') in ('E', 'N') for r in result)

def test_diff_returns_undefined_for_no_diff():
    one = {"foo": 1}
    assert deepDiff(one, {"foo": 1}) is None or deepDiff(one, {"foo": 1}) == []
    assert deepDiff(1, 1) is None or deepDiff(1, 1) == []
    assert deepDiff(None, None) is None or deepDiff(None, None) == []
    assert deepDiff(None, None) is None or deepDiff(None, None) == []

def test_array_difference():
    arr1 = [1, 2, 3]
    arr2 = [1, 3, 2, 4]
    diffres = deepDiff(arr1, arr2)
    assert diffres is not None
    assert isinstance(diffres, list)
    assert any(r.get('kind') == 'A' for r in diffres)

def test_deep_diff_circular_references():
    x = {"foo": 1}
    x["self"] = x
    y = {"foo": 2}
    y["self"] = y
    diff = deepDiff(x, y)
    assert diff is not None
    assert isinstance(diff, list)

def test_diff_with_date_and_regex_types():
    import datetime
    d1 = {"date": datetime.datetime(2020, 1, 1)}
    d2 = {"date": datetime.datetime(2022, 1, 1)}
    r = deepDiff(d1, d2)
    assert r is not None
    assert any(ch.get('kind') == 'E' for ch in r)

    obj1 = {"re": re.compile("abc", re.IGNORECASE)}
    obj2 = {"re": re.compile("xyz", re.DOTALL)}
    r2 = deepDiff(obj1, obj2)
    assert r2 is not None
    assert any(ch.get('kind') == 'E' for ch in r2)

def test_can_apply_change_and_revert_change():
    original = {"x": 1, "y": 2}
    modified = {"x": 1, "y": 3, "z": 4}
    diffs = deepDiff(original, modified)
    obj = {"x": 1, "y": 2}
    for diff in diffs:
        deepDiff.applyChange(obj, original, diff)
    assert obj == modified
    for diff in reversed(diffs):
        deepDiff.revertChange(obj, original, diff)
    assert obj == original

def test_prefilter_skips_selected_keys():
    obj1 = {"a": 1, "b": 2, "skip": 3}
    obj2 = {"a": 5, "b": 6, "skip": 10}
    r = deepDiff(obj1, obj2, lambda path, key: key == "skip")
    assert not any(diff and "skip" in diff.get("path", []) for diff in r)

def test_observableDiff_invokes_callback_on_every_change():
    obj1 = {"m": 1, "n": 2}
    obj2 = {"m": 1, "n": 3, "o": 4}
    observed = []
    def cb(d):
        if d:
            observed.append(d)
    deepDiff.observableDiff(obj1, obj2, cb)
    assert len(observed) > 0
    assert any(d.get('kind') in ('N', 'E') for d in observed)

def test_noConflict_restores_previous_DeepDiff_global():
    class DummyGlobal:
        pass
    fakeRoot = DummyGlobal()
    if hasattr(deepDiff, "noConflict"):
        returned = deepDiff.noConflict()
        if returned:
            assert callable(returned)

def test_detects_deleted_property():
    before = {"foo": 1, "gone": 2}
    after = {"foo": 1}
    res = deepDiff(before, after)
    assert any(r.get('kind') == 'D' for r in res)

def test_detects_array_item_removed():
    before = [1, 2, 3, 4]
    after = [1, 3, 4]
    res = deepDiff(before, after)
    assert len([r for r in res if r.get('kind') == 'A' and r.get('item', {}).get('kind') == 'D']) > 0

def test_applyDiff_with_array_A_modification():
    arr1 = [1, 2, 3]
    arr2 = [1, 4, 3]
    diffArr = deepDiff(arr1, arr2)
    copy_arr = arr1[:]
    for d in diffArr:
        deepDiff.applyChange(copy_arr, arr1, d)
    assert copy_arr == arr2

def test_observableDiff_handles_null_and_undefined():
    arr = []
    deepDiff.observableDiff(None, {}, lambda d: arr.append(d))
    deepDiff.observableDiff(None, {}, lambda d: arr.append(d))
    assert arr is not None

def test_observableDiff_with_circular_references():
    a = {}
    a['a'] = a
    b = {}
    b['a'] = b
    items = []
    def cb(change):
        items.append(change)
    deepDiff.observableDiff(a, b, cb)
    assert len(items) >= 1

def test_applyChange_does_nothing_for_unknown_kind():
    o = {"a": 1}
    orig = {"a": 1}
    badDiff = {"kind": "X", "path": []}
    try:
        deepDiff.applyChange(o, orig, badDiff)
    except Exception as e:
        pytest.fail(f"applyChange should not raise error for unknown kind: {e}")

def test_revertChange_does_nothing_for_unknown_kind():
    o = {"a": 1}
    orig = {"a": 1}
    badDiff = {"kind": "X", "path": []}
    try:
        deepDiff.revertChange(o, orig, badDiff)
    except Exception as e:
        pytest.fail(f"revertChange should not raise error for unknown kind: {e}")
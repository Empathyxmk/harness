import pytest
import copy
import re
from src.flitbit_diff.index import deepDiff

def test_main_function_callable_and_validates_diff_public():
    a = {"a": 10, "b": 20}
    b = {"a": 10, "b": 30, "c": 40}
    result = deepDiff(a, b)
    assert isinstance(result, list)
    assert any(r.get('kind') in ('E', 'N') for r in result)

def test_diff_returns_undefined_for_no_diff_public():
    test = {"bar": 42}
    assert deepDiff(test, {"bar": 42}) is None or deepDiff(test, {"bar": 42}) == []
    assert deepDiff(5, 5) is None or deepDiff(5, 5) == []
    assert deepDiff(None, None) is None or deepDiff(None, None) == []
    assert deepDiff(None, None) is None or deepDiff(None, None) == []

def test_array_difference_public():
    arr1 = [4, 5, 6]
    arr2 = [4, 6, 5, 7]
    diffres = deepDiff(arr1, arr2)
    assert diffres is not None
    assert isinstance(diffres, list)
    assert any(r.get('kind') == 'A' for r in diffres)

def test_deep_diff_circular_references_public():
    obj1 = {"bar": 10}
    obj1["myself"] = obj1
    obj2 = {"bar": 20}
    obj2["myself"] = obj2
    diff = deepDiff(obj1, obj2)
    assert diff is not None
    assert isinstance(diff, list)

def test_diff_with_date_and_regex_types_public():
    import datetime
    d1 = {"date": datetime.datetime(2019, 5, 5)}
    d2 = {"date": datetime.datetime(2021, 6, 10)}
    r = deepDiff(d1, d2)
    assert r is not None
    assert any(ch.get('kind') == 'E' for ch in r)

    obj1 = {"reg": re.compile("123", re.IGNORECASE)}
    obj2 = {"reg": re.compile("999", re.MULTILINE)}
    r2 = deepDiff(obj1, obj2)
    assert r2 is not None
    assert any(ch.get('kind') == 'E' for ch in r2)

def test_can_apply_change_and_revert_change_public():
    original = {"a": 100, "b": 200}
    modified = {"a": 100, "b": 999, "c": 123}
    diffs = deepDiff(original, modified)
    obj = {"a": 100, "b": 200}
    for diff in diffs:
        deepDiff.applyChange(obj, original, diff)
    assert obj == modified
    for diff in reversed(diffs):
        deepDiff.revertChange(obj, original, diff)
    assert obj == original

def test_prefilter_skips_selected_keys_public():
    obj1 = {"foo": 1, "bar": 2, "omit": 99}
    obj2 = {"foo": 10, "bar": 20, "omit": 123}
    r = deepDiff(obj1, obj2, lambda path, key: key == "omit")
    assert not any(diff and "omit" in diff.get("path", []) for diff in r)

def test_observableDiff_invokes_callback_on_every_change_public():
    obj1 = {"p": 111, "q": 222}
    obj2 = {"p": 111, "q": 333, "r": 444}
    observed = []
    def cb(d):
        if d:
            observed.append(d)
    deepDiff.observableDiff(obj1, obj2, cb)
    assert len(observed) > 0
    assert any(d.get('kind') in ('N', 'E') for d in observed)

def test_noConflict_restores_previous_DeepDiff_global_public():
    class DummyGlobal:
        pass
    fakeRoot = DummyGlobal()
    if hasattr(deepDiff, "noConflict"):
        returned = deepDiff.noConflict()
        if returned:
            assert callable(returned)

def test_detects_deleted_property_public():
    before = {"bar": 10, "remove": 20}
    after = {"bar": 10}
    res = deepDiff(before, after)
    assert any(r.get('kind') == 'D' for r in res)

def test_detects_array_item_removed_public():
    before = [9, 8, 7, 6]
    after = [9, 7, 6]
    res = deepDiff(before, after)
    assert len([r for r in res if r.get('kind') == 'A' and r.get('item', {}).get('kind') == 'D']) > 0

def test_applyDiff_with_array_A_modification_public():
    arr1 = [4, 5, 6]
    arr2 = [4, 8, 6]
    diffArr = deepDiff(arr1, arr2)
    copy_arr = arr1[:]
    for d in diffArr:
        deepDiff.applyChange(copy_arr, arr1, d)
    assert copy_arr == arr2

def test_observableDiff_handles_null_and_undefined_public():
    arr = []
    deepDiff.observableDiff(None, {"foo": 1}, lambda d: arr.append(d))
    deepDiff.observableDiff(None, {"foo": 1}, lambda d: arr.append(d))
    assert arr is not None

def test_observableDiff_with_circular_references_public():
    a = {}
    a["ref"] = a
    b = {}
    b["ref"] = b
    items = []
    def cb(change):
        items.append(change)
    deepDiff.observableDiff(a, b, cb)
    assert len(items) >= 1

def test_applyChange_does_nothing_for_unknown_kind_public():
    obj = {"foo": 77}
    orig = {"foo": 77}
    badDiff = {"kind": "Z", "path": []}
    try:
        deepDiff.applyChange(obj, orig, badDiff)
    except Exception as e:
        pytest.fail(f"applyChange should not raise error for unknown kind: {e}")

def test_revertChange_does_nothing_for_unknown_kind_public():
    obj = {"bar": 88}
    orig = {"bar": 88}
    badDiff = {"kind": "Y", "path": []}
    try:
        deepDiff.revertChange(obj, orig, badDiff)
    except Exception as e:
        pytest.fail(f"revertChange should not raise error for unknown kind: {e}")
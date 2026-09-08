from src.fast_deep_equal.react import react_deep_equal as equal

def test_ignore_owner_on_react_elements():
    REACT_ELEMENT = "react.element"
    # Simulate symbol by using string tag
    reactElementA = {
        "$$typeof": REACT_ELEMENT,
        "type": "div",
        "key": None,
        "ref": None,
        "props": {"children": "hi"},
        "_owner": {"some": "circular"}
    }
    reactElementB = {
        "$$typeof": REACT_ELEMENT,
        "type": "div",
        "key": None,
        "ref": None,
        "props": {"children": "hi"},
        "_owner": {"some": "other"}
    }
    assert equal(reactElementA, reactElementB) is True

def test_fallback_to_normal_behavior_non_react():
    assert equal({"a": 1}, {"a": 1}) is True
    assert equal({"a": 1}, {"a": 2}) is False

def test_deeply_unequal_react():
    REACT_ELEMENT = "react.element"
    eltA = {
        "$$typeof": REACT_ELEMENT,
        "foo": {"bar": [1, 2, 3]},
        "_owner": {},
        "baz": 5
    }
    eltB = {
        "$$typeof": REACT_ELEMENT,
        "foo": {"bar": [1, 2, 4]},
        "_owner": {},
        "baz": 5
    }
    assert equal(eltA, eltB) is False
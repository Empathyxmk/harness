from src.fast_deep_equal.react import react_deep_equal as equal

def test_ignore_owner_on_react_elements_public():
    REACT_ELEMENT = "react.element"
    reactElementA = {
        "$$typeof": REACT_ELEMENT,
        "type": "span",
        "key": None,
        "ref": None,
        "props": {"children": "hello world"},
        "_owner": {"alt": "something"}
    }
    reactElementB = {
        "$$typeof": REACT_ELEMENT,
        "type": "span",
        "key": None,
        "ref": None,
        "props": {"children": "hello world"},
        "_owner": {"alt": "another"}
    }
    assert equal(reactElementA, reactElementB) is True

def test_fallback_to_normal_behavior_non_react_public():
    assert equal({"x": 2}, {"x": 2}) is True
    assert equal({"x": 2}, {"x": 3}) is False

def test_deeply_unequal_react_public():
    REACT_ELEMENT = "react.element"
    eltA = {
        "$$typeof": REACT_ELEMENT,
        "first": {"second": [4, 5, 6]},
        "_owner": {},
        "third": "abc"
    }
    eltB = {
        "$$typeof": REACT_ELEMENT,
        "first": {"second": [4, 5, 7]},
        "_owner": {},
        "third": "abc"
    }
    assert equal(eltA, eltB) is False
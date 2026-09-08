import pytest

from src import nodeCreator

def test_reject_unhandled_type():
    with pytest.raises(Exception):
        nodeCreator.createNode(True, {}, lambda: None, None)

def test_is_frozen_false_for_nonobject():
    assert nodeCreator.isFrozen(123) is False
    assert nodeCreator.isFrozen(None) is False

def test_set_value_and_call_update_cb():
    updated = {'value': False}
    def updateCB():
        updated['value'] = True
        return [42]
    node = nodeCreator.createNode([], {}, updateCB, "freezer")
    node.set(0, 100)
    assert updated['value'] is True

def test_delete_using_node_delete():
    updated = {'value': False}
    def updateCB():
        updated['value'] = True
        return []
    node = nodeCreator.createNode([], {}, updateCB, "freezer")
    node.push(1)
    node.push(2)
    # 'delete' as a non-function property
    getattr(node, 'delete')(0)
    assert updated['value'] is True
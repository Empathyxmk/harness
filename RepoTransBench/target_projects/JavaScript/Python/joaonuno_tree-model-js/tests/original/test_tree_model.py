import pytest
from src.tree_model import TreeModel

def sample_tree_dict():
    return {
        'id': 1,
        'name': 'root',
        'children': [
            {
                'id': 11,
                'name': 'child1',
                'children': [
                    {'id': 111, 'name': 'grandchild1'},
                    {'id': 112, 'name': 'grandchild2'}
                ]
            },
            {
                'id': 12,
                'name': 'child2',
                'children': []
            }
        ]
    }

def test_create_tree_basic_properties():
    tree = TreeModel(sample_tree_dict())
    assert tree.node['id'] == 1
    assert tree.node['name'] == "root"
    assert len(tree.children) == 2
    assert tree.children[0].node['id'] == 11

def test_parent_relationships():
    tree = TreeModel(sample_tree_dict())
    child1 = tree.children[0]
    child2 = tree.children[1]
    grandchild1 = child1.children[0]
    assert child1.parent is tree
    assert child2.parent is tree
    assert grandchild1.parent is child1
    assert grandchild1.root is tree

def test_is_root():
    tree = TreeModel(sample_tree_dict())
    child1 = tree.children[0]
    assert tree.is_root()
    assert not child1.is_root()

def test_is_leaf():
    tree = TreeModel(sample_tree_dict())
    child1 = tree.children[0]
    grandchild1 = child1.children[0]
    assert not tree.is_leaf()
    assert not child1.is_leaf()
    assert grandchild1.is_leaf()

def test_add_child_and_remove_child():
    tree = TreeModel({'id': 2, 'name': 'A'})
    child = TreeModel({'id': 3, 'name': 'B'})
    tree.add_child(child)
    assert child in tree.children
    assert child.parent is tree

    tree.remove_child(child)
    assert child not in tree.children
    assert child.parent is None

def test_get_path():
    tree = TreeModel(sample_tree_dict())
    child1 = tree.children[0]
    grandchild1 = child1.children[0]
    path = grandchild1.get_path()
    assert [n.node['id'] for n in path] == [1,11,111]

def test_find_in_subtree():
    tree = TreeModel(sample_tree_dict())
    leaf = tree.find(lambda n: n.node['id'] == 112)
    assert leaf is not None
    assert leaf.node['name'] == "grandchild2"

def test_walk_traversal_order():
    tree = TreeModel(sample_tree_dict())
    visited = []
    def visit(node):
        visited.append(node.node['id'])
    tree.walk(visit)
    # Should be pre-order traversal
    assert visited == [1,11,111,112,12]

def test_walk_stop_iteration():
    tree = TreeModel(sample_tree_dict())
    visited = []
    def visit(node):
        visited.append(node.node['id'])
        if node.node['id'] == 11:
            return False  # Stop traversal
    tree.walk(visit)
    assert 1 in visited
    assert 11 in visited
    assert 111 not in visited
    assert 12 not in visited

def test_traverse_post_order():
    tree = TreeModel(sample_tree_dict())
    order = []
    tree.walk(lambda n: order.append(n.node['id']), post_order=True)
    assert order == [111,112,11,12,1]

def test_exception_on_remove_nonchild():
    tree = TreeModel({'id': 2, 'name': 'A'})
    not_a_child = TreeModel({'id': 99, 'name': 'X'})
    with pytest.raises(ValueError):
        tree.remove_child(not_a_child)

def test_to_dict_round_trip():
    original = sample_tree_dict()
    tree = TreeModel(original)
    as_dict = tree.to_dict()
    assert as_dict == original

def test_custom_property_on_node():
    original = sample_tree_dict()
    tree = TreeModel(original)
    tree.node['foo'] = 'bar'
    assert tree.node['foo'] == 'bar'

def test_repr_and_str():
    tree = TreeModel(sample_tree_dict())
    s = str(tree)
    r = repr(tree)
    assert 'root' in s
    assert 'TreeModel' in r

def test_depth_and_height():
    tree = TreeModel(sample_tree_dict())
    child1 = tree.children[0]
    grandchild1 = child1.children[0]
    assert tree.depth() == 0
    assert child1.depth() == 1
    assert grandchild1.depth() == 2

    # Assuming height is implemented
    assert tree.height() == 2
    assert child1.height() == 1
    assert grandchild1.height() == 0
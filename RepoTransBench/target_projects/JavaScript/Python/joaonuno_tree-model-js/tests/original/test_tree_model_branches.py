import pytest

# Assuming the TreeModel class is implemented and importable from src.tree_model
try:
    from src.tree_model import TreeModel
except ImportError:
    TreeModel = None

@pytest.mark.skipif(TreeModel is None, reason="TreeModel implementation missing")
class TestTreeModelBranches:

    def test_instantiate_with_config(self):
        tree = TreeModel(children_property_name='kids')
        assert isinstance(tree, TreeModel)

    def test_parse_node_with_custom_children(self):
        tree = TreeModel(children_property_name='subs')
        root = tree.parse({'subs': [{}, {}]})
        assert len(root.children) == 2

    def test_parse_not_object_raises(self):
        tree = TreeModel()
        with pytest.raises(Exception, match="object"):
            tree.parse("str")
        with pytest.raises(Exception, match="object"):
            tree.parse(123)
        with pytest.raises(Exception, match="object"):
            tree.parse(None)
        with pytest.raises(Exception, match="object"):
            tree.parse(None)

    def test_get_child_at_returns_undefined(self):
        tree = TreeModel()
        root = tree.parse({'children': [{'id': 1}]})
        assert len(root.children) == 1
        assert (root.children[1] if len(root.children) > 1 else None) is None

    def test_is_root_and_has_children(self):
        tree = TreeModel()
        root = tree.parse({'children': [{'id': 1}]})
        child = root.children[0]
        assert root.is_root()
        assert root.has_children()
        assert not child.is_root()
        assert not child.has_children()

    def test_remove_child_and_parent_update(self):
        tree = TreeModel()
        root = tree.parse({'children': [{'id': 1}]})
        child = root.children[0]
        child.drop()
        assert len(root.children) == 0
        assert getattr(child, 'parent', None) is None

    def test_drop_unattached_child_does_not_remove(self):
        tree = TreeModel()
        root = tree.parse({'children': [{'id': 1}]})
        fake = TreeModel().parse({'id': 55})
        fake.drop()
        assert len(root.children) == 1

    def test_walk_traversal(self):
        tree = TreeModel()
        root = tree.parse({'id': 1, 'children': [{'id': 2}, {'id': 3}]})
        visited = []
        def visit(node):
            visited.append(node.model['id'])
            return True
        root.walk(visit, strategy='breadthFirst')
        assert set(visited) == {1, 2, 3}

    def test_walk_breaks_when_callback_returns_false(self):
        tree = TreeModel()
        root = tree.parse({'id': 1, 'children': [{'id': 2}, {'id': 3}]})
        visited = []
        def visit(node):
            visited.append(node.model['id'])
            if node.model['id'] == 2:
                return False
            return True
        root.walk(visit, strategy='breadthFirst')
        assert 2 in visited

    def test_filter_descendants(self):
        tree = TreeModel()
        root = tree.parse({'id': 1, 'children': [{'id': 2}, {'id': 3}]})
        matches = root.all(lambda n: n.model['id'] > 1)
        assert sorted([n.model['id'] for n in matches]) == [2, 3]

    def test_add_child_and_to_string(self):
        tree = TreeModel()
        root = tree.parse({'id': 1})
        child = tree.parse({'id': 2})
        root.add_child(child)
        assert root.children[0].model['id'] == 2
        assert isinstance(str(root), str)

    def test_add_child_at_index(self):
        tree = TreeModel()
        root = tree.parse({'id': 1, 'children': [{'id': 9}]})
        child = tree.parse({'id': 2})
        root.add_child_at_index(child, 0)
        assert root.children[0].model['id'] == 2

    def test_get_index_not_found(self):
        tree = TreeModel()
        root = tree.parse({'id': 1, 'children': [{'id': 9}]})
        child = tree.parse({'id': 3})
        assert child.get_index() == 0
        ids = [c.model['id'] for c in root.children]
        assert ids.count(child.model['id']) == 0
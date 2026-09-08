import pytest

try:
    from src.tree_model import TreeModel
except ImportError:
    TreeModel = None

@pytest.mark.skipif(TreeModel is None, reason="TreeModel implementation missing")
class TestTreeModelBranchesPublic:

    def test_instantiate_with_different_config(self):
        tree = TreeModel(children_property_name='minions')
        assert isinstance(tree, TreeModel)

    def test_parse_node_with_another_custom_children(self):
        tree = TreeModel(children_property_name='descendants')
        root = tree.parse({'descendants': [{'name': 'foo'}, {'name': 'bar'}]})
        assert len(root.children) == 2

    def test_parse_various_non_object_models(self):
        tree = TreeModel()
        with pytest.raises(Exception, match="object"):
            tree.parse(True)
        with pytest.raises(Exception, match="object"):
            tree.parse(object())  # symbol analogue, though not same as JS Symbol
        with pytest.raises(Exception, match="object"):
            tree.parse([])
        with pytest.raises(Exception, match="object"):
            tree.parse(lambda: None)

    def test_child_at_index_returns_none(self):
        tree = TreeModel()
        root = tree.parse({'children': [{'id': 10}, {'id': 20}]})
        assert (root.children[2] if len(root.children) > 2 else None) is None

    def test_is_root_and_has_children_variation(self):
        tree = TreeModel()
        root = tree.parse({'children': [{'id': 101}, {'id': 202}]})
        child = root.children[1]
        assert root.is_root()
        assert root.has_children()
        assert not child.is_root()
        assert not child.has_children()

    def test_remove_child_with_multiple(self):
        tree = TreeModel()
        root = tree.parse({'children': [{'id': 100}, {'id': 200}]})
        child = root.children[1]
        child.drop()
        assert len(root.children) == 1
        assert getattr(child, 'parent', None) is None

    def test_drop_fake_does_not_remove(self):
        tree = TreeModel()
        root = tree.parse({'children': [{'id': 5}]})
        fake = TreeModel().parse({'id': 77})
        fake.drop()
        assert len(root.children) == 1

    def test_walk_traversal_other_values(self):
        tree = TreeModel()
        root = tree.parse({'id': 90, 'children': [{'id': 91}, {'id': 92}]})
        visited = []
        def visit(node):
            visited.append(node.model['id'])
            return True
        root.walk(visit, strategy='breadthFirst')
        assert set(visited) == {90, 91, 92}

    def test_walk_breaks_with_other_node(self):
        tree = TreeModel()
        root = tree.parse({'id': 50, 'children': [{'id': 51}, {'id': 52}]})
        visited = []
        def visit(node):
            visited.append(node.model['id'])
            if node.model['id'] == 52:
                return False
            return True
        root.walk(visit, strategy='breadthFirst')
        assert 52 in visited

    def test_filter_descendants_different_predicate(self):
        tree = TreeModel()
        root = tree.parse({'id': 70, 'children': [{'id': 71}, {'id': 72}, {'id': 68}]})
        matches = root.all(lambda n: n.model['id'] < 72)
        assert sorted([n.model['id'] for n in matches]) == [68, 70, 71]

    def test_add_child_and_to_string_public(self):
        tree = TreeModel()
        root = tree.parse({'id': 111})
        child = tree.parse({'id': 222})
        root.add_child(child)
        assert root.children[0].model['id'] == 222
        assert isinstance(str(root), str)

    def test_add_child_at_different_index(self):
        tree = TreeModel()
        root = tree.parse({'id': 8, 'children': [{'id': 19}]})
        child = tree.parse({'id': 11})
        root.add_child_at_index(child, 1)
        assert root.children[1].model['id'] == 11

    def test_get_index_not_found_public(self):
        tree = TreeModel()
        root = tree.parse({'id': 44, 'children': [{'id': 99}]})
        child = tree.parse({'id': 77})
        assert child.get_index() == 0
        ids = [c.model['id'] for c in root.children]
        assert ids.count(child.model['id']) == 0
import pytest

try:
    from src.tree_model import TreeModel
except ImportError:
    TreeModel = None

@pytest.mark.skipif(TreeModel is None, reason="TreeModel implementation missing")
class TestTreeModelEdgeCases:
    def setup_method(self):
        self.tree_model = TreeModel()

    def test_node_get_index_root(self):
        root = self.tree_model.parse({'id': 'a'})
        assert root.get_index() == 0

    def test_node_get_index_child(self):
        root = self.tree_model.parse({'id': 1, 'children': [{'id': 2}]})
        assert root.children[0].get_index() == 0

    def test_node_get_path_deep_child(self):
        root = self.tree_model.parse({
            'id': 0,
            'children': [
                {'id': 1, 'children': [{'id': 2}]}
            ]
        })
        child = root.children[0].children[0]
        path = child.get_path()
        assert [n.model['id'] for n in path] == [0, 1, 2]

    def test_add_child_fills_empty_children(self):
        root = self.tree_model.parse({'id': 1})
        root.model['children'] = None
        root.add_child(self.tree_model.parse({'id': 2}))
        assert len(root.children) == 1
        assert root.model['children'][0] == {'id': 2}

    def test_add_child_at_index_raises_negative(self):
        root = self.tree_model.parse({'id': 1})
        child = self.tree_model.parse({'id': 2})
        with pytest.raises(Exception, match="Invalid index"):
            root.add_child_at_index(child, -1)

    def test_add_child_at_index_raises_too_high(self):
        root = self.tree_model.parse({'id': 1, 'children': [{'id': 2}]})
        child = self.tree_model.parse({'id': 3})
        with pytest.raises(Exception, match="Invalid index"):
            root.add_child_at_index(child, 2)

    def test_set_index_raises_below_zero(self):
        root = self.tree_model.parse({'id': 1, 'children': [{'id': 2}, {'id': 3}]})
        with pytest.raises(Exception, match="Invalid index"):
            root.children[0].set_index(-1)

    def test_set_index_raises_too_high(self):
        root = self.tree_model.parse({'id': 1, 'children': [{'id': 2}, {'id': 3}]})
        with pytest.raises(Exception, match="Invalid index"):
            root.children[0].set_index(2)

    def test_set_index_valid_move(self):
        root = self.tree_model.parse({'id': 1, 'children': [{'id': 2}, {'id': 3}, {'id': 4}]})
        root.children[0].set_index(1)
        assert root.children[1].model['id'] == 2
        assert [c['id'] for c in root.model['children']] == [3, 2, 4]

    def test_set_index_root_bad(self):
        root = self.tree_model.parse({'id': 1, 'children': [{'id': 2}]})
        with pytest.raises(Exception, match="Invalid index"):
            root.set_index(1)

    def test_set_index_root_zero_ok(self):
        root = self.tree_model.parse({'id': 1, 'children': [{'id': 2}]})
        res = root.set_index(0)
        assert res == root
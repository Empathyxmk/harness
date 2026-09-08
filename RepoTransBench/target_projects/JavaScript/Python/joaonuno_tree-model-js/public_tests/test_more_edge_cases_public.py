import pytest

try:
    from src.tree_model import TreeModel
except ImportError:
    TreeModel = None

@pytest.mark.skipif(TreeModel is None, reason="TreeModel implementation missing")
class TestTreeModelEdgeCasesPublic:
    def setup_method(self):
        self.tree_model = TreeModel()

    def test_get_index_root_different_id(self):
        root = self.tree_model.parse({'id': 'z'})
        assert root.get_index() == 0

    def test_get_index_child_other_values(self):
        root = self.tree_model.parse({'id': 3, 'children': [{'id': 4}]})
        assert root.children[0].get_index() == 0

    def test_get_path_another_deep_child(self):
        root = self.tree_model.parse({
            'id': 5,
            'children': [
                {'id': 6, 'children': [{'id': 7}]}
            ]
        })
        child = root.children[0].children[0]
        path = child.get_path()
        assert [n.model['id'] for n in path] == [5, 6, 7]

    def test_add_child_fills_empty_children_public(self):
        root = self.tree_model.parse({'id': 10})
        root.model['children'] = None
        root.add_child(self.tree_model.parse({'id': 20}))
        assert len(root.children) == 1
        assert root.model['children'][0] == {'id': 20}

    def test_add_child_at_index_raises_negative_public(self):
        root = self.tree_model.parse({'id': 100})
        child = self.tree_model.parse({'id': 101})
        with pytest.raises(Exception, match="Invalid index"):
            root.add_child_at_index(child, -2)

    def test_add_child_at_index_raises_too_high_public(self):
        root = self.tree_model.parse({'id': 21, 'children': [{'id': 22}]})
        child = self.tree_model.parse({'id': 23})
        with pytest.raises(Exception, match="Invalid index"):
            root.add_child_at_index(child, 3)

    def test_set_index_raises_below_zero_public(self):
        root = self.tree_model.parse({'id': 99, 'children': [{'id': 98}, {'id': 97}]})
        with pytest.raises(Exception, match="Invalid index"):
            root.children[0].set_index(-7)

    def test_set_index_raises_too_high_public(self):
        root = self.tree_model.parse({'id': 83, 'children': [{'id': 84}, {'id': 85}]})
        with pytest.raises(Exception, match="Invalid index"):
            root.children[0].set_index(2)

    def test_set_index_valid_move_public(self):
        root = self.tree_model.parse({'id': 50, 'children': [{'id': 51}, {'id': 52}, {'id': 53}]})
        root.children[1].set_index(0)
        assert root.children[0].model['id'] == 52
        assert [c['id'] for c in root.model['children']] == [52, 51, 53]

    def test_set_index_root_bad_public(self):
        root = self.tree_model.parse({'id': 75, 'children': [{'id': 76}]})
        with pytest.raises(Exception, match="Invalid index"):
            root.set_index(5)

    def test_set_index_root_zero_ok_public(self):
        root = self.tree_model.parse({'id': 60, 'children': [{'id': 61}]})
        res = root.set_index(0)
        assert res == root
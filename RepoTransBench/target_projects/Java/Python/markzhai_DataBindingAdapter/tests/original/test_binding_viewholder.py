import pytest
from unittest import mock

class ViewDataBinding:
    def getRoot(self):
        return None

class BindingViewHolder:
    def __init__(self, binding):
        self._binding = binding

    def getBinding(self):
        return self._binding

@pytest.fixture
def setup_binding_viewholder():
    view = mock.Mock()
    binding = mock.Mock(spec=ViewDataBinding)
    binding.getRoot.return_value = view
    return binding, view

def test_get_binding(setup_binding_viewholder):
    binding, _ = setup_binding_viewholder
    holder = BindingViewHolder(binding)
    assert holder.getBinding() == binding
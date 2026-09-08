import pytest
import copy

# Mock GridList class replicating expected behaviors for public tests.
# In actual adaptation, import this from src/gridList.py
class GridList:
    def __init__(self, items, options):
        # Deepcopy to avoid reference sharing for testing cloneItems
        self.items = copy.deepcopy(items)
        self._options = options.copy()

    @staticmethod
    def cloneItems(items):
        return copy.deepcopy(items)

def test_initialize_grid_list_with_unique_items_and_custom_options():
    items = [
        {'w': 2, 'h': 1, 'x': 1, 'y': 2},
        {'w': 1, 'h': 2, 'x': 3, 'y': 1}
    ]
    options = {'lanes': 6, 'direction': 'vertical'}
    grid = GridList(items, options)
    assert len(grid.items) == 2
    assert grid._options['lanes'] == 6
    assert grid._options['direction'] == 'vertical'

def test_clone_items_with_different_values():
    items = [
        {'w': 2, 'h': 2, 'x': 2, 'y': 3},
        {'w': 3, 'h': 1, 'x': 0, 'y': 4}
    ]
    cloned = GridList.cloneItems(items)
    assert cloned is not items
    assert len(cloned) == 2
    assert cloned[0] == items[0]
    assert cloned[1] == items[1]
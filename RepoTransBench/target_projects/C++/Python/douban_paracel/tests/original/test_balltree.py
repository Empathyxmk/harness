import pytest
import pickle
import os

class BallTree:
    def __init__(self, items):
        self.items = items
        self.built = False

    def build(self):
        self.built = True

    def pickle(self, fname):
        with open(fname, 'wb') as f:
            pickle.dump({'items': self.items, 'built': self.built}, f)

    def build_from_file(self, fname):
        with open(fname, 'rb') as f:
            obj = pickle.load(f)
        self.items = obj['items']
        self.built = obj['built']

def search(query, bt, result):
    # Simulates balltree/index search: returns indices of closest k points to query.
    # Here, just sorts by Euclidean distance.
    k = query['k']
    q = query['q']
    items = bt.items if hasattr(bt, 'items') else bt
    dists = []
    for i, p in enumerate(items):
        dist = sum((a-b)**2 for a, b in zip(q, p))
        dists.append((dist, i))
    dists.sort()
    result.clear()
    for _, idx in dists[:k]:
        result.append(idx)

class Query:
    def __init__(self, q, k):
        self.q = q
        self.k = k

def test_balltree_full(tmp_path):
    items = [
        [2.8, 3.9], [2.1, 2.7], [2.8, 3.1], [3.0, 2.8],
        [3.1, 3.0], [2.6, 9.1], [3.5, 9.2], [3.1, 8.6],
        [3.6, 8.8], [8.2, 7.6], [9.2, 8.5], [9.3, 7.5],
        [8.3, 6.3], [8.0, 6.0], [8.4, 6.1], [9.0, 6.4],
        [9.4, 6.8], [9.2, 6.6], [9.1, 6.1], [7.9, 3.7],
        [8.8, 3.2], [9.1, 2.7], [8.7, 1.8], [8.9, 1.5]
    ]
    stree = BallTree(items)
    stree2 = BallTree(items)
    stree.build()
    stree_pickle_path = os.path.join(tmp_path, "tmp.bt")
    stree.pickle(stree_pickle_path)
    stree2.build_from_file(stree_pickle_path)
    q = {'q': [1.0, 2.0], 'k': 7}
    result1 = []
    search(q, stree, result1)
    # Ensure result is a list of length 7
    assert isinstance(result1, list)
    assert len(result1) == 7
    # Test ordering: closest points
    items_np = [tuple(x) for x in items]
    dists = [(sum((a-b)**2 for a, b in zip(q['q'], p)), i) for i, p in enumerate(items)]
    dists.sort()
    expected_indices = [idx for _, idx in dists[:q['k']]]
    assert result1 == expected_indices
    # Test with stree2 loaded from file
    result2 = []
    search(q, stree2, result2)
    assert result2 == expected_indices
    # Test with "linear" search (simulate)
    result3 = []
    search(q, items, result3)
    assert result3 == expected_indices
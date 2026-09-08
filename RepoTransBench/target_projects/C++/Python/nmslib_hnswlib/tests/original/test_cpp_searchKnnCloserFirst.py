import unittest
import numpy as np

class TestSearchKnnCloserFirst(unittest.TestCase):
    def test_search_knn_closer_first(self):
        try:
            import hnswlib
        except ImportError:
            self.skipTest("hnswlib Python package is not installed")
            return

        d = 4
        n = 100
        nq = 10
        k = 10

        np.random.seed(47)
        data = np.random.rand(n, d).astype(np.float32)
        query = np.random.rand(nq, d).astype(np.float32)

        # Brute-force: compute all distances and sort for top-k nearest
        bf_labels = []
        for qv in query:
            dists = np.linalg.norm(data - qv, axis=1)
            bf_labels.append(np.argsort(dists)[:k])
        bf_labels = np.array(bf_labels)

        # HNSWlib index
        index = hnswlib.Index(space='l2', dim=d)
        index.init_index(max_elements=n, ef_construction=100, M=16)
        index.add_items(data)
        index.set_ef(50)
        labels, distances = index.knn_query(query, k=k)

        n_correct = 0
        for brute, hnsw in zip(bf_labels, labels):
            n_correct += len(set(brute.tolist()) & set(hnsw.tolist()))
        total = nq * k
        # HNSW is not always perfect; allow at least 80% recall relative to brute-force baseline
        self.assertGreaterEqual(n_correct, int(0.8 * total),
                                f"HNSW found only {n_correct} of {total} brute-force neighbors")
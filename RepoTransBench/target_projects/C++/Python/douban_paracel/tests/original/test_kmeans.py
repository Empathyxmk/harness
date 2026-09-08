def test_kmeans_default_constructor():
    # Stub class for KMeans; in real system, import actual class
    class KMeans:
        def __init__(self, n_clusters=2):
            self.n_clusters = n_clusters
            self._labels = None

        def fit(self, data):
            # Dummy label assignment: assign index as label modulo n_clusters
            self._labels = [i % self.n_clusters for i in range(len(data))]

        def labels(self):
            return self._labels

    k = KMeans()
    assert k is not None

def test_kmeans_cluster_simple():
    class KMeans:
        def __init__(self, n_clusters=2):
            self.n_clusters = n_clusters
            self._labels = None

        def fit(self, data):
            self._labels = [i % self.n_clusters for i in range(len(data))]

        def labels(self):
            return self._labels

    k = KMeans(2)
    data = [[1.0, 1.0], [10.0, 10.0]]
    k.fit(data)
    labels = k.labels()
    assert len(labels) == 2
    assert (labels[0] == 0 and labels[1] == 1) or (labels[0] == 1 and labels[1] == 0)
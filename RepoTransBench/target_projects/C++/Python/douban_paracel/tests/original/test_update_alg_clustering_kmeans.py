def local_update_kmeans_clusters_stl(a, b):
    # a and b are list of list of floats, same size
    return [
        [a[i][j] + b[i][j] for j in range(len(a[0]))]
        for i in range(len(a))
    ]

def local_update_kmeans_groups_stl(a, b):
    # a and b are dict<int, list<str>>
    from collections import defaultdict
    c = defaultdict(list)
    for k, v in a.items():
        c[k].extend(v)
    for k, v in b.items():
        c[k].extend(v)
    return c

def test_clusters_sum():
    a = [[1.0, 2.5], [3.0, 4.0]]
    b = [[0.5, 1.5], [2.0, 0.0]]
    r = local_update_kmeans_clusters_stl(a, b)
    assert r[0][0] == 1.5
    assert r[0][1] == 4.0
    assert r[1][0] == 5.0
    assert r[1][1] == 4.0

def test_groups_merge():
    a = {0: ["a", "b"], 1: ["c"]}
    b = {1: ["d", "e"], 2: ["f"]}
    c = local_update_kmeans_groups_stl(a, b)
    assert len(c[0]) == 2
    assert len(c[1]) == 3   # "c", "d", "e"
    assert len(c[2]) == 1   # "f"
    assert c[2][0] == "f"
    assert c[1][0] == "c"
    assert c[1][1] == "d"
    assert c[1][2] == "e"

def test_groups_merge_empty_a():
    a = {}
    b = {3: ["x", "y"]}
    c = local_update_kmeans_groups_stl(a, b)
    assert len(c[3]) == 2
    assert c[3][0] == "x"
    assert c[3][1] == "y"
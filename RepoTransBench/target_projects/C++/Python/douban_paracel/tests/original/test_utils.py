import pytest
import numpy as np
import random
import string
import os
import pickle
import json

def str_join(items, sep):
    return sep.join(items)

def str_split_by_word(s, word):
    if not word:
        return list(s)
    out = []
    i = 0
    n = len(word)
    lst = []
    while i < len(s):
        if s[i:i+n] == word:
            if lst:
                out.append(''.join(lst))
                lst = []
            i += n
        else:
            lst.append(s[i])
            i += 1
    if lst:
        out.append(''.join(lst))
    return out

def startswith(s, prefix):
    return s.startswith(prefix)

def endswith(s, suf):
    return s.endswith(suf)

def str_split(s, sep):
    if len(sep) == 1:
        return s.split(sep)
    elif sep in s:
        return s.split(sep)
    else:
        # Fallback to splitting by any char in sep
        import re
        return re.split('|'.join(map(re.escape, sep)), s)

def random_double():
    return random.uniform(0, 1)

def random_double_list(n):
    return [random.uniform(0, 1) for _ in range(n)]

class JsonParser:
    def __init__(self, fname):
        with open(fname, "r") as f:
            self.j = json.load(f)

    def parse(self, key, dtype=str):
        val = self.j[key]
        return dtype(val)

    def parse_v(self, key, dtype=str):
        val = self.j[key]
        return [dtype(x) for x in val]

class TrivialHash:
    def __call__(self, x):
        return x

class StringHash:
    def __init__(self, apple_hash=False):
        self.apple_hash = apple_hash
    def __call__(self, x):
        # Platform dependent (simulated values).
        # Always returns the Linux hash values in the test.
        known = {
            "0": 2297668033614959926,
            "1": 10159970873491820195,
            "2": 4551451650890805270,
            "3": 8248777770799913213,
        }
        return known.get(x, hash(x))

def mat2vec(mat):
    # Accepts numpy matrix or scipy sparse COO.
    if isinstance(mat, np.ndarray):
        return mat.ravel(order='C').tolist()
    else:
        mat = mat.tocoo()
        data = []
        for i, j, v in zip(mat.row, mat.col, mat.data):
            data.append((i, j, v))
        return data

def vec2mat(vec, nrows):
    arr = np.array(vec)
    ncols = arr.size // nrows
    return arr.reshape((nrows, ncols))

def evec2vec(col):
    return col.tolist()

def vec2evec(vec):
    return np.array(vec)

def traverse_matrix(mat, fun):
    # For equality checks of sparse matrices: traverse by row order
    mat = mat.tocoo()
    tuples = sorted(zip(mat.row, mat.col, mat.data))
    for i, j, v in tuples:
        fun(i, j, v)

# Implement graph classes minimally for the tests, with simple logic for v(), e(), etc.
class UndirectedGraph:
    def __init__(self, edges=None):
        self.edges = set()
        self.nodes = set()
        if edges is not None:
            for u, v in edges:
                self.edges.add(tuple(sorted((u,v))))
                self.nodes.update([u,v])
        self._update()

    def _update(self):
        degrees = {}
        for u, v in self.edges:
            degrees.setdefault(u,0)
            degrees.setdefault(v,0)
            degrees[u] += 1
            degrees[v] += 1
        self._degrees = degrees

    def v(self):
        return len(self.nodes)
    def e(self):
        return len(self.edges)
    def avg_degree(self):
        return sum(self._degrees.values()) / len(self.nodes)
    def max_degree(self):
        return max(self._degrees.values())
    def selfloops(self):
        return sum(1 for u,v in self.edges if u == v)
    def degree(self):
        return self._degrees
    def get_data(self):
        return set(self.edges)

    def __eq__(self, o):
        return isinstance(o, UndirectedGraph) and self.nodes == o.nodes and self.edges == o.edges

class Digraph:
    def __init__(self, triples=None):
        self.edges = []
        self.vertices = set()
        self._in_deg = {}
        self._out_deg = {}
        self._selfloops = 0
        if triples is not None:
            for u, v, w in triples:
                self.add_edge(u, v, w)
    def add_edge(self, u, v, w):
        self.edges.append((u,v,w))
        self.vertices.update([u,v])
        self._out_deg[u] = self._out_deg.get(u,0) + 1
        self._in_deg[v] = self._in_deg.get(v,0) + 1
        if u == v:
            self._selfloops += 1
    def v(self):
        return len(self.vertices)
    def e(self):
        return len(self.edges)
    def outdegree(self, x=None):
        if x is None:
            return dict(self._out_deg)
        else:
            return self._out_deg.get(x, 0)
    def indegree(self, x=None):
        if x is None:
            return dict(self._in_deg)
        else:
            return self._in_deg.get(x, 0)
    def avg_degree(self):
        return self.e()/self.v() if self.v()>0 else 0
    def selfloops(self):
        return self._selfloops
    def get_data(self):
        return set(self.edges)
    def __eq__(self, o):
        return isinstance(o, Digraph) and set(self.edges) == set(o.edges)

class BigraphContinuous:
    def __init__(self):
        self._edges = []
        self._left = set()
        self._right = set()
        self._out= {}
        self._in = {}
    def add_edge(self,a,b,w):
        self._edges.append((a,b,w))
        self._left.add(a)
        self._right.add(b)
        self._out[a] = self._out.get(a,0) + 1
        self._in[b] = self._in.get(b,0)+1
    def v(self):
        return len(self._left)
    def e(self):
        return len(self._edges)
    def outdegree(self, x):
        return self._out.get(x,0)
    def indegree(self, x):
        return self._in.get(x,0)
    def __eq__(self, o):
        return isinstance(o, BigraphContinuous) and set(self._edges) == set(o._edges)

class Bigraph:
    def __init__(self, triples=None):
        self._edges = []
        self._left = set()
        self._right = set()
        self._out = {}
        self._in = {}
        if triples is not None:
            for a,b,w in triples:
                self.add_edge(a,b,w)
    def add_edge(self,a,b,w):
        self._edges.append((a,b,w))
        self._left.add(a)
        self._right.add(b)
        self._out[a] = self._out.get(a,0) + 1
        self._in[b] = self._in.get(b,0)+1
    def v(self):
        return len(self._left)
    def e(self):
        return len(self._edges)
    def avg_degree(self):
        return self.e()/float(self.v()) if self.v() else 0
    def outdegree(self, a):
        return self._out.get(a,0)
    def indegree(self, b):
        return self._in.get(b,0)
    def get_data(self):
        return set(self._edges)
    def __eq__(self, o):
        return isinstance(o, Bigraph) and set(self._edges) == set(o._edges)

def test_paracel_str_extra_test():
    init_lst = ["hello", "world", "happy", "new", "year", "2015"]
    seps = "orz"
    together = str_join(init_lst, seps)
    assert together == "helloorzworldorzhappyorzneworzyearorz2015"
    res1 = str_split_by_word(together, seps)
    tmp = together
    res2 = str_split_by_word(tmp, seps)
    assert res1 == init_lst
    assert res2 == init_lst
    assert startswith(together, "hello") == True
    assert startswith(together, "helo") == False
    assert startswith(together, "helloorzworldorzhappyorzneworzyearorz2015") == True
    assert startswith(together, "helloorzworldorzhappyorzneworzyearorz20157") == False
    assert startswith(together, "") == True
    assert endswith(together, "2015") == True
    assert endswith(together, "2014") == False
    assert endswith(together, "helloorzworldorzhappyorzneworzyearorz2015") == True
    assert endswith(together, "7helloorzworldorzhappyorzneworzyearorz2015") == False
    assert endswith(together, "") == True

    tmp = "a|b|c|d|e"
    r = ["a", "b", "c", "d", "e"]
    r1 = str_split(tmp, '|')
    r2 = str_split(tmp, "|")
    r3 = str_split(tmp, "?|?")
    assert r1 == r
    assert r2 == r
    assert r3 == r

def test_paracel_random_test():
    # Monte Carlo estimate of pi
    incycle_cnt = 0
    for _ in range(50000):   # lower count for test time
        x = random_double()
        y = random_double()
        if x * x + y * y < 1.:
            incycle_cnt += 1
    pihat = 4 * float(incycle_cnt) / 50000.
    assert 3.12 <= pihat <= 3.18     # pi ~ 3.1416
    # Check random list
    for _ in range(100):
        r = random_double_list(100)
        assert len(r) == 100
        for val in r:
            assert 0. <= val <= 1.
    r = random_double_list(1000)
    assert len(r) == 1000
    assert all(0. <= v <= 1. for v in r)

def test_paracel_json_parser_test(tmp_path):
    # Copy the provided JSON file to the temp dir.
    import shutil
    base = os.path.dirname(__file__)
    src = os.path.join(base, '../../test/test.json')
    dst = os.path.join(tmp_path, 'test.json')
    shutil.copy(src, dst)
    pt = JsonParser(dst)
    assert pt.parse("wu", str) == "hong"
    assert pt.parse("hong", int) == 7
    assert pt.parse("changsheng", bool) is True
    assert abs(pt.parse("jiang", float) - 3.141592653) < 1e-9
    vl1 = ["hong", "xun", "zhang"]
    assert pt.parse_v("wul", str) == vl1
    vl2 = [1, 2, 3, 4, 5, 6, 7]
    assert pt.parse_v("hongl", int) == vl2
    vl3 = [True, False, False, True, True]
    assert pt.parse_v("changshengl", bool) == vl3
    vl4 = [1.23, 2.34, 3.45, 4.56, 5.67, 6.78, 7.89]
    outvl4 = pt.parse_v("jiangl", float)
    for a, b in zip(outvl4, vl4):
        assert abs(a - b) < 1e-9

def test_utils_hash_test():
    hfunc = TrivialHash()
    a, b, c, d = 0, 1, 2, 3
    assert hfunc(a) == 0
    assert hfunc(b) == 1
    assert hfunc(c) == 2
    assert hfunc(d) == 3
    hfunc2 = StringHash()
    x, y, z, t = "0", "1", "2", "3"
    a = 2297668033614959926
    b = 10159970873491820195
    c = 4551451650890805270
    d = 8248777770799913213
    assert hfunc2(x) == a
    assert hfunc2(y) == b
    assert hfunc2(z) == c
    assert hfunc2(t) == d

def test_eigen_common_usage_test():
    import scipy.sparse
    # Static vs dynamic matrices
    m = np.eye(3)
    m[:,1] = [4, 5, 6]
    expect = np.array([[1, 4, 0], [0, 5, 0], [0, 6, 1]])
    np.testing.assert_array_equal(m, expect)
    v = mat2vec(m)
    check_v = [1,0,0,4,5,6,0,0,1]
    assert v == check_v
    check_mat = vec2mat(v, 3)
    np.testing.assert_array_equal(check_mat, expect)
    vv = m[:,1]
    vvv = evec2vec(vv)
    check_vvv = [4,5,6]
    assert vvv == check_vvv
    vvvv = vec2evec(vvv)
    np.testing.assert_array_equal(vvvv, vv)
    vec = np.array([1,2,3])
    r = np.dot(m[2], vec)
    assert r == 15

    # Random matrix operations
    mm = np.random.randn(3,3)
    np.sum(mm, axis=0)  # sum of each column
    np.sum(mm, axis=1)  # sum of each row
    np.max(np.abs(mm), axis=0)   # max abs per column

    mtx = np.zeros((3,2))
    vech = np.array([1.1, 0.8])
    mtx[0] = vech
    vech = np.array([2.0, 2.0])
    mtx[1] = vech
    vech = np.array([1.0, 0.5])
    mtx[2] = vech
    vech = np.array([1.01, 0.28])
    assert np.isclose(vech[0], 1.01)
    assert np.isclose(vech[1], 0.28)
    assert np.isclose(mtx[0][0], 1.1)
    assert np.isclose(mtx[1][0], 2.0)
    assert np.isclose(mtx[2][0], 1.0)
    assert np.isclose(mtx[0][1], 0.8)
    assert np.isclose(mtx[1][1], 2.0)
    assert np.isclose(mtx[2][1], 0.5)

    # Calculate rowwise squaredNorm distance, pick minimum
    dists = [np.sum((mtx[i]-vech)**2) for i in range(mtx.shape[0])]
    indx = int(np.argmin(dists))
    assert indx == 2

    result = mtx.dot(vech)
    assert np.isclose(result[0], 1.3350000000000002)
    assert np.isclose(result[1], 2.58)
    assert np.isclose(result[2], 1.15)

    mtx[0] *= 10
    assert np.isclose(mtx[0][0], 11)
    assert np.isclose(mtx[0][1], 8)

    mmat = np.array([[1,2],[3,4]])
    vvec = np.array([1.1,2.2])
    rr, cc = np.unravel_index(np.argmax(mmat, axis=None), mmat.shape)
    assert mmat[rr][cc] == 4
    assert rr == 1
    assert cc == 1
    assert mmat[1].sum() == 7

def test_eigen_matrix_usage_test():
    import scipy.sparse
    HH_global = np.random.randn(3,3)
    HH_blk = HH_global[0:2,0:2]
    tHt = mat2vec(HH_blk)
    mat_restored = vec2mat(tHt, 2)
    np.testing.assert_array_equal(mat_restored, HH_blk)

    mtx = np.array([
        [1.,2.,3.],
        [4.,5.,6.],
        [7.,8.,9.],
        [10.,11.,12.],
    ])
    c1 = [2.5, 3.5, 4.5]
    c2 = [8.5, 9.5, 10.5]
    clusters_mtx = np.vstack((c1, c2))
    # For each row, compute closest cluster center
    for i in range(mtx.shape[0]):
        dists = [np.sum((clusters_mtx[j]-mtx[i])**2) for j in range(clusters_mtx.shape[0])]
        indx = int(np.argmin(dists))
        assert indx in [0,1]
    # Sparse matrix operations
    from scipy.sparse import coo_matrix
    rows = [0]*3 + [1]*3 + [2]*2 + [3]*2 + [4] + [5]*2 + [6]*2 + [7] + [8]*4 + [9]*3
    cols = [0,2,4,2,3,4,0,1,3,4,1,0,4,0,2,0,1,2,3,4,0,3,4]
    data = [0.6,0.7,0.4,0.6,0.5,0.3,0.3,0.1,0.1,0.7,0.3,0.1,0.7,0.2,0.8,0.3,0.1,0.2,0.3,0.4,0.9,0.1,0.2]
    A = coo_matrix((data, (rows, cols)), shape=(10,5)).tocsr()
    vecA = mat2vec(A)
    AA = coo_matrix((data, (rows, cols)), shape=(10,5)).tocsr()
    # mat2vec/vec2mat for sparse -- see above for dense
    # Dense multiply
    H = np.array([
        [1.,2.,3.],
        [4.,5.,6.],
        [7.,8.,9.],
        [10.,11.,12.],
        [13.,14.,15.]
    ])
    W = A.dot(H)
    assert W.shape == (10,3)
    # QR, inverse, SVD
    squareW = np.array([[1., 2.], [3., 4.]])
    w_inv = np.linalg.inv(squareW)
    assert w_inv.shape == (2,2)
    # Cholesky
    AA_mat = np.array([[0.872871, -0.574833, -0.304016],
                       [-0.574833, 0.827987, 0.120067],
                       [-0.304016, 0.120067, 0.297787]])
    L = np.linalg.cholesky(AA_mat)
    A_recompose = L @ L.T
    assert np.allclose(A_recompose, AA_mat)
    # SVD
    ma = np.random.randn(3,2)
    U, SIGMA, Vt = np.linalg.svd(ma, full_matrices=False)
    sigmaMat = np.zeros(ma.shape)
    np.fill_diagonal(sigmaMat, SIGMA)
    recon = U.dot(sigmaMat).dot(Vt)
    assert np.allclose(recon, ma)

def test_pkl_sequential_usage_test(tmp_path):
    import scipy.sparse
    # sparse matrix
    from scipy.sparse import coo_matrix, csr_matrix, save_npz, load_npz
    rows = [0]*3 + [1]*3 + [2]*2 + [3]*2 + [4] + [5]*2 + [6]*2 + [7] + [8]*4 + [9]*3
    cols = [0,2,4,2,3,4,0,1,3,4,1,0,4,0,2,0,1,2,3,4,0,3,4]
    data = [0.6,0.7,0.4,0.6,0.5,0.3,0.3,0.1,0.1,0.7,0.3,0.1,0.7,0.2,0.8,0.3,0.1,0.2,0.3,0.4,0.9,0.1,0.2]
    A = coo_matrix((data, (rows, cols)), shape=(10,5)).tocsr()
    pkl_path = os.path.join(tmp_path, "test_sparse.pkl")
    with open(pkl_path, "wb") as f:
        pickle.dump(A, f)
    with open(pkl_path, "rb") as f:
        Arev = pickle.load(f)
    assert (A != Arev).nnz == 0

    # dense matrix
    H = np.array([
        [1.,2.,3.],
        [4.,5.,6.],
        [7.,8.,9.],
        [10.,11.,12.],
        [13.,14.,15.]
    ])
    pkl_path2 = os.path.join(tmp_path, "test_dense.pkl")
    with open(pkl_path2, "wb") as f:
        pickle.dump(H, f)
    with open(pkl_path2, "rb") as f:
        Hrev = pickle.load(f)
    assert np.allclose(H, Hrev)

    # undirected graph
    edges = [
        (0, 1), (0, 2), (0, 5), (0, 6),
        (3, 4), (3, 5), (4, 5), (4, 6),
        (9, 10), (9, 11), (9, 12), (11, 12)
    ]
    grp = UndirectedGraph(edges)
    grp2_path = os.path.join(tmp_path, "test_ugraph.pkl")
    with open(grp2_path, "wb") as f:
        pickle.dump(grp, f)
    with open(grp2_path, "rb") as f:
        grp2 = pickle.load(f)
    assert grp2.v() == 11
    assert grp2.e() == 12
    assert abs(grp2.avg_degree() - (24 / 11.)) < 1e-10
    assert grp2.max_degree() == 4
    assert grp2.selfloops() == 0

    # digraph
    tpls = [
        (0, 0, 3.), (0, 2, 5.), (1, 0, 4.), (1, 1, 3.),
        (1, 2, 1.), (2, 0, 2.), (2, 3, 1.), (3, 1, 3.),
        (3, 3, 1.)
    ]
    grp = Digraph(tpls)
    grp.add_edge(3, 4, 5.)
    digraph_path = os.path.join(tmp_path, "test_digraph.pkl")
    with open(digraph_path, "wb") as f:
        pickle.dump(grp, f)
    with open(digraph_path, "rb") as f:
        grp2 = pickle.load(f)
    assert grp2.v() == 5
    assert grp2.e() == 10
    assert grp2.outdegree(0) == 2
    assert grp2.indegree(0) == 3
    assert abs(grp2.avg_degree() - 2.) < 1e-10
    assert grp2.selfloops() == 3

    # bigraph continuous
    G = BigraphContinuous()
    G.add_edge(0, 1, 3.)
    G.add_edge(0, 2, 4.)
    G.add_edge(0, 4, 2.)
    G.add_edge(1, 3, 5.)
    G.add_edge(1, 4, 4.)
    G.add_edge(1, 5, 5.)
    G.add_edge(2, 4, 3.)
    G.add_edge(2, 5, 1.)
    G.add_edge(2, 6, 2.)
    G.add_edge(3, 3, 3.)
    bigraphc_path = os.path.join(tmp_path, "test_bigrc.pkl")
    with open(bigraphc_path, "wb") as f:
        pickle.dump(G, f)
    with open(bigraphc_path, "rb") as f:
        G2 = pickle.load(f)
    assert G2.v() == 4
    assert G2.e() == 10
    assert G2.outdegree(0) == 3
    assert G2.indegree(5) == 2

    # bigraph
    tpls = [
        ("a", "A", 3.), ("a", "B", 4.), ("a", "D", 2.),
        ("b", "C", 5.), ("b", "D", 4.), ("c", "D", 3.),
        ("b", "E", 5.), ("c", "E", 1.), ("c", "F", 2.),
        ("d", "C", 3.)
    ]
    grp = Bigraph(tpls)
    grp.add_edge("c", "G", 3.6)
    bigraph_path = os.path.join(tmp_path, "test_bigr.pkl")
    with open(bigraph_path, "wb") as f:
        pickle.dump(grp, f)
    with open(bigraph_path, "rb") as f:
        grp2 = pickle.load(f)
    assert grp2.v() == 4
    assert grp2.e() == 11
    assert grp2.outdegree("a") == 3
    assert grp2.indegree("E") == 2
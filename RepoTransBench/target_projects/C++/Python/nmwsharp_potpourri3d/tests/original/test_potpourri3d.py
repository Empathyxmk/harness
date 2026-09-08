import os
import sys
import os.path as path 
import numpy as np
import scipy
import pytest

try:
    import potpourri3d as pp3d
except ImportError:
    import sys; sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)+"/../../src"))
    import potpourri3d as pp3d

asset_path = os.path.abspath(os.path.dirname(__file__))

def generate_verts(n_pts=999):
    np.random.seed(777)        
    return np.random.rand(n_pts, 3)

def generate_faces(n_pts=999):
    np.random.seed(777)        
    rand_faces = np.random.randint(0, n_pts, size=(2*n_pts,3))
    coverage_faces = np.arange(n_pts).reshape(-1, 3)
    faces = np.vstack((rand_faces, coverage_faces))
    return faces

def is_symmetric(A, eps=1e-6):
    resid = A - A.T
    return np.all(np.abs(resid.data) < eps)

def is_nonnegative(A, eps=1e-6):
    return np.all(A.data > -eps)

def test_write_read_mesh(tmp_path):
    for ext in ['obj']:
        V = generate_verts()
        F = generate_faces()
        fname = os.path.join(tmp_path, "test." + ext)
        pp3d.write_mesh(V,F,fname)
        Vnew, Fnew = pp3d.read_mesh(fname)
        assert np.amax(np.abs(V-Vnew)) < 1e-6
        assert (F==Fnew).all()
        # UV writes (smoke tests, output not parsed)
        UV_vert = V[:,:2]
        pp3d.write_mesh(V,F,fname,UV_coords=UV_vert, UV_type='per-vertex')
        UV_face = F[:,:2] * .3
        pp3d.write_mesh(V,F,fname,UV_coords=UV_face, UV_type='per-face')
        UV_corner = np.zeros((F.shape[0]*F.shape[1],2))
        pp3d.write_mesh(V,F,fname,UV_coords=UV_corner, UV_type='per-corner')

def test_write_read_point_cloud(tmp_path):
    for ext in ['obj', 'ply']:
        V = generate_verts()
        fname = os.path.join(tmp_path, "test_cloud." + ext)
        pp3d.write_point_cloud(V, fname)
        Vnew = pp3d.read_point_cloud(fname)
        assert np.amax(np.abs(V-Vnew)) < 1e-6

def test_mesh_heat_distance():
    V = generate_verts()
    F = generate_faces()
    solver = pp3d.MeshHeatMethodDistanceSolver(V,F)
    dist = solver.compute_distance(7)
    assert dist.shape[0] == V.shape[0]
    dist = solver.compute_distance_multisource([1,2,3])
    assert dist.shape[0] == V.shape[0]
    dist = pp3d.compute_distance(V,F,7)
    assert dist.shape[0] == V.shape[0]
    dist = pp3d.compute_distance_multisource(V,F,[1,3,4])
    assert dist.shape[0] == V.shape[0]

def test_mesh_vector_heat():
    V, F = pp3d.read_mesh(os.path.join(asset_path, "bunny_small.ply"))
    solver = pp3d.MeshVectorHeatSolver(V,F)
    ext = solver.extend_scalar([1, 22], [0., 6.])
    assert ext.shape[0] == V.shape[0]
    assert np.amin(ext) >= 0.
    basisX, basisY, basisN = solver.get_tangent_frames()
    assert basisX.shape[0] == V.shape[0]
    assert basisY.shape[0] == V.shape[0]
    assert basisN.shape[0] == V.shape[0]
    L_conn = solver.get_connection_laplacian()
    assert isinstance(L_conn, scipy.sparse.csc_matrix)
    max_diag_imag = np.max(np.abs(L_conn.diagonal().imag))
    assert max_diag_imag < 1e-4
    ext = solver.transport_tangent_vector(1, [6., 6.])
    assert ext.shape[0] == V.shape[0]
    assert ext.shape[1] == 2
    ext = solver.transport_tangent_vectors([1, 22], [[6., 6.], [3., 4.]])
    assert ext.shape[0] == V.shape[0]
    assert ext.shape[1] == 2
    logmap = solver.compute_log_map(1)
    assert logmap.shape[0] == V.shape[0]
    assert logmap.shape[1] == 2

def test_mesh_cotan_laplace():
    V, F = pp3d.read_mesh(os.path.join(asset_path, "bunny_small.ply"))
    L = pp3d.cotan_laplacian(V,F) 
    assert L.shape[0] == V.shape[0]
    assert L.shape[1] == V.shape[0]
    assert abs(np.sum(L)) < 1e-6

def test_mesh_areas():
    V, F = pp3d.read_mesh(os.path.join(asset_path, "bunny_small.ply"))
    face_area = pp3d.face_areas(V,F)
    assert face_area.shape[0] == F.shape[0]
    assert np.all(face_area >= 0)
    vert_area = pp3d.vertex_areas(V,F) 
    assert abs(np.sum(face_area) - np.sum(vert_area)) < 1e-6

def test_mesh_flip_geodesic():
    V, F = pp3d.read_mesh(os.path.join(asset_path, "bunny_small.ply"))
    path_solver = pp3d.EdgeFlipGeodesicSolver(V,F)
    path_pts = path_solver.find_geodesic_path(v_start=14, v_end=22)
    assert len(path_pts.shape) == 2
    assert path_pts.shape[1] == 3
    path_pts = path_solver.find_geodesic_path(v_start=14, v_end=22, max_iterations=100, max_relative_length_decrease=0.5)
    for i in range(5):
        path_pts = path_solver.find_geodesic_path(v_start=14, v_end=22+i)
        assert len(path_pts.shape) == 2
        assert path_pts.shape[1] == 3
    path_pts = path_solver.find_geodesic_path_poly([1173, 148, 870, 898])
    assert len(path_pts.shape) == 2
    assert path_pts.shape[1] == 3
    path_pts = path_solver.find_geodesic_path_poly([1173, 148, 870, 898], max_iterations=100, max_relative_length_decrease=0.5)
    loop_pts = path_solver.find_geodesic_loop([1173, 148, 870, 898])
    assert len(loop_pts.shape) == 2
    assert loop_pts.shape[1] == 3
    loop_pts = path_solver.find_geodesic_loop([307, 757, 190]) 
    assert len(loop_pts.shape) == 2
    assert loop_pts.shape[1] == 3
    loop_pts = path_solver.find_geodesic_loop([307, 757, 190], max_iterations=100, max_relative_length_decrease=0.5)

def test_geodesic_trace():
    V, F = pp3d.read_mesh(os.path.join(asset_path, "bunny_small.ply"))
    tracer = pp3d.GeodesicTracer(V,F)
    import numpy as np
    trace_pts = tracer.trace_geodesic_from_vertex(22, np.array((0.3, 0.5, 0.4)))
    assert len(trace_pts.shape) == 2 and trace_pts.shape[1] == 3
    trace_pts = tracer.trace_geodesic_from_vertex(22, np.array((0.3, 0.5, 0.4)), max_iterations=10)
    assert len(trace_pts.shape) == 2 and trace_pts.shape[1] == 3
    trace_pts = tracer.trace_geodesic_from_face(31, np.array((0.1, 0.4, 0.5)), np.array((0.3, 0.5, 0.4)))
    assert len(trace_pts.shape) == 2 and trace_pts.shape[1] == 3
    trace_pts = tracer.trace_geodesic_from_face(31, np.array((0.1, 0.4, 0.5)), np.array((0.3, 0.5, 0.4)), max_iterations=10)
    assert len(trace_pts.shape) == 2 and trace_pts.shape[1] == 3

def test_point_cloud_distance():
    P = generate_verts()
    solver = pp3d.PointCloudHeatSolver(P)
    dist = solver.compute_distance(7)
    assert dist.shape[0] == P.shape[0]
    dist = solver.compute_distance_multisource([1,2,3])
    assert dist.shape[0] == P.shape[0]

def test_point_cloud_vector_heat():
    P = generate_verts()
    solver = pp3d.PointCloudHeatSolver(P)
    ext = solver.extend_scalar([1, 22], [0., 6.])
    assert ext.shape[0] == P.shape[0]
    assert np.amin(ext) >= 0.
    basisX, basisY, basisN = solver.get_tangent_frames()
    assert basisX.shape[0] == P.shape[0]
    assert basisY.shape[0] == P.shape[0]
    assert basisN.shape[0] == P.shape[0]
    ext = solver.transport_tangent_vector(1, [6., 6.])
    assert ext.shape[0] == P.shape[0]
    assert ext.shape[1] == 2
    ext = solver.transport_tangent_vectors([1, 22], [[6., 6.], [3., 4.]])
    assert ext.shape[0] == P.shape[0]
    assert ext.shape[1] == 2
    logmap = solver.compute_log_map(1)
    assert logmap.shape[0] == P.shape[0]
    assert logmap.shape[1] == 2

def test_point_cloud_local_triangulation():
    num = 31
    import numpy as np
    t = np.linspace(0, 2*np.pi, num-1, endpoint=False)
    points = np.concatenate([np.zeros([1, 3]), np.stack([np.cos(t), np.sin(t), 0*t], 1)], 0)
    pcl_local_tri = pp3d.PointCloudLocalTriangulation(points)
    idxs = pcl_local_tri.get_local_triangulation()
    def next_id(i):
        assert i != 0
        if i == num-1:
            return 1
        return i+1
    def prev_id(i):
        assert i != 0
        if i == 1:
            return num-1
        return i-1
    res0 = set(tuple(r) for r in idxs[0])
    ref0 = set((0, j, next_id(j)) for j in range(1, num))
    assert res0 == ref0
    for i in range(1, num):
        assert all(idxs[i, 2:] == -1)
        res = set(tuple(r) for r in idxs[i, :2])
        ref = {(i, next_id(i), 0), (i, 0, prev_id(i))}
        assert res == ref
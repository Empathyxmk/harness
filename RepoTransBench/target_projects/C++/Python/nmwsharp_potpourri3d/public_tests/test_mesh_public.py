import pytest
from potpourri3d import mesh

@pytest.fixture
def tet_mesh():
    verts = [
        [0, 0, 0], 
        [1, 0, 0], 
        [0, 1, 0], 
        [0, 0, 1]
    ]
    faces = [
        [0, 1, 2],
        [0, 1, 3],
        [0, 2, 3],
        [1, 2, 3]
    ]
    return verts, faces

def test_mesh_area_public(tet_mesh):
    verts, faces = tet_mesh
    area = mesh.surface_area(verts, faces)
    import math
    expected = (4 * (3**0.5) / 4)
    assert math.isclose(area, expected, abs_tol=1e-5)

def test_mesh_edges_public(tet_mesh):
    _, faces = tet_mesh
    edges = mesh.edges(faces)
    # For tetrahedron: 6 edges
    assert len(edges) == 6
    for e in edges:
        assert len(e) == 2
        assert 0 <= e[0] <= 3 and 0 <= e[1] <= 3
        assert e[0] != e[1]

def test_mesh_euler_public(tet_mesh):
    verts, faces = tet_mesh
    euler = mesh.euler_characteristic(verts, faces)
    assert euler == 2
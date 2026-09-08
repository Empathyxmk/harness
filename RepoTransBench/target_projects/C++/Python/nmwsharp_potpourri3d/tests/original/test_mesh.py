import pytest
from potpourri3d import mesh

@pytest.fixture
def tetra_mesh():
    verts = [[0,0,0],[1,0,0],[0,1,0],[0,0,1]]
    faces = [[0,1,2],[0,1,3],[1,2,3],[2,0,3]]
    return verts, faces

def test_face_areas(tetra_mesh):
    verts, faces = tetra_mesh
    areas = mesh.face_areas(verts, faces)
    assert len(areas) == len(faces)
    assert all(a > 0 for a in areas)

def test_vertex_normals(tetra_mesh):
    verts, faces = tetra_mesh
    normals = mesh.vertex_normals(verts, faces)
    assert len(normals) == len(verts)
    import math
    for n in normals:
        assert math.isclose(sum(i**2 for i in n)**0.5, 1.0, abs_tol=1e-3)
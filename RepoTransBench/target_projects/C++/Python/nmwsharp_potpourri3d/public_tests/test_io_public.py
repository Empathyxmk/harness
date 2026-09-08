import pytest
import os
from potpourri3d import io

@pytest.fixture
def verts_faces():
    verts = [[2,3,4],[4,6,8],[1,7,5]]
    faces = [[0,2,1]]
    return verts, faces

def test_export_import_ply_public(verts_faces):
    verts, faces = verts_faces
    filename = "test_public_tmp.ply"
    io.save_mesh_ply(filename, verts, faces)
    v2, f2 = io.load_mesh_ply(filename)
    assert len(v2) == len(verts)
    assert len(f2) == len(faces)
    os.remove(filename)

def test_invalid_load_public():
    with pytest.raises(Exception):
        io.load_mesh_ply("definitely_nonexistent_file.ply")
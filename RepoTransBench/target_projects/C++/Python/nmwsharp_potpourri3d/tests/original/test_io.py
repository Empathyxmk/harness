import pytest
import os
from potpourri3d import io

@pytest.fixture
def basic_mesh():
    verts = [[0,0,0],[1,0,0],[0,1,0]]
    faces = [[0,1,2]]
    return verts, faces

def test_export_import_ply(basic_mesh):
    verts, faces = basic_mesh
    filename = "test_tmp.ply"
    io.save_mesh_ply(filename, verts, faces)
    v2, f2 = io.load_mesh_ply(filename)
    assert len(v2) == len(verts)
    assert len(f2) == len(faces)
    os.remove(filename)

def test_invalid_load():
    with pytest.raises(Exception):
        io.load_mesh_ply("nonexistent_file.ply")
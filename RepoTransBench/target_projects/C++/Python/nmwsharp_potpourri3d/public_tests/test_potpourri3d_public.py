import pytest
import potpourri3d

def test_import_public():
    assert hasattr(potpourri3d, 'core')
    assert hasattr(potpourri3d, 'mesh')
    assert hasattr(potpourri3d, 'point_cloud')
    assert hasattr(potpourri3d, 'io')

def test_help_str_public():
    s = str(potpourri3d)
    assert "potpourri3d" in s.lower()
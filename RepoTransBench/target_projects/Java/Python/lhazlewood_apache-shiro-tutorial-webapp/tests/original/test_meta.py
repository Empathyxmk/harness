import os

def test_project_structure_exists():
    assert os.path.isfile("pom.xml"), "pom.xml should exist"
    assert os.path.isfile("README.md"), "README.md should exist"
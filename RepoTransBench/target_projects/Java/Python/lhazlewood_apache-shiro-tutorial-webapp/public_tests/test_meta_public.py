import os

def test_project_required_files_exist_public():
    assert os.path.isfile("pom.xml"), "pom.xml must be present in the repo"
    assert os.path.isfile("LICENSE"), "LICENSE should exist in project root"
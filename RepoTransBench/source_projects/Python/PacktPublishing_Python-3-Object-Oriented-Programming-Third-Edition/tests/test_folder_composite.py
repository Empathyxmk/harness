import pytest
from Chapter11 import folder_composite

def setup_module(module):
    folder_composite.root.children.clear()

def test_folder_and_file_basic_structure():
    f = folder_composite.Folder("documents")
    folder_composite.root.add_child(f)
    file_txt = folder_composite.File("notes.txt", "abc")
    f.add_child(file_txt)

    assert f.children["notes.txt"] is file_txt
    assert file_txt.parent is f

def test_move_and_delete_behavior():
    # Setup
    f1 = folder_composite.Folder("docs1")
    f2 = folder_composite.Folder("docs2")
    folder_composite.root.add_child(f1)
    folder_composite.root.add_child(f2)
    myfile = folder_composite.File("my.txt", "content")
    f1.add_child(myfile)
    # Move myfile to f2
    myfile.move("/docs2")
    assert myfile.parent is f2
    assert "my.txt" in f2.children
    # Delete file from f2
    myfile.delete()
    assert "my.txt" not in f2.children

def test_get_path_returns_correct_node():
    f = folder_composite.Folder("foo")
    folder_composite.root.add_child(f)
    res = folder_composite.get_path("/foo")
    assert res is f
    # Add nested folder, and verify
    sub = folder_composite.Folder("bar")
    f.add_child(sub)
    path = folder_composite.get_path("/foo/bar")
    assert path is sub

def test_file_and_folder_init():
    file1 = folder_composite.File("dafile.txt", "cc")
    assert file1.name == "dafile.txt"
    assert file1.contents == "cc"
    folder = folder_composite.Folder("bktest")
    assert folder.name == "bktest"

def test_folder_add_child_sets_parent():
    p = folder_composite.Folder("parentf")
    c = folder_composite.Folder("childf")
    p.add_child(c)
    assert c.parent is p
    assert "childf" in p.children
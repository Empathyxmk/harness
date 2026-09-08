import pytest

def quad_replace_extension(filename, ext):
    if '.' in filename:
        core = '.'.join(filename.split('.')[:-1])
    else:
        core = filename
    return core + ext

def test_replace_extension_public():
    assert quad_replace_extension("mytest.doc.md", ".bak") == "mytest.doc.bak"
    assert quad_replace_extension("notes", ".md") == "notes.md"
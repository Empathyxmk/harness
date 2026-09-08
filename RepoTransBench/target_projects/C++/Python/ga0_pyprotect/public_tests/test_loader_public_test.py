import sys
import os
import shutil

def test_encrypt_tree_public(tmp_path):
    # PUBLIC TEST: encrypt a different file, 'foo.py', instead of 'app.py', using a different exclude!
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

    from encrypt import encrypt_tree

    root_dir = os.path.dirname(os.path.abspath(__file__))
    srcroot = os.path.join(root_dir, '..', 'test', 'app')
    # Use a different file in the app as "entrance"
    entrances = [(os.path.normpath(os.path.join(srcroot, 'foo.py')), 'main')]
    destroot = tmp_path / "dest_public"

    # Exclude nothing for this test (empty list)
    excludes = []

    # Remove destroot if exists
    if os.path.exists(destroot):
        shutil.rmtree(destroot)

    encrypt_tree(srcroot, entrances, str(destroot), excludes)
    # Check that destroot now exists and is a directory
    assert destroot.exists() and destroot.is_dir(), "Public Destination directory was not created"
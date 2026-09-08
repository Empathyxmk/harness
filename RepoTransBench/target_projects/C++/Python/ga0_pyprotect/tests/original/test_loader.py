import sys
import os
import shutil

def test_encrypt_app_tree(tmp_path):
    # 1. encrypt app
    # We assume encrypt.py exists one level above.
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

    from encrypt import encrypt_tree

    root_dir = os.path.dirname(os.path.abspath(__file__))
    srcroot = os.path.join(root_dir, '..', 'test', 'app')

    entrances = [(os.path.normpath(os.path.join(srcroot, 'app.py')), 'main')]
    destroot = tmp_path / "dest"
    excludes = [os.path.normpath(os.path.join(srcroot, 'exclude.py'))]

    # Remove destroot if it exists from previous runs
    if os.path.exists(destroot):
        shutil.rmtree(destroot)

    # encrypt_tree should not raise exceptions
    encrypt_tree(srcroot, entrances, str(destroot), excludes)
    # Check that destroot now exists
    assert destroot.exists() and destroot.is_dir(),"Destination directory was not created"
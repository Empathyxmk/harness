import os
import tempfile

from src.getAllFiles import getAllFiles

def test_getAllFiles_finds_files_in_structure():
    with tempfile.TemporaryDirectory() as tempdir_:
        file1 = os.path.join(tempdir_, 'file1.txt')
        with open(file1, 'w') as f:
            f.write('a')
        subdir = os.path.join(tempdir_, 'sub')
        os.mkdir(subdir)
        file2 = os.path.join(subdir, 'file2.txt')
        with open(file2, 'w') as f:
            f.write('b')

        result = getAllFiles(tempdir_)
        result_str = [str(x) for x in result]
        assert any('file1.txt' in x for x in result_str)
        assert any('file2.txt' in x for x in result_str)
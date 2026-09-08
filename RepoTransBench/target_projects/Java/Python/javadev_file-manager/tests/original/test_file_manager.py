import os
import shutil
import pytest

# We assume a skeleton FileManager class.
# In real usage, FileManager would be imported from the actual source.
class FileManager:
    def fileExists(self, filename):
        if filename is None:
            return False
        return os.path.exists(filename)

    def createFile(self, filename):
        if filename is None:
            raise ValueError("filename cannot be None")
        if os.path.exists(filename):
            return False
        with open(filename, 'w') as f:
            pass
        return True

    def deleteFile(self, filename):
        if filename is None or not os.path.exists(filename):
            return False
        os.remove(filename)
        return True

    def copyFile(self, source, dest):
        if source is None or dest is None:
            raise ValueError("Source and destination cannot be None")
        if not os.path.exists(source):
            return False
        shutil.copyfile(source, dest)
        return True


class TestFileManager:
    testFile = "testfile.txt"
    copiedFile = "copiedfile.txt"
    nullFile = None

    def setup_method(self, method):
        self.fm = FileManager()

    def teardown_method(self, method):
        for fname in [self.testFile, self.copiedFile, "dummy.txt"]:
            if os.path.exists(fname):
                os.remove(fname)

    def test_file_exists_false(self):
        assert not self.fm.fileExists("notreallypresent.txt")

    def test_file_exists_true(self):
        open(self.testFile, 'w').close()
        assert self.fm.fileExists(self.testFile)

    def test_file_exists_null(self):
        assert not self.fm.fileExists(None)

    def test_create_file_success(self):
        assert self.fm.createFile(self.testFile)
        # Creating again should return False (already exists)
        assert not self.fm.createFile(self.testFile)

    def test_create_file_null(self):
        with pytest.raises(ValueError):
            self.fm.createFile(self.nullFile)

    def test_delete_file_exists(self):
        open(self.testFile, 'w').close()
        assert self.fm.deleteFile(self.testFile)
        # File should not exist after deletion
        assert not os.path.exists(self.testFile)

    def test_delete_file_not_exists(self):
        assert not self.fm.deleteFile("dummy.txt")

    def test_delete_file_null(self):
        assert not self.fm.deleteFile(self.nullFile)

    def test_copy_file_success(self):
        open(self.testFile, 'w').close()
        assert self.fm.copyFile(self.testFile, self.copiedFile)
        assert os.path.exists(self.copiedFile)

    def test_copy_file_source_null(self):
        with pytest.raises(ValueError):
            self.fm.copyFile(None, "dest.txt")

    def test_copy_file_dest_null(self):
        with pytest.raises(ValueError):
            self.fm.copyFile("src.txt", None)
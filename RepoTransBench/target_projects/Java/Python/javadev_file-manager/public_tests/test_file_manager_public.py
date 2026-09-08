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


class TestFileManagerPublic:
    publicTestFile = "public_sample.txt"
    publicCopiedFile = "public_copied.txt"
    publicNullFile = None

    def setup_method(self, method):
        self.fm = FileManager()

    def teardown_method(self, method):
        for fname in [self.publicTestFile, self.publicCopiedFile, "unused_public.txt", "another_public.txt"]:
            if os.path.exists(fname):
                os.remove(fname)

    def test_file_exists_false_public(self):
        assert not self.fm.fileExists("definitelynotexisting_public.txt")

    def test_file_exists_true_public(self):
        open(self.publicTestFile, 'w').close()
        assert self.fm.fileExists(self.publicTestFile)

    def test_file_exists_null_public(self):
        assert not self.fm.fileExists(None)

    def test_create_file_success_public(self):
        assert self.fm.createFile(self.publicTestFile)
        # Creating again should return False (already exists)
        assert not self.fm.createFile(self.publicTestFile)

    def test_create_file_null_public(self):
        with pytest.raises(ValueError):
            self.fm.createFile(self.publicNullFile)

    def test_delete_file_exists_public(self):
        open(self.publicTestFile, 'w').close()
        assert self.fm.deleteFile(self.publicTestFile)
        # File should not exist after deletion
        assert not os.path.exists(self.publicTestFile)

    def test_delete_file_not_exists_public(self):
        assert not self.fm.deleteFile("unused_public.txt")

    def test_delete_file_null_public(self):
        assert not self.fm.deleteFile(self.publicNullFile)

    def test_copy_file_success_public(self):
        open(self.publicTestFile, 'w').close()
        assert self.fm.copyFile(self.publicTestFile, self.publicCopiedFile)
        assert os.path.exists(self.publicCopiedFile)

    def test_copy_file_source_null_public(self):
        with pytest.raises(ValueError):
            self.fm.copyFile(None, "another_public.txt")

    def test_copy_file_dest_null_public(self):
        with pytest.raises(ValueError):
            self.fm.copyFile("another_public.txt", None)
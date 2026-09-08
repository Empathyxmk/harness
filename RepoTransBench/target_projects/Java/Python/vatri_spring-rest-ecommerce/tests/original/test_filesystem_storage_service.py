import os
import shutil
import tempfile
import pytest
from pathlib import Path
from unittest import mock

class StorageException(Exception):
    pass

class StorageFileNotFoundException(Exception):
    pass

class StorageProperties:
    def __init__(self):
        self._location = "uploads"
    def getLocation(self):
        return self._location
    def setLocation(self, loc):
        self._location = loc

class FileSystemStorageService:
    def __init__(self, properties):
        self.location = Path(properties.getLocation())
    def init(self):
        try:
            self.location.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise StorageException("Could not initialize storage") from e
    def store(self, f, path):
        if hasattr(f, 'read') and callable(getattr(f, 'read')):
            file_content = f.read()
            if not file_content:
                raise StorageException("Failed to store empty file")
            subdir = self.location / path
            subdir.mkdir(parents=True, exist_ok=True)
            filename = getattr(f, 'filename', 'file.txt')
            tgt_file = subdir / filename
            with open(tgt_file, "wb") as out:
                out.write(file_content)
            return filename
        else:
            raise StorageException("Invalid file input for store")
    def loadAll(self):
        try:
            if not self.location.exists():
                return iter([])
            return (p for p in self.location.rglob("*") if p.is_file())
        except Exception as e:
            raise StorageException("Failed to read stored files") from e
    def load(self, filename):
        return self.location / filename
    def loadAsResource(self, filename):
        file_path = self.location / filename
        if not file_path.exists():
            raise StorageFileNotFoundException(filename)
        class Resource:
            def __init__(self, path):
                self._path = path
            def exists(self):
                return self._path.exists()
            def is_readable(self):
                try:
                    with open(self._path, "rb"):
                        return True
                except Exception:
                    return False
        return Resource(file_path)
    def deleteAll(self):
        if self.location.exists():
            shutil.rmtree(self.location)

@pytest.fixture(scope='module')
def test_dir():
    tmpdir = tempfile.mkdtemp()
    yield tmpdir
    shutil.rmtree(tmpdir, ignore_errors=True)

@pytest.fixture
def storage_service(test_dir):
    props = StorageProperties()
    props.setLocation(test_dir)
    srv = FileSystemStorageService(props)
    srv.deleteAll()
    srv.init()
    yield srv
    srv.deleteAll()

def test_init_creates_directory(storage_service, test_dir):
    root_path = Path(test_dir)
    assert root_path.exists()
    assert root_path.is_dir()

def test_store_valid_file(storage_service, test_dir):
    fname = "test.txt"
    path = "subdir"
    data = b"Spring Boot"
    mfile = mock.Mock()
    mfile.read = mock.Mock(return_value=data)
    mfile.filename = fname
    stored_name = storage_service.store(mfile, path)
    expected_dir = Path(test_dir) / path
    assert expected_dir.exists()
    files = list(expected_dir.iterdir())
    assert any(f.name == stored_name for f in files)

def test_store_empty_file_throws(storage_service):
    mfile = mock.Mock()
    mfile.read = mock.Mock(return_value=b"")
    mfile.filename = "empty.txt"
    with pytest.raises(StorageException) as ex:
        storage_service.store(mfile, "")
    assert "Failed to store empty file" in str(ex.value)

def test_loadall_lists_files(storage_service):
    # Add a file
    mfile = mock.Mock()
    mfile.read = mock.Mock(return_value=b"Test")
    mfile.filename = "loadall.txt"
    storage_service.store(mfile, "")
    files = list(storage_service.loadAll())
    assert len(files) > 0

def test_load_returns_correct_path(storage_service, test_dir):
    filename = "myfile.txt"
    written = Path(test_dir) / filename
    with open(written, "wb") as f:
        f.write(b"hello")
    loaded = storage_service.load(filename)
    assert loaded == written

def test_loadasresource_returns_resource(storage_service, test_dir):
    filename = "resource.txt"
    written = Path(test_dir) / filename
    with open(written, "wb") as f:
        f.write(b"hello")
    resource = storage_service.loadAsResource(filename)
    assert resource.exists()
    assert resource.is_readable()

def test_loadasresource_filenotfound(storage_service):
    filename = f"notexist-{os.urandom(6).hex()}.txt"
    with pytest.raises(StorageFileNotFoundException) as ex:
        storage_service.loadAsResource(filename)
    assert filename in str(ex.value)

def test_deleteall_deletes_directory(storage_service, test_dir):
    file_path = Path(test_dir) / "toremove.txt"
    with open(file_path, "wb") as f:
        f.write(b"bye")
    assert file_path.exists()
    storage_service.deleteAll()
    assert not Path(test_dir).exists()
    # restore for next tests
    storage_service.init()

def test_init_ioexception_throws(test_dir):
    class BrokenProperties(StorageProperties):
        def getLocation(self):
            # Unlikely to be writable
            return "/root/forbidden-" + str(os.getpid())
    props = BrokenProperties()
    service = FileSystemStorageService(props)
    with pytest.raises(StorageException) as ex:
        service.init()
    assert "Could not initialize storage" in str(ex.value)

def test_store_ioexception_throws(storage_service):
    mfile = mock.Mock()
    mfile.read = mock.Mock(side_effect=IOError("forced"))
    mfile.filename = "bad.txt"
    with pytest.raises(StorageException) as ex:
        storage_service.store(mfile, "badpath")
    assert "Invalid file input for store" in str(ex.value) or "Failed to store file" in str(ex.value) or "forced" in str(ex.value)

def test_loadall_ioexception_throws():
    class BrokenProperties:
        def getLocation(self):
            return "/root/forbidden-" + str(os.getpid())
    service = FileSystemStorageService(BrokenProperties())
    with pytest.raises(StorageException) as ex:
        list(service.loadAll())
    assert "Failed to read stored files" in str(ex.value)

def test_loadasresource_malformed_url(storage_service):
    class BadService(FileSystemStorageService):
        def load(self, filename):
            # Invalid path with illegal character
            return Path("\0invalid")
    bad_service = BadService(storage_service)
    with pytest.raises(StorageFileNotFoundException):
        bad_service.loadAsResource("badfile")
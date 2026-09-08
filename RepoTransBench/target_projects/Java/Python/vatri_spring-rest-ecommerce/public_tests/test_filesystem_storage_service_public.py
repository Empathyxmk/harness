import pytest
from pathlib import Path
import shutil

class StorageProperties:
    def __init__(self):
        self._location = "test-public-upload-dir"
    def getLocation(self):
        return self._location
    def setLocation(self, loc):
        self._location = loc

class StorageFileNotFoundException(Exception):
    pass

class StorageException(Exception):
    pass

class FileSystemStorageService:
    def __init__(self, properties):
        self.location = Path(properties.getLocation())
    def init(self):
        self.location.mkdir(parents=True, exist_ok=True)
    def store(self, f, path):
        path_out = self.location
        full_path = path_out / (f.filename if hasattr(f, 'filename') else path)
        with open(full_path, "wb") as fg:
            fg.write(f.read())
        return full_path.name
    def load(self, filename):
        return self.location / filename
    def loadAsResource(self, filename):
        fp = self.location / filename
        if not fp.exists():
            raise StorageFileNotFoundException(filename)
        class Resource:
            def __init__(self, path):
                self._path = path
            def exists(self):
                return self._path.exists()
        return Resource(fp)
    def loadAll(self):
        return (p for p in self.location.iterdir() if p.is_file())
    def deleteAll(self):
        for f in self.location.iterdir():
            if f.is_file():
                f.unlink()
            elif f.is_dir():
                shutil.rmtree(f)

class MockMultipartFile:
    def __init__(self, name, filename, content_type, content_bytes):
        self.name = name
        self.filename = filename
        self.content_type = content_type
        self._content = content_bytes
    def read(self):
        return self._content

import os

@pytest.fixture(autouse=True)
def cleanup_dir():
    testLocation = Path("test-public-upload-dir")
    if testLocation.exists():
        shutil.rmtree(testLocation)
    testLocation.mkdir(exist_ok=True)
    yield
    if testLocation.exists():
        shutil.rmtree(testLocation)

def test_store_and_load_public_file():
    properties = StorageProperties()
    properties.setLocation("test-public-upload-dir")
    storageService = FileSystemStorageService(properties)
    storageService.init()
    file = MockMultipartFile("publicfile", "publicfile.txt", "text/plain", b"test public content")

    storedFileName = storageService.store(file, "publicfile.txt")
    assert storedFileName == "publicfile.txt"

    testLocation = Path("test-public-upload-dir")
    loadedPath = storageService.load("publicfile.txt")
    assert loadedPath.resolve() == testLocation.resolve() / "publicfile.txt"

    resource = storageService.loadAsResource("publicfile.txt")
    assert resource is not None
    assert resource.exists()

    found = any(p.name == "publicfile.txt" for p in storageService.loadAll())
    assert found

def test_delete_all_public():
    properties = StorageProperties()
    properties.setLocation("test-public-upload-dir")
    storageService = FileSystemStorageService(properties)
    storageService.init()

    testLocation = Path("test-public-upload-dir")
    (testLocation / "todelete-public.txt").write_bytes(b"dummy")
    assert (testLocation / "todelete-public.txt").exists()
    storageService.deleteAll()
    assert not (testLocation / "todelete-public.txt").exists()
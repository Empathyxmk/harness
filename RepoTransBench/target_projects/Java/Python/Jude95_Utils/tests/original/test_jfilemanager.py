import unittest
import os
import tempfile
import shutil
import pickle

class JFileManagerFolder:
    """Stub for JFileManager.Folder"""
    def __init__(self, directory):
        self._dir = directory
        os.makedirs(directory, exist_ok=True)
    def getFile(self):
        class _File:
            def __init__(self, path):
                self._path = path
            def exists(self):
                return os.path.exists(self._path)
        return _File(self._dir)
    def writeStringToFile(self, content, filename):
        with open(os.path.join(self._dir, filename), "w", encoding="utf-8") as f:
            f.write(content)
    def readStringFromFile(self, filename):
        try:
            with open(os.path.join(self._dir, filename), "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return None
    def writeObjectToFile(self, obj, filename):
        with open(os.path.join(self._dir, filename), "wb") as f:
            pickle.dump(obj, f)
    def readObjectFromFile(self, filename):
        with open(os.path.join(self._dir, filename), "rb") as f:
            return pickle.load(f)
    def deleteChild(self, filename):
        fpath = os.path.join(self._dir, filename)
        if os.path.exists(fpath):
            os.remove(fpath)
    def listChildFile(self):
        return [f for f in os.listdir(self._dir) if os.path.isfile(os.path.join(self._dir, f))]
    def getChildFile(self, fname):
        class _File:
            def __init__(self, path):
                self._path = path
            def exists(self):
                return os.path.exists(self._path)
        return _File(os.path.join(self._dir, fname))


class JFileManager:
    _instance = None
    def __init__(self):
        self._folders = {}
        self._inited = False
    @classmethod
    def getInstance(cls):
        if not cls._instance:
            cls._instance = JFileManager()
        return cls._instance
    def init(self, context, dirs):
        self._folders = {d: JFileManagerFolder(context.getFilesDir()) for d in dirs}
        self._inited = True
    def getFolder(self, dirname):
        return self._folders[dirname]
    def clearAllData(self):
        for folder in self._folders.values():
            for file in folder.listChildFile():
                folder.deleteChild(file)

class DummyContext:
    def __init__(self, temp_dir):
        self._dir = temp_dir
    def getFilesDir(self):
        return self._dir

class TestObj:
    def __init__(self, x):
        self.x = x

class TestJFileManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tempdir = tempfile.mkdtemp("jfilemanager_test")
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls._tempdir, ignore_errors=True)

    def setUp(self):
        self.mgr = JFileManager.getInstance()
        self.mgr.init(DummyContext(self._tempdir), ["TEST"])
        self.folder = self.mgr.getFolder("TEST")

    def tearDown(self):
        self.mgr.clearAllData()

    def testInitAndGetFolder(self):
        folder = self.folder
        self.assertIsNotNone(folder)
        self.assertTrue(folder.getFile().exists())

    def testWriteAndReadString(self):
        folder = self.folder
        folder.writeStringToFile("hello world", "string.txt")
        read = folder.readStringFromFile("string.txt")
        self.assertEqual("hello world", read)
        self.assertIsNone(folder.readStringFromFile("not_exist.txt"))

    def testWriteAndReadObject(self):
        folder = self.folder
        obj = TestObj(1234)
        folder.writeObjectToFile(obj, "obj.bin")
        read = folder.readObjectFromFile("obj.bin")
        self.assertEqual(1234, read.x)
        folder.deleteChild("obj.bin")
        with self.assertRaises(Exception):
            folder.readObjectFromFile("obj.bin")

    def testListAndDeleteChild(self):
        folder = self.folder
        folder.writeStringToFile("data1", "f1.txt")
        folder.writeStringToFile("data2", "f2.txt")
        self.assertEqual(2, len(folder.listChildFile()))
        folder.deleteChild("f1.txt")
        self.assertEqual(1, len(folder.listChildFile()))

    def testClearAllData(self):
        folder = self.folder
        folder.writeStringToFile("t", "f.txt")
        self.assertTrue(folder.getChildFile("f.txt").exists())
        self.mgr.clearAllData()
        self.assertFalse(folder.getChildFile("f.txt").exists())

if __name__ == "__main__":
    unittest.main()
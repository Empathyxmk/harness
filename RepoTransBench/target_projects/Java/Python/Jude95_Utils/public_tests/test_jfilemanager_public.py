import unittest
import os

class JFileManager:
    @staticmethod
    def getFileNameFromPath(path):
        return os.path.basename(path)
    @staticmethod
    def getFileExtension(filename):
        return os.path.splitext(filename)[-1][1:]
    @staticmethod
    def isAbsolutePath(path):
        return os.path.isabs(path)

class TestJFileManagerPublic(unittest.TestCase):

    def testFilePathExtractionPublic(self):
        filePath = "/storage/emulated/0/Download/public_test_file2.txt"
        fileName = JFileManager.getFileNameFromPath(filePath)
        self.assertEqual("public_test_file2.txt", fileName)

    def testGetFileExtensionPublic(self):
        fileName = "sample_document.data"
        extension = JFileManager.getFileExtension(fileName)
        self.assertEqual("data", extension)

    def testIsPathAbsolutePublic(self):
        path = "/home/user/example"
        self.assertTrue(JFileManager.isAbsolutePath(path))
        relPath = "docs/readme.txt"
        self.assertFalse(JFileManager.isAbsolutePath(relPath))

if __name__ == "__main__":
    unittest.main()
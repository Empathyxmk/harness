using System;
using System.IO;
using Xunit;
using FileManager;

namespace FileManagerTests
{
    public class FileManagerTest : IDisposable
    {
        private readonly FileManager.FileManager _fm;
        private readonly string testFile = "testfile.txt";
        private readonly string copiedFile = "copiedfile.txt";
        private readonly string nullFile = null;

        public FileManagerTest()
        {
            _fm = new FileManager.FileManager();
        }

        public void Dispose()
        {
            CleanUp();
        }

        private void CleanUp()
        {
            DeleteIfExists(testFile);
            DeleteIfExists(copiedFile);
            DeleteIfExists("dummy.txt");
        }

        private void DeleteIfExists(string path)
        {
            if (path == null) return;
            if (File.Exists(path))
                File.Delete(path);
        }

        [Fact]
        public void TestFileExists_False()
        {
            Assert.False(_fm.FileExists("notreallypresent.txt"));
        }

        [Fact]
        public void TestFileExists_True()
        {
            FileInfo f = new FileInfo(testFile);
            Assert.True(!f.Exists);
            using (f.Create()) { }
            Assert.True(_fm.FileExists(testFile));
        }

        [Fact]
        public void TestFileExists_Null()
        {
            Assert.False(_fm.FileExists(null));
        }

        [Fact]
        public void TestCreateFile_Success()
        {
            Assert.True(_fm.CreateFile(testFile));
            // Creating again should return false (already exists)
            Assert.False(_fm.CreateFile(testFile));
        }

        [Fact]
        public void TestCreateFile_Null()
        {
            Assert.Throws<ArgumentException>(() => _fm.CreateFile(nullFile));
        }

        [Fact]
        public void TestDeleteFile_Exists()
        {
            using (File.Create(testFile)) { }
            Assert.True(_fm.DeleteFile(testFile));
            Assert.False(File.Exists(testFile));
        }

        [Fact]
        public void TestDeleteFile_NotExists()
        {
            Assert.False(_fm.DeleteFile("dummy.txt"));
        }

        [Fact]
        public void TestDeleteFile_Null()
        {
            Assert.False(_fm.DeleteFile(nullFile));
        }

        [Fact]
        public void TestCopyFile_Success()
        {
            using (File.Create(testFile)) { }
            Assert.True(_fm.CopyFile(testFile, copiedFile));
            Assert.True(File.Exists(copiedFile));
        }

        [Fact]
        public void TestCopyFile_SourceNull()
        {
            Assert.Throws<ArgumentException>(() => _fm.CopyFile(null, "dest.txt"));
        }

        [Fact]
        public void TestCopyFile_DestNull()
        {
            Assert.Throws<ArgumentException>(() => _fm.CopyFile("src.txt", null));
        }
    }
}
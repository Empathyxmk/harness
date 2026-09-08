using System;
using System.IO;
using Xunit;
using FileManager;

namespace FileManagerPublicTests
{
    public class FileManagerPublicTest : IDisposable
    {
        private readonly FileManager.FileManager _fm;
        private readonly string publicTestFile = "public_sample.txt";
        private readonly string publicCopiedFile = "public_copied.txt";
        private readonly string publicNullFile = null;

        public FileManagerPublicTest()
        {
            _fm = new FileManager.FileManager();
        }

        public void Dispose()
        {
            CleanUp();
        }

        private void CleanUp()
        {
            DeleteIfExists(publicTestFile);
            DeleteIfExists(publicCopiedFile);
            DeleteIfExists("unused_public.txt");
            DeleteIfExists("another_public.txt");
        }

        private void DeleteIfExists(string path)
        {
            if (path == null) return;
            if (File.Exists(path))
                File.Delete(path);
        }

        [Fact]
        public void TestFileExists_False_Public()
        {
            Assert.False(_fm.FileExists("definitelynotexisting_public.txt"));
        }

        [Fact]
        public void TestFileExists_True_Public()
        {
            FileInfo f = new FileInfo(publicTestFile);
            Assert.True(!f.Exists);
            using (f.Create()) { }
            Assert.True(_fm.FileExists(publicTestFile));
        }

        [Fact]
        public void TestFileExists_Null_Public()
        {
            Assert.False(_fm.FileExists(null));
        }

        [Fact]
        public void TestCreateFile_Success_Public()
        {
            Assert.True(_fm.CreateFile(publicTestFile));
            Assert.False(_fm.CreateFile(publicTestFile));
        }

        [Fact]
        public void TestCreateFile_Null_Public()
        {
            Assert.Throws<ArgumentException>(() => _fm.CreateFile(publicNullFile));
        }

        [Fact]
        public void TestDeleteFile_Exists_Public()
        {
            using (File.Create(publicTestFile)) { }
            Assert.True(_fm.DeleteFile(publicTestFile));
            Assert.False(File.Exists(publicTestFile));
        }

        [Fact]
        public void TestDeleteFile_NotExists_Public()
        {
            Assert.False(_fm.DeleteFile("unused_public.txt"));
        }

        [Fact]
        public void TestDeleteFile_Null_Public()
        {
            Assert.False(_fm.DeleteFile(publicNullFile));
        }

        [Fact]
        public void TestCopyFile_Success_Public()
        {
            using (File.Create(publicTestFile)) { }
            Assert.True(_fm.CopyFile(publicTestFile, publicCopiedFile));
            Assert.True(File.Exists(publicCopiedFile));
        }

        [Fact]
        public void TestCopyFile_SourceNull_Public()
        {
            Assert.Throws<ArgumentException>(() => _fm.CopyFile(null, "another_public.txt"));
        }

        [Fact]
        public void TestCopyFile_DestNull_Public()
        {
            Assert.Throws<ArgumentException>(() => _fm.CopyFile("another_public.txt", null));
        }
    }
}
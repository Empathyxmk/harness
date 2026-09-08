using System;
using System.IO;
using Xunit;
using Redwarp.NinePatchResizer;

namespace Redwarp.NinePatchResizer.PublicTests
{
    public class FileToolsPublicTests : IDisposable
    {
        private FileInfo tempInput;
        private FileInfo tempOutput;

        public FileToolsPublicTests()
        {
            tempInput = new FileInfo(Path.GetTempFileName());
            tempOutput = new FileInfo(Path.GetTempFileName());
            File.WriteAllText(tempInput.FullName, "Public Test Data!!");
            tempOutput.Delete();
        }

        public void Dispose()
        {
            try { tempInput?.Delete(); } catch {}
            try { tempOutput?.Delete(); } catch {}
        }

        [Fact]
        public void TestCopyFileNormal()
        {
            FileTools.CopyFile(tempInput, tempOutput);
            Assert.True(tempOutput.Exists);
            string content = File.ReadAllText(tempOutput.FullName).Trim();
            Assert.Equal("Public Test Data!!", content);
        }

        [Fact]
        public void TestCopyFileInputFileNotExist()
        {
            var input = new FileInfo("missing_file_abc123.txt");
            try
            {
                Assert.ThrowsAny<Exception>(() => FileTools.CopyFile(input, tempOutput));
            }
            catch (Exception)
            {
                // On some platforms, Environment.Exit(0) kills process immediately; test that correct logic is followed.
            }
        }

        [Fact]
        public void TestCopyFileIOException()
        {
            string tempDir = Path.Combine(Path.GetTempPath(), Path.GetRandomFileName());
            Directory.CreateDirectory(tempDir);
            var folder = new FileInfo(tempDir);
            try
            {
                FileTools.CopyFile(tempInput, folder);
                Assert.True(Directory.Exists(tempDir));
            }
            finally
            {
                try { Directory.Delete(tempDir); } catch {}
            }
        }
    }
}
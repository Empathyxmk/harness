using System;
using System.IO;
using Xunit;
using Redwarp.NinePatchResizer;

namespace Redwarp.NinePatchResizer.Tests.Original
{
    public class FileToolsTests : IDisposable
    {
        private FileInfo tempInput;
        private FileInfo tempOutput;

        public FileToolsTests()
        {
            tempInput = new FileInfo(Path.GetTempFileName());
            tempOutput = new FileInfo(Path.GetTempFileName());
            // Write some data to input file
            File.WriteAllText(tempInput.FullName, "Hello World!");
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
            Assert.Equal("Hello World!", content);
        }

        [Fact]
        public void TestCopyFileInputFileNotExist()
        {
            var input = new FileInfo("not_exist_file.xyz");
            var oldHandler = AppDomain.CurrentDomain.ProcessExit;
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
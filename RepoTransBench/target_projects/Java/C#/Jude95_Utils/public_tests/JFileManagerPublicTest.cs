using Xunit;
using Jude95_Utils;

namespace Jude95_Utils.PublicTests
{
    public class JFileManagerPublicTest
    {
        [Fact]
        public void TestFilePathExtractionPublic()
        {
            string filePath = "/storage/emulated/0/Download/public_test_file2.txt";
            string fileName = JFileManager.GetFileNameFromPath(filePath);
            Assert.Equal("public_test_file2.txt", fileName);
        }

        [Fact]
        public void TestGetFileExtensionPublic()
        {
            string fileName = "sample_document.data";
            string extension = JFileManager.GetFileExtension(fileName);
            Assert.Equal("data", extension);
        }

        [Fact]
        public void TestIsPathAbsolutePublic()
        {
            string path = "/home/user/example";
            Assert.True(JFileManager.IsAbsolutePath(path));

            string relPath = "docs/readme.txt";
            Assert.False(JFileManager.IsAbsolutePath(relPath));
        }
    }
}
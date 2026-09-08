using System.Text;
using System.IO;
using Xunit;

namespace AndroidUtils.Tests
{
    public class FileUtilsTest
    {
        [Fact]
        public void TestWriteAndReadFile()
        {
            var tmp = Path.GetTempFileName();
            try
            {
                string testStr = "hello";
                using (var inStream = new MemoryStream(Encoding.UTF8.GetBytes(testStr)))
                {
                    FileUtils.WriteFile(tmp, inStream);
                }

                string res = FileUtils.ReadFile(tmp);
                Assert.Contains("hello", res);
            }
            finally
            {
                File.Delete(tmp);
            }
        }
    }

    public static class FileUtils
    {
        public static void WriteFile(string path, Stream input)
        {
            using (var outStream = File.OpenWrite(path))
            {
                input.CopyTo(outStream);
            }
        }
        public static string ReadFile(string path)
        {
            return File.ReadAllText(path);
        }
    }
}
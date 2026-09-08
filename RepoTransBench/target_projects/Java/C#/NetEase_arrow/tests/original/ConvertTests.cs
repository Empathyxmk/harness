using System;
using System.IO;
using System.Text;
using Xunit;
using NetEaseArrow;

namespace NetEaseArrowTests.Original
{
    public class ConvertTests : IDisposable
    {
        private readonly string _gbkFile;
        private readonly string _utf8File;

        public ConvertTests()
        {
            // Setup: create GBK-encoded file with content "你好"
            _gbkFile = Path.GetTempFileName();
            _utf8File = Path.GetTempFileName();

            // .NET doesn't ship with GBK by default. Register codepage provider.
            Encoding.RegisterProvider(CodePagesEncodingProvider.Instance);

            var gbkEncoding = Encoding.GetEncoding("GBK");
            var bytes = gbkEncoding.GetBytes("你好");
            File.WriteAllBytes(_gbkFile, bytes);

            // Ensure utf8File is deleted so it can be created by the test
            if (File.Exists(_utf8File)) File.Delete(_utf8File);
        }

        public void Dispose()
        {
            // Test teardown: cleanup files
            if (File.Exists(_gbkFile)) File.Delete(_gbkFile);
            if (File.Exists(_utf8File)) File.Delete(_utf8File);
            var tmp = _gbkFile + ".tmp";
            if (File.Exists(tmp)) File.Delete(tmp);
        }

        [Fact]
        public void TestConvertGbkToUtf8InPlace()
        {
            string[] args = { _gbkFile };
            Convert.Main(args);

            // File should still exist and now be UTF-8
            var content = File.ReadAllText(_gbkFile, Encoding.UTF8);
            Assert.Contains("你好", content);
        }

        [Fact]
        public void TestConvertGbkToUtf8WithDifferentOutputFile()
        {
            string[] args = { _gbkFile, _utf8File };
            Convert.Main(args);

            Assert.True(File.Exists(_utf8File));
            var content = File.ReadAllText(_utf8File, Encoding.UTF8);
            Assert.Contains("你好", content);
        }

        [Fact]
        public void TestIOExceptionIsHandled()
        {
            string[] args = { "/not/exists/input/file.txt" };
            // Should not throw an exception; Convert.Main handles and writes to stdout
            Exception ex = Record.Exception(() => Convert.Main(args));
            Assert.Null(ex);
        }
    }
}
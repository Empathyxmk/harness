using System;
using System.IO;
using System.Text;
using Xunit;
using NetEaseArrow;

namespace NetEaseArrowTests.Public
{
    public class ConvertPublicTests : IDisposable
    {
        private readonly string _gbkFile;
        private readonly string _utf8File;

        public ConvertPublicTests()
        {
            // Create GBK-encoded file with content "世界"
            _gbkFile = Path.GetTempFileName();
            _utf8File = Path.GetTempFileName();

            Encoding.RegisterProvider(CodePagesEncodingProvider.Instance);
            var gbkEncoding = Encoding.GetEncoding("GBK");
            var bytes = gbkEncoding.GetBytes("世界");
            File.WriteAllBytes(_gbkFile, bytes);

            if (File.Exists(_utf8File)) File.Delete(_utf8File);
        }

        public void Dispose()
        {
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

            var content = File.ReadAllText(_gbkFile, Encoding.UTF8);
            Assert.Contains("世界", content);
        }

        [Fact]
        public void TestConvertGbkToUtf8WithDifferentOutputFile()
        {
            string[] args = { _gbkFile, _utf8File };
            Convert.Main(args);

            Assert.True(File.Exists(_utf8File));
            var content = File.ReadAllText(_utf8File, Encoding.UTF8);
            Assert.Contains("世界", content);
        }

        [Fact]
        public void TestIOExceptionIsHandled()
        {
            string[] args = { "/definitely/doesnotexist/inputfile_public.txt" };
            Exception ex = Record.Exception(() => Convert.Main(args));
            Assert.Null(ex);
        }
    }
}
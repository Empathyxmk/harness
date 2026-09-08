using System;
using System.IO;
using System.Text;
using Xunit;
using Moq;
using xzr.hkf.utils;

namespace libxzr_HorizonKernelFlasher.Tests.Original.Utils
{
    public class AssetsUtilTests
    {
        private Mock<IContext> _context;
        private Mock<IAssetManager> _assetManager;

        public AssetsUtilTests()
        {
            _context = new Mock<IContext>();
            _assetManager = new Mock<IAssetManager>();
            _context.Setup(c => c.GetAssets()).Returns(_assetManager.Object);
        }

        [Fact]
        public void TestExportFiles_Directory()
        {
            _assetManager.Setup(am => am.List("src")).Returns(new string[] { "f1", "f2" });
            _assetManager.Setup(am => am.List("src/f1")).Returns(Array.Empty<string>());
            _assetManager.Setup(am => am.List("src/f2")).Returns(Array.Empty<string>());
            _assetManager.Setup(am => am.Open(It.IsAny<string>())).Returns<string>(name => new MemoryStream(Encoding.UTF8.GetBytes("content")));
            var tempDir = Path.Combine(Path.GetTempPath(), "assetsutiltest");
            Directory.CreateDirectory(tempDir);

            AssetsUtil.exportFiles(_context.Object, "src", tempDir);
            Assert.True(Directory.Exists(tempDir));
        }

        [Fact]
        public void TestExportFiles_EmptyFile()
        {
            _assetManager.Setup(am => am.List("foo")).Returns(Array.Empty<string>());
            var isStream = new MemoryStream(Encoding.UTF8.GetBytes("ok"));
            _assetManager.Setup(am => am.Open("foo")).Returns(isStream);
            var tempFile = Path.GetTempFileName();
            AssetsUtil.exportFiles(_context.Object, "foo", tempFile);
            Assert.Equal(2, new FileInfo(tempFile).Length);
            File.Delete(tempFile);
        }

        [Fact]
        public void TestExportFiles_IOException()
        {
            _assetManager.Setup(am => am.List("bad")).Throws(new IOException("failtest"));
            Assert.Throws<IOException>(() => AssetsUtil.exportFiles(_context.Object, "bad", "/tmp/notused"));
        }
    }
}
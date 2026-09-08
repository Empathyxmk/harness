using System;
using System.IO;
using System.Text;
using Xunit;
using Moq;
using xzr.hkf.utils;

namespace libxzr_HorizonKernelFlasher.PublicTests.Utils
{
    public class AssetsUtilPublicTests
    {
        private Mock<IContext> _context;
        private Mock<IAssetManager> _assetManager;

        public AssetsUtilPublicTests()
        {
            _context = new Mock<IContext>();
            _assetManager = new Mock<IAssetManager>();
            _context.Setup(c => c.GetAssets()).Returns(_assetManager.Object);
        }

        [Fact]
        public void TestExportFiles_Directory_Public()
        {
            _assetManager.Setup(am => am.List("pub")).Returns(new string[] { "a", "b", "c" });
            _assetManager.Setup(am => am.List("pub/a")).Returns(Array.Empty<string>());
            _assetManager.Setup(am => am.List("pub/b")).Returns(Array.Empty<string>());
            _assetManager.Setup(am => am.List("pub/c")).Returns(Array.Empty<string>());
            _assetManager.Setup(am => am.Open(It.IsAny<string>())).Returns<string>(name => new MemoryStream(Encoding.UTF8.GetBytes("pubdata")));
            var tempDir = Path.Combine(Path.GetTempPath(), "assetsutilpublictest");
            Directory.CreateDirectory(tempDir);

            AssetsUtil.exportFiles(_context.Object, "pub", tempDir);
            Assert.True(Directory.Exists(tempDir));
        }

        [Fact]
        public void TestExportFiles_EmptyFile_Public()
        {
            _assetManager.Setup(am => am.List("baz")).Returns(Array.Empty<string>());
            var isStream = new MemoryStream(Encoding.UTF8.GetBytes("OK"));
            _assetManager.Setup(am => am.Open("baz")).Returns(isStream);
            var tempFile = Path.GetTempFileName();
            AssetsUtil.exportFiles(_context.Object, "baz", tempFile);
            Assert.Equal(2, new FileInfo(tempFile).Length);
            File.Delete(tempFile);
        }

        [Fact]
        public void TestExportFiles_IOException_Public()
        {
            _assetManager.Setup(am => am.List("broken")).Throws(new IOException("failtest-broken"));
            Assert.Throws<IOException>(() => AssetsUtil.exportFiles(_context.Object, "broken", "/tmp/notusedpub"));
        }
    }
}
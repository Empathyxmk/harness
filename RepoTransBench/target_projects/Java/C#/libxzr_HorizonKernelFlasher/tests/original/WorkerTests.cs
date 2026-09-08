using System;
using System.IO;
using Xunit;
using Moq;
using xzr.hkf;

namespace libxzr_HorizonKernelFlasher.Tests.Original
{
    public class WorkerTests
    {
        private Mock<IActivity> _mockActivity;
        private Mock<Worker> _worker;

        public WorkerTests()
        {
            _mockActivity = new Mock<IActivity>();
            _mockActivity.Setup(a => a.GetFilesDir()).Returns(Path.GetTempPath());
            _worker = new Mock<Worker>(_mockActivity.Object) { CallBase = true };
            _worker.Object.uri = null;
        }

        [Fact]
        public void TestRootAvailable_True()
        {
            _worker.Setup(w => w.RunWithNewProcessReturn(true, "id")).Returns("root xzr");
            Assert.True(_worker.Object.rootAvailable());
        }

        [Fact]
        public void TestRootAvailable_False()
        {
            _worker.Setup(w => w.RunWithNewProcessReturn(true, "id")).Throws<IOException>();
            Assert.False(_worker.Object.rootAvailable());
        }

        [Fact]
        public void TestCopy_Throws()
        {
            _mockActivity.Setup(a => a.GetContentResolver()).Throws(new IOException("fail"));
            Assert.ThrowsAny<Exception>(() => _worker.Object.copy());
        }

        [Fact]
        public void TestGetBinary_NotExist()
        {
            _worker.Setup(w => w.RunWithNewProcessNoReturn(It.IsAny<bool>(), It.IsAny<string>()));
            _worker.Object.file_path = Path.Combine(Path.GetTempPath(), "notfound.zip");
            _worker.Object.binary_path = Path.Combine(Path.GetTempPath(), "notfound.update-binary");
            Assert.Throws<IOException>(() => _worker.Object.getBinary());
        }

        [Fact]
        public void TestPatch_AssetsUtilThrows()
        {
            _worker.Setup(w => w.RunWithNewProcessNoReturn(It.IsAny<bool>(), It.IsAny<string>())).Throws(new IOException("fail"));
            Assert.Throws<IOException>(() => _worker.Object.patch());
        }

        [Fact]
        public void TestFlash_Throws()
        {
            _worker.Setup(w => w.RunWithNewProcessReturn(It.IsAny<bool>(), It.IsAny<string>())).Throws(new IOException("fail"));
            Assert.Throws<IOException>(() => _worker.Object.flash(_mockActivity.Object));
        }
    }
}
using System;
using System.IO;
using Xunit;
using Moq;
using xzr.hkf;

namespace libxzr_HorizonKernelFlasher.PublicTests
{
    public class WorkerPublicTests
    {
        private Mock<IActivity> _mockActivity;
        private Mock<Worker> _worker;

        public WorkerPublicTests()
        {
            _mockActivity = new Mock<IActivity>();
            _mockActivity.Setup(a => a.GetFilesDir()).Returns(Path.Combine(Path.GetTempPath(), "workerpublictest"));
            _worker = new Mock<Worker>(_mockActivity.Object) { CallBase = true };
            _worker.Object.uri = null;
        }

        [Fact]
        public void TestRootAvailable_True_Public()
        {
            _worker.Setup(w => w.RunWithNewProcessReturn(true, "id")).Returns("root otheruser");
            Assert.True(_worker.Object.rootAvailable());
        }

        [Fact]
        public void TestRootAvailable_False_Public()
        {
            _worker.Setup(w => w.RunWithNewProcessReturn(true, "id")).Returns((string)null);
            Assert.False(_worker.Object.rootAvailable());
        }

        [Fact]
        public void TestCopy_Throws_Public()
        {
            _mockActivity.Setup(a => a.GetContentResolver()).Throws(new IOException("fail again"));
            Assert.ThrowsAny<Exception>(() => _worker.Object.copy());
        }

        [Fact]
        public void TestGetBinary_NotExist_Public()
        {
            _worker.Setup(w => w.RunWithNewProcessNoReturn(It.IsAny<bool>(), It.IsAny<string>()));
            _worker.Object.file_path = Path.Combine(Path.GetTempPath(), "definitely_missing.zip");
            _worker.Object.binary_path = Path.Combine(Path.GetTempPath(), "definitely_missing-binary");
            Assert.Throws<IOException>(() => _worker.Object.getBinary());
        }

        [Fact]
        public void TestPatch_AssetsUtilThrows_Public()
        {
            _worker.Setup(w => w.RunWithNewProcessNoReturn(It.IsAny<bool>(), It.IsAny<string>())).Throws(new IOException("fail2"));
            Assert.Throws<IOException>(() => _worker.Object.patch());
        }

        [Fact]
        public void TestFlash_Throws_Public()
        {
            _worker.Setup(w => w.RunWithNewProcessReturn(It.IsAny<bool>(), It.IsAny<string>())).Throws(new IOException("fail3"));
            Assert.Throws<IOException>(() => _worker.Object.flash(_mockActivity.Object));
        }
    }
}
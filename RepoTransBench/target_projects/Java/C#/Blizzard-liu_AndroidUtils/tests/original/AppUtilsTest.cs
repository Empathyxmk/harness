using System;
using Xunit;
using Moq;

namespace AndroidUtils.Tests
{
    public class AppUtilsTest
    {
        [Fact]
        public void TestGetVerCode_Normal()
        {
            // Simulate context and package manager behavior using Moq
            var contextMock = new Mock<IContext>();
            var packageManagerMock = new Mock<IPackageManager>();
            var packageInfo = new PackageInfo { VersionCode = 123 };
            contextMock.Setup(c => c.PackageName).Returns("pkg");
            contextMock.Setup(c => c.PackageManager).Returns(packageManagerMock.Object);
            packageManagerMock.Setup(pm => pm.GetPackageInfo("pkg", 0)).Returns(packageInfo);
            Assert.Equal(123, AppUtils.GetVerCode(contextMock.Object));
        }

        [Fact]
        public void TestGetVerCode_NotFound()
        {
            var contextMock = new Mock<IContext>();
            var packageManagerMock = new Mock<IPackageManager>();
            contextMock.Setup(c => c.PackageName).Returns("pkg");
            contextMock.Setup(c => c.PackageManager).Returns(packageManagerMock.Object);
            packageManagerMock.Setup(pm => pm.GetPackageInfo(It.IsAny<string>(), It.IsAny<int>())).Throws(new NameNotFoundException());
            Assert.Equal(-1, AppUtils.GetVerCode(contextMock.Object));
        }

        [Fact]
        public void TestGetVerName_Normal()
        {
            var contextMock = new Mock<IContext>();
            var packageManagerMock = new Mock<IPackageManager>();
            var packageInfo = new PackageInfo { VersionName = "verX" };
            contextMock.Setup(c => c.PackageName).Returns("pkg");
            contextMock.Setup(c => c.PackageManager).Returns(packageManagerMock.Object);
            packageManagerMock.Setup(pm => pm.GetPackageInfo("pkg", 0)).Returns(packageInfo);
            Assert.Equal("verX", AppUtils.GetVerName(contextMock.Object));
        }

        [Fact]
        public void TestGetVerName_NotFound()
        {
            var contextMock = new Mock<IContext>();
            var packageManagerMock = new Mock<IPackageManager>();
            contextMock.Setup(c => c.PackageName).Returns("pkg");
            contextMock.Setup(c => c.PackageManager).Returns(packageManagerMock.Object);
            packageManagerMock.Setup(pm => pm.GetPackageInfo(It.IsAny<string>(), It.IsAny<int>())).Throws(new NameNotFoundException());
            Assert.Equal("", AppUtils.GetVerName(contextMock.Object));
        }
    }

    // Stubs for interfaces and exceptions to simulate Android
    public interface IContext
    {
        string PackageName { get; }
        IPackageManager PackageManager { get; }
    }
    public interface IPackageManager
    {
        PackageInfo GetPackageInfo(string packageName, int flags);
    }
    public class PackageInfo
    {
        public int VersionCode { get; set; }
        public string VersionName { get; set; }
    }
    public class NameNotFoundException : Exception { }
    public static class AppUtils
    {
        public static int GetVerCode(IContext context)
        {
            try
            {
                var info = context.PackageManager.GetPackageInfo(context.PackageName, 0);
                return info.VersionCode;
            }
            catch (NameNotFoundException)
            {
                return -1;
            }
        }
        public static string GetVerName(IContext context)
        {
            try
            {
                var info = context.PackageManager.GetPackageInfo(context.PackageName, 0);
                return info.VersionName;
            }
            catch (NameNotFoundException)
            {
                return "";
            }
        }
    }
}
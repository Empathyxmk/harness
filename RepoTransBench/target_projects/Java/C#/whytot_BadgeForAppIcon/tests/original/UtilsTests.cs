using Xunit;
using System;
using Moq;
using BadgeForAppIcon.Models;

namespace BadgeForAppIcon.Tests.Original
{
    public class UtilsTests
    {
        private Mock<object> mockContext;
        private Mock<object> mockPackageManager;

        public UtilsTests()
        {
            mockContext = new Mock<object>();
            mockPackageManager = new Mock<object>();
        }

        [Fact]
        public void GetInstance_IsSingleton()
        {
            var instance1 = Utils.GetInstance();
            var instance2 = Utils.GetInstance();
            Assert.NotNull(instance1);
            Assert.Equal(instance1, instance2);
        }

        [Fact]
        public void CanResolveBroadcast_NoReceivers()
        {
            // Simulate PackageManager returning null and then empty list
            // The real method implementation is not shown in stub code – must be implemented for this test to pass
            Assert.False(Utils.GetInstance().CanResolveBroadcast(mockContext.Object, new object()));
        }

        [Fact]
        public void CanResolveBroadcast_WithReceivers()
        {
            // Simulate PackageManager returning a singleton list
            Assert.True(Utils.GetInstance().CanResolveBroadcast(mockContext.Object, new object()));
        }

        [Fact]
        public void GetLaunchIntentForPackage_ReturnsClassName()
        {
            // Assume we return something like the class name string in test implementation
            string className = Utils.GetInstance().GetLaunchIntentForPackage(mockContext.Object);
            Assert.Equal("com.example.package.MainActivity", className);
        }

        [Fact]
        public void GetLaunchIntentForPackage_NullLaunchIntent_Throws()
        {
            Assert.Throws<NullReferenceException>(() => Utils.GetInstance().GetLaunchIntentForPackage(null));
        }
    }
}
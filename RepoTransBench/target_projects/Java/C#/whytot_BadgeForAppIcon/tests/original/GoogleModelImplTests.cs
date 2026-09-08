using Xunit;
using System;
using System.Reflection;
using Moq;
using BadgeForAppIcon.Models;

namespace BadgeForAppIcon.Tests.Original
{
    public class GoogleModelImplTests : IDisposable
    {
        private GoogleModelImpl googleModel;
        private Mock<object> mockApplication;
        private Mock<object> mockNotification;
        private Mock<object> mockPackageManager;
        private Mock<Utils> mockUtils;
        private int originalSdkInt;

        public GoogleModelImplTests()
        {
            mockApplication = new Mock<object>();
            mockNotification = new Mock<object>();
            mockPackageManager = new Mock<object>();
            mockUtils = new Mock<Utils>();
            googleModel = new GoogleModelImpl();

            // Assume SDK versioning is emulated via static property (in test only)
            originalSdkInt = SdkVersionMocker.SdkInt;

            // Set up Utils singleton via reflection
            typeof(Utils).GetField("instance", BindingFlags.Static | BindingFlags.NonPublic)?.SetValue(null, mockUtils.Object);

            mockUtils.Setup(u => u.GetLaunchIntentForPackage(It.IsAny<object>())).Returns("com.example.package.MainActivity");
            mockUtils.Setup(u => u.CanResolveBroadcast(It.IsAny<object>(), It.IsAny<object>())).Returns(true);

            mockApplication.Setup(a => a.GetType().GetMethod("getPackageName").Invoke(a, null)).Returns("com.example.package");
            mockApplication.Setup(a => a.GetType().GetMethod("getPackageManager").Invoke(a, null)).Returns(mockPackageManager.Object);
        }

        public void Dispose()
        {
            // Reset SDK version and Utils singleton for isolation
            SdkVersionMocker.SdkInt = originalSdkInt;
            typeof(Utils).GetField("instance", BindingFlags.Static | BindingFlags.NonPublic)?.SetValue(null, null);
        }

        private void SetSdkInt(int value) => SdkVersionMocker.SdkInt = value;

        [Fact]
        public void SetIconBadgeNum_SdkBelowO_Throws()
        {
            SetSdkInt(25); // API level below O (26)
            var ex = Assert.Throws<Exception>(() => googleModel.SetIconBadgeNum(mockApplication.Object, mockNotification.Object, 5));
            Assert.Equal("google not support before API O", ex.Message);
            mockApplication.Verify(a => a.GetType().GetMethod("sendBroadcast").Invoke(a, It.IsAny<object[]>()), Times.Never());
        }

        [Fact]
        public void SetIconBadgeNum_SdkAtOrAboveO_SendsBroadcast()
        {
            SetSdkInt(26); // API level O
            int testCount = 7;
            googleModel.SetIconBadgeNum(mockApplication.Object, mockNotification.Object, testCount);

            // Here you would normally capture the broadcast intent and verify its content.
            mockApplication.Verify(a => a.GetType().GetMethod("sendBroadcast").Invoke(a, It.IsAny<object[]>()), Times.Once());
        }
    }

    // Utility class for SDK version mocking
    public static class SdkVersionMocker
    {
        private static int sdkInt = 30; // default, can be reset in tests
        public static int SdkInt
        {
            get => sdkInt;
            set => sdkInt = value;
        }
        public static void ResetSdkVersion()
        {
            sdkInt = 30;
        }
    }
}
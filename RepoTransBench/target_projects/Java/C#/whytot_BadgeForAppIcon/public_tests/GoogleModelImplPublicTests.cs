using Xunit;
using System;
using System.Reflection;
using Moq;
using BadgeForAppIcon.Models;

namespace BadgeForAppIcon.Tests.Public
{
    public class GoogleModelImplPublicTests : IDisposable
    {
        private GoogleModelImpl googleModel;
        private Mock<object> mockApplication;
        private Mock<object> mockNotification;
        private Mock<object> mockPackageManager;
        private Mock<Utils> mockUtils;
        private int originalSdkInt;

        public GoogleModelImplPublicTests()
        {
            mockApplication = new Mock<object>();
            mockNotification = new Mock<object>();
            mockPackageManager = new Mock<object>();
            mockUtils = new Mock<Utils>();
            googleModel = new GoogleModelImpl();

            originalSdkInt = SdkVersionMocker.SdkInt;
            typeof(Utils).GetField("instance", BindingFlags.Static | BindingFlags.NonPublic)?.SetValue(null, mockUtils.Object);
            mockUtils.Setup(u => u.GetLaunchIntentForPackage(It.IsAny<object>())).Returns("sample.another.MainAct");
            mockUtils.Setup(u => u.CanResolveBroadcast(It.IsAny<object>(), It.IsAny<object>())).Returns(true);

            mockApplication.Setup(a => a.GetType().GetMethod("getPackageName").Invoke(a, null)).Returns("sample.another");
            mockApplication.Setup(a => a.GetType().GetMethod("getPackageManager").Invoke(a, null)).Returns(mockPackageManager.Object);
        }

        public void Dispose()
        {
            SdkVersionMocker.SdkInt = originalSdkInt;
            typeof(Utils).GetField("instance", BindingFlags.Static | BindingFlags.NonPublic)?.SetValue(null, null);
        }

        private void SetSdkInt(int value) => SdkVersionMocker.SdkInt = value;

        [Fact]
        public void SetIconBadgeNum_SdkBelowO_Throws_Public()
        {
            SetSdkInt(24); // API level N
            var ex = Assert.Throws<Exception>(() => googleModel.SetIconBadgeNum(mockApplication.Object, mockNotification.Object, 15));
            Assert.Equal("google not support before API O", ex.Message);
            mockApplication.Verify(a => a.GetType().GetMethod("sendBroadcast").Invoke(a, It.IsAny<object[]>()), Times.Never());
        }

        [Fact]
        public void SetIconBadgeNum_SdkAtOrAboveO_SendsBroadcast_Public()
        {
            SetSdkInt(27); // API level O_MR1
            int testCount = 21;
            googleModel.SetIconBadgeNum(mockApplication.Object, mockNotification.Object, testCount);
            mockApplication.Verify(a => a.GetType().GetMethod("sendBroadcast").Invoke(a, It.IsAny<object[]>()), Times.Once());
        }
    }

    public static class SdkVersionMocker
    {
        private static int sdkInt = 30;
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
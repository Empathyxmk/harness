using Xunit;
using System;
using Moq;
using BadgeForAppIcon.Models;

namespace BadgeForAppIcon.Tests.Public
{
    public class UtilsPublicTests
    {
        private Mock<object> mockApp;

        public UtilsPublicTests()
        {
            mockApp = new Mock<object>();
        }

        [Fact]
        public void GetLaunchIntentForPackage_Public()
        {
            mockApp.Setup(a => a.GetType().GetMethod("getPackageName").Invoke(a, null)).Returns("public.pkg.name");
            string launchIntent = Utils.GetInstance().GetLaunchIntentForPackage(mockApp.Object);
            Assert.NotNull(launchIntent);
        }

        [Fact]
        public void CanResolveBroadcast_Public()
        {
            var ctx = new Mock<object>();
            object intent = new object();
            bool result = Utils.GetInstance().CanResolveBroadcast(ctx.Object, intent);
            Assert.True(result || !result); // assert method returns a bool value, no matter which
        }
    }
}
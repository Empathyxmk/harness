using Xunit;
using System;
using Moq;
using BadgeForAppIcon.Models;

namespace BadgeForAppIcon.Tests.Public
{
    public class VIVOModelImplPublicTests
    {
        private VIVOModelImpl vivoModel;
        private Mock<object> mockApplication;
        private Mock<object> mockNotification;

        public VIVOModelImplPublicTests()
        {
            mockApplication = new Mock<object>();
            mockNotification = new Mock<object>();
            vivoModel = new VIVOModelImpl();
        }

        [Fact]
        public void SetIconBadgeNum_AlwaysThrows_Public()
        {
            var ex = Assert.Throws<Exception>(() => vivoModel.SetIconBadgeNum(mockApplication.Object, mockNotification.Object, 17));
            Assert.Equal("not support : vivo", ex.Message);
        }
    }
}
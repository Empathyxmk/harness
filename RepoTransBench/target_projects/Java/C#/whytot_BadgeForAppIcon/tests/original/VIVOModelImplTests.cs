using Xunit;
using System;
using Moq;
using BadgeForAppIcon.Models;

namespace BadgeForAppIcon.Tests.Original
{
    public class VIVOModelImplTests
    {
        private VIVOModelImpl vivoModel;
        private Mock<object> mockApplication;
        private Mock<object> mockNotification;

        public VIVOModelImplTests()
        {
            mockApplication = new Mock<object>();
            mockNotification = new Mock<object>();
            vivoModel = new VIVOModelImpl();
        }

        [Fact]
        public void SetIconBadgeNum_AlwaysThrows()
        {
            var ex = Assert.Throws<Exception>(() => vivoModel.SetIconBadgeNum(mockApplication.Object, mockNotification.Object, 10));
            Assert.Equal("not support : vivo", ex.Message);
        }
    }
}
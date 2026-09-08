using Xunit;
using System;
using Moq;
using BadgeForAppIcon.Models;

namespace BadgeForAppIcon.Tests.Public
{
    public class XiaoMiModelImplPublicTests
    {
        private XiaoMiModelImpl xiaoMiModel;
        private Mock<object> mockApplication;

        public class TestNotification
        {
            public TestExtraNotification ExtraNotification { get; } = new TestExtraNotification();

            public class TestExtraNotification
            {
                private int messageCount = 0;
                public void SetMessageCount(int count)
                {
                    messageCount = count;
                }
                public int GetMessageCount()
                {
                    return messageCount;
                }
            }
        }

        public XiaoMiModelImplPublicTests()
        {
            mockApplication = new Mock<object>();
            xiaoMiModel = new XiaoMiModelImpl();
        }

        [Fact]
        public void SetIconBadgeNum_NullNotification_Throws_Public()
        {
            var ex = Assert.Throws<Exception>(() => xiaoMiModel.SetIconBadgeNum(mockApplication.Object, null, 99));
            Assert.Equal("Xiaomi phones must send notification", ex.Message);
        }

        [Fact]
        public void SetIconBadgeNum_ValidNotification_Public()
        {
            var notification = new TestNotification();
            int testCount = 12;
            var result = xiaoMiModel.SetIconBadgeNum(mockApplication.Object, notification, testCount);
            Assert.NotNull(result);
            Assert.Same(notification, result);
            Assert.Equal(testCount, notification.ExtraNotification.GetMessageCount());
        }
    }
}
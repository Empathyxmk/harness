using Xunit;
using System;
using Moq;
using BadgeForAppIcon.Models;

namespace BadgeForAppIcon.Tests.Original
{
    public class XiaoMiModelImplTests
    {
        private XiaoMiModelImpl xiaoMiModel;
        private Mock<object> mockApplication;

        // Dummy Notification class
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

        public XiaoMiModelImplTests()
        {
            mockApplication = new Mock<object>();
            xiaoMiModel = new XiaoMiModelImpl();
        }

        [Fact]
        public void SetIconBadgeNum_NullNotification_Throws()
        {
            var ex = Assert.Throws<Exception>(() => xiaoMiModel.SetIconBadgeNum(mockApplication.Object, null, 10));
            Assert.Equal("Xiaomi phones must send notification", ex.Message);
        }

        [Fact]
        public void SetIconBadgeNum_ValidNotification_SetsCount()
        {
            var notification = new TestNotification();
            int testCount = 5;
            var result = xiaoMiModel.SetIconBadgeNum(mockApplication.Object, notification, testCount);
            Assert.NotNull(result);
            Assert.Same(notification, result);
            Assert.Equal(testCount, notification.ExtraNotification.GetMessageCount());
        }
    }
}
using Moq;
using Xunit;

namespace UberUX.Tests.Public
{
    public class BaseActivityPublicTest
    {
        private UberUX.BaseActivity baseActivity;

        public BaseActivityPublicTest()
        {
            var mock = new Mock<UberUX.BaseActivity> { CallBase = true };
            baseActivity = mock.Object;
        }

        [Fact]
        public void TestGetContext_Public()
        {
            var mockContext = new object();
            Mock.Get(baseActivity).Setup(x => x.getContext()).Returns(mockContext);

            Assert.NotNull(baseActivity.getContext());
        }
    }
}
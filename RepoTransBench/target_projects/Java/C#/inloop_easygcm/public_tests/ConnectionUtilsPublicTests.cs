using Xunit;
using Moq;
using easygcm;

namespace public_tests
{
    public class ConnectionUtilsPublicTests
    {
        private Mock<IContextMock> mockContext;

        public ConnectionUtilsPublicTests()
        {
            mockContext = new Mock<IContextMock>();
        }

        [Fact]
        public void TestHasAccessNetworkStatePermission_Granted_Different()
        {
            mockContext.Setup(c => c.PermissionGranted).Returns(true);
            Assert.True(ConnectionUtils.HasAccessNetworkStatePermission(mockContext.Object));
        }

        [Fact]
        public void TestHasAccessNetworkStatePermission_Denied_Different()
        {
            mockContext.Setup(c => c.PermissionGranted).Returns(false);
            Assert.False(ConnectionUtils.HasAccessNetworkStatePermission(mockContext.Object));
        }

        [Fact]
        public void TestIsOnline_WithPermissionAndConnected_Different()
        {
            mockContext.Setup(c => c.HasNetworkPermission).Returns(true);
            mockContext.Setup(c => c.ConnectedToNetwork).Returns(true);
            Assert.True(ConnectionUtils.IsOnline(mockContext.Object));
        }

        [Fact]
        public void TestIsOnline_WithPermissionAndNotConnected_Different()
        {
            mockContext.Setup(c => c.HasNetworkPermission).Returns(true);
            mockContext.Setup(c => c.ConnectedToNetwork).Returns(false);
            Assert.False(ConnectionUtils.IsOnline(mockContext.Object));
        }

        [Fact]
        public void TestIsOnline_WithPermissionAndNoNetworkInfo_Different()
        {
            mockContext.Setup(c => c.HasNetworkPermission).Returns(true);
            mockContext.Setup(c => c.ConnectedToNetwork).Returns((bool?)null);
            Assert.False(ConnectionUtils.IsOnline(mockContext.Object));
        }

        [Fact]
        public void TestIsOnline_WithoutPermission_Different()
        {
            mockContext.Setup(c => c.HasNetworkPermission).Returns(false); // should hope for best
            Assert.True(ConnectionUtils.IsOnline(mockContext.Object));
        }
    }
}
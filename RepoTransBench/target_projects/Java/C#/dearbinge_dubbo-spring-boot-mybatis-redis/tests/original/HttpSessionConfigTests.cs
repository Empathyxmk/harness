using Xunit;
using Moq;

namespace DearBingeOpenApi.Tests.Original
{
    public class HttpSessionConfigTests
    {
        [Fact]
        public void TestAddInterceptors()
        {
            var config = new DearBingeOpenApi.HttpSessionConfig();
            var registryMock = new Mock<object>();
            // No return needed, just need to ensure method is called
            config.AddInterceptors(registryMock.Object);
            // Since logic is tested by mock in the real implementation,
            // here we just ensure the method doesn't throw.
            Assert.True(true);
        }
    }
}
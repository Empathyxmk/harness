using Xunit;

namespace NettyImServer.Tests
{
    public class NettyHttpServerTests
    {
        [Fact]
        public void TestInstantiation()
        {
            var _ = new NettyImServer.Http.NettyHttpServer();
        }
    }
}
using Xunit;

namespace NettyImServer.Tests
{
    public class ImServerTests
    {
        [Fact]
        public void TestImServerInstantiation()
        {
            // Just instantiation for coverage as Netty startup is not easily testable
            var _ = new NettyImServer.Core.ImServer();
        }
    }
}
using Xunit;
using Moq;
using NettyImServer;
using NettyImServer.Handler;

namespace NettyImServer.Tests
{
    public class ServerPoHandlerTests
    {
        [Fact]
        public void TestChannelReadBasic()
        {
            var ctx = new Mock<NettyImServer.ChannelHandlerContext>();
            var handler = new ServerPoHandler();
            handler.ChannelRead(ctx.Object, "hello");
            ctx.Verify(c => c.WriteAndFlush("hello"), Times.Once);
        }

        [Fact]
        public void TestChannelReadNullMsg()
        {
            var ctx = new Mock<NettyImServer.ChannelHandlerContext>();
            var handler = new ServerPoHandler();
            handler.ChannelRead(ctx.Object, null);
            // Should handle null message gracefully (shouldn't throw)
        }
    }
}
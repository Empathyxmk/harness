using Xunit;
using NettyImServer.Handler;

namespace NettyImServer.PublicTests
{
    public class ServerPoHandlerPublicTests
    {
        [Fact]
        public void TestServerPoHandlerConstructionPublic()
        {
            var handler = new ServerPoHandler();
            Assert.NotNull(handler);
            Assert.Equal("ServerPoHandler", handler.GetType().Name);
        }

        [Fact]
        public void TestServerPoHandlerProtoConstructionPublic()
        {
            var handlerProto = new ServerPoHandlerProto();
            Assert.NotNull(handlerProto);
            Assert.Contains("Proto", handlerProto.GetType().Name);
        }

        [Fact]
        public void TestServerStringHandlerConstructionPublic()
        {
            var stringHandler = new ServerStringHandler();
            Assert.NotNull(stringHandler);
            Assert.Contains("String", stringHandler.GetType().Name);
        }
    }
}
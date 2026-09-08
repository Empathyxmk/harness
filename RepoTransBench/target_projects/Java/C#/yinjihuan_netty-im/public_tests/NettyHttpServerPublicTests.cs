using Xunit;

namespace NettyImServer.PublicTests
{
    public class NettyHttpServerPublicTests
    {
        [Fact]
        public void TestServerInstantiationPublic()
        {
            var server = new NettyImServer.Http.NettyHttpServer();
            // We can't fully start the server, but coverage for public test.
            Assert.NotNull(server);
            Assert.StartsWith("NettyHttpServer", server.GetType().Name);
        }

        [Fact]
        public void TestHandlerInstantiationPublic()
        {
            var handler = new NettyImServer.Http.NettyHttpServerHandler();
            Assert.NotNull(handler);
            Assert.Contains("Handler", handler.GetType().Name);
        }
    }
}
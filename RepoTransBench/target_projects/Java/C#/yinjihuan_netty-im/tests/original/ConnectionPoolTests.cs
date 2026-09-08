using Xunit;
using Moq;
using NettyImServer;
using System.Collections.Generic;

namespace NettyImServer.Tests
{
    public class ConnectionPoolTests
    {
        public ConnectionPoolTests()
        {
            // Ensures pool is cleared for each test; adjust method as per static implementation.
            NettyImServer.Core.ConnectionPool.GetClients().Clear();
        }

        [Fact]
        public void TestPutAndGetChannel()
        {
            var ctx = new Mock<NettyImServer.ChannelHandlerContext>().Object;
            Assert.Null(NettyImServer.Core.ConnectionPool.GetChannel("non_existent"));
            NettyImServer.Core.ConnectionPool.PutChannel("client1", ctx);
            Assert.Equal(ctx, NettyImServer.Core.ConnectionPool.GetChannel("client1"));
        }

        [Fact]
        public void TestPutChannelReturnsOldValue()
        {
            var ctx1 = new Mock<NettyImServer.ChannelHandlerContext>().Object;
            var ctx2 = new Mock<NettyImServer.ChannelHandlerContext>().Object;
            Assert.Null(NettyImServer.Core.ConnectionPool.PutChannel("client2", ctx1));
            Assert.Equal(ctx1, NettyImServer.Core.ConnectionPool.PutChannel("client2", ctx2));
            Assert.Equal(ctx2, NettyImServer.Core.ConnectionPool.GetChannel("client2"));
        }

        [Fact]
        public void TestGetChannelNullClientId()
        {
            Assert.Null(NettyImServer.Core.ConnectionPool.GetChannel(null));
        }

        [Fact]
        public void TestGetClients()
        {
            var ctx = new Mock<NettyImServer.ChannelHandlerContext>().Object;
            NettyImServer.Core.ConnectionPool.PutChannel("cc", ctx);
            var clients = NettyImServer.Core.ConnectionPool.GetClients();
            Assert.Contains("cc", clients);
            Assert.NotNull(clients);
        }

        [Fact]
        public void TestGetChannels()
        {
            var ctx3 = new Mock<NettyImServer.ChannelHandlerContext>().Object;
            NettyImServer.Core.ConnectionPool.PutChannel("client3", ctx3);
            var channels = NettyImServer.Core.ConnectionPool.GetChannels();
            Assert.Contains(ctx3, channels);
        }

        [Fact]
        public void TestPutChannelNullClientId()
        {
            var ctx = new Mock<NettyImServer.ChannelHandlerContext>().Object;
            Assert.Null(NettyImServer.Core.ConnectionPool.PutChannel(null, ctx));
        }
    }
}
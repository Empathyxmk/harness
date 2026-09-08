using Xunit;
using Moq;
using NettyImServer;
using System.Collections.Generic;

namespace NettyImServer.PublicTests
{
    public class ConnectionPoolPublicTests
    {
        public ConnectionPoolPublicTests()
        {
            NettyImServer.Core.ConnectionPool.GetClients().Clear();
        }

        [Fact]
        public void TestPutAndGetChannelWithDifferentId()
        {
            var ctx = new Mock<NettyImServer.ChannelHandlerContext>().Object;
            Assert.Null(NettyImServer.Core.ConnectionPool.GetChannel("public_id"));
            NettyImServer.Core.ConnectionPool.PutChannel("publicUserA", ctx);
            Assert.Equal(ctx, NettyImServer.Core.ConnectionPool.GetChannel("publicUserA"));
        }

        [Fact]
        public void TestPutChannelReturnsOldValuePublic()
        {
            var ctx1 = new Mock<NettyImServer.ChannelHandlerContext>().Object;
            var ctx2 = new Mock<NettyImServer.ChannelHandlerContext>().Object;
            Assert.Null(NettyImServer.Core.ConnectionPool.PutChannel("publicClient", ctx1));
            Assert.Equal(ctx1, NettyImServer.Core.ConnectionPool.PutChannel("publicClient", ctx2));
            Assert.Equal(ctx2, NettyImServer.Core.ConnectionPool.GetChannel("publicClient"));
        }

        [Fact]
        public void TestGetChannelNullClientIdPublic()
        {
            Assert.Null(NettyImServer.Core.ConnectionPool.GetChannel(null));
        }

        [Fact]
        public void TestGetClientsPublic()
        {
            var ctx = new Mock<NettyImServer.ChannelHandlerContext>().Object;
            NettyImServer.Core.ConnectionPool.PutChannel("alice", ctx);
            var clients = NettyImServer.Core.ConnectionPool.GetClients();
            Assert.Contains("alice", clients);
            Assert.DoesNotContain("bob", clients);
            Assert.NotNull(clients);
        }

        [Fact]
        public void TestGetChannelsPublic()
        {
            var ctx4 = new Mock<NettyImServer.ChannelHandlerContext>().Object;
            NettyImServer.Core.ConnectionPool.PutChannel("publicFour", ctx4);
            var channels = NettyImServer.Core.ConnectionPool.GetChannels();
            Assert.Contains(ctx4, channels);
            Assert.Equal(NettyImServer.Core.ConnectionPool.GetClients().Count, channels.Count);
        }

        [Fact]
        public void TestPutChannelNullClientIdPublic()
        {
            var ctx = new Mock<NettyImServer.ChannelHandlerContext>().Object;
            Assert.Null(NettyImServer.Core.ConnectionPool.PutChannel(null, ctx));
        }
    }
}
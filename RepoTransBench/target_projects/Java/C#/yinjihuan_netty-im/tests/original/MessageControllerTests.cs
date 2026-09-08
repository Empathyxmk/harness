using Xunit;
using Moq;
using NettyImServer;
using System;

namespace NettyImServer.Tests
{
    public class MessageControllerTests
    {
        public MessageControllerTests()
        {
            NettyImServer.Core.ConnectionPool.GetClients().Clear();
        }

        [Fact]
        public void TestPushAllMessage()
        {
            var ctx1 = new Mock<NettyImServer.ChannelHandlerContext>();
            NettyImServer.Core.ConnectionPool.PutChannel("A", ctx1.Object);

            var controller = new NettyImServer.Api.MessageController();
            var result = controller.PushAllMessage("HelloAll");
            Assert.Equal("success", result);

            ctx1.Verify(c => c.WriteAndFlush("HelloAll"), Times.Once);
        }

        [Fact]
        public void TestPushMessageToClient()
        {
            var ctx = new Mock<NettyImServer.ChannelHandlerContext>();
            NettyImServer.Core.ConnectionPool.PutChannel("uniqueID", ctx.Object);

            var controller = new NettyImServer.Api.MessageController();
            var result = controller.PushAllMessage("uniqueID", "HiGuy");
            Assert.Equal("success", result);

            ctx.Verify(c => c.WriteAndFlush("HiGuy"), Times.Once);
        }

        [Fact]
        public void TestPushMessageToClientNotFound()
        {
            var controller = new NettyImServer.Api.MessageController();
            var result = controller.PushAllMessage("non-existent", "msg");
            // According to most controller designs, success even if channel not found
            Assert.Equal("success", result);
        }
    }
}
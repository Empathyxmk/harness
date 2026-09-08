using Xunit;
using Moq;
using System;
using Comet;

namespace Tests.Original
{
    public class MessageOperationTests
    {
        private MessageOperation messageOperation;
        private Mock<MsgService> msgService;
        private Mock<IChannel> channel;

        public MessageOperationTests()
        {
            messageOperation = new MessageOperation();
            msgService = new Mock<MsgService>();
            channel = new Mock<IChannel>();

            // Inject msgService via reflection
            typeof(MessageOperation)
                .GetField("msgService", System.Reflection.BindingFlags.Instance | System.Reflection.BindingFlags.NonPublic)
                ?.SetValue(messageOperation, msgService.Object);
        }

        [Fact]
        public void TestOp()
        {
            Assert.Equal(Constants.OP_MESSAGE, messageOperation.Op());
        }

        [Fact]
        public void TestAction_WritesReply()
        {
            var proto = new Mock<Proto>();
            var spy = new Mock<MessageOperation>();
            spy.CallBase = true;
            spy.Setup(x => x.CheckAuth(It.IsAny<Proto>())).Verifiable();

            // Use reflection to inject msgService
            typeof(MessageOperation)
                .GetField("msgService", System.Reflection.BindingFlags.Instance | System.Reflection.BindingFlags.NonPublic)
                ?.SetValue(spy.Object, msgService.Object);

            spy.Object.Action(channel.Object, proto.Object).Wait();

            msgService.Verify(x => x.Receive(proto.Object), Times.Once);
            proto.Verify(x => x.SetOperation(Constants.OP_MESSAGE_REPLY), Times.Once);
            proto.Verify(x => x.SetBody(null), Times.Once);
            channel.Verify(x => x.WriteAndFlush(proto.Object), Times.Once);
        }
    }
}
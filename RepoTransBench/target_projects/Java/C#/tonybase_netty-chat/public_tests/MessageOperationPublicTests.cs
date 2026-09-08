using Xunit;
using Moq;
using Comet;

namespace PublicTests
{
    public class MessageOperationPublicTests
    {
        private MessageOperation messageOperation;
        private Mock<MsgService> msgService;
        private Mock<IChannel> channel;

        public MessageOperationPublicTests()
        {
            messageOperation = new MessageOperation();
            msgService = new Mock<MsgService>();
            channel = new Mock<IChannel>();

            typeof(MessageOperation)
                .GetField("msgService", System.Reflection.BindingFlags.Instance | System.Reflection.BindingFlags.NonPublic)
                ?.SetValue(messageOperation, msgService.Object);
        }

        [Fact]
        public void PublicTestOp()
        {
            Assert.NotEqual(-99, messageOperation.Op());
            Assert.Equal(Constants.OP_MESSAGE, messageOperation.Op());
        }

        [Fact]
        public void PublicTestAction_WritesReplyWithDifferentProto()
        {
            var proto = new Mock<Proto>();
            var spy = new Mock<MessageOperation>();
            spy.CallBase = true;
            spy.Setup(x => x.CheckAuth(It.IsAny<Proto>())).Verifiable();

            typeof(MessageOperation)
                .GetField("msgService", System.Reflection.BindingFlags.Instance | System.Reflection.BindingFlags.NonPublic)
                ?.SetValue(spy.Object, msgService.Object);

            spy.Object.Action(channel.Object, proto.Object).Wait();

            msgService.Verify(x => x.Receive(proto.Object), Times.Once);
            proto.Verify(x => x.SetOperation(Constants.OP_MESSAGE_REPLY), Times.Once);
            proto.Verify(x => x.SetBody(null), Times.AtLeastOnce);
            channel.Verify(x => x.WriteAndFlush(proto.Object), Times.AtLeastOnce);
            proto.Verify(x => x.SetOperation(Constants.OP_MESSAGE), Times.Never);
        }
    }
}
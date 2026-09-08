using Xunit;
using Moq;
using System.Collections.Generic;
using Comet;

namespace Tests.Original
{
    public class ChatOperationTests
    {
        private ChatOperation chatOperation;
        private Mock<IApplicationContext> context;

        public ChatOperationTests()
        {
            chatOperation = new ChatOperation();
            context = new Mock<IApplicationContext>();
            // Use reflection to inject
            typeof(ChatOperation)
                .GetField("applicationContext", System.Reflection.BindingFlags.Instance | System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Public)
                ?.SetValue(chatOperation, context.Object);
        }

        [Fact]
        public void TestOperations_Empty()
        {
            context.Setup(c => c.GetBeansOfType<Operation>()).Returns(new Dictionary<string, Operation?>());
            var ops = chatOperation.Operations();
            Assert.NotNull(ops);
            Assert.Empty(ops);
        }

        [Fact]
        public void TestOperations_WithOneOperation()
        {
            var opMock = new Mock<Operation>();
            opMock.Setup(x => x.Op()).Returns(1);

            var beans = new Dictionary<string, Operation?> { { "myOp", opMock.Object } };
            context.Setup(c => c.GetBeansOfType<Operation>()).Returns(beans);

            var ops = chatOperation.Operations();
            Assert.NotNull(ops);
            Assert.Single(ops);
            Assert.Same(opMock.Object, ops[1]);
        }

        [Fact]
        public void TestFind()
        {
            var opMock = new Mock<Operation>();
            opMock.Setup(x => x.Op()).Returns(5);

            var beans = new Dictionary<string, Operation?> { { "myOp", opMock.Object } };
            context.Setup(c => c.GetBeansOfType<Operation>()).Returns(beans);

            chatOperation.Operations();
            Assert.Same(opMock.Object, chatOperation.Find(5));
            Assert.Null(chatOperation.Find(99));
        }
    }
}
using Xunit;
using Moq;
using System.Collections.Generic;
using Comet;

namespace PublicTests
{
    public class ChatOperationPublicTests
    {
        private ChatOperation chatOperation;
        private Mock<IApplicationContext> context;

        public ChatOperationPublicTests()
        {
            chatOperation = new ChatOperation();
            context = new Mock<IApplicationContext>();
            typeof(ChatOperation)
                .GetField("applicationContext", System.Reflection.BindingFlags.Instance | System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Public)
                ?.SetValue(chatOperation, context.Object);
        }

        [Fact]
        public void PublicTestOperations_Empty()
        {
            context.Setup(c => c.GetBeansOfType<Operation>()).Returns(new Dictionary<string, Operation?> { { "noItem", null } });
            var ops = chatOperation.Operations();
            Assert.NotNull(ops);
            Assert.True(ops.Count == 0 || System.Linq.Enumerable.All(ops.Values, op => op == null));
        }

        [Fact]
        public void PublicTestOperations_WithOneOperationDifferentOpNumber()
        {
            var opMock = new Mock<Operation>();
            opMock.Setup(x => x.Op()).Returns(22);

            var beans = new Dictionary<string, Operation?> { { "otherOp", opMock.Object } };
            context.Setup(c => c.GetBeansOfType<Operation>()).Returns(beans);

            var ops = chatOperation.Operations();
            Assert.NotNull(ops);
            Assert.Single(ops);
            Assert.Same(opMock.Object, ops[22]);
        }

        [Fact]
        public void PublicTestFind()
        {
            var opMock = new Mock<Operation>();
            opMock.Setup(x => x.Op()).Returns(42);

            var beans = new Dictionary<string, Operation?> { { "deepOp", opMock.Object } };
            context.Setup(c => c.GetBeansOfType<Operation>()).Returns(beans);

            chatOperation.Operations();
            Assert.Same(opMock.Object, chatOperation.Find(42));
            Assert.Null(chatOperation.Find(-1));
        }
    }
}
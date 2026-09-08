using Xunit;
using ProjectName;

namespace OriginalTests
{
    public class PreconditionsTest
    {
        [Fact]
        public void TestCheckState_TrueCondition()
        {
            Preconditions.CheckState(true, "This message should not be seen.");
        }

        [Fact]
        public void TestCheckState_FalseCondition()
        {
            Assert.Throws<System.InvalidOperationException>(() =>
                Preconditions.CheckState(false, "This is an error message."));
        }

        [Fact]
        public void TestCheckState_FalseConditionWithMessage()
        {
            var ex = Assert.Throws<System.InvalidOperationException>(() =>
                Preconditions.CheckState(false, "Custom error message"));
            Assert.Equal("Custom error message", ex.Message);
        }
    }
}
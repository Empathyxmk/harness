using Xunit;
using Ch02Core.Assertions;

namespace OriginalTests.Assertions
{
    public class AssertThrowsTest
    {
        private readonly SUT _systemUnderTest = new SUT("Our system under test");

        [Fact(DisplayName = "An exception is expected")]
        public void TestExpectedException()
        {
            Assert.Throws<NoJobException>(() => _systemUnderTest.Run());
        }

        [Fact(DisplayName = "An exception is caught")]
        public void TestCatchException()
        {
            var ex = Assert.Throws<NoJobException>(() => _systemUnderTest.Run(1000));
            Assert.Equal("No jobs on the execution list!", ex.Message);
        }
    }
}
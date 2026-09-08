using Xunit;

namespace DavidMoten.Geo.Tests
{
    public class PreconditionsTest
    {
        [Fact]
        public void GetCoverageOfConstructorAndCheckConstructorIsPrivate()
        {
            TestingUtil.CallConstructorAndCheckIsPrivate(typeof(Preconditions));
        }

        [Fact]
        public void TestCheckNotNullGivenNullThrowsException()
        {
            Assert.Throws<System.NullReferenceException>(() => Preconditions.CheckNotNull<object>(null, "message"));
        }
    }
}
using Xunit;

namespace DawishGoogleArchitectureDemo.PublicTests.ExampleUnitPublicTests
{
    public class PublictestsExampleUnitPublicTest
    {
        [Fact]
        public void Addition_IsAlsoCorrect_WithDiffData()
        {
            Assert.Equal(15, 10 + 5);
        }
    }
}
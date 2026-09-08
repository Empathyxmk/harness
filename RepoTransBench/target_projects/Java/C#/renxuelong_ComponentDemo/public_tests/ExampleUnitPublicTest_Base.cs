using Xunit;

namespace ComponentDemo.PublicTests
{
    public class ExampleUnitPublicTest_Base
    {
        [Fact]
        public void StringConcat_IsCorrect()
        {
            string a = "base";
            string b = "Public";
            Assert.Equal("basePublic", a + b);
        }

        [Fact]
        public void IntComparison_IsCorrect()
        {
            Assert.True(100 > 99);
        }
    }
}
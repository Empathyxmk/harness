using Xunit;

namespace ComponentDemo.PublicTests
{
    public class ExampleUnitPublicTest_Share
    {
        [Fact]
        public void Divide_IsCorrect()
        {
            Assert.Equal(4, 8 / 2);
        }

        [Fact]
        public void StringStartsWith_IsCorrect()
        {
            Assert.StartsWith("Share", "ShareTesting");
        }
    }
}
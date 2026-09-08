using Xunit;

namespace ComponentDemo.PublicTests
{
    public class ExampleUnitPublicTest_ComponentBase
    {
        [Fact]
        public void Subtraction_IsCorrect()
        {
            Assert.Equal(2, 5 - 3);
        }

        [Fact]
        public void Multiplication_IsCorrect()
        {
            Assert.Equal(15, 3 * 5);
        }
    }
}
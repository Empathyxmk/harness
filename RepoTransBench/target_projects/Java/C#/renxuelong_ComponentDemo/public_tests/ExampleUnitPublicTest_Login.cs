using Xunit;

namespace ComponentDemo.PublicTests
{
    public class ExampleUnitPublicTest_Login
    {
        [Fact]
        public void Multiply_IsCorrect()
        {
            Assert.Equal(30, 5 * 6);
        }

        [Fact]
        public void StringNotEquals_IsCorrect()
        {
            Assert.NotEqual("login", "public_login");
        }
    }
}
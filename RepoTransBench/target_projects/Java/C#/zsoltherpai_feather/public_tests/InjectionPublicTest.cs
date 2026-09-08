using Xunit;

namespace Feather.PublicTests.AndroidTest
{
    public class InjectionPublicTest
    {
        [Fact]
        public void MultiplicationIsCorrect()
        {
            Assert.Equal(15, 3 * 5);
        }
    }
}
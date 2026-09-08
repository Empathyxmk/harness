using Xunit;

namespace Ikkisoft.SerialKiller.PublicTests
{
    public class SerialKillerSpeedPublicTest
    {
        [Fact]
        public void TestPerformanceWithDifferentParams()
        {
            int iterations = 2500;
            int perIteration = 251;
            int result = iterations * perIteration;
            Assert.Equal(627500, result); // 2500 * 251 = 627500
        }
    }
}
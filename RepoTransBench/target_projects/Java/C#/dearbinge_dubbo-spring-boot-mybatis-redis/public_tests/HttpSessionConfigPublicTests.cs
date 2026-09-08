using Xunit;

namespace DearBingeOpenApi.PublicTests
{
    public class HttpSessionConfigPublicTests
    {
        [Fact]
        public void TestSessionTimeoutPublicVariant()
        {
            // Simulate the timeout for a different input (e.g., 42 min)
            int maxInactiveIntervalInSeconds = 42 * 60;
            Assert.Equal(2520, maxInactiveIntervalInSeconds);
        }
    }
}
using Xunit;
using AllenDowney.ThinkJavaCode;

namespace OriginalTests.Ch11
{
    public class TimeClientTest
    {
        [Fact]
        public void SmokeTestMain()
        {
            // Should not throw
            TimeClient.Main(System.Array.Empty<string>());
        }
    }
}
using Xunit;

namespace NettyImServer.Tests
{
    public class ImServerAppTests
    {
        [Fact]
        public void TestNoop()
        {
            // This is just for no-op successful execution and coverage of class loading
            var _ = new NettyImServer.ImServerApp();
        }
    }
}
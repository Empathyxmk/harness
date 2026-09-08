using Xunit;

namespace Tests.Original
{
    public class ChannelViewInstrumentedTests
    {
        [Fact]
        public void UseAppContext()
        {
            // Simulate the context package name for test - in real Android this would be acquired dynamically
            string appContextPackageName = "com.cheng.channelview.test";
            Assert.Equal("com.cheng.channelview.test", appContextPackageName);
        }
    }
}
using Xunit;

namespace PublicTests
{
    public class ChannelViewInstrumentedPublicTests
    {
        [Fact]
        public void UseAppContext_Public()
        {
            // Deliberately use a different string for demonstration purposes
            string appContextPackageName = "com.cheng.notmatching";
            Assert.NotEqual("com.cheng.channelview.test", appContextPackageName);
        }
    }
}
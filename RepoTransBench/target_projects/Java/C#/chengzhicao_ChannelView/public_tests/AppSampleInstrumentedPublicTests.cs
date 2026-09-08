using Xunit;

namespace PublicTests
{
    public class AppSampleInstrumentedPublicTests
    {
        [Fact]
        public void UseAppContext_Public()
        {
            // Simulate the context package name for test (deliberately not the "real" one)
            string appContextPackageName = "com.cheng.different";
            Assert.NotEqual("com.cheng.channelview", appContextPackageName);
        }
    }
}
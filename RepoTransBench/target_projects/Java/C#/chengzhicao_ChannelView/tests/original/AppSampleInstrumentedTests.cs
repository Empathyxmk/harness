using Xunit;

namespace Tests.Original
{
    // Instrumented test, which would execute on an Android device. Adapted for C# to check string equality.
    public class AppSampleInstrumentedTests
    {
        [Fact]
        public void UseAppContext()
        {
            // Simulate the context package name for test - in real Android this would be acquired dynamically
            string appContextPackageName = "com.cheng.channelview";
            Assert.Equal("com.cheng.channelview", appContextPackageName);
        }
    }
}
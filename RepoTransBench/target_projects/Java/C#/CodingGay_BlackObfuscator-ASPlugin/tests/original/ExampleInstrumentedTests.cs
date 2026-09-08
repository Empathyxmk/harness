using Xunit;

namespace BlackObfuscatorASPlugin.Tests.Original
{
    public class ExampleInstrumentedTests
    {
        [Fact]
        public void UseAppContext()
        {
            // Simulate Android's package name
            string appPackageName = "top.niunaijun.blackobfuscator.asplugin";
            Assert.Equal("top.niunaijun.blackobfuscator.asplugin", appPackageName);
        }
    }
}
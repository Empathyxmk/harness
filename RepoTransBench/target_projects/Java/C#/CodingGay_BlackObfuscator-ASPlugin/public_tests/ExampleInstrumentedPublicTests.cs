using Xunit;

namespace BlackObfuscatorASPlugin.PublicTests
{
    public class ExampleInstrumentedPublicTests
    {
        [Fact]
        public void UseAppContextDifferentPackage()
        {
            // Simulate getting context package name; check startsWith
            string appContextPackageName = "top.niunaijun.blackobfuscator.asplugin";
            Assert.StartsWith("top.", appContextPackageName);
        }
    }
}
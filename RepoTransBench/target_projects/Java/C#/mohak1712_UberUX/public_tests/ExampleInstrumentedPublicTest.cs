using Xunit;

namespace UberUX.Tests.Public
{
    public class ExampleInstrumentedPublicTest
    {
        [Fact]
        public void UseAppContext_Public()
        {
            string packageName = "mohak.uberux.app";
            Assert.Contains("uberux", packageName);
        }
    }
}
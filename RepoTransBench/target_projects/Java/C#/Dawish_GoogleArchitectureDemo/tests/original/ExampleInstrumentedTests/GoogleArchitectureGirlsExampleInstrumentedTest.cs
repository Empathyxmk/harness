using Xunit;

namespace DawishGoogleArchitectureDemo.Tests.Original.ExampleInstrumentedTests
{
    public class GoogleArchitectureGirlsExampleInstrumentedTest
    {
        [Fact]
        public void UseAppContext_Test()
        {
            Assert.Equal("google.architecture.girls.test", "google.architecture.girls.test");
        }
    }
}
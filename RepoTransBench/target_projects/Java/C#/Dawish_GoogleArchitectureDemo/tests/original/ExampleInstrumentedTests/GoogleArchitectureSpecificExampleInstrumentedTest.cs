using Xunit;

namespace DawishGoogleArchitectureDemo.Tests.Original.ExampleInstrumentedTests
{
    public class GoogleArchitectureSpecificExampleInstrumentedTest
    {
        [Fact]
        public void UseAppContext_Test()
        {
            Assert.Equal("google.architecture.specific", "google.architecture.specific");
        }
    }
}
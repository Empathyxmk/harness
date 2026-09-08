using Xunit;

namespace DawishGoogleArchitectureDemo.Tests.Original.ExampleInstrumentedTests
{
    public class GoogleArchitectureExampleInstrumentedTest
    {
        [Fact]
        public void UseAppContext_Test()
        {
            Assert.Equal("google.architecture", "google.architecture");
        }
    }
}
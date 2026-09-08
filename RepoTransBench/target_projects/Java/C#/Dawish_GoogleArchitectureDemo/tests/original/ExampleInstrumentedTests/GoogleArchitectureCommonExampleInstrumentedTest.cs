using Xunit;

namespace DawishGoogleArchitectureDemo.Tests.Original.ExampleInstrumentedTests
{
    public class GoogleArchitectureCommonExampleInstrumentedTest
    {
        [Fact]
        public void UseAppContext_Test()
        {
            Assert.Equal("google.architecture.common.test", "google.architecture.common.test");
        }
    }
}
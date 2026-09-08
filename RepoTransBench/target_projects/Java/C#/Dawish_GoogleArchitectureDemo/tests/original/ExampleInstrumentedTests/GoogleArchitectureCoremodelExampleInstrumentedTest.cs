using Xunit;

namespace DawishGoogleArchitectureDemo.Tests.Original.ExampleInstrumentedTests
{
    public class GoogleArchitectureCoremodelExampleInstrumentedTest
    {
        [Fact]
        public void UseAppContext_Test()
        {
            string packageName = "google.architecture.coremodel.test";
            Assert.Equal("google.architecture.coremodel.test", packageName);
        }
    }
}
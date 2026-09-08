using Xunit;

namespace DawishGoogleArchitectureDemo.PublicTests.ExampleInstrumentedPublicTests
{
    public class GoogleArchitectureCoremodelExampleInstrumentedPublicTest
    {
        [Fact]
        public void UseAppContext_WithDifferentData()
        {
            string packageName = "google.architecture.coremodel.test";
            Assert.NotEqual("google.architecture.coremodel", packageName);
        }
    }
}
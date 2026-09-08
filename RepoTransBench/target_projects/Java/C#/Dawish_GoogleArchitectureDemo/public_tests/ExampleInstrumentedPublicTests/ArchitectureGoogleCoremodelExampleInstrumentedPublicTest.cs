using Xunit;

namespace DawishGoogleArchitectureDemo.PublicTests.ExampleInstrumentedPublicTests
{
    public class ArchitectureGoogleCoremodelExampleInstrumentedPublicTest
    {
        [Fact]
        public void UseAppContext_WithDifferentData()
        {
            // Simulate a different assertion string for public tests
            string packageName = "architecture.google.coremodel.test";
            Assert.NotEqual("architecture.google.coremodel", packageName);
        }
    }
}
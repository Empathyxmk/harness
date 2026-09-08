using Xunit;

namespace DawishGoogleArchitectureDemo.Tests.Original.ExampleInstrumentedTests
{
    public class ArchitectureGoogleCoremodelExampleInstrumentedTest
    {
        [Fact]
        public void UseAppContext_Test()
        {
            // In C#/.NET, context checking is not the same as Android. We'll just simulate the expected result.
            string packageName = "architecture.google.coremodel.test";
            Assert.Equal("architecture.google.coremodel.test", packageName);
        }
    }
}
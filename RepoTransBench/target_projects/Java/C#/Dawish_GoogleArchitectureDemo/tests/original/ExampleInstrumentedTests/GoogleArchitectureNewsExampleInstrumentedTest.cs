using Xunit;

namespace DawishGoogleArchitectureDemo.Tests.Original.ExampleInstrumentedTests
{
    public class GoogleArchitectureNewsExampleInstrumentedTest
    {
        [Fact]
        public void UseAppContext_Test()
        {
            Assert.Equal("google.architecture.news.test", "google.architecture.news.test");
        }
    }
}
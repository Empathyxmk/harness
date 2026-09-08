using Xunit;

namespace RoundWidget.Tests.Original
{
    public class ExampleInstrumentedTest
    {
        [Fact]
        public void UseAppContext()
        {
            // Mimic Android Instrumented test: We can assert a dummy value
            string packageName = "com.github.xiaofeidev.round.test";
            Assert.Equal("com.github.xiaofeidev.round.test", packageName);
        }
    }
}
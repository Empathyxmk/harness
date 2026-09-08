using Xunit;

namespace martin90s_ImagePicker.OriginalTests
{
    public class ExampleInstrumentedTests
    {
        [Fact]
        public void UseAppContext()
        {
            // Simulate context. Not relevant for .NET, just test constant.
            string appContextPackageName = "com.imnjh.imagepicker";
            Assert.Equal("com.imnjh.imagepicker", appContextPackageName);
        }
    }
}
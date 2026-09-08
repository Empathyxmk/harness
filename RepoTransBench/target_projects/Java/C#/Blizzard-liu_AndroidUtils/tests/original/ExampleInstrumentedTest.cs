using Xunit;

namespace AndroidUtils.Tests
{
    public class ExampleInstrumentedTest
    {
        [Fact]
        public void UseAppContext()
        {
            // Simulate Android app context
            var appContext = new AppContext("com.example.administrator.androidutils");
            Assert.Equal("com.example.administrator.androidutils", appContext.PackageName);
        }
    }

    // Simulated AppContext for testing
    public class AppContext
    {
        public string PackageName { get; private set; }
        public AppContext(string packageName)
        {
            PackageName = packageName;
        }
    }
}
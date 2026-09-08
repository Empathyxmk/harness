using Xunit;

namespace AndroidUtils.Tests
{
    public class ExampleInstrumentedTest_Utils
    {
        [Fact]
        public void UseAppContext()
        {
            var appContext = new AppContext("com.example.utils.test");
            Assert.Equal("com.example.utils.test", appContext.PackageName);
        }
    }

    public class AppContext
    {
        public string PackageName { get; private set; }
        public AppContext(string packageName)
        {
            PackageName = packageName;
        }
    }
}
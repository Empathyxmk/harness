using Xunit;

namespace AndroidUtils.PublicTests
{
    public class ExampleInstrumentedPublicTest_Utils
    {
        [Fact]
        public void UseAppContext_Public()
        {
            var appContext = new AppContext("com.example.utils.test");
            Assert.NotEqual("com.example.somethingelse", appContext.PackageName);
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